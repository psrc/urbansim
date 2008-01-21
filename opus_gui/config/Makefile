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

all: 
	$(MAKE) -C datamanager
	$(MAKE) -C filetree
	$(MAKE) -C modelmanager
	$(MAKE) -C resultsmanager
	$(MAKE) -C scenariomanager
	$(MAKE) -C xmlmodelview
	$(MAKE) -C xmltree

clean:
	$(RM) *.pyc
	$(RM) *~
	$(MAKE) -C datamanager clean
	$(MAKE) -C filetree clean
	$(MAKE) -C modelmanager clean
	$(MAKE) -C resultsmanager clean
	$(MAKE) -C scenariomanager clean
	$(MAKE) -C xmlmodelview clean
	$(MAKE) -C xmltree clean


