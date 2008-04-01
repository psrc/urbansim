package SetupUtah;

	require Exporter;
	@ISA = qw(Exporter);
	@EXPORT = qw(
	setGeneral setupEmp setupDev setupHh setupPrice
	setFilenames setEmploymentSectors setPlantypes
	clearCaseGlobals
	$home_path $getDataDir $cmdTail $resTail
	$readPre $varPre $estPre $resPre
	$case $model $idType $fildir $dataTail
	$aux $path $base $olddir @ids @obs $obsfile
	$runId $nvar
	$transfileHead $transfileTail $transfile
	$eventCountMin
	$seccomm $secread $secdesc $seccoef $secsep
	$ovcomm	$ovread	$ovdesc @ovlist $ovcoefr $ovsep
	$parcomm $parread $pardesc $pardef $pardstat 
	@parlist $parcoefr $parsep
	$plandef $plandstat $plancoefr @planlist $plansep
	);


# Basic settings
#	$home_path	Path to top level directory, used by $path to
#				create full path to models
#	$getDataDir	Path to input data from UrbanSim Exporter
#				All necessary data for models must be there.
#
#	$cmdTail	Tail of command files for estimation files
#	$resTail	Tail for resulting model files
#
# Prefixes for filenames
#	$readPre	- Prefix for read data filename
#	$varPre	- -- define variables filename
#	$estPre	- -- estimation filename
#	$resPre	- -- result filename
#
# Case details
#	$case	- Descriptive name of case, printed in comment section
#				at top of files
#	$model	- Code for model type: "emp", "dev", "hh"
#	$idType	- Type of ID, "Sector" for employment, "Devtype" for dev
#	$fildir	- prefix of individual model dir (ID tail is left out)
#	$dataTail Name of input data file, prefixed ID left out
#	$aux	- Auxiliary code for sub-case type: "app","res"
#	$path	- Full path through case dir to overall model dir
#	$base	- Full path to model base dir that stores various files
#	$olddir	- Full path to dir that stores old files
#	@ids	- Array of individual model ids
#	@obs	- Array of number of observations in each individual model
#	$obsfile  Full path and filename to a number of observations file
#				that has been created with countLines.pl
#				If given this creates @obs
#	$runId	- Id number added to command files
#	$nvar		(number of variables, changes depending on 
#				number of employment sectors and plantypes)
#
# Developer models
#	$transFileHead	Full path and filename prefix (before id) of
#				the transition count yearly files
#				(they are moved from the getDataDir to this
#				location)
#	$transFileTail	.tab	ending of transition filenames.
#	$transfile Full path and filename to a file listing the developer event
#				transition counts summed for all years.
#	$eventCountMin	- Minimum number of events for transition
#						to be included in transfile
# Employment sectors
#	$seclist	(sector list for Limdep read command comment)
#	$sectors	(sector list for Limdep read command)
#	$secdesc	(sector list for Limdep field description)
#	$seccoef	(sector coefficients for Limdep MNL command)
#	$secsep		(Separator in Limdep)
# Overlays
#	$ovcomm		(Limdep read comment)
#	$ovread		(Limdep read)
#	$ovdesc		(Limdep read description)
#	@ovlist		(Developer model list of overlay var names)
#	$ovcoefr	(Limdep REGRESS coeff list)
#	$ovsep		(Separator in Limdep)
# Partials
#	$parcomm	(Limdep read comment)
#	$parread	(Limdep read)
#	$pardesc	(Limdep read description)
#	$pardef		(Change partials to percentages in vardef)
#	$pardstat	(Partials DSTAT command)
#	@parlist	(Developer model list of partials var names)
#	$parcoefr	(Limdep REGRESS coeff list)
#	$parsep		(Separator in Limdep)
# Plantypes
#	$plandef	(Limdep plantype dummy var definitions)
#	$plandstat	(Plantype dummy var list for DSTAT)
#	$plancoefr	(plantype coeffs for Limdep REGRESS command)
#	@planlist	(Developer model list of plan dummy var names)
#	$plansep	(Separator in Limdep)

sub setGeneral {
	$Applied = shift;
	$Research = shift;
	
	$home_path	= "//Urban/Data/UrbanEst/Cities";
	$getDataDir	= "//Urban/Data/InputData/AppliedUtah/Scenarios/Default/Output";

	$cmdTail  	= ".lim";	# Tail of command files
	$resTail	= ".log";	# Tail of output result log files
	
	$sep		= ",";		# Limdep variable separator
}

