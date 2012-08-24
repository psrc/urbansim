import os, sys
from opus_core.logger import logger
import opus_core.tools.restart_run as restart_run
from opus_core.services.run_server.run_manager import RunManager
import shutil, glob
import hudson_common

def main(option_group=None, args=None):

    # When we restart a run, it's critical that we either do it on the same
    # hudson slave, or that we somehow access the run directory on the hudson
    # slave where the job was originally run.
    node_name = os.getenv("NODE_NAME")
    if not node_name:
        logger.log_error("NODE_NAME environment variable not set.  Are you running within hudson?")
        sys.exit(1)

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

    # Get configuration from DB to check where the run was originally
    # performed.  Note that we pass a dummy value for restart_year because we
    # might not know it yet.  But when we actually restart the run, we will
    # pass the correct year.
    run_resources = run_manager.create_run_resources_from_history(run_id=run_id,
                                                                  restart_year=2010)
    try:
        original_node = run_resources['hudson_details']['node']
        if not original_node:
            raise KeyError
    except KeyError:
        logger.log_error("Faied to determine original hudson node.")
        raise

    if node_name != original_node:
        logger.log_warning("Mounting %s's run directory for access to run." %
                           original_node)
        # We assume that the workspace layout for all hudson slaves is the
        # same.  This allows us to assume that the paths on the slaves are
        # identical.
        cache_dir = run_resources['cache_directory']
        if os.path.exists(cache_dir) and os.path.ismount(cache_dir):
            # Here we assume that if the cache_directory is a mounted fs, then
            # it must be the one that we're expecting.
            pass
        else:
            if os.path.exists(cache_dir):
                # The local cache dir should be empty.  But sometimes it's not.
                # Like if sshfs fails during a model run or something.  So we
                # blow away the contents.
                shutil.rmtree(cache_dir)
            os.makedirs(cache_dir)
            cmd = 'sshfs hudson@' + original_node + ':' + cache_dir + ' ' + cache_dir
            logger.log_status("mount command: " + cmd)
            rc = os.system(cmd)
            if (rc != 0):
                raise IOError("Failed to '" + cmd + "'")

    if not year:
        # guess the year based on how the cache dir is populated
        years = map(lambda y : int(os.path.basename(y)),
                    glob.glob(os.path.join(cache_dir, "2*")))
        year = max(years)

    # ensure that the report generation can know the current directory
    hudson_common.dump_cache_dir(cache_directory)

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
