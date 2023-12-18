# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

#WARNING: THIS SCRIPT IS OBSOLETE AND WILL LIKELY NOT WORK

import time, os
import MySQLdb
from matplotlib.pylab import *
from numpy import *
from opus_core.bhhh_mnl_estimation import *
from opus_core.resources import Resources
from opus_core.misc import unique
from urbansim.constrain_choices import constrain_choices

program_start = time.clock()
alts = 8

Con = MySQLdb.connect(host=os.environ['MYSQLHOSTNAME'],
    user=os.environ['MYSQLUSERNAME'], passwd=os.environ['MYSQLPASSWORD'],db="paris_estimation")
    
Cursor = Con.cursor()
sql = "select LPImput, Lmaison, LColl, EmpTot9, delta_emp from hlcm_estimation_data"
#sql = "select LPImput, priceAge, PriceIncome, TC, TCSex, VP, NPAMVP, VPVoit, EmpTot9, delta_emp,\
#Lmaison, LColl, LmaisonNPER, NPER1com, NPER2com, NPER3com, NPAM0com, NPAM1com, NPAM2com, young_Com, medium_Com,\
#old_Com, rich_Com, medInc_Com, poor_com, foreign_Com, foreign_NoCom from hlcm_estimation_data"
Cursor.execute(sql)
#data = Cursor.fetchall()
data = array(Cursor.fetchall())
#data = array(data)
len_vars = data.shape[1]
data = reshape(data,(-1,alts,len_vars))

#Get probabilities
sql = 'select pred1 from probabilities'
Cursor.execute(sql)
unscaled_probability = reshape(array(Cursor.fetchall()),(-1,alts))
#print 'unscaled_probability.shape',unscaled_probability.shape
#print 'one_array.shape',one_array.shape
#Scale probabilities to 1 to ensure there is not a rounding error
probability = unscaled_probability/resize(sum(unscaled_probability,axis=1),(117872,8))
check1 = sum(probability,axis=1)
print('All probability sums close to 1.0:', ma.allclose(check1,1.0,rtol=1e-10))

#Get index
sql = 'select commune_id from probabilities'
#sql = 'select com from hlcm_estimation_data'
Cursor.execute(sql)
probability_index = reshape(array(Cursor.fetchall()),(-1,alts))-1
idx = reshape(array(Cursor.fetchall()),(-1,)).astype(Int)
unique = unique(idx)
#print unique[0:200]
#print 'shape.unique:',unique.shape

#Get capacity
sql = 'select supply from supply order by commune'
Cursor.execute(sql)
capacity = reshape(array(Cursor.fetchall()),(-1,))/5

Con.close

resources = Resources({"capacity":capacity,"index":probability_index})
#resources = Resources({"capacity":capacity})
#print 'Probability.shape:',probability.shape

C = constrain_choices()
C.compute(probability,resources)

#B = bhhh_estimation()
#B.compute(data,resources)
print('Total Elapsed Time:',time.clock()-program_start)
