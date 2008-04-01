# perl -w /projects/urbansim7/scripts/private/petecaba/perl/CopyTblDb.pl

#!/usr/bin/perl -w
use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);

########
# This script requests two inputs from the user:  
# 	-database A, which must exist
#	-database B, which must not exist (yet).
#It then creates database B and fills it with all tables from A.
##########

use strict;
use DBI;

my $server = 'trondheim.cs.washington.edu';
my $username = 'urbansim';
my $password = 'UrbAnsIm4Us';

print "What database to you want to use? ";
my $db_in = <STDIN>;
chomp $db_in;
#print "What database to you want to create and copy to? ";
#my $db_out = <STDIN>;
#chomp $db_out;
print "What is the table list you want to use? ";
my $table_list = <STDIN>;
chomp $table_list;


my $dbh_in = DBI->connect("dbi:mysql:$db_in:$server", $username, $password);


########
# Make sure the output database doesn't exist
#my $check_query = "show databases";
#my $sth_check = $dbh_in->prepare($check_query);
#$sth_check->execute();
#while (my $dbases = $sth_check->fetchrow_arrayref) {
#	my $t = $$dbases[0];
# 	print "@$dbases  ... $t\n";
#	if ($t eq $db_out) {die "Database $t already exists."};
#}

########
# Create output database
#my $create_query = "create database $db_out";
#my $sth_create = $dbh_in->prepare($create_query);
#$sth_create->execute();

#my $dbh_out = DBI->connect("dbi:mysql:$db_out:$server", $username, $password);

open TABLE_LIST, "$table_list";
	#|| die "unable to open the table list file $table_list\n";

#my @table_list = ();
while (<TABLE_LIST>) {
	chomp;
	#push @table_list, $_;
	print join("\t",$_),"\n";
	my $write_query = "drop table $_ ";
	my $sth_in = $dbh_in->prepare($write_query);
	$sth_in->execute(); 
}	


########
# Get list of tables to copy from input database
#my $query = "show tables";
#my $sth = $dbh_in->prepare($query);
#$sth->execute();


########
# Copy tables to new output database
#while (my $row = $sth->fetchrow_arrayref) {
#	 print join("\t",@$row),"\n";
# 	my $write_query = "create table @$row select * from $db_in.@$row";
#	my $sth_out = $dbh_out->prepare($write_query);
#	$sth_out->execute(); 
#}

$dbh_in->disconnect;
#$dbh_out->disconnect;




