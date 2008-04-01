use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);
use strict;
use DBI;
#srand( time() ^ ($$ + ($$ << 15)) );
srand(0);


# This does not yet distinguish between proprietors and leftovers from the job allocator
#  In the future, we should place different proportions of county jobs on res parcels,
#  depending on whether they are proprietors or job allocator leftovers.

#INPUT TABLES AND FIELDS:
# JOB_PROPORTIONS_BY_SECTOR
#	COUNTY
#	SECTOR
#	PROPORTION_OF_JOBS_HOMEBASED (SUM OF PROPORTION_OF_COUNTY_JOBS_HOMEBASED AND PROPORTION_OF_COUNTY_JOBS_NONHOMEBASED SHOULD = 1)
#	PROPORTION_OF_JOBS_NONHOMEBASED
# JOBS_PER_COUNTY
#	COUNTY
#	SECTOR
#	TOTAL_COUNTY_JOBS (the sum of proprietors AND leftovers from the job allocator)
# ZONE_WEIGHTS  (possibly calculated proportion of placed jobs from the job allocator in a given zone)
#	COUNTY
#	ZONE
#	ZONE_WEIGHT_HOMEBASED
#	ZONE_WEIGHT_NONHOMEBASED
# PARCELS
#	COUNTY
#	ZONE
#	FAZ_GROUP
#	LAND_USE
#	PARCEL_ID
#	JOB_COUNT
#	SQFT
#	GENERIC_LAND_USE_1
#	GENERIC_LAND_USE_2
# SECTOR_LAND_USE_WEIGHTS
# 	FAZ_GROUP
#   SECTOR
#	LAND_USE
#	SEC_LU_WEIGHT
#
#OUTPUT TABLE:
# JOBS_ROUNDED


#my $server = 'trondheim.cs.washington.edu';
my $server = 'localhost';
my $username = 'urbansim';
my $password = 'UrbAnsIm4Us';

print "Input database: ";
my $db = <STDIN>;
chomp $db;
#my $db = 'PSRC_proprietors_distributor_king'; #Real run for King County
#my $db = 'PSRC_proprietors_distributor_test_1'; # basic test database
#my $db = 'PSRC_proprietors_distributor_test_2';#'PSRC_proprietors_distributor_king';
print "test 1 \n";
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

#my $max_res_parcels_in_county = &get_max_res_parcels_in_county;
#my $max_nonres_parcels_in_county = &get_max_nonres_parcels_in_county;

my $jobs_placed = 0;
#-----------------main routine------------------------
# Run SQL queries to generate JOBS_PER_ZONE tables
#my $SQL_system_statement_1 = "mysql -u urbansim -f --password=UrbAnsIm4Us $db < /projects/urbansim7/scripts/private/cpeak/proprietors_distributor/get_jobs_per_zone.sql";
#system($SQL_system_statement_1);
#print "jobs placed: \n";
# Distribute homebased jobs in each zone across all parcels in that zone

# Get all sector/zones and their homebased job totals
my $qry_get_zone = "SELECT COUNTY, SECTOR, ZONE, HOMEBASED_JOBS FROM HOMEBASED_JOBS_PER_ZONE";
my $sth_get_zone = $dbh->prepare($qry_get_zone);
$sth_get_zone->execute();
# Iterate over each sector-zone combo for homebased jobs
while (my $sector_maz = $sth_get_zone->fetchrow_arrayref) {
	my ($county, $sector, $zone, $homebased_jobs) = (@$sector_maz[0], @$sector_maz[1], @$sector_maz[2], @$sector_maz[3]);
	print "COUNTY: $county, Sector: $sector, ZONE: $zone, Jobs: $homebased_jobs, Homebased: 1 \n";
	&distribute_to_parcels_main($homebased_jobs, $county, $zone, $sector, 1);# do the work for that sector-zone
}

