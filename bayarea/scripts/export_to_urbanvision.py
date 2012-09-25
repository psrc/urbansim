# dump urbansim results to postgres db for visualization in urbanvision.

from optparse import OptionParser
from hudson_common import *
from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
import sys
import psycopg2

class UrbanvisionOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self,
                                    usage="python %prog [options]",
                                    description="Dump urbansim results to urbanvision db")
        self.parser.add_option("-r", "--run-id", dest="run_id", default=None,
                               help="run ID on which to run the report.  If this option is specified, -c is ignored.")
        self.parser.add_option("-c", "--cache_directory", dest="cache_directory", default=None,
                               help="cache directory containing run data to dump.")


def main():
    option_group = UrbanvisionOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    if not options.run_id and not options.cache_directory:
        print "ERROR: either -r or -c is required"
        sys.exit(1)

    if options.run_id:
        run_id = options.run_id
    elif options.cache_directory:
        run_id = run_id_from_cache_dir(options.cache_directory)
        if not run_id:
            print "Failed to parse run ID from cache directory name"
            sys.exit(1)

    # Note the dummy restart_year.  Because we're not actually going to
    # restart the run, this will be ignored.
    run_manager = RunManager(option_group.get_services_database_configuration(options))
    run_resources = run_manager.create_run_resources_from_history(run_id=run_id,
                                                                  restart_year=2010)
    cache_directory = run_resources['cache_directory']
    mount_cache_dir(run_resources)
    scenario = run_resources['scenario_name']
    scenario = scenario.replace("_hudson", "")

    # Ensure that there's a suitable scenario abiding by the urbanvision
    # convention
    scenario_name = ("%s run %s" % (scenario, run_id)).replace("_", " ")
    passwd = os.environ['OPUS_DBPASS']
    conn_string = "host='paris.urbansim.org' dbname='bayarea' user='urbanvision' password='%s'" % passwd
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    s = "select id from scenario where name='{}'".format(scenario_name)
    cursor.execute(s)
    records = cursor.fetchall()
    if len(records) == 0:
        print "Creating new scenario '" + scenario_name + "'"
        s = "insert into scenario (name, parent) values ('{}', 1)".format(scenario_name)
        cursor.execute(s)
        conn.commit()
        s = "select id from scenario where name='{}'".format(scenario_name)
        cursor.execute(s)
        records = cursor.fetchall()
        assert(len(records) == 1)
        id = records[0][0]
    elif len(records) == 1:
        id = records[0][0]
    else:
        print "ERROR: Found more than one scenario named %s!" % scenario_name
        cursor.close()
        conn.close()
        sys.exit(1)

    cursor.close()
    conn.close()

    # Now that we have the scenario id, we can run the script that inserts the
    # records into the db
    psql = os.path.join(os.path.split(__file__)[0], "process_building_to_sql.py")
    cmd = "%s %s %s %d" % (sys.executable, psql, cache_directory, id)
    cmd += " | psql -h paris.urbansim.org -q -U urbanvision bayarea > /dev/null"
    print "Exporting buildings to db: " + cmd
    if os.system("export PGPASSWORD=$OPUS_DBPASS; " + cmd) != 0:
        print "ERROR: Failed to export buildings to urbanvision DB"
        sys.exit(1)

if __name__ == '__main__':
    main()
