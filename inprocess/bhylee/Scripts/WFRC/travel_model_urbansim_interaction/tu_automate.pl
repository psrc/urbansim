#!/usr/bin/perl
#
# Perl script that reads parameter file automating travel model urbansim interaction:
#	imports data from travel model to urbansim,
#	formats data from travel model,
#	creates urbansim parameter file as specified in script parameter file, and run urbansim,
#	transforms urbansim contiuation data from output database to scenario database,
#	creates urbansim indicators table,
#	creates gis data tables,
#	format data for travel model,
#	exports urbansim output table to travel model.
#
# Author: Liming Wang (lmwang AT u.washington.edu)
#
# This script is presented AS IS, with no responsibility
# stated or implied for harm caused by the use or lack of use
# of this script, nor for any functionality or lack thereof.
# 
# TODO add function to transfer urbansim baseyear data to travel model;
# TODO create database, such as scenario database if not already existing;
# TODO enable the script to run when output database are different over year.
# 
# v0.7 added time stamp when prompting
# v0.6 rewrote tests
# v0.5 fixed problems when calling urbansim.bat
# v0.4 fixed bug of exporting data from urbansim to travel model
# v0.3 added default parameter settings in code to simplify configuration of parameter file
# v0.2 cleaned code, added tests
# v0.1 first working version

use Cwd;
use DBI;
use XML::DOM;
use Getopt::Long;
use Win32;

# GLOBAL VARIABLES:
# $xml_file
# $prompt
# $verbose
# $test
#
# $base_year			urbansim baseyear
# $year0			start year per urbansim run
# $year1			end year per urbansim run
# $parameters_root		script xml parameter root
# $time				current time stamp
#
# %databases
# 	%baseyear_db
# 		host,db,username,password
# 	%scenario_db
# 		host,db,username,password
# 	%output_db
# 		host,db,username,password

# 
# %directories
# 	urbansim-directory
# 	urbansim-parameter-file
# 	travel-model-directory
# 	data-to-urbansim-directory
# 	data-from-urbansim-directory
# 	travel-model-batch-file
#	
# $DEBUG = 0;

$myName = "tu_automate";

get_time();

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

	open_xml_file();
	my @years=get_all_years($parameters_root->getElementsByTagName("run")->item(0));

	my $num_years=scalar(@years);

	for (my $i=0;$i<$num_years;$i++){
		$year0 = $years[$i];
		if ($i == ($num_years-1)) {
			$year1 = @years[$i]
		}
		else {
			$year1 = @years[$i+1]; 
		}
		
		#find the node that contain $year
		my $run_node = $parameters_root->getElementsByTagName("run")->item(0);
		my $year_node = get_year_node($run_node,$year0);
		
		if ($prompt) {print "\n==${time} cycle begins for starting year $year0 and end year $year1==\n";}

		#extract parameters
		if ($prompt) {print "#envrionment variables#\n";}
		parse_directory_setting();
		parse_dataset_setting();
		
		if ($prompt) {print "\n#run section#\n";}	
		do_run($year_node,$i,$num_years);

		if ($prompt) {print "\n==${time} cycle finishes for starting year $year0 and end year $year1==\n\n";}		
	}
}

sub open_xml_file {

	if (!(-e $xml_file)) {
		print "Travel model UrbanSim automation parameter file $xml_file not found\n";
		exit(0);
	}

	my $parser = new XML::DOM::Parser;
	my $doc = $parser->parsefile ($xml_file);
	$parameters_root = $doc->getDocumentElement;	
}

sub do_run{	
	my ($_year_node,$i,$num_years) = @_;
	my $t;
	
	DEFAULT:
	@run = (
		[
#		 { 'run-travel-model' => ''},
#		 { 'exchange-data' =>"from-travel-model-to-urbansim" },
#		 { 'format-data' => "format-data-from-travel-model"},
		 { 'run-urbansim' => '' },
		 { 'format-data' => "format-data-for-travel-model"},
		 { 'exchange-data' => "from-urbansim-to-travel-model"}
		 ],
		[
		 { 'run-travel-model' => ''},
		 { 'exchange-data' => "from-travel-model-to-urbansim"},
		 { 'format-data' => "format-data-from-travel-model"},
		 { 'format-data' => "output-to-continuation"},
		 { 'run-urbansim' => ''},
		 { 'format-data' => "format-data-for-travel-model"},
		 { 'exchange-data' => "from-urbansim-to-travel-model"}
		],
		[
		 { 'run-travel-model' => ''},
		 { 'exchange-data' => "from-travel-model-to-urbansim"},
		 { 'format-data' => "format-data-from-travel-model"},
		 { 'format-data' => "output-to-continuation"},
		 { 'run-urbansim' => ''},
		 { 'format-data' => "create-indicators"},
		 { 'format-data' => "create-gis-data" },
		 { 'format-data' => "format-data-for-travel-model"},
		 { 'exchange-data' => "from-urbansim-to-travel-model"}
		],
		[
		 { 'run-travel-model'=>''}
		],
		[
		 { 'run-urbansim'=>"transfer-baseyear-data-to-travel-model"},  #transfer-baseyear-data-to-travel, not implemented yet
		 { 'format-data'=>"format-baseyear-data-for-travel-model"},
		 { 'exchange-data'=>"from-urbansim-to-travel-model"},
		 { 'run-travel-model'=>''}
		]
		
	);
	
	if (!($_year_node->hasChildNodes)) {
		if ($verbose) {print "    Couldn't find action definition node, using DEFAULT setting\n";}
	}else{
		my %run_p = ();
		foreach my $child($_year_node->getChildNodes){
			next if ($child->getNodeType != ELEMENT_NODE); 
			my $child_name = $child->getNodeName;
			 $run_p{$child_name} = $child;
		}
	}
	
	#switch case No. of year for the order of running
	if ($i==0) {$t = 0;}
	elsif ($i>0 && $i<$num_years-2) {$t = 1;}
	elsif ($i==$num_years-2) {$t = 2;}
	elsif ($i==$num_years-1) {$t = 3;}
	
	my $actions = $run[$t];

	foreach my $action (@$actions) {
		my ($func,$para) = each %$action;
		if ($func eq "run-urbansim"){
			run_urbansim($run_p{$func});
		}
		#elsif ($func eq "run-urbansim-indicators"){}
		elsif ($func eq "run-travel-model"){
			run_travel_model();
		}
		elsif ($func eq "exchange-data"){
			exchange_data($para);
		}
		elsif ($func eq "format-data"){
			format_data($para);
		}
	}
}

