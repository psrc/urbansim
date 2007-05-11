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
field_to_duplicate = gp.getparameterastext(1)
new_field_name = gp.getparameterastext(2)

fields = gp.listfields(table)
field = fields.next()

#this will currently look for and add a text field or short field
while field:
    if field.name == field_to_duplicate:
        field_type = str(field.type)
        if field_type == "String":
            field_type = "text"
            field_length = field.length
            gp.AddField(table, new_field_name, field_type, "#", "#", field_length, "#", "#", "#", "#")
        elif field_type == "SmallInteger":
            field_type = "short"
            field_precision = field.precision
            gp.AddField(table, new_field_name, field_type, field_precision, "#", "#", "#", "#", "#", "#")
        elif field_type == "Integer":
            field_type = "long"
            field_precision = field.precision
            gp.AddField(table, new_field_name, field_type, field_precision, "#", "#", "#", "#", "#", "#")
        elif field_type == "Double":
            field_type = "double"
            field_scale = field.scale
            gp.AddField(table, new_field_name, field_type, "#", field_scale, "#", "#", "#", "#", "#")
        elif field_type == "OID":
            field_type = "long"
            field_precision = 15
            gp.AddField(table, new_field_name, field_type, field_precision, "#", "#", "#", "#", "#", "#")
        elif field_type == "Geometry":
            gp.AddError("The type of field specified has the type: GEOMETRY. \nThis script cannot duplicate this field.")
        elif field_type == "BLOB":
            gp.AddError("The type of field specified has the type: BLOB. \nThis script cannot duplicate this field.")
        else:
            gp.addmessage("The script found a field_type of: %s \nThis script has not been told how to deal with it." % (field_type))
    field = fields.next()

#this will duplicate the contents
expression = "[%s]" % (field_to_duplicate)
gp.CalculateField(table, new_field_name, expression)
