#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

import win32com.client as w32c
from opus_core.logger import logger

def run_transcad_macro(macroname, dbname, args=None):
    tc = w32c.Dispatch("TransCAD.AutomationServer")
    error_msg = tc.Macro(macroname, dbname, args)
    if error_msg is not None:
        logger.log_error( error_msg[-1][-1] )

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-m", "--macroname", dest="macroname", action="store", type="string",
                         help="Name of macro")
    parser.add_option("-u", "--dbname", dest="dbname", action="store", type="string",
                      help="ui database file name")
    parser.add_option("-a", "--args", dest="args", action="store", type="int",
                      help="argument values")

    (options, args) = parser.parse_args()
    run_transcad_macro(options.macroname, options.dbname, options.args)
 