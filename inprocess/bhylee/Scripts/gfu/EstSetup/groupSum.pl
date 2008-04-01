#
# Script to group on columns, sum columns, in multiple files
#
# Usage: perl groupSum.pl [group list] [sum list] outfile infile1 ... infile_n
#
# Handles filenames with full or relative path.
#
# set $rmHead to control whether header lines are ignored or not
#	0	don't ignore first line
#	1	ignore first line
#
# Author: Gudmundur Freyr Ulfarsson

my $rmHead = 1;
unless (@ARGV>3) {
	print "Usage: perl groupSum.pl [group list] [sum list] outfile infile_1 ... infile_n\n";
	print "Groups on columns and sums.\n";
	print "Ignores first line from files.\n" if $rmHead;
	exit;
}

my %result = ();

my $groupList = shift @ARGV;
my $sumList = shift @ARGV;
my $outFile = shift @ARGV;

open(OUT,">$outFile")
	or die "Can't open outfile: $outFile\n";

$groupList =~ s/\[|\]//g;
$sumList =~ s/\[|\]//g;

my @groups = split ',',$groupList;
my @sums = split ',',$sumList;

my $files = 0;
my $ref;
while ($inFile = shift @ARGV) {
	# have processed zero or more files in @ARGV

	my @path = split '/',$inFile;
	my $filename = pop @path;
	my $path = join '/',@path;
	$path .= "/" if @path;
	
	open(INN,"<$inFile")
		or die "Can't open infile: $inFile\n";

	$files++;
	if ($rmHead) {
		$_ = <INN>;
		chomp;
		tr/\t/,/;
		if ($files == 1) {
			my @header = split ',';
			my $sumcol;
			foreach $sumcol (@sums) {
				$header[$sumcol-1] = "Sum of $header[$sumcol-1]";
			}
			my $outline = join ',',@header;
			print OUT "$outline\n";
		}
	}
	my $nr=0;
	while (<INN>) {
		# processed zero or more lines in <INN>
		$nr++;
		chomp;
		tr/\t/,/;
		my @cols = split ',';
		
##print OUT "$nr:\t$_\n";
		
		$ref = \%result;
		my $i;
		for($i=0; $i<@groups-1; $i++) {
			# have stepped down zero or more grouped-by columns
			# in the result hash, each is key level
			$ref = \%{$ref->{$cols[$groups[$i]-1]}};
##print OUT "$nr:$i:$groups[$i]:key: $cols[$groups[$i]-1]\n";
		}
##print OUT "\t$i:$groups[$i]:key: $cols[$groups[$i]-1]\n";
		
		$ref = \@{$ref->{$cols[$groups[$i]-1]}};
		
		$i=0;
		my $sumcol;
		foreach $sumcol (@sums) {
			$ref->[$i] += $cols[$sumcol-1];
##print OUT "\t$ref->[$i],";
			$i++;
		}
##print OUT "\n\n";
		
	}	
	close(INN);
}

# Print %results

$ref = \%result;
printResults($ref,"");

close(OUT);

#
# End main program
#

sub printResults {
	my $ref = $_[0] if ref $_[0];
	my $string = $_[1];
	
	my (@keys,@sums);

	@keys = keys %$ref if ref $ref eq "HASH";
	@sums = @$ref if ref $ref eq "ARRAY";
	
	if (@keys) {
		my $key;
		foreach $key (sort numerically @keys) {
			# print OUT "key $key,";
			printResults($ref->{$key},"${string}$key,");
		}
	}
	elsif (@sums) {
		my $sum;
		$sum = shift @sums;
		$string .= "$sum";
		foreach $sum (@sums) {
			$string .= ",$sum";
		}
		$string .= "\n";
		print OUT "$string";
		$string = "";
	}
	else {
		print "Error while printing results\n";
	}
}

sub numerically { $a <=> $b; }

