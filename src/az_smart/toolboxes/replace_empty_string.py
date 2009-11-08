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
field = gp.getparameterastext(1)
new_value = gp.getparameterastext(2)
whereclause = "%s = ''" % (field)

#create update cursor
rows = gp.updatecursor(table, whereclause)
row = rows.next()

#loop through rows replacing empty strings with
#new values for specified table, field, and new_value
while row:
    exec 'row.' + field + ' = new_value'
    rows.updaterow(row)
    row = rows.next()

#print finished message
gp.addmessage("\nFINISHED")
