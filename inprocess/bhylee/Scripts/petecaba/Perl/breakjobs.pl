
###This script is used to import travel model output into mysql database 

#created by lmwang on 07/03



#!/usr/local/bin/perl -w

use lib "/projects/urbansim7/users/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

$DEBUG=1;  # Define DEBUG flag

#setting up before running
$host = "trondheim.cs.washington.edu";
$user = "urbansim";
$passwd = "UrbAnsIm4Us";

#init data
$DB = 'enlisted_military'; 
$src_table = 'enlisted_in_grid';
$des_table = 'enlisted_out_grid';

$DB_conn = "DBI:mysql:database=$DB :host=$host";
$dbh = DBI->connect($DB_conn,$user,$passwd) 
	or die "failed to open database connection " . DBI->errstr;

$rv = $dbh->do("drop table if exists $des_table")
	or die "failed to drop table $des_table";
$rv = $dbh->do("create table $des_table (GRID_ID int(11), SIC int(11), EMPLOYER_ID text)")
	or die "failed to create table $des_table";


$stm1 = "select GRID_ID, SIC, JOBS, EMPLOYER_ID from $src_table";
if ($DEBUG) {print "$stm1\n";}

$sth1 = $dbh->prepare($stm1)
	or die "failed to prepare statement.\n";
$sth1->execute() 
	or die "couldn't execute statement: " . $sth1->errstr;

while (@record=$sth1->fetchrow()) {
if ($DEBUG) {print "@record\n";}
	for ($i=0; $i<$record[2]; $i++){
		$stm2  = "insert into $des_table (GRID_ID, SIC, EMPLOYER_ID) VALUES (${record[0]}, ${record[1]}, '${record[3]}')";
		$rv=$dbh->do($stm2) 
			or die "failed to insert into $des_table " . DBI->errstr;

		if ($DEBUG) {print "$stm2\n";}
	}

}
	
$sth1->finish;
$dbh->disconnect;
