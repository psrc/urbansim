# Copyright (C) 1998-2003 University of Washington
# Author: Chris Peak

#!/usr/bin/perl -w
use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);

# use strict;
use DBI;
#srand( time() ^ ($$ + ($$ << 15)) );
#srand(0);

############################# Round subroutine ##########################
#
#sub round {
#	my $num = @_;
#	my $big_num = 10 * $num;
#	my $trimmed_num = $big_num % 10;
#	my $rounded_num;
#	if ($trimmed_num >= 5) {
#		$rounded_num =
#
#	$rounded_num;
#}
############################# Main Routiine #############################

my $server = 'trondheim.cs.washington.edu';
my $username = 'urbansim';
my $password = 'UrbAnsIm4Us';

# Get the database to use
print "What database to you want to use? ";
my $db = <STDIN>;
chomp $db;
#my $db = "job_table_test_cpeak";

# Run script to prepare data from employers table to be split into jobs
my $system_statement = "mysql -h trondheim -u urbansim -f --password=UrbAnsIm4Us $db ";
$system_statement .="< /projects/urbansim7/scripts/private/cpeak/employers_to_jobs_prep.sql";
system($system_statement);


my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);



# split employers_sector_homebased_grid_id into jobs

my $qry_job_query_0 = "CREATE TABLE jobs (JOB_ID INT, GRID_ID VARCHAR(15), SECTOR INT, HOME_BASED TINYINT, SIC INT)";
my $sth_job_query_0 = $dbh->prepare($qry_job_query_0);
$sth_job_query_0->execute();

my $qry_job_query_1 = "SELECT * FROM tmp_employers_4";
my $sth_job_query_1 = $dbh->prepare($qry_job_query_1);
$sth_job_query_1->execute();
my $job_id = 1;
while (my $employer = $sth_job_query_1->fetchrow_arrayref) {
	my ($grid_id, $sector, $home_based, $employer_jobs, $sic) = ("NULL","NULL","NULL","NULL", "NULL");
	$grid_id = @$employer[0] if defined(@$employer[0]);
	# print "job_id = $job_id \n";
	$sector = @$employer[1] if defined(@$employer[1]);
	$home_based = @$employer[2] if defined(@$employer[2]);
	$employer_jobs = @$employer[3] if defined(@$employer[3]);
	$sic = @$employer[4] if defined(@$employer[4]);
	for ($i=1; $i<=$employer_jobs; $i++) {
		#print "employer jobs = $employer_jobs \n";
		#print "i = $i \n";
		#print "job number: $job_id \n";
		my $qry_insert_1 = "INSERT INTO jobs (JOB_ID, GRID_ID, SECTOR, HOME_BASED, SIC) ";
		$qry_insert_1 .= "VALUES ($job_id, $grid_id, $sector, $home_based, $sic)";
		my $sth_insert_1 = $dbh->prepare($qry_insert_1);
		$sth_insert_1->execute();
		$job_id = $job_id + 1;
	}
	#print "grid id = $grid_id.\n";
}

my $sth_drop_table =  $dbh->prepare("DROP TABLE tmp_employers_4");
#$sth_drop_table->execute();

$dbh->disconnect;
