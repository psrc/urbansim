def go():
    from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
    import os
    
    indicators = {
        'zone_jobs':Indicator(
           dataset_name = 'zone',
           attribute = 'urbansim.zone.number_of_jobs')          
    }
    
    from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
    from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData
    
    project_name = 'eugene_gridcell'
    run_name1 = 'base_year_data'
    years = [1980, 1980]
    
    source_data = SourceData(
       cache_directory = os.path.join(os.environ['OPUS_DATA_PATH'],project_name,run_name1),
       #comparison_cache_directory = '',
       years = years,
       dataset_pool_configuration = DatasetPoolConfiguration(
             package_order=['urbansim','opus_core'],
             ),
       project_name = project_name
    )
    
    ################################################################
    #COMPUTE indicators
    ################################################################
    from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker
    
    maker = Maker(project_name)
    computed_indicators = maker.create_batch(
                                indicators = indicators, 
                                source_data = source_data)
    
    ############################################
    #VISUALIZE the resulting computed indicators
    ############################################
    from opus_gui.results_manager.run.indicator_framework.visualizer.visualization_factory import VisualizationFactory
    
    visualizer = VisualizationFactory()
    visualizations = []
    
    maps = [('zone_jobs','matplotlib_chart')]
    
    for item in maps:
        vistype = 'mapnik_map' # default to map
        if type(item) == type(()): item, vistype = item
        print "Generating indicator %s" % item
        
        visualizations += visualizer.visualize(
            indicators_to_visualize = [item], # override default indicators to visualize (all)
            computed_indicators = computed_indicators,
            visualization_type = vistype,
            name = item)
    
    print "Done generating indicators."

    return dict((v.name,v.get_file_path()) for v in visualizations)

if __name__ == '__main__':
    print go()