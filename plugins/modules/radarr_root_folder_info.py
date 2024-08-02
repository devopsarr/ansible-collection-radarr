#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_root_folder_info

short_description: Get information about Radarr root folder.

version_added: "1.0.0"

description: Get information about Radarr root folder.

options:
    path:
        description: Actual root folder.
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all root folders.
- name: Gather information about all root folders
  devopsarr.radarr.radarr_root_folder_info:

# Gather information about a single root folder.
- name: Gather information about a single root folder
  devopsarr.radarr.radarr_root_folder_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
root_folders:
    description: A list of root folders.
    returned: always
    type: list
    elements: dict
    contains:
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
        path=dict(type='str'),
    )


def list_root_folder(result):
    try:
        return client.list_root_folder()
    except radarr.ApiException as e:
        module.fail_json('Error listing root folders: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing root folders: %s' % to_native(e), **result)


def populate_root_folders(result):
    folders = []
    # Check if a resource is present already.
    for root_folder in list_root_folder(result):
        if module.params['path']:
            if root_folder.path == module.params['path']:
                folders = [root_folder.model_dump(by_alias=False)]
        else:
            folders.append(root_folder.model_dump(by_alias=False))
    return folders


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
        root_folders=[],
    )

    # List resources.
    result.update(root_folders=populate_root_folders(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
