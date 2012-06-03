# This is a sample config file for running the MTC travel mode.  To create the
# real config, copy this file to mtc.config and edit it.  Some additional
# notes:
#
# The M drive (M:) is the spot from which the server and its subordinate nodes
# lauch the model processes.

class MTCConfig:
    # The main server that runs the travel model and delegates jobs to the
    # nodes.  Unfortunately, due to some windows permission restrictions on the
    # other side, we need to have the password for the server.  Public key
    # authentication will not do.
    server = "cube@detroit.urbansim.org:********"
    server_admin = "Administrator@detroit.urbansim.org:********"

    # This is the list of subordinate nodes to which the travel model delegates
    # jobs.
    nodes = [
        "Gue@169.229.154.17:********",
        "Gue@169.229.154.19:********",
        "Gue@169.229.154.21:********",
        "Gue@169.229.154.23:********",
    ]

    # The subordinate notes mount a share from the server as a network drive in
    # order to read and write the model files.  The following are the location
    # of the share, the username, and the password.  Oh.  And do me a favor.
    # Be sure that '\' is escaped in netdrive.
    #
    # SECURITY WARNING: This config file contains a password.  It should not be
    # world readable, and no real passwords should be checked in!
    netdrive = "\\\\detroit.urbansim.org\\mtc_travel_model"
    netuser = "cube"
    netpw = "********"

    # This is the base directory where all instances of the travel model for
    # the different scenarios are organized.
    travel_model_home = "/cygdrive/e/mtc_travel_model/"
