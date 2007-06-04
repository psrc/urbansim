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
import opus.ISSTA2006

basepath = opus.ISSTA2006.__path__[0]
path = os.path.join(basepath)

cwd = os.getcwd()
os.chdir(path)    

documents = ["main"]
for doc_name in documents:
    # run latex, then bibtex, then latex again
    if os.system("pdflatex -interaction=nonstopmode " + doc_name) > 0:
        raise Exception("pdflatex failed")
    if os.system("bibtex " + doc_name) > 0:
        raise Exception("bibtex failed")
    if os.system("bibtex " + doc_name) > 0:
        raise Exception("bibtex failed")
    if os.system("pdflatex -interaction=nonstopmode " + doc_name) > 0:
        raise Exception("Latex failed")
    if os.system("pdflatex -interaction=nonstopmode " + doc_name) > 0:
        raise Exception("Latex failed")
    
os.chdir(cwd)