sub setupEmp {
	$case = "Utah";
	$model = "emp";
	$idType = "Sector";
	$fildir = $model;
	$dataTail = "emplocest.csv";

	if ($Applied) {
		$aux = "app";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		#@ids = ( "11" );
		#@obs = ( "50000" );
		@ids = (	"01","02","03","04","05","06","07",
					"08","09","10","11","12","13","14"
		);
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "32";
	}
	if ($Research) {
		$aux = "app";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		@ids = ( "11" );
		@obs = ( "50000" );
		#@ids = (	"01","02","03","04","05","06","07",
		#			"08","09","10","11","12","13","14",
		#			"15","16","17","18","19","20");
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "38";
	}
	setFilenames();
	setEmploymentSectors();
}

sub setupDev {
	$case = "Utah";
	$model = "dev";
	$idType = "OldDev";
	$fildir = $model;
	$dataTail = "estdata.csv";
	
	if ($Applied) {
		$aux = "app";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		@ids = (	"09","17"	);
		#@ids = (	"01","02","03","04","05","06","07","08",
#					"09","10","11","12","13","14","15","16",
#					"17","18","19","20","21","22","23","24");
		#$obsfile = "$base/numObs.log";
		$obsfile = "$base/numObs090and17.log";
		$runId = "0";	# ID of the run
		#$nvar = "42";
		
		$transfileHead = "$base/EventCount/Event";
		$transfileTail = ".tab";
		$transfile = "$base/TransitionCount.csv";
		#$transfile = "$base/TransitionCount24.csv";
		$eventCountMin = 30;
		
	}
	if ($Research) {
		$aux = "res";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		#@ids = (	"18"	);
		#@obs = (	1467	);
		#@ids = (	"01","02","03","04","05","06","07","08",
		#			"09","10","11","12","13","14","15","16",
		#			"17","18","19","20","21","22","23","24");
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "42";
		
		$transfileHead = "$base/EventCount/Event";
		$transfileTail = ".tab";
		$transfile = "$base/TransitionCount.csv";
		$eventCountMin = 10;

	}
	setFilenames();
	#setOverlays();
	setPartials();
	setPlantypes();
}

sub setupHh {
	$case = "Utah";
	$model = "hh";
	$idType = "OldDev";
	$fildir = $model;
	$dataTail = "HHLocEst.csv";
	
	if ($Applied) {
		$aux = "app";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		#@ids = (	"01"	);
		#@obs = (	1467	);
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "47";
	}
	if ($Research) {
		$aux = "res";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		#@ids = (	"01"	);
		#@obs = (	1467	);
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "53";
	}
	setFilenames();
	setEmploymentSectors();
}

sub setupPrice {
	$case = "Utah";
	$model = "price";
	$idType = "OldDev";
	$fildir = $model;
	$dataTail = "PriceAdjEst.csv";
	
	if ($Applied) {
		$aux = "app";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		#@ids = (	"01"	);
		#@obs = (	1467	);
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "27";
	}
	if ($Research) {
		$aux = "res";
		$path = "$home_path/$case/$aux/$model";
		$base = "$path/${model}Base";
		$olddir = "$home_path/$case/$aux/oldData";
		#@ids = (	"01"	);
		#@obs = (	1467	);
		$obsfile = "$base/numObs.log";
		$runId = "0";	# ID of the run
		#$nvar = "27";
	}
	setFilenames();
	#setOverlays();
	setPartials();
	setPlantypes();
}

sub setFilenames {
	# Prefixes for filenames
	# $readPre	- Prefix for read data filename
	# $varPre	- -- define variables filename
	# $estPre	- -- estimation filename
	# $resPre	- -- result filename

	$readPre  = "est${runId}1_Read";
	$varPre   = "est${runId}2_VarDef";
	$estPre   = "est${runId}4_";
	$resPre   = "est${runId}9_Res";
}

