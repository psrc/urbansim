#!/usr/bin/perl -w
use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);


########
# This script creates csv and html versions of the tables listed in the @tables array.
##########

use strict;
use DBI;

my $server = 'trondheim.cs.washington.edu';
my $username = 'urbansim';
my $password = 'UwUrbAnsIm';

my $db = 'PSRC_2000_data_quality_indicators';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

# Set local path to check out to, work in, and commit from
my $working_path = "/projects/urbansim7/cpeak/DataQuality/exported_indicators";
# Set repository root
my $repository_root = "/projects/urbansim2/repository";
# Set repository path
my $repository_path = "Website/projects/psrc/indicator_results";

# Create list of tables to be exported
my @tables = qw(
	indicators_runs
	summary_indicators_city_level
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
	building_parcel_sqft_summary_comparison
	parcels_missing_employment
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
	faz_summaries
	faz_hhld_summaries
	faz_job_summaries
);

# Check out indicator results from cvs
#system "cd $working_path";
system "cvs -d $repository_root checkout -d $working_path $repository_path";

#Navigate to the database
my $qry_use = "use $db";
my $sth_use = $dbh->prepare($qry_use);
$sth_use->execute();

my $table;
my $qry_records;

# Run queries on each table in @tables
foreach $table (@tables) {

	print "Processing table: $table \n";

	##### Prepare the field headers for the output table

	# Prep csv file to receive the headers
	my $file_csv = "${working_path}/${table}.csv";
	open OUTTABLE_CSV, "> $file_csv";

	# Prep html file to receive the headers
	my $file_html = "${working_path}/${table}.html";
	open OUTTABLE_HTML, "> $file_html";

	# Prepare and execute describe query
	my $qry_describe = "DESCRIBE $table";
	my $sth_describe = $dbh->prepare($qry_describe);
	$sth_describe->execute();

	# Write the field names to the output files
	print OUTTABLE_HTML "<TABLE BORDER = \'1\'><TBODY><TR>";
	while (my @field_name = $sth_describe->fetchrow_array){
		my $field = "$field_name[0]";
		#print "$field \n";
		print OUTTABLE_CSV "$field_name[0]",',';
		print OUTTABLE_HTML "<TD>$field_name[0]</TD>";
	}
	print OUTTABLE_CSV "\n";
	print OUTTABLE_HTML "</TR>\n";


	##### Prepare the output files to receive data

	# Prepare and execute the select query
	$qry_records = "SELECT * FROM $db.$table";
	my $sth_records = $dbh->prepare($qry_records);
	$sth_records->execute();

	# Write the contents of the table to the output file
	while (my @record = $sth_records->fetchrow_array){
		foreach my $item (@record){		#change null fields to '0'
			if (! defined($item)){
				$item = "NULL";
			}
		}
		my $line = join (",",@record);
		#print "$line \n";
		print OUTTABLE_CSV "$line \n";               # write data to OUTTABLE
		print OUTTABLE_HTML "<TR>";
		foreach my $rec (@record){
			print OUTTABLE_HTML "<TD>$rec</TD>";
		}
		print OUTTABLE_HTML "</TR>\n";
	}
	print OUTTABLE_HTML "</TBODY></TABLE>";
	close OUTTABLE_CSV;
	close OUTTABLE_HTML;
}

$dbh->disconnect;

# Commit changes to website section of cvs

system "cvs -d $repository_root commit -m '(cpeak) latest indicators' $working_path";