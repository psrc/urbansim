#!/usr/bin/perl -w
#
# Perl script that updates data quality indicators:
#	parse xml file for indicator configuration;
#	execute sql-query to mysql database, create indicator table;
#       export indicator table as .html and .csv files;
#       check those files in to CVS repository.
#
# UrbanSim software.
# Copyright (C) 1998-2003 University of Washington
# 
# You can redistribute this program and/or modify it under the
# terms of the GNU General Public License as published by the
# Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# file LICENSE.htm for copyright and licensing information, and the
# file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
# 
# Author: Liming Wang (lmwang AT u.washington.edu)
#         Chris Peak 
#
# TODO:	parse xml file for indicator configuration;
# TODO:	execute sql-query to mysql database, create indicator table;
# TODO: export indicator table as .html and .csv files;
# TODO: check those files in to CVS repository.
# 

use lib qw(/projects/urbansim7/lmwang/cpan/lib/perl5/site_perl/5.6.1/i386-linux);
use Cwd;
use DBI;
use Getopt::Long qw(:config no_ignore_case bundling);

# GLOBAL VARIABLES:
# $dq_script_dir
# $cvsroot
# $repository_path
# $working_path, or . otherwise
# $cvs_dir
# $log_file
$prompt = 1;
# $debug = 0;
# $verbose
# %db
#	host,db,username,password
# @script_files 
#      script file used to update database before dq indicator runs
# $tex_script
#      script converting .csv table to teX ready file

	
$myName = "DQIUpdate";

processSwitches();

do_work();

###########################
#
# Main subroutines
#

sub do_work {
    my @dq_script_files = scan_dq_script_dir();
    open(LOG, ">${working_path}${log_file}") or die "failed to open log file ${working_path}$log_file: $!\n";
    #chdir($working_path);
    $dbh=db_conn($db);

    update_data() if $update;

    checkout_files();  #checkout indicators from repository
    foreach my $dq_script_file (@dq_script_files) {

	my ($dq_name,$sql_query);
	eval {
	    ($dq_name,$sql_query) = read_dq_script($dq_script_file);
	    print "\n\n===execute indicator: $dq_name===\n" if $prompt;
	    my @non_exist_files = check_file_existence($dq_name);   # check if indicator exist at repository

	    backup_indicators($dq_name);    #backup indicator table to archive database
	    execute_sql_query($sql_query);
	    export_table($dq_name);
	    commit_files(\@non_exist_files, $dq_name);

	};
	print_log($dq_name,$@);
    }    
    $dbh->disconnect;
    close(LOG);
    
    
    #call script to convert .csv table to teX ready file

    exec("perl $tex_script") if $tex;

}

sub update_data {
    print "===update databases===================================================\n" if $prompt;
    foreach my $script_file (@script_files) {
	my $system_statement = "mysql -h $host -u $user -f --password=$passwd ";
	$system_statement .="< $dq_script_dir$script_file";
	print "$system_statement\n" if $verbose;
	system($system_statement);	
    }

}
sub backup_indicators {
    my $table_name = shift;

    my $time = get_time("short");
    my ($back_stm,$drop_stm);
    my $archived_short_name;

    #should test if table exists first
    if ( exist_table($table_name)) {

	$archived_short_name = archived_short_name($table_name);

	$backup_stm = "create table $archive_db.${archived_short_name}_$time ";
	$backup_stm .= "select * from $table_name";

	print "===backup indicator===================================================\n" if $prompt;
	print "$backup_stm\n" if $verbose;

	#if table name is "indicators_runs" or "summary_indicators_city_level"
	#empty indicator tables instead of drop them
	if (($table_name eq "indicators_runs" ) || ($table_name eq "summary_indicators_city_level")) {
	    $drop_stm = "delete from $table_name";
	}else {
	    $drop_stm = "drop table if exists $table_name";
	}

	print "$drop_stm\n" if $verbose;
	execute_sql($backup_stm);
	execute_sql($drop_stm);
    }
}

sub archived_short_name {
    my $table_name = shift;

    my $mapping_table = "archived_short_table_name_mapping";
    my $stm = "select short_name from ${archive_db}.${mapping_table} where long_name = '" . $table_name . "'";
    
    my $sth = $dbh->prepare($stm);
    $sth->execute();

    my @short_names = $sth->fetchrow();
    
    if (defined ${short_names[0]}) {
	$name = $short_names[0];
    }else {
	$name = $table_name;
    }

    $sth->finish;

    return $name;
}

sub exist_table {
    my $table_name = shift;
    
    my $exist = 0;
    my $stm = "show tables";
    my $sth = $dbh->prepare($stm);
    $sth->execute();

    while (my @name=$sth->fetchrow()){
	if ($name[0] =~ /^$table_name$/){ 
	    $exist = 1;
	    last;
	}
    }
    
    $sth->finish;
   return $exist;
}

