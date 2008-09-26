# UrbanSim software. Copyright (C) 1998-2008 University of Washington
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

all: databasesettingsedit_ui.py

clean:
	$(RM) databasesettingsedit_ui.py
	$(RM) *.pyc
	$(RM) *~

databasesettingsedit_ui.py: databasesettingsedit.ui
	pyuic4 -o databasesettingsedit_ui.py databasesettingsedit.ui

