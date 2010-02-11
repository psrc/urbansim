# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import MySQLdb
import numpy
import adjusting_sample_joint_distribution
import drawing_households
import psuedo_sparse_matrix
import psuedo_sparse_matrix_noper
import time

from PyQt4.QtCore import *

def prepare_data_noper(db, project):


    dbc = db.cursor()
    
    scenarioDatabase = '%s%s%s' %(project.name, 'scenario', project.scenario)
    projectDatabase = project.name

    try:
        dbc.execute('drop table %s.hhld_sample' %(scenarioDatabase))
        dbc.execute('drop table %s.gq_sample' %(scenarioDatabase))
        dbc.execute('drop table %s.person_sample' %(scenarioDatabase))
        dbc.execute('drop table %s.hhld_marginals' %(scenarioDatabase))
        dbc.execute('drop table %s.gq_marginals' %(scenarioDatabase))
        dbc.execute('drop table %s.person_marginals' %(scenarioDatabase))
        if project.sampleUserProv.defSource == 'ACS 2005-2007':
            dbc.execute('drop table %s.serialcorr' %(scenarioDatabase))

    except:
        pass

    dbc.execute('create table %s.hhld_sample select * from %s.hhld_sample'
                %(scenarioDatabase, projectDatabase))
    dbc.execute('alter table %s.hhld_sample add index(serialno)' %(scenarioDatabase))
    
    dbc.execute('create table %s.gq_sample select * from %s.gq_sample'
                %(scenarioDatabase, projectDatabase))
    dbc.execute('alter table %s.gq_sample add index(serialno)' %(scenarioDatabase))

    dbc.execute('create table %s.person_sample select * from %s.person_sample'
                %(scenarioDatabase, projectDatabase))
    dbc.execute('alter table %s.person_sample add index(serialno, pnum)' %(scenarioDatabase))

    if project.selVariableDicts.hhldMargsModify:
        dbc.execute('create table %s.hhld_marginals select * from %s.hhld_marginals_modpgq'
                    %(scenarioDatabase, projectDatabase))
    else:
        dbc.execute('create table %s.hhld_marginals select * from %s.hhld_marginals'
                    %(scenarioDatabase, projectDatabase))


    dbc.execute('create table %s.gq_marginals select * from %s.gq_marginals'
                %(scenarioDatabase, projectDatabase))

    if project.sampleUserProv.defSource == 'ACS 2005-2007':
        dbc.execute('create table %s.serialcorr select * from %s.serialcorr'
                    %(scenarioDatabase, projectDatabase))

    try:
        dbc.execute('create table %s.person_marginals select * from %s.person_marginals'
                    %(scenarioDatabase, projectDatabase))
    except Exception, e:
        print e
        pass


#    Processes/ methods to be called at the beginning of the pop_synthesis process


# Identifying the number of housing units to build the Master Matrix
    dbc.execute('select * from hhld_sample')
    hhld_units = dbc.rowcount
    dbc.execute('select * from gq_sample')
    gq_units = dbc.rowcount

    ti = time.clock()
# Identifying the control variables for the households, gq's, and persons
    hhld_control_variables = project.hhldVars
    gq_control_variables = project.gqVars

# Identifying the number of categories within each control variable for the households, gq's, and persons
    hhld_dimensions = project.hhldDims
    gq_dimensions = project.gqDims

    print '------------------------------------------------------------------'
    print 'Preparing Data for the Synthesizer Run'
    print '------------------------------------------------------------------'




    print 'Dimensions and Control Variables in %.4f' %(time.clock()-ti)
    ti = time.clock()

    update_string = adjusting_sample_joint_distribution.create_update_string(db, hhld_control_variables, hhld_dimensions)
    adjusting_sample_joint_distribution.add_unique_id(db, 'hhld_sample', 'hhld', update_string)
    update_string = adjusting_sample_joint_distribution.create_update_string(db, gq_control_variables, gq_dimensions)
    adjusting_sample_joint_distribution.add_unique_id(db, 'gq_sample', 'gq', update_string)
    adjusting_sample_joint_distribution.add_unique_id(db, 'person_sample', 'person', '1')

    print 'Uniqueid\'s in %.4fs' %(time.clock()-ti)
    ti = time.clock()

# Populating the Master Matrix
    populated_matrix = psuedo_sparse_matrix_noper.populate_master_matrix(db, 99999, hhld_units, gq_units, hhld_dimensions,
                                                                                               gq_dimensions)
    print 'Populated in %.4fs' %(time.clock()-ti)
    ti = time.clock()

# Sparse representation of the Master Matrix
    ps_sp_matrix = psuedo_sparse_matrix.psuedo_sparse_matrix(db, populated_matrix, 99999)
    print 'Psuedo Sparse Matrix in %.4fs' %(time.clock()-ti)
    ti = time.clock()
#______________________________________________________________________
#Creating Index Matrix
    index_matrix = psuedo_sparse_matrix.generate_index_matrix(db, 99999)
    print 'Index Matrix in %.4fs' %(time.clock()-ti)
    ti = time.clock()
    dbc.close()

#______________________________________________________________________
# creating synthetic_population tables in MySQL
    drawing_households.create_synthetic_attribute_tables(db)

# creating performance_statistics table in MySQL
    drawing_households.create_performance_table(db)

# Total PUMS Sample x composite_type adjustment for hhld
    adjusting_sample_joint_distribution.create_joint_dist(db, 'hhld', hhld_control_variables, hhld_dimensions, 0, 0, 0)

# Total PUMS Sample x composite_type adjustment for gq
    adjusting_sample_joint_distribution.create_joint_dist(db, 'gq', gq_control_variables, gq_dimensions, 0, 0, 0)

if __name__ == '__main__':


    db = MySQLdb.connect(user = 'root', passwd = '1234', db = 'aacog')
    prepare_data(db)
    db.commit()
    db.close()

