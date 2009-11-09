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

all: newtoolbatch_ui.py newtoollibrary_ui.py configuretool_ui.py executetool_ui.py executetoolset_ui.py

clean:
	$(RM) newtoolbatch_ui.py newtoollibrary_ui.py configuretool_ui.py executetool_ui.py executetoolset_ui.py
	$(RM) *.pyc
	$(RM) *~

newtoolbatch_ui.py: newtoolbatch.ui
	pyuic4 -o ui_newtoolbatch.py newtoolbatch.ui

newtoollibrary_ui.py: newtoollibrary.ui
	pyuic4 -o ui_newtoollibrary.py newtoollibrary.ui

configuretool_ui.py: configuretool.ui
	pyuic4 -o ui_configuretool.py configuretool.ui

executetool_ui.py: executetool.ui
	pyuic4 -o ui_executetool.py executetool.ui

executetoolset_ui.py: executetoolset.ui
	pyuic4 -o ui_executetoolset.py executetoolset.ui

