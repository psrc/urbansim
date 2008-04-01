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


# This script is used to generate transition_types table for baseyear database
# from development_event_history table
# 
# created by lmwang on 03/04

#########################
# Global variables
# $dbh
# %db
# 	host
# 	db
# 	user
# 	passwd

use lib qw(/projects/urbansim7/users/lmwang/cpan/lib/perl5/site_perl/5.8.3/i386-linux-thread-multi);
use DBI;
use Getopt::Long qw(:config no_ignore_case bundling);

$myName = "transition_types";

processSwitches();

$src_table = 'development_event_history';
$rst_table = 'transition_types';

%cal_fields = (
		  'RESIDENTIAL_UNITS'      => 'HOUSING_UNITS',
		  'COMMERCIAL_SQFT'        => 'COMMERCIAL_SQFT',
		  'INDUSTRIAL_SQFT'        => 'INDUSTRIAL_SQFT',
		  'GOVERNMENTAL_SQFT'      => 'GOVERNMENTAL_SQFT',
		  'RESIDENTIAL_IMPROVEMENT_VALUE'      => 'HOUSING_IMPROVEMENT_VALUE',
		  'COMMERCIAL_IMPROVEMENT_VALUE'       => 'COMMERCIAL_IMPROVEMENT_VALUE',
		  'INDUSTRIAL_IMPROVEMENT_VALUE'       => 'INDUSTRIAL_IMPROVEMENT_VALUE',
		  'GOVERNMENTAL_IMPROVEMENT_VALUE'     => 'GOVERNMENTAL_IMPROVEMENT_VALUE'
	       );
@id_fields = qw(
		STARTING_DEVELOPMENT_TYPE_ID
		ENDING_DEVELOPMENT_TYPE_ID
		);

do_work();

###########################
#
# Main subroutines
#

sub do_work {
	$dbh = db_conn();
	init_table() if (!$test);  #make sure src table exists; empty rst table if exists, quit if it doesn't

	$sth = build_sth();

	$pre_row = $cur_row = $sth->fetchrow_hashref;
	%rst_hash = ();
	%tmp_hash = (); #hash of array to store rows of the same id in hash for use of computing sd
	#init_array();

	while ($cur_row)
	{
	    if (!same_type()){
		compute_id(); #insert id into result hash %rst_hash
		compute_msd(); #compute mean and standard deviation and append them to %rst_hash

		insert_row();
		%tmp_hash = (); %rst_hash = ();
	    }

	    compute_mms(); #compute max,min,and sum
	    push_cur_row();
	    $pre_row = $cur_row;
	    $cur_row = $sth->fetchrow_hashref;	    
	}

	# insert the last transition record into $rst_table
	compute_id(); 
	compute_msd(); 
	insert_row();

	$sth->finish();
	$dbh->disconnect();
}

sub compute_id {
    foreach my $id (@id_fields){
	my $id_value = $pre_row->{$id};
	$rst_hash{$id} = $id_value;
    }
}


sub compute_msd {
    foreach my $field (keys %cal_fields){
	my $cal_field = $cal_fields{$field};
	#print $cal_field, @{$tmp_hash{$cal_field}}, "\n" if $verbose;
	my $length = @{$tmp_hash{$cal_field}};
	my $sum = $rst_hash{$cal_field . '_MEAN'};
	my $min = $rst_hash{$cal_field . '_MIN'};
	my $max = $rst_hash{$cal_field . '_MAX'};
	print $cal_field,": sum=",$sum," min=",$min," max=", $max, " with ",$length," events\n" if $verbose;

	$rst_hash{$cal_field . '_MEAN'} /= $length if $length;
	my $mean = $rst_hash{$cal_field . '_MEAN'};

	my $sums = 0; my $i = 0;
	foreach my $value (@{$tmp_hash{$cal_field}}) {
	    $sums += ($value - $mean) * ($value - $mean);
	    $i++;
	}
	#print $i," items iterated\n" if $verbose;
	$rst_hash{$cal_field . '_STANDARD_DEVIATION'} = sqrt($sums/$length) if $length;
    }
}    


