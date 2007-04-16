## Update integer values in a PGDB.

import sys, string, os, arcgisscripting
gp = arcgisscripting.create()

table = "D:\PimaCountyGIS\extracted_testing\squares.shp"
whereclause = "NEWFIELD = ''" #"NEWFIELD IS NOT NULL"

print "Updating feature class..."

cur = gp.updatecursor(table, whereclause)
row = cur.next()
while row:
#    x = row.getvalue("newfield")
#    y = row.getvalue("sq_area")
#    z = row.getvalue("UNIQUE_ID")
#    print x, y, z
#    row = cur.next()
    row.newfield = 'done'
    cur.updaterow(row)
    row = cur.next()




##cur = gp.UpdateCursor(table)
##row = cur.Next()
##while row:
##    # If the value is 10890, change it to 50.
##    x = row.GetValue("newfield")
##    if x == '':
##        row.newfield = 'blah'
##    
##    cur.UpdateRow(row)
##    row = cur.Next()