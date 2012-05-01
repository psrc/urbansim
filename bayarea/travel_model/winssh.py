import sys
import pxssh

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
        print "Attempting to login to " + user + "@" + host
        self.s.login(host, user, pw, login_timeout=20)
        self.s.setecho(False)

    def cmd(self, c):
        self.s.sendline(c)
        self.s.prompt(timeout=None)
        output = "\r\n".join(self.s.before.split("\r\n")[1:])
        self.s.sendline("echo $?")
        self.s.prompt()
        rc = self.s.before.split("\r\n")[1]
        return (int(rc), output)

    def cmd_or_fail(self, c, supress_cmd=False, supress_output=True):
        (rc, out) = self.cmd(c)
        if rc != 0:
            if supress_cmd:
                print "Command Failed",
            else:
                print "Failed to " + c,
            print "(" + str(rc) + "):"
            print out
            sys.exit(1)
        if not supress_output:
            print out

if __name__ == '__main__':
    node1 = winssh(CONNECT_STRING)
    assert(node1.cmd("echo 12345")[1] == "12345\r\n")
    assert(node1.cmd("false")[0] == 1)
