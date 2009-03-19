# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

class CheckTravelModelInput(object):
    """Pre-checks to run on the data given to emme2. Could be run every time emme2 is run. """
        
    def check_syntax_of_emme2_input_tazdata(self, taz_data_path):
        """TAZDATA.MA2 needs to have the header at the top. There should be no leading spaces for the header.
        The data values need at least one leading space. Spaces and colons both count as white space. 
        Throws an exception if there is a problem. """
        # check if file exists
        f = open(taz_data_path, 'r')
        all_lines = f.readlines()
        f.close()
        
        # strip out header lines
        idx = 0
        while all_lines[idx][0].isalpha():
            idx += 1
        
        # check data lines
        for a_line in all_lines[idx:]:
            if len(a_line) == 0:
                break
            if not a_line[0].isspace():
                raise SyntaxError("Syntax error in " + taz_data_path)
            if '\t' in a_line:
                raise SyntaxError(taz_data_path + " contains tabs.")
            if not a_line.replace(' ', '').replace('-', '').replace(':', '').replace('.', '').replace('\n', '').isdigit():
                raise SyntaxError("non number or whitespace in line")
            
    def check_urbansim_output_tables(self, urbansim_output_db):
        """Look for dublicates in id's for exported tables"""
        tables_to_check = {"gridcells_exported":"grid_id, year", "jobs_exported":"job_id, year", \
                           "households_exported":"household_id, year", "zones_exported":"zone_id, year"}
        sql = "select count(*) as occur from %(table)s group by %(id)s having occur > 1 limit 1"
        for table, id in tables_to_check.iteritems():
            result = urbansim_output_db.GetResultsFromQuery(sql % {'table':table, 'id':id})
            if len(result) > 1:
                raise StandardError("duplicate entries in urbansim output database in " + table)
            

from opus_core.tests import opus_unittest
import tempfile
class TestCheckTravelModelInput(opus_unittest.OpusTestCase):
    
    def test_check_syntax_of_emme2_input_tazdata(self):
        mock_tazdata = open(tempfile.mktemp(), 'w')
        mock_tazdata.write("""c  p:\forecast\newtg\00_n03.prn
c  prepared: 08/18/05 17:02:35
t matrices
m matrix="hhemp"
   1    101:    59.90 
   1    102:  1055.00 
   1    103:   637.00 
   1    104:   521.00 
   1    105:   431.00 
   1    106:     0.00 
   1    107:    33.00 
""")
        mock_tazdata.close()
        CheckTravelModelInput().check_syntax_of_emme2_input_tazdata(mock_tazdata.name)
        
        try:
            mock_tazdata = open(tempfile.mktemp(), 'w')
            mock_tazdata.write(""""c  p:\forecast\newtg\00_n03.prn
c  prepared: 08/18/05 17:02:35
t matrices
m matrix="hhemp"
   1    101:    59.90 
   1    102:  1055.00 
   1    103:   637.00 
   1    104:   521.00 
   1    105:   431.00 
   1    106:     0.00 
1    107:    33.00 
""")
            mock_tazdata.close()
            CheckTravelModelInput().check_syntax_of_emme2_input_tazdata(mock_tazdata.name)
            self.assert_(False, "CheckTravelModelInput should have found an error but it didn't")
        except SyntaxError:
            pass


if __name__ == '__main__':
    opus_unittest.main()
            