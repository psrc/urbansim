import mtc_config
import pxssh
import winssh
import sys
from optparse import OptionParser

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-n", "--non-interactive", dest="yesmode", action="store_true",
                      help="Answer yes to everything (i.e., non-interactive mode)")
    parser.add_option("-s", "--scenario", dest="scenario", action="store",
                      help="Specify the scenario (e.g., studio)")
    parser.add_option("-y", "--year", dest="year", action="store",
                      help="Specify the scenario year (e.g., 2020)")
    parser.add_option("-p", "--skip-popsyn", dest="skippopsyn", action="store_true",
                      help="Skips population synthesis step")
    (options, args) = parser.parse_args()

    config = mtc_config.MTCConfig()

    if options.scenario == None:
        print "ERROR: Please specify a scenario with -s"
        sys.exit(1)

    if options.year == None:
        print "ERROR: Please specify a scenario year with -y"
        sys.exit(1)

    # TODO: This should really be calculated somehow from travel_model_home.
    windows_travel_model_home = "E:\\\\mtc_travel_model"

    # Set up the server.
    print "Setting up proper directory structure..."
    server_admin = winssh.winssh(config.server_admin)
    modeldir = options.year + "_" + options.scenario
    abs_modeldir = config.travel_model_home + modeldir
    if server_admin.cmd("test -e " + abs_modeldir)[0] != 0:
        print "ERROR: Model directory " + abs_modeldir + " does not appear to exist"
        sys.exit(1)
    server_admin.cmd("subst /D M:")
    server_admin.cmd_or_fail("subst M: " + windows_travel_model_home)
    server_admin.cmd('rm /cygdrive/m/commpath')
    server_admin.cmd_or_fail('cmd /c "mklink /D M:\\\\commpath M:\\\\' + modeldir + '"')

    server = winssh.winssh(config.server)

    # Clean house before proceeding
    print "Killing old processes..."
    server.cmd('Taskkill /IM Cluster.exe /F')
    server.cmd('Taskkill /IM Voyager.exe /F')
    server.cmd('Taskkill /IM runtpp.exe /F')
    server.cmd('taskkill /im java.exe /F')

    print "Removing stale model outputs..."
    delfiles = server.cmd("find " + abs_modeldir + " -maxdepth 1 -not -wholename " + abs_modeldir)[1].split("\r\n")
    for f in map(lambda s: abs_modeldir + '/' + s, ("RunModel.bat", "CTRAMP", "INPUT", "README.txt", "urbansim")):
        try:
            delfiles.remove(f)
        except ValueError:
            continue
    if not options.yesmode:
        print "\r\n".join(delfiles)
        print "Can I rm -rf all of the files above? [y/n] "
        y = ""
        while True:
            y = sys.stdin.read(1)
            if y == "\n":
                continue
            elif y != "y" and y != "n":
                print "Please enter y or n"
            else:
                break
        if y != 'y':
            sys.exit(0)

    for f in delfiles:
        print "Removing " + f
        server.cmd("rm -rf " + f)

    print "Setting up M drive on server..."
    server.cmd("subst /D M:")

    server.cmd_or_fail("subst M: " + windows_travel_model_home)

    # Prepare synthesized population or skip if option supplied
    if not options.skippopsyn:
        print "Synthesizing population..."
        synth_script = "TazAndPopSyn.bat"
        server.cmd_or_fail('cd ' + config.travel_model_home + 'land_use_and_synthesizer')
        server.cmd_or_fail('cmd /c "' + synth_script + ' ' + options.scenario + ' ' + options.year + ' > M:\\\\' + modeldir + '\\\\synthOutput.log"')
    else:
        print "Skipping population synthesis."
        server.cmd_or_fail('cmd /c "echo Skipped population synthesis > M:\\\\' + modeldir + '\\\\synthOutput.log"')

    print "Launching runMain..."
    # Note here that we just send the line to the server with no regard for the
    # return value.  The reason is that this script starts a bunch of java
    # processes and doesn't return until they terminate.  So we assume success
    # here.  If we wanted to get fancy, we could poll the log file.
    server.cmd_or_fail('cd /cygdrive/m/commpath/CTRAMP/runtime')
    server.s.sendline('cmd /c "JavaOnly_runMain.cmd > runMainOutput.log"')

    nodes = []
    nodenum = 1
    for n in config.nodes:
        print "Preparing node " + str(nodenum)
        w = winssh.winssh(n)

        # Mount the M: drive on each node.  Start cleanly by killing any java
        # processes and unmount the M drive
        w.cmd('taskkill /im java.exe /F')
        w.cmd("net use M: /delete")

        mount_cmd = "net use M: "
        mount_cmd += "'" + config.netdrive + "' /user:" + config.netuser
        mount_cmd += " '" +config.netpw + "' /persistent:no"
        w.cmd_or_fail(mount_cmd, supress_cmd=True)

        # For some reason, we're not allowed to navigate symlinks unless we
        # spit out this magic.
        w.cmd_or_fail("fsutil behavior set SymlinkEvaluation L2L:1 R2R:1 L2R:1 R2L:1")

        w.cmd_or_fail('cd /cygdrive/m/commpath/CTRAMP/runtime')

        # Like the server's java processes, the node java processes will block
        # this cmd shell too.
        w.s.sendline('cmd /c "JavaOnly_runNode' + str(nodenum) + '.cmd > runNode' + str(nodenum) + '.log"')
        nodenum = nodenum + 1
        nodes.append(w)

    # Start the model.  We need a new winssh here because the existing one is
    # blocking on the java processes.
    server_model = winssh.winssh(config.server)

    print "Setting up M drive on server..."
    server_model.cmd("subst /D M:")
    server_model.cmd_or_fail("subst M: " + windows_travel_model_home)
    server_model.cmd_or_fail('cd /cygdrive/m/commpath/CTRAMP/runtime')

    print "Starting Model"
    server_model.cmd_or_fail('cd /cygdrive/m/commpath/')
    server_model.cmd_or_fail("cmd /c 'RunModel.bat' | tee RunModelOutput.log", supress_output=False, pipe_position=0)
