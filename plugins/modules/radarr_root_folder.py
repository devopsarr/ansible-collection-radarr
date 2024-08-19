#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_root_folder

short_description: Manages Radarr root folder.

version_added: "0.0.2"

description: Manages Radarr root folder.

options:
    path:
        description: Actual root folder.
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
# Create a root folder
- name: Create a root folder
  devopsarr.radarr.radarr_root_folder:
    path: '/series'

# Delete a root folder
- name: Delete a root_folder
  devopsarr.radarr.radarr_root_folder:
    path: '/series'
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: root folder ID.
    type: int
    returned: always
    sample: '1'
path:
    description: The root folder path.
    type: str
    returned: 'on create/update'
    sample: '/series'
accessible:
    description: Access flag.
    type: str
    returned: 'on create/update'
    sample: 'true'
unmapped_folders:
    description: List of unmapped folders
    type: dict
    returned: always
    sample: '[]'
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
        path=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_root_folder(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_root_folder(root_folder_resource=want)
        except radarr.ApiException as e:
            module.fail_json('Error creating root folder: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating root folder: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_root_folders(result):
    try:
        return client.list_root_folder()
    except radarr.ApiException as e:
        module.fail_json('Error listing root folders: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing root folders: {}'.format(to_native(e)), **result)


def find_root_folder(path, result):
    for folder in list_root_folders(result):
        if folder.path == path:
            return folder
    return None


def delete_root_folder(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_root_folder(result['id'])
            except radarr.ApiException as e:
                module.fail_json('Error deleting root folder: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting root folder: {}'.format(to_native(e)), **result)
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
    client = radarr.RootFolderApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_root_folder(module.params['path'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_root_folder(result)

    # Create a new resource.
    if result['id'] == 0:
        create_root_folder({'path': module.params['path']}, result)

    # No need for update
    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
