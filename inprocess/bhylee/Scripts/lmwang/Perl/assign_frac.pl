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


# This script is used to assign fraction residential units and built 
# sqft to gridcells based on Monte Carlo process
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
# $table 

use lib qw(/projects/urbansim7/users/lmwang/cpan/lib/perl5/site_perl/5.6.1/i386-linux);
use DBI;
use Getopt::Long qw(:config no_ignore_case bundling);

$myName = "assign_frac";

processSwitches();

# @frac_fields = qw(
# COMMERCIAL_SQFT_ADDED
# COMMERCIAL_IMPROVEMENT_VALUE_ADDED
# INDUSTRIAL_SQFT_ADDED
# INDUSTRIAL_IMPROVEMENT_VALUE_ADDED
# GOVERNMENTAL_SQFT_ADDED
# GOVERNMENTAL_IMPROVEMENT_VALUE_ADDED
# RESIDENTIAL_UNITS_ADDED
# RESIDENTIAL_IMPROVEMENT_VALUE_ADDED
# 		  );

%frac_fields = qw(
		  COMMERCIAL_SQFT_ADDED      => COMMERCIAL_IMPROVEMENT_VALUE_ADDED,
		  INDUSTRIAL_SQFT_ADDED      => INDUSTRIAL_IMPROVEMENT_VALUE_ADDED,
		  GOVERNMENTAL_SQFT_ADDED    => GOVERNMENTAL_IMPROVEMENT_VALUE_ADDED,
		  RESIDENTIAL_UNITS_ADDED    => RESIDENTIAL_IMPROVEMENT_VALUE_ADDED
		  );
@id_fields = qw(
		PARCEL_ID
		COUNTY
		YEAR_BUILT
		);

#if ($test) {
#	do_tests();
#}
#else {
do_work();
#}

###########################
#
# Main subroutines
#

sub do_work {
	$dbh = db_conn();
	$sth = build_sth();
	
	%pooled_impv = (); 

	$res_table = $db{'table_name'} . "_no_frac";
	init_table();  #drop table if exists, and then create it
	$pre_row = $cur_row = $sth->fetchrow_hashref;
	%r = propose_prob();
	#init_array();
	while ($cur_row){
	    $res_row = $cur_row;
	    if (!same_parcel()){		
		%r = propose_prob();
		assign_frac();
		insert_row();
		%pooled_impv = (); 
	    }

	    $pre_row = $cur_row;
	    $cur_row = $sth->fetchrow_hashref;	    
	}

	$sth->finish();
	$dbh->disconnect();
}

sub assign_frac {
    foreach my $unit_field (keys %frac_fields) {
	my $impv_field = $frac_fields{$unit_field};

	print "----for field $frac_field:\n" if $verbose;
	#first assign improvement_value field then unit/sqft field
	#$res_row stores the result rows
	my $cur_value = $cur_row->{$impv_field};
	my $odds =$r{$impv_field};
	my $decimal = split_decimal($cur_value);

	if ($odds <= $decimal) {
	    $res_row->{$impv_field} = split_whole($cur_value) + 1;
	} else {
	    $res_row->{$impv_field} = split_whole($cur_value);
	}

	my $cur_value = $cur_row->{$unit_field};
	my $odds =$r{$unit_field};
	my $decimal = split_decimal($cur_value);
	
	if ($odds <= $decimal) {
	    $res_row->{$unit_field} = split_whole($cur_value) + 1;
	    $res_row->{$impv_field} += $pooled_impv{$impv_field};
	} else {
	    $res_row->{$unit_field} = split_whole($cur_value);
	}

	if ($res_row->{$unit_field} == 0) {
	    $pooled_impv{$impv_field} += $cur_row->{$impv_field};
	    $cur_row->{$impv_field} = 0;
	}

	$r{$frac_field} -= split_decimal($cur_value);

	foreach my $field (keys %r) {
	    $r{$field} += 1 if ($r{$field}<0);
	}

	$res_value = $res_row->{$frac_field} if $verbose;   # for diagnostic and debug purpose only
	print "    init odds= $odds |frac=$decimal |adj odds ${r{$frac_field}}\n" if $verbose;
	print "    assign value $cur_value to $res_value\n" if $verbose; 

    }
}

