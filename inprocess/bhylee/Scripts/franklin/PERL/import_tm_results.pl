#!/usr/bin/local/perl -w
# import_tm_results.pl
use Cwd;
use DBI;
use warnings;

$output_db = "WFRC_1997_output_2030_const";
$db_host = "trondheim.cs.washington.edu";
$db_username = "urbansim";
$db_password = "UwUrbAnsIm";
$mcpost_table = "travel_model_mcpost_report";
$shares_table = "travel_model_shares_report";

$tm_root_dir = "c:/WFRC/const/";

$mcpost_subdir = "9AnalysisHwy/1HwyStats/County_PeriodReports/MCpost/";
$mcpost_file = "Aq_10_0_RE_model_MCpost.txt";

$shares_subdir = "9AnalysisTran/9Shares/";
$shares_file = "SharesAndLinkedTrips_Region.txt";

@tm_years = (1997, 2000, 2003, 2008, 2012, 2016, 2020, 2025, 2030);

%databases = (
	'output_db' => {
		host => $db_host,
		db => $output_db,
		username => $db_username,
		password => $db_password,
	}
)

$dbh = db_conn($databases{'output_db'})

# Loop through the travel model years
for $tm_year (@tm_years) {
	
	# If this is the first year in the list, delete the old tables and a new, empty ones.
	if $tm_year=$tm_years[0] {
		my $_stm = "drop table if exists $mcpost_table;";
		$_rv = $dbh -> do($_stm) 
			or die "failed to execute \"$_stm\"\nbecause: " . DBI->errstr;
		$_stm = "create table $mcpost_table (YEAR int, GROUP string, DELAY double, VHT double, "
			."SPEED double, VMT double, PCTVC_gt1 double, PCTVC_gt1pt2 double);";
		$_rv = $dbh -> do($_stm) 
			or die "failed to execute \"$_stm\"\nbecause: " . DBI->errstr;
			
		$_stm = "drop table if exists $shares_table;";
		$_rv = $dbh -> do($_stm) 
			or die "failed to execute \"$_stm\"\nbecause: " . DBI->errstr;
		$_stm = "create table $shares_table (YEAR int, GROUP string, DELAY double, VHT double, "
			."SPEED double, VMT double, PCTVC_gt1 double, PCTVC_gt1pt2 double);";
		$_rv = $dbh -> do($_stm) 
			or die "failed to execute \"$_stm\"\nbecause: " . DBI->errstr;
	}
	
	$tm_subdir = "DV31_UrbanSim_$tm_year/";
	
	# Open the MCPOST report file
	$filepath = $tm_root_dir.$tm_subdir.$mcpost_subdir.$mcpost_file;
	open MCPOST, $filepath or die "Error on opening MCPOST for $tm_year\nbecause: $!";
	print "Opened $filepath.\n";
	
	my $dbh = db_conn($output_db);
	
	$rownum=0;
	
	
	while(<MCPOST>) {
		$rownum++;
		
		$row = $_;
		chomp($row);
		@columns = split(/\s+/, $row);
		
		# Specify which rows of the report to skip
		$skip=0;
		$skip=1 if $row<4;
		$skip=1 if $row=9;
		$skip=1 if $row=15;
		$skip=1 if $row=21;
		$skip=1 if $row=27;
		$skip=1 if $row=33;
		$skip=1 if $row=39;
		
		# Import data to MySQL unless the row is skipped
		unless ($skip) {
			$_stm = "insert into $mcpost_table select $tmyear as YEAR, @columns[0] as GROUP, @columns[1] as DELAY, @columns[2] as VHT, "
				."@columns[3] as SPEED, @columns[4] as VMT, @columns[5] as PCTVC_gt1, @columns[6] as PCTVC_gt1pt2;"
			$_rv = $dbh -> do($_stm) 
				or die "failed to execute \"$_stm\"\nbecause: " . DBI->errstr;
		}
	}
	
	# Close the MCPOST report file
	close(MCPOST)
		or die "can't close $_file";
	
	# Open the SHARES report file
	$filepath=$tm_root_dir.$tm_subdir.$shares_subdir.$shares_file;
	open SHARES, $filepath or die "Error on opening SHARES for $tm_year\nbecause: $!";
	print "Opened $filepath.\n";
	
	while(<MCPOST>) {
		$rownum++;

		$row = $_;
		chomp($row);
		$row = s/|/\d/;
		
		@columns = split(/\s+/, $row);
		
		# Specify which rows of the report to skip
		$skip=0;
		$skip=1 if $row<3;
		$skip=1 if $row=6;
		$skip=1 if $row=8;
		$skip=1 if $row=12;
		$skip=1 if $row=14;
		$skip=1 if $row=18;
		$skip=1 if $row=22;
		$skip=1 if $row=26;
		$skip=1 if $row>29;
		
		# Import data to MySQL unless the row is skipped
		unless ($skip) {
			$_stm = "insert into $mcpost_table select $tmyear as YEAR, @columns[0] as GROUP, @columns[1] as DELAY, @columns[2] as VHT, "
				."@columns[3] as SPEED, @columns[4] as VMT, @columns[5] as PCTVC_gt1, @columns[6] as PCTVC_gt1pt2;"
			$_rv = $dbh -> do($_stm) 
				or die "failed to execute \"$_stm\"\nbecause: " . DBI->errstr;
		}
	}
	
	# Close the SHARES report file
	close(MCPOST)
		or die "can't close $_file";
}