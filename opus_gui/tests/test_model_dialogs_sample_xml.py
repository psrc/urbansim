# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#IGNORE_THIS_FILE
#TODO: replace with loading of actual xml configs
model_templates_xml  = \
'''
<model_system type="dictionary" setexpanded="True">
    <dummy_model>
        <structure>
            <dummy_child>text</dummy_child>    
        </structure>
    </dummy_model>
    <estimation_config type="dictionary">
        <cache_directory parser_action="prefix_with_opus_data_path" type="directory">eugene_gridcell/base_year_data</cache_directory>
        <estimation_database_configuration type="class">
            <Class_name flags="hidden" type="string">EstimationDatabaseConfiguration</Class_name>
            <Class_path flags="hidden" type="string">opus_core.database_management.configurations.estimation_database_configuration</Class_path>
            <database_name type="string"/>
        </estimation_database_configuration>
        <datasets_to_preload parser_action="list_to_dictionary" type="selectable_list">
            <gridcell choices="Load|Skip" copyable="True" followers="my_dataset" type="dataset">Load</gridcell>
        </datasets_to_preload>
        <dataset_pool_configuration type="class">
            <Class_name flags="hidden" type="string">DatasetPoolConfiguration</Class_name>
            <Class_path flags="hidden" type="string">opus_core.configurations.dataset_pool_configuration</Class_path>
            <package_order type="list">['eugene', 'urbansim', 'opus_core']</package_order>
            <package_order_exceptions type="dictionary"/>
        </dataset_pool_configuration>
        <datasets_to_cache_after_each_model type="list">[]</datasets_to_cache_after_each_model>
        <low_memory_mode type="boolean">False</low_memory_mode>
        <base_year type="integer">1980</base_year>
        <years type="tuple">
            <firstyear type="integer">1980</firstyear>
            <lastyear type="integer">1980</lastyear>
        </years>
        <save_estimation_results choices="True|False" type="boolean">True</save_estimation_results>
    </estimation_config>
    <simple_model_template copyable="True" type="dictionary">
        <specification></specification>
        <structure>
            <import type="dictionary">
                <opus_core.simple_model type="string">SimpleModel</opus_core.simple_model>
            </import>
            <init type="dictionary">
                <name type="string">SimpleModel</name>
            </init>
            <run type="dictionary">
                <dataset type="string">fill in</dataset>
                <expression type="quoted_string">fill in</expression>
                <outcome_attribute parser_action="blank_to_None" type="quoted_string"/>
                <dataset_pool type="string">dataset_pool</dataset_pool>
            </run>
            <prepare_for_run/>
            <estimate/>
            <prepare_for_estimate/>
        </structure>
    </simple_model_template>
    <choice_model_template copyable="True" type="dictionary">
        <specification></specification>
        <structure>
            <import type="dictionary">
                <opus_core.choice_model type="string">ChoiceModel</opus_core.choice_model>
            </import>
            <init type="dictionary">
                <name type="string">ChoiceModel</name>
                <choice_set type="string">fill in</choice_set>
                <utilities type="quoted_string">opus_core.linear_utilities</utilities>
                <probabilities type="quoted_string">opus_core.mnl_probabilities</probabilities>
                <choices type="quoted_string">opus_core.random_choices</choices>
                <submodel_string parser_action="blank_to_None" type="string"/>
                <choice_attribute_name type="quoted_string">choice_id</choice_attribute_name>
                <interaction_pkg type="quoted_string">opus_core</interaction_pkg>
                <run_config parser_action="blank_to_None" type="string"/>
                <estimate_config type="dictionary">
                    <estimation_size_agents type="float">1.0</estimation_size_agents>
                </estimate_config>
                <debuglevel type="integer">0</debuglevel>
                <dataset_pool type="string">dataset_pool</dataset_pool>
            </init>
            <run type="dictionary">
                <specification type="string">specification</specification>
                <coefficients type="string">coefficients</coefficients>
                <agent_set type="string">fill in</agent_set>
                <agents_index type="string">cm_index</agents_index>
                <chunk_specification parser_action="blank_to_None" type="string"/>
                <data_objects type="string">datasets</data_objects>
            </run>
            <prepare_for_run type="dictionary">
                <name type="string">prepare_for_run</name>
                <agent_set parser_action="blank_to_None" type="string"/>
                <agent_filter parser_action="blank_to_None" type="quoted_string"/>
                <specification_storage type="string">base_cache_storage</specification_storage>
                <specification_table type="quoted_string">choice_model_template_specification</specification_table>
                <coefficients_storage type="string">base_cache_storage</coefficients_storage>
                <coefficients_table type="quoted_string">choice_model_template_coefficients</coefficients_table>
                <sample_coefficients type="boolean">False</sample_coefficients>
                <cache_storage type="string">base_cache_storage</cache_storage>
                <multiplicator type="integer">1</multiplicator>
                <output type="string">(specification, coefficients, cm_index)</output>
            </prepare_for_run>
            <estimate type="dictionary">
                <specification type="string">specification</specification>
                <agent_set type="string">fill in</agent_set>
                <agents_index type="string">cm_index</agents_index>
                <procedure type="quoted_string">opus_core.bhhh_mnl_estimation</procedure>
                <data_objects type="string">datasets</data_objects>
                <output type="string">(coefficients, dummy)</output>
            </estimate>
            <prepare_for_estimate type="dictionary">
                <name type="string">prepare_for_estimate</name>
                <agent_set parser_action="blank_to_None" type="string"/>
                <agent_filter parser_action="blank_to_None" type="quoted_string"/>
                <specification_storage type="string">base_cache_storage</specification_storage>
                <specification_table type="quoted_string">choice_model_template_specification</specification_table>
                <output type="string">(specification, cm_index)</output>
            </prepare_for_estimate>
        </structure>
    </choice_model_template>
    <regression_model_template copyable="True" type="dictionary">
        <specification></specification>
        <structure>
            <import type="dictionary">
                <opus_core.regression_model type="string">RegressionModel</opus_core.regression_model>
            </import>
            <init type="dictionary">
                <name type="string">RegressionModel</name>
                <regression_procedure type="quoted_string">opus_core.linear_regression</regression_procedure>
                <submodel_string parser_action="blank_to_None" type="string"/>
                <run_config parser_action="blank_to_None" type="string"/>
                <estimate_config parser_action="blank_to_None" type="string"/>
                <debuglevel type="integer">0</debuglevel>
                <dataset_pool type="string">dataset_pool</dataset_pool>
            </init>
            <run type="dictionary">
                <specification type="string">specification</specification>
                <coefficients type="string">coefficients</coefficients>
                <dataset type="string">fill in</dataset>
                <index parser_action="blank_to_None" type="string">rm_index</index>
                <chunk_specification parser_action="blank_to_None" type="string"/>
                <data_objects type="string">datasets</data_objects>
            </run>
            <prepare_for_run type="dictionary">
                <name type="string">prepare_for_run</name>
                <dataset parser_action="blank_to_None" type="string"/>
                <dataset_filter parser_action="blank_to_None" type="quoted_string"/>
                <specification_storage type="string">base_cache_storage</specification_storage>
                <specification_table type="quoted_string">regression_model_template_specification</specification_table>
                <coefficients_storage type="string">base_cache_storage</coefficients_storage>
                <coefficients_table type="quoted_string">regression_model_template_coefficients</coefficients_table>
                <sample_coefficients type="boolean">False</sample_coefficients>
                <cache_storage type="string">base_cache_storage</cache_storage>
                <multiplicator type="integer">1</multiplicator>
                <output type="string">(specification, coefficients, rm_index)</output>
            </prepare_for_run>
            <estimate type="dictionary">
                <specification type="string">specification</specification>
                <dataset type="string">fill in</dataset>
                <dependent_variable config_name="outcome_attribute" type="quoted_string">fill in</dependent_variable>
                <index parser_action="blank_to_None" type="string">rm_index</index>
                <procedure type="quoted_string">opus_core.estimate_linear_regression</procedure>
                <data_objects type="string">datasets</data_objects>
                <output type="string">(coefficients, dummy)</output>
            </estimate>
            <prepare_for_estimate type="dictionary">
                <name type="string">prepare_for_estimate</name>
                <dataset parser_action="blank_to_None" type="string"/>
                <dataset_filter parser_action="blank_to_None" type="quoted_string"/>
                <specification_storage type="string">base_cache_storage</specification_storage>
                <specification_table type="quoted_string">regression_model_template_specification</specification_table>
                <output type="string">(specification, rm_index)</output>
            </prepare_for_estimate>
        </structure>
    </regression_model_template>
    <allocation_model_template copyable="True" type="dictionary">
        <specification></specification>
        <structure>
            <import type="dictionary">
                <opus_core.allocation_model type="string">AllocationModel</opus_core.allocation_model>
            </import>
            <init type="dictionary">
                <name type="string">AllocationModel</name>
            </init>
            <run type="dictionary">
                <dataset type="string">fill in</dataset>
                <outcome_attribute type="quoted_string">fill in</outcome_attribute>
                <weight_attribute type="quoted_string">fill in</weight_attribute>
                <control_totals type="string">cts</control_totals>
                <current_year type="string">year</current_year>
                <control_total_attribute type="quoted_string">fill in</control_total_attribute>
                <year_attribute type="quoted_string">year</year_attribute>
                <capacity_attribute parser_action="blank_to_None" type="quoted_string"/>
                <dataset_pool type="string">dataset_pool</dataset_pool>
            </run>
            <prepare_for_run type="dictionary">
                <name type="string">prepare_for_run</name>
                <storage type="string">base_cache_storage</storage>
                <control_totals_table_name type="quoted_string">fill in</control_totals_table_name>
                <control_totals_id_name type="list">['year']</control_totals_id_name>
                <control_totals_dataset_name type="quoted_string">control_totals</control_totals_dataset_name>
                <output type="string">cts</output>
            </prepare_for_run>
            <estimate/>
            <prepare_for_estimate/>
        </structure>
    </allocation_model_template>
    <agent_location_choice_model_template copyable="True" type="dictionary">
        <specification></specification>
        <structure>
            <import type="dictionary">
                <urbansim.models.agent_location_choice_model type="string">AgentLocationChoiceModel</urbansim.models.agent_location_choice_model>
            </import>
            <init type="dictionary">
                <name type="string">AgentLocationChoiceModel</name>
                <location_set type="string">fill in</location_set>
                <sampler type="quoted_string">opus_core.samplers.weighted_sampler</sampler>
                <utilities type="quoted_string">opus_core.linear_utilities</utilities>
                <probabilities type="quoted_string">opus_core.mnl_probabilities</probabilities>
                <choices type="quoted_string">urbansim.lottery_choices</choices>
                <filter parser_action="blank_to_None" type="quoted_string"/>
                <submodel_string parser_action="blank_to_None" type="quoted_string"/>
                <location_id_string parser_action="blank_to_None" type="quoted_string"/>
                <dataset_pool type="string">dataset_pool</dataset_pool>
                <model_name type="quoted_string">AgentLocationChoiceModel</model_name>
                <short_name type="quoted_string">ALCM</short_name>
                <variable_package type="quoted_string">urbansim</variable_package>
                <debuglevel type="string">debuglevel</debuglevel>
                <run_config type="dictionary">
                    <sample_size_locations type="integer">30</sample_size_locations>
                    <sample_proportion_locations parser_action="blank_to_None" type="integer"/>
                    <compute_capacity_flag type="boolean">True</compute_capacity_flag>
                    <capacity_string parser_action="blank_to_None" type="quoted_string"/>
                    <number_of_units_string parser_action="blank_to_None" type="quoted_string"/>
                    <number_of_agents_string parser_action="blank_to_None" type="quoted_string"/>
                    <lottery_max_iterations type="integer">3</lottery_max_iterations>
                </run_config>
                <estimate_config type="dictionary">
                    <weights_for_estimation_string parser_action="blank_to_None" type="quoted_string"/>
                    <sample_size_locations type="integer">30</sample_size_locations>
                    <sample_proportion_locations parser_action="blank_to_None" type="integer"/>
                    <estimation_size_agents type="float">1.0</estimation_size_agents>
                </estimate_config>
            </init>
            <prepare_for_estimate type="dictionary">
                <name type="string">prepare_for_estimate</name>
                <output type="string">(alcm_specification, alcm_index)</output>
                <specification_storage type="string">base_cache_storage</specification_storage>
                <specification_table type="quoted_string">agent_location_choice_model_specification</specification_table>
                <agent_set type="string">fill in</agent_set>
                <agents_for_estimation_storage type="string">base_cache_storage</agents_for_estimation_storage>
                <agents_for_estimation_table type="quoted_string">fill in</agents_for_estimation_table>
                <data_objects type="string">datasets</data_objects>
                <index_to_unplace parser_action="blank_to_None" type="string"/>
                <join_datasets choices="True|False" type="boolean">True</join_datasets>
                <portion_to_unplace type="string">1.0</portion_to_unplace>
                <filter parser_action="blank_to_None" type="quoted_string"/>
                <location_id_variable parser_action="blank_to_None" type="quoted_string"/>
            </prepare_for_estimate>
            <estimate type="dictionary">
                <output type="string">(alcm_coefficients, dummy)</output>
                <agent_set type="string">fill in</agent_set>
                <agents_index type="string">alcm_index</agents_index>
                <procedure type="quoted_string">opus_core.bhhh_mnl_estimation</procedure>
                <data_objects type="string">datasets</data_objects>
                <debuglevel type="string">debuglevel</debuglevel>
                <specification type="string">alcm_specification</specification>
            </estimate>
            <prepare_for_run type="dictionary">
                <name type="string">prepare_for_run</name>
                <output type="string">(alcm_specification, alcm_coefficients)</output>
                <coefficients_storage type="string">base_cache_storage</coefficients_storage>
                <coefficients_table type="quoted_string">agent_location_choice_model_coefficients</coefficients_table>
                <specification_storage type="string">base_cache_storage</specification_storage>
                <specification_table type="quoted_string">agent_location_choice_model_specification</specification_table>
            </prepare_for_run>
            <run type="dictionary">
                <agent_set type="string">fill in</agent_set>
                <agents_index parser_action="blank_to_None" type="string"/>
                <chunk_specification type="string">{'records_per_chunk':50000}</chunk_specification>
                <coefficients type="string">alcm_coefficients</coefficients>
                <data_objects type="string">datasets</data_objects>
                <debuglevel type="string">debuglevel</debuglevel>
                <specification type="string">alcm_specification</specification>
                <maximum_runs type="integer">10</maximum_runs>
            </run>
        </structure>
    </agent_location_choice_model_template>
    <basic_estimation_template copyable="True" type="model_estimation">
        <submodel copyable="True" type="submodel">
            <description type="string">No submodel</description>
            <submodel_id type="integer">-2</submodel_id>
            <variables type="variable_list">var1</variables>
        </submodel>
    </basic_estimation_template>
    <choice_model_with_equations_estimation_template copyable="True" type="model_estimation">
        <submodel copyable="True" type="submodel">
            <description type="string">No submodel</description>
            <submodel_id type="integer">-2</submodel_id>
            <choice_1 copyable="True" type="dictionary">
                <equation_id type="integer">1</equation_id>
                <variables type="variable_list">constant</variables>
            </choice_1>
            <choice_2 copyable="True" type="dictionary">
                <equation_id type="integer">2</equation_id>
                <variables type="variable_list">var1</variables>
            </choice_2>
        </submodel>
    </choice_model_with_equations_estimation_template>
</model_system>
'''