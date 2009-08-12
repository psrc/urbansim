##This script creates HouseholdsByZone and JobsByZone tables based on 
##jobs and households in output database, GridCells and GridCellsFraction tables from baseyear database.

#!/usr/local/bin/perl -w
$DEBUG=1;

use lib "/homes/june/lmwang/pm/lib/perl5/site_perl/5.6.1/i386-linux";
use DBI;

my $mysql_host='trondheim.cs.washington.edu';
my $mysql_output_db='WFRC_1997_output_jpf_2030_0_va'; 
my $mysql_user='urbansim';
my $mysql_passwd='UwUrbAnsIm';
my $mysql_frac_table ='tmp_gridcell_fractions_in_zones';
my $mysql_gridcell ='tmp_gridcells';
my $mysql_changes_table ='tmp_households_by_gridcells';
my $id ='HOUSEHOLD_ID';
my $mysql_zone_table ='households_by_zone';

#print "Please specify the names for necessary tables.\nAll tables have to be in the same database.\n";

#print "Input the name of GridCellsFraction table: ";
#$mysql_frac_table=<STDIN>;
#chomp $mysql_frac_table;

#print "Input the name of GridCells table: ";
#$mysql_gridcell=<STDIN>;
#chomp $mysql_gridcell;

#print "Input the name of Changes table(HouseholdsChanges/JobsChanges): ";
#$mysql_changes_table=<STDIN>;
#chomp $mysql_changes_table;

#if ($mysql_changes_table eq 'JobsChanges') {
#   $id='JOB_ID';
#   $mysql_zone_table='JobsByZoneb';
#} else { 
#   $id='HOUSEHOLD_ID'; 
#   $mysql_zone_table='HouseholdsByZoneb';
#}

#print "Input the log file name: ";
if ($DEBUG eq 0){
$log_file='households_by_zone.log'; #<STDIN>;
chomp $log_file;
open(LOG,">$log_file") || die "Couldn't open $log_file\n";
print LOG "Create $mysql_zone_table from $mysql_changes_table and $mysql_frac_table.\n\n";

my ($sec,$min,$hour)=localtime[0,1,2];
print LOG "start time: $hour:$min:$sec.\n";
}else {
print "Create $mysql_zone_table from $mysql_changes_table and $mysql_frac_table.\n\n";
}
my $data_source="DBI:mysql:database=" . $mysql_output_db . ":host=" . $mysql_host;
my $dbh=DBI->connect($data_source,$mysql_user,$mysql_passwd)
   or die "failed to open connection" . DBI->errstr;

my $rv=$dbh->do("CREATE TABLE $mysql_zone_table (YEAR smallint(6), $id int(11),GRID_ID int(11),ZONE_ID int(11))") or
   die "failed to create table: " . DBI->errstr;

my ($mysql_id,$mysql_is_frac,$mysql_frac,$mysql_insert);
my ($sth_id,$sth_is_frac,$sth_frac);
my (@data_id,@data_is_frac,@data_frac);

$mysql_id="SELECT YEAR,$id,gc.GRID_ID,gc.ZONE_ID FROM $mysql_changes_table changes INNER JOIN $mysql_gridcell gc ON changes.GRID_ID=gc.GRID_ID";
$sth_id=$dbh->prepare($mysql_id)
   or die "failed to prepare statement.\n";
$sth_id->execute() or 
   die "couldn't execute statement: " . $sth_id->errstr;

while (@data_id=$sth_id->fetchrow()) {
if ($DEBUG eq 0){
   print LOG "data_id:$data_id[0]\t$data_id[1]\t$data_id[2]\t$data_id[3]\n";   
}else{
   print "data_id:$data_id[0]\t$data_id[1]\t$data_id[2]\t$data_id[3]\n";   
}
   $mysql_is_frac="SELECT COUNT(*) FROM $mysql_frac_table WHERE GRID_ID=$data_id[2]";
   $sth_is_frac=$dbh->prepare($mysql_is_frac) or die "";
   $sth_is_frac->execute() or die "";
   @data_is_frac=$sth_is_frac->fetchrow();

   if ($data_is_frac[0]==0) {
     $mysql_insert="INSERT INTO $mysql_zone_table VALUES ($data_id[0],$data_id[1],$data_id[2],$data_id[3])";
     $rv=$dbh->do($mysql_insert) or die "";   
if ($DEBUG eq 0) {
     print LOG ">>inserted:$data_id[0]\t$data_id[1]\t$data_id[2]\t$data_id[3]\n"; }else {
     print ">>inserted:$data_id[0]\t$data_id[1]\t$data_id[2]\t$data_id[3]\n"; 
     }
   } else 
   {

   $mysql_frac="SELECT GRID_ID,ZONE_ID,FRACTION FROM $mysql_frac_table WHERE GRID_ID=" . $data_id[2];

   $sth_frac=$dbh->prepare($mysql_frac)
      or die "failed to prepare statement";
   $sth_frac->execute() 
      or die "failed to execute query.\n";

   srand();
   $r=rand 1; 
if ($DEBUG eq 0){
   print LOG "---begin fraction process---\n";
}else {
   print "---begin fraction process---\n";
}
   while (@data_frac=$sth_frac->fetchrow()) {

if ($DEBUG eq 0){
     print LOG "data_frac:$data_frac[0]\t$data_frac[1]\t$data_frac[2]\n";

     print LOG "fraction:$data_frac[2]\t random: $r \n";

}else {
     print "data_frac:$data_frac[0]\t$data_frac[1]\t$data_frac[2]\n";

     print "fraction:$data_frac[2]\t random: $r \n";
}
     if ($r<$data_frac[2]) {
        last;
     } else {$r=$r-$data_frac[2];}

     }

     $mysql_insert="INSERT INTO $mysql_zone_table VALUES ($data_id[0],$data_id[1],$data_id[2],$data_frac[1])";
     #print "$mysql_insert\n";
     $rv=$dbh->do($mysql_insert) or die "";

if ($DEBUG eq 0){
     print LOG ">>inserted:$data_id[0]\t$data_id[1]\t$data_id[2]\t$data_frac[1]\n";
     print LOG "---end fraction process--\n\n" 
}else {
     print ">>inserted:$data_id[0]\t$data_id[1]\t$data_id[2]\t$data_frac[1]\n";
     print "---end fraction process--\n\n" 
}
   }
}   
$sth_frac->finish;
$sth_is_frac->finish;
$sth_id->finish;

$dbh->disconnect();

($sec,$min,$hour)=localtime[0,1,2];
print "end time: $hour:$min:$sec.\n";

exit 0;

