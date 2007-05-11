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

#specify variables
table = gp.getparameterastext(0)

#Adds specific AZ-SMART toolbox so the next command can be executed
#as a native method on the gp object
gp.addtoolbox("D:/svn_working/az_smart/toolboxes/AZ-SMART - Pima County.tbx")

#creates a new field called 'improvement_value' and copies the contents of
#the existing 'ASDFCV' field to it
gp.addmessage("Running duplicate field script....")
gp.DuplicateField(table, "ASDFCV", "improvement_value")

#create a table view that only contains records specified
#by the where_clause
gp.addmessage("Making table view....")
where_clause = '"improvement_value" =0'
gp.MakeTableView(table, "table_view", where_clause)

#calculate
gp.addmessage("Calculating field....")
expression = "[ACTUAL]"
gp.CalculateField("table_view", "improvement_value", expression)