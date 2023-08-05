# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ecl import service_filter


class BlockStoreService(service_filter.ServiceFilter):
    """The block store service."""

    valid_versions = [service_filter.ValidVersion('v2')]

    def __init__(self, version=None):
        """Create a block store service."""
        super(BlockStoreService, self).__init__(service_type='volumev2',
                                                version=version,
                                                requires_project_id=True)