sub run_urbansim{
	#
	# $ip_		interaction parameter nodes
	# $up_		urbansim parameter node
	# 
	#
	my $ip_node = shift;
	if ($prompt) {print "--${time} run urbansim\n"; }

	#if ($auto_create_urbansim_parameter_file eq "true") {
	update_urbansim_parameter_file($ip_node);
	#}
	#
	#keep current working directory
	
	my $dir = cwd();
	
	#run urbansim using the parameter file created
	chdir($directories{'urbansim-directory'})
	  or die "chdir to " . $directories{'urbansim-directory'} ." failed: $!\n\n";
  	my $urbansim_parameter_file = $directories{'urbansim-parameter-file'};
	$urbansim_parameter_file = Win32::GetShortPathName($urbansim_parameter_file);
	system("urbansim.bat", "$urbansim_parameter_file");

	chdir($dir)
	  or die "change to $dir failed: $!\n\n";
}		


			
sub run_travel_model{
	#keep current working directory
	
	my $dir = cwd();
	chdir($directories{'travel-model-directory'})
	  or die "chdir to travel model directory " . $directories{'travel-model-directory'} . "failed: $!\n\n";
	
	if ($prompt) {print "--${time} run travel_model...\n"; }

	my $status = system($directories{'travel-model-batch-file'});
	die "--travel_model failed, exited with $?, quit running...\n" if ($status != 0);

	chdir($dir)
	  or die "chdir to $dir failed: $!\n\n";
}

sub parse_exchange_data_setting{
	DEFAULT:
	my %exchanges = (
	'from-travel-model-to-urbansim' => {'AccessLogsum' => "
					FROM_ZONE_ID int,
					TO_ZONE_ID int,
					LOGSUM0 double,
					LOGSUM1 double,
					LOGSUM2 double
					",						
					    'HighwayTimes' => "
					FROM_ZONE_ID int, 
					TO_ZONE_ID int, 
					HWYTIME double
					 "
					    },
	  
	'from-urbansim-to-travel-model' =>  {'HHdistrib_joint_inclohi' => "",
					     'SEdata' => ""
					     },
	);

	my $_exchg_node = $parameters_root->getElementsByTagName("exchange-data")->item(0);
	
	if (!(defined $_exchg_node)) {
		if ($verbose) {print "    Couldn't find exchange-data section in parameter file, using DEFAULT setting\n";}
		return %exchanges;	
		
		#apply default setting
	}
	
	if(!($_exchg_node->hasChildNodes)) {
		if ($verbose) {print "    Couldn't find definition of exchange-data section in parameter file, using DEFAULT setting\n";}
		return %exchanges;	
	}
	
	foreach my $_from_to_node ($_exchg_node->getChildNodes) {
		next if ($_from_to_node->getNodeType != ELEMENT_NODE);
		my $_from_to = $_from_to_node->getNodeName;
		if (!($_from_to_node->hasChildNodes)){
			if ($verbose) {print "    Couldn't find <table> tag in exchange-data section, using DEFAULT setting\n";}
			return %exchanges;
		}
		
		foreach my $_table_node ($_from_to_node->getChildNodes) {
			next if ($_table_node->getNodeType != ELEMENT_NODE);
			my $_table_name = $_table_node->getAttribute("name");
			my $_fields_def = $_table_node->getAttribute("fields-defintion");
			
			$exchanges{$_from_to}{$_table_name} = $_fields_def,
		}
	}

	return %exchanges;
}
	
