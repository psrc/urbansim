#!/usr/local/bin/perl -w
@lines = `perldoc -u -f atan2`;
foreach (@lines) {
	s/\w<([^>]+)>/\U$1/g;
	print;
}

