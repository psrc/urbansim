
###This script is used to import travel model output into mysql database 

##Run: perl devConstraints.pl

#created by lmwang on 07/03



#!/usr/local/bin/perl -w

use lib "/homes/june/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

$DEBUG=0;  # Define DEBUG flag

#$dir_sep="/";

#setting up before running
$host = "trondheim.cs.washington.edu";
$user = "urbansim";
$passwd = "UwUrbAnsIm";

$year = 1990;
$windir = '';
$DB = ''; 

if (scalar(@ARGV) < 4) {
	print "Usage: perl mysqlexchg.pl import windir year DB table_name \n";
	print "or, \n";
	print "perl mysqlexchg.pl export DB table_name windir year \n";
	print "where table_name is one of AccessLogsum, HighwayTimes for import option\n";
	
	exit(0);
}	

if ($ARGV[0] eq "import") {
	($action, $windir, $year, $DB, $table) = @ARGV;
} 
elsif ($ARGV[0] eq "export") {
	($action, $DB, $table, $windir, $year) = @ARGV;
}

$DB_conn = "DBI:mysql:database=$DB :host=$host";
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
		$file = $windir . $year . "_AccessLogsum.tab";
	}
	elsif ("\L$table" eq "highwaytimes") {
		$stm = "create table $table (
			FROM_ZONE_ID int, 
			TO_ZONE_ID int, 
			HWYTIME double
			)";
		$file = $windir . $year . "_HighwayTimes.tab";
	}
	else {  print "incorrect table name.\n";
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
	exporttabletofile ($dbh, $table, $windir, $year);
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
		
		my $_stm = "insert into $table values ("; 
		foreach $column (@column) {
			$_stm = "$_stm $column,"; 
			
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
	my $_year = $_[3];
	
#	my $_stm = "select ZONE from $_table group by ZONE";
#	my $_sth = $_dbh->prepare($_stm)
#		or die "failed to prepare statement.\n";
#	$_sth->execute() 
#		or die "couldn't execute statement: " . $_sth->errstr;
#
#	while ($year=$_sth->fetchrow()) {
		my $_file = $_windir . $_table . ".dat";
		open(EXPORTF, ">$_file") or 
			die "Couldn't open $_file";
		# print EXPORTF "#";
		
		my $_stm = "select * from $_table"; # where YEAR = $year";
		my $_sth = $_dbh->prepare($_stm)
			or die "failed to prepare statement.\n";
		$_sth->execute()
			or die "couldn't execute statement: " . $_sth->errstr;
		
#		@column_name = @{$_sth->{NAME}}; 
#		foreach $column_name (@column_name) {
# 			print EXPORTF "$column_name\t";
#		}
#		print EXPORTF "\n";
		
		while (@column=$_sth->fetchrow()) {
			foreach $column (@column) {
 				print EXPORTF "$column\t";
			}
			print EXPORTF "\n";
		}
		
		close(EXPORTF)
			or die "can't close $_file";
#	}
	
	$_sth->finish;
}
