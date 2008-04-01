#!/usr/bin/perl
#/*
# * UrbanSim software.
# * Copyright (C) 1998-2003 University of Washington
# * 
# * You can redistribute this program and/or modify it under the
# * terms of the GNU General Public License as published by the
# * Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
# * 
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * file LICENSE.htm for copyright and licensing information, and the
# * file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
# * 
# */


# This script is used to export mysql table to tab delimited files
# 
# created by lmwang on 08/03

#########################
# Global variables
# $dbh
# %db
# 	host
# 	db
# 	user
# 	passwd
# $file_dir
# $file
# $import/export
# $header


use DBI;
use Getopt::Long qw(:config no_ignore_case bundling);

$myName = "mysqlport";


processSwitches();


if ($test) {
	do_tests();
}
else {
	do_work();
}

###########################
#
# Main subroutines
#

sub do_work {
	$dbh = db_conn();
	
	improt_file_to_table();

	export_table_to_file();

	$dbh->disconnect();
}

sub do_tests {
	my ($errors,$tests) = (0,0);
	my ($numerr,$numtests) = (0,0);

	print "##################\nRunning tests\n";
	($numerr,$numtests) = test_all($errors,$tests);
	$errors += $numerr; $tests += $numtests;	
	#($numerr,$numtests) = test_export_table_to_file($errors,$tests);
	#$errors += $numerr; $tests += $numtests;
	
	print "$errors Failure";
	print "s" if $errors != 1;
	print " out of $tests Test";
	print "s" if $tests+1 != 1;
	print ".\n##################\n";
}

sub exist_table {
	my $search_table = shift;
	my ($sth, $table);
	my $found = 0;
	
	$sth = $dbh->prepare("show tables")
		or die "failed to prepare statement.\n";
	$sth->execute()
		or die "couldn't execute statement: " . $sth->errstr;

	while ($table = $sth->fetchrow()) {
		if ($table eq $search_table) {
			print "table $search_table found\n" if $verbose;
			$found = 1;
			last;
		}
	}
	
	$sth->finish;
	
	return $found;
}
	
sub import_file_to_table {

	return if (!$import);
	
	die "table $table_name doesn't exist, you need to create $table_name table before you import to it\n"
	    if ( !exist_table($table_name) );
	
	my ($stm, $rv, $column);
	my @columns = ();
	
	open(IMPF, "<$file_dir$file") or 
		die "Couldn't open $file_dir$file";

	if ($header) {
		<IMPF>;
		print "skip the header of $file_dir$file\n" if $verbose;
	}
		
	while(<IMPF>) {
		chomp;
		@columns = split /\t/;
		
		$stm = "insert into $table_name values ("; 
		foreach $column (@columns) {
			$stm = "$stm $column,"; 
			
		}
		chop($stm);  #chop the last ","
		$stm = $stm . ")";

		print "$stm\n" if $verbose;

		my $rv=$dbh->do($stm) 
			or die "failed to insert @column into table $table_name " . DBI->errstr;
		
	}

	close(IMPF)
		or die "could't close $file_dir$file";
}

sub export_table_to_file {

	return if (!$import);
	
	my ($stm, $sth);
	my ($table, $found);
	
	open(EXPF, ">$file_dir$file") or
		die "Couldn't open $file_dir$file";
	print "exporting $table_name to $file_dir$year$file\n" if $verbose;
	
	die "table $table_name doesn't exist\n" 
	    if ( !exist_table($table_name) );
	
	$stm = "select * from $table_name";
	$sth = $dbh->prepare($stm)
		or die "failed to prepare statement.\n";
	$sth->execute()
		or die "couldn't execute statement: " . $sth->errstr;
		
	if ($header) {
		my @column_names = @{$sth->{NAME}}; 
		my $column_name = join "\t", @column_names, "\n";
		print EXPF "$column_name";
		print "$column_name" if $verbose;
	}
		
	while (my @columns=$sth->fetchrow()) {
		print EXPF join "\t", @columns,"\n";
		print join "\t", @columns,"\n" if $verbose;
	}
		
	close(EXPF)
		or die "Couldn't close $file";

	$sth->finish;
}

sub db_conn{
	my ($DB_conn,$dbh);
	my ($host,$DB,$user,$passwd) = 
	    ($db{'host'},$db{'db'},$db{'username'},$db{'password'});
	$DB_conn = "DBI:mysql:database=$DB :host=$host";
	print "connecting to database $DB at $host\n" if $verbose;
	$dbh = DBI->connect($DB_conn,$user,$passwd) 
	  or die "failed to open database connection " . DBI->errstr;	
	
	return $dbh;

}

