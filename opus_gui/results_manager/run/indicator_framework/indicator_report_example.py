# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from indicator_report import IndicatorReport, ReportSpec

def main():
    REPORTDIR = os.path.join(os.environ['OPUS_DATA_PATH'],'reports')
    REPORTNAME = 'testindicatorreport'
    
    # form is project config, batch name, vis name, data source name, year
    preconfigured_indicators = {
        'population': ('eugene_gridcell_default.xml', 'zone_indicator_batch', 'population', 'base_year_data', 1980),
        'jobs':  ('eugene_gridcell_default.xml', 'zone_indicator_batch', 'jobs', 'base_year_data', 1980),
        'population_density':  ('eugene_gridcell_default.xml', 'zone_indicator_batch', 'population_density', 'base_year_data', 1980),    
        'land_value':  ('eugene_gridcell_default.xml', 'zone_indicator_batch', 'land_value', 'base_year_data', 1980),
        'table':  ('eugene_gridcell_default.xml', 'zone_indicator_batch', 'gridcell_table', 'base_year_data', 1980),
    }
    
    ir = IndicatorReport(preconfigured_indicators)
    ir.generate_indicators()
    filepaths = ir.filepaths 
    
    import hardcoded_indicators
    hardcoded_visualizatons = hardcoded_indicators.go() 
    for key, value in hardcoded_visualizatons.items(): 
        filepaths[key] = value # hardcoded indicators are now available for display
    
    ir.move_files(filepaths,REPORTDIR,REPORTNAME)
    
    def mapindicatornametocell(name): 
        global filepaths
        if not name: return ''
        imgname = os.path.basename(filepaths[name])    
        return '<A HREF="%s"><IMG width=400 src="%s"></a><br>[%s]\n' % (imgname,imgname,name)
    
    f = open(os.path.join(REPORTDIR,REPORTNAME,'index.html'),'w')
    rs = ReportSpec(f)
    rs.writeheader()
    rs.writeindicatortable([['population','jobs'],['population_density',None],['land_value',None]],mapindicatornametocell,title='Various base year data indicators',headers=['Gridcell data','Zone data'])
    rs.writeindicatortable([['zone_jobs']],mapindicatornametocell,title='Silly demo chart')
    rs.writesimpletable(filepaths['table'],title='Table of gridcell data for 1980',numrows=20)
    rs.writefooter()
    
    print "Finished generating indicator report"
    
if __name__ == '__main__':
    main()
    