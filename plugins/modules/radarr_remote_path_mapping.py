#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_remote_path_mapping

short_description: Manages Radarr remote path mapping.

version_added: "0.0.2"

description: Manages Radarr remote path mapping.

options:
    host:
        description: Download Client host.
        required: true
        type: str
    remote_path:
        description: Download Client remote path.
        required: true
        type: str
    local_path:
        description: Local path.
        required: true
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials
    - devopsarr.radarr.radarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a remote path mapping
- name: Create a remote path mapping
  devopsarr.radarr.remote_path_mapping:
    host: 'transmission-host'
    remote_path: '/download/complete/'
    local_path: '/series-download/'


# Delete a remote path mapping
- name: Delete a remote_path_mapping
  devopsarr.radarr.remote_path_mapping:
    host: 'transmission-host'
    remote_path: '/download/complete/'
    local_path: '/series-download/'
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
        host=dict(type='str', required=True),
        remote_path=dict(type='str', required=True),
        local_path=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_remote_path_mapping(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_remote_path_mapping(remote_path_mapping_resource=want)
        except radarr.ApiException as e:
            module.fail_json('Error creating remote path mapping: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating remote path mapping: %s' % to_native(e), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_remote_path_mappings(result):
    try:
        return client.list_remote_path_mapping()
    except radarr.ApiException as e:
        module.fail_json('Error listing remote path mappings: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing remote path mappings: %s' % to_native(e), **result)


def find_remote_path_mapping(host, remote_path, local_path, result):
    for mapping in list_remote_path_mappings(result):
        if mapping.host == host and \
           mapping.remote_path == remote_path and \
           mapping.local_path == local_path:
            return mapping
    return None


def update_remote_path_mapping(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_remote_path_mapping(remote_path_mapping_resource=want, id=str(want.id))
        except radarr.ApiException as e:
            module.fail_json('Error updating remote path mapping: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating remote path mapping: %s' % to_native(e), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_remote_path_mapping(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_remote_path_mapping(result['id'])
            except radarr.ApiException as e:
                module.fail_json('Error deleting remote path mapping: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting remote path mapping: %s' % to_native(e), **result)
            result['id'] = 0
    module.exit_json(**result)


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
        id=0,
    )

    # Check if a resource is present already.
    state = find_remote_path_mapping(module.params['host'], module.params['remote_path'], module.params['local_path'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_remote_path_mapping(result)

    # Set wanted resource.
    want = radarr.RemotePathMappingResource(
        host=module.params['host'],
        remote_path=module.params['remote_path'],
        local_path=module.params['local_path'],
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_remote_path_mapping(want, result)

    # No need for update
    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
