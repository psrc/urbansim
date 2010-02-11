# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

# This file contains a MySQL class that helps manipulate data. The instance of
# the class also stores the results of the query as a list.

import time
import MySQLdb
import os
from re import match
from numpy import asarray as arr
from numpy import fix as quo
from numpy import zeros
from defining_a_database import *

def create_dimensions(db, synthesis_type, control_variables):
    pums = database(db, '%s_pums'%synthesis_type)
    dimensions = []
    if len(control_variables) > 0:
        for i in control_variables:
            dimensions.append(pums.categories(i))
    return dimensions

def choose_control_variables(db, synthesis_type):
    if synthesis_type == 'hhld':
#        control_variables = [ 'hhldtype', 'hhldsize', 'hhldinc']
        control_variables = ['childpresence', 'hhldtype', 'hhldsize', 'hhldinc']
    elif synthesis_type == 'gq':
        control_variables = ['groupquarter']
    elif synthesis_type == 'person':
        control_variables = ['gender', 'age', 'race']
#        control_variables = ['gender', 'age', 'race', 'employment']
    return control_variables

def create_update_string(db, control_variables, dimensions):
    update_string = ''
    for i in range(len(control_variables)):
        if i == 0:
	    if len(control_variables) ==1:
		update_string = '%s' %(control_variables[i])
	    else:
                update_string = '(%s - 1)* %s' %(control_variables[i], dimensions[i+1:].prod())
        elif i == len(control_variables)-1:
            update_string = update_string + ' + ' + '(%s) * %s' %(control_variables[i], dimensions[i+1:].prod())
        else:
            update_string = update_string + ' + ' + '(%s - 1) * %s' %(control_variables[i], dimensions[i+1:].prod())
    return(update_string)

def add_unique_id(db, tablename, synthesis_type, update_string):
    dbc = db.cursor()

    if len(update_string) >0:
        try:
            dbc.execute('alter table %s ADD %suniqueid int'%(tablename, synthesis_type))
        except Exception, e:
            pass
        dbc.execute('update %s set %suniqueid = %s' %(tablename, synthesis_type, update_string))
    dbc.close()
    db.commit()

def create_joint_dist(db, synthesis_type, control_variables, dimensions, pumano = 0, tract = 0, bg = 0):

    dbc = db.cursor()
    pums = database(db, '%s_pums'%synthesis_type)
    dummy = create_aggregation_string(control_variables)

    table_rows = dimensions.cumprod()[-1]
    table_cols = len(dimensions) + 4
    dummy_table = zeros((table_rows, table_cols), dtype =int)
    index_array = num_breakdown(dimensions)


    try:
        dbc.execute('create table %s_%s_joint_dist select %s from %s_pums where 0 '%(synthesis_type, pumano, dummy, synthesis_type))
        dbc.execute('alter table %s_%s_joint_dist add pumano int first'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add tract int after pumano'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add bg int after tract'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add frequency float(27)'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add index(tract, bg)'%(synthesis_type, pumano))
    except:
#        print 'Table %s_%s_joint_dist present' %(synthesis_type, pumano)
        pass

    variable_list = 'pumano, tract, bg, '
    for i in control_variables:
        variable_list = variable_list + i + ', '
    variable_list = variable_list + 'frequency'

    if pumano ==0:
        dbc.execute('select %s, count(*), %suniqueid from %s_pums group by %s '%(dummy, synthesis_type, synthesis_type, dummy))
        #print ('select %s, count(*), %suniqueid from %s_pums group by %s '%(dummy, synthesis_type, synthesis_type, dummy))
        result = arr(dbc.fetchall())
        dummy_table[:,:3] = [pumano, tract, bg]
        dummy_table[:,3:-1] = index_array
        dummy_table[result[:,-1]-1,-1] = result[:,-2]
    else:
        dbc.execute('select %s, count(*), %suniqueid from %s_pums where pumano = %s group by %s '%(dummy, synthesis_type, synthesis_type, pumano, dummy))
        result = arr(dbc.fetchall())
        dummy_table[:,:3] = [pumano, tract, bg]
        dummy_table[:,3:-1] = index_array
        dummy_table[result[:,-1]-1,-1] = result[:,-2]


    dbc.execute('delete from %s_%s_joint_dist where tract = %s and bg = %s' %(synthesis_type, pumano, tract, bg))
    dummy_table = str([tuple(i) for i in dummy_table])

    #try:
    #    dbc.execute('alter table %s_%s_joint_dist drop column %suniqueid' %(synthesis_type, pumano, synthesis_type))
    #except:
    #    pass

    dbc.execute('insert into %s_%s_joint_dist (%s) values %s' %(synthesis_type, pumano, variable_list, dummy_table[1:-1]))
    dbc.close()

    update_string = create_update_string(db, control_variables, dimensions)
    add_unique_id(db, '%s_%s_joint_dist' %(synthesis_type, pumano), synthesis_type, update_string)

    db.commit()

