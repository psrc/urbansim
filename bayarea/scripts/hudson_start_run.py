# Why does hudson need his own wrapper for start_run?  The reason is that to
# support concurrent runs, we must somehow dump the cache directory to the
# hudson environment.  This was the quickest way to do this.

import opus_core.tools.start_run as start_run
import os

if __name__ == "__main__":
    option_group = start_run.StartRunOptionGroup()
    option_group.parse()
    options, config, run_manager = start_run.prepare_run_manager(option_group)
    # Dump the cache_directory before we launch the run so that if the run
    # fails, we can still know the cache directory and can run the report.
    ws = os.getenv("WORKSPACE")
    if ws:
        cache_directory = run_manager.get_current_cache_directory()
        f = open(os.path.join(ws, "current_cache_dir.txt"), "w")
        f.write(cache_directory)
        f.close()

    run_manager.run_run(config,
                        scenario_name=options.scenario_name,
                        run_as_multiprocess=not options.run_as_single_process)
