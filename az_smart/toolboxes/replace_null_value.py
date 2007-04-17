#imports
import arcgisscripting

#create geoprocessor
gp = arcgisscripting.create()

#set up variables
table = gp.getparameterastext(0)
field = gp.getparameterastext(1)
new_value = gp.getparameterastext(2)
whereclause = "%s IS NULL" % (field)

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
