#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_naming

short_description: Manages Radarr naming.

version_added: "1.0.0"

description: Manages Radarr naming.

options:
    standard_movie_format:
        description: Standard movie format.
        required: true
        type: str
    movie_folder_format:
        description: Movie folder format.
        required: true
        type: str
    colon_replacement_format:
        description: Colon replacement format.
        required: true
        type: str
        choices: ["delete", "dash", "spaceDash", "spaceDashSpace"]
    rename_movies:
        description: Rename movies.
        required: true
        type: bool
    replace_illegal_characters:
        description: Replace illegal characters.
        required: true
        type: bool

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update naming
- name: Update naming
  devopsarr.radarr.radarr_naming:
    rename_movies: true
    replace_illegal_characters: true
    colon_replacement_format: 'dash'
    movie_folder_format: '{Movie Title} ({Release Year})'
    standard_movie_format: '{Movie Title} ({Release Year}) {Quality Full}'
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        standard_movie_format=dict(type='str', required=True),
        movie_folder_format=dict(type='str', required=True),
        colon_replacement_format=dict(type='str', required=True, choices=["delete", "dash", "spaceDash", "spaceDashSpace"]),
        rename_movies=dict(type='bool', required=True),
        replace_illegal_characters=dict(type='bool', required=True),
    )


def read_naming(result):
    try:
        return client.get_naming_config()
    except Exception as e:
        module.fail_json('Error getting naming: %s' % to_native(e.reason), **result)


def update_naming(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_naming_config(naming_config_resource=want, id="1")
        except Exception as e:
            module.fail_json('Error updating naming: %s' % to_native(e.reason), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = radarr.NamingConfigApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_naming(result)
    if state:
        result.update(state.model_dump(by_alias=False))

    want = radarr.NamingConfigResource(
        standard_movie_format=module.params['standard_movie_format'],
        movie_folder_format=module.params['movie_folder_format'],
        colon_replacement_format=module.params['colon_replacement_format'],
        rename_movies=module.params['rename_movies'],
        replace_illegal_characters=module.params['replace_illegal_characters'],
        id=1,
        # add not used parameters to compare resource
        include_quality=False,
        replace_spaces=False,
        separator=None,
        number_style=None,
    )

    # Update an existing resource.
    if want != state:
        update_naming(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
