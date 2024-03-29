import mtc_config
import pxssh
import winssh
import sys, os
from optparse import OptionParser

def confirm_delete(yesmode, sshterm, delfiles):
    try:
        delfiles.remove("")
    except ValueError:
        pass
    if delfiles == []:
        return
    if not yesmode:
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
        sshterm.cmd("rm -rf " + f)

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
    parser.add_option("-o", "--output-dir", dest="outdir", action="store",
                      help="Optional output directory for travel model output data " +
                      "(relative to travel_model_home)")
    (options, args) = parser.parse_args()

    config = mtc_config.MTCConfig()

    if options.scenario == None:
        print "ERROR: Please specify a scenario with -s"
        sys.exit(1)

    if options.year == None:
        print "ERROR: Please specify a scenario year with -y"
        sys.exit(1)

    # Set up the server.
    print "Setting up proper directory structure..."
    server_admin = winssh.winssh(config.server_admin, "OPUS_MTC_SERVER_ADMIN_PASSWD")
    modeldir = options.year + "_" + options.scenario
    abs_modeldir = config.travel_model_home + modeldir
    if server_admin.cmd("test -e " + abs_modeldir)[0] != 0:
        print "ERROR: Model directory " + abs_modeldir + " does not appear to exist"
        sys.exit(1)
    server_admin.cmd("subst /D M:")
    (rc, windows_travel_model_home) = server_admin.cmd("cygpath -w " + config.travel_model_home)
    windows_travel_model_home = "'" + windows_travel_model_home.replace('\r\n','')[:-1] + "'"
    server_admin.cmd_or_fail("subst M: " + windows_travel_model_home)
    server_admin.cmd('rm /cygdrive/m/commpath')
    server_admin.cmd_or_fail('cmd /c "mklink /D M:\\\\commpath M:\\\\' + modeldir + '"')
    server = winssh.winssh(config.server, "OPUS_MTC_SERVER_PASSWD")

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
    confirm_delete(options.yesmode, server, delfiles)

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
    nodenum = 0
    for n in config.nodes:
        print "Preparing node " + str(nodenum + 1)
        w = winssh.winssh(n, "OPUS_MTC_NODE_" + str(nodenum) + "_PASSWD")

        # Mount the M: drive on each node.  Start cleanly by killing any java
        # processes and unmount the M drive
        w.cmd('taskkill /im java.exe /F')
        w.cmd("net use M: /delete")

        mount_cmd = "net use M: "
        mount_cmd += "'" + config.netdrive + "' /user:" + config.netuser
        if config.netpw:
            pw = config.netpw
        else:
            pw = os.getenv("OPUS_MTC_NET_PASSWD")
            if not pw:
                raise ValueError("No password found for network mount")

        mount_cmd += " '" + pw + "' /persistent:no"
        w.cmd_or_fail(mount_cmd, supress_cmd=True)

        # For some reason, we're not allowed to navigate symlinks unless we
        # spit out this magic.
        w.cmd_or_fail("fsutil behavior set SymlinkEvaluation L2L:1 R2R:1 L2R:1 R2L:1")

        w.cmd_or_fail('cd /cygdrive/m/commpath/CTRAMP/runtime')

        # Like the server's java processes, the node java processes will block
        # this cmd shell too.
        w.s.sendline('cmd /c "JavaOnly_runNode' + str(nodenum + 1) + '.cmd > runNode' + str(nodenum + 1) + '.log"')
        nodenum = nodenum + 1
        nodes.append(w)

    # Start the model.  We need a new winssh here because the existing one is
    # blocking on the java processes.
    server_model = winssh.winssh(config.server, "OPUS_MTC_SERVER_PASSWD")

    print "Setting up M drive on server..."
    server_model.cmd("subst /D M:")
    server_model.cmd_or_fail("subst M: " + windows_travel_model_home)
    server_model.cmd_or_fail('cd /cygdrive/m/commpath/CTRAMP/runtime')

    print "Starting Model"
    server_model.cmd_or_fail('cd /cygdrive/m/commpath/')
    server_model.cmd_or_fail("cmd /c 'RunModel.bat' | tee RunModelOutput.log", supress_output=False, pipe_position=0)

    if options.outdir:
        outdir = config.travel_model_home + options.outdir
        server_model.cmd_or_fail("mkdir -p " + outdir)
        delfiles = server_model.cmd("find " + outdir + " -maxdepth 1 -not -wholename " + outdir)[1].split("\r\n")
        confirm_delete(options.yesmode, server_model, delfiles)
        for d in ["database", "hwy", "logs", "main", "nonres", "skims", "trn", "popsyn", "urbansim", "landuse"]:
            d = abs_modeldir + "/" + d
            print "Preserving output " + d + " to " + outdir
            server_model.cmd_or_fail("cp -r " + d + " " + outdir)

    # Leave the machine idle and be sure to logout.  This should probably be a
    # finally block
    server_model.cmd('Taskkill /IM Cluster.exe /F')
    server_model.cmd('Taskkill /IM Voyager.exe /F')
    server_model.cmd('Taskkill /IM runtpp.exe /F')
    server_model.cmd('taskkill /im java.exe /F')
    server_model.logout()
    server.logout()
    server_admin.logout()
