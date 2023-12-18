# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from PyQt4.QtGui import QIcon

class IconLibrary(object):
    '''
    A static library for accessing images in OpusGUI.

    The simplest function, icon(), takes a name (no path and no extension) of an image and
    returns the QIcon for it (an empty QIcon is returned when the image was not found).
    Example:
       IconLibrary.icon('cog') resolves to: QIcon(':Images/Images/cog.png')

    The library also holds a set of alias for fetching common icons.
    These are accessed through constants with the prefix 'STD_ICON_'
    Some examples:
       IconLibrary.STD_ICON_SUB_MODEL => IconLibrary.icon('bluecog')
       IconLibrary.STD_ICON_EDIT_ACTION
       IconLibrary.STD_ICON_DELETE_ACTION
    '''
    _PATH = ':Images/Images/'   # resource path to images
    _EXTENSION = 'png'          # extension to assume (without the dot)

    # Avoid loading a new icon into memory every time one is requested by placing them in a cache
    # on the first load
    __cached_icons = {}

# Todo --  replace these fields in XmlModel with load calls to IconLibrary.icon()

    @classmethod
    def _get_image_path(cls, image_name):
        image_name = '%s.%s' % (image_name, cls._EXTENSION)
        return os.path.join(IconLibrary._PATH, image_name)

    @classmethod
    def icon(cls, image_name):
        '''
        Returns a QIcon for the given name.
        The name is prefixed with IconLibrary._PATH and suffixed with IconLibrary._EXTENSION
        (':Images/Images' and 'png' respectively)
        @param image_name (str) the name of the image to get
        @return the icon (QIcon) containing the given image (empty QICons are return when the image
        is not found)
        '''
        if not image_name in cls.__cached_icons:
            image_path = cls._get_image_path(image_name)
            icon = QIcon(image_path)
            if not icon:
                print('no icon %s' % image_path)
                icon = QIcon()
            cls.__cached_icons[image_name] = icon
        return cls.__cached_icons[image_name]

    @classmethod
    def icon_for_type(cls, type_name):
        '''
        Return the icon that is mapped to the given type_name
        @param type_name (str) the type to get icon for
        @return the icon (QIcon) for the given type
        '''
        if type_name in cls.NODE_TYPE_TO_ICON_NAME:
            return cls.icon(cls.NODE_TYPE_TO_ICON_NAME[type_name])
        return cls.icon('bullet_black')

    # Mapping of node types to their respective icons
    NODE_TYPE_TO_ICON_NAME =  {
        '': 'bullet_black',
        'all_source_data': 'folder',
        'boolean': 'bool',
        'cacheConfig': 'database_link',
        'configuration': 'configure',
        'class': 'class',
        'dataset': 'folder_database',
        'dictionary': 'dict',
        'dir_path': 'dir',
        'directory': 'dir',
        'file': 'page_white',
        'float': 'float',
        'group': 'folder',
        'indicator': 'table',
        'indicator_group': 'folder',
        'indicator_library': 'folder',
        'indicator_result': 'map_go',
        'integer': 'int',
        'list': 'list',
        'model': 'model',
        'model_choice': 'model',
        'password': 'password',
        'path': 'folder_database',
        'scenario': 'chart_organisation',
        'selectable_list': 'selectable_list',
        'source_data': 'database',
        'string': 'string',
        'quoted_string': 'string',
        'submodel': 'submodel',
        'table': 'table',
        'tool_config': 'wrench',
        'tool': 'wrench_orange',
        'tool_group': 'folder_wrench',
        'tool_library': 'bullet_black',
        'tool_set': 'folder_wrench',
        'tool_sets': 'bullet_black',
        'tuple': 'tuple',
        'unicode': 'string'
    }

if __name__ == '__main__':
    # TODO unit tests
    from PyQt4.QtGui import QApplication
    app = QApplication([], True)
    b = IconLibrary.icon('fisk')
    b2 = IconLibrary.icon('fisk')
    b4 = IconLibrary.icon('fisk')
    print('\n'.join(map(str, [b, b2,  b4])))
