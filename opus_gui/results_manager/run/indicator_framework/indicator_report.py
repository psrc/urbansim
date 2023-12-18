# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, csv

from opus_gui.main.opus_project import OpusProject
from opus_gui.results_manager.run.batch_processor import BatchProcessor
from opus_gui.results_manager.results_manager_functions import get_batch_configuration
from opus_core import paths

OPUSHOME = paths.OPUS_HOME
PROJECTCONFIGBASE = paths.OPUS_PROJECT_CONFIGS_PATH

class IndicatorReport:
    def __init__(self, indicators):
        self.indicators = indicators
    
    def generate_indicators(self):
        self.filepaths = {}

        for name, (projconfig, batchname, visname, datasourcename, year) in list(self.indicators.items()):
            op = OpusProject()
            op.open(os.path.join(PROJECTCONFIGBASE, projconfig))
        
            bp = BatchProcessor(op)
            visualizationsconf = get_batch_configuration(project = op, batch_name = batchname, vis_name = visname)
            bp.set_data(visualizations = visualizationsconf, source_data_name = datasourcename, years = [year,year])
            bp.run()
            
            visualizations = bp.get_visualizations()
        
            # visualizations in batch
            assert len(visualizations) == 1
            vistype, visualizations = visualizations[0]
            # indicators in visualization
            assert len(visualizations) == 1
            self.filepaths[name] = visualizations[0].get_file_path()
            
    def move_files(self, filepaths, reportdir, reportname):
        if not os.path.exists(reportdir): os.mkdir(reportdir)
        reportdir = os.path.join(reportdir,reportname)
        if not os.path.exists(reportdir): os.mkdir(reportdir)
            
        # should move the files into the directory so that it can just be zipped up for shipment
        for name, file in filepaths.items():
            import shutil
            newfile = os.path.join(reportdir,os.path.basename(file))
            shutil.copy(file,newfile)
            self.filepaths[name] = newfile

class ReportSpec():
    def __init__(self, outputf):
        self.f = outputf 
    
    def writeheader(self):
        self.f.write('<HTML>')
        self.f.write('<HEAD><link rel="StyleSheet" href="http://www.chives.de/style/chives-tables.css" type="text/css"></HEAD>')
    
    def writeindicatortable(self, rows, mapindicatornametocell, title=None, dims=None, headers=None):
        self.f.write('<TABLE>\n')
        if title: self.f.write('<caption>%s</caption>'%title)
        if headers:
            self.f.write('  <TR>\n')
            for item in headers:
                self.f.write('    <TH>%s\n'%item)    
        for row in rows:
            self.f.write('  <TR>\n')
            for item in row:
                self.f.write('    <TD align=center>%s\n'%mapindicatornametocell(item))
        self.f.write('</TABLE><br><br>')
        
    def writesimpletable(self, tabf, title=None, numrows=-1):
        dr = csv.DictReader(open(tabf), delimiter='\t')
        self.f.write('<TABLE>\n')
        if title: self.f.write('<caption>%s</caption>'%title)
        self.f.write('  <TR>\n')
        for item in dr.fieldnames:
            self.f.write('    <TH>%s\n'%item) 
        for row in dr:
            self.f.write('  <TR>\n')
            for item in dr.fieldnames:
                self.f.write('    <TD align=center>%s\n'%row[item])
            if numrows != -1: numrows-=1
            if numrows == 0: break
        self.f.write('  <TR><TD align=center colspan=%d><A HREF="%s">Get full data file...</A>' % (len(dr.fieldnames),os.path.basename(tabf)))
        self.f.write('</TABLE><br><br>')
        
    def writefooter(self):
        self.f.write('</HTML>')