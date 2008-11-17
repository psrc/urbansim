#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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


import os, sys, string
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.opus_database import OpusDatabase

import numpy
import synthesizer.adjusting_pums_joint_distribution
import synthesizer.drawing_households
import synthesizer.psuedo_sparse_matrix
import time


def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)


    # get parameter values
    database_name = param_dict['database_name']
    database_server_connection = param_dict['database_server_connection']

    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    opus_db = OpusDatabase(database_server_configuration=dbs_config, database_name=database_name)
    
    

#    Processes/ methods to be called at the beginning of the pop_synthesis process 
    
# Identifying the number of housing units to build the Master Matrix
    housing_units = opus_db.execute('select count(*) from housing_pums').fetchone()[0]

    ti = time.clock()
# Identifying the control variables for the households, gq's, and persons
    hhld_control_variables = adjusting_pums_joint_distribution.choose_control_variables(opus_db, 'hhld')
    gq_control_variables = adjusting_pums_joint_distribution.choose_control_variables(opus_db, 'gq')
    person_control_variables = adjusting_pums_joint_distribution.choose_control_variables(opus_db, 'person')

# Identifying the number of categories within each control variable for the households, gq's, and persons
    hhld_dimensions = numpy.asarray(adjusting_pums_joint_distribution.create_dimensions(opus_db, 'hhld', hhld_control_variables))
    gq_dimensions = numpy.asarray(adjusting_pums_joint_distribution.create_dimensions(opus_db, 'gq', gq_control_variables))
    person_dimensions = numpy.asarray(adjusting_pums_joint_distribution.create_dimensions(opus_db, 'person', person_control_variables))
        
    print 'Dimensions and Control Variables created in %.4f' %(time.clock()-ti)
    ti = time.clock()
    
    update_string = adjusting_pums_joint_distribution.create_update_string(opus_db, hhld_control_variables, hhld_dimensions)
    adjusting_pums_joint_distribution.add_unique_id(opus_db, 'hhld', update_string)
    update_string = adjusting_pums_joint_distribution.create_update_string(opus_db, gq_control_variables, gq_dimensions)
    adjusting_pums_joint_distribution.add_unique_id(opus_db, 'gq', update_string)
    update_string = adjusting_pums_joint_distribution.create_update_string(opus_db, person_control_variables, person_dimensions)
    adjusting_pums_joint_distribution.add_unique_id(opus_db, 'person', update_string)
    
    print 'Uniqueid\'s created in %.4f' %(time.clock()-ti)
    ti = time.clock()
    
# Populating the Master Matrix    
    populated_matrix = psuedo_sparse_matrix.populate_master_matrix(opus_db, 0, housing_units, hhld_dimensions, 
                                                                                               gq_dimensions, person_dimensions)
    print 'Frequency Matrix Populated in %.4f' %(time.clock()-ti)
    ti = time.clock()

# Sparse representation of the Master Matrix    
    ps_sp_matrix = psuedo_sparse_matrix.psuedo_sparse_matrix(opus_db, populated_matrix, 0)
    print 'Psuedo Sparse Representation of the Frequency Matrix created in %.4f' %(time.clock()-ti)
    ti = time.clock()
#______________________________________________________________________
#Creating Index Matrix
    index_matrix = psuedo_sparse_matrix.generate_index_matrix(opus_db, 0)
    print 'Index matrix created in %.4f' %(time.clock()-ti)
    ti = time.clock()
    #dbc.close()
#______________________________________________________________________
# creating synthetic_population tables in MySQL
    drawing_households.create_synthetic_attribute_tables(opus_db)

# Total PUMS Sample x composite_type adjustment for hhld    
    adjusting_pums_joint_distribution.create_joint_dist(opus_db, 'hhld', hhld_control_variables, hhld_dimensions, 0, 0, 0)

# Total PUMS Sample x composite_type adjustment for gq    
    adjusting_pums_joint_distribution.create_joint_dist(opus_db, 'gq', gq_control_variables, gq_dimensions, 0, 0, 0)

# Total PUMS Sample x composite_type adjustment for person    
    adjusting_pums_joint_distribution.create_joint_dist(opus_db, 'person', person_control_variables, person_dimensions, 0, 0, 0)

opus_db.close()