sub exchange_data{
	my $ip_node = shift;
	my $from_to;
	
	#Test if ip_node
	#	  i) is not a node,
	#then $from_to = $ip_node use
	my $ch= ();
	eval{$ch = $ip_node->hasChildNodes;};
	if ($@) {
		$from_to = $ip_node;
	}
	elsif ($ch) {
		foreach my $child ($ip_node->getChildNodes) {
			next if ($child->getNodeType != ELEMENT_NODE);
			$from_to = $child->getNodeName;
		}
	}
	elsif (defined $ip_node->getAttributes) {
		$from_to = $ip_node->getAttribute("value");
	}
	
	if ($prompt) {print "--${time} exchange data $from_to \n";}
	
	my %exchanges = parse_exchange_data_setting();
	my $tables = $exchanges{$from_to};
	my ($dbh,$table_name,$fields_def,$exchange_file) = ();
	if ($from_to eq "from-travel-model-to-urbansim") {
		
		my $dbh = db_conn($databases{'scenario_db'});
		foreach	my $table_name (keys %$tables) {			
			$fields_def = $tables->{$table_name};
			
			my $data_to_urbansim_directory = $directories{'data-to-urbansim-directory'};
			opendir(DIR, "$data_to_urbansim_directory") ||
			  die "   Couldn't open directory $data_to_urbansim_directory\n\n";
			
			foreach my $entry (readdir DIR) {
				if ("\L$entry" =~ /\L$table_name/){
					$exchange_file = $entry;
					last;
				}
			}
			
			closedir(DIR);
			if (!(defined $exchange_file)) {
				die "Couldn't find file for importing to $table_name\n\n";
			}
			
			$exchange_file = $data_to_urbansim_directory . $exchange_file;
			
			if ($prompt) {print "    ${time} improting table $table_name...\n";}
			if ($prompt) { print "    from file $exchange_file\n";}
			
			$rv=$dbh->do("drop table if exists $table_name") 
				or die "failed to drop table $table_name " . DBI->errstr . "\n\n";
				
			my $stm = "create table " . $table_name . " (" . $fields_def . ")";
			$rv=$dbh->do($stm) 
				or die "failed to create table $table_name " . DBI->errstr . "\n\n";
						
			read_file_to_table($exchange_file,$dbh,$table_name);
						
			if ($prompt) {print "    ${time} finished improting table $table_name\n";}
		}
		$dbh->disconnect;
	}elsif ($from_to eq "from-urbansim-to-travel-model") {
		my $dbh = db_conn($databases{'output_db'});
		foreach	my $table_name (keys %$tables) {
			$fields_def = $tables->{$table_name};  #not used when porting table to file

			my $data_from_urbansim_directory = $directories{'data-from-urbansim-directory'};
			#export data from urbansim to travel model directory of cycle end year
			#$data_from_urbansim_directory =~ s/$year0/$year1/;
			#$data_from_urbansim_directory = $data_from_urbansim_directory;
			my $exchange_file = $data_from_urbansim_directory . $table_name . ".dat";
			
			if ($prompt) {print "    ${time} exporting table $table_name\n";}
			if ($prompt) {print "    to file $exchange_file\n";}
			
			export_table_to_file ($dbh, $table_name, $exchange_file, $year1);
		}
		$dbh->disconnect;
	}
		
}

sub parse_format_data_setting{
	DEFAULT:
	my %scripts = (
		'format-data-from-travel-model' =>
			"./sql_scripts/format_data_from_travel_model.sql",
		'format-data-for-travel-model'  =>
			"./sql_scripts/format_data_for_travel_model.sql",
		'create-indicators' =>
			"./sql_scripts/urbansim_indicators.sql",
		'create-gis-data' =>
			"./sql_scripts/output_data_to_grid_zone.sql",
		'output-to-continuation' =>
			"./sql_scripts/output_to_continuation.sql",
	);
	
	my $_t1_node = $parameters_root->getElementsByTagName("format-data")->item(0);
	if (!(defined $_t1_node)) {
		if ($verbose) {print "    Couldn't find format-data section in parameter file, using DEFAULT setting\n";}
		return %scripts;
	}
	if (!($_t1_node->hasChildNodes)) {
		if ($verbose) {print "    Couldn't find format definition tag in format-data section, using DEFAULT setting\n";}
		return %scripts;
	}

	foreach my $child ($_t1_node->getChildNodes) {
		next if ($child->getNodeType != ELEMENT_NODE);
		my $format_def = $child->getNodeName;
		my $script_file = $child->getAttribute('sql-script-file');
		if (!(defined $script_file)) {
			if ($verbose) {print "    Couldn't find sql-script-file attribution in format-data section, using DEFAULT setting\n";}
			return %scripts;
		}
		
		$scripts{$format_def} = $script_file;
	}
	
	return %scripts;
}

sub format_data{
	my $ip_node = shift;
	my ($format_str,$sql_script_file) = ();
	my %scripts;

	#Test if ip_node
	#	  i) is not a node,
	#then $format_str = $ip_nodeuse
	my $ch= ();
	eval{$ch = $ip_node->hasChildNodes;};
	if ($@) {
		$format_str = $ip_node;
	}
	elsif ($ch) {
		foreach my $child ($ip_node->getChildNodes) {
			next if ($child->getNodeType != ELEMENT_NODE);
			$format_str = $child->getNodeName;
			break;
		}
	}elsif (defined $ip_node->getAttributes) {
		$format_str = $ip_node->getAttribute("value");
	}
	if ($prompt) {print "--${time} formating data $format_str \n";}

	%scripts = parse_format_data_setting();
	$sql_script_file = $scripts{$format_str};
	
	if ($prompt) {print "    using sql script file $sql_script_file\n";}
	
	my $dbh;
	my @commands = parse_sql_file($sql_script_file); # breaks a SQL script into its component commands and contains in an array
	foreach $command (@commands) {
		#replace_pattern($command);
		execute_sql($dbh,$command);
	}
	$dbh->disconnect;
 	#for output-to-continuation otuput_db has to be the same through the years, 
	#otherwise, the code needs to be changed, probably, add a $previous_output_db pattern
	#currently the databases' host, username, and password have to be the same.
}


