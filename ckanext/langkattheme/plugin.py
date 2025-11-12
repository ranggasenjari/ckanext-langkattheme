from typing import Any, cast
from ckan.types import Context, Schema, Validator, ValidatorFactory
import logging


from ckan.common import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import json


import ckanext.langkattheme.cli as cli
# import ckanext.langkattheme.helpers as helpers
# import ckanext.langkattheme.views as views
# from ckanext.langkattheme.logic import (
#     action, auth, validators
# )

def group_list():
    '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'title asc', 'all_fields': True, 'include_dataset_count': False})

    # Truncate the list to the 10 most popular groups only.
    # groups = groups[:10]

    return groups

def format_number(number):
    formatted = "{:,.0f}".format(number).replace(",", ".")
    return formatted


def get_visualization():
    return config.get('ckanext.langkattheme.visualization', '')

def get_metadata_fields():
    metafields = config.get('ckanext.langkattheme.metadata_fields', '')
    if not metafields:
        return []
    return json.loads(metafields)

def get_metadata_keys_fields():
    metafields = get_metadata_fields()
    return [item['key'] for item in metafields]

def get_metadata_object(extras, key):
    result = {}
    for item in extras:
        if item['key'] == key:
            result = item
            break  # Keluar dari loop setelah menemukan yang cocok
    return result

def get_metadata_object_val(extras, key):
    obj = get_metadata_object(extras, key)
    if ( 'value' in obj ) :
        return obj['value']
    return None

def prepare_metadata_form():
    custom_fields = {}
    metakeys = get_metadata_keys_fields()
    for key in metakeys :
        custom_fields[key] = [
            toolkit.get_converter('convert_from_extras'),
            toolkit.get_validator('ignore_missing')
        ]
    return custom_fields

class LangkatthemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    
    # plugins.implements(plugins.IAuthFunctions)
    # plugins.implements(plugins.IActions)
    # plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.ITemplateHelpers)
    # plugins.implements(plugins.IValidators)
    

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "langkattheme")

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')

        schema.update({
            'ckanext.langkattheme.visualization': [ignore_missing, unicode_safe],
            'ckanext.langkattheme.metadata_fields': [ignore_missing, unicode_safe],
        })

        return schema
    
    # IAuthFunctions

    # def get_auth_functions(self):
    #     return auth.get_auth_functions()

    # IActions

    # def get_actions(self):
    #     return action.get_actions()

    # IBlueprint

    # def get_blueprint(self):
    #     return views.get_blueprints()

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # ITemplateHelpers

    def get_helpers(self):
        '''Register the group_list() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'langkattheme_group_list': group_list,
            'langkattheme_format_number' : format_number, 
            'langkattheme_get_visualization': get_visualization,
            'langkattheme_get_metadata_fields': get_metadata_fields,
            'langkattheme_get_metadata_keys_fields': get_metadata_keys_fields,
            'langkattheme_get_metadata_object': get_metadata_object,
            'langkattheme_get_metadata_object_val': get_metadata_object_val,
        }

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True
    
    def package_types(self) -> list[str]:
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
    
    def _modify_package_schema(self, schema: Schema):
        # for _key in get_metadata_keys_fields() :
        #     schema.update({
        #         _key : [toolkit.get_validator('ignore_missing'),
        #             toolkit.get_converter('convert_to_extras')]
        #         })
        
        # # # Add our custom_resource_text metadata field to the schema
        # # cast(Schema, schema['resources']).update({
        # #         'custom_resource_text' : [ toolkit.get_validator('ignore_missing') ]
        # #         })

        self.write_log('_modify_package_schema')
        self.write_log(schema['resources'])

        return schema
    
    def create_package_schema(self) -> Schema:
        self.write_log('create_package_schema')
        schema: Schema = super(LangkatthemePlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self) -> Schema:
        self.write_log('update_package_schema')
        schema: Schema = super(LangkatthemePlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self) -> Schema:
        self.write_log('show_package_schema updated')
        schema: Schema = super(LangkatthemePlugin, self).show_package_schema()        
        # schema = self._modify_package_schema(schema)
        self.write_log(schema)

        return schema
    
    def write_log(self, object):
        logger = logging.getLogger(__name__)
        logger.debug(object)

    # 
    # def before_create(self, context, pkg_dict):
    #     '''Callback sebelum package dibuat'''
    #     self._add_custom_fields(pkg_dict)

    # def before_update(self, context, pkg_dict):
    #     '''Callback sebelum package diupdate'''
    #     self._add_custom_fields(pkg_dict)

    # def _add_custom_fields(self, pkg_dict):
    #     '''Menambahkan field ekstra dinamis ke dalam package'''
    #     # Ambil konfigurasi field ekstra dari JSON atau sumber konfigurasi lainnya
    #     for _key in get_metadata_keys_fields() :
    #         pkg_dict["extras"].append({"key": _key, "value": ""})