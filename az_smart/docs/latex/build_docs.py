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

import os
import az_smart

basepath = az_smart.__path__[0]
path = os.path.join(basepath, "docs", "latex")

cwd = os.getcwd()
os.chdir(path)    

modules = ["az_smart_architecture"]
for module in modules:
    # hack - make a fake index file to prime the pump, so that latex doesn't give an error the first time it is run
    # (There's probaby a better way to do this, but this works.)
    index_file = file(module + ".ind", 'w')
    index_file.write(r"\begin{theindex} \end{theindex}")
    index_file.close()
   # run latex, make the index, then run latex again to resolve cross-references correctly and include the index
    if os.system("pdflatex -interaction=nonstopmode " + module + ".tex") > 0:
        raise Exception("pdflatex failed")
    # The makeindex command will fail if the module doesn't have an index - so it's important NOT to check 
    # if the result of the system call succeeded.  (The advantage of calling it anyway is that we can just
    # process all of the files with a loop, rather than having separate processing for modules with and without indices.)
    os.system("makeindex " + module + ".idx")
    if os.system("pdflatex -interaction=nonstopmode " + module + ".tex") > 0:
        raise Exception("Latex failed")
    
os.chdir(cwd)

# The old script called latex (rather than pdflatex), followed by dvips and ps2pdf
#  -  pdflatex works better that latex followed by  dvips and ps2pdf for producing pdf files if there are no figures
#     (gets links right in table of contents)