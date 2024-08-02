#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_indexer_config_info

short_description: Get information about Radarr indexer config.

version_added: "1.0.0"

description: Get information about Radarr indexer config.

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch indexer config
- name: fetch indexer config
  devopsarr.radarr.radarr_indexer_config_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Indexer config ID.
    type: int
    returned: always
    sample: '1'
prefer_indexer_flags:
    description: Prefer indexer flags.
    returned: always
    type: bool
    sample: 'true'
allow_hardcoded_subs:
    description: Allow hardcoded subs.
    returned: always
    type: bool
    sample: 'true'
maximum_size:
    description: Maximum size.
    returned: always
    type: int
    sample: '0'
minimum_age:
    description: Minimum age.
    returned: always
    type: int
    sample: '0'
retention:
    description: Retention.
    returned: always
    type: int
    sample: '0'
rss_sync_interval:
    description: RSS sync interval.
    returned: always
    type: int
    sample: '100'
availability_delay:
    description: Availability delay.
    returned: always
    type: int
    sample: '0'
whitelisted_hardcoded_subs:
    description: Whitelisted hardcoded subs.
    returned: always
    type: str
    sample: ''
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def get_indexer_config(result):
    try:
        return client.get_indexer_config()
    except radarr.ApiException as e:
        module.fail_json('Error getting indexer config: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting indexer config: %s' % to_native(e), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.IndexerConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_indexer_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
