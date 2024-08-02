#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_remote_path_mapping_info

short_description: Get information about Radarr remote path mapping.

version_added: "1.0.0"

description: Get information about Radarr remote path mapping.

options:
    id:
        description: Remote path mapping id.
        type: int

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all remote path mappings.
- name: Gather information about all remote path mappings
  devopsarr.radarr.radarr_remote_path_mapping_info:

# Gather information about a single remote path mapping.
- name: Gather information about a single remote path mapping
  devopsarr.radarr.radarr_remote_path_mapping_info:
    id: 1
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
remote_path_mappings:
    description: A list of remote path mappings.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: remote path mapping ID.
            type: int
            returned: always
            sample: '1'
        host:
            description: Download Client host.
            type: str
            returned: 'always'
            sample: 'transmission-host'
        remote_path:
            description: Download Client remote path.
            type: str
            returned: 'always'
            sample: '/download/complete/'
        local_path:
            description: Local remote path.
            type: str
            returned: 'always'
            sample: '/series-download/'
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        id=dict(type='int'),
    )


def list_remote_path_mapping(result):
    try:
        return client.list_remote_path_mapping()
    except radarr.ApiException as e:
        module.fail_json('Error listing remote path mappings: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing remote path mappings: %s' % to_native(e), **result)


def populate_remote_path_mappings(result):
    mappings = []
    # Check if a resource is present already.
    for remote_path_mapping in list_remote_path_mapping(result):
        if module.params['id']:
            if remote_path_mapping.id == module.params['id']:
                mappings = [remote_path_mapping.model_dump(by_alias=False)]
        else:
            mappings.append(remote_path_mapping.model_dump(by_alias=False))
    return mappings


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.RemotePathMappingApi(module.api)
    result = dict(
        changed=False,
        remote_path_mappings=[],
    )

    # List resources.
    result.update(remote_path_mappings=populate_remote_path_mappings(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
