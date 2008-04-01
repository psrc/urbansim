#!/usr/bin/perl

# development_types
#+---------------------+--------------------+-----------+-----------+----------+----------+----------------------+
#| DEVELOPMENT_TYPE_ID | NAME               | MIN_UNITS | MAX_UNITS | MIN_SQFT | MAX_SQFT | PRIMARY_USE          |
#+---------------------+--------------------+-----------+-----------+----------+----------+----------------------+
#|                   1 | R1                 |         1 |         1 |        0 |      999 | Residential          |
#|                   2 | R2                 |         2 |         4 |        0 |      999 | Residential          |
#|                   3 | R3                 |         5 |         9 |        0 |      999 | Residential          |
#|                   4 | R4                 |        10 |        14 |        0 |     2499 | Residential          |
#|                   5 | R5                 |        15 |        21 |        0 |     2499 | Residential          |
#|                   6 | R6                 |        22 |        30 |        0 |     2499 | Residential          |
#|                   7 | R7                 |        31 |        75 |        0 |     4999 | Residential          |
#|                   8 | R8                 |        76 |     65000 |        0 |     4999 | Residential          |
#|                   9 | M1                 |         1 |         9 |     1000 |     4999 | Mixed Use            |
#|                  10 | M2                 |        10 |        30 |     2500 |     4999 | Mixed Use            |
#|                  11 | M3                 |        10 |        30 |     5000 |    24999 | Mixed Use            |
#|                  12 | M4                 |        10 |        30 |    25000 |    49999 | Mixed Use            |
#|                  13 | M5                 |        10 |        30 |    50000 |  9999999 | Mixed Use            |
#|                  14 | M6                 |        31 |     65000 |     5000 |    24999 | Mixed Use            |
#|                  15 | M7                 |        31 |     65000 |    25000 |    49999 | Mixed Use            |
#|                  16 | M8                 |        31 |     65000 |    50000 |  9999999 | Mixed Use            |
#|                  17 | C1                 |         0 |         9 |     5000 |    24999 | Commercial           |
#|                  18 | C2                 |         0 |         9 |    25000 |    49999 | Commercial           |
#|                  19 | C3                 |         0 |         9 |    50000 |  9999999 | Commercial           |
#|                  20 | I1                 |         0 |         9 |     1000 |    24999 | Industrial           |
#|                  21 | I2                 |         0 |         9 |    25000 |    49999 | Industrial           |
#|                  22 | I3                 |         0 |         9 |    50000 |  9999999 | Industrial           |
#|                  23 | GV                 |         0 |         9 |     1000 |  9999999 | Government           |
#|                  24 | Vacant Developable |         0 |         0 |        0 |        0 | Vacant Developable   |
#|                  25 | Undevelopable      |         0 |         0 |        0 |        0 | Vacant Undevelopable |
#+---------------------+--------------------+-----------+-----------+----------+----------+----------------------+

# cells
#	id	units	csqft	isqft	gsqft	devtype
#	1	1		0		0		0		1
#	2	1		500		0		0		1
#	3	1		1000	0		0		9  
#	4	0		500		0		0		17

# Globals

@dt = read_devtype_table();
@cells = read_cells_table();
@types = classify();

suite();

###
#
# Program

sub read_devtype_table {
	open(INN,"<$0")
		or die "Cannot open $0: $!\n";
	
	my @header;
	my $header;
	my $temp;
	my $i=0;
	my $j=0;
	my $found = 0;
	while (<INN>) {
		$found = /^\s*#\s*development_types\s*$/;
		last if $found;
	}
	if ($found) {
		<INN>;
		$header = <INN>;
		chomp $header;
		$header =~ tr/[A-Z]/[a-z]/;
		
		@header = split /\s*\|\s*/,$header;
		shift @header;
		
		<INN>;
	}
	else {
		close(INN);
		return ();
	}

	$j=0;
	while (<INN>) {
		last if (/-----/ || /^\s*$/);
		chomp;
		my @fields = split /\s*\|\s*/;
		shift @fields;
		$i=0;
		foreach $temp (@header) {
			$dt[$j]{$temp} = $fields[$i];
			$i++;
		}
		$j++;
	}
	close(INN);
	return @dt;
}

sub read_cells_table {
	open(INN,"<$0")
		or die "Cannot open $0: $!\n";
	
	my @header;
	my $header;
	my $temp;
	my $i=0;
	my $j=0;
	my $found = 0;
	while (<INN>) {
		$found = /^\s*#\s*cells\s*$/;
		last if $found;
	}
	if ($found) {
		$header = <INN>;
		chomp $header;
		$header =~ tr/[A-Z]/[a-z]/;
		
		@header = split /\s+/,$header;
		shift @header;
	}
	else {
		close(INN);
		return ();
	}

	$j=0;
	while (<INN>) {
		last if /^\s*$/;
		chomp;
		my @fields = split /\s+/;
		shift @fields;
		$i=0;
		foreach $temp (@header) {
			$cells[$j]{$temp} = $fields[$i];
			$i++;
		}
		$j++;
	}
	close(INN);
	return @cells;
}

sub classify {
	my @types;
	my $cell;

	foreach $cell (@cells) {
		push @types, classify_cell($cell);
	}
	return @types;
}

