# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
import collections

import ipaddr
import netaddr

from neutronclient.common import exceptions as neutron_exc

from cloudferry.lib.base import exception
from cloudferry.lib.base.action import action
from cloudferry.lib.os.network import neutron
from cloudferry.lib.utils import log
from cloudferry.lib.utils import mapper
from cloudferry.lib.utils import proxy_client
from cloudferry.lib.utils import utils


LOG = log.getLogger(__name__)


class CheckNetworks(action.Action):
    """
    Check networks segmentation ID, subnets and floating IPs overlapping. Also
    check if VMs from SRC spawned in external networks directly.

    Returns list of all overlaps and prints it to the LOG. If this list is
    non-empty, raise exception (AbortMigrationError).

    It must be done before actual migration in the 'preparation' section.
    The action uses filtered search opts and must be run after 'act_get_filter'
    action.
    """

    def run(self, **kwargs):
        LOG.debug("Checking networks...")
        has_overlapping_resources = False
        has_invalid_resources = False

        src_net = self.src_cloud.resources[utils.NETWORK_RESOURCE]
        dst_net = self.dst_cloud.resources[utils.NETWORK_RESOURCE]
        src_compute = self.src_cloud.resources[utils.COMPUTE_RESOURCE]

        tenant_ids = kwargs.get('search_opts_tenant', {}).get('tenant_id')
        search_opts = kwargs.get('search_opts', {})

        LOG.debug("Retrieving Network information from Source cloud...")
        ports = src_net.get_ports_list()
        src_net_info = NetworkInfo(src_net.read_info(tenant_id=tenant_ids),
                                   ports)
        LOG.debug("Retrieving Network information from Destination cloud...")
        dst_net_info = NetworkInfo(dst_net.read_info())
        LOG.debug("Retrieving Compute information from Source cloud...")
        src_compute_info = ComputeInfo(src_compute, search_opts, tenant_ids)

        ext_net_map = mapper.Mapper('ext_network_map')

        # Check external networks mapping
        if ext_net_map:
            LOG.info("Check external networks mapping...")
            invalid_ext_net_ids = src_net_info.get_invalid_ext_net_ids(
                dst_net_info, ext_net_map)
            if invalid_ext_net_ids['src_nets'] or \
                    invalid_ext_net_ids['dst_nets']:
                invalid_src_nets = invalid_ext_net_ids['src_nets']
                invalid_dst_nets = invalid_ext_net_ids['dst_nets']
                invalid_nets_str = ""

                if invalid_src_nets:
                    invalid_nets_str = 'Source cloud:\n' + \
                                       '\n'.join(invalid_src_nets) + '\n'
                if invalid_dst_nets:
                    invalid_nets_str += 'Destination cloud:\n' + \
                                        '\n'.join(invalid_dst_nets) + '\n'

                LOG.error("External networks mapping file has non-existing "
                          "network UUIDs defined:\n%s\nPlease update '%s' "
                          "file with correct values and re-run networks "
                          "check.",
                          invalid_nets_str, self.cfg.migrate.ext_net_map)
                has_invalid_resources = True

        # Check networks' segmentation IDs overlap
        LOG.info("Check networks' segmentation IDs overlapping...")
        nets_overlapping_seg_ids = (src_net_info.get_overlapping_seg_ids(
            dst_net_info))
        if nets_overlapping_seg_ids:
            LOG.warning("Segmentation IDs for these networks in source cloud "
                        "WILL NOT BE KEPT regardless of options defined in "
                        "config, because networks with the same segmentation "
                        "IDs already exist in destination: %s.",
                        '\n'.join([n['src_net_id']
                                   for n in nets_overlapping_seg_ids]))

        # Check external subnets overlap
        LOG.info("Check external subnets overlapping...")
        overlapping_external_subnets = (
            src_net_info.get_overlapping_external_subnets(dst_net_info,
                                                          ext_net_map))
        if overlapping_external_subnets:
            pool_fmt = '"{pool}" pool of subnet "{snet_name}" ({snet_id})'
            fmt = "{src_pool} overlaps with {dst_pool}"
            overlapping_nets = []

            for snet in overlapping_external_subnets:
                overlapping_nets.append(
                    fmt.format(
                        src_pool=pool_fmt.format(
                            pool=snet['src_subnet']['allocation_pools'],
                            snet_name=snet['src_subnet']['name'],
                            snet_id=snet['src_subnet']['id']),
                        dst_pool=pool_fmt.format(
                            pool=snet['dst_subnet']['allocation_pools'],
                            snet_name=snet['dst_subnet']['name'],
                            snet_id=snet['dst_subnet']['id'],
                        )))

            message = ("Following external networks have overlapping "
                       "allocation pools in source and destination:\n{}.\nTo "
                       "resolve this:\n"
                       " 1. Manually change allocation pools in source or "
                       "destination networks to be identical;\n"
                       " 2. Use '[migrate] ext_net_map' external networks "
                       "mapping. Floating IPs will NOT BE KEPT in that "
                       "case.".format('\n'.join(overlapping_nets)))

            LOG.error(message)
            has_overlapping_resources = True

        # Check floating IPs overlap
        LOG.info("Check floating IPs overlapping...")
        floating_ips = src_net_info.list_overlapping_floating_ips(dst_net_info,
                                                                  ext_net_map)
        if floating_ips:
            LOG.error("Following floating IPs from source cloud already exist "
                      "in destination, but either tenant, or external "
                      "network doesn't match source cloud floating IP: %s\n"
                      "In order to resolve you'd need to either delete "
                      "floating IP from destination, or recreate floating "
                      "IP so that they match fully in source and destination.",
                      '\n'.join(floating_ips))
            has_overlapping_resources = True

        # Check busy physical networks on DST of FLAT network type
        LOG.info("Check busy physical networks for FLAT network type...")
        busy_flat_physnets = src_net_info.busy_flat_physnets(dst_net_info,
                                                             ext_net_map)
        if busy_flat_physnets:
            LOG.error("Flat network(s) allocated in different physical "
                      "network(s) exist in destination cloud:\n%s\nIn order "
                      "to resolve flat networks in the list must be "
                      "connected to the same physical network in source and "
                      "destination.",
                      '\n'.join([str(n) for n in busy_flat_physnets]))
            has_overlapping_resources = True

        # Check physical networks existence on DST for VLAN network type
        LOG.info("Check physical networks existence for VLAN network type...")
        dst_neutron_client = dst_net.neutron_client
        missing_vlan_physnets = src_net_info.missing_vlan_physnets(
            dst_net_info, dst_neutron_client, ext_net_map)
        if missing_vlan_physnets:
            LOG.error("Following physical networks are not present in "
                      "destination, but required by source cloud networks: "
                      "%s\nIn order to resolve make sure neutron has "
                      "required physical networks defined in config.",
                      '\n'.join(missing_vlan_physnets))

            has_overlapping_resources = True

        # Check VMs spawned directly in external network
        LOG.info("Check VMs spawned directly in external networks...")
        devices = src_net_info.get_devices_from_external_networks()
        vms_list = src_compute_info.list_vms_in_external_network(devices)
        if vms_list:
            LOG.warning('Following VMs are booted directly in external '
                        'network, which is not recommended: %s', vms_list)

        # Print LOG message with all overlapping stuff and abort migration
        if has_overlapping_resources or has_invalid_resources:
            raise exception.AbortMigrationError(
                "There is a number of overlapping/invalid network resources "
                "which require manual resolution. See error messages above "
                "for details.")


