#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_movie_info

short_description: Get information about Radarr movie.

version_added: "1.0.0"

description: Get information about Radarr movie.

options:
    tmdb_id:
        description: TMDB ID.
        type: int

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all movie.
- name: Gather information about all movie
  devopsarr.radarr.radarr_movie_info:

# Gather information about a single movie.
- name: Gather information about a single movie
  devopsarr.radarr.radarr_movie_info:
    tmdb_id: 12345678
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
movie_list:
    description: A list of movie.
    returned: always
    type: list
    elements: dict
    contains:
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        tmdb_id=dict(type='int'),
    )


def list_movie(result):
    try:
        return client.list_movie()
    except radarr.ApiException as e:
        module.fail_json('Error listing movie: %s\n body: %s' % (to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing movie: %s' % to_native(e), **result)


def populate_movie(result):
    movie = []
    # Check if a resource is present already.
    for single_movie in list_movie(result):
        if module.params['tmdb_id']:
            if single_movie.tmdb_id == module.params['tmdb_id']:
                movie = [single_movie.model_dump(by_alias=False)]
        else:
            movie.append(single_movie.model_dump(by_alias=False))
    return movie


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
        movie_list=[],
    )

    # List resources.
    result.update(movie_list=populate_movie(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