# do nonhomebased_jobs
# Get all sector/mazs and their nonhomebased job totals
my $qry_get_maz_nonhome = "SELECT COUNTY, SECTOR, ZONE, NONHOMEBASED_JOBS FROM NONHOMEBASED_JOBS_PER_ZONE";
my $sth_get_maz_nonhome = $dbh->prepare($qry_get_maz_nonhome);
$sth_get_maz_nonhome->execute();
# Iterate over each sector-zone combo for homebased jobs
while (my $sector_maz_nh = $sth_get_maz_nonhome->fetchrow_arrayref) {
	my ($county, $sector, $zone, $nonhomebased_jobs) = (@$sector_maz_nh[0], @$sector_maz_nh[1], @$sector_maz_nh[2], @$sector_maz_nh[3]);
	print "COUNTY: $county, Sector: $sector, ZONE: $zone, Jobs: $nonhomebased_jobs, Homebased: 0  \n";
	&distribute_to_parcels_main($nonhomebased_jobs, $county, $zone, $sector, 0);# do the work for that sector-zone
}

#run script to create JOBS_ROUNDED table (with jobs on gridcells as opposed to jobs on parcels)
my $map_to_gridcells_stmt = "echo $db | perl -w /projects/urbansim7/scripts/private/cpeak/proprietors_distributor/proprietors_allocation_to_gridcells.pl";
print "map_to_gridcells_stmt = $map_to_gridcells_stmt \n";
system($map_to_gridcells_stmt);


print "proprietors distributor finished. \n";
#------------end of main routine-----------------------------


sub distribute_to_parcels_main {
	my ($jobs, $county, $zone, $sector, $is_homebased) = @_;
	my (%parcel_sec_lu_weight_hash, %parcel_sqft_hash, %parcel_tax_exempt_hash, %parcel_job_count_hash);
	# get a list of parcels in sector-zone, including sqft_per_job weight, sector_landuse_weight, and total weight.
	#my $qry_get_parcels = &get_parcel_query_safe($county, $zone, $sector, $is_homebased, 0);
	#print "get parcel query: HOMEBASED = $is_homebased \n";
	my $qry_get_parcels = &get_non_null_parcel_query($county, $zone, $sector, $is_homebased, 0);
	#print "parcel query: $qry_get_parcels \n";
	my $sth_get_parcels = $dbh->prepare($qry_get_parcels);
	$sth_get_parcels->execute();
	# create hashes for the return values from the query
	while (my $returned_row = $sth_get_parcels->fetchrow_arrayref){
		if ($is_homebased) { # if the job is homebased, give all parcels equal initial weights
			$parcel_sec_lu_weight_hash{$$returned_row[0]} = 1;
			$parcel_sqft_hash{$$returned_row[0]} = 1;
			$parcel_job_count_hash{$$returned_row[0]} = 0;
			$parcel_tax_exempt_hash{$$returned_row[0]} = 0; # normally should be $$returned_row[4];
		} else { # otherwise, weight the parcels
			$parcel_sec_lu_weight_hash{$$returned_row[0]} = $$returned_row[1];
			$parcel_sqft_hash{$$returned_row[0]} = $$returned_row[2];
			$parcel_job_count_hash{$$returned_row[0]} = $$returned_row[3];
			$parcel_tax_exempt_hash{$$returned_row[0]} = $$returned_row[4];
		}
	}
	my %parcel_sqft_per_job_weight_hash;
	my %parcel_total_weight_hash;
	#%parcel_sqft_per_job_weight_hash = &get_parcel_sqft_weights(\%parcel_sqft_hash, \%parcel_job_count_hash);
	for (my $j=1; $j<=$jobs; $j++){  # for each job:
		#calculate weights
		%parcel_sqft_per_job_weight_hash = &get_parcel_sqft_weights(\%parcel_sqft_hash, \%parcel_job_count_hash); #calculate sqft_per_job weight
		%parcel_total_weight_hash =
				&get_parcel_total_weight_hash(\%parcel_sqft_per_job_weight_hash, \%parcel_sec_lu_weight_hash, \%parcel_tax_exempt_hash, $is_homebased); #recalculate total weight
		my %cumulative_prob_dist = &get_cumulative_probability_distribution(\%parcel_total_weight_hash); # create cumulative distribution of parcels
		my $random_num = &get_random(\%cumulative_prob_dist); # get random number between 0 and the max from the cumulative distribution of parcels
		#print "Random_num: $random_num \n";
		my $selected_parcel_id = &get_parcel_id_from_cumulative_dist(
			\%cumulative_prob_dist,
			$random_num,
			\%parcel_total_weight_hash
		); # match job to a parcel

		&add_job_to_output_table ($sector, $selected_parcel_id, $county, $is_homebased); # add the job and parcel to the output table
		# update the job count for the newly matched parcel, given the new sqft-to-job ratio.
		%parcel_job_count_hash = &add_job_to_parcel_record(\%parcel_job_count_hash, $county, $selected_parcel_id);
	}
	$jobs_placed = $jobs_placed + $jobs;
	print "jobs placed: $jobs_placed \n";
}


