#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_quality_profile

short_description: Manages Radarr quality profile.

version_added: "1.0.0"

description: Manages Radarr quality profile.

options:
    name:
        description: Name.
        required: true
        type: str
    upgrade_allowed:
        description: Upgrade allowed flag.
        type: bool
        default: False
    cutoff:
        description: Quality ID to which cutoff.
        type: int
    cutoff_format_score:
        description: Cutoff format score.
        type: int
        default: 0
    min_format_score:
        description: Min format score.
        type: int
        default: 0
    min_upgrade_format_score:
        description: Min upgrade format score.
        type: int
        default: 1
    language:
        description: Language.
        type: dict
        suboptions:
            name:
                description: Language name.
                type: str
            id:
                description: Language ID.
                type: int
    quality_groups:
        description: Quality groups ordered list. Define only the allowed groups.
        type: list
        elements: dict
        default: []
        suboptions:
            name:
                description: Quality group name.
                type: str
            id:
                description: Quality group ID.
                type: int
            qualities:
                description: Quality list.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Quality name.
                        type: str
                    resolution:
                        description: Quality resolution.
                        type: str
                    source:
                        description: Quality source.
                        type: str
                    id:
                        description: Quality ID.
                        type: int
    formats:
        description: Format items list. Define only the used custom formats.
        type: list
        elements: dict
        default: []
        suboptions:
            name:
                description: Format name.
                type: str
            id:
                description: Format ID.
                type: int
            score:
                description: Format score.
                type: int

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials
    - devopsarr.radarr.radarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a quality profile
- name: Create a quality profile
  devopsarr.radarr.radarr_quality_profile:
    name: "Example"
    upgrade_allowed: true
    cutoff: 1
    min_format_score: 0
    cutoff_format_score: 0
    min_upgrade_format_score: 1
    language:
        name: Any
        id: -1
    quality_groups:
      - qualities:
        - id: 1
          name: "SDTV"
          source: "television"
          resolution: 480
      - name: "WEB 720p"
        id: 1001
        qualities:
          - id: 14
            name: "WEBRip-720p"
            source: "webRip"
            resolution: 720
          - id: 5
            name: "WEBDL-720p"
            source: "web"
            resolution: 720
    formats: []

# Delete a quality profile
- name: Delete a quality_profile
  devopsarr.radarr.radarr_quality_profile:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Quality Profile ID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: Example
upgrade_allowed:
    description: Upgrade allowed flag.
    returned: always
    type: bool
    sample: false
cutoff:
    description: Quality ID to which cutoff.
    returned: always
    type: int
    sample: 1
cutoff_format_score:
    description: Cutoff format score.
    returned: always
    type: int
    sample: 0
min_format_score:
    description: Min format score.
    returned: always
    type: int
    sample: 0
min_upgrade_format_score:
    description: Min upgrade format score.
    returned: always
    type: int
    sample: 1
language:
    description: Language.
    returned: always
    type: dict
    sample:
        name: Any
        id: -1
items:
    description: Quality groups
    returned: always
    type: list
    elements: dict
    sample: []
