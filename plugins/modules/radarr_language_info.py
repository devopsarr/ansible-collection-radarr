#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: radarr_language_info

short_description: Get information about Radarr language.

version_added: "1.0.0"

description: Get information about Radarr language.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.radarr.radarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all languages.
- name: Gather information about all languages
  devopsarr.radarr.radarr_language_info:

# Gather information about a single language.
- name: Gather information about a single language
  devopsarr.radarr.radarr_language_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
languages:
    description: A list of languages.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: language ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
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
        name=dict(type='str'),
    )


def list_languages(result):
    try:
        return client.list_language()
    except Exception as e:
        module.fail_json('Error getting languages: %s' % to_native(e.reason), **result)


def populate_languages(result):
    languages = []
    # Check if a resource is present already.
    for language in list_languages(result):
        if module.params['name']:
            if language.name == module.params['name']:
                languages = [language.model_dump(by_alias=False)]
        else:
            languages.append(language.model_dump(by_alias=False))
    return languages


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = RadarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = radarr.LanguageApi(module.api)
    result = dict(
        changed=False,
        languages=[],
    )

    # List resources.
    result.update(languages=populate_languages(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
