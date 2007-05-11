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
import arcgisscripting

#create geoprocessor
gp = arcgisscripting.create()

#set up variables
table = gp.getparameterastext(0)
unique_id_field_name = gp.getparameterastext(1)

gp.addmessage("Adding unique ID field")
gp.AddField(table, unique_id_field_name, "LONG", "#", "#", "#", "#", "#", "#", "#")

#create update cursor
gp.addmessage("Creating update cursor")
rows = gp.updatecursor(table)
row = rows.next()

gp.addmessage("Calculating unique ID")
x = 1
while row:
    exec 'row.' + unique_id_field_name + ' = x'
    rows.updaterow(row)
    x += 1
    row = rows.next()

#print finished message
gp.addmessage("\nFINISHED")