class ComputeInfo(object):
    def __init__(self, src_compute, search_opts, tenant_ids):
        self.instances = {s.id for s in src_compute.get_instances_list(
            search_opts, tenant_ids)}

    def list_vms_in_external_network(self, devices):
        """
        Get list of VMs IDs, that are spawned in external network directly.

        :param devices: List of devices which are connected to the external
                        networks
        :return list:
        """
        if not devices:
            LOG.debug('There are no any devices in external networks on the '
                      'SRC cloud. Finishing check.')
            return []

        return list(self.instances & devices)


class NetworkInfo(object):
    def __init__(self, info, ports=None):
        self.by_id = {}
        self.by_hash = collections.defaultdict()
        self.subnets = info['subnets']
        self.floating_ips = {}
        self.networks_info = info['networks']
        for net_map in self.networks_info:
            network = Network(net_map)
            self.by_id[network.id] = network
            self.by_hash[network.hash] = network
        for subnet in self.subnets:
            network = self.by_id[subnet['network_id']]
            network.add_subnet(subnet)
        for floating_ip_map in info['floating_ips']:
            floating_ip = FloatingIp(floating_ip_map)
            self.floating_ips[floating_ip.address] = floating_ip
        self.ports = ports

    def get_networks(self):
        return self.by_id.values()

    def get_network_by_segmentation_id(self, net_type, segmentation_id):
        """
        Get network by it's type and segmentation ID.

        :param net_type: Network type (f.e. gre, vlan, etc.)
        :param segmentation_id: Segmentation ID

        :result: Network instance, that fits with requirements
        """

        for net in self.get_networks():
            if net.network_type == net_type and net.seg_id == segmentation_id:
                return net

    def get_devices_from_external_networks(self):
        """
        Get list of devices which are connected to the external networks.

        :return list: List of ids of instances
        """

        networks_ids = {subnet['network_id'] for subnet in self.subnets
                        if subnet['external']}
        return {port['device_id'] for port in self.ports
                if port['network_id'] in networks_ids}

    def list_overlapping_floating_ips(self, dst_info, ext_net_map):
        """
        Get list of Floating IPs, that overlap with the DST.

        :param dst_info: NetworkInfo instance of DST cloud
        :param ext_net_map: External networks mapping dictionary. Format:
                        {<src_external_network>: <dst_external_network>, ...}
        """

        floating_ips_list = []

        for floating_ip in self.floating_ips.values():
            dst_floating_ip = dst_info.floating_ips.get(floating_ip.address)
            if not dst_floating_ip:
                LOG.debug("There is no such Floating IP on DST: '%s'. "
                          "Continue...", floating_ip.address)
                continue

            LOG.debug('Floating IP `%s` has been found on DST. Checking for '
                      'overlap...', floating_ip.address)

            if floating_ip.network_id in ext_net_map:
                LOG.debug("Floating IP '%s' is related to the external network"
                          " '%s', that specified in external networks mapping."
                          " Skipping floating IP...",
                          floating_ip.address, floating_ip.network_id)
                continue

            try:
                floating_ip.check_floating_ips_overlapping(dst_floating_ip)
            except exception.AbortMigrationError:
                floating_ips_list.append(floating_ip.address)

        return floating_ips_list

    def get_overlapping_external_subnets(self, dst_info, ext_net_map):
        """
        Get lists of subnets, that overlap with the DST.

        :param dst_info: NetworkInfo instance of DST cloud
        :param ext_net_map: External networks mapping dictionary. Format:
                        {<src_external_network>: <dst_external_network>, ...}

        :return list of dicts: Overlapping subnets in format:
                                [{'src_subnet': <src_subnet_id>,
                                'dst_subnet': <dst_subnet_id>}, ...]
        """

        src_ext_subnets = [snet for snet in self.subnets if snet['external']]
        dst_ext_subnets = [sub for sub in dst_info.subnets if sub['external']]

        overlapping_external_subnets = []

        for src_subnet in src_ext_subnets:
            for dst_subnet in dst_ext_subnets:
                LOG.debug("SRC subnet: '%s', DST subnet: '%s'",
                          src_subnet['id'], dst_subnet['id'])
                if src_subnet['res_hash'] == dst_subnet['res_hash']:
                    src_net = self.by_id[src_subnet['network_id']]
                    dst_net = dst_info.by_id[dst_subnet['network_id']]
                    if check_equal_networks(src_net, dst_net):
                        LOG.debug("We have the same subnet on DST by hash")
                        continue

                cidr_overlap = cidr_overlapping(src_subnet['cidr'],
                                                dst_subnet['cidr'])
                if not cidr_overlap:
                    LOG.debug("CIDRs do not overlap")
                    continue
                pools_overlap = allocation_pools_overlapping(
                    src_subnet['allocation_pools'],
                    dst_subnet['allocation_pools'])
                if not pools_overlap:
                    LOG.debug("Allocation pools do not overlap")
                    continue

                if src_subnet['network_id'] in ext_net_map:
                    LOG.debug("Subnet '%s' is related to the external network "
                              "'%s', that specified in external networks "
                              "mapping. Skipping subnet... ",
                              src_subnet['id'], src_subnet['network_id'])
                    continue

                overlap = {'src_subnet': src_subnet,
                           'dst_subnet': dst_subnet}
                LOG.debug("Allocation pool of subnet '%s' on SRC overlaps "
                          "with allocation pool of subnet '%s' on DST.",
                          src_subnet['id'], dst_subnet['id'])
                overlapping_external_subnets.append(overlap)

        return overlapping_external_subnets

    def get_overlapping_seg_ids(self, dst_info):
        """
        Get list of nets, that have overlapping segmentation IDs with the DST.

        :param dst_info: NetworkInfo instance of DST cloud

        :return: List of networks IDs with overlapping segmentation IDs.
        """

        dst_net_info = dst_info.networks_info
        dst_seg_ids = neutron.get_segmentation_ids_from_net_list(dst_net_info)
        nets_with_overlapping_seg_ids = []

        for network in self.get_networks():
            dst_net = dst_info.by_hash.get(network.hash)
            if dst_net and check_equal_networks(network, dst_net):
                # Current network matches with network on DST
                # Have the same networks on SRC and DST
                LOG.debug("SRC network '%s' and DST network '%s' are the same",
                          network.id, dst_net.id)
            else:
                # Current network does not match with any network on DST
                # Check Segmentation ID overlapping with DST
                LOG.debug("Check segmentation ID for SRC network: '%s'",
                          network.id)
                try:
                    network.check_segmentation_id_overlapping(dst_seg_ids)
                except exception.AbortMigrationError:
                    dst_network = dst_info.get_network_by_segmentation_id(
                        network.network_type, network.seg_id)
                    overlap = {'src_net_id': network.id,
                               'dst_net_id': dst_network.id}
                    nets_with_overlapping_seg_ids.append(overlap)

        return nets_with_overlapping_seg_ids

    def busy_flat_physnets(self, dst_info, ext_net_map):
        """
        Get list of busy physical networks for FLAT network type.

        :param dst_info: NetworkInfo instance of DST cloud
        :param ext_net_map: External networks mapping dictionary. Format:
                        {<src_external_network>: <dst_external_network>, ...}

        :return: List of busy FLAT physnets.
        """

        dst_flat_physnets = [net.physnet for net in dst_info.get_networks() if
                             net.network_type == 'flat']
        busy_flat_physnets = []

        for network in self.get_networks():
            if network.network_type != 'flat':
                continue

            dst_net = dst_info.by_hash.get(network.hash)
            if dst_net:
                continue

            if network.external and network.id in ext_net_map:
                LOG.debug("Network '%s' is external and specified in the "
                          "external networks mapping. Skipping network...",
                          network.id)
                continue

            if network.physnet in dst_flat_physnets:
                busy_flat_physnets.append(network)

        return busy_flat_physnets

    def missing_vlan_physnets(self, dst_info, dst_neutron_client, ext_net_map):
        """
        Get list of missing physical networks for VLAN network type.

        :param dst_info: NetworkInfo instance of DST cloud
        :param dst_neutron_client: DST neutron client
        :param ext_net_map: External networks mapping dictionary. Format:
                        {<src_external_network>: <dst_external_network>, ...}

        :return: List of missing VLAN physnets.
        """

        missing_vlan_physnets = []
        dst_vlan_physnets = [net.physnet for net in dst_info.get_networks() if
                             net.network_type == 'vlan']

        # We need to specify segmentation ID in case of VLAN network creation
        # in OpenStack versions earlier than Juno (f.e. Icehouse, Grizzly etc.)
        dst_seg_ids = neutron.get_segmentation_ids_from_net_list(
            dst_info.networks_info)
        # We do not care about free segmentation ID on source cloud, we only
        # need to have destination one for checking purpose
        free_seg_id = neutron.generate_new_segmentation_id(dst_seg_ids,
                                                           dst_seg_ids,
                                                           'vlan')

        for network in self.get_networks():
            if network.network_type != 'vlan':
                continue

            if network.physnet in dst_vlan_physnets:
                continue

            if network.external and network.id in ext_net_map:
                LOG.debug("Network '%s' is external and specified in the "
                          "external networks mapping. Skipping network...",
                          network.id)
                continue

            with proxy_client.expect_exception(neutron_exc.BadRequest):
                try:
                    network_info = {
                        'network': {
                            'provider:physical_network': network.physnet,
                            'provider:network_type': 'vlan',
                            'provider:segmentation_id': free_seg_id
                        }
                    }
                    new_net = dst_neutron_client.create_network(network_info)
                except neutron_exc.NeutronClientException:
                    missing_vlan_physnets.append(network.physnet)
                else:
                    dst_neutron_client.delete_network(new_net['network']['id'])

        return missing_vlan_physnets

    def get_invalid_ext_net_ids(self, dst_info, ext_net_map):
        """
        Get invalid external networks IDs.

        Check existence and validity of external networks, specified in the map
        file (config.migrate.ext_net_map - path to this file)

        :param dst_info: NetworkInfo instance of DST cloud
        :param ext_net_map: External networks mapping dictionary. Format:
                        {<src_external_network>: <dst_external_network>, ...}

        :return dict: Dictionary of all invalid external networks, specified in
                      the mapping file. Format:
                      {'src_nets': [<src_net_id_0>, <src_net_id_1>, ...],
                       'dst_nets': [<dst_net_id_0>, <dst_net_id_1>, ...]}
        """

        invalid_ext_nets = {'src_nets': [], 'dst_nets': []}

        src_ext_nets_ids = [net.id for net in self.by_id.itervalues() if
                            net.external]
        dst_ext_nets_ids = [net.id for net in dst_info.by_id.itervalues() if
                            net.external]

        for src_net_id, dst_net_id in ext_net_map.iteritems():
            if src_net_id not in src_ext_nets_ids:
                invalid_ext_nets['src_nets'].append(src_net_id)
            if dst_net_id not in dst_ext_nets_ids:
                invalid_ext_nets['dst_nets'].append(dst_net_id)

        return invalid_ext_nets


