# This is a sample config file for running the MTC travel mode.  To create the
# real config, copy this file to mtc.config and edit it.  Some additional
# notes:
#
# The M drive (M:) is the spot from which the server and its subordinate nodes
# lauch the model processes.
#
# Many of these configuration items are connect strings of the following form:
#
# user@machine[:password]
#
# Note that the password is optional.  If it is not supplied, it is expected to
# be in an environment variable, which is specified below alongside the related
# configuration item.

class MTCConfig:
    # The connect string for the main server that runs the travel model and
    # delegates jobs to the nodes.  Unfortunately, due to some windows
    # permission restrictions on the other side, we need to have the password
    # for the server.  Public key authentication will not do.
    #
    # Another unfortunate limitation is that some operations on the windows
    # server can only be performed by Administrator.  Even a user with
    # Administator rights won't work.  So you must also configure a connect
    # string for the Administrator.
    #
    # If a password is not specified in this connect string, the value of the
    # environment variable OPUS_MTC_SERVER_PASSWD is used.
    # OPUS_MTC_SERVER_ADMIN_PASSWD is used for the Administrator.
    server = "cube@detroit.urbansim.org"
    server_admin = "Administrator@detroit.urbansim.org"

    # This is the list connection strings for the subordinate nodes to which
    # the travel model delegates jobs.  If a password is not specified, the
    # value of the environment variable OPUS_MTC_NODE_X_PASSWD is used, where X
    # is the index of the connect string in this list (e.g.,
    # OPUS_MTC_NODE_0_PASSWD would be set to the password of the first node.)
    nodes = [
        "Gue@169.229.154.102",
        "Gue@169.229.154.103",
        "Gue@169.229.154.104",
        "Gue@169.229.154.105",
    ]

    # The subordinate notes mount a share from the server as a network drive in
    # order to read and write the model files.  The following are the location
    # of the share, the username, and the password.  Oh.  And do me a favor.
    # Be sure that '\' is escaped in netdrive.
    #
    # If netpw is None or "", the environment variable OPUS_MTC_NET_PASSWD will
    # be used.
    netdrive = "\\\\detroit.urbansim.org\\mtc_travel_model"
    netuser = "cube"
    netpw = None

    # This is the base directory where all instances of the travel model for
    # the different scenarios are organized.
    travel_model_home = "/cygdrive/e/mtc_travel_model/"
