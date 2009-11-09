The batch files and emme/2 macros in this folder are used for converting 
a normal PSRC travel model into a version with double-wide lanes.  To do
this:

1.  Create a travel model directory with the baseline travel model.
2.  Copy the macros and batch files from this directory into the 
	travel model's base directory, e.g., into 
	D:\baseline_travel_model_psrc_highway.
3.  Execute the double_for_4_years.bat file.

The results will be visible in files named like lx1002.txt (that's a
L in the first character).  These files show the lane widths after
the macros executed.  Maximum lane width is 9.9.  The sum should
be very close to double the original lane widths.

To see what the original lane widths are, change the 
replace the lanesx2.mac macro with the contents of 
print_lane_widths.mac, and repeat the above steps.  
The produced .txt files will contain the values currently in the
data banks.
