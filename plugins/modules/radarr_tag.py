#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_tag

short_description: Manages Radarr tag.

version_added: "0.0.1"

description: Manages Radarr tag.

options:
    label:
        description: Actual tag.
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
# Create a tag
- name: Create a tag
  devopsarr.radarr.radarr_tag:
    label: default

# Delete a tag
- name: Delete a tag
  devopsarr.radarr.radarr_tag:
    label: wrong
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Tag ID.
    type: int
    returned: always
    sample: '1'
label:
    description: The output message that the test module generates.
    type: str
    returned: 'on create/update'
    sample: 'hd'
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
        label=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_tag(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_tag(tag_resource=want)
        except radarr.ApiException as e:
            module.fail_json('Error creating tag: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating tag: %s' % to_native(e), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_tags(result):
    try:
        return client.list_tag()
    except radarr.ApiException as e:
        module.fail_json('Error listing tags: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing tags: %s' % to_native(e), **result)


def find_tag(label, result):
    for tag in list_tags(result):
        if tag.label == label:
            return tag
    return None


def delete_tag(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_tag(result['id'])
            except radarr.ApiException as e:
                module.fail_json('Error deleting tag: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting tag: %s' % to_native(e), **result)
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
    client = radarr.TagApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_tag(module.params['label'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_tag(result)

    # Create a new resource.
    if result['id'] == 0:
        create_tag({'label': module.params['label']}, result)

    # No need for update
    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
