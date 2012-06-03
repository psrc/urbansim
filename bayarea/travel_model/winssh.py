import sys
import pxssh
from opus_core.logger import logger

# You can test winssh by running python winssh.py.  But you'll have to supply a
# suitable connect string
CONNECT_STRING = "cube@detroit.urbansim.org:********"

class winssh:

    def __init__(self, connectspec):
        """
        Initialize an ssh terminal connection
        connectspec: a connection specification such as user@host:pw
        """
        self.s = None
        pw = connectspec.split(':')[1]
        user = connectspec.split(':')[0].split('@')[0]
        host = connectspec.split(':')[0].split('@')[1]
        self.s = pxssh.pxssh()
        self.s.force_password = True
        logger.log_status("Attempting to login to " + user + "@" + host)
        self.s.login(host, user, pw, login_timeout=20)
        self.s.setecho(False)

    def cmd(self, c):
        self.s.sendline(c)
        self.s.prompt(timeout=None)
        logger.log_debug("BEFORE PROMPT")
        logger.log_debug(repr(self.s.before))
        output = "\r\n".join(self.s.before.split("\r\n")[1:])
        logger.log_debug("OUTPUT")
        logger.log_debug(output)
        self.s.sendline("echo $?")
        self.s.prompt()
        logger.log_debug("BEFORE $? PROMPT")
        logger.log_debug(repr(self.s.before))
        rc = self.s.before.split("\r\n")[1]
        return (int(rc), output)

    def cmd_or_fail(self, c, supress_cmd=False, supress_output=True):
        (rc, out) = self.cmd(c)
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