def num_breakdown(dimensions):
    """This method breaksdown the cell number 'n' into its index wrt to the
    categories defined by 'm' """
    index_array = []
    index = []
    table_size = dimensions.cumprod()[-1]
    composite_index = range(table_size)

    for j in composite_index:
        n = j
        for i in reversed(dimensions):
            quotient = quo(n/i)
            remainder = n - quotient * i
            n = quotient
            index.append(remainder+1)
        index.reverse()
        index_array.append(index)
        index = []
    return index_array

def create_aggregation_string(control_variables):
    string = ''
    for dummy in control_variables:
        if len(string) == 0:
            string = string + dummy
        else:
            string = string + ',' + dummy
    return string


def adjust_weights(db, synthesis_type, control_variables, pumano = 0, tract = 0, bg = 0):

    dbc = db.cursor()

    control_marginals = prepare_control_marginals (db, synthesis_type, control_variables, pumano, tract, bg)

    tol = 1
    iteration = 0
    adjustment_old = []
    target_adjustment = []
    while (tol):

        iteration = iteration +1
        adjustment_all = []

        for i in range(len(control_variables)):
            adjusted_marginals = marginals(db, synthesis_type, control_variables[i], pumano, tract, bg)

            for j in range(len(adjusted_marginals)):
                if adjusted_marginals[j] == 0:
                    adjusted_marginals[j] = 1

            adjustment = arr(control_marginals[i]) / arr(adjusted_marginals)
            update_weights(db, synthesis_type, control_variables, control_variables[i], pumano, tract, bg, adjustment)

            for k in adjustment:
                adjustment_all.append(k)
                if iteration == 1:
                    if k == 0:
                        adjustment_old.append(0)
                    else:
                        adjustment_old.append(k/k)
                    target_adjustment = [adjustment_old]

        tol = tolerance(adjustment_all, adjustment_old, iteration)
        adjustment_old = adjustment_all
        adjustment_characteristic = abs(arr(adjustment_all) - arr(target_adjustment)).sum() / len(adjustment_all)


    if (iteration>=250):
        pass
#        print "Maximum iterations reached\n"
    else:
#        print "Convergence Achieved in iterations - %s\n" %iteration
        pass
#    print "Marginals off by - %s" %adjustment_characteristic
    dbc.close()
    db.commit()

def marginals(db, synthesis_type, variable_name, pumano, tract, bg):
# Returns the marginals wrt the entered dimension for calculating the adjustment in each iteration
    dbc = db.cursor()
    dbc.execute('select %s, sum(frequency) from %s_%s_joint_dist where tract = %s and bg = %s group by %s' %( variable_name, synthesis_type, pumano, tract, bg, variable_name))
    result = dbc.fetchall()
    marginal = []
    for i in result:
        marginal.append(float(i[1]))
    dbc.close()
    db.commit()
    return marginal

def update_weights (db, synthesis_type, control_variables, control_variable, pumano, tract, bg, adjustment):
    dbc = db.cursor()