class Network(object):
    def __init__(self, info):
        self.info = info
        self.subnets_hash = info['subnets_hash']
        self.subnets = []
        self.id = info['id']
        self.hash = info['res_hash']

        self.external = self.info['router:external']
        self.network_type = self.info['provider:network_type']
        self.seg_id = self.info["provider:segmentation_id"]
        self.physnet = self.info["provider:physical_network"]

    def __str__(self):
        return "{name} ({uuid}), physnet: {phy}".format(
            name=self.info['name'], uuid=self.id, phy=self.physnet)

    def add_subnet(self, info):
        self.subnets.append(info)

    def check_segmentation_id_overlapping(self, dst_seg_ids):
        """
        Check if segmentation ID of current network overlaps with destination.

        :param dst_seg_ids: Dictionary with busy segmentation IDs on DST
        """

        if self.network_type not in dst_seg_ids:
            return

        if self.seg_id in dst_seg_ids[self.network_type]:
            message = ("Segmentation ID '%s' (network type = '%s', "
                       "network ID = '%s') is already busy on the destination "
                       "cloud.") % (self.seg_id, self.network_type, self.id)
            LOG.warning(message)
            raise exception.AbortMigrationError(message)


class FloatingIp(object):
    def __init__(self, info):
        self.address = info['floating_ip_address']
        self.tenant = info['tenant_name']
        self.network = info['network_name']
        self.net_tenant = info['ext_net_tenant_name']
        self.port_id = info['port_id']
        self.network_id = info['floating_network_id']

    def __eq__(self, other):
        if not isinstance(other, FloatingIp):
            return False

        return (self.address == other.address and
                self.tenant == other.tenant and
                self.network == other.network and
                self.net_tenant == other.net_tenant)

    def check_floating_ips_overlapping(self, dst_floating_ip):
        """
        Check if Floating IP overlaps with DST.

        Parameters to compare:
        - same floating ip address;
        - same tenant;
        - same network;
        - same network's tenant.

        Also check if this Floating IP is not busy (i.e. is not associated to
        VM on SRC and DST at the same time) on both environments.

        :param dst_floating_ip: DST FloatingIp instance.

        :raise AbortMigrationError: If FloatingIp overlaps with the DST.
        """

        # Check association to VMs on SRC and DST aa the same time
        ports_overlap = self.port_id and dst_floating_ip.port_id

        if not self == dst_floating_ip or ports_overlap:
            message = ("Floating IP '%s' overlaps with the same IP on DST." %
                       self.address)
            LOG.error(message)
            raise exception.AbortMigrationError(message)


