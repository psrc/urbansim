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

table = gp.getparameterastext(0)
field = gp.getparameterastext(1)
new_field_name = gp.getparameterastext(2)

gp.AddField(table, new_field_name, "long", "#", "#", "#", "#", "#", "#", "#")

#this will duplicate the contents
expression = "int([%s])" % (field)
gp.CalculateField(table, new_field_name, expression)
