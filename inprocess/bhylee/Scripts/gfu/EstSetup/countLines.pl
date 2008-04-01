#
# Script to count lines, i.e. observations, in files give on the command line
# 	The script also counts $sep delimited columns
#
# perl countLines.pl outfile infile1 ... infile_n
#
# set $rmHead to control whether header lines are counted or not
#	zero	count first line
#	1	don't count first line
#
# Author: Gudmundur Freyr Ulfarsson

$rmHead = 0;
$sep = "\t";

unless (@ARGV) {
	print "Usage: perl countLines.pl outfile infile_1 ... infile_n\n";
	print "Counts lines in all infiles and returns results in outfile.\n";
	print "Doesn't count first line in files.\n" if $rmHead;
	exit;
}
print "Doesn't count first line in files.\n" if $rmHead;

$outFile = shift @ARGV;

open(OUT, ">$outFile")
	or die "Can't open $outFile: $1\n";
print OUT "File_number,Filename,Lines,Columns\n";

$files = 0;
while ($inFile = shift @ARGV) {
	# have counted lines in zero or more files
	# whose names were given on the command line

	print "Counting lines in: $inFile\n";

	open(INN, "<$inFile")
		or die "Can't open $inFile: $1\n";
	$files++;
	$col = 0;
	if ($rmHead) {
		<INN>;
	}
	$nr=0;
	
	if (defined($_ = <INN>)) {
		# Read first line separately to count columns
		# Assume all lines have same number of columns
		my @linAr = split "$sep";
		$col = $#linAr+1 if @linAr;
		$nr++;
	}
	
	while (<INN>) {
		# have counted zero or more lines in the current file
		$nr++;
	}		
	close(INN);

	print OUT "$files,$inFile,$nr,$col\n";
}

close(OUT);

