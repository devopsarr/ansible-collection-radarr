#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_import_list

short_description: Manages Radarr import list.

version_added: "1.0.0"

description: Manages Radarr import list.

options:
    name:
        description: Name.
        required: true
        type: str
    search_on_add:
        description: Search on add flag.
        type: bool
    enable_auto:
        description: Enable automatic add flag.
        type: bool
    enabled:
        description: Enabled flag.
        type: bool
    quality_profile_id:
        description: Quality profile ID.
        type: int
    list_order:
        description: List order.
        type: int
    monitor:
        description: Should monitor.
        type: str
    root_folder_path:
        description: Root folder path.
        type: str
    list_type:
        description: List type.
        type: str
    minimum_availability:
        description: Minimum availability.
        type: str
    update_secrets:
        description: Flag to force update of secret fields.
        type: bool
        default: false

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials
    - devopsarr.radarr.radarr_implementation
    - devopsarr.radarr.radarr_taggable
    - devopsarr.radarr.radarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a import list
- name: Create a import list
  devopsarr.radarr.radarr_import_list:
    enable_auto: false
    enabled: true
    monitor: "unknown"
    quality_profile_id: 1
    list_order: 1
    root_folder_path: "/config"
    search_on_add: false
    fields:
    - name: "apiKey"
      value: "Key"
    - name: "baseUrl"
      value: "localhost"
    - name: "languageProfileIds"
      value: [1]
    name: "RadarrImport"
    list_type: "standard"
    minimum_availability: "tba"
    config_contract: "RadarrSettings"
    implementation: "RadarrImport"
    tags: []

# Delete a import list
- name: Delete a import list
  devopsarr.radarr.radarr_import_list:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: import listID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
enable_auto:
    description: Enable automatic add flag.
    returned: always
    type: bool
    sample: false
enabled:
    description: Enabled flag.
    returned: always
    type: bool
    sample: false
search_on_add:
    description: Search on add flag.
    returned: always
    type: bool
    sample: false
quality_profile_id:
    description: Quality profile ID.
    returned: always
    type: int
    sample: 1
list_order:
    description: List order.
    returned: always
    type: int
    sample: 1
monitor:
    description: Should monitor.
    returned: always
    type: str
    sample: "unknown"
root_folder_path:
    description: Root folder path.
    returned: always
    type: str
    sample: "/path"
list_type:
    description: List type.
    returned: always
    type: str
    sample: "standard"
minimum_availability:
    description: Minimum availability.
    returned: always
    type: str
    sample: "tba"
config_contract:
    description: Config contract.
    returned: always
    type: str
    sample: "CustomSettings"
implementation:
    description: Implementation.
    returned: always
    type: str
    sample: "CustomImport"
protocol:
    description: Protocol.
    returned: always
    type: str
    sample: "torrent"
tags:
    description: Tag list.
    type: list
    returned: always
    elements: int
    sample: [1,2]
fields:
    description: field list.
    type: list
    returned: always
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_field_utils import FieldHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def is_changed(status, want):
    if (want.name != status.name or
            want.enable_auto != status.enable_auto or
            want.enabled != status.enabled or
            want.monitor != status.monitor or
            want.quality_profile_id != status.quality_profile_id or
            want.list_order != status.list_order or
            want.search_on_add != status.search_on_add or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
            want.list_type != status.list_type or
            want.minimum_availability != status.minimum_availability or
            want.tags != status.tags):
        return True

    for status_field in status.fields:
        for want_field in want.fields:
            if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                return True
    return False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str', required=True),
        enable_auto=dict(type='bool'),
        enabled=dict(type='bool'),
        search_on_add=dict(type='bool'),
        quality_profile_id=dict(type='int'),
        list_order=dict(type='int'),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        monitor=dict(type='str'),
        root_folder_path=dict(type='str'),
        list_type=dict(type='str'),
        minimum_availability=dict(type='str'),
        tags=dict(type='list', elements='int', default=[]),
        fields=dict(type='list', elements='dict', options=field_helper.field_args),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
    )


def create_import_list(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_import_list(import_list_resource=want)
        except radarr.ApiException as e:
            module.fail_json('Error creating import list: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating import list: %s' % to_native(e), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_import_lists(result):
    try:
        return client.list_import_list()
    except radarr.ApiException as e:
        module.fail_json('Error listing import lists: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing import lists: %s' % to_native(e), **result)


def find_import_list(name, result):
    for import_list in list_import_lists(result):
        if import_list.name == name:
            return import_list
    return None


def update_import_list(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_import_list(import_list_resource=want, id=str(want.id))
        except radarr.ApiException as e:
            module.fail_json('Error updating import list: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating import list: %s' % to_native(e), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_import_list(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_import_list(result['id'])
            except radarr.ApiException as e:
                module.fail_json('Error deleting import list: %s\n body: %s'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting import list: %s' % to_native(e), **result)
            result['id'] = 0
    module.exit_json(**result)


def run_module():
    global client
    global module
    global field_helper

    # Init helper.
    field_helper = FieldHelper()

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = radarr.ImportListApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )
    # Check if a resource is present already.
    state = find_import_list(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_import_list(result)

    # Set wanted resource.
    want = radarr.ImportListResource(
        name=module.params['name'],
        search_on_add=module.params['search_on_add'],
        quality_profile_id=module.params['quality_profile_id'],
        list_order=module.params['list_order'],
        monitor=module.params['monitor'],
        root_folder_path=module.params['root_folder_path'],
        config_contract=module.params['config_contract'],
        implementation=module.params['implementation'],
        list_type=module.params['list_type'],
        minimum_availability=module.params['minimum_availability'],
        enable_auto=module.params['enable_auto'],
        enabled=module.params['enabled'],
        tags=module.params['tags'],
        fields=field_helper.populate_fields(module.params['fields']),
    )

    # Create a new resource, if needed.
    if result['id'] == 0:
        create_import_list(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        update_import_list(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
