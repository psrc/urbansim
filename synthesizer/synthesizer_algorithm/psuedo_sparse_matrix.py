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

def populate_master_matrix(db, pumano, hhld_units, gq_units, hhld_dimensions, gq_dimensions, person_dimensions):
# First we create an empty matrix based on the dimensions of the hhhld, gq, and person control variables
    hhld_types = arr(hhld_dimensions).prod()
    gq_types = arr(gq_dimensions).prod()
    person_types = arr(person_dimensions).prod()

# We add 2 more columns to also store the puma id, and housing pums id. Also note that the matrix indices start from 0
# Layout of the master matrix is as follows - puma id (0 th column), housing pums id, hhld types frequency,
# gq types frequency, person types frequency
    total_cols = 4 + hhld_types + gq_types + person_types
    total_rows = hhld_units + gq_units
    matrix = sparse.lil_matrix((total_rows, total_cols))

# In this part we populate the matrix
    dbc = db.cursor()
    rowHhidDict = {}
    row = 0
    for control_type in ['hhld', 'gq', 'person']:
# Here we determine the starting column in the master matrix for the hhld types, gq types and person types frequency within each home
	if control_type == 'hhld':
            start = 3
        elif control_type == 'gq':
	    start = 3 + arr(hhld_dimensions).prod()
        else:
            start = 3 + arr(hhld_dimensions).prod() + arr(gq_dimensions).prod()

# Read the pums data from the mysql files to
        if pumano == 0 or pumano == 99999:
            dbc.execute('Select state, pumano, hhid, serialno, %suniqueid from %s_sample' 
                        %(control_type, control_type))
        else:
            dbc.execute('Select state, pumano, hhid, serialno, %suniqueid from %s_sample where pumano = %s' 
                        %(control_type, control_type, pumano))

        result = arr(dbc.fetchall(), int)

        #print  result
# Master Matrix is populated here

        if control_type == 'hhld':

            for i in result[:,2]:
# Storing the pumano, housing puma id for all housing units
                rowHhidDict[i] = row
                matrix[row,:4] = result[row,:4]
                row = row + 1

        if control_type == 'gq':
            for i in result[:,2]:
                rowHhidDict[i] = row
                matrix[row,:4] = result[(row - hhld_units), :4]
                row = row + 1

# Populating the household type, gq type, person type frequencies
	for i in range(dbc.rowcount):
            matRow = rowHhidDict[result[i, 2]]
            matrix[matRow, start+result[i, -1]] = matrix[matRow, start+result[i, -1]] + 1

    dbc.close()
    db.commit()
    #print matrix[:100,:]
    return matrix


def psuedo_sparse_matrix(db, matrix, pumano):
# Sprase representation of the psuedo matrix
    sparse_matrix = []
    dummy = []
    rows = 0
    cols = 4
    temp_file = open('dummy.txt', 'w')

    for i in matrix.rows:
        if i:
            for j in i[4:]:
                dummy.append(matrix[rows, 3])
                dummy.append(rows)
                dummy.append(j)
                dummy.append(matrix.data[rows][cols])
                sparse_matrix.append(dummy)
                dummy = []
                temp_file.write(str(matrix[rows, 1]) + '\t' + str(rows) + '\t' + str(j) + '\t' + str(matrix.data[rows][cols]))
                temp_file.write('\n')
                cols = cols + 1
        cols = 4
        rows = rows + 1
    temp_file.close()

    path =  os.getcwd()+'\dummy.txt'
    path = os.path.normcase(path)
    path = path.replace('\\', '/')

    dbc = db.cursor()
    try:
        dbc.execute('create table sparse_matrix_%s(hhpumsid bigint, rowno mediumint, colno mediumint, freq mediumint);'%(pumano))
        dbc.execute("load data local infile '%s' into table sparse_matrix_%s" %(path, pumano))
    except:
        dbc.execute('drop table sparse_matrix_%s'%(pumano))
        dbc.execute('create table sparse_matrix_%s(hhpumsid bigint, rowno mediumint, colno mediumint, freq mediumint);'%(pumano))
        dbc.execute("load data local infile '%s' into table sparse_matrix_%s" %(path, pumano))
    os.remove('dummy.txt')
    dbc.close()
    db.commit()
    return arr(sparse_matrix)

def generate_index_matrix(db, pumano):
# Creating an index matrix that stores the row numbers for each constraint
    dbc = db.cursor()
    try:
        dbc.execute("drop table sparse_matrix1_%s"%(pumano))
    except:
        pass
    dbc.execute("create table sparse_matrix1_%s select * from sparse_matrix_%s order by colno, rowno"%(pumano, pumano))
    dbc.execute("alter table sparse_matrix1_%s add column id bigint primary key auto_increment not null first"%(pumano))
    try:
        dbc.execute("create table index_matrix_%s select colno, min(id), max(id) from sparse_matrix1_%s group by colno"%(pumano, pumano))
    except:
	dbc.execute("drop table index_matrix_%s"%(pumano))
        dbc.execute("create table index_matrix_%s select colno, min(id), max(id) from sparse_matrix1_%s group by colno"%(pumano, pumano))
    dbc.execute("select * from index_matrix_%s"%(pumano))
    result = dbc.fetchall()
    index_matrix = arr(result, int)
    dbc.close()
    db.commit()
    return index_matrix



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

