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

# Modify to RM = del for win
RM = rm -f
#RM = del

all: opusMain_ui.py opusMain_rc.py opusAbout_ui.py

clean:
	$(RM) opusMain_ui.py opusMain_rc.py opusAbout_ui.py
	$(RM) *.pyc
	$(RM) *~

opusMain_ui.py: opusMain.ui
	pyuic4 -o opusMain_ui.py opusMain.ui

opusAbout_ui.py: opusAbout.ui
	pyuic4 -o opusAbout_ui.py opusAbout.ui

opusMain_rc.py: opusMain.qrc
	pyrcc4 -o opusMain_rc.py opusMain.qrc

