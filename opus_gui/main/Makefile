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

all: opusmain_ui.py opusmain_rc.py opusabout_ui.py

clean:
	$(RM) opusmain_ui.py opusmain_rc.py opusabout_ui.py
	$(RM) *.pyc
	$(RM) *~

opusmain_ui.py: opusmain.ui
	pyuic4 -o opusmain_ui.py opusmain.ui

opusabout_ui.py: opusabout.ui
	pyuic4 -o opusabout_ui.py opusabout.ui

opusmain_rc.py: opusmain.qrc
	pyrcc4 -o opusmain_rc.py opusmain.qrc

