#!/bin/perl
#
# Perl script to set up estimations
#	for the UrbanSim econometric models in Limdep
#
#	Employment,Developer,Household location,Land price
#	for
#	Applied,Research
#	in
#	Eugene,Honolulu,Utah
#
# Author: Gudmundur Freyr Ulfarsson
# All rights reserved
#
###############
#
#

package EstSetup;

$myName = "estSetup";
$w_verbose = $^W;

#
# Run switches and general setup
#

$allowRun	= 1;	# True for this program to run
$verbose	= 1;	# Writes a run log into the verbose log

# Select case and city

$Applied	= 1;
$Research	= 0;

# Uncomment the setup package for the desired city
#	leaving other city packages commented out.
#
#	use SetupEugene;
	use SetupUtah;
#	use SetupHonolulu;

# Select models  (one or more)

$emp		= 0;		# Employment 
$dev		= 1;		# Developer
$hh		= 0;		# Household location
$price		= 0;		# Land price

# Other setup

$getData	= 0;	# Get data files from $getDataDir

$tab2csv	= 0;	# Changes tab files to csv files and removes header
					#	only if csv file is missing
$countObs	= 1;	# Counts observations automatically if needed

$makeTrans	= 1;	# Makes transfile with developer transitions
$groupList	= "[1,2]";	# Columns to group transitions by
$sumList	= "[3,4]";	# Columns to sum on groups

$writeCmds	= 1;	# Writes Limdep command files

$writeCases	= 1;	# Writes an estResulter case file
$casepath	= "//Urban/Data/UrbanEst/Cities/Scripts/EstRes";	# Path to estResulter


###############
#
# Update log:
#
# Updated files to handle overlays and partial covers
# Use casepath and find casefile from city pacage variables
# Count number of columns in countlines and use
#	in $nvar
# Read case specific variables from outside packages
#	through inheritance
# Save csv and tab files to a joint oldData dir for all
#	models within one aux case
# Write verbose log
# Count observations if asked by switch and we have obsfile
#	also on ID mismatch and we have obsfile
# Read observations from obsfile if no @obs given
# Get tab files from data depository, save current tab files
# Get Event Counts from data depository
# Concatenate Event counts and create transition file
# Writes estResulter case file for the cases
# Writes files with missing observations but gives a warning
# Improved STDOUT messages
# Change tab to csv if csv is missing and remove header line
# Only count observations when no obsfile is given or
#	if the data in obsfile causes an ID mismatch
# Added price model
# Sector descriptions in defVars routines
# Added Household location choice model
# Handles research and applied cases at same time
#	have to set up for applied for Honolulu and Utah
# Reads transitions from file
# Reads numbers of observations from file
# Handles research case, 20 employment sectors only
#
###############


###############
#
# Check switches for consistency
# with preconditions
#

die "Not allowed to run!\n" unless $allowRun;

die "Don't set both Applied and Research to 1\n"
	if ($Applied && $Research);
die "You need either Applied or Research set to 1\n"
	if (!$Applied && !$Research);

die "You need to set casepath if writeCases is set\n"
	if (!$casepath && $writeCases);


###############
#
# Verbose log
#

if ($verbose) {
	my $file;
	$file = "${case}_" if $case;
	$file .= "$myName.log";
	open(VER,">$file")
		or die "Can't open verbose log file: $file\n";
	print VER <<"EOF";
# Estimation Setup Verbose Log
#
# Estimation Setup script
# Author: Gudmundur Freyr Ulfarsson

EOF
	close(VER);
}


###############
#
# Process models
#

setGeneral($Applied,$Research);

if ($emp) {
	pv("Employment");
	clearGlobals();
	setupEmp();
	processCase();
}
if ($dev) {
	pv("Development");
	clearGlobals();
	setupDev();
	processCase();
}
if ($hh) {
	pv("Household location");
	clearGlobals();
	setupHh();
	processCase();
}
if ($price) {
	pv("Land price");
	clearGlobals();
	setupPrice();
	processCase();
}


###############
#
# Main program
#

sub processCase {

	# Globals: $id,$dataName,$readName,$varName,$estName,$resName

	# $id	- particular id during a loop
	# $dataName	- Input data filename
	# Limdep command filenames
	# $readName	- reads data
	# $varName	- defines variables
	# $estName	- estimates model
	# $resName	- output result filename
	
	pv("\n==========\nProcessing: $case $model $aux\n");

	if ($model ne "emp" && $model ne "dev"
		&& $model ne "hh" && $model ne "price") {
		die "Invalid model type: $model\n";
	}
	
	# $baseName	- full path to final directory except for last id
	#	$baseName$id - full path to files
	# $success	- Return status from functions
	my ($baseName,$success);
	$baseName = "$path/$fildir";
	
	unless (@ids) {
		$ids[0] = "";
	}
	
	if ($getData && $getDataDir) {
		$success |= getData();
		pv("Didn't find needed data\nExiting") unless $success;
		return 0 unless $success;
	}

	createTrans() 
		if ($makeTrans && $transfileHead && $transfile);

	tab2csv() if $tab2csv;
	
	getObs()
		if ($countObs || !@obs);
	
	writeResCase() if $writeCases;
	
	return 1 unless $writeCmds;
	
	# Define model specific globals
	&{"defVars_$model"};

	$varName = "$path/$varPre$model$cmdTail";
	&{"writeVarCmd_$model"};

	$i = 0;		# must be global
	
	$id = "$ids[$i]";
	$dataName = "$baseName$id/$id$dataTail";
	$readName = "$baseName$id/$readPre$id$model$cmdTail";
	$estName  = "$baseName$id/$estPre$id$model$cmdTail";
	$resName  = "$baseName$id/$resPre$id$model$resTail";
	
	&{"writeReadCmd_$model"};
	&{"writeEstCmd_$model"};
	&{"writeResLog_$model"};
	
	for($i=1; $i<@ids; $i++) {
		$id = "$ids[$i]";
		$dataName = "$baseName$id/$id$dataTail";
		$readName = "$baseName$id/$readPre$id$model$cmdTail";
		$estName  = "$baseName$id/$estPre$id$model$cmdTail";
		$resName  = "$baseName$id/$resPre$id$model$resTail";
	
		&{"writeReadCmd_$model"};
		&{"writeEstCmd_$model"};
		&{"writeResLog_$model"};
	} # end of id loop
	return 1;
}

##############################################
#
# Subroutines

# To sort in numerical order if the inputs are integers
#	otherwise use a string sort
sub numstr {
	if ( ($a =~ /^\d+$/) && ($b =~ /^\d+$/) ) {
		$a <=> $b;
	}
	else {
		$a cmp $b;
	}
}

sub pv {
	# print to the verbose log
	return 0 unless $verbose or $w_verbose;
	
	my $s = $_[0];
	chomp $s;
	
	if ($w_verbose && !$verbose) {
		print "$s\n";
		return 1;
	}

	unless ( open(VER,">>$myName.log") ) {
		print "Verbose write failure for: $s\n";
		return 0;
	}
	
	print VER "$s\n";
	
	close(VER);
	return 1;
}

