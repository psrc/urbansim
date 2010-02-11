# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import MySQLdb
import numpy


def display_results(db, pumano, tract, bg):
    print '------------------------------------------------------------------'
    print 'Geography: PUMA ID- %s, Tract ID- %0.2f, BG ID- %s' \
                                                                         %(pumano, float(tract)/100, bg)
    print '------------------------------------------------------------------'

    dbc = db.cursor()
    hh_variables = ['childpresence', 'hhldtype', 'hhldsize', 'hhldinc', 'groupquarter']
    hh_dimensions = [2, 5, 7, 8, 2]
    person_variables = ['gender', 'age', 'race', 'employment']
    person_dimensions = [2, 10, 7, 4]
    for i in range(len(hh_variables)):
        print hh_variables[i]
        est_list = []
        dbc.execute('''select %s, sum(frequency) from housing_synthetic_data
                            where pumano = %s and tract = %s and bg = %s group
                            by %s''' %(hh_variables[i], pumano, tract, bg,
                            hh_variables[i]))
        result = numpy.asarray(dbc.fetchall())

        for k in range(result.shape[0]):
            if result[k,1] <>0 and result[k,0] <>-99:
                 est_list.append(int(result[k,1]))
        print 'Estimated -- ',est_list

        obj_list = []
        for j in range(hh_dimensions[i]):
            dbc.execute('''select %s%s from housing_marginals where pumano = %s and
                       tract = %s and bg = %s'''%(hh_variables[i], j+1, pumano, tract,
                       bg))
            result = numpy.asarray(dbc.fetchall())
            if result[0][0] <> 0:
                obj_list.append(result[0][0])
        print 'Objective -- ',obj_list

    for i in range(len(person_variables)):
        print person_variables[i]
        est_list = []
        dbc.execute('''select %s, sum(frequency) from person_synthetic_data
                            where pumano = %s and tract = %s and bg = %s group
                            by %s''' %(person_variables[i], pumano, tract, bg,
                            person_variables[i]))
        result = numpy.asarray(dbc.fetchall())
        for k in range(result.shape[0]):
            if result[k,1] <>0 and result[k,0] <>-99:
                 est_list.append(int(result[k,1]))
        print 'Estimated -- ',est_list

        obj_list = []
        for j in range(person_dimensions[i]):
            dbc.execute('''select %s%s from person_marginals where pumano = %s
                               and tract = %s and bg = %s'''%(person_variables[i],
                               j+1, pumano, tract, bg))
            result = numpy.asarray(dbc.fetchall())
            if result[0][0] <> 0:
                obj_list.append(result[0][0])
        print 'Objective -- ',obj_list
    dbc.close()


if __name__ == '__main__':


    db = MySQLdb.connect(user = 'root', passwd = '1234', db = 'ncpopsyn')
    dbc = db.cursor()

    display_results(db, 2702, 52900, 4)
    dbc.close()
