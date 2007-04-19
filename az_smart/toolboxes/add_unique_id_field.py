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