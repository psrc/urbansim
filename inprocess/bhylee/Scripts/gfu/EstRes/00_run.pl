#!/usr/bin/perl
system("rm -f *.tab *.log");
$errors = 0;
system("perl 00_Utah_.pl");

#@models = qw/dev emp hh landprice resland/;
@models = qw/dev/;

foreach $model (@models) {
	if ($model eq "dev") {
		$name10="Development";
		$name20="developer";
	}
	elsif ($model eq "emp") {
		$name10="EmploymentLocation";
		$name20="employment_location_choice";
	}
	elsif ($model eq "hh") {
		$name10="ResidentialLocation";
		$name20="household_location_choice";
	}
	elsif ($model eq "landprice") {
		$name10="LandPrice";
		$name20="land_price";
	}
	elsif ($model eq "resland") {
		$name10="";
		$name20="residential_land_share";
	}
	$errors++ if system("diff Expected_${name10}Res.txt ${name10}Res.tab > testRes.log");
	$errors++ if system("diff Expected_${name10}Coeffs.txt ${name10}Coeffs.tab > testCoeffs.log");
	$errors++ if system("diff Expected_${name10}ColRes.txt ${name10}ColRes.tab > testColRes.log");
	$errors++ if system("diff Expected_${name20}_model_coefficients.txt ${name20}_model_coefficients.tab > test_coeffs.log");
	$errors++ if system("diff Expected_${name20}_model_specification.txt ${name20}_model_specification.tab > test_spec.log");
	if (-s "testRes.log") {
		warn "Long Result table acceptance test failed for $model\n";
		$errors++;
	}
	if (-s "testColRes.log") {
		warn "Matrix Result table acceptance test failed for $model\n";
		$errors++;
	}
	if (-s "testCoeffs.log") {
		warn "UrbanSim 1.0 coeff table acceptance test failed for $model\n";
		$errors++;
	}
	if (-s "test_coeffs.log") {
		warn "UrbanSim 2.0 coeff table acceptance test failed for $model\n";
		$errors++;
	}
	if (-s "test_spec.log") {
		warn "UrbanSim 2.0 specification table acceptance test failed for $model\n";
		$errors++;
	}

}

if ($errors) {
	warn "\nUnsuccessful run\nExamine logs\n";
}
else {
	#system("rm testRes.log testCoeffs.log testColRes.log test_coeffs.log test_spec.log");
	print "Success: All tests passed!\n";
}


