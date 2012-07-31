import sys
import pxssh
from opus_core.logger import logger
import os

# You can test winssh by running python winssh.py.  But you'll have to supply a
# suitable connect string
CONNECT_STRING = "cube@detroit.urbansim.org:********"

class winssh:

    def __init__(self, connectspec, passwd_env=None):
        """
        Initialize an ssh terminal connection
        connectspec: a connection specification such as user@host:pw
        """
        self.s = None
        connectparts = connectspec.split(':')
        if len(connectparts) == 2:
            pw = connectparts[1]
        elif passwd_env:
            pw = os.getenv(passwd_env)
            if not pw:
                raise ValueError("No password found in environment variable " + passwd_env)
        else:
            raise ValueError("No password found in connectspec or environment")
        user = connectparts[0].split('@')[0]
        host = connectparts[0].split('@')[1]
        self.s = pxssh.pxssh()
        self.s.force_password = True
        logger.log_status("Attempting to login to " + user + "@" + host)
        self.s.login(host, user, pw, login_timeout=20)
        self.s.setecho(False)

    def cmd(self, c, supress_output=True, pipe_position=None):
        """
        send command c

        supress_output keeps things silent

        pipe_position alters where we look for the exit code.  Usually, None is
        fine and we just echo $? to get the return code.  But in some cases,
        like if you say 'myprogram -a -b | tee foo.log', you really want the
        exit code of myprogram.  In this case you set pipe_position to 0.  If
        you wanted the exit code of tee, you'd set it to 1.
        """
        self.s.sendline(c)
        if supress_output:
            self.s.prompt(timeout=None)
        else:
            while not self.s.prompt(timeout=1):
                if self.s.before in (None, ""):
                    continue
                logger.log_status("\r\n".join(self.s.before.split("\r\n")[1:]))
                self.s.before = ""
                self.s.buffer = ""
        logger.log_debug("BEFORE PROMPT")
        logger.log_debug(repr(self.s.before))
        output = "\r\n".join(self.s.before.split("\r\n")[1:])
        logger.log_debug("OUTPUT")
        logger.log_debug(output)
        if pipe_position == None:
            self.s.sendline("echo $?")
        else:
            self.s.sendline('echo ${PIPESTATUS[' + str(pipe_position) + ']}')
        self.s.prompt()
        logger.log_debug("BEFORE $? PROMPT")
        logger.log_debug(repr(self.s.before))
        rc = self.s.before.split("\r\n")[1]
        return (int(rc), output)

    def cmd_or_fail(self, c, supress_cmd=False, supress_output=True, pipe_position=None):
        (rc, out) = self.cmd(c, supress_output, pipe_position)
        if rc != 0:
            if supress_cmd:
                logger.log_status("Command Failed:")
            else:
                logger.log_status("Failed to: " + c)
            logger.log_status("(" + str(rc) + "):")
            logger.log_status(out)
            sys.exit(1)
        if not supress_output:
            logger.log_status(out)

if __name__ == '__main__':
    node1 = winssh(CONNECT_STRING)
    assert(node1.cmd("echo 12345")[1] == "12345\r\n")
    assert(node1.cmd("false")[0] == 1)