sub get_parcel_query_simple { # returns the select query for all parcels (with buildings) of correct land use type in zone.
	my ($county, $zone, $sector, $homebased) = @_;
	my $qry_get_parcel =
		"SELECT
			a.PARCEL_ID,
			c.SEC_LU_WEIGHT,
			a. sqft,
			a.job_count,
			a.TAX_EXEMPT
		FROM PARCELS a
			INNER JOIN BUILDINGS b
			ON a.county = b.county AND a.parcel_id = b.parcel_id
			INNER JOIN SECTOR_LAND_USE_WEIGHTS c
			ON a.generic_land_use_1 = c.land_use AND a.FAZ_GROUP = c.FAZ_GROUP
		WHERE a.COUNTY = '$county'
			AND a.ZONE = '$zone'
			AND c.sector = $sector ";
	if ($homebased) {
		$qry_get_parcel .= "AND a.generic_land_use_2 = 'R' ";
	} else {
		$qry_get_parcel .= "AND a.generic_land_use_2 NOT IN ('R','GQ')";
	}
}

sub get_cumulative_probability_distribution { # Returns a cumulative probability distribution based on the total_weights for the input parcels.
	my ($parcel_total_weight_hash) = @_;
	#print join("\t",$sth_get_parcel),"\n";
	my %cumulative_prob_dist; # create a hash to hold the probability limit for each parcel
	my $max_prob_limit = 0; # holds the maximum probability limit as we iterate throught the parcels
	while  ( (my $parcel) = each %{$parcel_total_weight_hash}){
		#my $parcel_id = ${$parcel_total_weight_hash}{$parcel};
		$cumulative_prob_dist{$parcel} = ($max_prob_limit + ${$parcel_total_weight_hash}{$parcel});
		$max_prob_limit = $max_prob_limit + ${$parcel_total_weight_hash}{$parcel};
		#print "cumulative_dist for $parcel: $cumulative_prob_dist{$parcel} \n";
	}
	%cumulative_prob_dist; # returns the hash
}

sub get_random {  # returns a random number between 0 and the maximum from the cumulative probability distribution.
	my $cumulative_prob_dist = $_[0];
	my $max_prob_value = 0;
	my $hash_element_counter = 0;
	while ( (my $parcel_id, my $limit) = each %{$cumulative_prob_dist}) {
		$hash_element_counter = $hash_element_counter + 1;
		if ($limit > $max_prob_value) {
			$max_prob_value = $limit;
		}
	}
	my $random_number = rand($max_prob_value);
	#print "hash_element_counter: $hash_element_counter -- max_prob_value: $max_prob_value \n";
	#print "random number in get_random subroutine: $random_number \n";
	$random_number;
}

sub get_parcel_id_from_cumulative_dist { # Selects a parcel from the cumulative distribution hash based on a given number $r.
	my ($cumulative_prob_dist, $r, $parcel_total_weight_hash)= @_;
	# sort the hash by value:
	my @sorted_parcel_ids = sort { ${$cumulative_prob_dist}{$a} <=> ${$cumulative_prob_dist}{$b} } keys %{$cumulative_prob_dist};
	#print join ("\t", @sorted_parcel_ids), "\n";
	# iterate over sorted list until $r < the parcel's limit:
	my $parcel_id = &get_parcel_from_sorted_array(\@sorted_parcel_ids, $cumulative_prob_dist, $r, $parcel_total_weight_hash);
}


sub get_parcel_from_sorted_array { # iterates over an array of parcels until $r < the parcel's limit in the cumulative prob. distribution:
	my ($parcel_array, $cumulative_prob_dist, $r, $parcel_total_weight_hash) = @_;
	my $i = 0;
	my $selected_parcel;
	until ($selected_parcel) {
		#print join ("\t", $$parcel_array[0]), "\n";
		my $pin = ${$parcel_array}[$i];
		my $hash_count_cpd = keys (%$cumulative_prob_dist);
		#print "pin: $pin; hash count: $hash_count_cpd;  cummulative prob value: ${$cumulative_prob_dist}{$pin} \n";
		my @parcel_total_weight_hash = %$parcel_total_weight_hash;
		#print "parcel_total_weight_hash = @parcel_total_weight_hash \n";
		if ($r <= ${$cumulative_prob_dist}{$pin}) {
			$selected_parcel = ${$parcel_array}[$i];
		}
		$i = $i +1;
		#if ($i == 100) { $selected_parcel = -9999}
	}
	$selected_parcel;
}