sub processSwitches {
	my $result;
	my ($host,$db,$user,$passwd);
	
	
	$result = &GetOptions(
		"e"	=> \$export,
		"i"	=> \$import,
		"d:s"	=> \$file_dir,
		"f:s"	=> \$file,
		"H:s"	=> \$host,
		"D:s"	=> \$db,
		"T:s"	=> \$table_name,
		"U:s"	=> \$user,
		"P:s"	=> \$passwd,
		"l"	=> \$header, 
		"t"	=> \$test,
		"h"	=> \$help,
		"v"	=> \$verbose,
	);

	if (!$result) {
		die "Error in input. Use -h for help.\n";
	}

	if ($help) {
			die
"Usage: perl $myName.pl [switches]
-i\t\timport file to MySql table
-e\t\texport MySql table to file
-d [string]\tDirectory for file in -f
-f [string]\tExporting to file name
-H [string]\tMySql host name, Default = Localhost
-D [string]\tMySql database name
-U [string]\tMysql user name
-P [string]\tMysql password
-T [string]\tTable name
-t\t\tRun Tests
-v\t\tVerbose
-h\t\tThis help

Note: switches are case-sensitive.
";
	}
	
	$file_dir = "" unless $file_dir;
	print "Directory unspecified, use current directory\n" if $verbose;
	
	if ( !$test && ( !$db || !$table_name ) ) {
		die 
"When not run tests with -t, need to specify database setting. 
Use -h for help.\n";
	}

	if ( !$test && !$import && !$export ) {
		die 
"When not run tests with -t, need to specify either import with -i switch, 
or export with -e switch. Use -h for help.\n";
	}

	if ( !$test && $import && !$file ) {
"When not run tests with -t, need to specify file to import with -f. 
Use -h for help.\n";
	}
	
	if ( !$test && $export && !$file ) {
		$file = "$table_name.tab";
		print "Filename unspecified, use $file instead\n" if $verbose;
	}
	
	if ( !$test && !$host ){
		$host = "Localhost";
		print "Database host nameunspecified, use $host instead\n" if $verbose;
	}

	print "host=$host | db=$db | table=$table_name | user=$user | passwd=$passwd\n" if $verbose;
	%db = (
		host	=> $host,
		db	=> $db,
		user	=> $user,
		passwd	=> $passwd,
	);
	
}
###################################
# Tests
#
sub test_all {
	$file_dir = "tests\/";
	$file = "test_import.tab";
	$import = 1;
	$table_name = "temp_test_mysqlexchg";
	my $table_def = "create table $table_name (
		FROM_ZONE_ID int, 
		TO_ZONE_ID int, 
		HWYTIME double
	)";

	%db = (
		host	=> 'Localhost',
		db	=> 'test',
		user	=> 'mysql',
		passwd	=> '',
	);

	#create table and import file to table
	$dbh = db_conn();
	execute_sql("drop table if exists $table_name");
	execute_sql($table_def);
	import_file_to_table();

	#export that table to file
	$file = "test_export.tab";
	$export = 1;
	$table_name = "temp_test_mysqlexchg";	
	export_table_to_file();

	#Drop table after finish test
	execute_sql("drop table if exists $table_name");

	$dbh->disconnect();

	my @file;
	push @file, "$file";

	return compare_files(@file);
}

sub execute_sql {
	my $_command = shift;
	my ($sth,$stm);
	
	if ("\L$_command" =~ /^select/) {
		$stm = $_command;

		$sth = $dbh->prepare($stm) 
			or die "Failed to prepare statement: $stm. $sth->errstr \n"; 
		$sth->execute() 
			or die "Failed to execute statement: $stm. $sth->errstr \n";
		$sth->finish;
		
	}  elsif ("\L$_command" =~ /[a-z]/) { 
	## check to make sure $_command is a valid sql query 
	## ("\L$_command" =~ /^drop/ || "\L$_command" =~ /^delete/ || "\L$_command" =~ /^update/ || 
	## "\L$_command" =~ /^create/ || "\L$_command" =~ /^insert/){
	
		$stm = $_command;
		$rv=$dbh->do($stm) 
			or die "Failed to execute statement: $stm. ". DBI->errstr;
	}

}

sub compare_files {
	my ($errors,$tests) = (0,0);
	my $file;
	foreach $file (@_) {
		$tests++;
		my $error = diff_two_files("expected_${file}","${file}");
		if ($error) {
			print "Failed $file\n";
		}
		else {
			print "Success for $file\n";
		}
		$errors += $error;
	}
	
	return ($errors,$tests);
}

sub diff_two_files {
	my $expected = shift;
	my $result = shift;
	my $error = 0;
	$error++ if system("diff -w ${file_dir}$expected ${file_dir}$result > ${file_dir}${result}.log");
	system("rm ${file_dir}${result}.log") unless $error;
	return $error;
}

