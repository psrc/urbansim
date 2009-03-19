# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from xml.etree.cElementTree import Element

from PyQt4.QtGui import QMenu, QCursor
from opus_gui.main.controllers.dialogs.message_box import MessageBox

from opus_gui.results_manager.controllers.dialogs.add_indicator_batch import AddIndicatorBatch
from opus_gui.results_manager.controllers.dialogs.get_run_info import GetRunInfo
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.results_manager.controllers.dialogs.configure_existing_batch_indicator_visualization import ConfigureExistingBatchIndicatorVisualization
from opus_gui.results_manager.controllers.dialogs.configure_new_batch_indicator_visualization import ConfigureNewBatchIndicatorVisualization
from opus_gui.results_manager.controllers.dialogs.indicator_batch_run_form import IndicatorBatchRunForm
from opus_gui.results_manager.results_manager_functions import get_available_run_nodes, get_run_manager

class XmlController_Results(XmlController):
    ''' XmlController for the Results Manager '''

    def __init__(self, manager):
        XmlController.__init__(self, manager)

        i = self.model.acceptIcon
        t = "Add new indicator batch..."
        def show_add_batch_dialog():
            w = AddIndicatorBatch(callback = self._add_indicator_batch_callback,
                                  parent_widget = self.view)
            w.show()
        c = show_add_batch_dialog
        self.actAddNewIndicatorBatch = self.createAction(i, t, c)
        t =  'Add new indicator visualization...'
        c =  self._configureNewBatchIndicatorVisualization
        self.actAddVisualizationToBatch = self.createAction(i, t, c)
        t =  "Configure visualization"
        c = self._configureExistingBatchIndicatorVisualization
        self.actConfigureExistingBatchIndicatorVis = self.createAction(i, t, c)
        t =  "Show details"
        c = self._getInfoSimulationRuns
        self.actGetInfoSimulationRuns = self.createAction(i, t, c)
        t =  "Import run from disk"
        c = self._importRun
        self.actImportRun = self.createAction(i, t, c)

        i = self.model.removeIcon
        t = "Remove run and delete from hard drive..."
        c = self._delete_selected_run
        self.actDeleteRun = self.createAction(i, t, c)

    def _add_indicator_batch_callback(self, batch_name):
        '''
        Callback from the add indicator batch dialog.
        @param batch_name (String): the indicator batch name
        '''
        # Create a new node with the given name and insert it into the model
        node = Element(batch_name, {'type': 'indicator_batch'})
        self.model.add_node_to_path('Indicator_batches', node)

    def _configureNewBatchIndicatorVisualization(self):#, viz = None):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        batch_node = self.selectedItem().node

        window = ConfigureNewBatchIndicatorVisualization(self.project,
                                                         batch_node,
                                                         self.view)
        window.show()

    def _configureExistingBatchIndicatorVisualization(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        viz_node = self.selectedItem().node
        window = ConfigureExistingBatchIndicatorVisualization(self.project,
                                                              viz_node,
                                                              self.view)
        window.show()

    def _delete_selected_run(self):
        ''' Remove the selected run '''
        assert self.hasSelectedItem()
        self.delete_run(self.selectedItem().node)

    def delete_run(self, run_node):
        '''
        Remove a run both from the services database and from the model.
        @param run_node (Element): the node to remove.
        '''
        # Prevent the user from removing base years
        cache_directory = run_node.find('cache_directory').text
        if cache_directory.endswith('base_year_data'):
            msg = ('Removing the base year data directory is restricted from '
                   'within OpusGUI since doing so will make it impossible to '
                   'run any simulations or estimations.')
            MessageBox.warning(mainwindow = self.view,
                               text = 'Cannot remove base year data',
                               detailed_text  = msg)
            return
        try:
            run_manager = get_run_manager()
            run_id = int(run_node.find('run_id').text)
            run_manager.delete_everything_for_this_run(run_id, cache_directory)
            run_manager.close()
            self.model.remove_node(run_node)
        except Exception, ex:
            MessageBox.warning(self.view, 'Could not remove run', str(ex))

    def _importRun(self):
        ''' NO DOCUMENTATION '''
        self.manager.importRun()

    def _createBatchRunMenu(self, attach_to_menu):
        '''
        Create and populate a 'Run indicator batch' menu for all available runs
        @param attach_to_menu (QMenu) menu to attach actions to
        '''
        # TODO Verify that this is correct -- it was based on looking in a xml
        # file for 'source_data' and Simulation_runs was the only section I
        # could find it in.
        run_nodes = get_available_run_nodes(self.project)

        if not run_nodes:
            attach_to_menu.setEnabled(False)
            return

        #T: the following loop causes a problem where
        #   only "baseyear_data" will be passed to the _indicatorBatchRun method.
        #   I don't know why.

#        for run_node in run_nodes:
#            cb = lambda x = run_node: self._indicatorBatchRun(run_name = run_node.tag)
#            action = self.createAction(self.model.acceptIcon, run_node.tag, cb)
#            attach_to_menu.addAction(action)

        #T:  The following loop works, but its kind of a nasty method.
        for i in range(len(run_nodes)):
            exec 'cb%i=lambda x = run_nodes[%i]: self._indicatorBatchRun(run_name = run_nodes[%i].tag)'%(i,i,i) in locals()
            exec 'action%i=self.createAction(self.model.acceptIcon, run_nodes[%i].tag, cb%i)'%(i,i,i) in locals()
            exec 'attach_to_menu.addAction(action%i)'%i in locals()

    def _indicatorBatchRun(self, run_name):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        node = self.selectedItem().node

        window = IndicatorBatchRunForm(mainwindow = self.view,
                                       resultsManagerBase = self.manager,
                                       batch_name = node.tag,
                                       run_name = run_name)
        window.show()

    def _getInfoSimulationRuns(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        node = self.selectedItem().node
        window = GetRunInfo(node, self.view)
        window.show()

    def _viewDocumentation(self):
        ''' NO DOCUMENTATION '''
        pass

    def processCustomMenu(self, point):
        ''' NO DOCUMENTATION '''
        item = self.selectItemAt(point)
        if not item:
            return

        node = item.node
        menu = QMenu(self.view)

        # Populate menu
        if node.get('type') == 'source_data':
            menu.addAction(self.actGetInfoSimulationRuns)
            menu.addAction(self.actDeleteRun)
        elif node.tag == 'Indicator_batches':
            menu.addAction(self.actAddNewIndicatorBatch)
        elif node.tag == 'Simulation_runs':
            menu.addAction(self.actImportRun)
        elif node.get('type') == 'indicator_batch':
            # For indicator batches we want to be able to add new visualizations
            # as well as a sub menu for selecting cached runs to run the batch on
            menu.addAction(self.actAddVisualizationToBatch)
            run_batch_on_menu = QMenu('Run indicator batch on...')
            self._createBatchRunMenu(run_batch_on_menu)
            menu.addMenu(run_batch_on_menu)

        elif node.get('type') == 'batch_visualization':
            menu.addAction(self.actConfigureExistingBatchIndicatorVis)

        self.addDefaultMenuItems(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

#    def beforeAddIndicatorToBatchShown(self):
#        #batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
#        #existing_indicators = self.xml_helper.get_indicators_in_indicator_batch(batch_name)
#
#        available_indicators = self.xml_helper.get_available_indicator_names()
#
#        self.indicator_batch_menu.clear()
#        for indicator_info in available_indicators:
#            indicator_name = indicator_info['name']
##            if indicator_name in existing_indicators:
##                continue
#            indicator = QString(indicator_name)
#            act_indicator = QAction(self.acceptIcon,
#                                    indicator_name,
#                                    self.indicator_batch_menu)
#            callback = lambda indicator=indicator: self.addIndicatorToBatch(indicator)
#            QObject.connect(act_indicator, SIGNAL("triggered()"), callback)
#            self.indicator_batch_menu.addAction(act_indicator)
#
#    def addIndicatorToBatch(self, indicator):
#        batch_name = self.currentIndex.internalPointer().node().toElement().tagName()
#        self.xml_helper.addIndicatorToBatch(batch_name = batch_name,
#                                            indicator_name = indicator)



#    def _build_indicator_batch_menu(self):
#        #needs to be called when indicator_batch right clicked on...
##        self.indicator_batch_menu = QMenu(self.mainwindow)
##        self.indicator_batch_menu.setTitle(QString("Add new indicator visualization..."))
#
#
#
#        available_visualizations = self.xml_helper.get_visualization_options()
#
#        for viz in available_visualizations.keys():
#            viz = QString(viz)
#            act_viz = QAction(self.acceptIcon,
#                                    viz,
#                                    self.indicator_batch_menu)
#            callback = lambda viz=viz: self._configureNewBatchIndicatorVisualization(viz)
#            QObject.connect(act_viz, SIGNAL("triggered()"), callback)
#            self.indicator_batch_menu.addAction(act_viz)
#
#        self.menu.addMenu(self.indicator_batch_menu)
#
#
#        self.run_indicator_batch_menu = QMenu(self.mainwindow)
#        self.run_indicator_batch_menu.setTitle(QString('Run indicator batch on...'))
#        QObject.connect(self.run_indicator_batch_menu, SIGNAL('aboutToShow()'), self._createBatchRunMenu)
#
#        self.menu.addMenu(self.run_indicator_batch_menu)