sub classify_cell {
	my $cell = shift;
	my $type = -1;
	my ($id,$units,$csqft,$isqft,$gsqft) 
		= ($cell->{'id'},$cell->{'units'},
			$cell->{'csqft'},$cell->{'isqft'},$cell->{'gsqft'});

	my $primary_sqft_use = 'commercial';
	if ($isqft > $csqft && $isqft > $gsqft) {
		$primary_sqft_use = 'industrial';
	}
	elsif ($gsqft > $csqft && $gsqft > $isqft) {
		$primary_sqft_use = 'governmental';
	}
		
	print "Classifying cell $id, with (ucig) $units, $csqft, $isqft, $gsqft,";
	print " primary sqft $primary_sqft_use.\n";
	my @matching_dt;
	foreach $dt (@dt) {
		my $unitmatch = 0;
		my $csqftmatch = 0;
		my $isqftmatch = 0;
		my $gsqftmatch = 0;
		
		if ($units >= $dt->{'min_units'} &&
				$units <= $dt->{'max_units'}) {
			$unitmatch++;
			print "\tFound unit match in devtype $dt->{'development_type_id'}\n";
		}
		
		if ($primary_sqft_use eq 'commercial' && $csqft >= $dt->{'min_sqft'} &&
				$csqft <= $dt->{'max_sqft'}) {
			$csqftmatch++;
			print "\tFound csqft match in devtype $dt->{'development_type_id'}\n";
		}
		if ($primary_sqft_use eq 'industrial' && $isqft >= $dt->{'min_sqft'} &&
				$isqft <= $dt->{'max_sqft'}) {
			$isqftmatch++;
			print "\tFound isqft match in devtype $dt->{'development_type_id'}\n";
		}
		if ($primary_sqft_use eq 'governmental' && $gsqft >= $dt->{'min_sqft'} &&
				$gsqft <= $dt->{'max_sqft'}) {
			$gsqftmatch++;
			print "\tFound gsqft match in devtype $dt->{'development_type_id'}\n";
		}
		if ($unitmatch && ($isqftmatch || $gsqftmatch)) {
			push @matching_dt, $dt;
			print "\tFound unit and sqft match in devtype $dt->{'development_type_id'}\n";
		}
		
	}

	if (scalar @matching_dt == 1) {
		print "\tFound unique match\n";
		$type = $matching_dt[0]->{'development_type_id'};
	}
	elsif (scalar @matching_dt > 1) {
		print "\tFound multiple matches\n";
	}
	
	print "\tClassified into devtype $type\n";
	return $type;
}

###
#
# Tests

sub suite() {
	my $fails = 0;
	my $tests = 0;
	my @out = ();

	#print_arrayhash(@dt);
	#print_arrayhash(@cells);
	
	@out = test_read_dt();
	$fails += $out[0];
	$tests += $out[1];
	
	@out = test_read_cells();
	$fails += $out[0];
	$tests += $out[1];
	
	@out = test_classify();
	$fails += $out[0];
	$tests += $out[1];
	
	print "$fails/$tests: Failures/Tests\n";
	print "PASS\n" unless $fails;
	print "FAIL\n" if $fails;
}

sub print_arrayhash {
	my $row;
	my $field;
	foreach $field (sort keys %{$_[0]}) {
		print "$field\t";
	}
	print "\n";
	foreach $row (@_) {
		foreach $field (sort keys %{$row}) {
			print "$row->{$field}\t";
		}
		print "\n";
	}
}

sub test_read_dt {
	print "test_read_dt\n";
	my $maxdevtypeid = 25;
	my $devtypeidname = 'development_type_id';
	
	my $temp;
	my $i=0;
	my $fails = 0;
	my $tests= 0;
	my @expected = sort qw/development_type_id name 
		min_units max_units min_sqft max_sqft primary_use/;
	foreach $temp (sort keys %{$dt[0]}) {
		if ($temp ne $expected[$i]) {
			$fails++;
			print "\tExpected $expected[$i] but was $temp.\n";
		}
		$i++;
	}
	$tests += $i;
	
	$i=0;
	foreach $temp (@dt) {
		$i++;
		if ($i != $temp->{$devtypeidname}) {
			$fails++;
			print "\tExpected devtype $i but found $temp->{$devtypeidname}.\n";
		}
	}
	$tests += $i;
	
	if ($i != $maxdevtypeid) {
		$fails++;
		print "\tExpected maximum devtype id $maxdevtypeid but found $i.\n";
	}
	$tests++;
	
	print "\t$fails/$tests: test_read_dt failures/tests\n";
	return ($fails,$tests);
}

sub test_read_cells {
	print "test_read_cells\n";
	my $fails = 0;
	my $tests = 0;
	my $temp;
	
	my $i=0;
	my @expected = sort qw/id units csqft isqft gsqft devtype/;
	foreach $temp (sort keys %{$cells[0]}) {
		if ($temp ne $expected[$i]) {
			$fails++;
			print "\tExpected $expected[$i] but was $temp.\n";
		}
		$i++;
	}
	$tests += $i;

	$i=0;
	foreach $temp (@cells) {
		$i++;
	}
	if ($i <= 0) {
		$fails++;
		print "\tExpected 1 or more cells but found $i.\n";
	}
	$tests++;
	
	print "\t$fails/$tests: test_read_cells failures/tests\n";
	return ($fails,$tests);
}

sub test_classify {
	print "test_classify\n";
	my $fails = 0;
	my $tests = 0;
	my $i;
	my $cell;
	
	my $expected_field = 'devtype';
	
	$i=0;
	foreach $cell (@cells) {
		if ($types[$i] != $cell->{$expected_field}) {
			$fails++;
			print "\tCell ID $cell->{'id'} expected $cell->{$expected_field}";
			print " but was $types[$i].\n";
		}
		$i++;
	}
	$tests += $i;
	
	print "\t$fails/$tests: test_classify failures/tests\n";
	return ($fails,$tests);
}