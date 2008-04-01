#
#  UrbanSim software.
#  Copyright (C) 1998-2003 University of Washington
#
#  You can redistribute this program and/or modify it under the
#  terms of the GNU General Public License as published by the
#  Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  file LICENSE.htm for copyright and licensing information, and the
#  file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
#
#  Author: Chris Peak


# This script selects, for each parcel with NULL year_built, the year_built
#	of a randomly-selected parcel within X feet.  This distance X
#	is input by the user at runtime.
#
# INPUT:
#  One parcel table, the name of which will be requested by the program.
#		Required fields: PARCEL_ID, X_COORD, Y_COORD, YEAR_BUILT, IMPUTE_FLAG.
#		Note: X_COORD and Y_COORD must be non-null.
# OUTPUT:
# 	Writes to the input file, changing YEAR_BUILT to a value selected at random
#	    from parcels a given distance ($neighborhood_distance) away.


#!/usr/bin/perl -w
use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);

# use strict;
use DBI;
srand( time() ^ ($$ + ($$ << 15)) );
#srand(0);

my $server = 'trondheim.cs.washington.edu';
my $username = 'urbansim';
my $password = 'UrbAnsIm4Us';


 print "What neighborhood distance do you want to use? ";
 chomp(my $neighborhood_distance = <STDIN>);
#my $neighborhood_distance = 500;

 print "What database to you want to use? ";
 my $db = <STDIN>;
 chomp $db;
# my $db = "year_built_imputation_cpeak";

 print "What table do you want to process?";
 chomp(my $parceltable = <STDIN>);
#my $parceltable = "parcels_king_xy";


my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);


########
# Divide parcel file in two
my $nullstable = $parceltable ."_nulls";
print "Creating $nullstable. \n";
my $qry_make_nullstable = "CREATE TABLE $nullstable";
$qry_make_nullstable .= " SELECT PARCEL_ID, X_COORD, Y_COORD, YEAR_BUILT FROM $parceltable WHERE $parceltable";
$qry_make_nullstable .= ".YEAR_BUILT IS NULL";
#print "$qry_make_nullstable \n";
my $sth_nake_nullstable = $dbh->prepare($qry_make_nullstable);
$sth_nake_nullstable->execute();


my $valstable = $parceltable ."_vals";
print "Creating $valstable. \n";
my $qry_make_valstable = "CREATE TABLE $valstable";
$qry_make_valstable .= " SELECT PARCEL_ID, X_COORD, Y_COORD, YEAR_BUILT FROM $parceltable WHERE $parceltable";
$qry_make_valstable .= ".YEAR_BUILT IS NOT NULL AND IMPUTE_FLAG IS NULL";
#print $qry_make_valstable, "\n";
my $sth_make_valstable = $dbh->prepare($qry_make_valstable);
$sth_make_valstable->execute();


####### Create indexes for x, y columns in $valstable
print "Creating index on X,Y coordinates in $valstable. \n";
my $qry_coord_ind = "ALTER TABLE $valstable ADD INDEX coord_ind (X_COORD, Y_COORD)";
my $sth_coord_ind = $dbh->prepare($qry_coord_ind);
$sth_coord_ind->execute();


########
# Get min and max x and y for the parcels without YEAR_BUILT
print "Adding minimum and maximum X and Y coordinates to $nullstable. \n";

# add new columns to hold the new ranges.
my $qry_minx_add = "ALTER TABLE $nullstable ADD COLUMN MIN_X double";
my $qry_maxx_add = "ALTER TABLE $nullstable ADD COLUMN MAX_X double";
my $qry_miny_add = "ALTER TABLE $nullstable ADD COLUMN MIN_Y double";
my $qry_maxy_add = "ALTER TABLE $nullstable ADD COLUMN MAX_Y double";
my $minx_sth = $dbh->prepare($qry_minx_add);
my $maxx_sth = $dbh->prepare($qry_maxx_add);
my $miny_sth = $dbh->prepare($qry_miny_add);
my $maxy_sth = $dbh->prepare($qry_maxy_add);
$minx_sth->execute();
$maxx_sth->execute();
$miny_sth->execute();
$maxy_sth->execute();

# populate the new columns with values.
my $qry_updt_minx = "UPDATE $nullstable SET MIN_X = X_COORD - $neighborhood_distance";
my $qry_updt_maxx = "UPDATE $nullstable SET MAX_X = X_COORD + $neighborhood_distance";
my $qry_updt_miny = "UPDATE $nullstable SET MIN_Y = Y_COORD - $neighborhood_distance";
my $qry_updt_maxy = "UPDATE $nullstable SET MAX_Y = Y_COORD + $neighborhood_distance";
my $updt_minx_sth = $dbh->prepare($qry_updt_minx);
my $updt_maxx_sth = $dbh->prepare($qry_updt_maxx);
my $updt_miny_sth = $dbh->prepare($qry_updt_miny);
my $updt_maxy_sth = $dbh->prepare($qry_updt_maxy);
$updt_minx_sth->execute();
$updt_maxx_sth->execute();
$updt_miny_sth->execute();
$updt_maxy_sth->execute();


