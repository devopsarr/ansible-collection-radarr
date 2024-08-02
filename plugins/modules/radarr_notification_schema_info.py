#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_notification_schema_info

short_description: Get information about Radarr notification schema.

version_added: "1.0.0"

description: Get information about Radarr notification schema.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all notifications schema.
- name: Gather information about all notifications schema
  devopsarr.radarr.radarr_notification_schema_info:

# Gather information about a single notification schema.
- name: Gather information about a single notification schema
  devopsarr.radarr.radarr_notification_schema_info:
    name: BroadcastheNet
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
notifications:
    description: A list of notifications schema.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: notification ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        on_grab:
            description: On grab flag.
            returned: always
            type: bool
            sample: true
        on_download:
            description: On download flag.
            returned: always
            type: bool
            sample: false
        on_rename:
            description: On rename flag.
            returned: always
            type: bool
            sample: true
        on_movie_add:
            description: On movie add flag.
            returned: always
            type: bool
            sample: true
        on_movie_delete:
            description: On movie delete flag.
            returned: always
            type: bool
            sample: true
        on_movie_file_delete:
            description: On movie file delete flag.
            returned: always
            type: bool
            sample: true
        on_movie_file_delete_for_upgrade:
            description: On movie file delete for upgrade flag.
            returned: always
            type: bool
            sample: true
        on_health_issue:
            description: On health issue flag.
            returned: always
            type: bool
            sample: true
        on_health_restored:
            description: On health restored flag.
            returned: always
            type: bool
            sample: true
        on_application_update:
            description: On application update flag.
            returned: always
            type: bool
            sample: true
        on_manual_interaction_required:
            description: On manual interaction required flag.
            returned: always
            type: bool
            sample: true
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "WebhookSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "Webhook"
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
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str'),
    )


def list_notification_schema(result):
    try:
        return client.list_notification_schema()
    except radarr.ApiException as e:
        module.fail_json('Error listing notification schemas: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing notification schemas: %s' % to_native(e), **result)


def populate_notification_schema(result):
    notifications = []
    # Check if a resource is present already.
    for notification in list_notification_schema(result):
        if module.params['name']:
            if notification.implementation == module.params['name']:
                notifications = [notification.model_dump(by_alias=False)]
        else:
            notifications.append(notification.model_dump(by_alias=False))
    return notifications


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.NotificationApi(module.api)
    result = dict(
        changed=False,
        notifications=[],
    )

    # List resources.
    result.update(notifications=populate_notification_schema(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