sub getData {
	# gets data from $getDataDir and puts into current case dir

	return 0 unless $getData and $getDataDir;
		
	pv("Getting data from $getDataDir\n");

	my $success = 0;
	my $id;
	my $i=0;
	
	$success |= getDataFile($ids[$i]);
	for($i=1; $i<@ids; $i++) {
		$success |= getDataFile($ids[$i]);
	}
	# Need to change to csv since we just got tab files
	$tab2csv = 1;
	# Need to recount observations since we got new data
	$countObs = 1;
	
	unless ($transfileHead) {
		pv("Not fetching Event Counts\n");
		return $success;
	}
	pv("Fetching Event Counts\n");
	
	# Copy Event Count files
	
	unless ( opendir(DIR, $getDataDir) ) {
		pv("Can't opendir $getDataDir\n");
		return 0;
	}
	my @path = split '\/',$transfileHead;
	my $basename = pop @path;
	my $path = join '/',@path;
	my @files =	grep { /^(?:$getDataDir\/)?$basename/ && -f }
				map { "$getDataDir/$_" }
				readdir(DIR);
	closedir(DIR);
	$success |= @files;
	my $file;
	foreach $file (@files) {
		# copy event counts
#		pv("Copying $file\n");
		system("cp $file $path");
	}
	# Need to remake transition count
	$makeTrans = 0;
	$makeTrans = 1 if @files;
	return $success;
}

sub getDataFile {

	my $id = $_[0];
	my $oldid;
	my @tail = split '\.',$dataTail;
	my $tabname = "$tail[0].tab";

	my $datapath = "$path/$fildir$id";
	my $dataname = "$datapath/$id$tabname";

	# First check if there is a current tab file\
	#if (-e "$dataname" && $olddir) {
	#	pv("Moving current $id$tabname to $olddir\n");
	#	system("mv $dataname $olddir/$id$tabname");
	#}
	#elsif (-e "$dataname") {
	#	pv("$dataname overwritten\n");
	#}
		
	# Get new tab file
	if ($id =~ /^0(\d)$/) {
		# need to ignore trailing zero in IDs for some
		# data files in data depository
		$oldid = "$1";
	}
	else {
		$oldid = $id;
	}

	$dataname = "$getDataDir/$oldid$tabname";
	if (-e "$dataname") {
		pv("Copying $oldid$tabname to $datapath/$id$tabname\n");
		system("cp $dataname $datapath/$id$tabname");
	}
	else {
		pv("$dataname does not exist\n");
		return 0;
	}
	return 1;
}

sub createTrans {
	# Routine that creates a transition count file $transfile
	# from the basic yearly transition counts pointed to by
	# $transfileHead, using $groupList and $sumList
	
	# Get list of all yearly transition count files
	# using $transfileHead * $transfileTail into $infiles
	
	my (@path,$path,$basename,@files,$file,$infile);
	
	pv("Creating transitions file $transfile\n");

	@path = split '\/',$transfileHead;
	$basename = pop @path;
	$path = join '/',@path;
	
	opendir(DIR, $path)
		or die "Can't opendir $path\n";	
	@files =	grep { /^(?:$path\/)?$basename/ && -f }
				map { "$path/$_" }
				readdir(DIR);
	closedir(DIR);
	unless (@files) {
		pv("Didn't find transition files in: $path");
		return 0;
	}
	
	$infiles = shift @files;
	foreach $file (@files) {
		$infiles .= " $file";
	}
	
	system("perl groupSum.pl $groupList $sumList $transfile $infiles");
	return 1;
}

sub parseTransfile {
	# Reads transition file, that is a compilation of the
	#	event and non-event counts for all years.
	# Returns a ref to a hash, keyed by devtype (olddev),
	#	that contains a hash keyed by newdev
	#		that has a descriptive string appropriate for that transition
	# or return 0 on failure
	#
	# All transitions that have at least $evenCountMin events are
	# included.

	my (%res,@l);
	my ($odIdx,$ndIdx,$eveIdx,$neveIdx) = (0,1,2,3);
	
	# Global:
	$neveId = -1; 
	
	unless ( open(INN,"<$transfile") ) {
		pv("Can't open transition file $transfile\n");
		return 0;
	}
	<INN>;
	while (<INN>) {
		s/[\n\r]//;
		#chomp;
		@l = split ',';
		if ($l[$odIdx] eq $l[$ndIdx]) {
			$res{$l[$odIdx]}{$neveId} =
				"\t$l[$odIdx] to $l[$ndIdx]\tnon-event\t$l[$neveIdx]";		
		}
		next if ($l[$eveIdx]<$eventCountMin);
		if ($l[$odIdx]<23 && $l[$ndIdx]<$l[$odIdx]) {
		    print "Warning: Possibly bad transition: " 
			. $l[$odIdx] . "-->" . $l[$ndIdx] . ".\n";
		}
		$res{$l[$odIdx]}{$l[$ndIdx]} =
			"\t$l[$odIdx] to $l[$ndIdx]\tevent\t$l[$eveIdx]";
	}
	close(INN);
	return \%res;
}

sub tab2csv {
	# Checks the directories correspoinding to @ids
	# to check for csv files, if not found check for tab files
	# if tab files are found create csv files (dumping header line)

	return unless $tab2csv;
		
	pv("Checking data file format\n");
	
	my $i=0;
	tab2csvFile($ids[$i]);
	
	for($i=1; $i<@ids; $i++) {
		tab2csvFile($ids[$i]);
	}	
}

sub tab2csvFile {
	my $id = $_[0];
	my $datapath = "$path/$fildir$id";
	my $dataname = "$datapath/$id$dataTail";
	pv("Searching for datafile: $dataname");
	if (-e "$dataname") {
		# Found current data file
		pv("\tFound\n");
		unless ($getData && $getDataDir) {
			return 0;
		}
		if ($olddir) {
			# saving old csv file if possible
			pv("\tStoring it in $olddir\n");
			system("mv $dataname $olddir/$id$dataTail");
			system("gzip -f9 $olddir/$id$dataTail");
		}
		else {
			pv("\tIt will be overwritten\n");
		}	
	}
	else {
		pv("\tIt does not exist");
	}
	# The data file $id$dataTail does not exist or needs to be
	# updated from a new .tab file
	
	# Check for .tab version
	my @tail = split '\.',$dataTail;
	if ($tail[1] ne "csv") {
		pv("Warning: The data tail does not end in .csv: $dataTail\n");
	}
	my $tabname = "$datapath/$id$tail[0].tab";
	pv("Searching for $tabname\n");
	unless (-e $tabname) {
		pv("\tIt does not exist\n");
		return 0;
	}
	pv("\tChanging it to a .csv file\n");
	system("perl tab2csv.pl $tabname");	
	#if ($olddir) {
	#	# storing this tab file if possible
	#	pv("Moving $tabname to $olddir\n");
	#	system("mv $tabname $olddir/$id$tail[0].tab");
	#}
	system("rm $tabname");
	return 1;
}

sub getObs {
	# If $obsfile does not exist:
	# Counts the number of observations in all available .csv
	# data files and record in $obsfile
	# 
	# Read number of observations for all ids into @obs from $obsfile

	my $files=0;
	my ($obsref,$colref);

	pv("Fetching number of observations");

	unless ($countObs) {
		pv("Reading number of observations from: $obsfile\n");
		($obsref,$colref) = parseNumObs();
		@obs = @$obsref;
		$nvar = $colref->[0];
		return 1 if @obs;
	}
	# $countObs = 1 or we couldn't read observations from $obsfile
	unless ($obsfile) {
		pv("No obsfile is given, cannot count observations\n");
		return 0;
	}
	pv("Creating $obsfile\n");
	unless ( open(OUT,">$obsfile") ) {
		pv("\tCan't create $obsfile\n");
		pv("\tNumber of observations left blank\n");
		pv("\tNumber of variables left blank\n");
		@obs = ();
		$nvar = 0;
		return 0;
	}

	print OUT "File_number,Filename,Lines,Columns\n";
	pv("Counting observations\n");
	my $i=0;
	my ($newobs,$col) = countLines($ids[$i]);
	$files++;
	#push @obs, $newobs;
	print OUT "$files,$ids[$i]$dataTail,$newobs,$col\n";
	for($i=1; $i<@ids; $i++) {
		$files++;
		($newobs,$col) = countLines($ids[$i]);
		#push @obs, $newobs;
		print OUT "$files,$ids[$i]$dataTail,$newobs,$col\n";
	}
	close(OUT);
	($obsref,$colref) = parseNumObs();
	@obs = @$obsref;
	$nvar = $colref->[0];
	return 1 if @obs;
	return 0;
}