sub compute_mms {
    foreach my $field (keys %cal_fields){
	my $cal_field = $cal_fields{$field};

	if (defined $cur_row->{$field} ) {
	    my $value = $cur_row->{$field};
	    $rst_hash{$cal_field .'_MAX'} = $value if (!defined $rst_hash{$cal_field .'_MAX'});	
	    $rst_hash{$cal_field .'_MIN'} = $value if (!defined $rst_hash{$cal_field .'_MIN'});

	    $rst_hash{$cal_field . '_MAX'} = $rst_hash{$cal_field . '_MAX'} > $value ? 
		$rst_hash{$cal_field . '_MAX'} : $value;
	    $rst_hash{$cal_field . '_MIN'} = $rst_hash{$cal_field . '_MIN'} < $value ? 
		$rst_hash{$cal_field . '_MIN'} : $value;

	    $rst_hash{$cal_field . '_MEAN'} += $value;
	}
    }
}    

sub push_cur_row {
    foreach my $field (keys %cal_fields){
	my $cal_field = $cal_fields{$field};
	if (defined $cur_row->{$field} ) {
	    #my $value = ( defined $cur_row->{$field} ) ? $cur_row->{$field} : 0;
	    push(@{$tmp_hash{$cal_field}}, $cur_row->{$field});
	}
    }
}

sub insert_row {
    my $_stm;
    $_stm = build_insert_stm();
    print "$_stm\n" if $verbose;
    execute_sql($_stm);
}

sub build_insert_stm {
    my $_stm = "insert into $rst_table ";
    my ($field_list,$value_list);
    while(($field,$value) = each(%rst_hash)) {
	if (defined $value) {
	    $field_list .= "$field,";
	    #my @exist = grep(/$field/,@id_fields);
	    #if (@exist == 1) { 
		#$value_list .= "'" . $value . "',";
	    #} else {
	    $value_list .= "$value,";
	    #}
	}
    }
    chop($field_list);
    chop($value_list);
    $_stm .= "($field_list) values ($value_list)";

    return $_stm;
}

sub init_table {
    die "Table $src_table doesn't exist!\n" if (!exist_table($src_table));

    if (exist_table($rst_table)) {
	if (prompt_truncate_table($rst_table)) {
	    execute_sql("drop table $rst_table;\n");
	} else {
	    die "Table $rst_table needs to be truncated.\n";
	}
    }
    create_rst_table();
}

sub create_rst_table {
    @fields = qw(
		 TRANSITION_ID int(11) auto_increment, primary key(TRANSITION_ID),
		 INCLUDE_IN_DEVELOPER_MODEL tinyint(1) default 1,
		 STARTING_DEVELOPMENT_TYPE_ID int(11),
		 ENDING_DEVELOPMENT_TYPE_ID int(11),
		 HOUSING_UNITS_MEAN double,
		 HOUSING_UNITS_STANDARD_DEVIATION double,
		 HOUSING_UNITS_MIN int(11),
		 HOUSING_UNITS_MAX int(11),
		 COMMERCIAL_SQFT_MEAN double,
		 COMMERCIAL_SQFT_STANDARD_DEVIATION double,
		 COMMERCIAL_SQFT_MIN int(11),
		 COMMERCIAL_SQFT_MAX int(11),
		 INDUSTRIAL_SQFT_MEAN double,
		 INDUSTRIAL_SQFT_STANDARD_DEVIATION double,
		 INDUSTRIAL_SQFT_MIN int(11),
		 INDUSTRIAL_SQFT_MAX int(11),
		 GOVERNMENTAL_SQFT_MEAN double,
		 GOVERNMENTAL_SQFT_STANDARD_DEVIATION double,
		 GOVERNMENTAL_SQFT_MIN int(11),
		 GOVERNMENTAL_SQFT_MAX int(11),
		 HOUSING_IMPROVEMENT_VALUE_MEAN double,
		 HOUSING_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
		 HOUSING_IMPROVEMENT_VALUE_MIN int(11),
		 HOUSING_IMPROVEMENT_VALUE_MAX int(11),
		 COMMERCIAL_IMPROVEMENT_VALUE_MEAN double,
		 COMMERCIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
		 COMMERCIAL_IMPROVEMENT_VALUE_MIN int(11),
		 COMMERCIAL_IMPROVEMENT_VALUE_MAX int(11),
		 INDUSTRIAL_IMPROVEMENT_VALUE_MEAN double,
		 INDUSTRIAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
		 INDUSTRIAL_IMPROVEMENT_VALUE_MIN int(11),
		 INDUSTRIAL_IMPROVEMENT_VALUE_MAX int(11),
		 GOVERNMENTAL_IMPROVEMENT_VALUE_MEAN double,
		 GOVERNMENTAL_IMPROVEMENT_VALUE_STANDARD_DEVIATION double,
		 GOVERNMENTAL_IMPROVEMENT_VALUE_MIN int(11),
		 GOVERNMENTAL_IMPROVEMENT_VALUE_MAX int(11),
		 YEARS_TO_BUILD int(11)	default 1	 
		 );
    $fields = join(' ', @fields);
    $stm = 'create table ' . $rst_table;
    $stm .= "($fields)";
    print $stm if $verbose;
    execute_sql($stm);
}


