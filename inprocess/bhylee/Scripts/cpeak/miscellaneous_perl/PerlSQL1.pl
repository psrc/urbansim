#!/usr/bim/perl -w

use strict;
use DBI;

my $server = 'trondheim.cs.washington.edu';
my $db = 'cpeak_pums_HI';
my $username = 'urbansim';
my $password = 'UwUrbAnsIm';

my $dbh = DBI->connect("dbi:mysqlPP:$db:$server", $username, $password);

my $query = "SELECT COUNT(*) FROM PUMS90_NF";
my $sth = $dbh->prepare($query);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref) {
	print join("\t",@$row),"\n";
}

$dbh->disconnect;
