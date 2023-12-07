#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_movie

short_description: Manages Radarr movie.

version_added: "1.0.0"

description: Manages Radarr movie.

options:
    monitored:
        description: Monitored flag.
        type: bool
        default: false
    quality_profile_id:
        description: Quality profile ID.
        type: int
    tmdb_id:
        description: TMDB ID.
        required: true
        type: int
    path:
        description: Movie path.
        required: true
        type: str
    root_folder_path:
        description: Root folder path.
        type: str
    title:
        description: Movie title.
        required: true
        type: str
    minimum_availability:
        description: Minimum availability.
        type: str
        choices: ["tba", "announced", "inCinemas", "released", "deleted"]

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials
    - devopsarr.radarr.radarr_taggable
    - devopsarr.radarr.radarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a movie
- name: Create a movie
  devopsarr.radarr.radarr_movie:
    title: "The Matrix"
    tmdb_id: 603
    monitored: true
    path: "/config/the-matrix"
    root_folder_path: "/config/"
    quality_profile_id: 1
    minimum_availability: "announced"
    tags: [1,2]

# Delete a movie
- name: Delete a movie
  devopsarr.radarr.radarr_movie:
    title: "The Matrix"
    tmdb_id: 603
    path: "/config/the-matrix"
    minimum_availability: "announced"
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: movie ID.
    type: int
    returned: always
    sample: 1
monitored:
    description: Monitored flag.
    type: bool
    returned: always
    sample: false
quality_profile_id:
    description: Quality profile ID.
    type: int
    returned: always
    sample: 1
tmdb_id:
    description: TMDB ID.
    type: int
    returned: always
    sample: 12345678
path:
    description: Movie path.
    type: str
    returned: always
    sample: "/movie/movie_title"
root_folder_path:
    description: Root folder path.
    type: str
    returned: always
    sample: "/movie"
title:
    description: Movie title.
    type: str
    returned: always
    sample: "Movie Title"
minimum_availability:
    description: Minimum availability.
    returned: always
    type: str
    sample: "tba"
tags:
    description: Tag list.
    type: list
    returned: always
    elements: int
    sample: [1,2]
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def is_changed(status, want):
    if (want.title != status.title or
            want.monitored != status.monitored or
            want.minimum_availability != status.minimum_availability or
            want.quality_profile_id != status.quality_profile_id or
            want.tmdb_id != status.tmdb_id or
            want.path != status.path or
            want.root_folder_path != status.root_folder_path or
            want.tags != status.tags):
        return True

    return False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        monitored=dict(type='bool', default=False),
        title=dict(type='str', required=True),
        path=dict(type='str', required=True),
        root_folder_path=dict(type='str'),
        quality_profile_id=dict(type='int'),
        tmdb_id=dict(type='int', required=True),
        tags=dict(type='list', elements='int', default=[]),
        minimum_availability=dict(type='str', choices=['tba', 'announced', 'inCinemas', 'released', 'deleted']),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_movie(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_movie(movie_resource=want)
        except Exception as e:
            module.fail_json('Error creating movie: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))
    module.exit_json(**result)


def list_movie(result):
    try:
        return client.list_movie()
    except Exception as e:
        module.fail_json('Error listing movie: %s' % to_native(e.reason), **result)


def find_movie(tmdb_id, result):
    for movie in list_movie(result):
        if movie['tmdb_id'] == tmdb_id:
            return movie
    return None


def update_movie(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_movie(movie_resource=want, id=str(want.id))
        except Exception as e:
            module.fail_json('Error updating movie: %s' % to_native(e.reason), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.dict(by_alias=False))


def delete_movie(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_movie(result['id'])
            except Exception as e:
                module.fail_json('Error deleting movie: %s' % to_native(e.reason), **result)
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
    client = radarr.MovieApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_movie(module.params['tmdb_id'], result)
    if state:
        result.update(state.dict(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_movie(result)

    # Set wanted resource.
    want = radarr.MovieResource(**{
        'title': module.params['title'],
        'monitored': module.params['monitored'],
        'quality_profile_id': module.params['quality_profile_id'],
        'tmdb_id': module.params['tmdb_id'],
        'path': module.params['path'],
        'minimum_availability': module.params['minimum_availability'],
        'root_folder_path': module.params['root_folder_path'],
        'tags': module.params['tags'],
        'add_options': radarr.AddMovieOptions(**{
            'monitor': 'movieOnly',
            'search_for_movie': True,
        }),
    })

    # Create a new resource if needed.
    if result['id'] == 0:
        create_movie(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want):
        update_movie(want, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
