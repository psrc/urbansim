"""
python wrapper for calling R script from Bash
"""

import subprocess, os, sys

#placeholders for cmd-line args; in actuality these are parsed from xml config
#TODO: replace with live values 
yrStart=2010
yrEnd=2026
duration = yrEnd - yrStart
argFlag=True
rScriptPath=r'/home/aksel/Documents/Scripts/r'   
tab_directory=r'/home/aksel/Documents/Data/Urbansim/run_139.2012_05_15_21_23/indicators/2010_2035'

if duration<=10:
        print "Please select a run with more than %s years' duration" %duration
        sys.exit(1)

if argFlag: #distinction for testing purposes only 
    #command-line arg string
    arg ="%s %s %s" % ((os.sep.join(tab_directory.split(os.sep))),yrStart,yrEnd)
    command="Rscript %s" %(os.path.join(rScriptPath,'county_indicator_plots_index_ggplotfinal_arg_table.R'))
    bashCmd="%s %s" %(command, arg)
else:
    #command string
    command="Rscript %s" %(os.path.join(rScriptPath,'county_indicator_plots_index_ggplotfinal.R'))
    bashCmd=command


#call bash process as subprocess
process = subprocess.Popen(bashCmd.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
print output
