#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#


from opus_core.configurations.dataset_description import DatasetDescription

try:
    from enthought.traits.api import Constant, Directory, Int, Str, Trait, List, ListInt, Bool, DictStrAny, File, Instance
    from enthought.traits.api import Item, Group, View, EnumEditor, Handler, TreeEditor, TreeNode, BooleanEditor
    # later update the ui import to:   from enthought.traits.ui.api import Item, Group, View, EnumEditor, Handler, TreeEditor, TreeNode, BooleanEditor
    from enthought.traits.ui.menu import Action, Menu, MenuBar, CloseAction, HelpAction
except:
    from opus_core.logger import logger
    logger.log_warning('Could not load traits.ui. Skipping %s!' % __file__)
else:
    import wx, os, sys, thread, webbrowser
    from threading import Thread
    import cPickle as pickle
    from copy import copy
    
    from opus_core.indicator_framework.core import IndicatorFactory
    from opus_core.indicator_framework.traits import TraitsSourceData

    from opus_core.indicator_framework.traits import TraitsAbstractIndicator
    from opus_core.indicator_framework.traits.traits_image_types \
        import TraitsMap, TraitsChart, TraitsTable, TraitsLorenz
    
    from opus_core.indicator_framework.utilities import display_message_dialog
    
    class TraitsIndicatorHandler(Handler):
        """Handler for creating indicators."""
        
        # *** traits *** 
        # traits specific to the configuration being edited.
        #
        # pickle_file is the name of the file in which the pickled configuration and handler are stored.
        # these are stored as a tuple (configuration,handler)
        pickle_file = File
        # updated is true if the config has been changed since the last save 
        # busy is true if a set of requests are currently being run.
        updated = Bool(False)
        busy = Bool(False)
        has_results = Bool(False)
        
        # constants
        wildcard_string = Constant("Opus files (*.opus)|*.opus|All files (*.*)|*.*")
        default_config_file_name = Constant("indicator_config.opus")
        
        source_data = Instance(TraitsSourceData)
        indicator = Instance(TraitsAbstractIndicator)
        
        file_name_for_indicator_results = Str('indicator_results.html')
        results_page = Str
        
        output_type = Str
        cross_scenario_comparison_enabled = Bool(False)
            
        def open_editor(self, package_order, location=None):
            """Open an editor on the indicator_config at the given location.  If location is None, 
            open the editor in the default position.  Return the ui for the editor."""
            
            self.source_data = TraitsSourceData(package_order)
            self.indicator = TraitsTable()
    
            return self.configure_traits(view = self._make_view(location), 
                                         context = {'source_data':self.source_data, 
                                                    'object':self.source_data,
                                                    'indicator':self.indicator})   
                 
        def _check_input_integrity(self,info, source_data):
            '''checks to make sure that info inputted by user is valid'''
            
            # check that all specified cachedirs and respective years exist...
            for cache_directory in [source_data.cache_directory, source_data.comparison_cache_directory]:
                if cache_directory == '': continue
                cache_directory = source_data.cache_directory
                if not os.path.exists(cache_directory):
                    display_message_dialog("Cache directory '%s' does not exist. Please enter a "
                            "valid cache directory path." % cache_directory)
                    return False
                    
                unfound_years = []
                for year in source_data.years:
                    year_cache_dir = os.path.join(cache_directory, str(year))
                    if not os.path.exists(year_cache_dir):
                        unfound_years.append(year)
                if len(unfound_years) > 0:
                    display_message_dialog("Cannot find directory for years %s in cache directory %s. "
                            "Please enter other years." % (','.join(unfound_years), cache_directory))
                    return False
            
            return True
            
        def do_run(self, info):
            '''Takes the indicator_configuration and indicator and sends it off to the indicator factory.'''
            source_data = self.source_data.detraitify()
            input_valid = self._check_input_integrity(info, source_data)
            if not input_valid: return
            
            indicator = self.indicator.detraitify(source_data)
            self._generate_indicator([indicator])
            #the following code enables threads whenever run requests is clicked
