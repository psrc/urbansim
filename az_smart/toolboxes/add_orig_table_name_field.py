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

#imports
import arcgisscripting, sys, os

#create geoprocessor
gp = arcgisscripting.create()

table = gp.getparameterastext(0)

gp.addmessage("Adding orig_table_name field...")
gp.AddField(table, "orig_table_name", "text", "#", "#", "35", "#", "#", "#", "#")

base, filename = os.path.split(table)

expression = '"%s"' % (filename)

gp.addmessage("Filling in fields with: %s" % (filename))
gp.CalculateField(table, "orig_table_name", expression)

gp.addmessage("FINISHED")