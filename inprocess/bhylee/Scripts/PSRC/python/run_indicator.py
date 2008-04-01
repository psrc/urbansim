import indicators
import indicators.excel

class ExcelChart:
    def __init__(self, database_name, region_name):
        self.db = indicators.OutputDatabase( "trondheim.cs.washington.edu", "urbansim", "UrbAnsIm4Us", 
            database_name)
        self.geography = self.db.get_geography( region_name )

    def show(self, indicator_name):
        """Create an excel chart with just this indicator on it.
        """
        indicator = self.db.get_predefined_indicator( indicator_name, [], self.geography )
        chart = indicators.excel.Chart( )
        chart.add( indicator)
        chart.show( )    

# This database only contains values for 2010, 2020, and 2030.
database_name_for_2010_2020_2030_results = "PSRC_2000_base_run_output"
database_name_for_current_results = "PSRC_2000_base_run_output"
