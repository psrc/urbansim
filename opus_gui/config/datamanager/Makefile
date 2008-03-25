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

# Modify to RM = del for win
RM = rm -f
#RM = del

all: newscriptbatch_ui.py newscriptlibrary_ui.py configurescript_ui.py newdbconnection_ui.py

clean:
	$(RM) newscriptbatch_ui.py newscriptlibrary_ui.py configurescript_ui.py newdbconnection_ui.py
	$(RM) *.pyc
	$(RM) *~

newscriptbatch_ui.py: newscriptbatch.ui
	pyuic4 -o newscriptbatch_ui.py newscriptbatch.ui

newscriptlibrary_ui.py: newscriptlibrary.ui
	pyuic4 -o newscriptlibrary_ui.py newscriptlibrary.ui

configurescript_ui.py: configurescript.ui
	pyuic4 -o configurescript_ui.py configurescript.ui

newdbconnection_ui.py: newdbconnection.ui
	pyuic4 -o newdbconnection_ui.py newdbconnection.ui

