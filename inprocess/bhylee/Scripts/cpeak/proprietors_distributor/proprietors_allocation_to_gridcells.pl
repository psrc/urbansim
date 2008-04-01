#For each record in jobs_lost_in_translation{
#	for each jobs_lost{
#		select parcel fragments from parcel_fractions_in_gridcells
#		construct a cumulative distribution of parcel fragments
#		select a fragment randomly
#	}
#}

use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);
use strict;
use DBI;
$| = 1;
srand(0);

my $server = 'trondheim.cs.washington.edu';
my $username = 'urbansim';
my $password = 'UrbAnsIm4Us';

print "Input database: ";
my $db = <STDIN>;
chomp $db;
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $jobs_placed = 0;

my $SQL_system_statement_1 = "mysql -h trondheim -u urbansim -f --password=UrbAnsIm4Us $db < /projects/urbansim7/scripts/private/cpeak/proprietors_distributor/parcel_jobs_to_gridcells.sql";
system($SQL_system_statement_1);

my $qry_get_jobs = "SELECT PARCEL_ID, SECTOR, HOMEBASED, JOBS_LOST FROM jobs_lost_in_translation where jobs_lost > 0";
my $sth_get_jobs = $dbh->prepare($qry_get_jobs);
$sth_get_jobs->execute();
while (my $returned_row = $sth_get_jobs->fetchrow_arrayref) {
	my ($parcel_id, $sector, $homebased, $jobs) = (@$returned_row[0], @$returned_row[1], @$returned_row[2], @$returned_row[3]);
	print "PARCEL_ID: $parcel_id,  SECTOR: $sector,  HOMEBASED: $homebased,  JOBS: $jobs \n";
	&distribute_to_gridcells_main($parcel_id, $sector, $homebased, $jobs);# do the work for that sector-zone
}

sub distribute_to_gridcells_main {
	my ($parcel_id, $sector, $is_homebased, $jobs) = @_;
	my $qry_get_parcel_frags = "SELECT GRID_ID, PARCEL_ID, PARCEL_FRACTION FROM parcel_fractions_in_gridcells WHERE PARCEL_ID = '$parcel_id'";
	my $sth_get_parcel_frags = $dbh->prepare($qry_get_parcel_frags);
	$sth_get_parcel_frags->execute();
	# create hash for the return values from the query
	my %parcel_frag_grid_id_hash;
	while (my $returned_row = $sth_get_parcel_frags->fetchrow_arrayref){
		$parcel_frag_grid_id_hash{$$returned_row[0]} = $$returned_row[2];
	}
	for (my $j=1; $j<=$jobs; $j++){  # for each job:
		#calculate cumulative probability distribution
		my %cumulative_prob_dist = &get_cumulative_probability_distribution(\%parcel_frag_grid_id_hash); # create cumulative distribution of parcel fragments
		my $random_num = &get_random(\%cumulative_prob_dist); # get random number between 0 and the max from the cumulative distribution of parcels
		#print "Random_num: $random_num \n";
		my $selected_grid_id = &get_grid_id_from_cumulative_dist(\%cumulative_prob_dist, $random_num, \%parcel_frag_grid_id_hash); # match job to a gridcell
		&add_job_to_output_table ($selected_grid_id, $sector, $is_homebased); # add the job and gridcell to the output table
		# update the job count for the newly matched parcel, given the new sqft-to-job ratio.
	}
}

sub get_cumulative_probability_distribution { # Returns a cumulative probability distribution based on the total_weights for the input parcels.
	my ($raw_weight_hash) = @_;
	#print "raw_weight hash: ", join("\t",%$raw_weight_hash),"\n";
	my %cumulative_prob_dist; # create a hash to hold the probability limit for each parcel
	my $max_prob_limit = 0; # holds the maximum probability limit as we iterate throught the parcels
	while  ( (my $gridcell) = each %{$raw_weight_hash}){
		#my $parcel_id = ${$parcel_total_weight_hash}{$parcel};
		$cumulative_prob_dist{$gridcell} = ($max_prob_limit + ${$raw_weight_hash}{$gridcell});
		$max_prob_limit = $max_prob_limit + ${$raw_weight_hash}{$gridcell};
		#print "cumulative_dist for $parcel: $cumulative_prob_dist{$parcel} \n";
	}
	%cumulative_prob_dist; # returns the hash
}

sub get_random{ # returns a random number between 0 and the maximum from the cumulative probability distribution.
	my $cumulative_prob_dist = $_[0];
	my $max_prob_value = 0;
	my $hash_element_counter = 0;
	while ( (my $grid_id, my $limit) = each %{$cumulative_prob_dist}) {
		$hash_element_counter = $hash_element_counter + 1;
		if ($limit > $max_prob_value) {
			$max_prob_value = $limit;
		}
	}
	my $random_number = rand($max_prob_value);
	$random_number;
}

sub get_grid_id_from_cumulative_dist { # Selects a parcel from the cumulative distribution hash based on a given number $r.
	my ($cumulative_prob_dist, $r, $raw_weight_hash)= @_;
	# sort the hash by value:
	my @sorted_gridcell_ids = sort { ${$cumulative_prob_dist}{$a} <=> ${$cumulative_prob_dist}{$b} } keys %{$cumulative_prob_dist};
	# iterate over sorted list until $r < the parcel's limit:
	my $gridcell = &get_gridcell_from_sorted_array(\@sorted_gridcell_ids, $cumulative_prob_dist, $r, $raw_weight_hash);
}

sub add_job_to_output_table{ # Add job to output table JOBS
	my ($gridcell, $sector, $is_homebased) = @_;
	my $qry_insert_job = "INSERT INTO JOBS_ROUNDED (GRID_ID, SECTOR, HOME_BASED) VALUES ($gridcell, $sector, $is_homebased)";
	my $sth_insert_job = $dbh->prepare($qry_insert_job);
	$sth_insert_job->execute();
}

sub get_gridcell_from_sorted_array{# iterates over an array of parcels until $r < the parcel's limit in the cumulative prob. distribution:
	my ($sorted_gridcell_array, $cumulative_prob_dist, $r, $weight_hash) = @_;
	my $i = 0;
	my $selected_gridcell;
	until ($selected_gridcell) {
		my $pin = ${$sorted_gridcell_array}[$i];
		#print "pin: $pin \t probability value: ${$cumulative_prob_dist}{$pin} \t random number : $r \n";
		if ($r <= ${$cumulative_prob_dist}{$pin}) {
			$selected_gridcell = ${$sorted_gridcell_array}[$i];
		}
		$i = $i +1;
		#if ($i == 100) { $selected_parcel = -9999}
	}
	$selected_gridcell;
}