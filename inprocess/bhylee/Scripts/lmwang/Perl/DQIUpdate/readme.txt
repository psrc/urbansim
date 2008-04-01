DQIUpdate.pl and a collection of sql scripts and perl scripts update data quality indicators for PSRC database, including:
  -running sql script PSRC_collation_manager.sql (and its sub-scripts) in data quality indicator scripts directory to update database before indicator runs, activated with switch -u;
  -checking out dq indicators from CVS repository, backing up dq indicators to archived db, updating dq indicators, and then checking in updated dq indicators;
  -converting .csv table to TeX ready file using script /projects/urbansim7/scripts/private/cpeak/latex_table_formatter.pl, activated with switch -t;  

1. Script switches
DQIUpdate.pl is configurable with a bunch of switches. To see a list of command line switches available with DQIUpdate.pl run
perl DQIUpdate.pl -h

Usage: perl DQIUpdate.pl [switches]
-h              This help
-w [string]     Working path, default = cwd (current working directory)
-d [string]     Data quality indicator scripts directory, default = /projects/urbansim7/scripts/public/data_prep/
-l [string]     Log filename, default = current-time.log in working path specified by -w switch
-H [string]     MySql Host name, default = trondheim.cs.washington.edu
-D [string]     MySql Database name, default = PSRC_2000_data_quality_indicators
-A [string]     MySql Archive database name, default = PSRC_2000_archived_dq_indicators
-U [string]     Mysql User name
-P [string]     Mysql Password
-r [string]     Repository root, default = /projects/urbansim2/repository
-p [string]     Repository path for indicator results, default = Website/projects/psrc/indicator_results
-u              Update databases before running data quality indicators, default sql script = PSRC_collation_manager.sql in data quality indicator scripts directory
-t              Convert .csv table to teX ready file, default perl script = /projects/urbansim7/scripts/private/cpeak/latex_table_formatter.pl
-v              Verbose

A sample run with combined paramters

perl DQIUpdate.pl -w /projects/urbansim7/users/cpeak/DataQuality/exported_indicators/ -U uxxxxxxm -P Uxxxxxxxxm -u -t -v

(Keep the directory divider "/" at the end of working path (after -w) and data quality indicator scripts directory (after -d).)

2. Configuration and required tables
This script uses a table named archived_short_table_name_mapping in archive database to convert data quality name to short archived table name (because some archived table name exceeds MySQL table name limitation of 64 characters). 
If a record exists for a data quality indicator in this table, the "short_name" of that indicator will be used to create archived table for it. Otherwise, the (full) data quality indicator name will be used.

3. Required perl Modules: 
DBI
mysql-DBD
