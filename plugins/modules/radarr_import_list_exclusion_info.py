#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_import_list_exclusion_info

short_description: Manages Radarr import list exclusion.

version_added: "1.0.0"

description: Manages Radarr import list exclusion.

options:
    tmdb_id:
        description: TVDB ID.
        type: int

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all import list exclusion
- name: Gather information about all import list exclusion
  devopsarr.radarr.radarr_import_list_exclusion_info:

# Gather information about a single list exclusion
- name: Gather information about a single list exclusion
  devopsarr.radarr.radarr_import_list_exclusion_info:
    tmdb_id: 123
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
import_list_exclusions:
    description: A list of remote path mappings.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: import list exclusion ID.
            type: int
            returned: always
            sample: 1
        tmdb_id:
            description: TVDB ID.
            type: int
            returned: 'always'
            sample: 12345
        title:
            description: Title.
            type: str
            returned: 'always'
            sample: 'Gladiator'
        year:
            description: Year.
            type: int
            returned: 'always'
            sample: 1990
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
        tmdb_id=dict(type='int'),
    )


def list_import_list_exclusion(result):
    try:
        return client.list_exclusions()
    except Exception as e:
        module.fail_json('Error listing import list exclusions: %s' % to_native(e.reason), **result)


def populate_import_list_exclusions(result):
    exclusions = []
    # Check if a resource is present already.
    for import_list_exclusion in list_import_list_exclusion(result):
        if module.params['tmdb_id']:
            if import_list_exclusion['tmdb_id'] == module.params['tmdb_id']:
                exclusions = [import_list_exclusion.dict(by_alias=False)]
        else:
            exclusions.append(import_list_exclusion.dict(by_alias=False))
    return exclusions


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.ImportExclusionsApi(module.api)
    result = dict(
        changed=False,
        import_list_exclusions=[],
    )

    # List resources.
    result.update(import_list_exclusions=populate_import_list_exclusions(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
