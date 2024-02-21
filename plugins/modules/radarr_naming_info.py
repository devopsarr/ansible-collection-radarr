#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_naming_info

short_description: Get information about Radarr naming.

version_added: "1.0.0"

description: Get information about Radarr naming.

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch naming
- name: fetch naming
  devopsarr.radarr.radarr_naming_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Naming ID.
    type: int
    returned: always
    sample: '1'
standard_movie_format:
    description: Standard movie format.
    returned: always
    type: str
    sample: '{Movie Title} ({Release Year}) {Quality Full}'
movie_folder_format:
    description: Movie folder format.
    returned: always
    type: str
    sample: '{Movie Title} ({Release Year})'
colon_replacement_format:
    description: Colon replacement format.
    returned: always
    type: str
    sample: 'dash'
rename_movies:
    description: Rename movies.
    returned: always
    type: bool
    sample: true
replace_illegal_characters:
    description: Replace illegal characters.
    returned: always
    type: bool
    sample: true
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def get_naming_config(result):
    try:
        return client.get_naming_config()
    except Exception as e:
        module.fail_json('Error getting naming: %s' % to_native(e.reason), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.NamingConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_naming_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
