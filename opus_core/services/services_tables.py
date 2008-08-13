#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from elixir import Entity, Field, Integer, DateTime, Text, \
                   ManyToOne, OneToOne, using_options, BLOB

    
class ResultsComputedIndicators(Entity):
    using_options(tablename='computed_indicators')

    indicator_name = Field(Text)
    dataset_name = Field(Text)
    expression = Field(Text)
    run_id = ManyToOne('RunsRunActivity', colname = 'run_id')
    data_path = Field(Text)
    processor_name = Field(Text)
    date_time = Field(DateTime)
        
class RunsRunActivity(Entity):
    using_options(tablename='run_activity')
    
    run_id = Field(Integer, primary_key = True)
    run_name = Field(Text)
    run_description = Field(Text)
    cache_directory = Field(Text)
    processor_name = Field(Text)
    date_time = Field(DateTime)
    status = Field(Text)
    resources = Field(BLOB)


#class ResultsVisualizations(Entity):
#    using_options(tablename='visualizations')
#
#    years = List
#    indicators = ManyToMany('computed_indicators')
#    data_path = Field(String)
#    visualization_type = Integer
    