sub add_job_to_output_table { # Add job to output table DISTRIBUTED_JOBS
	my ($sector, $parcel_id, $county, $is_homebased) = @_;
	my $qry_insert_job =
		"INSERT INTO DISTRIBUTED_JOBS (
			COUNTY,
			SECTOR,
			PARCEL_ID,
			HOMEBASED
		) VALUES (
			'$county',
			$sector,
			'$parcel_id',
			$is_homebased
		)";
	my $sth_insert_job = $dbh->prepare($qry_insert_job);
	$sth_insert_job->execute();
}

sub add_homebased_job_to_parcel_record { # increments the JOB_COUNT field in the PARCELS table by 1.
	my ($county, $parcel) = @_;
	my $qry_add_job =
		"UPDATE PARCELS
		SET JOB_COUNT = JOB_COUNT + 1
		WHERE COUNTY = '$county'
			AND PARCEL_ID = '$parcel'";
	my $sth_add_job = $dbh->prepare($qry_add_job);
	$sth_add_job->execute();
}

sub add_job_to_parcel_record {  # update the job count for the newly matched parcel, given the new sqft-to-job ratio. Commit to database.
	my ($parcel_job_count_hash, $county, $selected_parcel_id) = @_;
	$$parcel_job_count_hash{$selected_parcel_id} = $$parcel_job_count_hash{$selected_parcel_id} + 1;
	my $qry_add_job = "UPDATE PARCELS SET JOB_COUNT = JOB_COUNT + 1 WHERE COUNTY = '$county' AND PARCEL_ID = '$selected_parcel_id'";
	my $sth_add_job = $dbh->prepare($qry_add_job);
	$sth_add_job->execute();
	%$parcel_job_count_hash;
}


sub get_sum_value_from_hash {  # Returns the sum of the values from the input hash
	my ($hash) = @_;
	my $sum_value = 0;
	while ((my $key) = each %{$hash}) {
		$sum_value = ($sum_value + $$hash{$key});
	}
	$sum_value;
}

sub get_max_value_from_hash { #returns the maximum value from a hash
	my ($hash) = @_;
	my $max_value = 0;
	while ((my $key) = each %{$hash}) {
		if ($$hash{$key} > $max_value) {
			$max_value = $$hash{$key};
		}
	}
	#if ($max_value == 0) {$max_value = 1}
	$max_value;
}

sub get_parcel_sqft_per_job { # returns a hash of sqft per job rate for each parcel
	my ($parcel_sqft_hash, $parcel_job_count_hash) = @_;
	my %sqft_per_job_hash;
	while ((my $parcel) = each %{$parcel_sqft_hash}) {
		$sqft_per_job_hash{$parcel} = ($$parcel_sqft_hash{$parcel} / ($$parcel_job_count_hash{$parcel} + 1));
	}
	%sqft_per_job_hash;
}

sub get_parcel_sqft_weights { #returns a hash of the parcel_sqft_weights for each parcel in the input hashes.
	my ($parcel_sqft_hash, $parcel_job_count_hash) = @_;
	my %parcel_sqft_weights_hash;
	my %parcel_sqft_per_job_hash = &get_parcel_sqft_per_job($parcel_sqft_hash, $parcel_job_count_hash); # get the sqft per job
	#my $sum_sqft_per_job_rate = &get_sum_sqft_per_job (\%parcel_sqft_per_job_hash); # get the sum of the sqft-per-job
	my $max_sqft_per_job_rate = &get_max_value_from_hash (\%parcel_sqft_per_job_hash); # get the max  sqft-per-job
	if (! $max_sqft_per_job_rate) {$max_sqft_per_job_rate = 1}
	while ((my $parcel) = each %parcel_sqft_per_job_hash) {
		$parcel_sqft_weights_hash{$parcel} = ($parcel_sqft_per_job_hash{$parcel} / $max_sqft_per_job_rate );#or / $sum_sqft_per_job_rate
		#print "sqft_per_job_rate: $parcel_sqft_weights_hash{$parcel} \n";
	}
	%parcel_sqft_weights_hash;
}

