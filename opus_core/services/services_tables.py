# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from elixir import Entity, Field, Integer, DateTime, Text, \
                   ManyToOne, OneToOne, using_options, BLOB

    
class ResultsComputedIndicators(Entity):
    using_options(tablename='computed_indicators')

    indicator_name = Field(Text)
    dataset_name = Field(Text)
    expression = Field(Text)
    run_id = Field(Integer)
    data_path = Field(Text)
    processor_name = Field(Text)
    date_time = Field(DateTime)
    project_name = Field(Text)
        
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
    project_name = Field(Text)


#class ResultsVisualizations(Entity):
#    using_options(tablename='visualizations')
#
#    years = List
#    indicators = ManyToMany('computed_indicators')
#    data_path = Field(String)
#    visualization_type = Integer
    