sub setEmploymentSectors {
	# 
	# Used in Emp and Hh models
	#
	#	Applied/Research specific
	#
	#	$seccomm	(sector list for Limdep read command comment)
	#	$secread	(sector list for Limdep read command)
	#	$secdesc	(sector list for Limdep field description)
	#	$seccoef	(sector coefficients for Limdep MNL command)
	#	$secsep		(Separator in Limdep)

	if ($Applied) {
		$seccomm = "?	sec1_600,sec2_600,sec3_600,sec4_600,sec5_600,
?	sec6_600,sec7_600,sec8_600,sec9_600,sec10_600,sec11_600,
?	sec12_600,sec13_600,sec14_600";
		$secread = "s01,s02,s03,s04,s05,s06,s07,
		s08,s09,s10,s11,s12,s13,s14";
		$secdesc = "?	s01	sec1_600
?	s02	sec2_600
?	s03	sec3_600
?	s04	sec4_600
?	s05	sec5_600
?	s06	sec6_600
?	s07	sec7_600
?	s08	sec8_600
?	s09	sec9_600
?	s10	sec10_600
?	s11	sec11_600
?	s12	sec12_600
?	s13	sec13_600
?	s14	sec14_600";
		$seccoef = "+Bs01*s01
+Bs02*s02
+Bs03*s03
+Bs04*s04
+Bs05*s05
+Bs06*s06
+Bs07*s07
+Bs08*s08
+Bs09*s09
+Bs10*s10
+Bs11*s11
+Bs12*s12
+Bs13*s13
+Bs14*s14";
	}
	elsif ($Research) {
		$seccomm = "?	sec1_600,sec2_600,sec3_600,sec4_600,sec5_600,
?	sec6_600,sec7_600,sec8_600,sec9_600,sec10_600,sec11_600,
?	sec12_600,sec13_600,sec14_600,sec15_600,sec16_600,
?	sec17_600,sec18_600,sec19_600,sec20_600";
		$secread = "s01,s02,s03,s04,s05,s06,s07,
		s08,s09,s10,s11,s12,s13,s14,s15,
		s16,s17,s18,s19,s20";
		$secdesc = "?	s01	sec1_600
?	s02	sec2_600
?	s03	sec3_600
?	s04	sec4_600
?	s05	sec5_600
?	s06	sec6_600
?	s07	sec7_600
?	s08	sec8_600
?	s09	sec9_600
?	s10	sec10_600
?	s11	sec11_600
?	s12	sec12_600
?	s13	sec13_600
?	s14	sec14_600
?	s15	sec15_600
?	s16	sec16_600
?	s17	sec17_600
?	s18	sec18_600
?	s19	sec19_600
?	s20	sec20_600";
		$seccoef = "+Bs01*s01
+Bs02*s02
+Bs03*s03
+Bs04*s04
+Bs05*s05
+Bs06*s06
+Bs07*s07
+Bs08*s08
+Bs09*s09
+Bs10*s10
+Bs11*s11
+Bs12*s12
+Bs13*s13
+Bs14*s14
+Bs15*s15
+Bs16*s16
+Bs17*s17
+Bs18*s18
+Bs19*s19
+Bs20*s20";
	}
	$secsep = $sep;
}


sub setOverlays {
	# Used in Dev, Price
	#
	#	$ovcomm		(Limdep read comment)
	#	$ovread		(Limdep read)
	#	$ovdesc		(Limdep read description)
	#	@ovlist		(Developer model list of overlay var names)
	#	$ovcoefr	(Limdep REGRESS coeff list)
	#	$ovsep		(Separator in Limdep)
	
	$ovcomm = "FLOOD,SLOPE,STREAM,UGB,WETLAND";
	$ovread = "flo,slo,str,ugb,wet";
	$ovdesc = "?art	art		0/1 for presence of arterial within 300 m of
?				this cell in the base year
?flo	flood		0/1 if this cell is in a flood plane
?slo	slope		0/1 if this cell is on a slope
?str	stream	0/1 if this cell is close to a stream ...
?ugb	ugb		0/1 if within urban growth boundary
?wet	wetland	0/1 if this cell is close to a wetland";
	@ovlist = (
	"flo","slo","str","ugb","wet"
	);
	$ovcoefr = "flo,slo,str,ugb,wet";
	$ovsep = $sep;
	
}


