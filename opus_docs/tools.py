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
import subprocess
import re

AUTO=-1

def build(modules, cwd=os.getcwd(), make_bibliography=AUTO, make_index=AUTO):
    for module in modules:
        out_dir = os.path.join(cwd, module+".out")
        module_base_path = os.path.join(out_dir, module)
        delete_full(out_dir)
        os.mkdir(out_dir)
        latex_command = ["pdflatex","-interaction","nonstopmode","-output-directory",out_dir,module+".tex"]
        print "* Building docs for module", module
        reun = False
        print "  * Running pdflatex, initial pass"
        result = run(latex_command, cwd)
        check_run(result, error_fns=[check_returncode])
        rerun = bool(check_latex_rerun(result))
        if (make_bibliography == True) or \
                (make_bibliography == AUTO and check_latex_wants_bbl(result)):
            print "  * Running bibtex"
            result = run(["bibtex",module_base_path], cwd)
            check_run(result, error_fns=[check_returncode])
            rerun = True
        if (make_index == True) or \
                (make_index == AUTO and os.access(module_base_path+".idx", os.F_OK)):
            print "  * Running makeindex"
            result = run(["makeindex",module_base_path+".idx"], cwd)
            check_run(result, error_fns=[check_returncode])
            rerun = True
        pass_number = 1
        while rerun:
            print "  * Running pdflatex, integration pass", pass_number
            result = run(latex_command, cwd)
            rerun = bool(check_latex_rerun(result))
            pass_number += 1
        check_run(result, stop_on_warning=True, warning_fns=[check_latex_warnings], error_fns=[check_returncode])
        move_file(module+".pdf", out_dir, cwd)
        print "  * Running latex2html"
        result = run(["latex2html","-local_icons","-bottom_navigation","-address","info (at) urbansim.org",
                      "-external_file",module_base_path,module], cwd)
        check_run(result, error_fns=[check_returncode])

# Delete everything reachable from the directory named in 'top',
# assuming there are no symbolic links.
def delete_full(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
        os.rmdir(root)

def move_file(file, src, dst):
    dst_file = os.path.join(dst, file)
    if os.access(dst_file, os.F_OK):
        os.remove(dst_file)
    os.rename(os.path.join(src, file), dst_file)

def check_returncode(run_result):
    (command, returncode, stdout) = run_result
    if returncode != 0:
        return ["Nonzero return code: " + str(returncode)]
    else:
        return []

def check_latex_warnings(run_result):
    (command, returncode, stdout) = run_result
    warnings = []
    format = re.compile(r"\n +")
    prog = re.compile(r"(?P<hbox>(?:Under|Over)full \\hbox.*?\n(?:\n|\[\d))|" +
                        r"(?P<end>\))|" +
                        r"\((?P<file>.*?)[\s)]|" +
                        r"LaTeX Warning: (?P<warning>.*?)\n\n",
                      re.DOTALL)
    result = prog.search(stdout)
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
        result = prog.search(stdout[pos:])
    return warnings
    
def check_latex_rerun(run_result):
    (command, returncode, stdout) = run_result
    message = []
    result = stdout.find("LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n\n")
    if result != -1:
        message = ["Label(s) may have changed."]
    return message

def check_latex_wants_bbl(run_result):
    (command, returncode, stdout) = run_result
    message = []
    prog = re.compile(r"\nNo file (.*?\.bbl)\.\n")
    result = prog.search(stdout)
    if result is not None:
        message = ["No file %s" % result.group(1)]
    return message

def run(command, cwd):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdout, stderr) = proc.communicate()
    return (command, proc.returncode, stdout)

def check_run(run_result, stop_on_warning=False, warning_fns=[], error_fns=[]):
    (command, returncode, stdout) = run_result
    warning_msgs = []
    error_msgs = []
    for warning_fn in warning_fns:
        warning_msgs += warning_fn(run_result)
    for error_fn in error_fns:
        error_msgs += error_fn(run_result)
    if warning_msgs:
        print "**** Warnings for command: " + str(command)
        print "\n".join(warning_msgs)
    if error_msgs:
        print "**** Errors for command: " + str(command)
        print "\n".join(error_msgs)
    if warning_msgs or error_msgs:
        print "\n**** Command output:"
        print stdout
    if error_msgs or (stop_on_warning and warning_msgs):
        raise Exception()