format_items:
    description: Format items list.
    returned: always
    type: list
    elements: dict
    sample: []
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
        name=dict(type='str', required=True),
        cutoff=dict(type='int'),
        min_format_score=dict(type='int', default=0),
        min_upgrade_format_score=dict(type='int', default=1),
        cutoff_format_score=dict(type='int', default=0),
        upgrade_allowed=dict(type='bool', default=False),
        language=dict(type='dict', options=dict(
            name=dict(type='str'),
            id=dict(type='int'))),
        quality_groups=dict(type='list', elements='dict', default=[]),
        formats=dict(type='list', elements='dict', default=[], options=dict(
            name=dict(type='str'),
            id=dict(type='int'),
            score=dict(type='int'))),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_quality_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_quality_profile(quality_profile_resource=want)
        except radarr.ApiException as e:
            module.fail_json('Error creating quality profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating quality profile: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_quality_profiles(result):
    try:
        return client.list_quality_profile()
    except radarr.ApiException as e:
        module.fail_json('Error listing quality profiles: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing quality profiles: {}'.format(to_native(e)), **result)


def find_quality_profile(name, result):
    for profile in list_quality_profiles(result):
        if profile.name == name:
            return profile
    return None


def update_quality_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_quality_profile(quality_profile_resource=want, id=str(want.id))
        except radarr.ApiException as e:
            module.fail_json('Error updating quality profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating quality profile: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_quality_profile(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_quality_profile(result['id'])
            except radarr.ApiException as e:
                module.fail_json('Error deleting quality profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting quality profile: {}'.format(to_native(e)), **result)
            result['id'] = 0
    module.exit_json(**result)


def populate_quality_groups(result):
    # Needed for both disallowed qualities and modifier
    temp_client = radarr.QualityDefinitionApi(module.api)
    # GET resources.
    try:
        all_qualities = temp_client.list_quality_definition()
    except radarr.ApiException as e:
        module.fail_json('Error listing qualities: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing qualities: {}'.format(to_native(e)), **result)

    quality_groups = []
    allowed_qualities = []
    for item in module.params['quality_groups']:
        if len(item['qualities']) == 1:
            for q in all_qualities:
                if item['qualities'][0]['id'] == q.quality.id:
                    quality_groups.append(radarr.QualityProfileQualityItemResource(
                        quality=radarr.Quality(
                            id=item['qualities'][0]['id'],
                            name=item['qualities'][0]['name'],
                            source=item['qualities'][0]['source'],
                            resolution=item['qualities'][0]['resolution'],
                            modifier=q.quality.modifier,
                        ),
                        items=[],
                        allowed=True,
                    ))
                    allowed_qualities.append(item['qualities'][0]['id'])
        else:
            qualities = []
            for quality in item['qualities']:
                for q in all_qualities:
                    if quality['id'] == q.quality.id:
                        qualities.append(radarr.QualityProfileQualityItemResource(
                            quality=radarr.Quality(
                                id=quality['id'],
                                name=quality['name'],
                                source=quality['source'],
                                resolution=quality['resolution'],
                                modifier=q.quality.modifier,
                            ),
                            allowed=True,
                            items=[]
                        ))
                        allowed_qualities.append(quality['id'])

            quality_groups.append(radarr.QualityProfileQualityItemResource(
                allowed=True,
                name=item['name'],
                id=item['id'],
                items=qualities,
            ))

    # Add disallowed qualities
    for q in all_qualities[::-1]:
        if q.quality.id not in allowed_qualities:
            quality_groups.insert(0, radarr.QualityProfileQualityItemResource(
                quality=radarr.Quality(
                    id=q.quality.id,
                    name=q.quality.name,
                    source=q.quality.source,
                    resolution=q.quality.resolution,
                    modifier=q.quality.modifier,
                ),
                items=[],
                allowed=False,
            ))

    return quality_groups


def populate_formats(result):
    formats = []
    used_formats = []
    for item in module.params['formats']:
        formats.append(radarr.ProfileFormatItemResource(
            name=item['name'],
            format=item['id'],
            score=item['score'],
        ))
        used_formats.append(item['id'])

    # Add unused formats
    temp_client = radarr.CustomFormatApi(module.api)
    # GET resources.
    try:
        all_formats = temp_client.list_custom_format()
    except radarr.ApiException as e:
        module.fail_json('Error listing formats: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing formats: {}'.format(to_native(e)), **result)

    for f in all_formats:
        if f.id not in used_formats:
            formats.append(radarr.ProfileFormatItemResource(
                name=f.name,
                format=f.id,
                score=0,
            ))

    return formats


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = radarr.QualityProfileApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_quality_profile(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_quality_profile(result)

    # Populate quality groups and formats.
    quality_groups = populate_quality_groups(result)
    formats = populate_formats(result)

    # Set wanted resource.
    want = radarr.QualityProfileResource(
        name=module.params['name'],
        cutoff=module.params['cutoff'],
        upgrade_allowed=module.params['upgrade_allowed'],
        cutoff_format_score=module.params['cutoff_format_score'],
        min_format_score=module.params['min_format_score'],
        min_upgrade_format_score=module.params['min_upgrade_format_score'],
        language=radarr.Language(
            name=module.params['language']['name'],
            id=module.params['language']['id'],
        ),
        items=quality_groups,
        format_items=formats,
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_quality_profile(want, result)

    # Update an existing resource.
    want.id = result['id']
    if want != state:
        update_quality_profile(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