sub countLines {
	# Gets an input ID
	# Reads the data file $path/$fildir$id/$id$dataTail
	# and counts all lines in it and returns the line count
	# and the number of columns that are separated by $sep

	my $id = $_[0];
	
	my $sep = ",";
	my $infile = "$path/$fildir$id/$id$dataTail";
	
	unless ( open(INN,"<$infile") ) {
		pv("Can't open $infile\n");
		return ();
	}
	my $nr=0;
	my $col = 0;
	if (defined($_ = <INN>)) {
		# Read first line separately to count columns
		# Assume all lines have same number of columns
		my @linAr = split "$sep";
		$col = $#linAr+1 if @linAr;
		$nr++;
	}
	while (<INN>) {
		# have counted zero or more lines in $infile
		$nr++;
	}
	close(INN);
	return ($nr,$col);
}

sub parseNumObs {
	# Reads a number of observations file that has been created
	# by countLines.pl and returns a ref to array of the number of
	# observations in the order they appear in the file
	# and a ref to array of number of columns in each file

	my (@inline,@obs,@files,@nids,@cols);
	my ($i,$file,$numIdx,$filIdx,$obsIdx,$colIdx);
	
	$numIdx = 0;		# file number in col. 1
	$filIdx = 1;		# filename is in col. 2
	$obsIdx = 2;		# countLines.pl writes number of obs. in col 3.
	$colIdx	= 3;		# number of columns in col. 4

	unless ( open(INN,"<$obsfile") ) {
		pv("Can't open $obsfile\n");
		pv("Warning: Number of observations not read!\n");
		return ();
	}
	<INN>;
	while (<INN>) {
		chomp;
		@inline = split ',';
		push @files,$inline[$filIdx];
		push @obs,$inline[$obsIdx];
		push @cols,$inline[$colIdx];
	}
	close(INN);
	
	# Check if read ids fit with given ids
	foreach $file (@files) {
		$file =~ /^(\d\d?)?$dataTail$/;
		if ($1) {
			push @nids,$1;
		}
		else {
			push @nids,"";
		}
	}
	for ($i=0; $i<@ids; $i++) {
		if ($ids[$i] ne $nids[$i]) {
			pv("$ids[$i] != $nids[$i]: ID mismatch in $obsfile\n");
			return ();
		}
	}
	return (\@obs,\@cols);
}

sub clearGlobals {
	# Routine that clears main globals for a new run

	# processCase globals
	$id = "";
	$dataName = "";
	$readName = "";
	$varName = "";
	$estName = "";
	$resName = "";

	clearCaseGlobals();
}

sub writeResCase {
	
	my $name = "";
	$name .= "$case" if $case;
	$name .= "_$aux" if $aux;
	$name .= "_$model" if $model;

	my $file = "setup";
	$file .= "_$name" if $name;
	$file .= "_v$runId" if $runId;
	$file .= ".dat";

	my $casefile = "";
	$casefile .= "$casepath/" if $casepath;
	$casefile .= "setup";
	$casefile .= "_$case" if $case;
	$casefile .= "_Cases.dat";
	
	open(OUT,">>$casefile")
		or die "Can't open $casefile\n";
	print OUT <<"EOF";
CASE
CASENAME="$name"
CASEPATH="$path"
CASESETUP="$file"
CASEDIR="/$model"
CASEFILEH="/$resPre"
CASEFILET="$model$resTail"
EOF
	print OUT "CASEIDS=\"";
	my $i=0;
	print OUT $ids[$i] if defined($ids[$i]);
	for($i=1; $i<@ids; $i++) {
		print OUT ",$ids[$i]";
	}
	print OUT "\"\n";
	print OUT "\n";
	close(OUT);
	
	pv("Added this case to $casefile\n");
}


###################
#
# Limdep command file write routines
#
###################


###################
#
# Employment models
#

sub writeReadCmd_emp {
	# Basic Limdep read command file
	
	open(OUT,">$readName")
		or die "Can't open read file $readName: $!\n";
	print OUT <<"EOF";
?????????????????????????????
?
? $case
?
? Reading files into projects
?
?
? Field list:
?
?	sector,group,alt_total,alt_num,chosen,gridid,devtype,
?	totsqft,totunits,totval,accpop,accemp,disthwy,cbdtime,airtime,
?	unit600,lvac600,valunit600,
$seccomm
?	
?
??????????????????????????????
?
? Reading data
?

reset \$
read
	; file = "$dataName"
	; nobs = $obs[$i]
	; nvar = $nvar
	; names = sec,gro,alt,aln,cho,gid,dev,
		tsq,tun,tva,apo,aem,dhw,cbt,air,
		uni,lva,val${secsep}
		$secread
\$

????????????????????????????????????????????????????????????????

namelist ;	all = sec,gro,alt,aln,cho,gid,dev,
		tsq,tun,tva,apo,aem,dhw,cbt,air,
		uni,lva,val${secsep}
		$secread
\$
skip \$
dstat ; rhs = all \$

????????????????????????????????????????????????????????????????
?	Field		Description
? ==============================================================
?
?	sec	sector
?	gro	group
?	alt	alt_total
?	aln	alt_num
?	cho	chosen
?	gid	gridid
?	dev	devtype
?	tsq	totSqft
?	tun	totUnits
?	tva	totVal
?	apo	accPop
?	aem	accEmp
?	dhw	distHwy
?	cbt	cbdTime
?	air	airTime
?	uni	unit600
?	lva	lvac600
?	val	valUnit600
$secdesc
EOF
	close(OUT);
	pv("Wrote $readName\n");
}

sub writeVarCmd_emp {
	# Basic Limdep variable definitions command file
	open(OUT,">$varName")
		or die "Can't open var. def. file $varName: $!\n";
	print OUT <<"EOF";
????????????????????????????
?
? $case
?
? Variable definitions
?
?
?
create
; if (tsq>=1) ltsq=log(tsq)	; (else) ltsq=0
; if (tun>=1) ltun=log(tun)	; (else) ltun=0
; if (tva>=1) ltva=log(tva)	; (else) ltva=0
; if (apo>=1) lapo=log(apo)	; (else) lapo=0
; if (aem>=1) laem=log(aem)	; (else) laem=0
; if (dhw>=1) ldhw=log(dhw)	; (else) ldhw=0
; if (uni>=1) luni=log(uni)	; (else) luni=0
; if (lva>=1) llva=log(lva)	; (else) llva=0
; if (val>=1) lval=log(val)	; (else) lval=0
\$
create
; if (dev=1)  d01=1	; (else) d01=0
; if (dev=2)  d02=1	; (else) d02=0
; if (dev=3)  d03=1	; (else) d03=0
; if (dev=4)  d04=1	; (else) d04=0
; if (dev=5)  d05=1	; (else) d05=0
; if (dev=6)  d06=1	; (else) d06=0
; if (dev=7)  d07=1	; (else) d07=0
; if (dev=8)  d08=1	; (else) d08=0
; if (dev=9)  d09=1	; (else) d09=0
; if (dev=10) d10=1	; (else) d10=0
; if (dev=11) d11=1	; (else) d11=0
; if (dev=12) d12=1	; (else) d12=0
; if (dev=13) d13=1	; (else) d13=0
; if (dev=14) d14=1	; (else) d14=0
; if (dev=15) d15=1	; (else) d15=0
; if (dev=16) d16=1	; (else) d16=0
; if (dev=17) d17=1	; (else) d17=0
; if (dev=18) d18=1	; (else) d18=0
; if (dev=19) d19=1	; (else) d19=0
; if (dev=20) d20=1	; (else) d20=0
; if (dev=21) d21=1	; (else) d21=0
; if (dev=22) d22=1	; (else) d22=0
; if (dev=23) d23=1	; (else) d23=0
; if (dev=24) d24=1	; (else) d24=0
\$
create
; dre=d01+d02+d03+d04+d05+d06+d07+d08
; dmi=d09+d10+d11+d12+d13+d14+d15+d16
; dco=d17+d18+d19
; dig=d20+d21+d22+d23
\$
dstat	; rhs=ltsq,ltun,ltva,lapo,laem,
ldhw,luni,llva,lval,
d01,d02,d03,d04,d05,d06,d07,d08,d09,d10,
d11,d12,d13,d14,d15,d16,d17,d18,d19,d20,
d21,d22,d23,d24,dre,dmi,dco,dig
\$
EOF
	close(OUT);
	pv("Wrote $varName\n");
}

