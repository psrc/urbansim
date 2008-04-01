#!c:\perl\bin -w

use strict;
use DBI;

my $server = 'trondheim.cs.washington.edu';
my $db = 'cpeak_pums_HI'; # Input database
my $db2 = 'cpeak_test'; # Output database
my $username = 'urbansim';
my $password = 'UwUrbAnsIm';

my $dbh = DBI->connect("dbi:mysqlPP:$db:$server", $username, $password);
my $dbh2 = DBI->connect("dbi:mysqlPP:$db2:$server", $username, $password);

my $query = "show tables";
my $sth = $dbh->prepare($query);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref) {
	print join("\t",@$row),"\n";
	my $tbl = "@$row";
	
	# copy tables 
	my $query2 = "create table $db2.$tbl select * from $db.$tbl";
	my $sth2 = $dbh2->prepare($query2);
	$sth2->execute();
}

$dbh->disconnect;
