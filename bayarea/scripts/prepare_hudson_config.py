# hudson, which we use to scale and automate model runs, can pass parameters to
# a build.  The parameters are passed in the environment, and many of them must
# be set in the project xml file.  So we have this utility to create a wrapper
# xml file based on the environment variables.  The wrapper goes around a
# specified parent xml file specified with the -x option.  We also must prepare
# a suitable database config, and the passwords for this come from the
# environment too.  What follows is a descrption of the environment variables:

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
#
# HUDSON_PRICE_EQUILIBRATION: Whether or not to enable price equilibration in
# the location choice models
#
# HUDSON_TRAVEL_MODEL_HOME: override the travel model base directory with this
# variable if it is set.  This enables the caller to mount the travel model
# directory however s/he wishes.
#
# HUDSON_TRAVEL_MODEL_SSHFS: urbansim can use sshfs to mount the travel model
# directory.  Set this variable to the ssh connect_string (e.g.,
# cube@detroit.urbansim.org:/cygdrive/e/mtc_travel_model) to use this feature
#
# OPUS_DBPASS: This is the database password used by the developer model
# HUDSON_DBPASS: This is the databse password used by hudson for the urbansim
# services db.
#
# NODE_NAME: hudson automatically sets this variable to the name of the slave
# node that is running the job.  We preserve this in the configuration so that
# when we restart jobs we can ensure that we have access to the correct run
# directory.

import sys, os
from optparse import OptionParser
from lxml import etree
from copy import deepcopy
from StringIO import StringIO

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                           help="file name of xml configuration (must also provide a scenario name using -s)")
    parser.add_option("-o", "--output", dest="xml_output", default=None, 
                           help="file name for output xml config file")
    parser.add_option("-d", "--dbfile", dest="db_output", default=None,
                           help="file name for database config file")
    (options, args) = parser.parse_args()

    if options.xml_configuration == None:
        print "ERROR: Please specify a suitable xml_configuration"
        sys.exit(1)

    parent_scenario = os.getenv("HUDSON_SCENARIO")
    if parent_scenario == None:
        print "ERROR: HUDSON_SCENARIO environment variable must be set"
        sys.exit(1)

    node_name = os.getenv("NODE_NAME")
    if not node_name:
        print "ERROR: NODE_NAME environment variable must be set"
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

    # if we enable price equilibration, we do so under the model manager.
    price_equlibration = os.getenv("HUDSON_PRICE_EQUILIBRATION")
    if price_equlibration == "true":
        model_manager = etree.Element("model_manager")
        project.append(model_manager)
        models = etree.Element("models", config_name="model_system",
                               hidden="False", name="Models", setexpanded="True",
                               type="dictionary")
        model_manager.append(models)

        # prepare common structure/init/argument node
        structure = etree.Element("structure", type="dictionary")
        init = etree.Element("init", type="dictionary")
        arg = etree.Element("argument", name="choices", parser_action="quote_string",
                            type="string")
        arg.text = "opus_core.upc.equilibration_choices"
        init.append(arg)
        structure.append(init)

        blcm = etree.Element("model", name="business_location_choice_model",
                             type="model")
        blcm.append(structure)
        models.append(blcm)
        hlcm_owner = etree.Element("model",
                                   name="submarket_household_location_choice_model_owner",
                                   type="model")
        hlcm_owner.append(deepcopy(structure))
        models.append(hlcm_owner)
        hlcm_renter = etree.Element("model",
                                    name="submarket_household_location_choice_model_renter",
                                    type="model")
        hlcm_renter.append(deepcopy(structure))
        models.append(hlcm_renter)

    # Now we create a child scenario of HUDSON_SCENARIO that we can use to
    # override some options.
    scenario_manager = etree.Element("scenario_manager")
    project.append(scenario_manager)
    scenario = etree.Element("scenario", executable="True",
                             name=parent_scenario + "_hudson",
                             type="scenario")
    hudson_details = etree.Element("hudson_details", type="dictionary")
    node = etree.Element("node", type="string")
    node.text = node_name
    hudson_details.append(node)
    scenario.append(hudson_details)

    hudson_details.append
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

    # set up a project-specific travel model base directory if necessary.
    tm_home = os.getenv("HUDSON_TRAVEL_MODEL_HOME")
    if tm_home:
        tmh = etree.Element("travel_model_home", type="dictionary")
        tmbd = etree.Element("directory", type="string")
        tmbd.text = tm_home
        tmh.append(tmbd)
        tm_sshfs = os.getenv("HUDSON_TRAVEL_MODEL_SSHFS")
        if tm_sshfs:
            tmproto = etree.Element("proto", type="string")
            tmproto.text = "sshfs"
            tmconnect = etree.Element("connect_string", type="string")
            tmconnect.text = tm_sshfs
            tmh.append(tmproto)
            tmh.append(tmconnect)
        tmc.append(tmh)
    models = etree.Element("models", type="selectable_list")
    tmc.append(models)
    invoke_tm = etree.Element("selectable",
                              name="bayarea.travel_model.invoke_run_travel_model",
                              type="selectable")
    import_tm = etree.Element("selectable",
                              name="bayarea.travel_model.import_travel_model_data",
                              type="selectable")
    travel_model = os.getenv("HUDSON_TRAVEL_MODEL")
    if travel_model:
        if (travel_model == "true") or (travel_model == "FULL"):
            invoke_tm.text = "True"
            import_tm.text = "True"
        elif travel_model == "SKIMS":
            invoke_tm.text = "False"
            import_tm.text = "True"
        else:
            invoke_tm.text = "False"
            import_tm.text = "False"
            
        models.append(invoke_tm)
        models.append(import_tm)
        scenario.append(tmc)

    print etree.tostring(project, pretty_print=True)

    if options.db_output:
        # Start by reading in the template:
        db_template = os.path.split(__file__)[0]
        db_template = os.path.join(db_template, "hudson_db_config.xml")
        f = open(db_template)
        xml = f.read()
        f.close()
        tree = etree.parse(StringIO(xml))
        pw = os.getenv("OPUS_DBPASS")
        if pw:
            tree.xpath("/database_server_configurations/urbanvision/password")[0].text = pw
        else:
            sys.stderr.write("WARNING: OPUS_DBPASS was not set\n")
        pw = os.getenv("HUDSON_DBPASS")
        if pw:
            tree.xpath("/database_server_configurations/services_database_server/password")[0].text = pw
        else:
            sys.stderr.write("WARNING: HUDSON_DBPASS was not set\n")

        f = open(options.db_output, "w")
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