sub writeEstCmd_emp {
	# Basic Limdep estimation command file
	
	open(OUT,">$estName")
		or die "Can't open est. file $estName: $!\n";
	print OUT <<"EOF";
??????????????????????????????
?
?	$case
?
?	Limdep command file for logit model
?	of employment location choice.
?
?	Section 1:	MNL
?
?????????????????????????????
? Section 1
?????????????????????????????
? MNL
?
?
skip \$
nlogit ; lhs = cho
; choices = job0,job1,job2,job3,job4,job5,job6,job7,job8,job9
; model:
U(job0,job1,job2,job3,job4,job5,job6,job7,job8,job9) =
?? Btsq*tsq
??+Btun*tun
??+Btva*tva
??+Bapo*apo
??+Baem*aem
??+Bdhw*dhw
 Bltsq*ltsq
+Bltun*ltun
+Bltva*ltva
+Blapo*lapo
??+Blaem*laem
+Bldhw*ldhw
+Bcbt*cbt
+Bair*air
??+Buni*uni
??+Blva*lva
??+Bval*val
+Bluni*luni
+Bllva*llva
+Blval*lval
+Bdmi*dmi
+Bd17*d17
+Bd18*d18
+Bd19*d19
+Bdig*dig
$seccoef
\$
EOF
	close(OUT);
	pv("Wrote $estName\n");
}

sub writeResLog_emp {
	# Basic Limdep result output log file
	my ($newid);
	$newid = $id+0;
	open(OUT,">$resName")
		or die "Can't open result file $resName: $!\n";
	print OUT <<"EOF";
$case

$idType $newid

	Employment location choice model
	Descriptive statistics

Descriptive statistics
<Insert Limdep descriptive statistics here>

Employment location choice model
<Insert Limdep model output here>
EOF
	close(OUT);
	pv("Wrote $resName\n");
}

sub defVars_emp {
	# 
	# Employment model variables
	#
	#	Applied/Research specific
	#
}

###################
#
# Developer models
#