sub checkout_files {
    print "===checkout indicators from repository================================\n" if $prompt;

    system "cvs -d $cvsroot checkout -d $working_path $repository_path";
}

sub commit_files {
    my $ptr_files = shift;
    my $dq_name = shift;
    print "===commit files to repository=========================================\n" if $prompt;

    foreach my $file (@$ptr_files) {
	print "cvs -d $cvsroot add ${working_path}$dq_name$file\n" if $verbose;
	system("cvs -d $cvsroot add ${working_path}$dq_name$file");
    }
    
    print "cvs -d $cvsroot commit -m '(cpeak&lmwang) latest indicator' ${working_path}$dq_name.csv\n" if $verbose;
    system("cvs -d $cvsroot commit -m '(cpeak&lmwang) latest indicator' ${working_path}$dq_name.csv");
    print "cvs -d $cvsroot commit -m '(cpeak&lmwang) latest indicator' ${working_path}$dq_name.html\n" if $verbose;
    system("cvs -d $cvsroot commit -m '(cpeak&lmwang) latest indicator' ${working_path}$dq_name.html");
}

sub check_file_existence {
    my $table_name = shift;
    my @non_exist = ();
    if (!(-e "${working_path}${table_name}.html")) {
	print "file ${working_path}$table_name.html doesn't exists\n" if $verbose;
	push(@non_exist, ".html");
    }
    if (!(-e "${working_path}$table_name.csv")) {
	print "file ${working_path}$table_name.csv doesn't exists\n" if $verbose;
	push(@non_exist, ".csv");
    }
    return @non_exist;
}


sub scan_dq_script_dir {
    opendir(DIR, "$dq_script_dir") ||
    die "   Couldn't open directory $dq_script_dir: $!\n";
    
    foreach my $entry (readdir DIR) {
	if ("\L$entry" =~ /^dq_.*sql$/){
	    push(@dq_script_files, $entry);
	}
    }
    
    closedir(DIR);
    return @dq_script_files;
}

sub read_dq_script {
    my $dq_file = shift;
    my $table_name = $dq_file;
    $table_name =~ s/^dq_(.*)\.sql/$1/g;

    $dq_file = $dq_script_dir . $dq_file;
    if (!(-e "$dq_file")) {
		print "$dq_file was not found\n";  #it is less possible to happen.
		exit(0);
	}

    
    open(DQ,"<$dq_file")
	or die "failed to open script file $dq_file: $!\n";
    my $sql_query = "";
    while(<DQ>){
	$sql_query =  $sql_query . $_;
    }
    close(DQ);
    return ($table_name, $sql_query);
}

sub execute_sql_query {
    my $sql_query = shift;
    my @commands = parse_sql_scripts($sql_query); # breaks SQL script into an array

    print "===executing query====================================================\n" if $prompt;
    foreach $command (@commands) {
	print "$command\n" if $verbose;
	execute_sql($command);
    }
}

sub print_log {
    my $table_name = shift;
    my $err = shift; 

    my $time = get_time("long");

    if ($err) {
	print LOG "===${time}\t${table_name} update failed\n";
	print LOG "${err}\n";
	print "===${time}\t${table_name} update failed\n" if $prompt;
	print "${err}\n" if $verbose;
    } else {
	print LOG "${time}\t${table_name} updated succuessfully.\n";
	print "===${time}\t${table_name} updated succuessfully.\n" if $prompt;
    }
}

