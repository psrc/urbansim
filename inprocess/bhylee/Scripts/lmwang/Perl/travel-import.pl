
###This script is used to import travel model output into mysql database 

########################################################################
#SCRIPT FOR INPUT TO MYSQL:
#	Set a parameter <YEAR> = some four-digit integer
#	Set a parameter <WinDir> = a valid Windows File System Path
#	Set parameters for a MySQL server, username, and password
#	Set a parameter <DB> = a valid MySQL database name
#	
#	Open a connection to the MySQL server using the parameters
#	
#	Part 1:
#		Get from the Windows file system:
#			"<WinDir>\<YEAR>AccessLogsum.tab"
#		which is a tab-delimited text file with 5 columns and no column 
#		names;
#	Part 2:
#		Put it into the Trondheim MySQL database:
#			"<DB>"
#		as a table named:
#			"AccessLogsum"
#		where the five columns are, in order:
#			FROM_ZONE_ID (long integer)
#			TO_ZONE_ID (long integer)
#			LOGSUM0 (double)
#			LOGSUM1 (double)
#			LOGSUM2 (double)
#	Part 3:
#		Get from the Windows file system:
#			"<WinDir>\<YEAR>procHighwayTimes.tab"
#		which is a tab-delimited text file with 3 columns and no column 
#		names;
#	Part 4:
#		Put it into the Trondheim MySQL database:
#			"WFRC_1997_scenario_jpf_5yr"
#		as a table named:
#			"procHighwayTimes"
#		where the five columns are, in order:
#			FROM_ZONE_ID (long integer) 
#			TO_ZONE_ID (long integer) 
#			HWYTIME (double)
##############################################################################

##Run: perl devConstraints.pl

#created by lmwang on 07/03



#!/usr/local/bin/perl -w

#use lib "/homes/june/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

$DEBUG=0;  # Define DEBUG flag

#setting up before running
$host = 'trondheim.cs.washington.edu';
$user = 'urbansim';
$passwd = 'UwUrbAnsIm';

$year = 1990;
$windir = "c:\";
$DB = ''; 

if (scalar(@ARGV) < 4) {
	print "Usage: perl travel_data.pl <import> <windir> <year> <DB> <table name> \n";
	print "table name is one of the following: AccesslogSum, procHighwayTimes \n";
	print "or, \n"
	print "Usage: perl travel_data.pl <export> <DB> <table name> <windir>\n";
	print "table name is one of the following: \n";
	
	exit(0);
}	

if ($ARGV[0] eq "import") {
	($action, $windir, $year, $DB, $table) = @ARGV;
} 
elseif ($ARGV[0] eq "export") {
	($action, $DB, $table, $windir) = @ARGV;
}

$DB_conn = "DBI:mysql:database = $DB :host = $host";
$dbh = DBI->connect($DB_conn,$user,$passwd) 
	or die "failed to open database connection " . DBI->errstr;

#import table
if ($action eq "import") {
	if ("\L$table" eq "accesslogsum") {
		$stm = "create table $table (
			FROM_ZONE_ID int,
			TO_ZONE_ID int,
			LOGSUM0 double,
			LOGSUM1 double,
			LOGSUM2 double
			)";
		$file = "$windir\" . $year . "AccessLogsum.tab";
	}
	elseif ("\L$table" eq "prochighwaytimes") {
		$stm = "create table $table (
			FROM_ZONE_ID int, 
			TO_ZONE_ID int, 
			HWYTIME double
			)";
		$file = "$windir\" . $year . "procHighwayTimes.tab";
	}
	else {  print "incorrect table name.\n"
		$dbh->disconnect();
		exit(0);
	}


	$rv=$dbh->do("drop table if exists $table") 
		or die "failed to drop table $table " . DBI->errstr;

	$rv=$dbh->do($stm) 
		or die "failed to create table $table " . DBI->errstr;

	readfiletotable($file,$dbh,$table);

}



##export table
if ($action eq "export") {
	exporttabletofile ($dbh, $table, $windir);
}

$dbh->disconnect();
exit(0);


sub readfiletotable {
	my $_file=$_[0];
	my $_dbh=$_[1];
	my $_table=$_[2];
	open(IMPORTF, $file) or 
		die "Couldn't open $file";

	while(<IMPORTF>) {
		$row = $_;
		chomp($row);
		@column = split(/\t/, $row);
		
		foreach $column (@column) {
			
			my $_stm = "insert into $table values ($column,"; 
		}
		chop($_stm);  #chop the last ","
		$_stm = $_stm . ")";

		if ($DEBUG) {print "$_stm\n";}		

		$_rv=$_dbh->do($_stm) 
			or die "failed to insert @column into table $table " . DBI->errstr;
		
	}

	close(IMPORTF)
		or die "can't close $file";
}

sub exporttabletofile {
	my $_dbh = $_[0];
	my $_table = $_[1];
	my $_windir = $_[2];
	
	my $_stm = "select YEAR from $_table group by YEAR";
	my $_sth = $_dbh->prepare($_stm)
		or die "failed to prepare statement.\n";
	$_sth->execute() 
		or die "couldn't execute statement: " . $_sth->errstr;

	while ($year=$_sth->fetchrow()) {
		my $_file = $_windir . "_" . $_table;
		open(EXPORTF, $_file) or 
			die "Couldn't open $_file";
		print EXPORTF "#";
		
		my $_stm = "select * from $_table where YEAR = $year";
		my $_sth = $_dbh->prepare($_stm)
			or die "failed to prepare statement.\n";
		$_sth->execute()
			or die "couldn't execute statement: " . $_sth->errstr;
		
		@column_name = @{$_sth->name}; 
		foreach $column_name (@column_name) {
 			print EXPORTF $column_name\t;
		}
		print EXPORTF "\n";
		
		while (@column=$_sth->fetchrow()) {
			foreach $column_name (@column_name) {
 				print EXPORTF $column_name\t;
			}
			print EXPORTF "\n";
		}
		
		close(EXPORTF)
			or die "can't close $_file";
	}
	
	$_sth->finish;
}
