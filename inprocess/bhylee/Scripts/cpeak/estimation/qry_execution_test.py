"""
This is just a test to see if python processes commands to mysql
in parallel or sequentially.
"""

import sys
import os
print os.path.join(sys.path[0], r'..\..\..\Estimation\Library')
sys.path.append(os.path.join(sys.path[0], r'..\..\..\Estimation\Library'))
import mdbi


myDB = mdbi.DbConnection(db = "PSRC_parcels_all_counties",
                        hostname = os.environ['MYSQLHOSTNAME'],
                        username = os.environ['MYSQLUSERNAME'],
                        password = os.environ['MYSQLPASSWORD'])

for i in ['C','R','G']:
    qry = """select count(*) from parcels a inner join 
        PSRC_2000_data_quality_indicators.land_use_generic_reclass b
        on a.county = b.county and a.land_use = b.county_land_use_code
        where b.generic_land_use_2 = '%s'""" % i
    print "qry = " + qry
    
    myDB.DoQuery(qry)
      
     