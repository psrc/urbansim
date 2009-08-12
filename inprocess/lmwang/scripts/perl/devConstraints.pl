##This script is used to diagnose grid cell development constraints from tables: 
##gridcells, development_constraints, transition_types and urbansim_constants in base year database
#Created by Liming Wang on 06/03
#last updated on 06/11/03

#!/usr/local/bin/perl -w

use lib "/homes/june/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

my $DEBUG=0;  # define DEBUG flag

my $mysql_host='trondheim.cs.washington.edu';
my $mysql_output_db='WFRC_1997_baseyear_lmwang'; 
my $mysql_user='urbansim';
my $mysql_passwd='UwUrbAnsIm';


my $table_gridcells ='gridcells';
my $table_constraints ='development_constraints';
my $table_transition_types ='transition_types';
my $table_urbansim_constants='urbansim_constants';
my $table_gridcells_dev_constraints = 'tmp_gridcells_dev_constraints';  # output table

#define the constraints fields
my @constraints =qw(city_id county_id percent_floodplain percent_stream_buffer percent_wetland percent_slope is_outside_urban_growth_boundary plan_type_id);
my @constraints_d =qw(city_id county_id is_in_floodplain is_in_stream_buffer is_in_wetland is_on_steep_slope is_outside_urban_growth_boundary plantype_x);

#define the output table fields
my @max_value_fields =qw(housing_units_mean commercial_sqft_mean industrial_sqft_mean governmental_sqft_mean);

my @devtype_x;
for (my $x = 1; $x <= 23; $x++) {
      push(@devtype_x,'DEVTYPE_' . $x);
}

my $stm_create ='CREATE TABLE ' . $table_gridcells_dev_constraints;
$stm_create = $stm_create . "(GRID_ID INT(11),DEVELOPMENT_TYPE_ID INT(11), PLAN_TYPE_ID INT(11),";
my $field_count = 3;  #count the number of fields other than devtype and max value fields.

foreach $devtype (@devtype_x) {
	$stm_create =$stm_create . "\U$devtype int(2),";
}

foreach $max_value_fields (@max_value_fields) {
	$stm_create =$stm_create . "MAX_\U$max_value_fields double,";
}

chop($stm_create);  #chop the last ","
$stm_create =$stm_create . ")";

if ($DEBUG) {print "$stm_create\n";}

my $data_source="DBI:mysql:database=" . $mysql_output_db . ":host=" . $mysql_host;
my $dbh=DBI->connect($data_source,$mysql_user,$mysql_passwd) 
	or die "failed to open database connection" . DBI->errstr;

#get the PERCENT_CONVERAGE_THRESHOLD
$sth_threshold=$dbh->prepare("SELECT PERCENT_COVERAGE_THRESHOLD FROM $table_urbansim_constants") 
	or die "failed to prepare statement.\n";
$sth_threshold->execute() 
	or die "couldn't execute statement: " . $sth_gridcell->errstr;
$select_threshold=$sth_threshold->fetchrow(); 

$sth_threshold->finish;

if ($DEBUG) {print "$select_threshold\n";}

my $rv=$dbh->do("DROP TABLE IF EXISTS $table_gridcells_dev_constraints") or die "failed to drop old output table: " . DBI->errstr;
$rv=$dbh->do($stm_create) or die "failed to create table: " . DBI->errstr;

##select constraint fields for each gridcell
$stm_gridcell ="SELECT GRID_ID,DEVELOPMENT_TYPE_ID,PLAN_TYPE_ID,";
foreach $constraints (@constraints) {
	$stm_gridcell =$stm_gridcell . "\U$constraints,";
}
chop($stm_gridcell);  #chop the last ","
$stm_gridcell =$stm_gridcell . " FROM " . $table_gridcells;

if($DEBUG){print "$stm_gridcell\n";}

$sth_gridcell=$dbh->prepare($stm_gridcell) 
	or die "failed to prepare statement.\n";
$sth_gridcell->execute() 
	or die "couldn't execute statement: " . $sth_gridcell->errstr;