########
## For each parcel P in $nullstable, get the set of parcels in $valstable that lie within P's neighborhood.
##  Then impute P's YEAR_BUILT by randomly selecting one of the year_builts from the selected records from $valstable.

my $qry_select1 = "SELECT PARCEL_ID, MIN_X, MAX_X, MIN_Y, MAX_Y FROM $nullstable";
my $select_sth1 = $dbh->prepare($qry_select1);
$select_sth1->execute();
my $process_counter = 1;
while (my $nullrow = $select_sth1->fetchrow_arrayref) {
	print "$process_counter parcels processed. \n";
	my $null_pin = @$nullrow[0];
	my $nbr_min_x = @$nullrow[1];
	my $nbr_max_x = @$nullrow[2];
	my $nbr_min_y = @$nullrow[3];
	my $nbr_max_y = @$nullrow[4];
	my $qry_neighbors = "SELECT PARCEL_ID, YEAR_BUILT FROM $valstable WHERE X_COORD >= $nbr_min_x";
	$qry_neighbors .= " AND X_COORD <= $nbr_max_x AND Y_COORD >= $nbr_min_y AND Y_COORD <= $nbr_max_y";
	my $sth_neighbors = $dbh->prepare($qry_neighbors);
	$sth_neighbors->execute();
	####### import the neihborhood parcels and their YEAR_BUILTs into two arrays @nbr_pin and @nbr_year_built
	while (my $neighbor = $sth_neighbors->fetchrow_arrayref) {
		#push (@nbr_pin, @$neighbor[0]);
		push (@nbr_year_built, @$neighbor[1]);
		#print @$neighbor[1], "\n";
	}

	####### print a summary of the year_builts within the neighborhood.
	#my $qry_summary = "SELECT COUNT(*) AS CNT, YEAR_BUILT FROM $valstable WHERE X_COORD >= $nbr_min_x";
	#$qry_summary .= " AND X_COORD <= $nbr_max_x AND Y_COORD >= $nbr_min_y AND Y_COORD <= $nbr_max_y";
	#$qry_summary .= " GROUP BY YEAR_BUILT";
	#my $sth_summary = $dbh->prepare($qry_summary);
	#$sth_summary->execute();
	#while (my $summary_rec = $sth_summary->fetchrow_arrayref) {
	#	print join("\t", @$summary_rec), "\n";
	#}
	####### end summary


	my $max_nbr_ref = $#nbr_year_built + 1; #the number of parcels in $null_pin's neighborhood.
	####### If there are any parcels in the neighborhood of parcel $null_pin,
	#######  draw a random integer $selected_nbr_index between 0 and the highest index in @nbr_year_built, and use this
	#######  as the index by which to select year_built from the neighborhing parcels.
	if ($max_nbr_ref == 0) {
		print "There are no neighboring parcels for PARCEL_ID $null_pin. \n";
		print "YEAR_BUILT for PARCEL_ID $null_pin not changed. \n";
	} else {
		my $selected_nbr_index = int(rand $max_nbr_ref); # Get a random # between 0 and the # of neighboring parcels
		my $imputed_year_built = $nbr_year_built[$selected_nbr_index];
		# print $nbr_pin[$selected_nbr_index], "\t $nbr_year_built[$selected_nbr_index] \t $selected_nbr_index \n";
		####### Slect $nbr_year_built[rndm] as the land use to ascribe to $nullparcel.
		my $qry_impute = "UPDATE $parceltable SET YEAR_BUILT = \"$imputed_year_built\" WHERE PARCEL_ID = \"$null_pin\" ";
		#print $qry_impute, "\n";
		print "Imputing YEAR_BUILT for PARCEL_ID $null_pin to \"$imputed_year_built\".\n";
		my $sth_impute = $dbh->prepare($qry_impute);
		#######
		$sth_impute->execute();
		my $qry_set_flag = "UPDATE $parceltable SET IMPUTE_FLAG = 1 WHERE PARCEL_ID = \"$null_pin\" ";
		my $sth_set_flag = $dbh->prepare($qry_set_flag);
		$sth_set_flag->execute();
	}
	@nbr_year_built = ();  #Clear the list of possible year_builts.
	$process_counter = $process_counter +1;
}

#### Delete $nullstable and $valstable
my $qry_drop_nullstable = "DROP TABLE $nullstable";
my $qry_drop_valstable = "DROP TABLE $valstable";
my $sth_drop_nullstable = $dbh->prepare($qry_drop_nullstable);
my $sth_drop_valstable = $dbh->prepare($qry_drop_valstable);
$sth_drop_nullstable ->execute();
$sth_drop_valstable ->execute();


#### This block changes parcel 99999999999 and 8808958888 back to null, for repeated running of the script.  for testing purposes only.
my $qry_rectify = "UPDATE $parceltable SET YEAR_BUILT = NULL WHERE PARCEL_ID = \"9999999999\"";
$qry_rectify .= " OR PARCEL_ID = \"8808958888\"";
#print $qry_rectify, "\n";
my $sth_rectify = $dbh->prepare($qry_rectify);
#$sth_rectify->execute();

$dbh->disconnect;
$dbh->disconnect;