sub parse_directory_setting{
	#get directories
	%directories=();
	
	my $_t1_node = $parameters_root->getElementsByTagName("directory")->item(0);
	if (!(defined $_t1_node)) {
		die "Couldn't find directory tag in parameter file\n\n";
	}elsif (!($_t1_node->hasChildNodes)) {
		die "Couldn't find directories setting in parameter file\n\n";
	}
	
	foreach my $child ($_t1_node->getChildNodes) {
		next if ($child->getNodeType != ELEMENT_NODE);
		$directories{$child->getNodeName} = $child->getAttribute("value");
	}

	foreach my $directory (keys %directories) {
		replace_pattern($directories{$directory});
		if ($prompt) {
			print "$directory = " . $directories{$directory} . "\n";
		}

	}
	
	
	if (!(defined $directories{'urbansim-parameter-file'})) {
		$directories{'urbansim-parameter-file'}="urbansim_parameters_" . $year0 . "_to_" . $year1 . ".xml";
	}

	
	return %directories;

}

sub parse_dataset_setting{

	#get urbansim dataset
	#global variables#
	%databases = ();
	
	my ($scenario_db_str,$scenario_db_host,$scenario_db,$scenario_db_username,$scenario_db_password) = ();
	my ($output_db_str,$output_db_host,$output_db,$output_db_username,$output_db_password) = ();
	my ($baseyear_db_str,$baseyear_db_host,$baseyear_db,$baseyear_db_username,$baseyear_db_password) = ();
	$base_year = ();
	
	#global variables

	my $_t2_node = $parameters_root->getElementsByTagName("dataset")->item(0);
	if (!(defined $_t2_node)) {
		die "Couldn't find dataset node in parameter file\n\n";
	}
	
	my ($_a,$_b)=();
	my @databases = $_t2_node->getElementsByTagName("database");
	if (defined @databases) {
		foreach my $database (@databases) {
			if ($database->getAttribute("contains") eq "scenario-data") {
				my $mysql_node = $database->getElementsByTagName("mysql")->item(0);
				$scenario_db_str = $mysql_node->getAttribute("url");
				$scenario_db_username = $mysql_node->getAttribute("username");
				$scenario_db_password = $mysql_node->getAttribute("password");
				($_a,$_b,$scenario_db_host,$scenario_db) = split (/\//,$scenario_db_str);
				
			}
			elsif ($database->getAttribute("contains") eq "outputdata") {
				my $mysql_node = $database->getElementsByTagName("mysql")->item(0);
				
				$output_db_str = $mysql_node->getAttribute("url");
				$output_db_username = $mysql_node->getAttribute("username");
				$output_db_password = $mysql_node->getAttribute("password");
				($_a,$_b,$output_db_host,$output_db) = split (/\//,$output_db_str);
				
			}
			elsif ($database->getAttribute("contains") eq "baseyear-data") {
				my $mysql_node = $database->getElementsByTagName("mysql")->item(0);
				
				$baseyear_db_str = $mysql_node->getAttribute("url");
				$baseyear_db_username = $mysql_node->getAttribute("username");
				$baseyear_db_password = $mysql_node->getAttribute("password");
				($_a,$_b,$baseyear_db_host,$baseyear_db) = split (/\//,$baseyear_db_str);
				
			}
		}

		replace_pattern($scenario_db);
		replace_pattern($output_db);
		replace_pattern($baseyear_db);
	}

	%databases = (
		'scenario_db' => {
				    host => $scenario_db_host,
				    db => $scenario_db,
				    username => $scenario_db_username,
				    password => $scenario_db_password,
			    	},
		'output_db'  => {
				    host => $output_db_host,
				    db => $output_db,
				    username => $output_db_username,
				    password => $output_db_password,
			    	},
		'baseyear_db' => {
				    host => $baseyear_db_host,
				    db => $baseyear_db,
				    username => $baseyear_db_username,
				    password => $baseyear_db_password,
			    	}
	);
		
	#get baseyear from base_year table in baseyear database
	my $dbh = db_conn($databases{'baseyear_db'});
	my $sth = $dbh->prepare("select YEAR from base_year") 
	  or die "incorrect base_year table in baseyear database: $baseyear_db\n\n";
	$sth->execute()
	  or die "failed to execute statement select YEAR from base_year.\n\n";
	$base_year = $sth->fetchrow();

	$sth->finish;$dbh->disconnect;
	
	if ($prompt) {print "baseyear-db: $baseyear_db_host, $baseyear_db \n";} #,$output_db_username,$output_db_password \n";}
	if ($prompt) {print "secnario-db: $scenario_db_host, $scenario_db \n";} #,$scenario_db_username,$scenario_db_password \n";}
	if ($prompt) {print "output-db: $output_db_host, $output_db \n";} #,$output_db_username,$output_db_password \n";}
	
	return %databases;
}

sub update_urbansim_parameter_file{
	my $ip_node = $_[0];
	#interaction parameter node

	DEFAULT:
	my %models = (
	 	  'accessibility-model' => '',
    		  'employment-location-choice-model' => {'weighted-choiceset'=>"true"},
    		  'employment-relocation-choice-model' =>'',
		  'household-relocation-choice-model'=>'',
		  'household-transition-model' => '',
    		  'employment-transition-model' => '',
    		  'household-location-choice-model' => { 'weighted-choiceset' => "true"},
		  'land-price-model' => '',
    		  'developer-model-with-vacancy-adjustment'=>'',
	);
	my %models_att = (
		'random-seed' => "0"
	);
	
	
	#only update dataset and models section currently
	my $urbansim_parameter_file = $directories{'urbansim-parameter-file'};
	my ($up_parser,$up_doc,$up_root,$up_xml_pi,$up_doc_type) = ();
	#parser for urbansim parameter doc & root
	if (-e $urbansim_parameter_file) {
		$up_parser = new XML::DOM::Parser;
		$up_doc = $up_parser->parsefile($urbansim_parameter_file);
		$up_root = $up_doc->getDocumentElement;
		
		$up_xml_pi = $up_doc->getXMLDecl; $up_xml_pi->setEncoding('UTF-8');
#		$up_doc_type = $up_doc->createDocumentType("urbansim-parameters", $directories{'urbansim-directory'}
#		 . "org/urbansim/urbansim-parameters.dtd");
	}
	else {
		
		$up_doc = new XML::DOM::Document;
		$up_root = $up_doc->createElement('urbansim-parameters');
		
		$up_xml_pi = $up_doc->createXMLDecl ('1.0');  $up_xml_pi->setEncoding('UTF-8');
#		$up_doc_type =$up_doc->createDocumentType ("urbansim-parameters", $directories{'urbansim-directory'}
#		  . "org/urbansim/urbansim-parameters.dtd");
		
		#add models section
		my $up_models_node = $up_doc->createElement('models');
		$up_root->appendChild($up_models_node);
			
		#add dataset section to new created parameter file
		my $dataset = $up_doc->createElement("dataset");
		$up_root->appendChild($dataset);
		
		my $database = $up_doc->createElement("database");
		$dataset->appendChild($database);
		
		$database->setAttribute("contains", "scenario-data");
		my $mysql = $up_doc->createElement("mysql");
		$database->appendChild($mysql);		

		my $database = $up_doc->createElement("database");
		$dataset->appendChild($database);
		
		$database->setAttribute("contains", "outputdata");
		my $mysql = $up_doc->createElement('mysql');
		$database->appendChild($mysql);

		#add exporter section
		my $up_exporter_node = $up_doc->createElement('exporter');
		$up_root->appendChild($up_exporter_node);
	}
	
	#update urbansim dataset section
	my @up_databases = $up_root->getElementsByTagName("database");
	foreach my $up_database (@up_databases) {
		my $up_mysql_node = $up_database->getElementsByTagName("mysql")->item(0);
		if (!(defined $up_mysql_node)) { 
			die "    parameter file is incorrect, missing <mysql> tag \n\n"
		}

		if ($up_database->getAttribute("contains") eq "scenario-data") {
			my $scenario_db = $databases{'scenario_db'};
			my $scenario_url_str = "jdbc:mysql://" . $scenario_db->{'host'} . "/" . $scenario_db->{'db'};
			$up_mysql_node->setAttribute("url",$scenario_url_str);
			$up_mysql_node->setAttribute("username",$scenario_db->{'username'});
			$up_mysql_node->setAttribute("password",$scenario_db->{'password'});
		}
		elsif ($up_database->getAttribute("contains") eq "outputdata") {
			my $output_db = $databases{'output_db'};			
			my $output_url_str = "jdbc:mysql://" . $output_db->{'host'} . "/" . $output_db->{'db'};
			$up_mysql_node->setAttribute("url",$output_url_str);
			$up_mysql_node->setAttribute("username",$output_db->{'username'});
			$up_mysql_node->setAttribute("password",$output_db->{'password'});
		}
	}
	
	#update urbansim models section
	my $up_models_node = $up_root->getElementsByTagName("models")->item(0);
	if (!(defined $up_models_node)) { 
		die "    error in urbansim parameter file is incorrect, missing <models> tag\n\n";
	}
	
	#Test if ip_node
	#	  i) is not a node, or 
	#	 ii) has no child, or
	#	iii) has no <models> child, and
	#	 iv) parameter file does not exist,
	#use default <models> setting
	my ($ch,$mch) = (); 
	eval{$ch = $ip_node->hasChildNodes;};
	if (!$@) {
		if ($ch) {
			my $ip_models_node = $ip_node->getElementsByTagName("models")->item(0);
			$mch = (defined $ip_models_node);
		}
	}	
	print "|$@|$ch|$mch|\n" if ($DEBUG);
	if ($@ || !$ch || !$mch) {
		if (-e $urbansim_parameter_file) { }
		else {# if no parameter file and no models section found
		if ($verbose) {"    Couldn't find urbansim parameter file or urbansim parameter section, applying DEFAULT setting\n";}
		while (my ($att_key,$att_value) = each %models_att) {
			$up_models_node->setAttribute($att_key,$att_value);
		}
	
		foreach my $model (keys %models) {
			my $up_new_child = $up_doc->createElement($model);

			#set attributes
			if ($verbose) {print "    <$model ";}
			while (($att_name,$att_value) = each %{$models{$model}}) {
				$up_new_child->setAttribute($att_name,$att_value);
				
				if ($verbose) {print "$att_name=$att_value";}
			}
			$up_models_node->appendChild($up_new_child);
			if ($verbose) {print "/>\n";}
		}
		}

	}
	elsif (($ip_node->hasChildNodes)){
		my $ip_models_node = $ip_node->getElementsByTagName("models")->item(0);
		if (defined $ip_models_node) {
			#copy models' attributes
			my $ip_models_att = $ip_models_node->getAttributes;
			if( defined $ip_models_att ){
				my $num_att = $ip_models_att->getLength;
				for(my $i=0; $i<$num_att; $i++){
					my $ip_att = $ip_models_att->item($i);
					$up_models_node->setAttribute($ip_att->getName,$ip_att->getValue);
				}
			}
			
			#copy models' childs if not already exists
			foreach my $ip_child ($ip_models_node->getChildNodes) {
				next if ($ip_child->getNodeType != ELEMENT_NODE);
				my $ip_child_name = $ip_child->getNodeName;
				#test if parameter file already has this node
				my $up_child_node = $up_models_node->getElementsByTagName($ip_child_name)->item(0);
				if (defined $up_child_node){
					if ($verbose) {print "    >>model " . $child_name . " exists\n";}
					next;
				}
				my $up_new_child = $up_doc->createElement($ip_child_name);
				my $att = $ip_child->getAttributes;
				if( defined $att ){
					my $n = $att->getLength;
					for(my $i=0; $i<$n; $i++){
						my $a = $att->item($i);
						$up_new_child->setAttribute($a->getName,$a->getValue);
					}
				}
				$up_models_node->appendChild($up_new_child);
			}				
		}
	}
	
	my $f = new FileHandle ($urbansim_parameter_file, "w");
	print $f $up_xml_pi->toString;
#	print $f $up_doc_type->toString;
	print $f $up_root->toString;
	
	close($f);
	
	$up_doc->dispose;
	
}

sub get_all_years{
	my ($_run_node) = @_;
	my @_years;
	if (!($_run_node->hasChildNodes)){
		die "Couldn't find year node in parameter file\n\n";
	}
	foreach my $child ($_run_node->getChildNodes){
		next if ($child->getNodeType != ELEMENT_NODE);
		if ($child->getNodeName eq "year") {
			my $attr = $child->getAttribute("name");
			push(@_years, split(/,/,$attr));
		}
	}
	
	return @_years;
}

sub get_year_node{
	my ($_run_node,$_year) = @_;
	foreach my $child ($_run_node->getChildNodes()){
		next if ($child->getNodeType != ELEMENT_NODE);
		if ($child->getNodeName eq "year") {
			my $attr = $child->getAttribute("name");
			if ($attr =~ /$_year/) {
				#if ($verbose) {print " $_year found\n";}
				return $child;
			}
		}
	}
	
}	

sub replace_pattern{
	#my ($var) = @_;
	$_[0] =~ s/\$year0/$year0/g;
	$_[0] =~ s/\$year1/$year1/g;
	$_[0] =~ s/\$base_year/$base_year/g;

	my $baseyear_db_host = $databases{'baseyear_db'}{'host'};
	my $baseyear_db = $databases{'baseyear_db'}{'db'};
	my $scenario_db = $databases{'scenario_db'}{'db'};
	my $output_db = $databases{'output_db'}{'db'};
	
	$_[0] =~ s/\$baseyear_db_host/$baseyear_db_host/g;
	$_[0] =~ s/\$baseyear_db/$baseyear_db/g;
	$_[0] =~ s/\$scenario_db/$scenario_db/g;
	$_[0] =~ s/\$output_db/$output_db/g;

	return 1;
}


sub parse_sql_file{
	my $script_file = shift;
	open(SCRIPTF, $script_file) or 
		die "Couldn't open $script_file";
	my @commands; 
	my $i=0;

	while(<SCRIPTF>) {
		$row = $_;
		chomp($row);
		$row =~ s/^\s+//; #discard spaces
		$row =~ s/\s+$//;
		next if ($row =~ /^#/);  # discard comments

		$commands[$i] = $commands[$i] . " " . $row;

                $commands[$i] =~ s/^\s+//;
                $commands[$i] =~ s/;//;	
	
		if ($row =~ s/\;//) {
		    $i++;} 
	}
	if ($verbose) {
		#foreach $command (@commands) {print "    sql command quene: $command\n";}
	}
	 
	close(SCRIPTF)
		or die "Couldn't close $script_file\n\n";
	return @commands;
	
}

sub execute_sql {
	my ($dbh,$_command) = @_;
	
	if ("\L$_command" =~ /^use/) {
		($_, $_db) = split(/ /, $_command);
		
		#chop the leading '$' in database name;
		$_db =~ s/\$//g;
		
		$dbh = db_conn($databases{$_db});
		#actually, all the databases' host, username and password have to be the same to work.

	} elsif ("\L$_command" =~ /^select/) {
		replace_pattern($_command);

		$stm = $_command;
		if ($verbose) {print "    $stm\n";}
		$sth = $dbh->prepare($stm) 
			or die "Failed to prepare statement: $stm. $sth->errstr \n"; 
		$sth->execute() 
			or die "Failed to execute statement: $stm. $sth->errstr \n";
		$sth->finish;
	}  elsif ("\L$_command" =~ /[a-z]/) { ##elsif ("\L$_command" =~ /^drop/ || "\L$_command" =~ /^delete/ || "\L$_command" =~ /^update/ || 
		  ##"\L$_command" =~ /^create/ || "\L$_command" =~ /^insert/){
		replace_pattern($_command);
		$stm = $_command;
		if ($verbose) {print "    $stm\n";}
		$rv=$dbh->do($stm) 
			or die "Failed to execute statement: $stm. ". DBI->errstr;
	}

	$_[0] = $dbh;
	#actually return the $dbh
}



sub db_conn{
	my $db = $_[0];
	my ($host,$DB,$user,$passwd) = ($db->{'host'},$db->{'db'},$db->{'username'},$db->{'password'});
	$DB_conn = "DBI:mysql:database=$DB :host=$host";
	if ($verbose) {print "    connecting to database $DB_conn\n";}
	$dbh = DBI->connect($DB_conn,$user,$passwd) 
	  or die "failed to open database connection " . DBI->errstr;	
	
	return $dbh;

}

sub read_file_to_table {
	my ($_file,$_dbh,$_table)=@_;
	open(IMPORTF, $_file) or 
		die "Couldn't open $_file";

	while(<IMPORTF>) {
		$row = $_;
		chomp($row);
		@column = split(/\t/, $row);
		
		my $_stm = "insert into $_table values ("; 
		foreach $column (@column) {
			$_stm = "$_stm $column,"; 
			
		}
		chop($_stm);  #chop the last ","
		$_stm = $_stm . ")";

		if ($verbose) {print "    $_stm\n";}		

		$_rv=$_dbh->do($_stm) 
			or die "failed to insert @column into table $table " . DBI->errstr;
		
	}

	close(IMPORTF)
		or die "can't close $_file";
}

sub export_table_to_file {
	my ($_dbh,$_table,$_export_file,$_year) = @_;

	open(EXPORTF, ">$_export_file") or 
		die "Couldn't open $_export_file";
	# print EXPORTF "#";
	
	my $_stm = "select * from $_table"; #where YEAR = $_year";
	my $_sth = $_dbh->prepare($_stm)
		or die "failed to prepare statement.\n";
	$_sth->execute()
		or die "couldn't execute statement: " . $_sth->errstr;

	while (@column=$_sth->fetchrow()) {
		foreach $column (@column) {
			print EXPORTF "$column\t";
		}
		print EXPORTF "\n";
	}
	
	close(EXPORTF)
			or die "can't close $_export_file";
	
	$_sth->finish;
}

sub get_time {
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

    $time="${Month}\/${DayInMonth}\/${Year},${Hours}\:${Minutes}\:${Seconds}";
}

sub processSwitches {
	my $result;
	
	$result = &GetOptions(
		"h"		=> \$help,
		"t"		=> \$test,
		"f:s"		=> \$xml_file,
		"p"		=> \$prompt,
		"v"		=> \$verbose,
	);

	if (!$result) {
		die "Error in input. Use -h for help.\n";
	}

	if ($help) {
			die
"Usage: perl $myName.pl [switches]
-h\t\tThis help
-t\t\tRun tests
-f [string]\tTravel model UrbanSim automation parameter file
-p\t\tDon't prompt
-v\t\tVerbose
";
	}
	$prompt =! $prompt; # make prompt be default
	$prompt = 0 if ( $test );

	if ( !$xml_file && !$test ) {
		die "When not running tests with -t\nneed parameter filename with -f. Use -h for help.\n";
	}
}

#############################################TEST SESSION############################################

sub do_tests {
	my ($errors,$tests) = (0,0);
	my ($numerr,$numtests) = (0,0);
	my %run_p = ();

	$xml_file = "./tests/test_batchrun-parameter_5yr.xml";

	open_xml_file();
	my @years=get_all_years($parameters_root->getElementsByTagName("run")->item(0));

	my $num_years=scalar(@years);

	print "##################\nRunning tests\n";

	for (my $i=0;$i<$num_years;$i++){
		$year0 = $years[$i];
		if ($i == ($num_years-1)) {
			$year1 = @years[$i]
		}
		else {
			$year1 = @years[$i+1]; 
		}
		
		#find the node that contain $year
		my $run_node = $parameters_root->getElementsByTagName("run")->item(0);
		my $year_node = get_year_node($run_node,$year0);
		
		($numerr,$numtests) = test_parse_directory_setting();
		$errors += $numerr; $tests += $numtests;
		($numerr,$numtests) = test_parse_dataset_setting();
		$errors += $numerr; $tests += $numtests;
		
		($numerr,$numtests) = test_parse_exchange_data_setting();
		$errors += $numerr; $tests += $numtests;
		($numerr,$numtests) = test_parse_format_data_setting();
		$errors += $numerr; $tests += $numtests;
		if ($i < $num_years-1) {
			if ($year_node->hasChildNodes) {
				foreach my $child($year_node->getChildNodes){
					next if ($child->getNodeType != ELEMENT_NODE); 
					my $child_name = $child->getNodeName;
					$run_p{$child_name} = $child;
				 }
			}			
			($numerr,$numtests) = test_update_urbansim_parameter_file($run_p{'run-urbansim'});
			$errors += $numerr; $tests += $numtests;
		}
	}
	
	print "$errors Failure";
	print "s" if $errors != 1;
	print " out of $tests Test";
	print "s" if $tests+1 != 1;
	print ".\n##################\n";
	
	exit(0);
}

sub test_parse_directory_setting{
	my ($numerr,$numtests) = (0,0);
	my %expected = (
		'urbansim-directory' => "C:/Program Files/UrbanSim/",
		'urbansim-parameter-file' => "./tests/test_WFRC_" . $year0 . "_parameters_5yr_" . $year1 . ".xml",
		'travel-model-directory' => "C:/WFRC/DV31_UrbanSim_$year0/",
		'data-to-urbansim-directory' =>"C:/WFRC/DV31_UrbanSim_$year0/5UrbanSim/Uo/",
		'data-from-urbansim-directory' => "C:/WFRC/DV31_UrbanSim_$year1/5UrbanSim/Ui/",
		'travel-model-batch-file' => "HailMaryNoPauses.bat",
	);
	print "run tests of parsing directory setting\n";

	parse_directory_setting();
	foreach my $key (sort keys %directories) {
		$numtests++;
		if (($directories{$key}) ne ($expected{$key})) {
			$numerr++;
			print "<failed $key = " . $directories{$key} . "\n";
			print ">failed $key = " . $expected{$key} . "\n";
			
		}
	}	
	
	return ($numerr,$numtests);
}

sub test_parse_dataset_setting{
	my ($numerr,$numtests) = (0,0);
	my %expected = (
		'scenario_db' => {
				    host => 'localhost',
				    db => "WFRC_$year0" . "_scenario_5yr",
				    username => 'mysql',
				    password => '',
			    	},
		'output_db'  => {
				    host => 'localhost',
				    db => "WFRC_1997_output_5yr_2003",
				    username => 'mysql',
				    password => '',
			    	},
		'baseyear_db' => {
				    host => 'localhost',
				    db => 'WFRC_1997_baseyear',
				    username => 'mysql',
				    password => '',
			    	},
		base_year => 1997,		
	);
	
	print "run tests of parsing dataset setting\n";
	
	%databases=parse_dataset_setting();

	foreach my $db (sort keys %databases) {
		foreach my $var (sort keys %{$databases{$db}}) {
			$numtests++;
			my $database = $databases{$db}{$field};
			my $expected = $expected{$db}{$field};
			$expected =~ s/\s+//gc;
			
			if ($exchange ne $expected) {
				$numerr++;
				print "<failed exchanges = " . $databases{$db}{$field} . "\n";
				print ">failed expected = " . $expected{$db}{$field} . "\n";
				
			}
		}
		
	}
	
	$numtests++;
	if ($base_year != ($expected{'base_year'})) {
		$numerr++;
		print "<failed base_year = $base_year \n";
		print ">failed base_year = " . $expected{'base_year'} . "\n";
	}
	
	return ($numerr,$numtests);	
}


sub test_parse_format_data_setting{
	my ($numerr,$numtests) = (0,0);
	my %expected = (
		'format-data-from-travel-model' =>
			"./sql_scripts/format_data_from_travel_model.sql",
		'format-data-for-travel-model'  =>
			"./sql_scripts/format_data_for_travel_model.sql",
		'create-indicators' =>
			"./sql_scripts/urbansim_indicators.sql",
		'create-gis-data' =>
			"./sql_scripts/output_data_to_grid_zone.sql",
		'output-to-continuation' =>
			"./sql_scripts/output_to_continuation.sql",
	);

	print "run tests of formating data setting\n";
	
	my %scripts = parse_format_data_setting();
	foreach my $action (sort keys %scripts) {
		$numtests++;
		
		if ($scripts{$action} ne $expected{$action}) {
			$numerr++;
			print "<failed $action = " . $scripts{$action} . "\n";
			print ">failed $action = " . $expected{$action} . "\n";
			
		}
	}
	
	return ($numerr,$numtests); 
}

sub test_parse_exchange_data_setting{
	my ($numerr,$numtests) = (0,0);
	my %expected = (
		'from-travel-model-to-urbansim' => {
			AccessLogsum => "
				FROM_ZONE_ID int,
				TO_ZONE_ID int,
				LOGSUM0 double,
				LOGSUM1 double,
				LOGSUM2 double
				",
			HighwayTimes => "
				FROM_ZONE_ID int, 
				TO_ZONE_ID int, 
				HWYTIME double
				",
			},
		'from-urbansim-to-travel-model' => {
			HHdistrib_joint_inclohi => "",
			SEdata => "" ,
			},
			
	);

  	print "run tests of parsing exchange data setting\n"; 
	
	my %exchanges = parse_exchange_data_setting();
	foreach my $from_to (sort keys %exchanges) {
		foreach my $table_name (sort keys %{$exchanges{$from_to}}) {
			$numtests++;
			my $exchange = $exchanges{$from_to}{$table_name};
			$exchange =~ s/\s+//gc;
			my $expected = $expected{$from_to}{$table_name};
			$expected =~ s/\s+//gc;
			
			if ($exchange ne $expected) {
				$numerr++;
				print "<failed exchanges = " . $exchanges{$from_to}{$table_name} . "\n";
				print ">failed expected = " . $expected{$from_to}{$table_name} . "\n";
				
			}
		}
		
	}

	return ($numerr,$numtests); 
}

sub test_update_urbansim_parameter_file{
	my $run_urbansim_node = shift;
	my ($numerr,$numtests) = (0,0);
	
	print "run tests of updating UrbanSim parameter file setting\n";
	
	update_urbansim_parameter_file($run_urbansim_node);
	($file_dir,$file) = extract_dir_file($directories{"urbansim-parameter-file"});
	my @file;
	push @file, "$file";

	return compare_files(@file);
}

sub extract_dir_file {
	my ($full) = @_;
	my ($path,$file);

	@full=split(/\//,"$full");
	$file = $full[$#full];
	if ($#full>0) { $path = join("/",@full[0..($#full-1)]); }
	else          { $path = "."; }
 	$path = $path . "/";
	return ($path,$file);
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
			print "Success for $file\n" if $verbose;
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

