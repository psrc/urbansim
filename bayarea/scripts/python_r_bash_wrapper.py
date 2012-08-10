"""
python wrapper for calling R script from Bash
"""

import subprocess, os, sys

##common
scenario=r'No_Project'
geography=r'superdistrict'
shp_file=r'superdistricts.shp'
script=r'summarize_geographic_indicators_map_general.R'
yrStart=2010
yrEnd=2020
duration = yrEnd - yrStart
localFlag=True

if localFlag:
    ##local paths
    tab_directory=r'/home/aksel/Documents/Data/Urbansim/run_107.2012_07_26_21_39/indicators'
    rScriptPath=r'/home/aksel/workspace/src/bayarea/scripts'
    shp_path=r'/home/aksel/Documents/Data/GIS'
else:
    ##remote paths
    tab_directory=r'/var/hudson/workspace/MTC_Model/data/bay_area_parcel/runs/run_107.2012_07_26_21_39/indicators' #raw_input()
    rScriptPath=r'/var/hudson/workspace/MTC_Model/src/bayarea/scripts'
    shp_path=r'/var/hudson/workspace/MTC_Model/data/bay_area_parcel/shapefiles'

"""
if duration<=8:
        print "Please select a run with more than %s years' duration" %duration
        sys.exit(1)
"""
#command-line arg string
arg ="%s %s %s %s %s %s %s" % ((os.sep.join(tab_directory.split(os.sep))),yrStart,yrEnd,shp_path,shp_file,scenario,geography)
command="Rscript %s" %(os.path.join(rScriptPath,script))
bashCmd="%s %s" %(command, arg)

print bashCmd
#call bash process as subprocess
#process = subprocess.Popen(bashCmd.split(), stdout=subprocess.PIPE)
#output = process.communicate()[0]
#print output
