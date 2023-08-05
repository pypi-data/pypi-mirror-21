# Copyright 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from cloudferry import model


@model.type_alias('tenants')
class Tenant(model.Model):
    object_id = model.PrimaryKey()
    name = model.String(required=True)
    enabled = model.Boolean(required=True)
    description = model.String(allow_none=True)

    def equals(self, other):
        # pylint: disable=no-member
        if super(Tenant, self).equals(other):
            return True
        return self.name.lower() == other.name.lower()


@model.type_alias('users')
class User(model.Model):
    object_id = model.PrimaryKey()
    name = model.String(required=True)
    enabled = model.Boolean(required=True)

    def equals(self, other):
        # pylint: disable=no-member
        if super(User, self).equals(other):
            return True
        return self.name.lower() == other.name.lower()


@model.type_alias('roles')
class Role(model.Model):
    object_id = model.PrimaryKey()
    name = model.String(required=True)

    def equals(self, other):
        # pylint: disable=no-member
        if super(Role, self).equals(other):
            return True
        return self.name.lower() == other.name.lower()


@model.type_alias('user_roles')
class UserRole(model.Model):
    object_id = model.PrimaryKey()
    tenant = model.Dependency(Tenant)
    user = model.Dependency(User)
    role = model.Dependency(Role)

    def equals(self, other):
        # pylint: disable=no-member
        if super(UserRole, self).equals(other):
            return True
        return self.tenant.equals(other.tenant) \
            and self.user.equals(other.user) \
            and self.role.equals(other.role)
