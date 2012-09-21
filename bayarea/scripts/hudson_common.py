import os, shutil
from opus_core.logger import logger
import socket

class HudsonError(Exception):
    pass

def dump_cache_dir(cache_directory):
    ws = os.getenv("WORKSPACE")
    if ws:
        f = open(os.path.join(ws, "current_cache_dir.txt"), "w")
        f.write(cache_directory)
        f.close()

def mount_cache_dir(run_resources):
    # When we restart a run, it's critical that we either do it on the same
    # hudson slave, or that we somehow access the run directory on the hudson
    # slave where the job was originally run.  We achieve this by mounting the
    # directory via ssh if necessary.
    node_name = os.getenv("NODE_NAME")
    if not node_name:
        node_name = socket.gethostname()
        print "WARNING: NODE_NAME environment variable not set."
        print "Assuming hudson node name equals hostname!"
    try:
        original_node = run_resources['hudson_details']['node']
        if not original_node:
            raise KeyError
    except KeyError:
        raise HudsonError("Faied to determine original hudson node.")

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
            # Attempt to unmount cache_dir to start fresh.  Sometimes the mount
            # lingers and gives unexpected results.
            cmd = 'fusermount -u ' + cache_dir
            rc = os.system(cmd)
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

def run_id_from_cache_dir(c):
    try:
        if c[-1] == os.sep:
            options.cache_directory = options.cache_directory[0:-1]
        run_id = c.split(os.sep)[-1].split('.')[0].split('_')[1]
        return run_id
    except:
        print "Failed to parse run ID from cache directory name"
        return None
