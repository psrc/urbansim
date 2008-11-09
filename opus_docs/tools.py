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
import re

def check_returncode(returncode, output):
    if returncode != 0:
        return ["Nonzero return code: " + str(returncode)]
    else:
        return []

def check_latex_warnings(returncode, output):
    warnings = []
    format = re.compile(r"\n +")
    prog = re.compile(r"(?P<hbox>(?:Under|Over)full \\hbox.*?\n(?:\n|\[\d))|(?P<end>\))|\((?P<file>.*?)[\s)]|LaTeX Warning: (?P<warning>.*?)\n\n", re.DOTALL)
    result = prog.search(output)
    pos = 0
    file_stack = []
    while result is not None:
        pos += result.end()
        if result.groupdict()["file"] is not None:
            if result.group(0)[-1] != ")":
                file_stack.append(result.groupdict()["file"])
        elif result.groupdict()["warning"] is not None:
            warnings.append("(%s) %s" % (file_stack[-1], format.sub(" ", result.groupdict()["warning"]).replace("\n", "")))
        elif result.groupdict()["end"] is not None:
            file_stack.pop()
        result = prog.search(output[pos:])
    return warnings

def build(modules, cwd=os.getcwd(), make_index=True):
    for module in modules:
        pass_1_interaction = "nonstopmode"
        print "* Building docs for module", module
        if make_index:
            pass_1_interaction = "batchmode"
            # run latex, make the index, then run latex twice more to resolve cross-references correctly and include the index
            # The first run is fine for checking for fatal errors; e.g. unresolved cross-references are not fatal errors
            print "  * Running pdflatex, index creation pass"
            run(["pdflatex","-draftmode","-interaction","nonstopmode",module+".tex"], cwd, error_fns=[check_returncode])
            # The makeindex command will fail if the module doesn't have an index - so it's important NOT to check 
            # if the result of the system call succeeded.  (The advantage of calling it anyway is that we can just
            # process all of the files with a loop, rather than having separate processing for modules with and without indices.)
            print "  * Running bibtex"
            run(["bibtex",module], cwd)
            print "  * Running makeindex"
            run(["makeindex",module+".idx"], cwd)
        # this is ludicrous -- but we need to run pdflatex *twice* -- otherwise the index isn't included in
        # the table of contents
        print "  * Running pdflatex, pass 1"
        run(["pdflatex","-draftmode","-interaction",pass_1_interaction,module+".tex"], cwd, error_fns=[check_returncode])
        print "  * Running pdflatex, pass 2"
        run(["pdflatex","-interaction","nonstopmode",module+".tex"],
            cwd, warning_fns=[check_latex_warnings], error_fns=[check_returncode])
        # run latex2html to make an html version of the manual.  
        print "  * Running latex2html"
        run(["latex2html","-local_icons","-bottom_navigation","-address","info (at) urbansim.org",module],
            cwd, error_fns=[check_returncode])

def run(command, cwd, warning_fns=[], error_fns=[]):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdout, stderr) = proc.communicate()
    warning_msgs = []
    error_msgs = []
    for warning_fn in warning_fns:
        warning_msgs += warning_fn(proc.returncode, stdout)
    for error_fn in error_fns:
        error_msgs += error_fn(proc.returncode, stdout)
    if warning_msgs:
        print "**** Warnings for command: " + str(command)
        print "\n".join(warning_msgs)
    if error_msgs:
        print "**** Errors for command: " + str(command)
        print "\n".join(error_msgs)
    if warning_msgs or error_msgs:
        print "\n**** Command output:"
        print stdout
    if error_msgs:
        raise Exception()
    return stdout

# The old script called latex (rather than pdflatex), followed by dvips and ps2pdf
#  -  pdflatex works better that latex followed by  dvips and ps2pdf for producing pdf files if there are no figures
#     (gets links right in table of contents)