sub writeReadCmd_dev {
	# Basic Limdep read command file
	open(OUT,">$readName")
		or die "Can't open read file $readName: $!\n";
	print OUT <<"EOF";
?????????????????????????????
?
? $case
?
? Reading files into projects
?
?
? Field list:
?
?	OBS,Obs_group,alt_num,GRID_ID,ALT_COUNT,Year,OldDev,NewDev,
?	CHOSEN,event,event_chosen,
?	Total_sqft,Total_units,Acc_pop,Dist_dev,Same,
?	Lagsame,LagRes,LagMix,LagCom,LagInd,LagGov,LagUnits,LagSqft,
?	PctSame,PctRes,PctMix,PctCom,PctInd,PctGov,Lvalue,Green,
?	Add_unit,Add_sqft,Hwy,Art${ovsep}
?	${ovcomm}${plansep}
?	Plantype${parsep}
?	${parcomm}?
?	
?
??????????????????????????????
?
? Reading data
?
?

reset \$
read
	; file = "$dataName"
	; nobs = $obs[$i]
	; nvar = $nvar
	; names = obs,obg,aln,gid,alc,yea,odt,ndt,cho,eve,evc,
		tsq,tun,acp,dis,sam,
		lsa,lre,lmi,lco,lin,lgo,lun,lsq,
		psa,pre,pmi,pco,pin,pgo,lva,gre,
		aun,asq,hwy,art${ovsep}
		${ovread}${plansep}
		pla${parsep}
		${parread}
\$

????????????????????????????????????????????????????????????????

namelist ;	all = cho,eve,
		tsq,tun,acp,dis,sam,
		lsa,lre,lmi,lco,lin,lgo,lun,lsq,
		psa,pre,pmi,pco,pin,pgo,lva,gre,
		aun,asq,hwy,art${ovsep}
		${ovread}${plansep}
		pla${parsep}
		${parread}
\$
skip \$
dstat ; rhs = all \$

?
? Variables that are alternative specific constants and should be
? left out 
?	aun (same number of units added for all observations)
?	asq (same number of sqft added for all observations)

????????????????????????????????????????????????????????????????
? Variable Field	Description
? ==============================================================
?obs	obs		observation number
?obg	obs_group	group number
?aln	alt_num	number of the alternative
?gid	grid_id	grid cell id
?alc	alt_count	number of alternatives
?yea	year		base year, from which transitions start
?odt	olddev	development type in base year
?ndt	newdev	development type in new year
?cho	chosen	0/1 for chosen olddev-newdev transition
?eve	event		0/1 for event alternative
?evc	event_chose	0/1 if event alternative was chosen
?tsq	total_sqft	Total developed sqft within 600 m in base year
?tun	total_units	Total developed number of units within 600 m in base year
?acp	acc_pop	Access to population
?dis	dist_dev	Distance to development (what units?)
?sam	same		0/1 olddev = newdev (event or no-event
?lsa	lagsame	Number of transitions of this type within 600 m
?				in previous three years
?lre	lagres	Number of transitions resulting in residential within 600 m
?				in previous three years
?lmi	lagmix	|| mixed use
?lco	lagcom	|| commercial
?lin	lagind	|| industrial
?lgo	laggov	|| government
?lun	lagunits	Number of residential units added within 600 m in prev. 3 years
?lsq	lagsqft	Number of commercial sqft added within 600 m in prev. 3 years
?psa	pctsame	Percentage of cells of this type within 600 m
?				in base year
?pre	pctres	Percentage of residential type cells within
?				600 m in base year
?pmi	pctmix	Percentage of mixed r/c type cells within
?				600 m in base year
?pco	pctcom	Percentage of commercial type cells within
?				600 m in base year
?pin	pctind	Percentage of industrial type cells within
?				600 m in base year
?pgo	pctgov	Percentage of government type cells within
?				600 m in base year
?lva	lvalue	Land value of this cell in base year
?gre	green		0/1 for vacant cells (devlopable and
?				undevelopable)
?aun	add_unit	Units added to this cell during the transition
?asq	add_sqft	Sqft added to this cell during the transition
?hwy	hwy		0/1 for presence of higway within 300 m of
?				this cell in the base year
$ovdesc
?pla	plantype	Land use plan type	
$pardesc
EOF
	close(OUT);
	pv("Wrote $readName\n");
}

sub writeVarCmd_dev {
	# Basic Limdep variable definitions command file
	open(OUT,">$varName")
		or die "Can't open var. def. file $varName: $!\n";
	print OUT <<"EOF";
????????????????????????????
?
? $case
?
? Variable definitions
?
?
?
create
; if (yea=1977) y77=1	; (else) y77=0
; if (yea=1978) y78=1	; (else) y78=0
; if (yea=1979) y79=1	; (else) y79=0
; if (yea=1980) y80=1	; (else) y80=0
; if (yea=1981) y81=1	; (else) y81=0
; if (yea=1982) y82=1	; (else) y82=0
; if (yea=1983) y83=1	; (else) y83=0
; if (yea=1984) y84=1	; (else) y84=0
; if (yea=1985) y85=1	; (else) y85=0
; if (yea=1986) y86=1	; (else) y86=0
; if (yea=1987) y87=1	; (else) y87=0
; if (yea=1988) y88=1	; (else) y88=0
; if (yea=1989) y89=1	; (else) y89=0
; if (yea=1990) y90=1	; (else) y90=0
; if (yea=1991) y91=1	; (else) y91=0
; if (yea=1992) y92=1	; (else) y92=0
; if (yea=1993) y93=1	; (else) y93=0
\$
$pardef
$plandef
create
; sdi=dis/150
; dst=(1000-dis)/1000
\$
create
; if (tsq>=1) lts=log(tsq) ; (else) lts=0
; if (tun>=1) ltu=log(tun) ; (else) ltu=0
; if (lun>=1) llu=log(lun) ; (else) llu=0
; if (lsq>=1) lls=log(lsq) ; (else) lls=0
; if (lva>=1) llv=log(lva) ; (else) llv=0
; if (aun>=1) lau=log(aun) ; (else) lau=0
; if (asq>=1) las=log(asq) ; (else) las=0
\$
skip \$
dstat	; rhs=y77,y78,y79,y80,y81,y82,y83,y84,y85,y86,y87,y88,y89,
y90,y91,y92,y93,
sdi,dst,psa,pre,pmi,pco,pin,pgo,lts,ltu,llu,lls,llv,lau,las
\$
$pardstat
$plandstat
EOF
	close(OUT);
	pv("Wrote $varName\n");
}

sub writeEstCmd_dev {
	# Basic Limdep estimation command file
	
	my ($altnum,$key,$newid,$i,@eqids,$var,$eqid,@coeffs);
	
	my $mainCodeIdx = 0;	# main code in devToCode
	
	my ($transref,%trans);
	
	if (!$transfile) {
		pv("Can't write developer estimation file without a transfile\n");
		return;
	}
	
	$transref = parseTransfile();
	if (!$transref || ref $transref ne "HASH") {
		pv("Can't write developer estimation file without transitions\n");
		return;
	}
	%trans = %$transref;
	
	$i=0;
	$newid = $id+0;
	$altnum=0;
	foreach $key (keys %{$trans{$newid}}) {
		$altnum++;
		next if ($key eq $neveId || $key eq $newid);
		push @eqids, $key;
	}
	$altnum--;
	@eqids = sort numstr @eqids;
	unshift @eqids, $newid if $trans{$newid}{$newid};
	# pv("Number of alternatives:\t$altnum\n");
	# $altnum is the number of alternatives - 1 
	#	(to subtract the base case)
	
	
	open(OUT,">$estName")
		or die "Can't open est. file $estName: $!\n";
	print OUT <<"EOF";
??????????????????????????????
?
?	$case
?
?	Limdep command file for logit model
?	of development choice.
?
?	Section 1:	MNL
?
?????????????????????????????
? Section 1
?????????????????????????????
? MNL
?
?
skip \$
nlogit ; lhs = cho
EOF

	print OUT "; choices = non";
	for ($i=0; $i<$altnum;$i++) {
		print OUT ",$chovar_dev$eqids[$i]";
	}
	print OUT "\n; model:\nU(non) = 0 /\nU($chovar_dev$eqids[$mainCodeIdx]";
	for ($i=1; $i<$altnum;$i++) {
		print OUT ",$chovar_dev$eqids[$i]";
	}
	print OUT ") =\n";
	
	# model commands

	@coeffs = ();
	print OUT "?eveAL*eve\n";				# event specific constant

	$var = "act";
	foreach $eqid (@eqids) {
		# alternative specific constant
		push @coeffs, "$var$eqid";
	}
	print OUT "+<",join ',',@coeffs;
	print OUT ">\n";

	my $devCodeIdx = 0;
	for ($i=1; $i<@varlist_dev;$i++) {
		@coeffs = ();
		$var = $varlist_dev[$i];
		next unless $var;
		foreach $eqid (@eqids) {
			push @coeffs, "$var$devToCode{$eqid}[$devCodeIdx]";
		}
		print OUT "+<",join ',',@coeffs;
		print OUT ">*$var\n";
	}
	print OUT "\$\n";

	#
	# write unrestricted model
	#
	
	print OUT "\n\n?????????????????????????????\n";
	print OUT "? Unrestricted model\n";
	print OUT "?????????????????????????????\n";
	print OUT "\nnlogit ; lhs = cho\n";
	print OUT "; choices = non";
	for ($i=0; $i<$altnum;$i++) {
		print OUT ",$chovar_dev$eqids[$i]";
	}
	print OUT "\n; model:\nU(non) = 0 /\nU($chovar_dev$eqids[$mainCodeIdx]";
	for ($i=1; $i<$altnum;$i++) {
		print OUT ",$chovar_dev$eqids[$i]";
	}
	print OUT ") =\n";
	
	# model commands
	@coeffs = ();
	print OUT "?eveAL*eve\n";						# event specific constant

	$var = "act";
	foreach $eqid (@eqids) {
		# alternative specific constant
		push @coeffs, "$var$eqid";
	}
	print OUT "+<",join ',',@coeffs;
	print OUT ">\n";

	for ($i=1; $i<@varlist_dev;$i++) {
		@coeffs = ();
		$var = $varlist_dev[$i];
		next unless $var;
		foreach $eqid (@eqids) {
			push @coeffs, "$var$eqid";
		}
		print OUT "+<",join ',',@coeffs;
		print OUT ">*$var\n";
	}
	print OUT "\$\n";
	
	close(OUT);
	pv("Wrote $estName\n");
}

sub writeResLog_dev {
	# Basic Limdep result output log file
	my ($key,$newid,@newdevs,$altnum);
	my (@tempkeys);

	my ($transref,%trans);
	
	if (!$transfile) {
		pv("Can't write developer result file correctly without a transfile\n");
	}
	else {	
		$transref = parseTransfile();
		if (!$transref || ref $transref ne "HASH") {
			pv("Can't write developer result file correctly without transitions\n");
		}
		%trans = %$transref;	
	}

	$newid = $id+0;
	open(OUT,">$resName")
		or die "Can't open result file $resName: $!\n";
	print OUT <<"EOF";
$case

$idType $newid
EOF

	# print non-event info
	print OUT "$trans{$newid}{$neveId}\n" if $transref;
	$altnum=0;
	foreach $key (keys %{$trans{$newid}}) {
		$altnum++;
		next if ($key eq $neveId || $key eq $newid);
		push @tempkeys, $key;
	}
	@tempkeys = sort numstr @tempkeys;
	unshift @tempkeys, $newid if $trans{$newid}{$newid};
	foreach $key (@tempkeys) {
		print OUT "$trans{$newid}{$key}\n";
	}

	print OUT "\nNumber of alternatives:\t$altnum\n";
	print OUT "\nAlternative codes\n";
	print OUT "$neveId\t$baseCode\n";
	foreach $key (@tempkeys) {
		print OUT "$key\t",join ',',@{$devToCode{$key}};
		print OUT "\n";
	}
	
	print OUT <<"EOF";

	Developer model
	Descriptive statistics

Descriptive statistics
<Insert Limdep descriptive statistics here>

Developer model
<Insert Limdep model output here>
EOF
	close(OUT);
	pv("Wrote $resName\n");
}

sub defVars_dev {
	# Defines variables and arrays needed for developer models
	
	$chovar_dev = "t";
	@varlist_dev = (
		"lts","ltu","dst","lsa","lre","lmi",
		"lco","lin","lgo","llu","lls",
		"psa","pre","pmi","pco","pin","pgo",
		"llv","hwy","art",
		@ovlist,
		@parlist,
		"y79",
		"y80","y81","y82","y83","y84","y85","y86",
		"y87","y88","y89",
		"y90","y91","y92","y93",
		@planlist
	);
	
	$baseCode = "Base";
	%devToCode = (
	1 => ['R','AL'],
	2 => ['R','AL'],
	3 => ['R','AL'],
	4 => ['R','AL'],
	5 => ['R','AL'],
	6 => ['R','AL'],
	7 => ['R','AL'],
	8 => ['R','AL'],
	9 => ['M','AL'],
	10 => ['M','AL'],
	11 => ['M','AL'],
	12 => ['M','AL'],
	13 => ['M','AL'],
	14 => ['M','AL'],
	15 => ['M','AL'],
	16 => ['M','AL'],
	17 => ['C','AL'],
	18 => ['C','AL'],
	19 => ['C','AL'],
	20 => ['I','AL'],
	21 => ['I','AL'],
	22 => ['I','AL'],
	23 => ['G','AL'],
	24 => ['V','AL'],
	);

}

###################
#
# Household location models
#


sub writeReadCmd_hh {
	# Basic Limdep read command file

	open(OUT,">$readName")
		or die "Can't open read file $readName: $!\n";
		
	print OUT <<"EOF";
?????????????????????????????
?
? Reading files into projects
?
?
? Field list:
?
?	hhid,group,alt_total,alt_num,chosen,inc,age,size,children,workers,autos,gridid,
?	devtype,totunits,totresval,resimpval,yrbuilt,
?	accemp0,accemp1,accemp2,accemp3,accpop,
?	unit600,valunit600,sqftind600,sqftcom600,sqfttot600,
?	pctres600,pctmix600,pctcom600,pctind600,pctgov600${secsep}
$seccomm
?	disthwy,cbdtime,airtime,lvac600,city
?
?	
?
??????????????????????????????
?
? Reading data
?
?
reset \$
read
	; file = "$dataName"
	; nobs = $obs[$i]
	; nvar = $nvar
	; names = hid,gro,alt,aln,cho,
		inc,age,siz,chi,wor,aut,
		gid,dev,tun,trv,tiv,yrb,
		ae0,ae1,ae2,ae3,apo,
		uni,val,sin,sco,sto,
		pre,pmi,pco,pin,pgo${secsep}
		$secread,
		dhw,cbt,air,lva,cit
\$
namelist ;	all = hid,gro,alt,aln,cho,
		inc,age,siz,chi,wor,aut,
		gid,dev,tun,trv,tiv,yrb,
		ae0,ae1,ae2,ae3,apo,
		uni,val,sin,sco,sto,
		pre,pmi,pco,pin,pgo${secsep}
		$secread,
		dhw,cbt,air,lva,cit
\$
reject ; inc=14 \$
create
	; inccode = inc
\$
recode
	; inc
	; 1 = 2500
	; 2 = 7500
	; 3 = 12500
	; 4 = 17500
	; 5 = 22500
	; 6 = 27500
	; 7 = 32500
	; 8 = 37500
	; 9 = 42500
	; 10= 47500
	; 11= 52500
	; 12= 57500
	; 13= 70000
\$
dstat ; rhs = all \$
????????????????????????????????????????????????????????????????
?	Field		Description
? ==============================================================
?
?	hid	hhid
?	gro	group
?	alt	alt_total
?	aln	alt_num
?	cho	chosen
?	inc	inc
?	age	age
?	siz	size
?	chi	children
?	wor	workers
?	aut	autos
?	gid	gridid
?	dev	devtype
?	tun	totunits - total number of units 
?	trv	totresval - total residential value (land value + improvement value)
?	tiv	resimpval - residential improvement value
?	yrb	yrbuilt - unit year built
?	ae0	accemp0 - access to employment for 0 car households
?	ae1	accemp1 - access to employment for 1 car households
?	ae2	accemp2 - access to employment for 2 car households
?	ae3	accemp3 - access to employment for 3 car households
?	apo	accpop - access to population
?	uni	unit600 - number of units within 600 m
?	val	valunit600 - value/unit within 600 m
?	sin	sqftInd600 - industrial sqft within 600 m
?	sco	sqftCom600 - commercial sqft within 600 m
?	sto	sqftTot600 - total sqft within 600 m
?	pre	pctRes600
?	pmi	pctMix600
?	pco	pctCom600
?	pin	pctInd600
?	pgo	pctGov600
$secdesc
?	dhw	disthwy - distance to highway
?	cbt	cbdtime - CBD time
?	air	airtime - Time to airport
?	lva	lvac600 - land value per acre within 600 m
?	cit	city - 0: 1: 2:
EOF
	close(OUT);
	pv("Wrote $readName\n");
}

sub writeVarCmd_hh {
	# Basic Limdep variable definitions command file
	open(OUT,">$varName")
		or die "Can't open var. def. file $varName: $!\n";
	print OUT <<"EOF";
????????????????????????????
?
? Variable definitions
?
?
?
create
; if (tun>=1) ltun=log(tun)	; (else) ltun=0
; if (trv>=1) ltrv=log(trv)	; (else) ltrv=0
; if (tiv>=1) ltiv=log(tiv)	; (else) ltiv=0
; if (ae0>=1) lae0=log(ae0)	; (else) lae0=0
; if (ae1>=1) lae1=log(ae1)	; (else) lae1=0
; if (ae2>=1) lae2=log(ae2)	; (else) lae2=0
; if (ae3>=1) lae3=log(ae3)	; (else) lae3=0
; if (apo>=1) lapo=log(apo)	; (else) lapo=0
\$
create
; if (uni>=1) luni=log(uni)	; (else) luni=0
; if (val>=1) lval=log(val)	; (else) lval=0
; if (sin>=1) lsin=log(sin)	; (else) lsin=0
; if (sco>=1) lsco=log(sco)	; (else) lsco=0
; if (sto>=1) lsto=log(sto)	; (else) lsto=0
; if (dhw>=1) ldhw=log(dhw)	; (else) ldhw=0
; if (lva>=1) llva=log(lva)	; (else) llva=0
\$
create
; if (dev=1)  d01=1	; (else) d01=0
; if (dev=2)  d02=1	; (else) d02=0
; if (dev=3)  d03=1	; (else) d03=0
; if (dev=4)  d04=1	; (else) d04=0
; if (dev=5)  d05=1	; (else) d05=0
; if (dev=6)  d06=1	; (else) d06=0
; if (dev=7)  d07=1	; (else) d07=0
; if (dev=8)  d08=1	; (else) d08=0
; if (dev=9)  d09=1	; (else) d09=0
\$
create
; if (dev=10) d10=1	; (else) d10=0
; if (dev=11) d11=1	; (else) d11=0
; if (dev=12) d12=1	; (else) d12=0
; if (dev=13) d13=1	; (else) d13=0
; if (dev=14) d14=1	; (else) d14=0
; if (dev=15) d15=1	; (else) d15=0
; if (dev=16) d16=1	; (else) d16=0
; if (dev=17) d17=1	; (else) d17=0
; if (dev=18) d18=1	; (else) d18=0
; if (dev=19) d19=1	; (else) d19=0
\$
create
; if (dev=20) d20=1	; (else) d20=0
; if (dev=21) d21=1	; (else) d21=0
; if (dev=22) d22=1	; (else) d22=0
; if (dev=23) d23=1	; (else) d23=0
; if (dev=24) d24=1	; (else) d24=0
\$
create
; dre=d01+d02+d03+d04+d05+d06+d07+d08
; drel=d01+d02+d03
; drem=d04+d05+d06
; dreh=d07+d08
\$
create
; dmi=d09+d10+d11+d12+d13+d14+d15+d16
; dmil=d09+d10+d11+d12+d13
; dmih=d14+d15+d16
; dcig=d17+d18+d19+d20+d21+d22+d23
\$
create
; if (cit=1) ci1=1	; (else) ci1=0
; if (cit=2) ci2=1	; (else) ci2=0
\$
create
; if (yrb>1994) yrb=1994	; (else) yrb=yrb
\$
create
; uag=1994-yrb
\$
create
; pmico=pmi+pco
; pingo=pin+pgo
\$
?create
?; pre=pre/100
?; pmi=pmi/100
?; pco=pco/100
?; pin=pin/100
?; pgo=pgo/100
?\$
create
; if (aut=0) clae0 = lae0; (else) clae0=0
; if (aut=1) clae1 = lae1; (else) clae1=0
; if (aut=2) clae2 = lae2; (else) clae2=0
; if (aut>=3) clae3 = lae3; (else) clae3=0
\$
create
; if (aut=0) c0lrd = luni; (else) c0lrd=0
; if (aut=1) c1lrd = luni; (else) c1lrd=0
; if (aut=2) c2lrd = luni; (else) c2lrd=0
; if (aut>=3) c3lrd = luni; (else) c3lrd=0
\$
create
; inclsin = inc*lsin
; inclsco = inc*lsco
; inclval = inc*lval
; incltun = inc*ltun
; hc = (inc - trv/(tun*10) ) / 1000
\$
create
; if (hc>0) hct=log(hc+1) ; (else) hct=hc
\$
create
; sizltun = siz*ltun
; sizluni = siz*luni
\$
create
; if (dev>5 & dev<9 & chi=0) r678nc=1	; (else) r678nc=0
; if (dev>8 & dev<17 & chi=0) devmnc=1	; (else) devmnc=0
\$
create
; childn = chi * tun
\$
create
; if (dev>5 & dev<9 & age<40) r678a40=1	; (else) r678a40=0
; if (dev>8 & dev<17 & age<40) devma40=1	; (else) devma40=0
\$
create
; iyb = inc * yrb
\$
create
; etmp = s10+s11+s12
; if (etmp>0) logret = log(etmp)		; (else) logret=0
\$
create
; if (aut<wor) carlret = logret		; (else) carlret=0
\$
create
; if (aut>=wor) cargret = logret		; (else) cargret=0
\$
create
; if (aut<wor) carlmdn = uni			; (else) carlmdn=0
; if (wor=0) accew0h = (ae0+ae1+ae2+ae3)	; (else) accew0h=0
; if (wor>0) accew1h = (ae0+ae1+ae2+ae3)	; (else) accew1h=0
\$
create
; if (aut=0) accec0 = ae0	; (else) accec0=0
\$
create
; if (cho=1) devcho=dev	; (else) devcho=0
\$
skip \$
dstat	; rhs=ltun,ltrv,ltiv,lae0,lae1,lae2,lae3,lapo,
luni,lval,lsin,lsco,lsto,ldhw,llva,
d01,d02,d03,d04,d05,d06,d07,d08,d09,d10,
d11,d12,d13,d14,d15,d16,d17,d18,d19,d20,
d21,d22,d23,d24,dre,drel,drem,dreh,dmi,dmil,dmih,dcig,
ci1,ci2,uag,pre,pmi,pco,pin,pgo,
clae0,clae1,clae2,clae3,c0lrd,c1lrd,c2lrd,c3lrd,
inclsin,inclsco,inclval,incltun,hc,hct,
sizltun,sizluni,
r678nc,devmnc,childn,r678a40,devma40,iyb,logret,
carlmdn,accew0h,accew1h,accec0,
devcho
\$
EOF
	close(OUT);
	pv("Wrote $varName\n");
}

sub writeEstCmd_hh {
	# Basic Limdep estimation command file
	
	open(OUT,">$estName")
		or die "Can't open est. file $estName: $!\n";
	print OUT <<"EOF";
??????????????????????????????
?	Limdep command file for models
?	of household location choice.
?
?????????????????????????????

skip \$
nlogit ; lhs = cho
; choices = un0,un1,un2,un3,un4,un5,un6,un7,un8,un9
; model:
U(un0,un1,un2,un3,un4,un5,un6,un7,un8,un9) =
+Bdrel*drel
+Bdrem*drem
+Bdreh*dreh
+Bdmil*dmil
+Bdmih*dmih
?+Bdcig*dcig
+Bltun*ltun
+Bltrv*ltrv
??+Bltiv*ltiv
??+Buag*uag
??+Blae0*lae0
??+Blae1*lae1
??+Blae2*lae2
??+Blae3*lae3
+Blapo*lapo
+Bluni*luni
+Blval*lval
+Blsin*lsin
+Blsco*lsco
+Blsto*lsto
+Bpre*pre
+Bpmi*pmi
??+Bpmico*pmico
+Bpco*pco
+Bpin*pin
+Bpgo*pgo
?+Bpingo*pingo
$seccoef
+Bldhw*ldhw
+Bcbt*cbt
+Bair*air
+Bllva*llva
??+Bci1*ci1
??+Bci2*ci2
+Bclae0*clae0
+Bclae1*clae1
+Bclae2*clae2
+Bclae3*clae3
+Bc0lrd*c0lrd
+Bc1lrd*c1lrd
+Bc2lrd*c2lrd
+Bc3lrd*c3lrd
+Binclsin*inclsin
+Binclsco*inclsco
+Binclval*inclval
+Bincltun*incltun
??+Bhc*hc
+Bhct*hct
+Bsizltun*sizltun
+Bsizluni*sizluni
+Br678nc*r678nc
+Bdevmnc*devmnc
+Bchildn*childn
+Br678a40*r678a40
+Bdevma40*devma40
+Biyb*iyb
+Blogret*logret
+Bcarlret*carlret
+Bcarlmdn*carlmdn
+Baccew0h*accew0h
+Baccew1h*accew1h
\$
EOF
	close(OUT);
	pv("Wrote $estName\n");
}

sub writeResLog_hh {
	# Basic Limdep result output log file
	open(OUT,">$resName")
		or die "Can't open result file $resName: $!\n";
	print OUT <<"EOF";

	Household location model
	Descriptive statistics

Descriptive statistics
<Insert Limdep descriptive statistics here>

Household location model
<Insert Limdep model output here>
EOF
	close(OUT);
	pv("Wrote $resName\n");
}

sub defVars_hh {
	# 
	# Household location model variables
	#
	#	Applied/Research specific
}


###################
#
# Land price models
#

sub writeReadCmd_price {
	# Basic Limdep read command file
	open(OUT,">$readName")
		or die "Can't open read file $readName: $!\n";
	
	print OUT <<"EOF";
?????????????????????????????
?
? Reading files into projects
?
?
? Field list:
?
?	gridid,devtype,landval,resimpval,nonresimpval,
?	units,sqft,plancode,units600,sqft600,totemp600,
?	avgvalunit600,avglanval600,accpop,accemp1,
?	pctres600,pctmix600,pctcom600,pctind600,pctgov600,
?	pctdev600,disthwy${ovsep}
?	${ovcomm}${parsep}
?	$parcomm
?
??????????????????????????????
?
? Reading data
?
?
reset \$
read
	; file = "$dataName"
	; nobs = $obs[$i]
	; nvar = $nvar
	; names = gid,dev,landval,resival,nrsival,
		units,sqft,pla,units6,sqft6,
		totemp6,avgvalu6,avglval6,accpop,accemp,
		pctres,pctmix,pctcom,pctind,pctgov,pctdev,
		disthwy${ovsep}
		${ovread}${parsep}
		${parread}
\$
namelist ;	all = gid,dev,landval,resival,nrsival,
		units,sqft,pla,units6,sqft6,
		totemp6,avgvalu6,avglval6,accpop,accemp,
		pctres,pctmix,pctcom,pctind,pctgov,pctdev,
		disthwy${ovsep}
		${ovread}${parsep}
		${parread}
\$
recode
	; pla
	; -1 = -999
\$
reject ; landval<1001 \$
skip \$
dstat ; rhs = all \$
????????????????????????????????????????????????????????????????
?	Field		Description
? ==============================================================
?
?	gid	gridid	- gridid
?	dev	devtype	- devtype
?		landval	- Land value
?		totresval - total residential value (land value + improvement value)
?		resival - residential improvement value
?		nrsival	- non-residential improvement value
?		units	- total number of units in cell
?		sqft	- total number of commercial sqft in cell
?		pla		- plancode 1-27
?		unit6	- number of units within 600 m
?		sqft6	- industrial sqft within 600 m
?		totemp6	- total employment within 600 m
?		avgvalu6- average total value (land value,improvement value,
?					non-residential improvement) per unit within 600 m
?		avglval6- average land value per acre within 600 m
?		accpop	- access to population
?		accemp	- access to employment
?		pctres	- percent residential within 600 m
?		pctmix	- percent mixed within 600 m
?		pctcom	- percent commercial within 600 m
?		pctind	- percent industrial within 600 m
?		pctgov	- percent governmental within 600 m
?		pctdev	- Percent developed within 600 m
?		disthwy - distance to highway
$ovdesc
$pardesc
EOF
	close(OUT);
	pv("Wrote $readName\n");
}

sub writeVarCmd_price {
	# Basic Limdep variable definitions command file
	open(OUT,">$varName")
		or die "Can't open var. def. file $varName: $!\n";
	print OUT <<"EOF";
create
;lglval=log(landval+1)
;impval=resival+nrsival
;lgival=log(impval+1)
;lgunit=log(units+1)
;lgsqft=log(sqft+1)
;lgunit6=log(units6+1)
;lgsqft6=log(sqft6+1)
;lgemp6=log(totemp6+1)
\$
create
;lgavu6=log(avgvalu6+1)
;lgavl6=log(avglval6+1)
;lgaccp=log(accpop+1)
;lgacce=log(accemp+1)
;lgpctd=log(pctdev+1)
;lgpctr=log(pctres+1)
;lgpctm=log(pctmix+1)
;lgpctc=log(pctcom+1)
;lgpcti=log(pctind+1)
;lgpctg=log(pctgov+1)
;lghwy=log(disthwy+1)
\$
create
; if (dev=1)  r1=1	; (else) r1=0
; if (dev=2)  r2=1	; (else) r2=0
; if (dev=3)  r3=1	; (else) r3=0
; if (dev=4)  r4=1	; (else) r4=0
; if (dev=5)  r5=1	; (else) r5=0
; if (dev=6)  r6=1	; (else) r6=0
; if (dev=7)  r7=1	; (else) r7=0
; if (dev=8)  r8=1	; (else) r8=0
\$
create
; if (dev=9)  m1=1	; (else) m1=0
; if (dev=10) m2=1	; (else) m2=0
; if (dev=11) m3=1	; (else) m3=0
; if (dev=12) m4=1	; (else) m4=0
; if (dev=13) m5=1	; (else) m5=0
; if (dev=14) m6=1	; (else) m6=0
; if (dev=15) m7=1	; (else) m7=0
; if (dev=16) m8=1	; (else) m8=0
; if (dev=17) c1=1	; (else) c1=0
; if (dev=18) c2=1	; (else) c2=0
; if (dev=19) c3=1	; (else) c3=0
\$
create
; if (dev=20) i1=1	; (else) i1=0
; if (dev=21) i2=1	; (else) i2=0
; if (dev=22) i3=1	; (else) i3=0
; if (dev=23) gv=1	; (else) gv=0
; if (dev=24) vc=1	; (else) vc=0
\$
$pardef
$plandef
create
; res=r1+r2+r3+r4+r5+r6+r7+r8
; mix=m1+m2+m3+m4+m5+m6+m7+m8
; com=c1+c2+c3+i1+i2+i3+gv
\$
create
; if ( disthwy<300)	hwy1=1	; (else) hwy1=0
; if ( 300<disthwy & disthwy<1000)	hwy2=1	; (else) hwy2=0
; if (1000<disthwy & disthwy<2000)	hwy3=1	; (else) hwy3=0
; if (2000<disthwy & disthwy<5000)	hwy4=1	; (else) hwy4=0
; if (5000<disthwy & disthwy<7500)	hwy5=1	; (else) hwy5=0
\$
dstat ; rhs = lglval,impval,lgival,lgunit,
lgsqft,lgunit6,lgsqft6,lgemp6,
lgavu6,lgavl6,lgaccp,lgacce,
lgpctd,lgpctr,lgpctm,lgpctc,lgpcti,lgpctg,
lghwy,r1,r2,r3,r4,r5,r6,r7,r8,m1,m2,m3,m4,
m5,m6,m7,m8,c1,c2,c3,i1,i2,i3,gv,vc,
res,mix,com,hwy1,hwy2,hwy3,hwy4,hwy5
\$
$pardstat
$plandstat

EOF
	close(OUT);
	pv("Wrote $varName\n");
}

sub writeEstCmd_price {
	# Basic Limdep estimation command file
	open(OUT,">$estName")
		or die "Can't open est. file $estName: $!\n";
	my ($ovsep,$parsep) = ("","");
	$ovsep = "," if ($ovcoefr);
	$parsep= "," if ($parcoefr);
	print OUT <<"EOF";
??????????????????????????????
?	Limdep command file for OLS regression model
?	of land price.
?
?
?????????????????????????????
?
?
skip \$
regress 
; lhs = lglval
; rhs = one,
	r2,r3,r4,r5,r6,r8,
	m1,m2,m3,m4,m5,
	c1,c2,c3,
	i1,i2,i3,
	$plancoefr,
	lgival,lgunit,lgunit6,lgemp6,lgacce,
	lgpctr,lgpctm,lgpctc,lgpcti,lgpctg,
	lghwy${ovsep}
	${ovcoefr}${parsep}
	$parcoefr
\$

EOF
	close(OUT);
	pv("Wrote $estName\n");

}

sub writeResLog_price {
	# Basic Limdep result output log file
	open(OUT,">$resName")
		or die "Can't open result file $resName: $!\n";
	print OUT <<"EOF";

	Land price model
	Descriptive statistics

Descriptive statistics
<Insert Limdep descriptive statistics here>

Land price model
<Insert Limdep model output here>
EOF
	close(OUT);
	pv("Wrote $resName\n");
}

sub defVars_price {

}

1;

