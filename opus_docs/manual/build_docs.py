#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
import opus_docs

basepath = opus_docs.__path__[0]
path = os.path.join(basepath, "manual")

cwd = os.getcwd()
os.chdir(path)    

modules = ["opus-userguide"]
for module in modules:
   # run latex, make the index, then run latex twice more to resolve cross-references correctly and include the index
    os.system("pdflatex -interaction=nonstopmode " + module + ".tex")
    # The makeindex command will fail if the module doesn't have an index - so it's important NOT to check 
    # if the result of the system call succeeded.  (The advantage of calling it anyway is that we can just
    # process all of the files with a loop, rather than having separate processing for modules with and without indices.)
    os.system("makeindex " + module + ".idx")
    # this is ludicrous -- but we need to run pdflatex *twice* -- otherwise the index isn't included in
    # the table of contents
    os.system("pdflatex -interaction=nonstopmode " + module + ".tex")
    os.system("pdflatex -interaction=nonstopmode " + module + ".tex")
    # run latex2html to make an html version of the manual.  
    latex2html_call = 'latex2html -local_icons -bottom_navigation -address "info (at) urbansim.org" %s' % module
    os.system( latex2html_call )

os.chdir(cwd)

# The old script called latex (rather than pdflatex), followed by dvips and ps2pdf
#  -  pdflatex works better that latex followed by  dvips and ps2pdf for producing pdf files if there are no figures
#     (gets links right in table of contents)