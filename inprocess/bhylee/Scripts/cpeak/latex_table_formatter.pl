# This is a script of hacks intended to reformat a csv table into a specific format
# for use in latex.  It should probably never be used again in future projects,
# and is recorded here for historical purposes only.

use lib qw(/projects/urbansim7/cpeak/perl_mysql/cpan/lib/perl5/site_perl/5.6.1/i386-linux);
use strict;

# Set local path to check out to, work in, and commit from
my $working_path_csv = "/projects/urbansim7/scratch/csv";#"/projects/urbansim7/cpeak/DataQuality/exported_indicators";
my $working_path_tex = "/projects/urbansim7/scratch/tex";#"/projects/urbansim7/cpeak/DataQuality/exported_indicators";
my $repository_root = "/projects/urbansim2/repository";
my $repository_path_csv = "Website/projects/psrc/indicator_results";#"Scripts/cpeak/sandbox/csvs";#
my $repository_path_tex = "Website/projects/psrc/documentation/tex/tables";#"Scripts/cpeak/sandbox/latex";#
system "cvs -d $repository_root checkout -d $working_path_csv $repository_path_csv";
system "cvs -d $repository_root checkout -d $working_path_tex $repository_path_tex";

my @tables = &get_tables($working_path_csv);
my @noninitialized_tex_files = &check_file_existence(\@tables, $working_path_tex);
&format(\@tables);
&add_nonexistent_files_to_cvs(\@noninitialized_tex_files);
print "committing tex tables to repository. \n";
system "cvs commit -m '(cpeak) latest table modification' $working_path_tex";

