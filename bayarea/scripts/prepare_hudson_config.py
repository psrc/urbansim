# hudson, which we use to scale and automate model runs, can pass parameters to
# a build.  The parameters are passed in the environment, and many of them must
# be set in the project xml file.  So we have this utility to create a wrapper
# xml file based on the environment variables.  The wrapper goes around a
# specified parent xml file specified with the -x option.  What follows is a
# descrption of the environment variables:

# HUDSON_SCENARIO: The scenario to which the environment variables will be
# applied.
# HUDSON_BASE_YEAR: The base year of the model
# HUDSON_FIRST_YEAR: The year to start running the model
# HUDSON_LAST_YEAR: The year to which the model should be run
# HUDSON_TRAVEL_MODEL: A boolean value that specifies whether the travel model
# should be run.
# HUDSON_LAND_USE_MODEL: A boolean value that specifies whether the land-use
# model should be run.  Typically, this is 1.  But for testing purposes, we
# might want to turn it off.

import sys, os
from optparse import OptionParser
from lxml import etree

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                           help="file name of xml configuration (must also provide a scenario name using -s)")
    parser.add_option("-o", "--output", dest="xml_output", default=None, 
                           help="file name for output xml config file")
    (options, args) = parser.parse_args()

    if options.xml_configuration == None:
        print "ERROR: Please specify a suitable xml_configuration"
        sys.exit(1)

    parent_scenario = os.getenv("HUDSON_SCENARIO")
    if parent_scenario == None:
        print "ERROR: HUDSON_SCENARIO environment variable must be set"
        sys.exit(1)

    project = etree.Element("opus_project")
    version = etree.Element("xml_version")
    version.text = "2.0"
    project.append(version)
    general = etree.Element("general")
    project.append(general)
    description = etree.Element("description", type="string")
    description.text = "auto-generated urbansim configuration used by hudson"
    general.append(description)
    parent = etree.Element("parent", type="file")
    parent.text = options.xml_configuration
    general.append(parent)

    # Now we create a child scenario of HUDSON_SCENARIO that we can use to
    # override some options.
    scenario_manager = etree.Element("scenario_manager")
    project.append(scenario_manager)
    scenario = etree.Element("scenario", executable="True",
                             name=parent_scenario + "_hudson",
                             type="scenario")
    scenario_manager.append(scenario)
    parent = etree.Element("parent", type="scenario_name")
    parent.text = parent_scenario
    scenario.append(parent)

    # Apply the overriden years to run:
    base_year = os.getenv("HUDSON_BASE_YEAR")
    if base_year:
        base = etree.Element("base_year", type="integer")
        base.text = base_year
        scenario.append(base)

    first_year = os.getenv("HUDSON_FIRST_YEAR")
    last_year = os.getenv("HUDSON_LAST_YEAR")
    ytr = etree.Element("years_to_run", config_name="years", type="tuple")
    if first_year:
        fy = etree.Element("firstyear", type="integer")
        fy.text = first_year
        ytr.append(fy)
    if last_year:
        ly = etree.Element("lastyear", type="integer")
        ly.text = last_year
        ytr.append(ly)
    if first_year or last_year:
        scenario.append(ytr)

    # Enable/disable land use model.  We disable by setting the list of models
    # to nothing.  We enable by inheriting the models to run from the parent
    # scenario.
    land_use = os.getenv("HUDSON_LAND_USE_MODEL")
    if land_use and land_use == "false":
        lu = etree.Element("models_to_run", config_name="models", type="selectable_list")
        scenario.append(lu)

    # apply the travel model specification
    tmc = etree.Element("travel_model_configuration", type="dictionary")
    models = etree.Element("models", type="selectable_list")
    tmc.append(models)
    selectable = etree.Element("selectable_list",
                               name="bayarea.travel_model.invoke_run_travel_model",
                               type="selectable")
    travel_model = os.getenv("HUDSON_TRAVEL_MODEL")
    if travel_model:
        if travel_model == "true":
            selectable.text = "True"
        else:
            selectable.text = "False"
        models.append(selectable)
        scenario.append(tmc)

    print etree.tostring(project, pretty_print=True)
