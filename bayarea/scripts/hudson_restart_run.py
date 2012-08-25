import os, sys
from opus_core.logger import logger
import opus_core.tools.restart_run as restart_run
from opus_core.services.run_server.run_manager import RunManager
import shutil, glob
import hudson_common

def main(option_group=None, args=None):

    if option_group is None:
        option_group = restart_run.RestartRunOptionGroup()
    parser = option_group.parser
    if args is None:
        options, args = option_group.parse()
    else: 
        options, _args = option_group.parse()
    run_manager = RunManager(option_group.get_services_database_configuration(options))
    run_as_multiprocess = not options.run_as_single_process

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    run_id = int(args[0])
    year = None
    if len(args) > 1:
        year = int(args[1])

    # Get configuration from DB and ensure the run directory is mounted.  Note
    # that we pass a dummy value for restart_year because we might not know it
    # yet.  But when we actually restart the run, we will pass the correct
    # year.
    run_resources = run_manager.create_run_resources_from_history(run_id=run_id,
                                                                  restart_year=2010)
    hudson_common.mount_cache_dir(run_resources)

    cache_dir = run_resources['cache_directory']
    if not year:
        # guess the year based on how the cache dir is populated
        years = map(lambda y : int(os.path.basename(y)),
                    glob.glob(os.path.join(cache_dir, "2*")))
        year = max(years)

    end_year = int(options.end_year) if options.end_year is not None else None
    run_manager.restart_run(run_id, 
                            year,
                            options.project_name,
                            end_year=end_year,
                            skip_urbansim=options.skip_urbansim,
                            create_baseyear_cache_if_not_exists=options.create_baseyear_cache_if_not_exists,
                            skip_cache_cleanup=options.skip_cache_cleanup,
                            run_as_multiprocess=run_as_multiprocess
                            )

if __name__ == "__main__":
    main()
