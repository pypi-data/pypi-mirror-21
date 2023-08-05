# coding=utf-8

# Copyright 2016 Spanish National Research Council
# Copyright 2016 INDIGO-DataCloud
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystoneauth1.exceptions import auth_plugins


class MissingOidcAuthorizationCode(auth_plugins.AuthPluginException):
    message = "Could not get an OpenID Connect authorization code."


class OidcAuthorizationEndpointNotFound(auth_plugins.AuthPluginException):
    message = "OpenID Connect authorization endpoint not provided."
