#!/usr/bin/perl
#
# Perl script that processes estimation model results
#	creates a coeff file for UrbanSim,
#	writes a tab delimited file with result tables,
#	writes a model file with coeffs restricted to results
#	writes a tab delimited file of results in similar manner
#		as coeff files but with a presentation format.
#
# Author: Gudmundur Freyr Ulfarsson
#
# This script is presented AS IS, with no responsibility
# stated or implied for harm caused by the use or lack of use
# of this script, nor for any functionality or lack thereof.
#

use Getopt::Long;
$myName = "estResulter04";

# To do
#
# When no alternative code is found trigger an error
# When the same alternative code is found multiple times
#	ignore the duplicates or remove them from the list
# Write appropriate statistics into verbose column table.
# Mark coefficients significant above a certain limit in
#	the verbose column table.
# Read significance limit from setup file.
# Read number of significant digits and exponent size limit
#	from setup file, is now hard coded.
# Transpose the verbose column table 
#	(so it becomes a verbose column table, it is now in rows).


# v4
#	Fixed Limdep MNL parse for Limdep 8.0
#	Fixed column order for UrbanSim 2.1 model specification table
#	Added handling for UrbanSim 2.0 model configuration tables
#	Added handling for UrbanSim 2.1 model configuration tables
#	Handle commented lines in VARIABLES
#	Fixed error where model statistics were written once too many
#		times in the verbose result file
#	Fixed error where equation ID was not written for a model with
#		one empty equation when the model is a part of a group of 
#		models that are generally multi-equation and need the 
#		equation ID column. Now write the Base Alternative Code.
#
# v3
#	Added initial handling of marking significance on
#		standard errors in verbose column table
#	Added initial print of model statistics into
#		verbose column table - this has errors!!
#		Errors: doesn't print for all equations
#	Keep trailing zeros in decimals in verbose column table.
#	Now prints a selected number of significant digits and
#		multiplies out exponents that are smaller than a
#		selected limit.
#	Write long variable description in verbose column table.
#	Write verbose column table, all alternatives in rows,
#		variables in columns - need to transpose.
#
# v2a
#	Handles a base case, writes out a row of zeros
#		for it in the coeff file, not in table file
#
# v2
#	Handles NLOGIT mnl and REGRESS ols from Limdep
#		and REG ols from SAS by reading model from setup
#	Handles cases without IDs
#	Reads filenames for coeff file, table file,
#		restricted model command file, from Setup.
#
# v1
#	Reads SAS linear regression results and
#		writes to a coeff and table file.
#	Writes an mnl estimation command file with all
#		the coefficients fixed to the result
#		(restricted model command file)
#	Handles the CASES section in the setup file
#	Writes a help file that is a heavily commented
#		setup file example
#	Writes a sample interface script to run estRes
#	Handles white space in setup file commands
#	Handles "N/A" label, by replacing it with
#		the coeff file label.
#	Handles parse rule for termination of
#		model output sections
#	Handles variables that are alternative specific
#		and carry a postfixed alternative ID in
#		their label.
#	Separates Limdep parsing from model printing
#	Handles decision maker specific variables
#	Handles section with description of alternatives
#	Reads necessary input about the job from a setup file
#	Script created

###########################
#
# Main program

# Main GLOBALS:
#	(there are more GLOBALS defined in the subroutines)
#	$fileLoop
#	$inFile

processSwitches();
setup();
prepare_headers();

foreach $inFile (@inFileAr) {
	initVars();
	
	processFile();
	
	postProcess();
}


###########################
#
# Main subroutines
#

sub processSwitches {
	my $result;
	
	$result = &GetOptions(
		"h"		=> \$help,
		"if:s"	=> \$modelfiles,
		"p:s"	=> \$path,
		"sf:s"	=> \$setup_file,
		"v"		=> \$verbose,
		"help"	=> \$longhelp,
		"hrun"	=> \$runhelp,
		"ver"	=> \$Verbose,
	);

	if (!$result) {
		die "Error in input. Use -h for help.\n";
	}

	if ($help) {
		helpswitches();
	}
	if ($longhelp) {
		helplong();
	}
	if ($runhelp) {
		if ($setup_file) {
			setup();
		}
		helprun();
	}
	
	if ( !$setup_file ) {
		die "Need filename for setup file with -sf. Use -h for help.\n";
	}	
	if (!$modelfiles) {
		die "Need at least one model file with -if\n";
	}
	else {
		@inFileAr = split ',',$modelfiles;
	}
	
#	if (!$fmt) {
#		$fmt = "limdep";
#	}
#	else {
#		$fmt =~ tr/[A-Z]/[a-z]/;
#		die "Error: Support only formats: [limdep,sas]\n"
#			if ($fmt ne "limdep" && $fmt ne "sas");
#	}
	if ($Verbose) {
		open(VER,">>$myName.log")
			or die "Can't open $myName.log: $1\n";
		$verbose=1;
	}
	elsif ($verbose) {
		open(VER,">$myName.log")
			or die "Can't open $myName.log: $1\n";
	}
	if ($verbose) {
		print VER "\n=================\n";
		print VER " $myName.pl\n";
		print VER " Author: Gudmundur Freyr Ulfarsson\n";
		print VER "=================\n\n";
		print VER "Setup file: $setup_file\n";
		print VER "Path to input: $path\n";
		print VER "Files to process: $modelfiles\n";
		print VER "\n";
	}

}

