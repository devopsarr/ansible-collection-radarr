#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_import_list_exclusion

short_description: Manages Radarr import list exclusion.

version_added: "1.0.0"

description: Manages Radarr import list exclusion.

options:
    tmdb_id:
        description: TMDB ID.
        required: true
        type: int
    year:
        description: Year.
        required: true
        type: int
    title:
        description: Title.
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
# Create a import list exclusion
- name: Create a import list exclusion
  devopsarr.radarr.radarr_import_list_exclusion:
    tmdb_id: 123
    year: 1990
    title: 'example'


# Delete a import list exclusion
- name: Delete a import_list_exclusion
  devopsarr.radarr.radarr_import_list_exclusion:
    tmdb_id: 123
    title: 'example'
    year: 1990
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: import list exclusion ID.
    type: int
    returned: always
    sample: 1
tmdb_id:
    description: TMDB ID.
    type: int
    returned: 'always'
    sample: 12345
year:
    description: Year.
    type: int
    returned: 'always'
    sample: 1990
title:
    description: Title.
    type: str
    returned: 'always'
    sample: 'Gladiator'
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
        tmdb_id=dict(type='int', required=True),
        year=dict(type='int', required=True),
        title=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_import_list_exclusion(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_exclusions(import_exclusions_resource=want)
        except radarr.ApiException as e:
            module.fail_json('Error creating import list exclusion: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating import list exclusion: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_import_list_exclusions(result):
    try:
        return client.list_exclusions()
    except radarr.ApiException as e:
        module.fail_json('Error listing import list exclusions: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing import list exclusions: {}'.format(to_native(e)), **result)


def find_import_list_exclusion(title, tmdb_id, result):
    for import_list_exclusion in list_import_list_exclusions(result):
        if import_list_exclusion.tmdb_id == tmdb_id and \
           import_list_exclusion.movie_title == title:
            return import_list_exclusion
    return None


def delete_import_list_exclusion(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_exclusions(result['id'])
            except radarr.ApiException as e:
                module.fail_json('Error deleting import list exclusion: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting import list exclusion: {}'.format(to_native(e)), **result)
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
    client = radarr.ImportExclusionsApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_import_list_exclusion(module.params['title'], module.params['tmdb_id'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_import_list_exclusion(result)

    # Set wanted resource.
    want = radarr.ImportExclusionsResource(
        tmdb_id=module.params['tmdb_id'],
        movie_year=module.params['year'],
        movie_title=module.params['title'],
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_import_list_exclusion(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
