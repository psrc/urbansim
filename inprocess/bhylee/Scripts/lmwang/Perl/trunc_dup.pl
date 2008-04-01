
###This script is used to import travel model output into mysql database 

#created by lmwang on 07/03



#!/usr/local/bin/perl -w

use lib "/homes/june/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

$DEBUG=1;  # Define DEBUG flag

#setting up before running
$host = "trondheim.cs.washington.edu";
$user = "urbansim";
$passwd = "UwUrbAnsIm";

#init data
$DB = 'parcel_quality_check_lmwang'; 
$src_table = 'prcl_mkt';
$des_table = 'prcl_mkt_nodup';

$DB_conn = "DBI:mysql:database=$DB :host=$host";
$dbh = DBI->connect($DB_conn,$user,$passwd) 
	or die "failed to open database connection " . DBI->errstr;

$rv = $dbh->do("drop table if exists $des_table")
	or die "failed to drop table $des_table";
$rv = $dbh->do("create table $des_table select * from $src_table where 1<>1")
	or die "failed to create table $des_table";  

$stm1 = "select distinct pin, MKT_ID from $src_table";

if ($DEBUG) {print "$stm1\n";}

$sth1 = $dbh->prepare($stm1)
	or die "failed to prepare statement.\n";
$sth1->execute() 
	or die "couldn't execute statement: " . $sth1->errstr;

while (@pin=$sth1->fetchrow()) {

	#if ($pin[0] ne '') {                  ##$pin[0] = "' '"; print "$pin[0]\n";}
	$stm2  = "insert into $des_table ";
	$stm2 .= "select * from $src_table where pin = " . '"' . $pin[0] . '"' . " and MKT_ID = $pin[1] order by AREA DESC limit 1";

	if ($DEBUG) {print "$stm2\n";}

	$rv=$dbh->do($stm2) 
		or die "failed to insert into $des_table " . DBI->errstr;

	#}
}
	
$sth1->finish;
$dbh->disconnect;
