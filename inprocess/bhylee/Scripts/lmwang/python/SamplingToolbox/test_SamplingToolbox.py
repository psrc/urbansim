#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

import os
import sys,time
from glob import glob
import path_configuration

from household.household import HouseholdSet, HouseholdSubset
from grid.Gridcells import GridcellSet
from multiDB.MultiDB import DbConnection
from SamplingToolbox import SamplingToolbox

indb = "Eugene_baseyear"

db_host_name=os.environ['MYSQLHOSTNAME']
db_user_name=os.environ['MYSQLUSERNAME']
db_password =os.environ['MYSQLPASSWORD']

print "Connecting database ..."
Con = DbConnection(db=indb, hostname=db_host_name, username=db_user_name, 
                   password=db_password)

bdir = "./households_export"

households = HouseholdSet(database_connection=Con, base_directory=bdir)
gridcells = GridcellSet(database_connection=Con, base_directory=bdir)

sample = SamplingToolbox(households,gridcells,sampling_method=(0,0),N=50,debuglevel=5)

sample.sampling_agents()

start_time1 = time.time()
sample.sampling_alt()
end_time1 = time.time()

sampled_hhs = HouseholdSubset(households,sample.sampled_agent_idx)
print "sampled household index (", sample.sampled_agent_idx.size(), "/", households.n, "):"
print sample.sampled_agent_idx
print "sampled household_id:"
print sampled_hhs.get_attribute('household_id')
print "which respectively resides at grid_id:"
print sampled_hhs.get_attribute('grid_id')
print "alternative set:"
print gridcells.get_attribute_by_index("grid_id",sample.choiceset_idx)
print "the selected choice matrix:"
print sample.selected_choice

start_time2 = time.time()
#sample.sampling_agents()
#sample.sampling_alt2()
end_time2 = time.time()

#sampled_hhs = HouseholdSubset(households,sample.sampled_agent_idx)
print "sampled household index (", sample.sampled_agent_idx.size(), "/", households.n, "):"
print sample.sampled_agent_idx
print "sampled household_id:"
print sampled_hhs.get_attribute('household_id')
print "which respectively resides at grid_id:"
print sampled_hhs.get_attribute('grid_id')
print "alternative set:"
print gridcells.get_attribute_by_index("grid_id",sample.choiceset_idx)
print "the selected choice matrix:"
print sample.selected_choice

start_time3 = time.time()
#sample.sampling_agents()
#sample.sampling_alt3()
end_time3 = time.time()

#sampled_hhs = HouseholdSubset(households,sample.sampled_agent_idx)
print "sampled household index (", sample.sampled_agent_idx.size(), "/", households.n, "):"
print sample.sampled_agent_idx
print "sampled household_id:"
print sampled_hhs.get_attribute('household_id')
print "which respectively resides at grid_id:"
print sampled_hhs.get_attribute('grid_id')
print "alternative set:"
print gridcells.get_attribute_by_index("grid_id",sample.choiceset_idx)
print "the selected choice matrix:"
print sample.selected_choice

print "1 Elapsed time (fast)= " + str(end_time1 - start_time1)
print "2 Elapsed time (regular)= " + str(end_time2 - start_time2)
print "3 Elapsed time (super_fast) = " + str(end_time3 - start_time3)


#clear up the exported files and directory
if len(glob(bdir)) > 0:
    map(lambda x: os.remove(x), glob(bdir+'/*'))
    os.rmdir(bdir)
