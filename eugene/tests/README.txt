To run all of the tests for the eugene package:

   python all_tests.py
   
 The test_simulate.py test runs the Eugene simulation.  It uses MySQL on the server 
 indicated by the environment variable MYSQLHOSTNAME, and expects to find a database 
 eugene_1980_baseyear.  See the installation instructions for configuring MySQL for
 more information on that.
 
 If you want to run this test and you don't have the eugene_1980_database already
 in MySQL, download the Eugene 1980 baseyear cache from the Opus/UrbanSim download page 
 at www.urbansim.org/download.  (Be sure and get the cache corresponding to your
 version of the code.)  Then use the do_export_cache_to_sql_database script in opus_core/tools
 to copy the data from the cache into MySQL.  The cache directory will be 
 eugene_1980_baseyear_cache/1980 (note the 1980 subdirectory).  You should copy it to 
 a database named eugene_1980_baseyear.
 