sub setPartials {
	# Used in Dev, Price
	#
	#	$parcomm		(Limdep read comment)
	#	$parread		(Limdep read)
	#	$pardesc		(Limdep read description)
	#	$pardef			(Change partials to percentages in vardef)
	#	$pardstat		(Partial percentage dstats
	#	@parlist		(Developer model list of partials var names)
	#	$parcoefr		(Limdep REGRESS coeff list)
	#	$parsep			(Separator in Limdep)

	$parcomm = "PartialWater,PartialRiparian,PartialFlood,
?	PartialWetland,PartialSlope,PartialOpen,PartialPublic,
?	PartialRoads";

	$parread = "pwa,pri,pfl,pwe,psl,pop,ppu,pro";
	$pardesc = "?pwa	PartialWater	0-25 Number of sub-cells that are
?					covered by water
?pri	PartialRiparian	0-25 # covered by animal sanctuary
?pfl	PartialFlood	0-25 # covered by flood plane
?pwe	PartialWetland	0-25 # covered by wetland
?psl	PartialSlope	0-25 # covered by slope
?pop	PartialOpen		0-25 # covered by open space
?ppu	PartialPublic	0-25 # covered by public space
?pro	PartialRoads	0-25 # covered by roads";
	$pardef = "create
; cwa = pwa/25
; cri = pri/25
; cfl = pfl/25
; cwe = pwe/25
; csl = psl/25
; cop = pop/25
; cpu = ppu/25
; cro = pro/25
\$";
	$pardstat = "dstat ; rhs=
cwa,cri,cfl,cwe,csl,cop,cpu,cro
\$";
	@parlist = (
	"cwa","cri","cfl","cwe","csl","cop","cpu","cro"
	);
	$parcoefr = "cwa,cri,cfl,cwe,csl,cop,cpu,cro";
	$parsep = $sep;
}

sub setPlantypes {
	# 
	# Used in Dev and Price models
	#
	#	$plandef	(Limdep plantype dummy var definitions)
	#	$plandstat	(Plantype dummy var list for DSTAT)
	#	$plancoefr	(plantype coeffs for Limdep REGRESS command)
	#	$planlist	(Developer model list of plan dummy var names)
	#	$plansep	(Separator in Limdep)
	
	$plandef = "create
; if (pla=1)  p01=1 ; (else) p01=0
; if (pla=2)  p02=1 ; (else) p02=0
; if (pla=3)  p03=1 ; (else) p03=0
; if (pla=4)  p04=1 ; (else) p04=0
; if (pla=5)  p05=1 ; (else) p05=0
; if (pla=6)  p06=1 ; (else) p06=0
; if (pla=7)  p07=1 ; (else) p07=0
; if (pla=8)  p08=1 ; (else) p08=0
; if (pla=9)  p09=1 ; (else) p09=0
; if (pla=10) p10=1 ; (else) p10=0
\$
";
	$plandstat = "dstat ; rhs=
p01,p02,p03,p04,p05,p06,p07,p08,p09,p10
\$";
	$plancoefr = "p01,p02,p03,p04,p05,p06,p07,p08,p09,p10";
	@planlist = (
		"p01","p02","p03","p04","p05","p06",
		"p07","p08","p09","p10"
		);
	$plansep = $sep;
}

sub clearCaseGlobals {
	# Routine that clears case specific
	# globals for a new run
	# Initial globals
	$case		= "";
	$model		= "";
	$idType		= "";
	$fildir		= "";
	$dataTail	= "";

	$aux			= "";
	$path			= "";
	$base			= "";
	$olddir			= "";
	@ids			= ();
	@obs			= ();
	$obsfile		= "";
	$transfileHead	= "";
	$transfileTail	= "";
	$transfile		= "";
	$eventCountMin	= "";
	$runId			= "";
	$nvar			= "";

	# Employment sector
	$seclist	= "";
	$sectors	= "";
	$secdesc	= "";
	$seccoef	= "";
	$secsep		= "";
	
	# Overlays
	$ovcomm		= "";
	$ovread		= "";
	$ovdesc		= "";
	@ovlist		= ();
	$ovcoefr	= "";
	$ovsep		= "";

	# Partials
	$parcomm	= "";
	$parread	= "";
	$pardesc	= "";
	$pardef		= "";
	$pardstat	= "";
	@parlist	= ();
	$parcoefr	= "";
	$parsep		= "";

	
	# Plantypes
	$plandef	= "";
	$plandstat	= "";
	$plancoefr	= "";
	$planlist	= "";
	$plansep	= "";
	
	
	# Filenames
	$readPre  = "";
	$varPre   = "";
	$estPre   = "";
	$resPre   = "";
}

1;