def cidr_overlapping(src_cidr, dst_cidr):
    """
    Check for subnets CIDRs overlap.

    :param src_cidr : SRC subnet's CIDR (f.e. '192.168.1.0/24')
    :param dst_cidr: DST subnet's CIDR (f.e. '192.168.1.0/24')

    :return bool: Whether CIDRs overlap or not.
    """

    src_net = ipaddr.IPNetwork(src_cidr)
    dst_net = ipaddr.IPNetwork(dst_cidr)

    return src_net.overlaps(dst_net)


def convert_allocation_pools_to_ip_set(allocation_pools):
    """
    Convert allocation pool to ip set.

    :param allocation_pools: Subnet's allocation pool (f.e.:
                               [{'start': '2.2.2.2', 'end': '2.2.2.10'},
                               {'start': '2.2.2.20', 'end': '2.2.2.30'}, ...])

    :return: netaddr.ip.sets.IPSet instance
    """

    ranges = [pool.values() for pool in allocation_pools]
    for count, pool in enumerate(ranges):
        ranges[count] = [netaddr.IPAddress(ip) for ip in pool]
        ranges[count].sort()

    ip_ranges = [netaddr.IPRange(*r) for r in ranges]
    ip_sets = [netaddr.IPSet(r) for r in ip_ranges]

    result_set = reduce(lambda res, ip_set: res.union(ip_set), ip_sets)

    return result_set


def allocation_pools_overlapping(src_pools, dst_pools):
    """
    Check for subnets allocation pools overlap.

    :param src_pools : SRC subnet's allocation pools
    :param dst_pools: DST subnet's allocation pools

    Allocation pools format the same as from the Neutron's result:
    [{'start': '2.2.2.2', 'end': '2.2.2.10'},
    {'start': '2.2.2.20', 'end': '2.2.2.30'}, ...]

    :return bool: Whether allocation pools overlap or not.
    """

    src_ip_set = convert_allocation_pools_to_ip_set(src_pools)
    dst_ip_set = convert_allocation_pools_to_ip_set(dst_pools)

    overlap = src_ip_set & dst_ip_set

    if not overlap:
        return False

    return True


def check_equal_networks(src_network, dst_network):
    """
    Check if 2 networks are equal.

    Networks are equal when they have the same hash and all hashes of their
    subnets are equal too.

    :param src_network: Network instance from source cloud
    :param dst_network: Network instance from destination cloud

    :return bool: Whether networks are equal or not.
    """

    networks_are_equal = (src_network.hash == dst_network.hash and
                          src_network.subnets_hash == dst_network.subnets_hash)

    if networks_are_equal:
        return True

    return False
