# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import waterdemand

basepath = waterdemand.__path__[0]
path = os.path.join(basepath, "docs", "latex")

cwd = os.getcwd()
os.chdir(path)    

modules = ["userguide"]
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