# Sets up GLOBAL variables
#	by reading information from the Setup file
sub setup {
	# GLOBALS:
	#
	# $cfile			filename for coeff file
	# $tfile			filename for table file
	# $vfile			filename for verbose column file
	# $cmdFile			filename for restricted model command file
	# $us2cFile			filename for UrbanSim 2 coeff file
	# $us2sFile			filename for UrbanSim 2 spec file
	# $fmt				model file format (limdep,sas)
	# $model			model type (ols,mnl)
	#
	# $pModel_Id		parse match for model ID
	# $pAlt				parse match for alternative description
	# $pAltNum			parse match for number of alternatives
	# $pAltCodes		parse match for alternative codes
	# $pModel			parse match for model section
	# $pVarForm			parse match for coeff labels
	# $pSecTerm			parse match for section terminator
	#
	# %var_info			Model labels mapped to info
	# @model_labels		order of keys in %var_info
	# $cHeadIdx			index to coeff_header in @$var_info{}
	# $varLegIdx		index to var. legend in @$var_info{}
	# $varNameIdx		index to var. name in @$var_info{}
	# $us2Idx			index to UrbanSim 2.0 var. name in @$var_info{}
	# @coeff_header		header for coeff file
	# @table_header		header for table file
	# @vtable_header	header for verbose column table file
	# %alt_info			Alt.ids mapped to alt. descriptions
	# %case_info		Casenames mapped to case info

	# Model ID is a word followed by a number,
	#	For example, employment sector models, we have
	#	one model for each sector. The model ID
	#	is then Sector followed by the sector number,
	#	i.e. "Sector 1"
	
	# %var_info is a hash that is
	#	keyed by coefficient labels of model variables
	#	points to array containing
	#	0)	UrbanSim 1 coeff file header
	#	1)	variable text legend
	#	2)	Limdep variable name
	#	3)	UrbanSim 2 variable name
	
	# @model_lables contains the labels of model variables
	#	and gives the order of the keys in %var_info
	
	# %alt_info is a hash that is keyed by alternative
	#	id codes, used as postfixes on coefficient labels
	#	in the model, and gives the descriptions
	#	for the alternative(s) the code refers to.

	# %case_info is a hash that is keyed by case names
	#	Each element refers to a hash with the fields
	#		casepath
	#		casesetup
	#		casedir
	#		casefileh
	#		casefilet
	#		caseids
	#			refers to an array with the IDs
	
	##########
	#
	# Setup file dependent section
	# <this section changes if the Setup file commands change>
	
	# Read setup from $setup_file
	#
	# Setup commands:
	#	SETUP
	#		COEFFILE,TABLEFILE,COLUMNTABLEFILE,RESTRFILE,
	#		US2COEF_FILE,US2SPEC_FILE
	#		FORMAT,MODEL
	#	PARSERULES
	#		PMODELID, PALT, PALTNUM, PALTCODES,
	#		PMODEL, PVARFORM, PSECTERM,
	#	VARIABLES
	#	ALTERNATIVES
	#	CASE
	#		CASENAME, CASEPATH, CASESETUP, CASEDIR,
	#		CASEFILEH, CASEFHILET, CASEIDS
	#	
	
	my $altidnum=0;
	my $NANAME="N/A";
	my $label;
	my $curcase="";
	
	# Indices to the row fields in the VARIABLES section
	my ($coefLabIdx,$shNamIdx,$longNamIdx,$varIdx) =
		(0,1,2,3,4);

	# Indices to the array in %var_info
	($cHeadIdx,$varLegIdx,$varNameIdx,$us2Idx) = (0,1,2,3);
	
	open(SET,"<$setup_file")
		or die "Can't open $setup_file: $1\n";
	while (<SET>) {
		s/\r//g;
		if (/^\s*SETUP\s*(?:#.*)?$/) {
			while (<SET>) {
				s/\r//g;
				if (/^\s*#/) {
					next;
				}
				elsif (/^\s*COEFFILE\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$cfile = $1;
				}
				elsif (/^\s*TABLEFILE\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$tfile = $1;
				}
				elsif (/^\s*COLUMNTABLEFILE\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$vfile = $1;
				}
				elsif (/^\s*RESTRFILE\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$cmdFile = $1;
				}
				elsif (/^\s*US2COEF_FILE\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$us2cFile = $1;
				}
				elsif (/^\s*US2SPEC_FILE\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$us2sFile = $1;
				}
				elsif (/^\s*FORMAT\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$fmt = $1;
					$fmt =~ tr/[A-Z]/[a-z]/;
				}
				elsif (/^\s*MODEL\s*=\s*"(\S+)"\s*(?:#.*)?$/) {
					$model = $1;
					$model =~ tr/[A-Z]/[a-z]/;
				}
				elsif (/^\s*$/) {
					last;
				}
			}
		}
		if (/^\s*PARSERULES\s*(?:#.*)?$/) {
			while (<SET>) {
				s/\r//g;
				if (/^\s*#/) {
					next;
				}
				elsif (/^\s*PMODELID\s*=\s*"(.+)"\s*(?:#.*)?$/) {
					$pModel_Id = $1;
				}
				elsif (/^\s*PALT\s*=\s*"(.+)"\s*(?:#.*)?$/) {
					$pAlt = $1;
				}
				elsif (/^\s*PALTNUM\s*=\s*"(.+)"\s*(?:#.*)?$/) {
					$pAltNum = $1;
				}
				elsif (/^\s*PALTCODES\s*=\s*"(.+)"\s*(?:#.*)?$/) {
					$pAltCodes = $1;
				}
				elsif (/^\s*PMODEL\s*=\s*"(.+)"\s*(?:#.*)?$/) {
					$pModel = $1;
				}
				elsif (/^\s*PVARFORM\s*=\s*"(.+)"\s*(?:#.*)?$/) {
					$pVarForm = $1;
				}
				elsif (/^\s*PSECTERM\s*=\s*"(.+)"/) {
					$pSecTerm = $1;
				}
				elsif (/^\s*$/) {
					last;
				}
			}
		}
		if (/^\s*VARIABLES\s*(?:#.*)?$/) {
			while (<SET>) {
				s/\r//g;
				if (/^\s*#/) {
					# skip commented lines
					next;
				}
				if (/^\s*(\S.*)\s*(?:#.*)?$/) {
					my @text = split "\t", $1;
					$label = $text[$coefLabIdx];
					$label =~ tr/[a-z]/[A-Z]/;
					$label = $text[$shNamIdx] if ($label eq $NANAME);
					push @model_labels, $label;
					my $i;
					for ($i=1; $i<@text; $i++) {
						push @{$var_info{$label}}, $text[$i];
					}
				}
#				if (/^\s*"(.+)"\s*,\s*"(.+)"\s*,\s*"(.*)"\s*(?:#.*)?$/) {
#					$label = $1;
#					$label = $2 if ($1 eq $NANAME);
#					push @{$var_info{$label}}, $2, $3;
#					push @model_labels, $label;
#				}
				elsif (/^\s*$/) {
					last;
				}
			}
		}
		if (/^\s*ALTERNATIVES\s*(?:#.*)?$/) {
			while (<SET>) {
				s/\r//g;
				if (/^\s*(.+)\s*\t\s*(.+)\s*(?:#.*)?$/) {
					$alt_info{$1}=$2;
					$altidnum++;
				}
				elsif (/^\s*$/) {
					last;
				}
			}
		}
		if (/^\s*CASE\s*(?:#.*)?$/) {
			while(<SET>) {
				s/\r//g;
				if (/^\s*CASENAME\s*="(.+)"\s*(?:#.*)?$/) {
					$curcase=$1;
				}
				elsif (/^\s*CASEPATH\s*="(.+)"\s*(?:#.*)?$/) {
					$case_info{$curcase}{"casepath"}=$1;
				}
				elsif (/^\s*CASESETUP\s*="(.+)"\s*(?:#.*)?$/) {
					$case_info{$curcase}{"casesetup"}=$1;
				}
				elsif (/^\s*CASEDIR\s*="(\/.+)"\s*(?:#.*)?$/) {
					$case_info{$curcase}{"casedir"}=$1;
				}
				elsif (/^\s*CASEFILEH\s*="(\/.+)"\s*(?:#.*)?$/) {
					$case_info{$curcase}{"casefileh"}=$1;
				}
				elsif (/^\s*CASEFILET\s*="(.+)"\s*(?:#.*)?$/) {
					$case_info{$curcase}{"casefilet"}=$1;
				}
				elsif (/^\s*CASEIDS\s*="(.+)"\s*(?:#.*)?$/) {
					my @temp = split ',',$1;
					my $id;
					foreach $id (@temp) {
						push @{$case_info{$curcase}{"caseids"}},"$id";
					}
				}
				elsif (/^\s*$/) {
					last;
				}
			}
		}
	}
	close(SET);
	
	$fmt = "limdep" if (!$fmt);
	$model = "mnl" if (!$model);
	
	if ($verbose) {
		print VER "Parse $setup_file\n";
		print VER "COEFFILE=$cfile\n";
		print VER "TABLEFILE=$tfile\n";
		print VER "COLUMNTABLEFILE=$vfile\n";
		print VER "RESTRFILE=$cmdFile\n";
		print VER "US2COEF_FILE=$us2cFile\n";
		print VER "US2SPEC_FILE$us2sFile\n";
		print VER "FORMAT=$fmt\n";
		print VER "MODEL=$model\n";
		print VER "PMODELID=$pModel_Id\n";
		print VER "PALT=$pAlt\n";
		print VER "PALTNUM=$pAltNum\n";
		print VER "PALTCODES=$pAltCodes\n";
		print VER "PMODEL=$pModel\n";
		print VER "PVARFORM=$pVarForm\n";
		print VER "PSECTERM=$pSecTerm\n";
		print VER "Read information for ";
		print VER $#model_labels+1," variables\n";
		print VER "Read information for ";
		print VER $altidnum," alternative codes\n";
		my $key;
		print VER "Cases: " if %case_info;
		foreach $key (keys %case_info) {
			print VER "$key,";
		}
		print VER "\n";
	}
	
	if (!$cfile && !$tfile && !$vfile && !$cmdFile) {
		print VER 
		"Warning: None of COEFFILE, TABLEFILE, COLUMNTABLEFILE, RESTRFILE defined\n"
			if $verbose;
	}
	if ($fmt ne "limdep" && $fmt ne "sas") {
		print VER "Error: Invalid FORMAT\n" if $verbose;
		close(VER) if $verbose;
		die "Error: Invalid FORMAT\n";
	}
	if ($model ne "mnl" && $model ne "ols") {
		print VER "Error: Invalid MODEL\n" if $verbose;
		close(VER) if $verbose;
		die "Error: Invalid MODEL\n";
	}
	if (!pModel) {
		print VER "Warning: No model location given with PMODEL\n"
			if $verbose;
	}
	if (!@model_labels) {
		print VER "Warning: No coefficient labels given "
			if $verbose;
		print VER "in VARIABLES section\n" if $verbose;
	}
	if ($altidnum && !$pVarForm) {
		print VER "Warning: ALTERNATIVES section " if $verbose;
		print VER "not used without PVARFORM\n" if $verbose;
	}
	if ($pVarForm && !$altidnum) {
		print VER "Warning: PVARFORM given without " if $verbose;
		print VER "an ALTERNATIVES section\n" if $verbose;
	}
	if ($pAltCodes && !$pVarForm) {
		print VER "Error: Alternative codes need PVARFORM\n" if $verbose;
		close(VER) if $verbose;
		die "Error: Alternative codes need PVARFORM\n";
	}
	if (!$pAltCodes && $pvarForm) {
		print VER "Warning: Variable form needs PALTCODES\n" if $verbose;
	}
}

sub initVars {
	my $file = "${path}$inFile";
	my $outline;
	

	$fileLoop++;

	open(INN,"<$file") or 
		die "Can't open $file: $1\n";
	
	if ($cfile) {
		open(OUTC,">>$cfile") or 
			die "Can't open $cfile: $1\n";
			
		if (-z $cfile) {
			$outline = join "\t",@coeff_header;
			print OUTC "#",$outline,"\n";
		}
	}
	if ($tfile) {
		open(OUTT,">>$tfile") or 
			die "Can't open $tfile: $1\n";
	}
	if ($vfile) {
		open(OUTV,">>$vfile") or 
			die "Can't open $vfile: $1\n";

		if (-z $vfile) {
			$outline = join "\t",@vtable_header;
			print OUTV "#",$outline,"\n";
		}
	}
	if ($cmdFile) {
		open(OUTCMD,">$cmdFile") or
			die "Can't open $cmdFile: $1\n";
	}
	
	if (!$cfile && !$tfile && !$vfile && !$cmdFile) {
		if ($verbose) {
			print VER "Error: None of COEFFILE, TABLEFILE,";
			print VER "COLUMNTABLEFILE, RESTRFILE defined.\n";
			close(VER);
		}
		die "Error: None of COEFFILE, TABLEFILE, COLUMNTABLEFILE, RESTRFILE defined.\n";
	}
	
	if ($verbose) {
		close(VER);
		open(VER,">>$myName.log")
			or die "Can't open $myName.log: $1\n";
		print VER "\n=================\n";
		print VER " Run $fileLoop\n";
		print VER "=================\n\n";
		print VER "Processing: $file\n";
	}

}

sub processFile {
	my $resRef;		# see fields in sub readFile

	# Read model input file
	$resRef = readFile();
	
	# Process $resRef and write output tables
	write_files($resRef);
	
#	# Write UrbanSim 2.0 output tables
#	write_urbansim20_output($resRef)
#		if $us2cFile || $us2sFile;

	# Write UrbanSim 2.1 output tables
	write_urbansim21_output($resRef)
		if $us2cFile || $us2sFile;
}

sub postProcess {
	close(INN);
	close(OUTC) if $cfile;
	close(OUTT) if $tfile;
	close(OUTV) if $vfile;
	close(OUTCMD) if $cmdFile;
	close(VER) if ($verbose);
}


###########################
#
# Support subroutines
#

sub readFile {
	# Reads the log files that the user creates with estimation
	# output on Limdep (or possibly SAS for OLS).
	
	my (%res);
	# Fields in %res
	#	"modelid"	the number after $pModel_Id
	#	"alt"		ref to array of strings
	#				each string describes an alternative
	#	"altnum"	number of alternatives (number after $pAltNum)
	#	"altcodes"	ref to a hash keyed by alternative code,
	#					alternative codes are the coefficient
	#					postfixes used to associate them with one or
	#					more alternatives. Each element is an array
	#					of the appropriate equation numbers (0,1,..)
	#					that this code belongs to. 
	#					These numbers are indices into eqids to
	#					get the equation id for each equation.
	#					can be found in 
	#	"eqids"		ref to array of equation ids (alternative ids)
	#					one id per equation. These are read from
	#					the alternative codes section.
	# 
	# 	<Estimation program dependent fields:>
	#
	#	"numobs"	Number of observations used
	#	"logconv"	Log-likelihood at convergence
	#	"logzero"	Log-likelihood at zero
	#	"rhosqrd"	Rho-squared
	#	"adjrho"	Adjusted Rho-squared
	#	"rsqrd"		R-squared
	#	"adjrsqrd"	Adjusted R-squared
	#	"model"		ref to array of hashes
	#				(one hash per variable in model)
	#		"label"		variable label
	#		"coeff"		coefficient
	#		"sterr"		St.err. of the estimated coefficient
	#		"tstat"		t-statistic
	#		"pvalu"		p-value
	
	my ($foundId,$foundAlt,$foundAltNum,$foundAltCodes,
		$foundModel);

	$foundId = 1 if !$pModel_Id;
	$foundAlt = 1 if !$pAlt;
	$foundAltNum = 1 if !$pAltNum;
	$foundAltCodes = 1 if !$pAltCodes;
	$foundModel = 1 if !$pModel;

	# Estimation program independent
	while (<INN>) {
		#
		# find model Id
		#
		if (!$foundId && /$pModel_Id\s+0*(\d+)/i) {
			$res{"modelid"} = $1;
			$foundId++;
			print VER "Found: $pModel_Id $1\n" if $verbose;
		}
		#
		# find alternative descriptions
		#
		if (!$foundAlt && /$pAlt/i) {
			while (<INN>) {
				s/\r//g;
				if (/^$pSecTerm$/) {
					last;
				}
				elsif (/^\s*(\S.*\S)\s*$/) {
					push @{$res{"alt"}}, $1;
				}
				else {
					last;
				}
			}
			
			$foundAlt++;
			print VER "Found: Alternative descriptions\n" if $verbose;
		}
		#
		# find number of alternatives
		#
		if (!$foundAltNum && /$pAltNum:?\s*(\d+)/i) {
			$res{"altnum"} = $1;
			$foundAltNum++;
			print VER "Found: $pAltNum $1\n" if $verbose;
		}
		
		#
		# find alternative codes
		#	this is a mapping between the number of the equation
		#	(i.e. alternative) and the different codes used
		#	on coefficients to indicate to which equation(s) they
		#	belong to. The descriptions of the codes are in the
		#	alternatives section of the Setup file.
		if (!$foundAltCodes && /$pAltCodes/i) {
			$foundAltCodes++;
			print VER "Found: Alternative codes section\n" if $verbose;
			my $i=0;
			while (<INN>) {
				s/\r//g;
				if (/^$pSecTerm$/) {
					last;
				}
				elsif (/^\s*(\S+)\s+(\S+)$/) {
					my @codes = split ',',$2;
					my $equid = $1;
					my ($tempcode,$foundtempcode)=("",0);
					foreach $tempcode (@codes) {
						if ($tempcode eq $equid) {
							$foundtempcode++;
							last;
						}
					}
					unshift @codes, $equid unless $foundtempcode;
					# we only add the code if it is not already
					# on the list to prevent duplicates
					push @{$res{"eqids"}}, $equid;
					my $code;
					foreach $code (@codes) {
						$code =~ tr/[a-z]/[A-Z]/;
						push @{$res{"altcodes"}{$code}}, $i;
					}
					$i++;
				}
				else {
					last;
				}
			}
			$res{"altnum"}=$i if (!$res{"altnum"});
		}
		
		#
		# find model
		#
		if (!$foundModel && /$pModel/i) {
			$foundModel++;
			print VER "Found: Model section\n" if $verbose;
			# Estimation program dependent (i.e. model output)
			my $call = "${fmt}_parseFile_${model}";
			&$call(\%res);

			#if ($fmt eq "limdep") {
			#	limdep_parseFile(\%res);
			#}
			#elsif ($fmt eq "sas") {
			#	sas_parseFile(\%res);
			#}
		}
		last if ($foundId && $foundAlt && $foundModel);
	}
	
	return \%res;
}

sub write_files {
	# Takes an input reference to a model result hash
	# (see sub readFile for field descriptions)
	# Processes the information in the hash and writes
	# it out to the output files.
	
	my $resRef = $_[0];

	my @cOut;
	my @vOut;
	my $i;
	my ($alt,$outline);
	my ($varHashRef,$poss_label,$label);
	my ($cout_i,$cout_i_start,$foundLabel);
	my ($altid,$altdesc,$vardesc);
	my $eqnum = $resRef->{"altnum"};
	my ($t90lim,$t95lim) = (1.645,1.96);
	
	$eqnum = 1 unless $eqnum > 0;	# number of equations is at least 1

	if (($cfile || $vfile) && $eqnum>1 && (!$pVarForm || !$pAltCodes)) {
		if ($verbose) {
		print VER "Warning: Coeff or Column file not produced for multi-equation\n";
		print VER "models without both PVARFORM and PALTCODES\n";
		}
	}

	#
	# Prepare headers
	#
	
	if ($tfile) {
		print OUTT "$pModel_Id $resRef->{\"modelid\"}\n";
		foreach $alt (@{$resRef->{"alt"}}) {
			print OUTT $alt,"\n";
		}
		print OUTT "\n";
		$outLine = join "\t",@table_header;
		print OUTT $outLine,"\n";
	}
	

	#
	# Prepare empty output matrix
	#
	
	if ($cfile || $vfile) {
		$cout_i_start = 0;
		for ($i=0;$i<$eqnum;$i++) {
			if ($pModel_Id) {
				# Form first column in coeff file, model id
				push @{$cOut[$i]},$resRef->{"modelid"} if $cfile;
				push @{$vOut[$i]},$resRef->{"modelid"} if $vfile;
				$cout_i_start++ unless $i;
			}
			if ($pAltCodes) {
				# Form second column in coeff file, equation id
				push @{$cOut[$i]},${$resRef->{"eqids"}}[$i] if $cfile;
				push @{$vOut[$i]},${$resRef->{"eqids"}}[$i] if $vfile;
				$cout_i_start++ unless $i;
			}
			foreach $poss_label (@model_labels) {
				# fill rest of @cOut columns with 0, so that left out
				# variables get the 0 coefficient
				push @{$cOut[$i]},"0" if $cfile;
				push @{$vOut[$i]},"0" if $vfile;
			}
		}
	}
	
	#
	# Prepare model output
	#
	
	foreach $varHashRef (@{$resRef->{"model"}}) {
		# For each variable in the model
		$label = $varHashRef->{"label"};
		$outline = "$label";
		$vardesc = "";
		$altdesc = "";
		if ($pVarForm) {
			$label =~ /^$pVarForm$/;
			$label = $1 if $1;
			$altid = $2;
		}

		$foundLabel=0;
		$cout_i=$cout_i_start;
		foreach $poss_label (@model_labels) {
			# For possible coefficient labels
			# this seeks out the location in @cOut of the current
			# model coefficient
			# this makes sure the coefficients appear in the order
			# given in the setup file
			
			#$poss_label =~ tr/[a-z]/[A-Z]/;
			#$label =~ tr/[a-z]/[A-Z]/;
			$cout_i++;
			next unless ($poss_label eq $label);
			$foundLabel++;
			if (($cfile || $vfile) && $eqnum>1 && $altid) {
				my $eqs;
				foreach $eqs (@{$resRef->{"altcodes"}{$altid}}) {
					$cOut[$eqs][$cout_i-1] = $varHashRef->{"coeff"}
						if $cfile;
					if ($vfile) {
						my ($tmpcoeff,$tmpsterr,$tmptstat,$sign_string);
						$tmpcoeff = round_number($varHashRef->{"coeff"});
						$tmpsterr = round_number($varHashRef->{"sterr"});
						$tmptstat = $varHashRef->{"tstat"};
						if (abs($tmptstat) > $t95lim) {
							$sign_string = "XDDX";
						}
						elsif (abs($tmptstat) > $t90lim) {
							$sign_string = "XDX";
						}
						else {
							$sign_string = "";
						}
#print "After rounding: $tmpcoeff ($tmpsterr)\n";
						$vOut[$eqs][$cout_i-1] = "$tmpcoeff ($tmpsterr)$sign_string";
#print "vout $eqs,$cout_i has: $vOut[$eqs][$cout_i-1]\n";
					#$vOut[$eqs][$cout_i-1] = 
					#	"$varHashRef->{\"coeff\"}  ($varHashRef->{\"sterr\"})"
					#	if $vfile;
					}
				}
			}
			elsif (($cfile || $vfile) && $eqnum==1) {
				$cOut[0][$cout_i-1] = $varHashRef->{"coeff"} if $cfile;
				if ($vfile) {
					my ($tmpcoeff,$tmpsterr,$tmptstat,$sign_string);
					$tmpcoeff = round_number($varHashRef->{"coeff"});
					$tmpsterr = round_number($varHashRef->{"sterr"});
					$tmptstat = $varHashRef->{"tstat"};
					if (abs($tmptstat) > $t95lim) {
						$sign_string = "XDDX";
					}
					elsif (abs($tmptstat) > $t90lim) {
						$sign_string = "XDX";
					}
					else {
						$sign_string = "";
					}
#print "After rounding: $tmpcoeff ($tmpsterr)\n";
					$vOut[0][$cout_i-1] = "$tmpcoeff ($tmpsterr)$sign_string";
#print "vout 0,$cout_i has: $vOut[0][$cout_i-1]\n";
				#$vOut[0][$cout_i-1] = 
				#	"$varHashRef->{\"coeff\"}  ($varHashRef->{\"sterr\"})"
				#	if $vfile;
				}		
			}
			elsif ($cfile || $vfile) {
				print VER "Warning: No alt. code on label $label!\n"
					if $verbose;
			}
			if ($tfile) {
				$vardesc = $var_info{$poss_label}->[$varLegIdx];
				$vardesc = $var_info{$poss_label}->[$cHeadIdx]
					if !$vardesc;
				$vardesc = $label if !$vardesc;
				$outline = "$vardesc";
				if ($pVarForm) {
					$altdesc = $alt_info{$altid};
					$altdesc = $altid if !$altdesc;
					$outline .= "\t$altdesc";
				}
			}
			last;
		}
		if (($cfile || $vfile)) {
			if ($verbose && !$foundLabel) {
				print VER "$pModel_Id $resRef->{\"modelid\"}: ";
				print VER "$label not found in Setup.\n";
			}
		}
		if ($tfile) {
			#$outline .= "\t" if !$altdesc;
			$outline .= "\t$varHashRef->{\"coeff\"}";
			$outline .= "\t$varHashRef->{\"tstat\"}\n";
			print OUTT $outline;
		}
	}
	
	#
	# Have accumulated all output vectors
	#
	
	#
	# Add model statistics and print
	#
	
	if ($vfile) {
		# Add model statistics to end of vfile row
		for ($i=0; $i<$eqnum; $i++) {
				push @{$vOut[$i]}, $resRef->{"numobs"};		#Obs.
				if ($model eq "mnl") {
					push @{$vOut[$i]}, $resRef->{"logzero"};	#Ln(L(0))
					push @{$vOut[$i]}, $resRef->{"logconv"};	#Ln(L(b))
					push @{$vOut[$i]}, $resRef->{"rhosqrd"};	#Rho^2
					push @{$vOut[$i]}, $resRef->{"adjrho"};	#Corr. rho^2
				}
				elsif ($model eq "ols") {
					push @{$vOut[$i]}, $resRef->{"rsqrd"};	#R^2
					push @{$vOut[$i]}, $resRef->{"adjrsqrd"};	#Adj. R^2
				}
		}
	}	

	if ($cfile || $vfile) {
		for ($i=0;$i<$eqnum;$i++) {
			if ($cfile) {
				$outline = join "\t",@{$cOut[$i]};
				print OUTC $outline,"\n";
			}
			if ($vfile) {
				#print "printing vfile coefficients for equation $i\n";
				$outline = join "\t",@{$vOut[$i]};
				print OUTV $outline,"\n";
			}
		}
	}
	if ($tfile) {
		if ($model eq "mnl") {
			print OUTT "Ln(L(0))\t$resRef->{\"logzero\"}\n";
			print OUTT "Ln(L(b))\t$resRef->{\"logconv\"}\n";
			print OUTT "Rho^2\t$resRef->{\"rhosqrd\"}\n";
			print OUTT "Corr. rho^2\t$resRef->{\"adjrho\"}\n";
		}
		elsif ($model eq "ols") {
			print OUTT "R^2\t$resRef->{\"rsqrd\"}\n";
			print OUTT "Adj. R^2\t$resRef->{\"adjrsqrd\"}\n";
		}
		print OUTT "Obs.\t$resRef->{\"numobs\"}\n";
		print OUTT "\n";
	}	
	if ($cmdFile) {
		# Estimation program dependent (i.e. model output)
		if ($fmt eq "limdep" && $model eq "mnl") {
			limdep_writeEst($resRef);
		}
		elsif ($fmt eq "sas") {
			print VER "Writing SAS command files is not supported\n"
				if $verbose;
			print "Writing SAS command files is not supported\n";
		}

	}
}


sub write_urbansim20_output {
	# Takes an input reference to a model result hash
	# (see sub readFile for field descriptions)
	# Processes the information in the hash and writes
	# it out to the output files on UrbanSim 2.0 form
	
	my $resRef = $_[0];

	# uses $us2cFile and $us2sFile;
	
	my @coeff_header = qw/SUB_MODEL_ID EQUATION_ID COEFFICIENT_NAME
		ESTIMATE STANDARD_ERROR T_STATISTIC P_VALUE/;
		
	my @spec_header = qw/SUB_MODEL_ID EQUATION_ID COEFFICIENT_NAME
		VARIABLE_NAME/;

	my ($needHeaderC,$needHeaderS) = (0,0);
	$needHeaderC = 1 unless (-e $us2cFile);
	$needHeaderS = 1 unless (-e $us2sFile);

	open(OUTC,">>$us2cFile")
		or die "Cannot open $us2cFile: $!\n";
	open(OUTS,">>$us2sFile")
		or die "Cannot open $us2sFile: $!\n";

	if ($needHeaderC) {
		print OUTC join "\t",@coeff_header;
		print OUTC "\n";
	}

	if ($needHeaderS) {
		print OUTS join "\t",@spec_header;
		print OUTS "\n";
	}

	my $i;
	my %model;
	my $eqs;
	my $altid;
	my $label;
	my @modelhashrefs = @{$resRef->{"model"}};
	for ($i=0; $i<=$#modelhashrefs; $i++) {
		# For model coefficient labels
		$label = $modelhashrefs[$i]{'label'};
		if ($pVarForm) {
			$label =~ /^$pVarForm$/;
			$label = $1 if $1;
			$altid = $2;
		}
		foreach $eqs (@{$resRef->{"altcodes"}{$altid}}) {
			$model{$label}{$resRef->{'eqids'}[$eqs]} = [
				$var_info{$label}[$us2Idx],$modelhashrefs[$i]{'coeff'},
				$modelhashrefs[$i]{'sterr'},$modelhashrefs[$i]{'tstat'},
				$modelhashrefs[$i]{'pvalu'}];
		}
	}
	# Have created a hash, keyed by label and equation id
	# that contains a reference to an array of
	#	UrbanSim 2.0 variable name, estimate, sterr, tstat, pvalue
	

	my ($poss_label,$foundlabel);
	my (@outcoeffs,@outspec);
	
	foreach $poss_label (@model_labels) {
		# For possible coefficient labels
		foreach $eqs (@{$resRef->{'eqids'}}) {
			# For each possible equation id
		
			if (exists $model{$poss_label}{$eqs}) {
				print OUTC "$resRef->{'modelid'}\t$eqs\t";
				print OUTC join "\t", @{$model{$poss_label}{$eqs}};
				print OUTC "\n";
				
				print OUTS "$resRef->{'modelid'}\t$eqs\t";
				print OUTS "$model{$poss_label}{$eqs}->[0]\t";
				print OUTS "$model{$poss_label}{$eqs}->[0]\n";
			}
			elsif (defined $var_info{$poss_label}[$us2Idx]) {
				print OUTC "$resRef->{'modelid'}\t$eqs\t";
				print OUTC "$var_info{$poss_label}[$us2Idx]\t";
				print OUTC "0\t0\t0\t0\n";
				
				print OUTS "$resRef->{'modelid'}\t$eqs\t";
				print OUTS "$var_info{$poss_label}[$us2Idx]\t";
				print OUTS "$var_info{$poss_label}[$us2Idx]\n";
			
			}
		}
		
	}
	
	close(OUTC);
	close(OUTS);
}

sub write_urbansim21_output {
	# Takes an input reference to a model result hash
	# (see sub readFile for field descriptions)
	# Processes the information in the hash and writes
	# it out to the output files on UrbanSim 2.1 form
	
	my $resRef = $_[0];
	
	my $not_used_code = -2;

	# uses $us2cFile and $us2sFile;
	
	my @coeff_header = qw/SUB_MODEL_ID COEFFICIENT_NAME
		ESTIMATE STANDARD_ERROR T_STATISTIC P_VALUE/;
		
	my @spec_header = qw/SUB_MODEL_ID EQUATION_ID VARIABLE_NAME
		COEFFICIENT_NAME/;

	my ($needHeaderC,$needHeaderS) = (0,0);
	$needHeaderC = 1 unless (-e $us2cFile);
	$needHeaderS = 1 unless (-e $us2sFile);

	open(OUTC,">>$us2cFile")
		or die "Cannot open $us2cFile: $!\n";
	open(OUTS,">>$us2sFile")
		or die "Cannot open $us2sFile: $!\n";

	if ($needHeaderC) {
		print OUTC join "\t",@coeff_header;
		print OUTC "\n";
	}

	if ($needHeaderS) {
		print OUTS join "\t",@spec_header;
		print OUTS "\n";
	}

#	foreach $poss_label (@model_labels) {
	my $i;
	my @modelhashrefs = @{$resRef->{"model"}};
	my $altid;
	my $eqs;
	for ($i=0; $i<=$#modelhashrefs; $i++) {
		# For possible coefficient labels
		my $label = $modelhashrefs[$i]{'label'};
		if ($pVarForm) {
			$label =~ /^$pVarForm$/;
			$label = $1 if $1;
			$altid = $2;
		}
		# print coefficient file
		print OUTC "$resRef->{'modelid'}\t";
#		print OUTC "$resRef->{'eqids'}[$eqs]\t";
		print OUTC "$var_info{$label}[$us2Idx]";
		print OUTC "_$altid" if $altid;
		print OUTC "\t";
		print OUTC "$modelhashrefs[$i]{'coeff'}\t";
		print OUTC "$modelhashrefs[$i]{'sterr'}\t";
		print OUTC "$modelhashrefs[$i]{'tstat'}\t";
		print OUTC "$modelhashrefs[$i]{'pvalu'}\n";
			
		unless (@{$resRef->{"altcodes"}{$altid}}) {
			print OUTS "$resRef->{'modelid'}\t";
			print OUTS "$not_used_code\t";
			print OUTS "$var_info{$label}[$us2Idx]";
			print OUTS "\t";
			print OUTS "$var_info{$label}[$us2Idx]";
			print OUTS "_$altid" if $altid;
			print OUTS "\n";		
		}
		foreach $eqs (@{$resRef->{"altcodes"}{$altid}}) {
#print "$resRef->{'modelid'}\taltid $altid has no $eqs, id $resRef->{'eqids'}[$eqs]\n";
			# print specification file
			print OUTS "$resRef->{'modelid'}\t";
			print OUTS "$resRef->{'eqids'}[$eqs]\t";
			print OUTS "$var_info{$label}[$us2Idx]";
			print OUTS "\t";
			print OUTS "$var_info{$label}[$us2Idx]";
			print OUTS "_$altid" if $altid;
			print OUTS "\n";
		}
	}
	
	close(OUTC);
	close(OUTS);
}


sub prepare_headers {
	my $key;

	# Header for coeff file columns
	#	followed by the coeff_header for
	#	the appropriate coefficients
	push @coeff_header, "${pModel_Id}" if $pModel_Id;
	push @coeff_header, "EqId" if ($pAltCodes);
	foreach $key (@model_labels) {
		push @coeff_header,$var_info{$key}->[$cHeadIdx];
	}

	# Header for verbose column table
	push @vtable_header, "${pModel_Id}" if $pModel_Id;
	push @vtable_header, "EqId" if ($pAltCodes);
	foreach $key (@model_labels) {
		push @vtable_header,$var_info{$key}->[$varLegIdx];
	}

	# Header for table file columns
	if ($pVarForm) {
		@table_header = (
		"Variable","Alternative","Coefficient","t-statistic",
		);
	}
	else {
		@table_header = (
		"Variable","Coefficient","t-statistic",
		);
	}
}


sub round_number {
	my $sign_digits = 3;	# number of significant digits to keep
	my $nopow = 3;	# multiply out exponents less than or equal to this

	my $n;
	$n = $_[0];

	my ($temp,$tempzeros);
	my $div = 10**$sign_digits;
#print "div $div\n";
	my $pow;
	my ($expcode,$expsign,$exppwr);

#print "Rounding $n\n";
	if ($n =~ /^(\+|-)?(\d*\.\d+)(?:(e|E)(\+|-)?(\d+))?$/) {
		$n = "";
		$n .= $1 if $1;
		$temp = $2;
		$expcode = $3;
		$expsign = $4;
		$exppwr = $5;
#print "temp is $temp\n";
		if ($sign_digits > 0) {
			$temp *= $div;
#print "temp is $temp\n";
			$temp += 0.5;
#print "temp is $temp\n";
			$temp = int $temp;
#print "temp is $temp\n";
			$tempzeros = $1 if ($temp =~ /^(?:\+|-)?\d*(0{1,$sign_digits}?)$/);
#print "tempzeros = $tempzeros\n";
			$temp = $temp / $div;
#print "temp is $temp\n";
		}
#gfu
# need to add 0 to string when $temp ends with 0 because it gets dropped
# in the divition
		$n .= $temp;
#print "n is $n\n";
		if ($expcode) {
			$pow = "";
			$pow = $expsign if $expsign;
			$pow .= $exppwr;
			if ($exppwr <= $nopow) {
				$temp = 10**($pow);
				$n *= $temp;
				$n .= $tempzeros if defined($tempzeros);
#print "expanding power: got $n\n";
			}
			else {
				$n .= $tempzeros if defined($tempzeros);
				$n .= $expsign if $expsign;
				$n .= $exppwr;
#print "keeping power: got $n\n";
			}
		}
		else {
			$n .= $tempzeros if defined($tempzeros);
#print "no power: got $n\n";
		}
	}
#print "It became $n\n";	
	return $n;
}
###########################
#
# Estimation software dependent subroutines
#

sub limdep_parseFile_mnl {
	# Limdep dependent
	# Takes a reference to a hash and adds the
	# Limdep dependent fields to it
	# (see sub readFile for field descriptions)

	my $resRef = $_[0];

	my (@coeffs,$i);
	
	#
	# Parse limdep NLOGIT mnl model result
	#
	
	# process model statistics
	while (<INN>) {
		if ( /Number of obs.=\s+(\d+)/i) {
			$resRef->{"numobs"} = $1;
			next;
		}
		if ( /LOG LIKELIHOOD FUNCTION\s+(\S+)\s+/i ) {
			$resRef->{"logconv"} = $1;
			next;
		}
		if ( /CONSTANTS ONLY\s+(.*)/i ) {
			my @temp = split '\s+',$1;
			$resRef->{"logzero"} = $temp[0];
			$resRef->{"rhosqrd"} = $temp[1];
			$resRef->{"adjrho"} = $temp[2];
			next;
		}
		if ( /NO COEFFICIENTS\s+(.*)/i ) {
			my @temp = split '\s+',$1;
			$resRef->{"logzero"} = $temp[0];
			$resRef->{"rhosqrd"} = $temp[1];
			$resRef->{"adjrho"} = $temp[2];
			next;
		}
		last if ( /\|Variable \| Coefficient/i );
		# jumps out when coeff section is found
	}
	
	# process coefficients
	<INN>;	# dumps the limdep partition row
	$i=0;
	while (<INN>) {
		s/\r//g;
		last if /^$pSecTerm$/;
		last if /Note: E\+nn/;
		last unless /^\s*(\w+)\s+(.*)$/;
		# jumps out if we don't find another coefficient
		
		@coeffs = split '\s+',$2;
		# @coeffs = (coefficient,st.error,t-stat,p-value)
		
		my $temp = $1;
		$temp =~ tr/[a-z]/[A-Z]/;
		$resRef->{"model"}[$i]{"label"} = $temp;
		$resRef->{"model"}[$i]{"coeff"} = $coeffs[0];
		$resRef->{"model"}[$i]{"sterr"} = $coeffs[1];
		$resRef->{"model"}[$i]{"tstat"} = $coeffs[2];
		$resRef->{"model"}[$i]{"pvalu"} = $coeffs[3];
		$i++;
	}
}

sub limdep_parseFile_ols {
	# Limdep dependent
	# Takes a reference to a hash and parses
	# an OLS regress command result into the hash fields
	# (see sub readFile for field descriptions)

	my $resRef = $_[0];

	my (@coeffs,$i);
	
	#
	# Parse Limdep REGRESS model result
	#
	
	# process model statistics
	while (<INN>) {
		if ( /Observations =\s*(\d+),/i) {
			$resRef->{"numobs"} = $1;
			next;
		}
		if ( /R-squared=\s+(\S+), Adjusted R-squared =\s+(\S+)\s/i) {
			$resRef->{"rsqrd"} = $1;
			$resRef->{"adjrsqrd"} = $2;
			next;
		}
		last if ( /\|Variable \| Coefficient/i );
		# jumps out when coeff section is found
	}
	
	# process coefficients
	<INN>;	# dumps the limdep partition row
	$i=0;
	while (<INN>) {
		s/\r//g;
		last if /^$pSecTerm$/;
		last unless ( /^\s*(\w+)\s+(.*)$/);
		# jumps out if we don't find another coefficient

		@coeffs = split '\s+',$2;
		# @coeffs = (coefficient,st.error,t-stat,p-value,mean of X)

		my $temp = $1;
		$temp =~ tr/[a-z]/[A-Z]/;
		$resRef->{"model"}[$i]{"label"} = $temp;
		$resRef->{"model"}[$i]{"coeff"} = $coeffs[0];
		$resRef->{"model"}[$i]{"sterr"} = $coeffs[1];
		$resRef->{"model"}[$i]{"tstat"} = $coeffs[2];
		$resRef->{"model"}[$i]{"pvalu"} = $coeffs[3];
		$i++;
	}
}

sub limdep_writeEst {
	# Limdep dependent
	# Takes a reference to a model result hash
	# Prints a Limdep MNL estimation command where
	# all coefficients are restricted to the estimated values.
	
	my $resRef = $_[0];
	
	my @varHashes = @{$resRef->{"model"}};
	my $numVars = $#varHashes+1 if @varHashes;
	my @altStr = @{$resRef->{"alt"}};
	my $numAlts = $#altStr+1 if @altStr;
	
	my ($modelstr,$cholist);
	
	my ($i,$label,$coeff,$varName);

	$cholist = "alt0" if @altStr;
	for ($i=1; $i<$altStr; $i++) {
		$cholist .= ",alt$i";
	}
	$cholist = "insert_choice_list" unless $cholist;
	
	$i=0;
	
	$label = $resRef->{"model"}[$i]{"label"};
	$coeff = $resRef->{"model"}[$i]{"coeff"};
	$varName = $var_info{$label}[$varNameIdx];
	$modelstr = "; model:\nU(${cholist}) =\n $label($coeff)*$varName\n";

	print OUTCMD <<"EOF";
nlogit ; lhs = insert_dependent_var
; choices = $cholist
; maxit=0
EOF
	
	for($i=1;$i<$numVars;$i++) {
		# for each variable in the model
		$label = $resRef->{"model"}[$i]{"label"};
		$coeff = $resRef->{"model"}[$i]{"coeff"};
		$varName = $var_info{$label}[$varNameIdx];
		$modelstr .= "+$label($coeff)*$varName\n";
	}
	print OUTCMD "$modelstr";
	print OUTCMD "\$\n";
}

sub sas_parseFile_ols {
	# SAS dependent
	# Takes a reference to a hash and adds the
	# SAS dependent fields to it by parsing a
	#	SAS OLS model (REG command)
	# (see sub readFile for field descriptions)

	my $resRef = $_[0];

	my (@coeffs,$i);
	
	#
	# Parse SAS model result
	#
	
	# process model statistics
	while (<INN>) {
		if ( /R-Square\s+(\S+)/i) {
			$resRef->{"rsqrd"} = $1;
			next;
		}
		if ( /Adj R-Sq\s+(\S+)/i) {
			$resRef->{"adjrsqrd"} = $1;
			next;
		}
		last if ( /Variable\s+DF\s+Estimate/i );
		# jumps out when coeff section is found
	}
	
	# process coefficients
	<INN>;	# dumps the sas partition row
	$i=0;
	while (<INN>) {
		s/\r//g;
		last if /^$pSecTerm$/;
		if (/The SAS System/i) {
			<INN>; $_ = <INN>;
			if (/The REG Procedure/i) {
				<INN>; <INN>; <INN>; <INN>;
				<INN>; <INN>; <INN>; <INN>;
				next;
			}
			else {
				last;
			}
		}
		last unless ( /^\s*(\w+)\s+(.*)$/);
		# jumps out if we don't find another coefficient

		@coeffs = split '\s+',$2;
		# @coeffs = (df,coefficient,st.error,t-stat,p-value)
		
		my $temp = $1;
		$temp =~ tr/[a-z]/[A-Z]/;
		$resRef->{"model"}[$i]{"label"} = $temp;
		$resRef->{"model"}[$i]{"coeff"} = $coeffs[1];
		$resRef->{"model"}[$i]{"sterr"} = $coeffs[2];
		$resRef->{"model"}[$i]{"tstat"} = $coeffs[3];
		$resRef->{"model"}[$i]{"pvalu"} = $coeffs[4];
		$i++;
	}
}

###########################
#
# Written help files
#

sub helpswitches {
	die
"Usage: perl $myName.pl [switches]
-if [string]\tList of input model files, e.g. \"f1,f2\"
-h\t\tThis help.
-p [string]\tFixed path to model files, e.g. /data
-sf [filename]\tName of setup file.
-v\t\tWrite messages in verbose log (overwrite log).
-help\t\tWrites detailed help in ${myName}_help.log.
-hrun\t\tWrites an interface script in ${myName}_.pl
-ver\t\tWrite messages in verbose log (add to log).
";
}

sub helplong {
	open(OUT,">${myName}_help.log")
		or die "Can't open ${myName}_help.log: $1\n";
	print OUT <<"EOF";
# This document describes the requirements for a estRes run.
#
# A pound sign, #, indicates a comment
#	the rest of a line after # is ignored by the estRes script.
#
# It is easiest to run the estRes script with an interface script.
#	An example of such a script will be written with -hrun
#
# estRes needs two files: Model output file, Setup file
#	The Model output file contains the estimated model output
#	and related information.
#
#	The Setup file contains information about how to find
#	information in the Model output, about the coefficients
#	and the alternatives. This file can actually be used
#	as a basis for a setup file since all non-setup rows
#	have been commented out with #.
#
# The model output (MNL model from Limdep) should be saved to
# a separate file, the Model output file. 
# This file should contain at least 2-3 things in this order:
#	model id
#	alternative descriptions (optional)
#	model output.
#
# Each of the three sections in the model output file should 
# begin with a string on a separate line indicating the
# section. This string is given in the Setup file. Each section
# should be terminated with a empty line or a terminator indicated 
# in the Setup file.
#
# In the model estimation the coefficient labels should follow
# a naming scheme that is consistent.
# If there are no alternative specific variables:
#	The label names are only restricted by the estimation
#		software.
# If there are alternative specific variables:
#	Each coefficient label is separated into two parts
#	The first part is of a fixed length, i.e. the first k letters.
#		It gives the variable name code.
#	The latter part has all the remaining letters of the label.
#		It gives a code for the alternative(s) this coefficient
#		belongs to.
#
#	The "variable name code" is mapped to a variable name and 
#		legend in the VARIABLES section in the Setup file.
#	The code for alternatives is mapped to alternatives in the
#		ALTERNATIVES section in the Setup file.
#
#<begin sample model output file>
#
# Model_type_title Numeric_model_id
#	Sector 1
#
# Alternative descriptions
#	Alternative		Observations
#	1				50
#	2				60
#
# Model section 1
# 	[limdep model output]
#
#<end sample model output file>
#
#
# The following describes the necessary setup file.
# The setup file name is given with -sf and contains commands
# that control the processing of model output.
# Here is a sample setup file with detailed explanations:
#
#<begin sample setup file>
#
# This is a Setup file for estRes
#	a script that reads model output files and 
#	writes cumulative tab delimited tables and coeff files.
#
# In the Setup file # indicates a comment.
# You can not use \\# to avoid it.
#
# UPPERCASE words are commands, described below.
# Some commands begin sections of related commands.
# Such a section is terminated by a blank row.

SETUP
# The SETUP command indicates the beginning of a
# section with various setup commands.
# The section is terminated by a blank row.
#
# These are the section commands:
#
#		At least one of the following filenames must be defined
#		If they are all left out the script does nothing.
#	COEFFILE="filename" for the UrbanSim 1.0 coefficient table
#	TABLEFILE="filename" for the long model after model table
#	COLUMNTABLEFILE="filename" for the model equation by row
#		variables by columns table file
#	RESTRFILE="filename" for the Limdep restricted command file
#	US2COEF_FILE="filename" for UrbanSim 2.0 model_coefficient table 
#	US2SPEC_FILE="filename" for UrbanSim 2.0 model_specification table
#
#	FORMAT="format_code", one of: "limdep","sas". Limdep is default.
#	MODEL="model_code", one of: "mnl","ols". MNL is default.
COEFFFILE=""
TABLEFILE=""
COLUMNTABLEFILE=""
RESTRFILE=""
US2COEF_FILE=""
US2SPEC_FILE=""

FORMAT=""
MODEL=""

PARSERULES
# The PARSERULES command indicates the beginning of a
# section with various parse rule commands.
# The section is terminated by a blank row.
#
# Parse rules give strings that are used to find particular
# sections in a model output file or process the model output.
#
# This is particularly needed if there are more than one
# section with similar information in a file, i.e. two MNL models.
# Then the rule must be able to distinguish between them.
# The sections in the model output file are assumed to be terminated
# by the first blank or illegal row. Illegal rows are those that
# do not fit the pattern for that section.
#
# These are parse rules for Perl, so certain symbols need \
# if they are to be found, since they have meaning in Perl:
#	e.g.: \\( \\) \\{ \\} \\[ \\] \\+ \\* \\? \\.
#
# If a parse rule is left out or it is an empty string
# it will not be used in the search.
#
# Parse rules are assumed to be processed in order.
# The order is:
#	PMODELID, PALT, PMODEL,
#
# It is important that the model output file contain the sections
# in that proper order.
# If a previous parse rule is not found a later one may not be found.
#
# The following rules don't depend on order in output model:
#	PVARFORM, PSECTERM,
#
# Description of parse rules:
# PMODELID="string", locates string in the file and
#	grabs a following number on the same row to give a model id
# PALT="string", locates the section that describes the
#	alternatives. They are assumed to be in the following rows
#	until the first blank row. Columns are assumed tab delimited.
# PALTNUM="string", locates string in the file and grabs the
#	following number on the same row to get the number of alternatives.
# PALTCODES="string", locates string in file and reads the following
#	rows for mappings between the equation number and the alternative
#	codes (that are described in the ALTERNATIVES section).
#	These codes are used as postfixes after coefficients to identify
#	the equation they belong to, and this section maps the code to
#	the actual equation number. The parsing stops at the first blank
#	row. The form of the lines is: equation number alternative code
#	delimited by a tab.
# PMODEL="string", locates the model that should be processed.
#	The model is assumed to be in the first text row below this 
#	header and continue until the first blank row.
# PVARFORM="(pattern_for_variable_name)(pattern_for_alternative_id)"
#	This is used to separate a model coefficient label into
#	the variable name, given in the VARIABLES section, and the
#	alternative identification part, given in the ALTERNATIVES section.
#	The alternative identification is use to tell which alternative
#	this variable belongs to.
# PSECTERM="pattern_for_model_output_section_terminator"
#	This is used in addition to a blank line in the model output
#	file, to determine the end of a section.
#	For example, this tells when to stop after reading model.
PMODELID="Devtype"
PALT="Devtype"
PALTNUM="Number of alternatives:"
PALTCODES="Alternative codes"
PMODEL="Discrete choice \\(multinomial logit\\) model"
PVARFORM="(\\w\\w\\w)(\\w+)"
PSECTERM="=+"

VARIABLES
# The VARIABLES command contains rows, with tab delimited strings.
#	The order of the variables in the rows controls the output order.
#	1st string: Fixed length "variable code" that is used in 
#		the coefficient label in the Model output file,
#		i.e. it does not include the alternative description
#		postfixes that are given in the ALTERNATIVES section.
#		"N/A" is a special name for coefficients that are
#		not in the model, but for which we want output into
#		the tables or coeff files.
#		The 1st string is always required.
#	2nd string: Short name for variable (UrbanSim 1 coeff file column header)
#		Required for -cf, otherwise can be the empty string
#	3rd string: Long description for variable (word table legend)
#		Required for -tf, otherwise can be the empty string
#	4th string: The underlying variable name, which can be
#		distinct from the coefficient label. 
#		Required for -rf, otherwise can be the empty string
#		(can also be left out but that is not recommended)
#	5th	string: UrbanSim 2 variable name
#		Required for UrbanSim 2 output, coefficient table and model
#		specification table
#
BLTSQ	LogSqft	Ln(Total commercial sqft in cell)	LTSQ	ln_commercial_sqft
BLTUN	LogTotUnit	Ln(Total number of units in cell)		ln_residential_units
N/A	NotUsedVar	Description of this variable

ALTERNATIVES
# The ALTERNATIVES command begins a section that contains rows
#	of mappings between the codes for alternatives used as postfixes
#	in coefficient labels and the descriptions of the alternatives.
#	The rows are tab delimited strings with two fields:
#	1st	Coefficient label postfix alternative identifier.
#	2nd	Description of alternatives that correspond to this postfix.
R	Residential locations
M	Mixed use

CASE
# The CASE section contains variables that are used to create the
#	interface script.
# There can be many CASE sections so that the script can process
#	a number of different estimation cases. For example
#	employment location models for different cities.
# The variables in this section are:
#	CASENAME="casename"
#	CASEPATH="path_to_case_from_root"
#	CASESETUP="case_setup_file_name"
#	CASEDIR="/case_directory_name"
#	CASEFILEH="/case_model_output_file_name_header"
#	CASEFILET="case_model_output_file_name_tail"
#	CASEIDS="case_id_1,case_id_2,..."
#
#	These variables define one case. For another case include
#	these variables again with different settings in the same file.
#
#	The cases have short case names, e.g. emp.
#	Each case can have a number of models, each with an ID.
#	The list of IDs belonging to the case are given by CASEIDS
#	A case is stored in a directory given by CASEDIR
#	Within CASEDIR there are subdirectories for each model.
#	The name of the subdirectories is given by {CASEDIR}{id}.
#	The name of a particular model output file is given by
#	{CASEFILEH}{id}{CASEFILET}.
#	The full path to a particular model output file is given by:
#		{CASEPATH}{CASEDIR}{id}{CASEFILEH}{id}{CASEFILET}
#	where id is a particular id from the list CASEIDS.
#	Note that {} are used here for clarity. The names must
#	include / in the appropriate places for the path to work.
#
#	The example case is for employment location with 
#	three models, representing sectors with ids 01,02,03.
#	The full path to the model result file for
#	sector 01 is:
#		c:/mydocu~1/emploc/emp01/result01emp.log
#	The setup file is in the current directory, i.e. from
#		where this script is run.
#
CASENAME="e_emp"
CASEPATH="c:/mydocu~1/emploc"
CASESETUP="emp_setup.dat"
CASEDIR="/emp"
CASEFILEH="/result"
CASEFILET="emp.log"
CASEIDS="01,02,03"

#<end setup file>
EOF
	close(OUT);
	die "Wrote the helpfile: ${myName}_help.log\n";
}

sub helprun {
	my $key;
	my $elem;
	
	open(OUT,">${myName}_.pl")
		or die "Can't open ${myName}.pl: $1\n";
	print OUT <<"EOF";
#!/usr/bin/perl
#
# Perl script to run $myName.pl on a number of input files
# <see $myName.pl for information>

\$estRes = $myName;

# Case switches
\$do_run = 0;

EOF
	if (!$setup_file) {
		print OUT "\$dev=0;\t\t# case \$dev\n";
		print OUT "\$do_run += \$dev;\n";
	}
	else {
		foreach $key (sort keys %case_info) {
			print OUT "\$$key=0;\t\t# case $key\n";
			print OUT "\t\$do_run += \$$key;\n";
		}
	}
	print OUT "\n#Case switches control which case is run\n";
	print OUT <<"EOF";
die "No case switches set to 1"
	if \$do_run == 0;
EOF
	
	# writing the case sections
	print OUT "\n# Case sections\n";
	my $casepath = "casepath";
	my $casesetup = "casesetup";
	my $casedir = "casedir";
	my $casefileh = "casefileh";
	my $casefilet = "casefilet";
	my $caseids = "caseids";
	
	foreach $key (sort keys %case_info) {
		my $i=1;
		my $idstr = "";
		foreach $elem (@{$case_info{$key}{$caseids}}) {
			$idstr .= "\"$elem\",";
			unless ($i % 5) {
				$idstr .= "\n\t\t";
			}
			$i++;
		}
		print OUT <<"EOF";
if (\$$key) {
	\$path = "$case_info{$key}{$casepath}";
	\$setup = "$case_info{$key}{$casesetup}";
	\$fildir = "$case_info{$key}{$casedir}";			# subdir prefix for individual models
	\$filh = "$case_info{$key}{$casefileh}";			# model output file prefix
	\$filt = "$case_info{$key}{$casefilet}";			# model output file postfix
	\@filIds = ($idstr);
	runEstRes();
}

EOF
	}	# end foreach $key
	
	if (!$setup_file) {
		print OUT <<"EOF";
if (\$dev) {
	\$path = "c:/mydocu~1/models/devch";
	\$setup = "estRes_dev.dat";
	\$fildir = "/dev";
	\$filh = "/estres";
	\$filt = "dev.log";
	\@filIds = ("01","02","03","04","05","06",
				"07","09","10","11","12","13",
				"14","15","17","18","19",
				"20","23","24");
	runEstRes();
}

EOF
	}

	print OUT <<"EOF";
# Routine to run the estRes for a particular case
sub runEstRes {
	my (\$files,\$id,\$i);
	\$i=0;
	\$id = "\$filIds[\$i]";
	\$files = "\$fildir\$id\$filh\$id\$filt";
	system("perl \$estRes.pl -p \$path -if \$files -sf \$setup -v");
	for(\$i=1; \$i<\@filIds; \$i++) {
		\$id = "\$filIds[\$i]";
		\$files = "\$fildir\$id\$filh\$id\$filt";
		system("perl \$estRes.pl -p \$path -if \$files -sf \$setup -ver");
	}
}
EOF
	close(OUT);
	die "Wrote the interface script: ${myName}_.pl\n";
}

