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
path = os.path.join(basepath, "docs", "latex", 'tutorials')
print "path = '%s'" % path

cwd = os.getcwd()
os.chdir(path)    

modules = ["run-eugene-model", "lorenz-curve"]
for module in modules:
   # run latex twice to resolve cross-references correctly
    os.system("pdflatex -interaction=nonstopmode " + module + ".tex")
    os.system("pdflatex -interaction=nonstopmode " + module + ".tex")
    # run latex2html to make an html version of the manual.  
    latex2html_call = 'latex2html -local_icons -bottom_navigation -address "info (at) urbansim.org" %s' % module
    os.system( latex2html_call )

os.chdir(cwd)