#            thread = Thread(target = self._generate_indicator, args = ([indicator],))
#            thread.start()

        def _generate_indicator(self, indicators):
            factory = IndicatorFactory()
            self.busy = True
            try:
                self.results_page = factory.create_indicators(
                    indicators,
                    show_results = False,
                    display_error_box = True)                
            except:
                display_message_dialog("Failed to generate indicator! Check the indicator log "
                        "in the indicators directory of the '%s' cache for further "
                        "details." % self.source_data.cache_directory)
            else:
                self.has_results = True
            
            self.busy = False

        def do_view_results(self, info):
            if self.has_results:
                webbrowser.open_new(self.results_page)
                
        # views
        def _make_view(self, location):
            # return a view customized for this handler 
            # location is either None, or a wx.Point that is the upper-left-hand corner of the new window
            #
            # menu & button items
            OpenAction = Action(name="Open ...", 
                                action="do_open")
            SaveAction = Action(name="Save", 
                                action="do_save", 
                                enabled_when="len(handler.pickle_file)>0")
            SaveAsAction = Action(name="Save as ...", 
                                  action="do_save_as")
            RevertAction = Action(name="Revert", 
                                  action="do_revert", 
                                  enabled_when="handler.updated and len(handler.pickle_file)>0")
            RunAction = Action(name="Run requests", 
                               action="do_run", 
                               enabled_when="not handler.busy")
            ResultsAction = Action(name="View results", 
                                   action="do_view_results", 
                                   enabled_when="handler.has_results and not handler.busy")
            #
            # menus
            file_menu = Menu(OpenAction, SaveAction, SaveAsAction, RevertAction, CloseAction, name='File')
            run_menu = Menu(RunAction, ResultsAction, name='Run')
            help_menu = Menu(HelpAction, name='Help')
            #
            # help strings
            #output_help = 'If checked, write the indicator results into the cache directory; otherwise write them into a separate directory'
            
            run_info = Group(
                Group(
                      Item('source_data.cache_directory', 
                           label = 'Cache directory',
                           width = 300)
                ), 
                Group(
                      Item('handler.cross_scenario_comparison_enabled', 
                           label = 'Compare to another cache directory?',
                           editor = BooleanEditor()
                       )
                ),
                Group(
                      Item('source_data.comparison_cache_directory', 
                           label = 'Comparison cache directory'),
                      visible_when = 'handler.cross_scenario_comparison_enabled'
                ),
                show_border=True,
                label='Scenario Information'
            )

            indicator_group = Group(
                Group(
                    Item('handler.output_type', 
                         label = 'Type',
                         editor = EnumEditor(
                                values=[
                                    'Comma-separated table',
                                    'Tab-separated table', 
                                    'Matplotlib map',
                                    'Chart',
                                    'Dbf table',
                                    'Lorenz curve'
                                ]),
                         style = 'simple',),
                ),
                Group(
                    Item('handler.indicator', 
                         style = 'custom', 
                         width = 450,
                         height = 175,
                         show_label = False),
                ),
                orientation = 'vertical',
                show_border = True,
                label = 'Indicator',
                )
                
            v = View(
                Group(run_info, 
                      indicator_group,
                      orientation = 'horizontal'
                      ),# layout='tabbed'),
                buttons = [RunAction, ResultsAction, CloseAction],
                menubar = MenuBar(file_menu, run_menu, help_menu),
                title='Indicator maker',
                scrollable=True,
                resizable=True,
                handler=self)
            
            if location is not None:
                v.x = location.x
                v.y = location.y
                
            return v
        
        def handler_output_type_changed(self, info):
            '''Change the type of the indicator when output_type changes'''
            new_output_type = info.handler.output_type
            if new_output_type == 'Tab-separated table':
                indicator = TraitsTable()
                indicator.output_type = 'tab'
            elif new_output_type == 'Comma-separated table':
                indicator = TraitsTable()
                indicator.output_type = 'csv'
            elif new_output_type == 'Matplotlib map':
                indicator = TraitsMap()
            elif new_output_type == 'Chart':
                indicator = TraitsChart()
            elif new_output_type == 'Dbf table':
                indicator = TraitsTable()
                indicator.output_type = 'dbf'
            elif new_output_type == 'Lorenz curve':
                indicator = TraitsLorenz()
            else:
                return
            
            #retain common values
            self.indicator.fill_indicator_with_basic_values(indicator)
            info.handler.indicator = indicator
                        
        ########## methods dealing with saving and loading previous configurations ############
        # override the setattr method to keep track of whether the object (i.e. the configuration) 
        # has been changed using the traits editor since the last save (see example p 35 of the Traits UI User Guide)
        def setattr(self, info, object, name, value):
            super(TraitsIndicatorHandler,self).setattr(info, object, name, value)
            # set flipped to true if we are changing 'updated' from False to True
            flipped = not(self.updated)
            self.updated = True
            if flipped:
                self._update_title(info)   
    
        def _update_title(self, info):
            # the title includes the name of the pickled file, and * if it needs saving
            if self.pickle_file=='':
                name = 'Untitled'
            else:
                name, ext = os.path.splitext(os.path.basename(self.pickle_file))
            if self.updated:
                mark = '*'
            else:
                mark = ''
            info.ui.title = name + mark + ' - Indicator maker'
    
        # methods to handle different menu and button actions
        def do_open(self,info):
            dlg = wx.FileDialog(None,
                                message="Open ...",
                                defaultFile=self.default_config_file_name,
                                style=wx.OPEN,
                                wildcard=self.wildcard_string)
            if dlg.ShowModal()==wx.ID_OK:
                name = dlg.GetPath()
                try:
                    f = open(name,'r')
                    (unpickled_config,unpickled_indicator, unpickled_handler) = pickle.load(f)
                    f.close()
                    # set the pickle file name of the unpickled_handler to the name of the file 
                    # just opened, since the file name isn't stored in the pickle file itself.  
                    # This doesn't count as making the handler dirty, so also set updated to false.
                    unpickled_handler.pickle_file = name
                    unpickled_handler.updated = False
                    
                    #replace state everytime for now, instead of creating new window...
                    self.copy_traits(unpickled_handler)
                    info.source_data.copy_traits(unpickled_config)
                    info.indicator.copy_traits(unpickled_indicator)
                    #for some reason, traits is not updating the self's source_data as well...
                    self.source_data.copy_traits(unpickled_config)
                    
                    self.pickle_file = name
                    self._update_title(info)
                    self.updated = False
                except pickle.UnpicklingError:
                    wx.MessageBox("%s is not a pickled configuration file." % self.file,
                              style=wx.OK | wx.ICON_EXCLAMATION)
            dlg.Destroy()
            
        def do_save(self,info):
            f = open(self.pickle_file,'w')
            # save a tuple (configuration,handler) into the pickle file
            pickle.dump((info.source_data, info.indicator, self), f)
            f.close()
            # mark the configuration as clean AFTER writing out the file
            # (In case there is an error in writing the file it won't be
            # marked as clean.)  The _updated field is automatically set
            # to False in the pickled copy that is written out by the 
            # IndicatorConfiguration's __getstate__ method.
            self.updated = False
            self._update_title(info)
            
        def do_save_as(self,info):
            dlg = wx.FileDialog(None,
                                message="Save configuration as ...",
                                defaultFile=self.default_config_file_name,
                                style=wx.SAVE | wx.OVERWRITE_PROMPT,
                                wildcard=self.wildcard_string)
            if dlg.ShowModal()==wx.ID_OK:
                self.pickle_file = dlg.GetPath()
                self.do_save(info)
            dlg.Destroy()
            
        def do_revert(self,info):
            # this button is only enabled when the pickle_file name is set and if updated is true
            filename = self.pickle_file
            f = open(filename, 'r')
            (unpickled_config,unpickled_handler) = pickle.load(f)
            f.close()
            info.object.copy_traits(unpickled_config)
            self.updated = False
            # update the title so that the * disappears, since it is no longer unsaved
            self._update_title(info)
        