sub get_scaled_hash { #returns the input hash, scaled to a maximum value of 1;
	my ($hash) = @_;
	my %scaled_hash;
	my $max_hash_value = &get_max_value_from_hash($hash);
	if (! $max_hash_value) {$max_hash_value = 1}
	while ((my $key) = each %{$hash}) {
		$scaled_hash{$key} = ($$hash{$key} / $max_hash_value);
	}
	#print "max_hash_value @ get_scaled_hash = $max_hash_value \n";
	%scaled_hash;
}

sub get_parcel_total_weight_hash_nonhomebased { # Returns a hash of the total_weight.
# if parcel is not tax-exempt, then total_weight = ((sqft_per_job_weight + sec_lu_weight)/2)
#  OR
# if parcel is tax-exempt, then total_weight = sec_lu_weight.
	my ($parcel_sqft_per_job_weight_hash, $parcel_sec_lu_weight_hash, $parcel_tax_exempt_hash) = @_;
	my %parcel_total_weight_hash;
	my %scaled_sec_lu_weight_hash = &get_scaled_hash($parcel_sec_lu_weight_hash);
	while ((my $parcel) = each %{$parcel_sqft_per_job_weight_hash}) {
		if ($$parcel_tax_exempt_hash{$parcel} == 0) {
			$parcel_total_weight_hash{$parcel} = ($$parcel_sqft_per_job_weight_hash{$parcel} + $scaled_sec_lu_weight_hash{$parcel}) / 2;
		} else {
			$parcel_total_weight_hash{$parcel} = $$parcel_sec_lu_weight_hash{$parcel};
		}
		#print "Parcel $parcel 's sqft_per_job_wt: $$parcel_sqft_per_job_weight_hash{$parcel} \t";
		#print "Scaled sec_lu_wt: $scaled_sec_lu_weight_hash{$parcel} \t total weight: $parcel_total_weight_hash{$parcel} \n";
	}
	#my $max_sqft_per_job_value = &get_max_value_from_hash($parcel_sqft_per_job_weight_hash);
	#my $max_sec_lu_weight_value = &get_max_value_from_hash(\%scaled_sec_lu_weight_hash);
	my $max_total_weight = &get_max_value_from_hash(\%parcel_total_weight_hash);
	#print "max_total_weight after all have been assigned = $max_total_weight \n";
	#print "max hash value gotten \n";
	if (! $max_total_weight) { #If the total weight is 0 or NULL, assign all parcels a total_weight of 1.
		%parcel_total_weight_hash = &get_flat_weights(\%parcel_total_weight_hash);
		#print "max_total_weight is null!!!!! \n";
	}
	#while ((my $p) = each %parcel_total_weight_hash){print "total weight at end of weight assignment = $parcel_total_weight_hash{$p} \n"}
	%parcel_total_weight_hash;

}

sub get_flat_weights{ # Sets all values in hash '%$a_hash' to 1.
	my ($a_hash) = @_;
	while ((my $record) = each %$a_hash) {
		$$a_hash{$record} = 1;
		#print "hash value set to $$a_hash{$record} \n";
	}
	%$a_hash;
}

sub get_parcel_total_weight_hash_homebased { # returns a hash with the same keys as the input parcel, with all values = 1;
	my ($parcel_hash) = @_;
	my %parcel_total_weight_hash_homebased;
	while ((my $parcel) = each %$parcel_hash) {
		$parcel_total_weight_hash_homebased{$parcel} = 1;
		#print "parcel_total_weight = $parcel_total_weight_hash_homebased{$parcel} \n";
	}
	%parcel_total_weight_hash_homebased;
}

sub get_parcel_total_weight_hash { # returns a hash for homebased or nonhomebased jobs, depending on the job being placed.
	my ($parcel_sqft_per_job_weight_hash, $parcel_sec_lu_weight_hash, $parcel_tax_exempt_hash, $is_homebased) = @_;
	#print "is_homebased (@ get_parcel_total_weight_hash)  = $is_homebased \n";
	my %parcel_total_weight_hash;
	if ($is_homebased) {
		%parcel_total_weight_hash = &get_parcel_total_weight_hash_homebased ($parcel_sqft_per_job_weight_hash);
	} else {
		%parcel_total_weight_hash = &get_parcel_total_weight_hash_nonhomebased($parcel_sqft_per_job_weight_hash,
																				$parcel_sec_lu_weight_hash,
																				$parcel_tax_exempt_hash);
	}
	%parcel_total_weight_hash;
}