sub format
{
	my ($table_names_array) = @_;
	my @table_names = @$table_names_array;
	foreach my $table (@table_names) {
		my $first_row = 1;
		open INFILE, "$working_path_csv/$table.csv" or die "Table $table.csv doesn't exist. \n";
		open OUTFILE, ">$working_path_tex/$table.tex" or die "Outfile $table.tex didn't open \n"; #tex for "LaTeX-ready
		while (<INFILE>) {
			chomp;
			chop if /\r$/;
			#Handle various table headers (change various words to greek symbols, split single header into double row header, etc.)
			#regarding Parcel_characteristics_2:
			s/\"Land_use\",\"Parcels\",\"Change_in_Parcels\",\"Acres\",\"Change_in_Acres\",\"Impval_000000\",\"Change_in_Impval\",\"Landval_000000\",\"Change_in_Landval\",\"units\",\"Change_in_Units\",\"Sqft_000\",\"Change_in_SQFT\"/ & & Change & & Change & ImpVal & Change & LandVal & Change & & Change & SQFT & Change \\\\ \n Land_Use & Parcels & in Parcels & Acres & in Acres & (millions) & in ImpVal & (millions) & in LandVal & Units & in Units & (thousands) & in SQFT  /;
			s/\"Land_use\",\"parcels\",\"Change_in_Parcels\",\"acres\",\"change_in_acres\",\"impval_000000\",\"change_in_impval\"/ & & & &  & ImpVal & \$\\Delta\$ ImpVal \\\\ \n Land_Use & Parcels & \$\\Delta\$ Parcels & Acres & \$\\Delta\$ Acres & (millions) & (millions) /;
			s/\"Land_Use\",\"landval_000000\",\"change_in_landval\",\"units\",\"change_in_units\",\"sqft_000\",\"change_in_sqft\"/ & Landval & \$\\Delta\$ LandVal & & & SQFT & \$\\Delta\$ SQFT\\\\ \n Land_Use  & (millions) & (millions) & Units & \$\\Delta\$ Units & (thousands) & (thousands)   /;
			s/\"Land_Use\",\"Parcels\",\"Acres\",\"Impval_000000\",\"Landval_000000\",\"Units\",\"Sqft_000\"/ & &  & Impval & Landval & & Sqft \\\\\n Land_Use & Parcels & Acres &\(millions\) & \(millions\) & Units & \(thousands\)/ ;
	        # re: unit_land_use_consistency_checks:
			s/\"county_name\",\"LAND_USE\",\"PARCELS_WITH_EXCESSIVE_UNITS\",\"PARCEL_COUNT\",\"EXCESSIVE_UNIT_RATE\"/COUNTY &  & PARCELS_WITH & TOTAL & PROPORTION OF \\\\ \n NAME & LAND USE & EXCESSIVE_UNITS & PARCEL COUNT & TOTAL UNITS/;
			s/\"COUNTY_NAME\",\"LAND_USE\",\"PARCELS_WITH_UNIT_UNDERCOUNTS\",\"PARCEL_COUNT\",\"UNIT_UNDERCOUNT_RATE\"/COUNTY &  & PARCELS_WITH & TOTAL & PROPORTION OF \\\\ \n NAME & LAND USE & UNIT UNDERCOUNTS & PARCEL COUNT & TOTAL UNITS/;
			# re: percentiles indicators
			s/\"county\",\"land_use\",\"total_number_of_parcels\",\"0_percentile\",\"1_percentile\",\"5_percentile\",\"10_percentile\",\"25_percentile\",\"50_percentile\",\"75_percentile\",\"90_percentile\",\"95_percentile\",\"99_percentile\",\"100_percentile\"/ &  & Total & \\multicolumn{11}{|c}{Percentile Values}\\\\ \n County & Land Use & Parcels & 0  & 1  & 5  & 10  & 25  & 50  & 75  & 90 & 95  & 99  & 100  \\/;
			s/\"county\",\"land_use\",\"total_number_of_parcels\",\"0_percentile_000\",\"1_percentile_000\",\"5_percentile_000\",\"10_percentile_000\",\"25_percentile_000\",\"50_percentile_000\",\"75_percentile_000\",\"90_percentile_000\",\"95_percentile_000\",\"99_percentile_000\",\"100_percentile_000\"/ &  & Total & \\multicolumn{11}{|c}{Percentile Values (thousands)}\\\\ \n County & Land Use & Parcels & 0  & 1  & 5  & 10  & 25  & 50  & 75  & 90 & 95  & 99  & 100  \\/;
			s/\"county\",\"land_use\",\"total_number_of_parcels\",\"tax_exempt_status\",\"0_percentile_000\",\"1_percentile_000\",\"5_percentile_000\",\"10_percentile_000\",\"25_percentile_000\",\"50_percentile_000\",\"75_percentile_000\",\"90_percentile_000\",\"95_percentile_000\",\"99_percentile_000\",\"100_percentile_000\"/ &  & Total & \\multicolumn{11}{|c}{Percentile Values (thousands)}\\\\ \n County & Land Use & Parcels & Exempt & 0  & 1  & 5  & 10  & 25  & 50  & 75  & 90 & 95  & 99  & 100  \\/;
			s/\"county\",\"land_use\",\"total_built_parcels\",\"0_percentile\",\"1_percentile\",\"5_percentile\",\"10_percentile\",\"25_percentile\",\"50_percentile\",\"75_percentile\",\"90_percentile\",\"95_percentile\",\"99_percentile\",\"100_percentile\"/ &  & Total Built & \\multicolumn{11}{|c}{Percentile Values}\\\\ \n County & Land Use & Parcels & 0  & 1  & 5  & 10  & 25  & 50  & 75  & 90 & 95  & 99  & 100  \\/;
			# re: faz comparison tables:
			s/\"FAZ\",\"U_Goved\",\"P_Goved\",\"goved_dif\",\"gov_ed_pct_dif\"/& \\multicolumn{4}{|c|}{Government and Education} \\\\ FAZ & UrbanSim & PSRC & \$\\Delta\$ & Percent \$\\Delta\$ /; #\\\\ \\hline \\endhead \\hline \\endfoot/;
			s/\"FAZ\",\"U_Retail\",\"P_Retail\",\"Retail_dif\",\"Retail_pct_dif\",\"U_FIRES\",\"P_FIRES\",\"FIRES_dif\",\"FIRES_pct_dif\"/ & \\multicolumn{4}{|c|}{Retail Trade} & \\multicolumn{4}{|c|}{FIRES} \\\\ FAZ & UrbanSim & PSRC & \$\\Delta\$ & Percent \$\\Delta\$ & UrbanSim & PSRC & \$\\Delta\$  & Percent \$\\Delta\$  /; #\\\\ \\hline \\endhead \\hline \\endfoot/;
			s/\"FAZ\",\"U_Manu\",\"P_Manu\",\"manu_dif\",\"manu_pct_dif\",\"U_WTCU\",\"P_WTCU\",\"wtcu_dif\",\"wtcu_pct_dif\"/ & \\multicolumn{4}{|c|}{Manufacturing} & \\multicolumn{4}{|c|}{Wholesale Transportation Communications \\& Utilities} \\\\ FAZ & UrbanSim & PSRC & \$\\Delta\$ & Percent \$\\Delta\$ & UrbanSim & PSRC & \$\\Delta\$  & Percent \$\\Delta\$  /; #\\\\ \\hline \\endhead \\hline \\endfoot/;
			#s/Impval_000/Impval\(000\)/g;
			#s/Landval_000/Landval\(000\)/g;
			#s/Sqft_000/Sqft\(000\)/g;
			s/Transportation Communication Utilities/Transport\/Com\/Util/g;
			s/Hospital \/ Convalescent Center/Hospital \/ Medical/g;
			s/_/ /g;
			s/%/\\%/g;
			s/\"//g;
			s/,/ & /g;
			# Add commas
			s/(\d)(\d\d\d\s&)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d\s&)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d,\d\d\d\s&)/$1,$2/g;
			s/(\d)(\d\d\d.\d+\s&)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d,\d+\s&)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d,\d\d\d.\d+\s&)/$1,$2/g;
			s/(\d)(\d\d\d$)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d$)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d,\d\d\d$)/$1,$2/g;
			s/(\d)(\d\d\d.\d+$)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d.\d+$)/$1,$2/g;
			s/(\d)(\d\d\d,\d\d\d,\d\d\d.\d+$)/$1,$2/g;
			if ($first_row) {
				print OUTFILE "$_ \\\\ \\hline \n";
				if ($table eq "average_land_value_per_acre_by_land_use"
					|| $table eq "built_sqft_per_parcel_percentiles_by_land_use_by_county"
					|| $table eq "floor_area_ratio_percentiles_by_county_by_land_use"
					|| $table eq "land_value_per_acre_percentiles_by_county_by_land_use"
					|| $table eq "improvement_value_per_sqft_percentiles_by_county_by_land_use"
					|| $table eq "indicators_runs_for_latex") {
					print OUTFILE "\\endhead \n";
				}
				if ($table eq "gov_ed"
					|| $table eq "manu_wtcu"
					|| $table eq "ret_fires") {
						print OUTFILE "\\endhead \\hline \\endfoot \n";
				}
				$first_row = 0;
			} else {
				print OUTFILE "$_ \\\\\n";
			}
		}
		close INFILE;
		close OUTFILE;
	}
}

sub add_nonexistent_files_to_cvs {
	my ($table_arrayref) = @_;
	my @non_exist_files = @$table_arrayref;
	foreach my $tab (@non_exist_files) {
		print "adding ${working_path_tex}/$tab \n";
		system "cvs -d $repository_root add ${working_path_tex}/$tab";
	}
}

sub check_file_existence {
	my ($table_names, $working_path_tex) = @_;
	my @tables = @$table_names;
	my @nonexist_tables = ();
	foreach my $tab (@tables) {
		 if (!(-e "$working_path_tex/$tab.tex")) {
		 	print "nonexistent table in check_file_existence: $working_path_tex/$tab.tex \n";
			push(@nonexist_tables, "$tab.tex");
		 }
   }
   return @nonexist_tables;
}

sub get_tables {
	my ($path) = @_;
	chdir "$path" or die "Can't change directory to $path.";
	my @table_names = glob "*.csv";
	foreach my $tab (@table_names) {
		$tab =~ s/\.csv$//;
	}
	@table_names;
}

