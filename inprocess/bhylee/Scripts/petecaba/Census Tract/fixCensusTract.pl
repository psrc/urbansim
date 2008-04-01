# script that changes census tract codes 

# Describe cases
# 1 changes non-decimal census tract codes that always
#	contain 2 decimal digits without .
#	and pads with 0 on left
#	example 23400 becomes 0234
#	example 2303 becomes 0023.03
# 2 change decimal census tract codes to pad them
#	with 0 on left

$test = 0;
$cases = 2;

$censusindex = 3;

if ($test) {
	$inputfile = "fixCensusTract-$cases.tst";
	$outputfile = "fixCensusTract-$cases.out";
}
else {
	$inputfile = "Honolulu_Vacancy_Rate_input.csv";
	$outputfile = "Honolulu_Vacancy_Rate_done.csv";
}

##### End setup
# Begin program

$runsub = "do_work_$cases";

# open input
open(INP,"<$inputfile")
	or die "cannot open $inputfile: $!\n";

# open output
open(OUT,">$outputfile")
	or die "cannot open $outputfile: $!\n";


if (defined($header = <INP>)) {
	$header =~ s/\015?\012//g;
	print OUT "$header\n";
	@row = split ",",$header;
	$columns=$#row+1;
	
}

while ($_ = <INP>) {
	# for each row in input 
	# print $_;
	$_ =~ s/\015?\012//g;
	
	@row = split ",",$_;

	for (my $i=0; $i<$columns; $i++) {
		$row[$i]=""
			if !defined($row[$i]);
	}
	
	$tract = $row[$censusindex]; 
	
	# print "tract:${tract}:\n" if !defined($tract);
	
	# fix census tract code
	$tract = &$runsub($tract);
	
	# write fixed row to output
	$row[$censusindex] = $tract;
	$outline = join ",",@row;
	print OUT "$outline\n";
}

# close input and output

close(INP);

close(OUT);

### Begin subroutines


sub do_work_1 {
# from 4522 and 123400 into standard form 
# 0045.22 and 1234
	my $tract = shift @_;
	my $newtract = "";
	# print "from $tract\n";
	
	# return $newtract if !defined($tract);
	
	#change 4522 into 0045.22
	$newtract = "$1.$2"
		if $tract =~ /^"(\d\d\d\d)(\d\d)"$/;
	$newtract = "0$1.$2"
		if $tract =~ /^"(\d\d\d)(\d\d)"$/;
	$newtract = "00$1.$2"
		if $tract =~ /^"(\d\d)(\d\d)"$/;
	$newtract = "000$1.$2"
		if $tract =~ /^"(\d)(\d\d)"$/;

	#change 1234.00 into 1234
	$newtract = "$1"
		if $newtract =~ /^(\d\d\d\d)\.00$/;	
		
	if (!$newtract) {
		warn "Empty new tract code for $tract.\n";
		$newtract = "0000";
	}
	
	$newtract = "\"$newtract\"";
	# print "to $newtract\n";
	
	return $newtract;
	
}

sub do_work_2 {
# from 45.22 and 12 into standard form 
# 0045.22 and 0012

	my $tract = shift @_;
	my $newtract = "";

	if ($tract =~ /^"?(\d\d\d)(\.\d\d)?"?$/) {
		$newtract = "0$1";
		$newtract .= "$2" if ($2);
	}			
	elsif ($tract =~ /^"?(\d\d)(\.\d\d)?"?$/) {
		$newtract = "00$1";
		$newtract .= "$2" if ($2);
	}			
	elsif ($tract =~ /^"?(\d)(\.\d\d)?"?$/) {
		$newtract = "000$1";
		$newtract .= "$2" if ($2);
	}		
	elsif ($tract =~ /^"?(\d\d\d\d)(\.\d\d)?"?$/) {
		$newtract = $tract;
	}			

	if (!$newtract) {
		warn "Empty new tract code for $tract.\n";
		$newtract = "0000";
	}

	$newtract = "\"$newtract\"";
	return $newtract;
}