while (@select_gridcell=$sth_gridcell->fetchrow()) {
#@select_gridcell=$sth_gridcell->fetchrow(); { #for debug, run only 1 record.
	if($DEBUG) {
		for($i=0;$i<=scalar(@constraints)+1;$i++){   #0 - grid_id, 1 - development_type_id
			print "$select_gridcell[$i]\t";
		}
		print "\n";
	} 
	
	$stm_constraints ="SELECT DISTINCT DEVTYPE_X, CONSTRAINT_ID  FROM " . $table_constraints . " WHERE ";
	$j=$field_count; #constraint fields begins after GRID_ID and DEVELOPMENT_TYPE_ID
	foreach $constraints (@constraints) {
		# if percent constraints <= percent coverage threshold, then is_in constraints = 0 else =1
		if (substr("\L$constraints",0,7) eq 'percent') {
			if ($select_gridcell[$j]<=$select_threshold) {
				$stm_constraints = $stm_constraints . "($constraints_d[$j-$field_count] =0 OR $constraints_d[$j-$field_count] =-1 ) AND ";
			} else {
				$stm_constraints = $stm_constraints . "($constraints_d[$j-$field_count] =1 OR $constraints_d[$j-$field_count] =-1 ) AND ";
			}
		} else {
			if ("\L$constraints" eq 'plan_type_id') {
				$stm_constraints = $stm_constraints . "($constraints_d[$j-$field_count] = $select_gridcell[$j] OR $constraints_d[$j-$field_count] =-1 ) AND ";
			} else {
				$stm_constraints = $stm_constraints . "($constraints = $select_gridcell[$j] OR  $constraints =-1 ) AND ";
			}
		}
		$j++;

	}
	chop($stm_constraints);chop($stm_constraints);chop($stm_constraints);chop($stm_constraints); #chop the last 'AND'
	if($DEBUG){print "$stm_constraints\n";} 
	if($DEBUG){print "@constraints_d\t";} 
	if($DEBUG){print "\n"; print "@select_gridcell\t";}
	if($DEBUG){print "\n";}
	
	$sth_constraints=$dbh->prepare($stm_constraints) 
		or die "failed to prepare statement.\n";

	$sth_constraints->execute() 
		or die "couldn't execute statement: " . $sth_constraints;
	##there should be a better way to specify this two arrays.
	my @max_values;
	for ($i=0;$i<scalar(@max_value_fields);$i++) {
		$max_values[$i] =0;
	}

	my @devtype_value;	
	for ($i=0;$i<scalar(@devtype_x);$i++) {
		$devtype_value[$i] =1;  #initially every devtype is allowed to build
	}
	
	while (@select_constraints=$sth_constraints->fetchrow()) {
		#delete the possible newline or white space
		chomp($select_constraints[0]);
		$select_constraints[0]=~ s/^\s+//;
		$select_constraints[0]=~ s/\s+$//;
		if ($DEBUG) {print "CONSTRAINT_ID: $select_constraints[1]  DEVETYPE_X: $select_constraints[0]\n";} 

		my @x; # store the split devtype
		if ($select_constraints[0] eq 'ALL') {
			for ($i=1; $i<=23; $i++) {
				push(@x, $i);
			}
		} else { 
			@x =split(/,/, $select_constraints[0]);
		}
		
		foreach $x (@x) {
			if ($x <= 23) {
				$devtype_value[$x-1] =0; 
				if ($DEBUG) {print "devtype_$x : $devtype_value[$x-1] \n";} 
			}
		}
	}

	for ($a=1;$a<=23;$a++) {
		if ($devtype_value[$a-1]==1) {

			$stm_max_value_fields ="SELECT "; 
			foreach $max_value_fields (@max_value_fields) { 
				$stm_max_value_fields = $stm_max_value_fields . $max_value_fields . ","
			}
			chop($stm_max_value_fields);
			$stm_max_value_fields =$stm_max_value_fields . " FROM " . $table_transition_types;
			$stm_max_value_fields =$stm_max_value_fields . " WHERE ";
			$stm_max_value_fields =$stm_max_value_fields . "STARTING_DEVELOPMENT_TYPE_ID =";
			$stm_max_value_fields =$stm_max_value_fields . " $select_gridcell[1]  AND ";
			$stm_max_value_fields =$stm_max_value_fields . "ENDING_DEVELOPMENT_TYPE_ID =";
			$stm_max_value_fields =$stm_max_value_fields . " $a";

			if ($DEBUG) {print "stm_max_value_fields: $stm_max_value_fields\n";}
		
			$sth_max_value_fields=$dbh->prepare($stm_max_value_fields) 
				or die "failed to prepare statement.\n";
			$sth_max_value_fields->execute() 
				or die "couldn't execute statement: " . $sth_max_value_fields; 
			while (@select_max_value_fields=$sth_max_value_fields->fetchrow()) { 
				if($DEBUG) { 
					for($i=0;$i<scalar(@max_value_fields);$i++){   
						print "$max_value_fields[$i]: $select_max_value_fields[$i]\n";
					
					}
				} 

				for ($j=0;$j<scalar(@max_value_fields);$j++) {
					if ($select_max_value_fields[$j] > $max_values[$j]) {
						$max_values[$j] = $select_max_value_fields[$j];
					}
				}
			}
		}
	}

	#insert values for this grid cell into output table 
	$stm_result = "INSERT INTO $table_gridcells_dev_constraints (GRID_ID,DEVELOPMENT_TYPE_ID,PLAN_TYPE_ID,"; 
	
	foreach $devtype (@devtype_x) { 
		$stm_result =$stm_result . $devtype . ","; 
	} 
	foreach $max_value_fields (@max_value_fields) { 
		$stm_result =$stm_result . "MAX_\U$max_value_fields,"; 
	} 
	
	chop($stm_result);  #chop the last ","
	$stm_result =$stm_result . ") VALUES (";
	$stm_result =$stm_result . "$select_gridcell[0],$select_gridcell[1],$select_gridcell[2],";
	
	foreach $devtype_value (@devtype_value) { 
		$stm_result =$stm_result . $devtype_value . ","; 
	} 
	foreach $max_values (@max_values) { 
		$stm_result =$stm_result . $max_values . ","; 
	} 
	
	chop($stm_result);  #chop the last ","

	$stm_result =$stm_result . ")";
	
	if ($DEBUG) {print "$stm_result\n";}
	
	$rv=$dbh->do($stm_result) 
		or die "failed to insert results";
}

$sth_gridcell->finish;
$sth_constraints->finish;
#$sth_max_value_fields->finish;

$dbh->disconnect();

exit 0;