# Updating weights after calculating adjustments along each dimension
    dbc.execute('select %s from %s_%s_joint_dist where tract = %s and bg = %s group by %s  ' %( control_variable, synthesis_type, pumano, tract, bg, control_variable))
    result = dbc.fetchall()
    for i in range(dbc.rowcount):
        dbc.execute('update %s_%s_joint_dist set frequency = frequency * %s where %s = %s and tract = %s and bg = %s' %(synthesis_type, pumano, adjustment[i], control_variable, result[i][0], tract, bg))
    dbc.close()
    db.commit()

def tolerance (adjustment_all, adjustment_old, iteration):
    adjustment_all = arr(adjustment_all)
    adjustment_old = arr(adjustment_old)
    adjustment_difference = abs(adjustment_all - adjustment_old)
    adjustment_convergence_characteristic = adjustment_difference.cumsum()[-1]
    if adjustment_convergence_characteristic > 1e-6:
        return 1
    else:
#        print "Convergence Criterion - %s" %adjustment_convergence_characteristic
        return 0

def prepare_control_marginals(db, synthesis_type, control_variables, pumano, tract, bg):

    dbc = db.cursor()
    if synthesis_type == 'hhld' or synthesis_type == 'gq':
	type = 'housing'
    else:
	type = 'person'
    marginals = database(db, '%s_marginals'%type)
    variable_names = marginals.variables()
    control_marginals = []
    for dummy in control_variables:
        variable_marginals =[]
        for i in variable_names:
            if match(dummy, i):
#                if synthesis_type == 'hhld' or synthesis_type =='person' or synthesis_type == 'gq':
                dbc.execute('select %s from %s_marginals where pumano = %s and tract = %s and bg = %s'%(i, type, pumano, tract, bg))
                result = dbc.fetchall()
                if result[0][0] <> 0:
                    variable_marginals.append(result[0][0])
                else:
                    variable_marginals.append(0.1)
        control_marginals.append(variable_marginals)
    dbc.close()
    db.commit()
    return control_marginals


def create_matching_string(table_name1, table_name2, control_variables):
    string = ''
    for dummy in control_variables:
        if len(string) == 0:
            string = string + table_name1 + '.' + dummy + '=' + table_name2 + '.' + dummy
        else:
            string = string + ' '+'and' + ' ' + table_name1 + '.' + dummy + '=' + table_name2 + '.' + dummy
    return string

def create_adjusted_frequencies(db, synthesis_type, control_variables, pumano, tract= 0, bg= 0):
    dbc = db.cursor()
    dummy_order_string = create_aggregation_string(control_variables)
    puma_table = ('%s_%s_joint_dist'%(synthesis_type, pumano))
    pums_table = ('%s_%s_joint_dist'%(synthesis_type, 0))

    dbc.execute('select * from %s where tract = %s and bg = %s order by %s' %(puma_table, tract, bg, dummy_order_string))
    puma_joint = arr(dbc.fetchall())
    puma_prob = puma_joint[:,-2] / sum(puma_joint[:,-2])
    upper_prob_bound = 0.5 / sum(puma_joint[:,-2])

    dbc.execute('select * from %s order by %s' %(pums_table, dummy_order_string))
    pums_joint = arr(dbc.fetchall())
    pums_prob = pums_joint[:,-2] / sum(pums_joint[:,-2])

    puma_adjustment = (pums_prob <= upper_prob_bound) * pums_prob + (pums_prob > upper_prob_bound) * upper_prob_bound
    correction = 1 - sum((puma_prob == 0) * puma_adjustment)
    puma_prob = ((puma_prob <> 0) * correction * puma_prob +
                 (puma_prob == 0) * puma_adjustment)
    puma_joint[:,-2] = sum(puma_joint[:,-2]) * puma_prob

    dbc.execute('delete from %s where tract = %s and bg = %s'%(puma_table, tract, bg))
    puma_joint_dummy = str([tuple(i) for i in puma_joint])
    dbc.execute('insert into %s values %s' %(puma_table, puma_joint_dummy[1:-1]))
    dbc.close()
    db.commit()

if __name__ == '__main__':
    pass




