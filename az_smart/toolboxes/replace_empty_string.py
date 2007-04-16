import arcgisscripting

gp = arcgisscripting.create()

table = gp.getparameterastext(0)
field = gp.getparameterastext(1)
new_value = gp.getparameterastext(2)
whereclause = "%s = ''" % (field)

rows = gp.updatecursor(table, whereclause)
row = rows.next()

while row:
    row.field = new_value
    rows.updaterow(row)
    row = rows.next()

gp.addmessage("\nFINISHED")

## ALL OF THIS WORKS
##import arcgisscripting, sys, os, string
##
##gp = arcgisscripting.create()
##
##table = "D:\\PimaCountyGIS\\AZ-SMART_geodb\\pima_source_data.gdb\\paregion"
###field = "use_temp"
###new_value = "99999"
##whereclause = "use_temp = ''"
##
##rows = gp.UpdateCursor(table, whereclause)
##row = rows.Next()
##
##while row:
##    row.use_temp = "99999"
##    rows.updaterow(row)
##    row = rows.next()
##
##gp.addmessage("\nFINISHED")
