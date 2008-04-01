###This script is used to submit a sql script to mysql server
##run:
##	perl sql.pl a_sql_file.sql

#created by lmwang on 07/03


#!/usr/local/bin/perl -w

use lib "/homes/june/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

$DEBUG=1;  # Define DEBUG flag

#Set these up before running
$host = "trondheim.cs.washington.edu";
$user = "urbansim";
$passwd = "UwUrbAnsIm";

#init data
$file = ''; 
$dbh = '';  #global variable for database handler;

if (scalar(@ARGV) != 1) {
	print "Usage: perl sql.pl sql_script_file_name \n";
	exit(0);
}	

$file = $ARGV[0];

@command = parse_file ($file);

foreach $command (@command) {
	parse_sql ($command);
}	

$dbh->disconnect();
exit(0);


sub parse_file {
	my $_file=$_[0];

	open(SCRIPTF, $_file) or 
		die "Couldn't open $_file";

	my @_command; 
	my $i=0;

	while(<SCRIPTF>) {
		$row = $_;
		chomp($row);
		$row =~ s/^\s+//;
		$row =~ s/\s+$//;
		next if ($row =~ /^#/);  # discard comments

		$_command[$i] = $_command[$i] . " " . $row;

                $_command[$i] =~ s/^\s+//;
                $_command[$i] =~ s/;//;

		if ($row =~ s/\;//) {
		    $i++;} 

	}
	if ($DEBUG) {foreach $_command (@_command) {print "$_command\n";}}
	 
	close(SCRIPTF)
		or die "Couldn't close $_file\n";
	
	return @_command;
}

sub parse_sql {
	my $_command=$_[0];
	
	if ("\L$_command" =~ /^use/) {
		($_, $_db) = split(/ /, $_command);
		$_DB_conn = "DBI:mysql:database=$_db :host=$host";

                if ($DEBUG) {print "$_command\n";}
		if ($DEBUG) {print "DB connection string: $_DB_conn\n";}
		
		#$dbh->disconnect();  #disconnect the old database connection;
		
		$dbh = DBI->connect($_DB_conn,$user,$passwd) 
			or die "failed to open database connection " . DBI->errstr;
		
	} elsif ("\L$_command" =~ /^select/) {
		$stm = $_command;

                if ($DEBUG) {print "$_command\n";}

		$sth = $dbh->prepare($stm) 
			or die "Failed to prepare statement: $stm. $sth->errstr \n"; 
		$sth->execute() 
			or die "Failed to execute statement: $stm. $_sth->errstr \n";
		$sth->finish;
	}  elsif ("\L$_command" =~ /[a-z]/) { ##elsif ("\L$_command" =~ /^drop/ || "\L$_command" =~ /^delete/ || "\L$_command" =~ /^update/ || 
		  ##"\L$_command" =~ /^create/ || "\L$_command" =~ /^insert/){
		$stm = $_command;
                if ($DEBUG) {print "$_command\n";}
		$rv=$dbh->do($stm) 
			or die "Failed to execute statement: $stm. ". DBI->errstr;
	}
}