sub adjust_prob {
    my $field = shift;
    my $cur_value = $cur_row->{$field};
    my $decimal = split_decimal($cur_value);
    my $r = $r{$field};
    print "    init odds=$r | ";
    $r{$field} += $decimal;
    print "adjusted odds =" . $r{$field} . "\n";
}

sub insert_row {
    my $_stm;
    $_stm = build_insert_stm();
    print "$_stm\n" if $verbose;
    execute_sql($_stm);
}

sub build_insert_stm {
    my $_stm = "insert into $res_table ";
    my ($field_list,$value_list);
    while(($field,$value) = each(%$res_row)) {
	if (defined $value) {
	    $field_list .= "$field,";
	    my @exist = grep(/$field/,@id_fields);
	    if (@exist == 1) { 
		$value_list .= "'" . $value . "',";
	    } else {
		$value_list .= "$value,";
	    }
	}
    }
    chop($field_list);
    chop($value_list);
    $_stm .= "($field_list) values ($value_list)";

    return $_stm;
}

sub init_table {
    my $_stm = "";
    $_stm = "drop table if exists $res_table;\n";
    execute_sql($_stm);
    $_stm = "create table $res_table select * from $db{'table_name'} where 1<>1;\n";
    execute_sql($_stm);

    $_stm = "alter table $res_table ";
    foreach my $unit_field (keys %frac_fields) {
	$_stm .= "modify $unit_field int,";
	my $impv_field = $frac_fields{$unit_field};
	$_stm .= "modify $impv_field int,";
    }
    chop($_stm);  #chop the last ","

    print "$_stm\n" if $verbose;

    execute_sql($_stm);
}

sub same_parcel {
    my $same_id = 0;
    my $num_id_field = @id_fields;
    foreach my $id_field (@id_fields) {
	$same_id++ if ($pre_row->{$id_field} == $cur_row->{$id_field});
    }
    #print "same_id:$same_id = num_id:$num_id_field same?" . ($same_id == $num_id_field) ."\n"; 
    return ($same_id == $num_id_field);
}

sub propose_prob {
    my %prob;
    srand;
    foreach my $unit_field (keys %frac_fields) {
	$prob{$unit_field} = rand 1;
	my $impv_field = $frac_fields{$unit_field};	
	$prob{$impv_field} = rand 1;
    }
    return %prob;
}

sub build_sth {
    my $_stm = "select * from $db{'table_name'} order by parcel_id,county,year_built"; 
    my $_sth = $dbh->prepare($_stm)
	or die "failed to prepare statement $_stm\n";
    $_sth->execute()
	or die "couldn't execute statement: " . $_sth->errstr;
    
    return $_sth;
}

sub split_whole {
    my $decvar = shift;
    my ($_whole, $_decimal) = split(/\./,$decvar);

    return $_whole;
}

sub split_decimal {
    my $decvar = shift;
    my ($_whole, $_decimal) = split(/\./,$decvar);
    $_decimal = $decvar - $_whole;

    return $_decimal;
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
	## should check to make sure $_command is a valid sql query 
	## ("\L$_command" =~ /^drop/ || "\L$_command" =~ /^delete/ || "\L$_command" =~ /^update/ || 
	## "\L$_command" =~ /^create/ || "\L$_command" =~ /^insert/){
	
		my $rv=$dbh->do($_stm) 
			or die "failed to execute statement: $_stm. ". DBI->errstr;
	}

}

sub db_conn{
	my ($DB_conn,$dbh);
	my ($host,$DB,$user,$passwd) = 
	    ($db{'host'},$db{'db'},$db{'user'},$db{'password'});
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
		"H:s"	=> \$host,
		"D:s"	=> \$db,
		"T:s"	=> \$table_name,
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
-T [string]\tTable name
-v \t\tVerbose
-h\t\tThis help

Note: switches are case-sensitive.
";
	}
	

	print "host=$host | db=$db | table=$table_name | user=$user | passwd=$passwd\n" if $verbose;
	%db = (
		host	 => $host,
		db	 => $db,
		user	 => $user,
		password => $passwd,
	        table_name => $table_name,
	);
	
}