sub get_non_null_parcel_query { # Create the query to select parcels and their weights in the right zone
# if the query generates an empty set, parcels of the alternate res/nonres type are sought.
# if still no parcels are generated, parcels for the appropriate res/nonres type are sought throught the county, irrespective of zone.
	my ($county, $zone, $sector, $homebased, $ex_counter) = @_;
	my $qry_get_parcel = &get_parcel_query_simple($county, $zone, $sector, $homebased);
	my $query_is_empty = &check_for_non_null_return($qry_get_parcel);
	if ($query_is_empty && $ex_counter < 1 ) { # if the query returns no parcels, try to get the parcels for the opposite $homebased value.
		my $opposite_of_homebased = &reverse_boolean($homebased);
		$qry_get_parcel = &get_non_null_parcel_query($county, $zone, $sector, $opposite_of_homebased, $ex_counter + 1);
	} elsif ($query_is_empty && $ex_counter >= 1) {
		print "No parcels in zone $zone.  Selecting all parcels in county.  \n\tYou might want to verify that this is expected.  \n\tProcessing may take a while... \n";
		$qry_get_parcel =
			"SELECT
				a.PARCEL_ID,
				c.SEC_LU_WEIGHT,
				a. sqft,
				a.job_count,
				a.TAX_EXEMPT
			FROM PARCELS a
				INNER JOIN SECTOR_LAND_USE_WEIGHTS c
				ON a.generic_land_use_1 = c.land_use
				AND a.FAZ_GROUP = c.FAZ_GROUP
			WHERE a.COUNTY = '$county'
				AND c.sector = $sector ";
		if (! $homebased) {
			#my $random_offset = int(rand($max_res_parcels_in_county));
			#print "random limit number: $random_offset. \n";
			$qry_get_parcel .= "AND a.generic_land_use_2 = 'R'";#  LIMIT $random_offset , 2";
		} else {
			#my $random_offset = int(rand($max_nonres_parcels_in_county));
			#print "random limit number: $random_offset. \n";
			$qry_get_parcel .= "AND a.generic_land_use_2 <> 'R' AND a.generic_land_use_2 <> 'GQ'";#  LIMIT $random_offset , 2";
		}
	}
	$qry_get_parcel;
}

sub reverse_boolean {
	my ($bool_val) = @_;
	if ($bool_val) {$bool_val = 0} else {$bool_val = 1}
	$bool_val;
}

sub check_for_non_null_return { #Returns true (1) if the query produces output, false (0) if it does not.
	my ($qry_get_parcels) = @_;
	my $is_empty;
	my @first_returned_row = $dbh->selectrow_array($qry_get_parcels);
	if ($first_returned_row[0]) {$is_empty = 0} else {$is_empty = 1}
	$is_empty;
}


##-------------------------------------- removed subroutines ------------------------------------
#sub get_parcel_query_chooser {
#	my ($county, $zone, $sector, $homebased) = @_;
#	my $qry_get_parcels;
#	if ($homebased) {
#		$qry_get_parcels = &get_parcel_query_many_parcels_expected($county, $zone, $sector, $homebased);
#	} else {
#		$qry_get_parcels = &get_parcel_query_few_parcels_expected($county, $zone, $sector, $homebased, 0);
#		print "$qry_get_parcels \n";
#	}
#	$qry_get_parcels;
#}

#sub get_max_res_parcels_in_county{
#	my $qry_total_res_parcels = "SELECT COUNT(*) FROM PARCELS WHERE GENERIC_LAND_USE_2 = 'R'";
#	my @first_returned_row = $dbh->selectrow_array($qry_total_res_parcels);
#	my $total_res_parcels = $first_returned_row[0];
#}

#sub get_max_nonres_parcels_in_county{
#	my $qry_total_res_parcels = "SELECT COUNT(*) FROM PARCELS WHERE GENERIC_LAND_USE_2 NOT IN ('R', 'GQ')";
#	my @first_returned_row = $dbh->selectrow_array($qry_total_res_parcels);
#	my $total_res_parcels = $first_returned_row[0];
#}