sub parse_sql_scripts{
	my $sql_scripts = shift;
	my @scripts;
	push(@scripts, split(/\n/,$sql_scripts));

	my @commands; 
	my $i=0;

	foreach my $row(@scripts) {
		chomp($row);

		$row =~ s/^\s+|\s+$//;           #discards spaces
		#$row =~ s/\s+$//;
		
		next if ($row =~ /^#/);     # discards comments
		$row =~ s/\#.*$//;
		
		$commands[$i] = $commands[$i] . " " . $row;

                $commands[$i] =~ s/^\s+//;
                $commands[$i] =~ s/;//;	
	
		if ($row =~ s/\;// || $row =~ /^\\\./) {     #breaks when encountering a ";" or a row beginning with "\."
 		    $i++;} 
	}
	#if ($verbose) {
	#	foreach $command (@commands) {print "sql command quene: $command\n";}
	#}

	return @commands;
}

sub execute_sql {
	my ($_command) = @_;
	
	if ("\L$_command" =~ /^use/) {
		#do nothing for "use database" syntax
                  #($_, $_db) = split(/ /, $_command);
		  #$dbh = db_conn($databases{$_db});

		#or, just execute it as other syntax:

		$stm = $_command;
		#if ($verbose) {print "executing $stm\n";}
		$rv=$dbh->do($stm) 
			or die "Failed to execute statement: $stm. ". DBI->errstr;
		
	} elsif ("\L$_command" =~ /^select/) {
		$stm = $_command;
		#if ($verbose) {print "executing $stm\n";}
		$sth = $dbh->prepare($stm) 
			or die "Failed to prepare statement: $stm. $sth->errstr \n"; 
		$sth->execute() 
			or die "Failed to execute statement: $stm. $sth->errstr \n";
		$sth->finish;		
	}  elsif ("\L$_command" =~ /[a-z]/) { 
		$stm = $_command;
		#if ($verbose) {print "executing $stm\n";}
		$rv=$dbh->do($stm) 
			or die "Failed to execute statement: $stm. ". DBI->errstr;
	}

	#$_[0] = $dbh;
	#actually return the $dbh
}

sub db_conn{
	my $db = $_[0];
	my ($host,$DB,$user,$passwd) = ($db->{'host'},$db->{'db'},$db->{'username'},$db->{'password'});
	$DB_conn = "DBI:mysql:database=$DB :host=$host";
	if ($verbose) {print "connecting to database $DB_conn\n";}
	$dbh = DBI->connect($DB_conn,$user,$passwd) 
	  or die "failed to open database connection " . DBI->errstr;	
	
	return $dbh;

}

sub export_table {
	my $dq_name = shift;
    
	print "===export indicators to file from db==================================\n" if $prompt;
	
	my $htmlheader = <<"EOF;";
<HTML>
<HEAD><TITLE>Data Quality Indicators</TITLE></HEAD>
<style type="text/css">
TABLE {
margin: 0px;
padding: 0px;
border: 1px solid black;
}

TD { 
border: 1px solid black; 
padding: 4px;
text-align: right ;
}
#header {
text-align: center ;	
}
#non-digit {
text-align: left ;
}
</style>
<BODY>
<TABLE ALIGN = "CENTER", CELLSPACING = 0>
<CAPTION><FONT SIZE="5">$dq_name</FONT></CAPTION>
<TR>
EOF;

	my $htmlfinal = <<"EOF;";
</TABLE>
<CENTER><A HREF="javascript:history.go(-1)">Back</A></CENTER>
</BODY></HTML>
EOF;
    
	open(EXPORTCSV, ">${working_path}$dq_name.csv") or 
		die "Couldn't open $dq_name.csv: $!\n";

	open(EXPORTHTML, ">${working_path}$dq_name.html") or 
		die "Couldn't open $dq_name.html: $!\n";

	# Prepare and execute describe query
	my $header_stm = "DESCRIBE $dq_name";
	my $header_sth = $dbh->prepare($header_stm);
	$header_sth->execute();
	
	#print EXPORTHTML $htmlheader;
	my (@field_name,@field_types, $csvheader,$csvrow,$htmlrow);

	while (@field_name=$header_sth->fetchrow()) {
	    if ($field_name[1] =~ /int/ || $field_name[1] =~ /double/) {
		push(@field_types, '');
	    }else {
		push(@field_types, ' id="non-digit"');
	    }

	    $csvheader = $csvheader . '"' . $field_name[0] . '"' . ',';
	    $htmlheader = $htmlheader . "<TD id='header'><B>$field_name[0]</B></TD>";
	}
	chop($csvheader);    #chop the last ","

	print EXPORTCSV $csvheader;
	print EXPORTHTML $htmlheader;

	print EXPORTCSV "\n";
	print EXPORTHTML "\n";

	my $stm = "select * from $dq_name"; 
	my $sth = $dbh->prepare($stm)
		or die "failed to prepare statement\n";
	$sth->execute()
		or die "couldn't execute statement: " . $sth->errstr;

	while (my @columns=$sth->fetchrow()) {
       		foreach my $item (@columns){		#set null fields
		    if (! defined($item)){
			$item = "NULL";
		    }
		}
 
                $csvrow = join(",", @columns);

		$htmlrow = "<TR>" ;
                for($i=0;$i<scalar(@columns);$i++) {
			$htmlrow = $htmlrow . "<TD" . $field_types[$i] . ">" . $columns[$i] . "</TD>"; 
                }

		print EXPORTCSV "$csvrow\n";
		print EXPORTHTML "$htmlrow\n";

		#print "$csvrow\n" if $debug;
		#print "$htmlrow\n" if $debug;
	}
	
	print EXPORTHTML $htmlfinal;

	close(EXPORTCSV)
			or die "couldn't close $dq_name.csv: $!\n";
	close(EXPORTHTML)
			or die "couldn't close $dq_name.html: $!\n";
	
	
	$header_sth->finish;
	$sth->finish;
}

