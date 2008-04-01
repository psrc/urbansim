#
# Script to change tab delimited text files to comma delimited
#
# Usage: perl tab2csv.pl infile1 ... infile_n
#
# Handles filenames with full or relative path.
#
# set $rmHead to control whether header lines are removed or not
#	0	don't remove first line
#	1	remove first line
#
# Author: Gudmundur Freyr Ulfarsson

$rmHead = 1;
unless (@ARGV) {
	print "Usage: perl tab2csv.pl infile_1.tab ... infile_n.tab\n";
	print "Changes tab delimited files to comma delimited.\n";
	print "Removes first line from files.\n" if $rmHead;
	exit;
}
$files = 0;
while ($inFile = shift @ARGV) {
	# have changed \t to , in zero or more files
	# whose names were given on the command line
	#$inFile =~ tr/A-Z/a-z/;

	@path = split '/',$inFile;
	$filename = pop @path;
	$path = join '/',@path;
	$path .= "/" if @path;
	
	@inFile = split '\.',$filename;
	#print "Copy $inFile to .csv format\n";
	#foreach $filepart (@inFile) {
	#	print "$filepart\t";
	#}
	#print "\n";
	die "$inFile doesn't end with .tab\n" unless $inFile[1] =~ /^tab$/i;
	open(INN,"<$inFile")
		or die "Can't open $inFile: $1\n";

	$outFile = "$inFile[0].csv";
	open(OUT,">${path}${outFile}")
		or die "Can't open $outFile: $1\n";

	$files++;
	if ($rmHead) {
		if (open(HDR,">${path}${inFile[0]}_header.csv") ) {
			unless (defined($_ = <INN>)) {
				close(HDR);
			}
			tr/\t/,/;
			print HDR $_;
			close(HDR);
		}
		else {
			<INN>;
		}
	}
	$nr=0;
	while (<INN>) {
		# have changed tab to , in zero or more lines in current file
		$nr++;
		tr/\t/,/;
		print OUT $_;
	}		
	close(INN);
	close(OUT);
}

