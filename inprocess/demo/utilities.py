# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


def indicator_to_XML_writer(indicators):
    unique_attributes = set([])
    results = []

    datasets = ['gridcell', 'zone', 'city', 'county', 'alldata',
                'building', 'parcel', 'faz', 'large_area', 'county',
                'building_type', 'development_template', 'employment_sector', 
                'generic_land_use_type', 'household', 'job_building_type', 
                'land_use_type']
    

    for name, computed_indicator in indicators.items():
        expression = computed_indicator.indicator.attribute
        alias = computed_indicator.indicator.get_attribute_alias()
        package = computed_indicator.indicator.get_variable_name().get_package_name()
        valid_datasets = 'GEOGRAPHY'
        doc_link = ""
        dataset_name = computed_indicator.dataset_name
        
        for dataset in datasets:
            if expression.find(dataset) != -1:
                expression = expression.replace(dataset, 'DATASET')
        
        library_element = (alias, package, valid_datasets, doc_link, expression)
        unique_attributes.add(library_element)

        source_data = 'eugene_baseline'        
        indicator_name = '%s.%s.%s'%(alias,dataset_name,source_data)
        result_element = (indicator_name, source_data, dataset_name, alias)
        results.append(result_element)
        
    output_library(unique_attributes)
    output_results(results)
        
def output_library(library_element_set):
    print '*******************\nAdd to proper indicator library section of XML\n******************'
    library_elements = list(library_element_set)

    indicator_template = ('%(i)s<%(alias)s type="indicator">\n'
                       '%(i)s  <package type="string">%(package)s</package>\n'
                       '%(i)s  <valid_datasets type="string">%(valid_datasets)s</valid_datasets>\n'
                       '%(i)s  <documentation_link type="string">%(doc_link)s</documentation_link>\n'
                       '%(i)s  <expression type="string">%(expression)s</expression>\n'
                       '%(i)s</%(alias)s>\n'
                       )
    for (alias, package, valid_datasets, doc_link, expression) in library_elements:
        map = {
               'package':package,
               'alias':alias,
               'valid_datasets':valid_datasets,
               'doc_link':doc_link,
               'expression':expression,
               'i':'        '
               }
        print indicator_template%map
        
        
def output_results(results):
    
    print '*******************\nAdd in Results section of XML\n******************' 
    result_template = ('%(i)s<%(indicator_name)s type="indicator_result">\n'
                       '%(i)s  <source_data type="string">%(source_data)s</source_data>\n'
                       '%(i)s  <indicator_name type="string">%(alias)s</indicator_name>\n'
                       '%(i)s  <dataset_name type="string">%(dataset_name)s</dataset_name>\n'
                       '%(i)s</%(indicator_name)s>\n'
                       )
    for (indicator_name, source_data, dataset_name, alias) in results:
        map = {
               'indicator_name':indicator_name,
               'alias':alias,
               'source_data':source_data,
               'dataset_name':dataset_name,
               'i':'      '
               }
        print result_template%map