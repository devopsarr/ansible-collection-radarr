#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_media_management_info

short_description: Get information about Radarr media management.

version_added: "1.0.0"

description: Get information about Radarr media management.

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch media management
- name: fetch media management info
  devopsarr.radarr.radarr_media_management_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Media management ID.
    type: int
    returned: always
    sample: '1'
chmod_folder:
    description: Permission in linux format.
    returned: always
    type: str
    sample: '755'
rescan_after_refresh:
    description: Rescan after refresh.
    returned: always
    type: str
    sample: 'afterManual'
recycle_bin:
    description: Bin path.
    returned: always
    type: str
    sample: '/tmp'
file_date:
    description: File date modification.
    returned: always
    type: str
    sample: 'localAirDate'
extra_file_extensions:
    description: Comma separated list of extra files extension to be imported.
    returned: always
    type: str
    sample: 'srt,info'
episode_title_required:
    description: Episode title required.
    returned: always
    type: str
    sample: 'bulkSeasonReleases'
download_propers_and_repacks:
    description: Download propers and repack.
    returned: always
    type: str
    sample: 'preferAndUpgrade'
chown_group:
    description: Linux group.
    returned: always
    type: str
    sample: 'arrs'
minimum_free_space_when_importing:
    description: Minimum free space when importing.
    returned: always
    type: int
    sample: '100'
recycle_bin_cleanup_days:
    description: Recycle bin days.
    returned: always
    type: int
    sample: '7'
auto_unmonitor_previously_downloaded_movies:
    description: Auto unmonitor previously downloaded movies.
    returned: always
    type: bool
    sample: 'true'
skip_free_space_check_when_importing:
    description: Skip free space check when importing.
    returned: always
    type: bool
    sample: 'true'
set_permissions_linux:
    description: Set linux permission flag.
    returned: always
    type: bool
    sample: 'true'
import_extra_files:
    description: Import extra files flag.
    returned: always
    type: bool
    sample: 'true'
enable_media_info:
    description: Enable media info flag.
    returned: always
    type: bool
    sample: 'true'
delete_empty_folders:
    description: Delete empty folders.
    returned: always
    type: bool
    sample: 'true'
create_empty_movie_folders:
    description: Create empty movie folder.
    returned: always
    type: bool
    sample: 'true'
auto_rename_folders:
    description: Auto rename folders.
    returned: always
    type: bool
    sample: 'true'
copy_using_hardlinks:
    description: Copy using hardlinks.
    returned: always
    type: bool
    sample: 'true'
paths_default_static:
    description: Paths default static.
    returned: always
    type: bool
    sample: 'true'
'''

from ansible_collections.devopsarr.radarr.plugins.module_utils.radarr_module import RadarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import radarr
    HAS_RADARR_LIBRARY = True
except ImportError:
    HAS_RADARR_LIBRARY = False


def get_media_management_config(result):
    try:
        return client.get_media_management_config()
    except Exception as e:
        module.fail_json('Error getting media management: %s' % to_native(e.reason), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.MediaManagementConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_media_management_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
