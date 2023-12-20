import MySQLdb
import numpy
from . import adjusting_pums_joint_distribution
from . import drawing_households
from . import psuedo_sparse_matrix
import time


def prepare_data(db):
#    Processes/ methods to be called at the beginning of the pop_synthesis process 
    dbc = db.cursor()

# Identifying the number of housing units to build the Master Matrix
    dbc.execute('select * from housing_pums')
    housing_units = dbc.rowcount
    ti = time.perf_counter()
# Identifying the control variables for the households, gq's, and persons
    hhld_control_variables = adjusting_pums_joint_distribution.choose_control_variables(db, 'hhld')
    gq_control_variables = adjusting_pums_joint_distribution.choose_control_variables(db, 'gq')
    person_control_variables = adjusting_pums_joint_distribution.choose_control_variables(db, 'person')

# Identifying the number of categories within each control variable for the households, gq's, and persons
    hhld_dimensions = numpy.asarray(adjusting_pums_joint_distribution.create_dimensions(db, 'hhld', hhld_control_variables))
    gq_dimensions = numpy.asarray(adjusting_pums_joint_distribution.create_dimensions(db, 'gq', gq_control_variables))
    person_dimensions = numpy.asarray(adjusting_pums_joint_distribution.create_dimensions(db, 'person', person_control_variables))
        
    print('Dimensions and Control Variables created in %.4f' %(time.perf_counter()-ti))
    ti = time.perf_counter()
    
    update_string = adjusting_pums_joint_distribution.create_update_string(db, hhld_control_variables, hhld_dimensions)
    adjusting_pums_joint_distribution.add_unique_id(db, 'hhld', update_string)
    update_string = adjusting_pums_joint_distribution.create_update_string(db, gq_control_variables, gq_dimensions)
    adjusting_pums_joint_distribution.add_unique_id(db, 'gq', update_string)
    update_string = adjusting_pums_joint_distribution.create_update_string(db, person_control_variables, person_dimensions)
    adjusting_pums_joint_distribution.add_unique_id(db, 'person', update_string)
    
    print('Uniqueid\'s created in %.4f' %(time.perf_counter()-ti))
    ti = time.perf_counter()
    
# Populating the Master Matrix	
    populated_matrix = psuedo_sparse_matrix.populate_master_matrix(db, 0, housing_units, hhld_dimensions, 
                                                                                               gq_dimensions, person_dimensions)
    print('Frequency Matrix Populated in %.4f' %(time.perf_counter()-ti))
    ti = time.perf_counter()

# Sparse representation of the Master Matrix    
    ps_sp_matrix = psuedo_sparse_matrix.psuedo_sparse_matrix(db, populated_matrix, 0)
    print('Psuedo Sparse Representation of the Frequency Matrix created in %.4f' %(time.perf_counter()-ti))
    ti = time.perf_counter()
#______________________________________________________________________
#Creating Index Matrix
    index_matrix = psuedo_sparse_matrix.generate_index_matrix(db, 0)
    print('Index matrix created in %.4f' %(time.perf_counter()-ti))
    ti = time.perf_counter()
    dbc.close()
#______________________________________________________________________
# creating synthetic_population tables in MySQL
    drawing_households.create_synthetic_attribute_tables(db)

# Total PUMS Sample x composite_type adjustment for hhld    
    adjusting_pums_joint_distribution.create_joint_dist(db, 'hhld', hhld_control_variables, hhld_dimensions, 0, 0, 0)

# Total PUMS Sample x composite_type adjustment for gq    
    adjusting_pums_joint_distribution.create_joint_dist(db, 'gq', gq_control_variables, gq_dimensions, 0, 0, 0)

# Total PUMS Sample x composite_type adjustment for person    
    adjusting_pums_joint_distribution.create_joint_dist(db, 'person', person_control_variables, person_dimensions, 0, 0, 0)


if __name__ == '__main__':
    db = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '1234', db = 'ncpopsyn')
    prepare_data(db)
    db.commit()
    db.close()
    
