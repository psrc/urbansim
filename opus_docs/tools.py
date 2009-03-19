# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
import sys
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
        rerun = False
        print "  * Running pdflatex, initial pass"
        result = run(latex_command, cwd)
        report_on_run(result, error_fns=[check_returncode])
        rerun = bool(check_latex_rerun(result))
        if (make_bibliography == True) or \
                (make_bibliography == AUTO and check_latex_wants_bbl(result)):
            print "  * Running bibtex"
            result = run(["bibtex",module_base_path], cwd)
            report_on_run(result, error_fns=[check_returncode])
            rerun = True
        if (make_index == True) or \
                (make_index == AUTO and os.access(module_base_path+".idx", os.F_OK)):
            print "  * Running makeindex"
            result = run(["makeindex",module_base_path+".idx"], cwd, log=module_base_path+".ilg")
            report_on_run(result, error_fns=[check_returncode,check_makeindex_errors])
            rerun = True
        pass_number = 1
        while rerun:
            print "  * Running pdflatex, integration pass", pass_number
            result = run(latex_command, cwd)
            rerun = bool(check_latex_rerun(result))
            pass_number += 1
        report_on_run(result, stop_on_warning=True, warning_fns=[check_latex_warnings], error_fns=[check_returncode])
        move_file(module+".pdf", out_dir, cwd)
        print "  * Running latex2html"
        result = run(["latex2html","-local_icons","-bottom_navigation","-address","info (at) urbansim.org",
                      "-external_file",module_base_path,module], cwd)
        report_on_run(result, error_fns=[check_returncode])

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
    if run_result.returncode != 0:
        return ["Nonzero return code: " + str(run_result.returncode)]
    else:
        return []

def check_latex_warnings(run_result):
    warnings = []
    format = re.compile(r"\n +")
    prog = re.compile(r"(?P<hbox>(?:Under|Over)full \\hbox.*?\n(?:\n|\[\d))|" +
                        r"(?P<end>\))|" +
                        r"\((?P<file>.*?)[\s)]|" +
                        r"LaTeX Warning: (?P<warning>.*?)\n\n",
                      re.DOTALL)
    result = prog.search(run_result.stdout)
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
        result = prog.search(run_result.stdout[pos:])
    return warnings
    
def check_latex_rerun(run_result):
    messages = []
    result = run_result.stdout.find("LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n\n")
    if result != -1:
        messages = ["Label(s) may have changed."]
    return messages

def check_latex_wants_bbl(run_result):
    messages = []
    prog = re.compile(r"\nNo file (.*?\.bbl)\.\n")
    result = prog.search(run_result.stdout)
    if result is not None:
        messages = ["No file %s" % result.group(1)]
    return messages

def check_makeindex_errors(run_result):
    messages = []
    prog = re.compile(r"(?:" +
                        r"(?P<idxerr>!! Input index error \(file = (?P<file>.+?), line = (?P<line>\d+?)\):)|" +
                        r"(?P<inderr>## Warning \(input = .*?)|" +
                        r"(?P<styerr>\*\* Input style error \(file = .*?)" +
                      r")\n   -- (?P<msg>.+?)\n",
                      re.DOTALL)
    result = prog.search(run_result.log)
    additional = False
    pos = 0
    file_cache = {}
    while result is not None:
        pos += result.end()
        if result.groupdict()["idxerr"] is not None:
            file_name = result.groupdict()["file"]
            if file_name not in file_cache:
                try:
                    file_cache[file_name] = open(result.groupdict()["file"], "r").readlines()
                except:
                    file_cache[file_name] = ""
            if file_cache[file_name]:
                line = file_cache[file_name][int(result.groupdict()["line"])-1].strip()
                messages.append("Index error for \"%s\":  %s" % (line,result.groupdict()["msg"]))
            else:
                additional = True
        elif result.groupdict()["inderr"] is not None:
            additional = True
        elif result.groupdict()["styerr"] is not None:
            additional = True
        result = prog.search(run_result.log[pos:])
    if additional:
        messages.append("Additional errors found; please refer to the log output for details.")
    return messages

class run_result:
    def __init__(self, command, cwd, returncode, stdout, stderr, log):
        self.command = command
        self.cwd = cwd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.log = log

def run(command, cwd, log=None):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    log_text = None
    if log is not None:
        if not os.path.isabs(log):
            log = os.path.join(cwd,log)
        try:
            log_text = open(log, "r").read()
        except:
            pass
    return run_result(command, cwd, proc.returncode, stdout, stderr, log_text)

def report_on_run(run_result, warning_fns=[], error_fns=[], stop_on_warning=False, outfile=sys.stderr):
    warning_msgs = []
    error_msgs = []
    for warning_fn in warning_fns:
        warning_msgs += warning_fn(run_result)
    for error_fn in error_fns:
        error_msgs += error_fn(run_result)
    if warning_msgs or error_msgs:
        outfile.write("****** Command \"%s\" generated " % (os.path.basename(run_result.command[0])) +
                      ("%d warning"%len(warning_msgs) if warning_msgs else "") +
                      ("s" if len(warning_msgs)>1 else "") +
                      (" and " if (warning_msgs and error_msgs) else "") +
                      ("%d error"%len(error_msgs) if error_msgs else "") +
                      ("s" if len(error_msgs)>1 else "") +
                      " ******\n\n\n")
        outfile.write("**** Command and arguments ****\n")
        for arg in run_result.command:
            outfile.write(arg+"\n")
    if warning_msgs:
        outfile.write("\n**** Warnings ****\n")
        outfile.write(" - " + "\n - ".join(warning_msgs)+"\n")
    if error_msgs:
        outfile.write("\n**** Errors ****\n")
        outfile.write(" - " + "\n - ".join(error_msgs)+"\n")
    if warning_msgs or error_msgs:
        if run_result.stdout or run_result.stderr or run_result.log:
            outfile.write("\n**** Command output ****\n")
        if run_result.stdout:
            outfile.write("\n** Standard output **\n")
            outfile.write(run_result.stdout)
        if run_result.stderr:
            outfile.write("\n** Standard error **\n")
            outfile.write(run_result.stderr)
        if run_result.log:
            outfile.write("\n** Log output **\n")
            outfile.write(run_result.log)
    if error_msgs or (stop_on_warning and warning_msgs):
        outfile.write("\n")
        raise Exception()
