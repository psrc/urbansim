# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

# Running IPF on Person and Household data

import time
import MySQLdb
import operator
import os
from math import exp
from numpy import asarray as arr
from numpy import ones, zeros
from numpy import histogram
from scipy import sparse
from scipy import poly1d
import adjusting_sample_joint_distribution as adjusting_sample_joint_distribution

def populate_master_matrix(db, pumano, hhld_units, hhld_dimensions):
# First we create an empty matrix based on the dimensions of the hhhld control variables
    hhld_types = arr(hhld_dimensions).prod()


# We add 2 more columns to also store the puma id, and housing pums id. Also note that the matrix indices start from 0
# Layout of the master matrix is as follows - puma id (0 th column), housing pums id, hhld types frequency,

    total_cols = 4 + hhld_types 
    total_rows = hhld_units 
    matrix = sparse.lil_matrix((total_rows, total_cols))

# In this part we populate the matrix
    dbc = db.cursor()
    rowHhidDict = {}
    row = 0
    for control_type in ['hhld']:
# Here we determine the starting column in the master matrix for the hhld types frequency within each home
        start = 3

# Read the pums data from the mysql files to
        if pumano == 0 or pumano == 99999:
            dbc.execute('Select state, pumano, hhid, serialno, %suniqueid from %s_sample'
                        %(control_type, control_type))
        else:
            dbc.execute('Select state, pumano, hhid, serialno, %suniqueid from %s_sample where pumano = %s'
                        %(control_type, control_type, pumano))



        result = arr(dbc.fetchall(), int)


# Master Matrix is populated here

        if control_type == 'hhld':

            for i in result[:,2]:
# Storing the pumano, housing puma id for all housing units
                rowHhidDict[i] = row
                matrix[row,:4] = result[row,:4]
                row = row + 1

# Populating the household type frequencies
	for i in range(dbc.rowcount):
            matRow = rowHhidDict[result[i, 2]]
            matrix[matRow, start+result[i, -1]] = matrix[matRow, start+result[i, -1]] + 1

    dbc.close()
    db.commit()
    return matrix


if __name__ == '__main__':

    sample_size = 156601
    pumano = 0

    db = MySQLdb.connect(user = 'root', passwd = '1234', db = 'ncpopsyn')

    hhld_dimensions = arr([5,7,8])
    person_dimensions = arr([2, 10, 7])

    hhld_control_variables = adjusting_sample_joint_distribution.choose_control_variables(db, 'hhld')
    person_control_variables = adjusting_sample_joint_distribution.choose_control_variables(db, 'person')

    update_string = adjusting_sample_joint_distribution.create_update_string(db, hhld_control_variables, hhld_dimensions)
    adjusting_sample_joint_distribution.add_unique_id(db, 'hhld', update_string)

    update_string = adjusting_sample_joint_distribution.create_update_string(db, person_control_variables, person_dimensions)
    adjusting_sample_joint_distribution.add_unique_id(db, 'person', update_string)

    ti = time.clock()
    print 'start - %s'%ti
    populated_matrix = populate_master_matrix(db, pumano, sample_size, hhld_dimensions, person_dimensions)
    print 'End Populated matrix - %s'%(time.clock()-ti)


    ti = time.clock()
    ps_sp_matrix = psuedo_sparse_matrix(db, populated_matrix, pumano)
    print 'Psuedo Sparse Matrix- %s'%(time.clock()-ti)


    index = generate_index_matrix(db, 0)