sub get_time {
    my $format = shift;
    # Get date information
    my ($Seconds, $Minutes, $Hours, $DayInMonth, $Month, $ShortYear,
	$DayOfWeek, $DayOfYear, $IsDST);
 
    ($Seconds, $Minutes, $Hours, $DayInMonth, $Month, $ShortYear,
     $DayOfWeek, $DayOfYear, $IsDST) = localtime(time);

    #Fix the month for beginning count at 0
    $Month = $Month + 1;

    # Fix the year for post-Y2K
    my $Year = $ShortYear + 1900;
    my $FixedYear;
    if ($ShortYear >= 100) {
    	$FixedYear = $ShortYear - 100 
    }

    #adjusted for one-digit numbers
    $Seconds = "0" . $Seconds if ($Seconds < 10);
    $Minutes = "0" . $Minutes if ($Minutes < 10);
    $Hours = "0" . $Hours if ($Hours < 10);
    $DayInMonth = "0" . $DayInMonth if ($DayInMonth < 10);
    $Month = "0" . $Month if ($Month < 10);
    $FixedYear = "0" . $FixedYear if ($FixedYear < 10);
    
    if ("\L$format" eq "long") {
	$time="$Month\/$DayInMonth\/$Year,$Hours\:$Minutes\:$Seconds";
    }else{  #("\L$format" eq "short") {
	$time="$Month$DayInMonth$FixedYear$Hours$Minutes";
    }
    
    return $time;
    
}

sub processSwitches {
	my $result;
	
	$result = &GetOptions(
		"h"		=> \$help,
		"w:s"		=> \$working_path,
		"d:s"           => \$dq_script_dir,
		"l:s"           => \$log_file,
 		"H:s"	        => \$host,
		"D:s"	        => \$db,
		"A:s"           => \$archive_db,
		"U:s"	        => \$user,
		"P:s"	        => \$passwd,
		"r:s"           => \$cvsroot,
                "p:s"           => \$repository_path,
		"u"             => \$update,
		"t"		=> \$tex,		
		"v"		=> \$verbose,
	);

	if (!$result) {
		die "Error in input. Use -h for help.\n";
	}

	if ($help) {
			die
"Usage: perl $myName.pl [switches]
-h\t\tThis help
-w [string]\tWorking path, default = cwd (current working directory)
-d [string]\tData quality indicator scripts directory, default = /projects/urbansim7/scripts/public/data_prep/ 
-l [string]\tLog filename, default = current-time.log
-H [string]\tMySql Host name, default = trondheim.cs.washington.edu
-D [string]\tMySql Database name, default = PSRC_2000_data_quality_indicators
-A [string]\tMySql Archive database name, default = PSRC_2000_archived_dq_indicators
-U [string]\tMysql User name
-P [string]\tMysql Password
-r [string]\tRepository root, default = /projects/urbansim2/repository
-p [string]\tRepository path for indicator results, default = Website/projects/psrc/indicator_results
-u \t\tUpdate databases before running data quality indicators, default sql script = PSRC_collation_manager.sql in data quality indicator scripts directory
-t \t\tConvert .csv table to teX ready file, default perl script = /projects/urbansim7/scripts/private/cpeak/latex_table_formatter.pl
-v\t\tVerbose

Note: switches are case-sensitive.
";
	}
    
	print "===parse parameters/switches==========================================\n" if $prompt;
	my $dir = cwd();
	$working_path = $dir if ( !$working_path );
	print "working path: $working_path\n" if $verbose;
	$dq_script_dir = "/projects/urbansim7/scripts/public/data_prep/" if (!$dq_script_dir);
	print "data quality script directory: $dq_script_dir\n" if $verbose;
	$cvsroot = "/projects/urbansim2/repository" if (!$cvsroot);
	print "CVS root: $cvsroot\n" if $verbose;
	$repository_path = "Website/projects/psrc/indicator_results" if (!$repository_path);
	print "repository path: $repository_path\n" if $verbose;

	my $time = get_time("short");
	
	$log_file = "${time}.log" if ( !$log_file );
	print "log file: $log_file\n" if $verbose;

	if ( !$host ){
	    $host = "trondheim.cs.washington.edu";
	    print "Database host name unspecified, use $host instead\n" if $verbose;
	}	

	if ( !$db ){
	    $db = "PSRC_2000_data_quality_indicators";
	    print "Database name unspecified, use $db instead\n" if $verbose;
	}

	if ( !$archive_db ){
	    $archive_db = "PSRC_2000_archived_dq_indicators";
	    print "Archive database name unspecified, use $archive_db instead\n" if $verbose;
	}

	print "host=$host | db=$db | user=$user | passwd=$passwd\n" if $verbose;
	$db = {
		host	        => $host,
		db	        => $db,
		username	=> $user,
		password	=> $passwd,
	} ;
	
	@script_files = qw( 
		PSRC_collation_manager.sql
		);
	
	$tex_script = "/projects/urbansim7/scripts/private/cpeak/latex_table_formatter.pl";
	
}
