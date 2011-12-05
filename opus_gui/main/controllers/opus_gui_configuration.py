# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from lxml.etree import ElementTree, SubElement
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSplashScreen, QPixmap

from opus_core.misc import directory_path_from_opus_path
from opus_core import paths

class OpusGuiConfiguration(object):
    def __init__(self):
        self.application_title = 'OPUS' # correct default value?
        self.xml_node = None
        self.xml_filename = None
        self.splash_screen = None
        self.fonts = {'tabs': 10,
                      'menu': 10,
                      'general': 10}
        self.load_latest_on_start = False
        self.latest_project_filename = ''
        self.load_latest_tab_on_start = True
        self.latest_tab_index = ''

    def load(self, filename = None, create_if_missing = True):
        '''
        Load the gui configuration from default directory
        @param filename: Filename (String) of the XML to load. If its None, the
        default gui configuration is loaded
        @param create_if_missing (bool): Flag to create the destinated file if
        it's missing.
        '''
        # Open the GUI configuration file
        if filename is None:
            # Try the users default configuration file
            usr_conf_dir = paths.OPUS_SETTINGS_PATH 
            if not os.path.exists(usr_conf_dir):
                os.mkdir(usr_conf_dir)
            filename = os.path.join(usr_conf_dir, 'gui_config.xml')

        if not os.path.exists(filename):
            # Didn't have a custom gui-configuration -- copy the default one
            # into the location before loading it
            print('Warning -- did not find GUI configuration file %s.'%
                  filename)
            if not create_if_missing:
                print('Not loading any GUI configuration file')
                return
            print('Copying the default GUI configuration to %s'% filename)
            default_config_dir = directory_path_from_opus_path('opus_gui.main')
            default_config_filename = os.path.join(default_config_dir,
                                                'default_gui_configuration.xml')
            # open the file and write it to the destination
            try:
                gui_config_file = open(default_config_filename)
                user_config_file = open(filename, 'w')
                user_config_file.write(''.join(gui_config_file.readlines()))
                user_config_file.close()
                gui_config_file.close()
                # Clean up namespace
                del user_config_file, gui_config_file
            except IOError, ex:
                print('Failed to copy default configuration to %s.\n'
                      '-- Error:%s\n'
                      '!- Not loading any GUI configuration file.\n'%
                      (filename, ex))
                return

        root = ElementTree(file=filename)

        self.xml_node = root
        self.xml_filename = filename

        # GUI Setting -- Splash screen
        node = root.find('startup_options/splash_logo')
        if node is None:
            # TODO Use a default ?
            self.splash_screen = QSplashScreen(QPixmap())
            self.splash_screen.showMessage('OPUS')
        else:
            # Load user splash
            dir_ = directory_path_from_opus_path('opus_gui.main.views.Images')
            splash_abs_filename = os.path.join(dir_, node.text)
            splash_pix = QPixmap(splash_abs_filename)
            splash_pix = splash_pix.scaled(600,252, Qt.KeepAspectRatio)
            self.splash_screen = QSplashScreen(splash_pix)

        # GUI Setting -- Application Title
        node = root.find('application_options/application_title')
        if node is not None:
            self.application_title = node.text

        # GUI Setting -- Font sizes
        for group, node_name in [('menu', 'menu_font_size'),
                                 ('tabs', 'main_tabs_font_size'),
                                 ('general', 'general_text_font_size')]:
            try:
                node = root.find('font_settings/%s' %node_name)
                self.fonts[group] = int(node.text)
            except ValueError:
                print 'Could not set font %s to "%s"' %(group, node.text or '')

        # GUI Setting -- Previous projects
        node = root.find('project_history/previous_project')
        if node is not None:
            self.latest_project_filename = node.text
        node = root.find('project_history/open_latest_project_on_start')
        if node is not None:
            self.load_latest_on_start = (node.text == "True")
        node = root.find('project_history/previous_tab')
        if node is not None:
            self.latest_tab_index = node.text
        node = root.find('project_history/open_latest_tab_on_start')
        if node is not None:
            self.load_latest_tab_on_start = (node.text == "True")

    def save(self):
        ''' Save the GUI configuration file to disk'''
        if self.xml_node is None:
            print('Warning -- Tried to save a GUI configuration that is not '
                  'loaded')
            return

        # Update font settings
        font_settings_node = self.xml_node.find('font_settings')
        pairs = [('menu', 'menu_font_size'),
                 ('tabs', 'main_tabs_font_size'),
                 ('general', 'general_text_font_size')]
        for group, node_name in pairs:
            font_settings_node.find(node_name).text = str(self.fonts[group])

        # Update latest project history
        proj_hist_node = self.xml_node.find('project_history')
        open_latest_node = proj_hist_node.find('open_latest_project_on_start')
        prevproj_node = proj_hist_node.find('previous_project')
        open_latest_tab_node = proj_hist_node.find('open_latest_tab_on_start')
        if open_latest_tab_node is None:
            open_latest_tab_node = SubElement(proj_hist_node, 'open_latest_tab_on_start')
        prevtab_node = proj_hist_node.find('previous_tab')
        if prevtab_node is None:
            prevtab_node = SubElement(proj_hist_node, 'previous_tab')

        # Ensure that the value is 'True' or 'False'
        open_latest_node.text = self.load_latest_on_start and 'True' or 'False'
        prevproj_node.text = self.latest_project_filename
        open_latest_tab_node.text = self.load_latest_tab_on_start and 'True' or 'False'
        prevtab_node.text = self.latest_tab_index

        # Write config to disk
        self.xml_node.write(self.xml_filename)