sub same_type {
    my $same_id = 0;
    my $num_id_field = @id_fields;
    foreach my $id_field (@id_fields) {
	$same_id++ if ($pre_row->{$id_field} == $cur_row->{$id_field});
    }
    #print "same_id:$same_id = num_id:$num_id_field same?" . ($same_id == $num_id_field) ."\n"; 
    return ($same_id == $num_id_field);
}


sub build_sth {
    my $_stm = "select * from $src_table order by";
    foreach my $id (@id_fields){
	$_stm .= " $id,";
    }
    chop($_stm);

    print $_stm, "\n" if $verbose;

    my $_sth = $dbh->prepare($_stm)
	or die "failed to prepare statement $_stm\n";
    $_sth->execute()
	or die "couldn't execute statement: " . $_sth->errstr;
    
    return $_sth;
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

sub prompt_truncate_table {
    my $table = shift;
#    print "Table $table exists, is it OK to empty it?[y/n]";
#    my $answer = <STDIN>;
#    chomp($answer);
#    if ("\L$answer" eq 'y') {
	return 1;
#    } else {
#	return 0;
#    }
}

sub execute_sql {
	my $_stm = shift;
	my $_sth;
	
	if ("\L$_stm" =~ /^select/) {

		$_sth = $dbh->prepare($_stm) 
			or die "failed to prepare statement: $_stm. $_sth->errstr \n"; 
		$_sth->execute() 
			or die "failed to execute statement: $_stm. $_sth->errstr \n";
		
	}  elsif ("\L$_stm" =~ /[a-z]/) {	
		my $rv=$dbh->do($_stm) 
			or die "failed to execute statement: $_stm. ". DBI->errstr;
	}
}

sub db_conn{
	my ($DB_conn,$dbh);
	my ($host,$DB,$user,$passwd) = 
	    ($db{'host'},$db{'db'},$db{'user'},$db{'password'});
	$DB_conn = "DBI:mysql:database=$DB:host=$host";
	print "connecting to database $DB at $host\n" if $verbose;
	$dbh = DBI->connect($DB_conn,$user,$passwd) 
	  or die "failed to open database connection " . DBI->errstr;	
	
	return $dbh;

}

sub processSwitches {
	my $result;
	my ($host,$db,$user,$passwd);
	
	
	$result = &GetOptions(
		"H:s"	=> \$host,
		"D:s"	=> \$db,
		"U:s"	=> \$user,
		"P:s"	=> \$passwd,
		"h"	=> \$help,
		"v"	=> \$verbose,
	);

	if (!$result) {
		die "Error in input. Use -h for help.\n";
	}

	if ($help) {
			die
"Usage: perl $myName.pl [switches]
-H [string]\tMySql host name, Default = Localhost
-D [string]\tMySql database name
-U [string]\tMysql user name
-P [string]\tMysql password
-v \t\tVerbose
-h\t\tThis help

Note: switches are case-sensitive.
";
	}
	

	print "host=$host | db=$db | user=$user | passwd=$passwd\n" if $verbose;
	%db = (
		host	 => $host,
		db	 => $db,
		user	 => $user,
		password => $passwd,
	);
	
}
