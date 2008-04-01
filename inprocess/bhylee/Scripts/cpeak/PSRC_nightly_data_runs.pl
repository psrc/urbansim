#!/usr/bin/perl -w
use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);


##########
#
#	This script archives the data quality indicator tables listed in the
#	@tables array and runs new data quality indicators.
#
##########

use strict;
use DBI;

my $server = 'trondheim.cs.washington.edu';
my $username = 'urbansim';
my $password = 'UwUrbAnsIm';

my $db = 'PSRC_2000_data_quality_indicators';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

####
# Get date information
my ($Seconds, $Minutes, $Hours, $DayInMonth, $Month, $ShortYear,
   $DayOfWeek, $DayOfYear, $IsDST);

($Seconds, $Minutes, $Hours, $DayInMonth, $Month, $ShortYear,
   $DayOfWeek, $DayOfYear, $IsDST) = localtime(time);

# Fix the year for post-Y2K
my $Year = $ShortYear + 1900;

# Fix the month and day for beginning count at 0
$Month = $Month + 1;
#$DayInMonth = $DayInMonth + 1;

# Specify input output (archive) databases
my $db_archive = "PSRC_2000_archived_dq_indicators";
my $db_current = "PSRC_2000_data_quality_indicators";

# Create list of tables to be backed up and dropped
my @tables_droppable = qw(
	census_block_imputed_unit_discrepancies
	census_block_assessors_unit_discrepancies
	land_use_summary_by_county
	land_use_summary_by_city
	land_use_summary_by_faz
	parcel_assessor_mfr_discrepancies_from_census
	parcel_assessor_sfr_discrepancies_from_census
	unit_land_use_consistency_check_overcount
	unit_land_use_consistency_check_undercount
	land_use_unit_tabulations_by_block
	land_use_unit_tabulations_by_block_group
	gridcell_res_unit_discrepancies_from_census
	parcel_imputed_mfr_unit_discrepancies_from_census
	parcel_imputed_sfr_unit_discrepancies_from_census
	sqft_per_unit_percentiles_by_city_and_land_use
	sqft_per_unit_percentiles_by_county_and_land_use
	sqft_per_parcel_percentiles_by_city_and_land_use
	sqft_per_parcel_percentiles_by_county_and_land_use
	improvement_value_per_sqft_percentiles_by_county_and_land_use
	improvement_value_per_sqft_percentiles_by_city_and_land_use
	placed_employer_summaries_by_decision
	placed_employer_summaries_by_land_use
	sqft_per_job_percentiles_by_county
	land_value_per_acre_percentiles_by_county_and_land_use
	parcels_missing_employment
	building_parcel_sqft_total_comparisons
	average_land_value_per_are_by_land_use
	land_value_per_acre_percentiles_by_te_status_and_land_use
	parcel_counts_units_sqft_by_region_by_year_built
	parcel_counts_units_sqft_by_county_by_year_built
	parcel_counts_units_sqft_by_city_by_year_built
	lot_sqft_per_housing_units_by_region_by_residential_land_use
	lot_sqft_per_housing_units_by_county_by_residential_land_use
	lot_sqft_per_housing_units_by_city_by_residential_land_use
	floor_area_ratio_by_region_by_non_residential_land_use
	floor_area_ratio_by_county_by_non_residential_land_use
	floor_area_ratio_by_city_by_non_residential_land_use
	land_value_per_acre_by_region_by_te_status
	land_value_per_acre_by_county_by_te_status
	land_value_per_acre_by_city_by_te_status
	built_sqft_per_parcel_percentiles_by_region_by_land_use
	built_sqft_per_parcel_percentiles_by_county_by_land_use
	built_sqft_per_parcel_percentiles_by_city_by_land_use
	floor_area_ratio_percentiles_by_region_by_land_use
	floor_area_ratio_percentiles_by_county_by_land_use
	floor_area_ratio_percentiles_by_city_by_land_use
	improvement_value_per_sqft_percentiles_by_region_by_land_use
	improvement_value_per_sqft_percentiles_by_county_by_land_use
	improvement_value_per_sqft_percentiles_by_city_by_land_use
	land_value_per_acre_percentiles_by_region_by_land_use
	land_value_per_acre_percentiles_by_county_by_land_use
	land_value_per_acre_percentiles_by_city_by_land_use
	lot_sqft_per_housing_unit_percentiles_by_region_by_land_use
	lot_sqft_per_housing_unit_percentiles_by_county_by_land_use
	lot_sqft_per_housing_unit_percentiles_by_city_by_land_use
	built_sqft_per_housing_unit_percentiles_by_region_by_land_use
	built_sqft_per_housing_unit_percentiles_by_county_by_land_use
	built_sqft_per_housing_unit_percentiles_by_city_by_land_use

);

#Navigate to the archive database
my $qry_use = "use $db_archive";
my $sth_use = $dbh->prepare($qry_use);
$sth_use->execute();

my $t;
my $qry_backup;
my $qry_drop;

# Run queries on each table in @tables_droppable
foreach $t (@tables_droppable) {

	print "Archiving table $t \n";
	# Create a backup version of $t in the archive database
	$qry_backup = "CREATE TABLE $db_archive.${Month}_${DayInMonth}_${t} ";
	$qry_backup .= "SELECT * from $db_current.$t";
	#print "$qry_backup \n";
	my $sth_backup = $dbh->prepare($qry_backup);
	$sth_backup->execute();

	# Delete $t from the current database
	$qry_drop = "DROP TABLE $db_current.$t";
	#print "$qry_drop \n";
	my $sth_drop = $dbh->prepare($qry_drop);
	$sth_drop->execute();
}

# Create list of tables to be backed up and emptied
my @tables_emptyable = qw(
	indicators_runs
	summary_indicators_city_level
	);

my $qry_empty;

# Run queries on each table in @tables_emptyable
foreach $t (@tables_emptyable) {

	print "Archiving table $t \n";
	# Create a backup version of $t in the archive database
	$qry_backup = "CREATE TABLE $db_archive.${t}_${Month}_${DayInMonth}_${Year}_${Hours}_${Minutes} ";
	$qry_backup .= "SELECT * from $db_current.$t";
	#print "$qry_backup \n";
	my $sth_backup = $dbh->prepare($qry_backup);
	$sth_backup->execute();

	# Delete $t from the current database
	$qry_empty = "DELETE FROM $db_current.$t";
	#print "$qry_empty \n";
	my $sth_empty = $dbh->prepare($qry_empty);
	$sth_empty->execute();
}

$dbh->disconnect;

# recombine parcel tables, regenertae gridcell table, and rerun dq indicators
my $system_statement = "mysql -h trondheim -u urbansim -f --password=UwUrbAnsIm ";
$system_statement .="< /projects/urbansim7/scripts/public/data_prep/PSRC_nightly_data_update.sql";
system($system_statement);

# export and commit new dq indicators to the web
my $system_statement_2 = "perl -w /projects/urbansim7/scripts/private/cpeak/PSRC_export_dq_indicators.pl";
system($system_statement_2);

