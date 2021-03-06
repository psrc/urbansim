# Prepare an output report
from optparse import OptionParser
import MySQLdb
import sys, os
import urbansim.tools.make_indicators
import shutil, glob
import textwrap
import traceback
from opus_core.configurations.xml_configuration import XMLConfiguration
import bayarea.travel_model.mtc_common as mtc_common
from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
import hudson_common

class ReportOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self,
                                    usage="python %prog [options]",
                                    description="Run hudson's reporting capability")
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None,
                               help="File name of xml configuration")
        self.parser.add_option("-y", "--years", dest="years",
                               help="List of years to make indicators for (e.g., range(2010,2012)).")
        self.parser.add_option("-o", "--output-directory", dest="output",
                               help="Output directory for results")
        self.parser.add_option("-c", "--cache-directory", dest="cache_directory", default=None,
                               help="Directory of UrbanSim cache to make indicators from (Defaults to most recent successful run)")
        self.parser.add_option("-r", "--run-id", dest="run_id", default=None,
                               help="run ID on which to run the report.  If this option is specified, -c and -s are ignored.")

def main():
    option_group = ReportOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    if not options.xml_configuration or \
           not options.years or \
           not options.output:
        print "ERROR: -x, -y, and -o are required options"
        sys.exit(1)

    # determine the run_id from the command line args
    if options.run_id:
        run_id = options.run_id
    elif options.cache_directory:
        run_id = hudson_common.run_id_from_cache_dir(options.cache_directory)
        if not run_id:
            print "Failed to parse run ID from cache directory name"
            sys.exit(1)
    else:
        # get most recent succesful run from DB
        conn = MySQLdb.connect('paris.urbansim.org', 'hudson', os.getenv('HUDSON_DBPASS'), 'services');
        c = conn.cursor()
        c.execute("SELECT max(date_time), run_id FROM run_activity where status='done'")
        results = c.fetchone()
        run_id = str(results[1])

    # Note the dummy restart_year.  Because we're not actually going to
    # restart the run, this will be ignored.
    run_manager = RunManager(option_group.get_services_database_configuration(options))
    run_resources = run_manager.create_run_resources_from_history(run_id=run_id,
                                                                  restart_year=2010)
    cache_directory = run_resources['cache_directory']
    scenario = run_resources['scenario_name']

    # The cache directory may not exist if this script is being run on a hudson
    # slave that did not perform the original run.  Ensure that we mount it if
    # nec.
    hudson_common.mount_cache_dir(run_resources)

    # Hudson appends "_hudson" to the scenario names.  Peel this off
    # if it's present.
    scenario = scenario.replace("_hudson", "")

    # prepare the report staging directory
    output_dir = os.path.join(options.output, scenario, "run_" + run_id)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    f = open(os.path.join(output_dir, "README.txt"), 'w')

    years = eval(options.years)
    text = ""
    if os.getenv("HUDSON_DRAFT_RESULTS") == "true":
        text += "\n".join(textwrap.wrap(
"""NOTICE: This report contains unofficial draft model results that have not
been reviewed or approved by any agency.
""")) + "\n\n"
    text += "\n".join(textwrap.wrap(
"""This report has been auto-generated by urbansim for the following model run:
"""
)) + """
project: bay_area_parcel
scenario: %s
years: %d-%d
cached data: %s
""" % (scenario, years[0], years[-1],
       os.sep.join(cache_directory.split(os.sep)[-3:]))
    comment = os.getenv("HUDSON_COMMENT")
    if comment:
        text += "\n".join(textwrap.wrap("comment: " + comment)) + "\n"
    f.write(text.replace("\n", "\r\n"))
    f.close()

    # prepare the indicators
    shutil.rmtree(os.path.join(output_dir, "indicators"), True)
    for indicator_batch in ["county_indicators", "zone_data", "superdistrict_indicators", "regional_indicators_short","pda_indicators","abag_eir_area_permutation"]:
        urbansim.tools.make_indicators.run(options.xml_configuration,
                                           indicator_batch,
                                           None,
                                           cache_directory,
                                           options.years)

    my_location = os.path.split(__file__)[0]
    shp_path = os.path.join(os.getenv("OPUS_HOME"), "data", "bay_area_parcel", "shapefiles")
    
    ##county-level summary report
    pdf_county_script = os.path.join(my_location, "summarize_county_indicators_map.R")
    cmd = "Rscript %s %s %d %d %s %s %s %s" % (pdf_county_script,
                                   os.path.join(cache_directory, "indicators"),
                                   years[0], years[-1],shp_path,"bayarea_counties.shp", scenario, "county")
    print "Summarizing county indicators: " + cmd
    if os.system(cmd) != 0:
        print "WARNING: Failed to generate county indicators"
       
    ##superdistrict-level summary report --never mind the name of the script; is en route to being generalized   
    pdf_supdist_script = os.path.join(my_location, "summarize_superdistrict_indicators_map.R")
    cmd = "Rscript %s %s %d %d %s %s %s %s" % (pdf_supdist_script,
                                   os.path.join(cache_directory, "indicators"),
                                   years[0], years[-1],shp_path,"superdistricts.shp", scenario, "superdistrict")
    print "Summarizing superdistrict indicators: " + cmd
    if os.system(cmd) != 0:
        print "WARNING: Failed to generate superdistrict indicators"

    
    shutil.copytree(os.path.join(cache_directory, "indicators"),
                    os.path.join(output_dir, "indicators"),
                    ignore=shutil.ignore_patterns("*_stored_data*", "*.log"))

    # add the travel model EMFAC output to the web report
    config = XMLConfiguration(options.xml_configuration).get_run_configuration(scenario)
    travel_model = os.getenv("HUDSON_TRAVEL_MODEL")
    travel_model_for_R ="FALSE"
    if travel_model and travel_model.lower() == "full":
        print "Copying over travel model output"
        travel_model_for_R = "TRUE"
        tm_base_dir = mtc_common.tm_get_base_dir(config)
        tm_dir = os.path.join(tm_base_dir, "runs", cache_directory.split(os.sep)[-1])
        for f in glob.glob(os.path.join(tm_dir, '*', 'emfac', 'output', 'EMFAC2011-SG Summary*Group 1.*')):
            shutil.copy(f, output_dir)
		
    p = os.path.join(cache_directory, "mtc_data")
    if os.path.exists(p):
        shutil.copytree(p, os.path.join(output_dir, "mtc_data"))
    
    #Generate PDA comparison chart
    pda_script = os.path.join(my_location, "pda_compare.R")
    cmd = "Rscript %s %s %d %d %s %s" % (pda_script,
                                   os.path.join(cache_directory, "indicators"),
                                   years[0], years[-1], run_id, scenario)
    print "Creating pda comparison chart: " + cmd
    
    
    #Generate county x PDA facet chart
    pda_county_script = os.path.join(my_location, "growth_by_county_by_pda.R")
    cmd = "Rscript %s %s %d %d %s %s" % (pda_county_script,
                                   os.path.join(cache_directory, "indicators"),
                                   years[0], years[-1], run_id, scenario)
    print "Creating county by pda chart: " + cmd
    
    
    # topsheet--need the EMFAC outputs to be generated first, so this goes last
    #travel_model_for_R = "TRUE" if travel_model else "FALSE" 
    topsheet_script = os.path.join(my_location, "regional_indicators.R")
    cmd = "Rscript %s %s %d %d %s %s %s" % (topsheet_script,
                                   os.path.join(cache_directory, "indicators"),
                                   years[0], years[-1], run_id, travel_model_for_R, scenario)
    print "Creating topsheet: " + cmd
    if os.system(cmd) != 0:
        print "WARNING: Failed to generate indicators"
if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        tb = traceback.format_exc()
        print tb
        print "report generation failed"
        sys.exit(1)
