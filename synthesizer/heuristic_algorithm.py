# Running IPF on Person and Household data

from psuedo_sparse_matrix import generate_index_matrix
import time
import MySQLdb
from math import exp, log
from numpy import asarray as arr
from numpy import ones, zeros


def heuristic_adjustment(db, pumano, index_matrix, weights, control, sp_matrix):
    dbc = db.cursor()
    ti =time.clock()
  

# Adjusting for household types
    dbc.execute('select hhlduniqueid from hhld_pums group by hhlduniqueid')
    hhld_colno = dbc.rowcount
    dbc.execute('select gquniqueid from gq_pums group by gquniqueid')
    gq_colno = dbc.rowcount

    hh_colno = hhld_colno + gq_colno
    tot_colno = index_matrix.shape[0]

    iteration = 0
    conv_criterion_array = []
    wts_personadj = []
    conv_criterion = 0
    convergence = 0
#    print 'Starting the Heuristic Procedure'    
    print 'iteration, Sum_Wts_Hhld_Adj, Sum_Wts_Person_Adj, Constraints, e-statistic, convergence (0/1)'
    while (iteration < 10 or convergence == 0):
        ti = time.clock()
        iteration = iteration + 1

# Adjusting for person types
        for i in index_matrix[hh_colno:,:]:
            adjustment = control[i[0]-2] / sum(weights[sp_matrix[i[1]-1:i[2], 2]] * sp_matrix[i[1]-1:i[2], 4])
            weights[sp_matrix[i[1]-1:i[2], 2]] = weights[sp_matrix[i[1]-1:i[2], 2]] * adjustment
        wts_personadj.append(sum(weights))

# Adjusting for housing types including both household and group quarters
        for i in index_matrix[:hh_colno,:]:
            if control[i[0]-2] == 0:
                print 'Zero Control'
            adjustment = control[i[0]-2] / sum(weights[sp_matrix[i[1]-1:i[2], 2]])
            weights[sp_matrix[i[1]-1:i[2], 2]] = weights[sp_matrix[i[1]-1:i[2], 2]] * adjustment
        
# Creating the evaluation statistic
        for i in index_matrix[hh_colno:,:]:
            dummy = (sum(weights[sp_matrix[i[1]-1:i[2], 2]] * sp_matrix[i[1]-1:i[2], 4]) - control[i[0]-2]) / control[i[0]-2]
            conv_criterion = conv_criterion + abs(dummy)

        """ Use the following lines if you are not going to use the whole PUMS sample for estimating weights for a small geography say you
        will just use the PUMS corresponding to the PUMA to which the small geography belongs
        sum_heuristic =0
        for i in weights:
            if i <0 and i <>-99:
                print 'wrong weight modified'
            if i>=0:
                sum_heuristic = sum_heuristic +i
        """
        conv_criterion = conv_criterion / ( tot_colno - hh_colno)
        conv_criterion_array.append(conv_criterion)
        if iteration >=2:
            convergence = abs(conv_criterion_array[-1] - conv_criterion_array[-2])
            if convergence < 1e-4:
                convergence = 1
            else:
                convergence = 0
        conv_criterion = 0
    conv_criterion = conv_criterion / ( tot_colno - hh_colno)
    print '%d, %.4f, %.4f, %d, %.4f, %d'%(iteration, sum(weights), wts_personadj[-1], tot_colno, conv_criterion_array[-1], convergence)
    return weights, conv_criterion_array, wts_personadj
        
# How to deal with the fact that zero marginals will multiply the weights out to zeros

if __name__ == '__main__':
    pass
