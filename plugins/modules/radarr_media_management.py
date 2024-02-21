#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_media_management

short_description: Manages Radarr media management.

version_added: "1.0.0"

description: Manages Radarr media management.

options:
    chmod_folder:
        description: Permission in linux format.
        required: true
        type: str
    rescan_after_refresh:
        description: Rescan after refresh.
        required: true
        type: str
        choices: ["always", "afterManual", "never"]
    recycle_bin:
        description: Bin path.
        required: true
        type: str
    file_date:
        description: File date modification.
        required: true
        type: str
        choices: ["none", "cinemas", "release"]
    extra_file_extensions:
        description: Comma separated list of extra files extension to be imported.
        required: true
        type: str
    download_propers_and_repacks:
        description: Download propers and repack.
        required: true
        type: str
        choices: ["preferAndUpgrade", "doNotUpgrade", "doNotPrefer"]
    script_import_path:
        description: Import sctipt path.
        type: str
        default: ""
    chown_group:
        description: Linux group.
        required: true
        type: str
    minimum_free_space_when_importing:
        description: Minimum free space when importing.
        required: true
        type: int
    recycle_bin_cleanup_days:
        description: Recycle bin days.
        required: true
        type: int
    use_script_import:
        description: Use import script flag.
        type: bool
        default: false
    auto_unmonitor_previously_downloaded_movies:
        description: Auto unmonitor previously downloaded movies.
        required: true
        type: bool
    skip_free_space_check_when_importing:
        description: Skip free space check when importing.
        required: true
        type: bool
    set_permissions_linux:
        description: Set linux permission flag.
        required: true
        type: bool
    import_extra_files:
        description: Import extra files flag.
        required: true
        type: bool
    enable_media_info:
        description: Enable media info flag.
        required: true
        type: bool
    delete_empty_folders:
        description: Delete empty folders.
        required: true
        type: bool
    create_empty_movie_folders:
        description: Create empty movie folder.
        required: true
        type: bool
    copy_using_hardlinks:
        description: Copy using hardlinks.
        required: true
        type: bool
    auto_rename_folders:
        description: Auto rename folders.
        required: true
        type: bool
    paths_default_static:
        description: Paths default static.
        required: true
        type: bool

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update media management
- name: Update media management
  devopsarr.radarr.radarr_media_management:
    chmod_folder: "755"
    rescan_after_refresh: "always"
    recycle_bin: ""
    file_date: "cinemas"
    extra_file_extensions: "srt,info"
    download_propers_and_repacks: "doNotPrefer"
    chown_group: "arrs"
    minimum_free_space_when_importing: 100
    recycle_bin_cleanup_days: 7
    auto_unmonitor_previously_downloaded_movies: true
    skip_free_space_check_when_importing: true
    set_permissions_linux: true
    import_extra_files: true
    enable_media_info: true
    delete_empty_folders: true
    create_empty_movie_folders: true
    copy_using_hardlinks: true
    paths_default_static: false
    auto_rename_folders: true
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
download_propers_and_repacks:
    description: Download propers and repack.
    returned: always
    type: str
    sample: 'preferAndUpgrade'
script_import_path:
    description: Import sctipt path.
    returned: always
    type: str
    sample: ""
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
use_script_import:
    description: Use import script flag.
    returned: always
    type: bool
    sample: false
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
copy_using_hardlinks:
    description: Copy using hardlinks.
    returned: always
    type: bool
    sample: 'true'
auto_rename_folders:
    description: Auto rename folders.
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        chmod_folder=dict(type='str', required=True),
        rescan_after_refresh=dict(type='str', required=True, choices=["always", "afterManual", "never"]),
        recycle_bin=dict(type='str', required=True),
        file_date=dict(type='str', required=True, choices=["none", "cinemas", "release"]),
        extra_file_extensions=dict(type='str', required=True),
        download_propers_and_repacks=dict(type='str', required=True, choices=["preferAndUpgrade", "doNotUpgrade", "doNotPrefer"]),
        chown_group=dict(type='str', required=True),
        script_import_path=dict(type='str', default=""),
        minimum_free_space_when_importing=dict(type='int', required=True),
        recycle_bin_cleanup_days=dict(type='int', required=True),
        auto_unmonitor_previously_downloaded_movies=dict(type='bool', required=True),
        use_script_import=dict(type='bool', default=False),
        skip_free_space_check_when_importing=dict(type='bool', required=True),
        set_permissions_linux=dict(type='bool', required=True),
        import_extra_files=dict(type='bool', required=True),
        enable_media_info=dict(type='bool', required=True),
        delete_empty_folders=dict(type='bool', required=True),
        create_empty_movie_folders=dict(type='bool', required=True),
        copy_using_hardlinks=dict(type='bool', required=True),
        auto_rename_folders=dict(type='bool', required=True),
        paths_default_static=dict(type='bool', required=True),
    )


def read_media_management(result):
    try:
        return client.get_media_management_config()
    except Exception as e:
        module.fail_json('Error getting media management: %s' % to_native(e.reason), **result)


def update_media_management(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_media_management_config(media_management_config_resource=want, id="1")
        except Exception as e:
            module.fail_json('Error updating media management: %s' % to_native(e.reason), **result)
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
    client = radarr.MediaManagementConfigApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_media_management(result)
    if state:
        result.update(state.model_dump(by_alias=False))

    want = radarr.MediaManagementConfigResource(
        chmod_folder=module.params['chmod_folder'],
        rescan_after_refresh=module.params['rescan_after_refresh'],
        recycle_bin=module.params['recycle_bin'],
        script_import_path=module.params['script_import_path'],
        file_date=module.params['file_date'],
        extra_file_extensions=module.params['extra_file_extensions'],
        download_propers_and_repacks=module.params['download_propers_and_repacks'],
        chown_group=module.params['chown_group'],
        id=1,
        minimum_free_space_when_importing=module.params['minimum_free_space_when_importing'],
        recycle_bin_cleanup_days=module.params['recycle_bin_cleanup_days'],
        use_script_import=module.params['use_script_import'],
        auto_unmonitor_previously_downloaded_movies=module.params['auto_unmonitor_previously_downloaded_movies'],
        skip_free_space_check_when_importing=module.params['skip_free_space_check_when_importing'],
        set_permissions_linux=module.params['set_permissions_linux'],
        import_extra_files=module.params['import_extra_files'],
        enable_media_info=module.params['enable_media_info'],
        delete_empty_folders=module.params['delete_empty_folders'],
        create_empty_movie_folders=module.params['create_empty_movie_folders'],
        copy_using_hardlinks=module.params['copy_using_hardlinks'],
        auto_rename_folders=module.params['auto_rename_folders'],
        paths_default_static=module.params['paths_default_static'],
    )

    # Update an existing resource.
    if want != state:
        update_media_management(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
