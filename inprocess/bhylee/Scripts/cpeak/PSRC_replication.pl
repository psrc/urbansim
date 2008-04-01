# This is a copy of the script running on the PSRC's computers dedicated to UrbanSim.
# It copies the tables listed in the get_arrays_of_databases subroutine
# onto the computer running the script.

#!/usr/bin/perl -w

use strict;
use DBI;

my $source_server = 'trondheim.cs.washington.edu';
my $source_username = 'urbansim';
my $source_password = 'UwUrbAnsIm';
my $dest_server = 'localhost';
my $dest_username = 'cpeak';
my $dest_password = '05.psrc.03';


my @databases = &get_arrays_of_databases();
my $overall_startime = time;
foreach my $dbase (@databases){
	eval{
		my $dbase_name = shift(@$dbase);
		my $dbh_source = DBI->connect("dbi:mysql:$dbase_name:$source_server", $source_username, $source_password);
		my $dbh_dest = DBI->connect("dbi:mysql:$dbase_name", $dest_username); #, $dest_password);
		print "\ndbase name: $dbase_name \n";
		foreach my $table (@$dbase) {
			#print "table: $table \t";
			my $startime = time;
			my $loctime = localtime(time);
			#print "localtime $loctime \n";
			&copy_table ($dbh_source, $dbh_dest, $table);
			my $endtime = time;
			my $elapsedtime = ($endtime - $startime)/60;
			print "table $table processed in $elapsedtime minutes. \n";
		}
	};
}
my $overall_endtime = time;
my $overall_elapsedtime = ($overall_endtime - $overall_startime )/60;
print "\nReplication completed. Total time: $overall_elapsedtime minutes. \n";
my %run_date = &get_date();
print "$run_date{Month}-$run_date{Day}-$run_date{Year} \n";

##############------------ Subroutines ---------------###################

sub copy_table { # main subroutine
	my ($dbh_source, $dbh_dest, $table) = @_;
	eval{
		&empty_table($dbh_dest, $table);
		my $field_names = &get_fields_from_table ($dbh_source, $table);
		&create_table_if_not_exists ($dbh_source, $dbh_dest, $table);
		my $qry_select = "SELECT * FROM $table";
		my $sth_select = $dbh_source->prepare($qry_select);
		$sth_select->execute();
		while (my $record_array = $sth_select->fetchrow_arrayref){
			&insert_into_local_table ($field_names, $dbh_dest, $table, $record_array) or die "insert_into_local_table call failed!!! \n";
		}
	};
	if ($@) {print "WARNING: an error occurred processing of table $table.  Table $table not replicated. \n\n"}
}

sub get_fields_from_table {
	my ($dbh_source, $table) = @_;
	my $qry_describe = "describe $table";
	my $sth_describe = $dbh_source->prepare($qry_describe);
	$sth_describe->execute();
	my @fields;
	my $i = 0;
	while (my @field_descriptor = $sth_describe ->fetchrow_array){
		$fields[$i] = $field_descriptor[0];
		$i = $i+1;
	}
	my $field_names = join ",", @fields;
	#print "\n \n$field_names \n \n";
	$field_names;
}

sub insert_into_local_table {
	my ($field_names, $dbh_dest, $table, $record_array) = @_;
	#print "field names: $field_names \n";
	my $values = &format_values_for_insert($record_array);
	my $qry_insert = "INSERT INTO $table ($field_names) VALUES ($values)";
	my $sth_insert = $dbh_dest->prepare($qry_insert);
	$sth_insert->execute() or die print "died on: $qry_insert \n \n";
}


sub format_values_for_insert {
	my ($value_array) = @_;
	foreach my $val (@$value_array) {
		if (! $val) {$val = "NULL"}
		if ($val =~ /[^0-9]/) { # If $val has any non-numeric characters
			$val =~ s/\"/s/g ; # get rid of double quotes within the $val
			$val = "\"$val\"";  # and enclose $val between double quotes.
		}
		if ($val eq "\"NULL\"") {$val = "NULL"}
	}
	my $values = join ",", @$value_array;
	$values;
}

sub get_field_names_and_types {
	my ($dbh_source, $table) = @_;
	my @field_names_and_types;
	my $qry_describe = "describe $table";
	my $sth_describe = $dbh_source->prepare($qry_describe);
	$sth_describe->execute();
	my $i = 0;
	while (my @field_descriptor = $sth_describe ->fetchrow_array){
		$field_names_and_types[$i] = " $field_descriptor[0] $field_descriptor[1]";
		$i = $i + 1;
	}
	my $field_names_and_types = join ",",@field_names_and_types;
	$field_names_and_types;
}

sub create_table_if_not_exists {
	my ($dbh_source, $dbh_dest, $table) = @_;
	my $field_names_and_types = &get_field_names_and_types($dbh_source, $table);
	my $qry_create_table = "CREATE TABLE IF NOT EXISTS $table ($field_names_and_types)";
	#print "$qry_create_table \n";
	my $sth_create_table = $dbh_dest->prepare($qry_create_table);
	$sth_create_table->execute();
}

sub empty_table {
	my ($dbh_dest, $table) = @_;
	my $qry_empty = "DROP TABLE $table";
	my $sth_empty = $dbh_dest->prepare($qry_empty);
	$sth_empty->execute();
}

sub get_arrays_of_databases { # The database and table names lists are constructed here.
	# Each array represents a database, and the first element of that array is the database name.
	# All other elements are the table names within that database.

	my @PSRC_parcels_kitsap = qw /PSRC_parcels_kitsap parcels/;
	push (my @databases, \@PSRC_parcels_kitsap);

	my @PSRC_parcels_king = qw /PSRC_parcels_king parcels/;
	push (@databases, \@PSRC_parcels_king);

	my @PSRC_parcels_pierce = qw /PSRC_parcels_pierce parcels/;
	push (@databases, \@PSRC_parcels_pierce);

	my @PSRC_parcels_snohomish = qw /PSRC_parcels_snohomish parcels/;
	push (@databases, \@PSRC_parcels_snohomish);

	my @PSRC_2000_baseyear= qw /PSRC_2000_baseyear gridcells jobs households/;
	push (@databases, \@PSRC_2000_baseyear);

	my @PSRC_2000_data_quality_indicators= qw /PSRC_2000_data_quality_indicators land_use_generic_reclass/;
	push (@databases, \@PSRC_2000_data_quality_indicators);

	@databases;
}

sub get_date {

####
# Get date information
my ($Seconds, $Minutes, $Hours, $DayInMonth, $Month, $ShortYear,
   $DayOfWeek, $DayOfYear, $IsDST);

($Seconds, $Minutes, $Hours, $DayInMonth, $Month, $ShortYear,
   $DayOfWeek, $DayOfYear, $IsDST) = localtime(time);

# Fix the year for post-Y2K
my $Year = $ShortYear + 1900;

# Fix the month and day for beginning count at 0
$Month = $Month + 1;
#$DayInMonth = $DayInMonth + 1;

my %date_time;
$date_time{Year} = $Year;
$date_time{Month} = $Month;
$date_time{Day} = $DayInMonth;

%date_time;
}