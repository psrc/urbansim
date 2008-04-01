#!/usr/bin/perl
#
# Perl script to run estResulter04.pl on a number of input files
# <see estResulter04.pl for information>

$estRes = estResulter04;

# Case switches
$do_run = 0;

$Eugene_app_dev=1;		# case Eugene_app_dev
	$do_run += $Eugene_app_dev;
$Eugene_app_emp=0;		# case Eugene_app_emp
	$do_run += $Eugene_app_emp;
$Eugene_app_hh=0;		# case Eugene_app_hh
	$do_run += $Eugene_app_hh;
$Eugene_app_price=0;		# case Eugene_app_price
	$do_run += $Eugene_app_price;

#Case switches control which case is run
die "No case switches set to 1"
	if $do_run == 0;

# Case sections
if ($Eugene_app_dev) {
	$path = "S:/urban-data/UrbanEst/Cities/Eugene/App/dev";
	$setup = "setup_Eugene_app_dev.dat";
	$fildir = "/dev";			# subdir prefix for individual models
	$filh = "/est09_Res";			# model output file prefix
	$filt = "dev.log";			# model output file postfix
	@filIds = ("01","02","03","04","05",
		"06","07","08","09","10",
		"11","12","13","14","15",
		"16","17","18","19","20",
		"21","22","23","24",);
	runEstRes();
}

if ($Eugene_app_emp) {
	$path = "S:/urban-data/UrbanEst/Cities/Eugene/App/emp";
	$setup = "setup_Eugene_app_emp.dat";
	$fildir = "/emp";			# subdir prefix for individual models
	$filh = "/est09_Res";			# model output file prefix
	$filt = "emp.log";			# model output file postfix
	@filIds = ("00","01","02","03","04",
		"05","06","07","08","09",
		"10","11","12","13","14",
		"15",);
	runEstRes();
}

if ($Eugene_app_hh) {
	$path = "S:/urban-data/UrbanEst/Cities/Eugene/App/hh";
	$setup = "setup_Eugene_app_hh.dat";
	$fildir = "/hh";			# subdir prefix for individual models
	$filh = "/est09_Res";			# model output file prefix
	$filt = "hh.log";			# model output file postfix
	@filIds = ();
	runEstRes();
}

if ($Eugene_app_price) {
	$path = "S:/urban-data/UrbanEst/Cities/Eugene/App/price";
	$setup = "setup_Eugene_app_price.dat";
	$fildir = "/price";			# subdir prefix for individual models
	$filh = "/est09_Res";			# model output file prefix
	$filt = "price.log";			# model output file postfix
	@filIds = ();
	runEstRes();
}

# Routine to run the estRes for a particular case
sub runEstRes {
	my ($files,$id,$i);
	$i=0;
	$id = "$filIds[$i]";
	$files = "$fildir$id$filh$id$filt";
	system("perl $estRes.pl -p $path -if $files -sf $setup -v");
	for($i=1; $i<@filIds; $i++) {
		$id = "$filIds[$i]";
		$files = "$fildir$id$filh$id$filt";
		system("perl $estRes.pl -p $path -if $files -sf $setup -ver");
	}
}
