#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

import os
import sys
import subprocess

def build(modules, cwd=os.getcwd(), make_bibliography_and_index=True):
    for module in modules:
        print "* Building docs for module", module
        if make_bibliography_and_index:
            # Run latex, make the bibliography and index, then run latex twice more to resolve cross-references 
            # correctly and include the index.
            # The first run is fine for checking for fatal errors; e.g. unresolved cross-references are not fatal errors.
            # We use -interaction=batchmode for all but the last run, so that warnings don't show up in the log.  On the 
            # final run we use -interaction=nonstop so that warnings do show up (allowing CruiseControl to scan for them).
            print "  * Running pdflatex, bibliography and index creation pass"
            run(["pdflatex","-interaction","batchmode",module+".tex"], cwd)
            # The makeindex command will fail if the module doesn't have an index - so it's important NOT to call
            # this if we aren't making an index.
            print "  * Running bibtex"
            run(["bibtex",module], cwd)
            print "  * Running makeindex"
            run(["makeindex",module+".idx"], cwd)
        # We need to run pdflatex twice more if making the bibliography and index -- otherwise the index isn't 
        # included in the table of contents.  And if not making the bibliography and index we need to run it twice
        # anyway, to get the cross-references right.
        print "  * Running pdflatex, pass 1"
        run(["pdflatex","-interaction","batchmode",module+".tex"], cwd)
        print "  * Running pdflatex, pass 2"
        run(["pdflatex","-interaction","nonstopmode",module+".tex"], cwd)
        # run latex2html to make an html version of the manual.  
        print "  * Running latex2html"
        run(["latex2html","-local_icons","-bottom_navigation","-address","info (at) urbansim.org",module], cwd)

def run(command, cwd, stop_on_error=True):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdout, stderr) = proc.communicate()
    if proc.returncode != 0:
        if stop_on_error:
            exception_msg = "Fatal error for command: " + str(command) + "\nCommand output:\n" + stdout;
            raise Exception(exception_msg)
        else:
            sys.stderr.write(stdout)

# The old script called latex (rather than pdflatex), followed by dvips and ps2pdf
#  -  pdflatex works better that latex followed by  dvips and ps2pdf for producing pdf files if there are no figures
#     (gets links right in table of contents)
