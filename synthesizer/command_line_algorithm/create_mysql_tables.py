# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import MySQLdb

def create_tables(db, project_name, path):

	dbc = db.cursor()
	print ('Create Database %s' %(project_name))
	dbc.execute('Create Database %s' %(project_name))
	dbc.close()

	db = MySQLdb.connect(user = 'root', passwd = '1234', db = '%s'%(project_name))
	dbc = db.cursor()

	dbc.execute('''Create Table housing_pums ( pumano int, hhpumsid int,
                                                   hhid int, hhtype int,
        					   childpresence int, hhldtype int,
						   hhldsize int, hhldinc int,
                                      		   groupquarter int )''')
	dbc.execute('''load data local infile '%s/housing_pums.dat' into table housing_pums'''%(path))

	dbc.execute('''Create Table person_pums ( pumano int, hhpumsid int,
								  hhid int, personid int,
								  gender int, age int,
								  race int, employment int )''')
	dbc.execute('''load data local infile '%s/person_pums.dat' into table person_pums''' %(path))

	dbc.execute('''Create Table housing_marginals ( county int, pumano int,
								         tract int, bg int,
								         hhtotal int, childpresence1 int,
								         childpresence2 int, hhldtype1 int,
								         hhldtype2 int, hhldtype3 int,
								         hhldtype4 int, hhldtype5 int,
								         hhldsize1 int, hhldsize2 int,
								         hhldsize3 int, hhldsize4 int,
								         hhldsize5 int, hhldsize6 int,
								         hhldsize7 int, hhldinc1 int,
								         hhldinc2 int, hhldinc3 int,
								         hhldinc4 int, hhldinc5 int,
								         hhldinc6 int, hhldinc7 int,
								         hhldinc8 int, groupquarter1 int,
								         groupquarter2 int )''')
	dbc.execute('''load data local infile '%s/housing_marginals.dat' into table housing_marginals'''%(path))

	dbc.execute('''Create Table person_marginals ( county int, pumano int,
								        tract int, bg int,
								        gender1 int, gender2 int,
								        age1 int, age2 int,
								        age3 int, age4 int,
								        age5 int, age6 int,
								        age7 int, age8 int,
								        age9 int, age10 int,
								        race1 int, race2 int,
								        race3 int, race4 int,
								        race5 int, race6 int,
								        race7 int, employment1 int,
								        employment2 int, employment3 int,
								        employment4 int )''')
	dbc.execute('''load data local infile '%s/person_marginals.dat' into table person_marginals'''%(path))
# Figure out a way to automate this process based on the number of hhtypes and the independent tables must only contain variables corresponding
# to the particular housing type
	hhld_variables = 'childpresence, hhldtype, hhldsize, hhldinc'
	gq_variables = 'groupquarter'
	dbc.execute('''create table hhld_pums select pumano, hhpumsid, hhid, %s from housing_pums where hhtype = 1'''%(hhld_variables))
	dbc.execute('''create table gq_pums select pumano, hhpumsid, hhid, %s from housing_pums where hhtype = 2'''%(gq_variables))
	dbc.close()
	db.commit()
	db.close()

if __name__ == '__main__':
	db = MySQLdb.connect(user = 'root', passwd = '1234')
# How to pickup the location of the flat-files, this can probably come from the GUI?
	path = 'c:/populationsynthesis/command_line_algorithm/northcarolina/data'
	create_tables (db, 'northcarolina', path)
	db.close()
