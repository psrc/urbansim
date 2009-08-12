import indicators
import indicators.excel
import indicators.word
import indicators.jump

db         = indicators.OutputDatabase( "trondheim.cs.washington.edu", "urbansim", "UrbAnsIm4Us", "PSRC_2000_baseyear_output_urbansim_lmwang")
geography  = db.get_geography( "faz" )
indicator1  = db.get_sql_indicator( "Dwelling density", """
create temporary table tmp_table1(YEAR int, GEOGRAPHY_ID int, INDICATOR_VALUE double);

insert into tmp_table1 (YEAR, INDICATOR_VALUE, GEOGRAPHY_ID )
select g.YEAR, 
       round(sum(g.RESIDENTIAL_UNITS)/sum(150*150*0.000247*g.FRACTION_RESIDENTIAL_LAND), 2) as INDICATOR_VALUE
       $$GEOGRAPHY_COLUMNS$$
from $$GEOGRAPHY_TABLES$$
     gridcells_exported g
where 1
      $$GEOGRAPHY_CONDITIONALS$$
group by g.YEAR
         $$GEOGRAPHY_GROUPS$$;

$$RESULT_STATEMENT(tmp_table1)$$

drop table tmp_table1;
""", [], geography)

#table = indicators.word.Table( )
#table.add( indicator)
#table.show()

#chart = indicators.excel.Chart( )
#chart.add( indicator )
#chart.show( )

tab = indicators.excel.Tab( )
tab.add( indicator )
tab.show( )


#map = indicators.jump.Map( )
#map.allow_more_maps(25);
#map.add( indicator )
#map.show( )
