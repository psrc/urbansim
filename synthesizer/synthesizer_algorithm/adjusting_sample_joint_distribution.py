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
            dbc.execute('alter table %s ADD %suniqueid bigint'%(tablename, synthesis_type))
        except Exception, e:
            pass
        dbc.execute('update %s set %suniqueid = %s' %(tablename, synthesis_type, update_string))
    dbc.close()
    db.commit()

def create_joint_dist(db, synthesis_type, control_variables, dimensions, pumano = 0, tract = 0, bg = 0):

    dbc = db.cursor()
    pums = database(db, '%s_sample'%synthesis_type)
    dummy = create_aggregation_string(control_variables)

    table_rows = dimensions.cumprod()[-1]
    table_cols = len(dimensions) + 4
    dummy_table = zeros((table_rows, table_cols), dtype =int)
    index_array = num_breakdown(dimensions)


    try:
        dbc.execute('create table %s_%s_joint_dist select %s from %s_sample where 0 '%(synthesis_type, pumano, dummy, synthesis_type))
        dbc.execute('alter table %s_%s_joint_dist add pumano bigint first'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add tract bigint after pumano'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add bg bigint after tract'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add frequency float(27)'%(synthesis_type, pumano))
        dbc.execute('alter table %s_%s_joint_dist add index(tract, bg)'%(synthesis_type, pumano))
    except Exception, e:
        #print e
        #print 'Table %s_%s_joint_dist present' %(synthesis_type, pumano)
        pass

    variable_list = 'pumano, tract, bg, '
    for i in control_variables:
        variable_list = variable_list + i + ', '
    variable_list = variable_list + 'frequency'

    if pumano >= 99999000 or pumano == 0:
        dbc.execute('select %s, count(*), %suniqueid from %s_sample group by %s '%(dummy, synthesis_type, synthesis_type, dummy))
        #print ('select %s, count(*), %suniqueid from %s_sample group by %s '%(dummy, synthesis_type, synthesis_type, dummy))
        result = arr(dbc.fetchall(), int)
        dummy_table[:,:3] = [pumano, tract, bg]
        dummy_table[:,3:-1] = index_array
        dummy_table[result[:,-1]-1,-1] = result[:,-2]
    else:
        dbc.execute('select %s, count(*), %suniqueid from %s_sample where pumano = %s group by %s '%(dummy, synthesis_type, synthesis_type, pumano, dummy))
        result = arr(dbc.fetchall(), int)
        if result.shape[0] == 0:
            print "The PUMS sample for the corresponding PUMA is empty. Therefore sample from the entire region is considered for the geography."
            dbc.execute('select %s, count(*), %suniqueid from %s_sample group by %s '%(dummy, synthesis_type, synthesis_type, dummy))
            result = arr(dbc.fetchall(), int)
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


def adjust_weights(db, synthesis_type, control_variables, varCorrDict, controlAdjDict,
                   state, county, pumano=0, tract=0, bg=0, parameters=0, hhldsizeMargsMod=False):

    dbc = db.cursor()

    control_marginals = prepare_control_marginals (db, synthesis_type, control_variables, varCorrDict, 
                                                   controlAdjDict, state, county, tract, bg, hhldsizeMargsMod)

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

        tol = tolerance(adjustment_all, adjustment_old, iteration, parameters)
        adjustment_old = adjustment_all
        adjustment_characteristic = abs(arr(adjustment_all) - arr(target_adjustment)).sum() / len(adjustment_all)


    if (iteration>=parameters.ipfIter):
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
    result = arr(dbc.fetchall(), float)
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
    rows = dbc.rowcount

    for i in range(rows):
        dbc.execute('update %s_%s_joint_dist set frequency = frequency * %s where %s = %s and tract = %s and bg = %s and frequency > 1e-300' %(synthesis_type, pumano, adjustment[i], control_variable, result[i][0], tract, bg))
    dbc.close()
    db.commit()

def tolerance (adjustment_all, adjustment_old, iteration, parameters):
    adjustment_all = arr(adjustment_all)
    adjustment_old = arr(adjustment_old)
    adjustment_difference = abs(adjustment_all - adjustment_old)
    adjustment_convergence_characteristic = adjustment_difference.cumsum()[-1]
    if adjustment_convergence_characteristic > parameters.ipfTol:
        return 1
    else:
#        print "Convergence Criterion - %s" %adjustment_convergence_characteristic
        return 0

def prepare_control_marginals(db, synthesis_type, control_variables, varCorrDict, controlAdjDict,
                              state, county, tract, bg, hhldsizeMargsMod=False):

    dbc = db.cursor()
    marginals = database(db, '%s_marginals'%synthesis_type)
    variable_names = marginals.variables()
    control_marginals = []
    #control_marginals_sum = []
    for dummy in control_variables:
        dbc.execute('select %s from %s_sample group by %s' %(dummy, synthesis_type, dummy))
        cats = arr(dbc.fetchall(), float)
        #print dummy, cats

        selVar = dummy
        selGeography = "%s,%s,%s,%s" %(state, county, tract, bg)
        
        variable_marginals1=[]
        try:
            #print hhldsizeMargsMod
            if (not hhldsizeMargsMod and synthesis_type == 'hhld') or synthesis_type <> 'hhld':
                #print 'household not modified in correspondence'
                variable_marginals_adj = controlAdjDict[selGeography][selVar]
            #print 'adjustment', variable_marginals_adj[0], variable_marginals_adj[1]
                for i in variable_marginals_adj[1]:
                    if i>0:
                        variable_marginals1.append(i)
                    else:
                        variable_marginals1.append(0.1)
            #check_marginal_sum = sum(variable_marginals1)
            else:
                raise Exception, 'Household marginal distributions modified to account for person total inconsistency'
        except Exception ,e:
            #print 'Exception: %s' %e

            #check_marginal_sum = 0
            for i in cats:
                corrVar = varCorrDict['%s%s' %(dummy, int(i[0]))]
                dbc.execute('select %s from %s_marginals where county = %s and tract = %s and bg = %s' %(corrVar, synthesis_type, county, tract, bg))
                result = arr(dbc.fetchall(), float)
                #check_marginal_sum = result[0][0] + check_marginal_sum

                if result[0][0] > 0:
                    variable_marginals1.append(result[0][0])
                else:
                    variable_marginals1.append(0.1)

        #exceptionStatus = False

        #if check_marginal_sum == 0 and (synthesis_type == 'hhld'):
        #    exceptionStatus = True
        #if check_marginal_sum == 0 and (synthesis_type == 'person'):
        #    exceptionStatus = True

            

        #if check_marginal_sum == 0 and (synthesis_type == 'hhld' or synthesis_type == 'person'):
        #    print 'Exception: The given marginal distribution for a control variable sums to zero.'
            #raise Exception, 'The given marginal distribution for a control variable sums to zero.'
        control_marginals.append(variable_marginals1)
        #control_marginals_sum.append(check_marginal_sum)
   # if synthesis_type == 'hhld' or synthesis_type == 'person':
   #     for i in control_marginals_sum[0:]:
   #         if i <> control_marginals_sum[0]:
   #             print """Warning: The totals from the marginal distributions for the control variables are not the same. The program """
   #             """will proceed but the results will depend on the the last control variable's distribution. The last control variable """
   #             """is last variable obtained by alphabetically sorting the variable names.""" 
                #raise Exception, 'The marginal distributions for the control variables are not the same.'

    #if exceptionStatus:
    #    print 'Warning: The marginal distribution for the control variable sums to zero.'

    dbc.close()
    db.commit()
    print 'marginals used', control_marginals
    return control_marginals

def check_marginals(marginals, control_variables):
    check_for_zero_marginaltotals(marginals, control_variables)
    check_for_unequal_marginaltotals(marginals, control_variables)
    


def check_for_zero_marginaltotals(marginals, control_variables):
    for i in range(len(marginals)):
        j = marginals[i]
        try:
            while(1):
                j.remove(0.1)
        except:
            pass
        if sum(j) == 0:
            print ("Warning: The marginals distribution sum of the %s control variable is zero."
                   %control_variables[i])
            
def check_for_unequal_marginaltotals(marginals, control_variables):
    i = marginals[0]
    try:
        while(1):
            i.remove(0.1)
    except:
        pass
    ref_sum = sum(i)
    for i in range(len(marginals[1:])):
        j = marginals[1+i]
        try:
            while(1):
                j.remove(0.1)
        except:
            pass
        if ref_sum <> sum(j):
            print ("Warning: The marginals distribution sum of %s and %s variables are not the same."
                   %(control_variables[0], control_variables[1+i]))
                      
        
def check_for_zero_housing_totals(hhld_marginals, gq_marginals=None):
    checkHhld = 0
    checkGq = 0
    for i in hhld_marginals:
        try:
            while(1):
                i.remove(0.1)
        except:
            pass
        if len(i) <> 0:
            checkHhld = checkHhld + 1
    if not gq_marginals is None:
        for i in gq_marginals:
            try:
                while(1):
                    i.remove(0.1)
            except:
                pass
            if len(i) <> 0:
                checkGq = checkGq + 1

    if checkHhld == 0 and checkGq == 0:
        raise Exception, "There are no households/groupquarters in the geography to synthesize data"


def check_for_zero_person_totals(person_marginals):
    checkPers = 0
    for i in person_marginals:
        try:
            while(1):
                i.remove(0.1)
        except:
            pass
        if len(i) <> 0:
            checkPers = checkPers + 1
    if checkPers == 0:
        raise Exception, "There are no persons in the geography to synthesize data"




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
    puma_joint = arr(dbc.fetchall(), float)
    puma_prob = puma_joint[:,-2] / sum(puma_joint[:,-2])
    upper_prob_bound = 0.5 / sum(puma_joint[:,-2])

    dbc.execute('select * from %s order by %s' %(pums_table, dummy_order_string))
    pums_joint = arr(dbc.fetchall(), float)
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




