#IGNORE_THIS_FILE
#TODO: replace with loading of actual xml configs
model_templates_xml  = \
'''
<model_system>
        <dummy_model>
            <dummy_child>text</dummy_child>
        </dummy_model>

      <simple_model_template copyable="True" type="dictionary" >
        <import flags="hidden" type="dictionary" >
          <opus_core.simple_model type="string" >SimpleModel</opus_core.simple_model>
        </import>
        <init type="dictionary" >
          <name flags="hidden" type="string" >SimpleModel</name>
        </init>
        <run type="dictionary" >
          <arguments type="dictionary" >
            <dataset type="string" >fill in</dataset>
            <expression type="quoted_string" >fill in</expression>
            <outcome_attribute parser_action="blank_to_None" type="quoted_string" />
            <dataset_pool flags="hidden" type="string" >dataset_pool</dataset_pool>
          </arguments>
        </run>
      </simple_model_template>
      <choice_model_template copyable="True" type="dictionary" >
        <import flags="hidden" type="dictionary" >
          <opus_core.choice_model type="string" >ChoiceModel</opus_core.choice_model>
        </import>
        <init type="dictionary" >
          <name flags="hidden" type="string" >ChoiceModel</name>
          <arguments type="dictionary" >
            <choice_set type="string" >fill in</choice_set>
            <utilities type="quoted_string" >opus_core.linear_utilities</utilities>
            <probabilities type="quoted_string" >opus_core.mnl_probabilities</probabilities>
            <choices type="quoted_string" >opus_core.random_choices</choices>
            <submodel_string parser_action="blank_to_None" type="string" />
            <choice_attribute_name type="quoted_string" >choice_id</choice_attribute_name>
            <interaction_pkg type="quoted_string" >opus_core</interaction_pkg>
            <run_config parser_action="blank_to_None" type="string" />
            <estimate_config type="dictionary" >
              <estimation_size_agents type="float" >1.0</estimation_size_agents>
            </estimate_config>
            <debuglevel flags="hidden" type="integer" >0</debuglevel>
            <dataset_pool flags="hidden" type="string" >dataset_pool</dataset_pool>
          </arguments>
        </init>
        <run type="dictionary" >
          <arguments type="dictionary" >
            <specification flags="hidden" type="string" >specification</specification>
            <coefficients flags="hidden" type="string" >coefficients</coefficients>
            <agent_set type="string" >fill in</agent_set>
            <agents_index flags="hidden" type="string" >cm_index</agents_index>
            <chunk_specification parser_action="blank_to_None" type="string" />
            <data_objects flags="hidden" type="string" >datasets</data_objects>
          </arguments>
        </run>
        <prepare_for_run type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_run</name>
          <arguments type="dictionary" >
            <agent_set parser_action="blank_to_None" type="string" />
            <agent_filter parser_action="blank_to_None" type="quoted_string" />
            <specification_storage type="string" >base_cache_storage</specification_storage>
            <specification_table type="quoted_string" >choice_model_template_specification</specification_table>
            <coefficients_storage type="string" >base_cache_storage</coefficients_storage>
            <coefficients_table type="quoted_string" >choice_model_template_coefficients</coefficients_table>
            <sample_coefficients type="boolean" >False</sample_coefficients>
            <cache_storage flags="hidden" type="string" >base_cache_storage</cache_storage>
            <multiplicator type="integer" >1</multiplicator>
          </arguments>
          <output flags="hidden" type="string" >(specification, coefficients, cm_index)</output>
        </prepare_for_run>
        <estimate type="dictionary" >
          <arguments type="dictionary" >
            <specification flags="hidden" type="string" >specification</specification>
            <agent_set type="string" >fill in</agent_set>
            <agents_index flags="hidden" type="string" >cm_index</agents_index>
            <procedure type="quoted_string" >opus_core.bhhh_mnl_estimation</procedure>
            <data_objects flags="hidden" type="string" >datasets</data_objects>
          </arguments>
          <output flags="hidden" type="string" >(coefficients, dummy)</output>
        </estimate>
        <prepare_for_estimate type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_estimate</name>
          <arguments type="dictionary" >
            <agent_set parser_action="blank_to_None" type="string" />
            <agent_filter parser_action="blank_to_None" type="quoted_string" />
            <specification_storage type="string" >base_cache_storage</specification_storage>
            <specification_table type="quoted_string" >choice_model_template_specification</specification_table>
          </arguments>
          <output flags="hidden" type="string" >(specification, cm_index)</output>
        </prepare_for_estimate>
      </choice_model_template>
      <regression_model_template copyable="True" type="dictionary" >
        <import flags="hidden" type="dictionary" >
          <opus_core.regression_model type="string" >RegressionModel</opus_core.regression_model>
        </import>
        <init type="dictionary" >
          <name flags="hidden" type="string" >RegressionModel</name>
          <arguments type="dictionary" >
            <regression_procedure type="quoted_string" >opus_core.linear_regression</regression_procedure>
            <submodel_string parser_action="blank_to_None" type="string" />
            <run_config parser_action="blank_to_None" type="string" />
            <estimate_config parser_action="blank_to_None" type="string" />
            <debuglevel flags="hidden" type="integer" >0</debuglevel>
            <dataset_pool flags="hidden" type="string" >dataset_pool</dataset_pool>
          </arguments>
        </init>
        <run type="dictionary" >
          <arguments type="dictionary" >
            <specification flags="hidden" type="string" >specification</specification>
            <coefficients flags="hidden" type="string" >coefficients</coefficients>
            <dataset type="string" >fill in</dataset>
            <index flags="hidden" parser_action="blank_to_None" type="string" >rm_index</index>
            <chunk_specification parser_action="blank_to_None" type="string" />
            <data_objects flags="hidden" type="string" >datasets</data_objects>
          </arguments>
        </run>
        <prepare_for_run type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_run</name>
          <arguments type="dictionary" >
            <dataset parser_action="blank_to_None" type="string" />
            <dataset_filter parser_action="blank_to_None" type="quoted_string" />
            <specification_storage type="string" >base_cache_storage</specification_storage>
            <specification_table type="quoted_string" >regression_model_template_specification</specification_table>
            <coefficients_storage type="string" >base_cache_storage</coefficients_storage>
            <coefficients_table type="quoted_string" >regression_model_template_coefficients</coefficients_table>
            <sample_coefficients type="boolean" >False</sample_coefficients>
            <cache_storage flags="hidden" type="string" >base_cache_storage</cache_storage>
            <multiplicator type="integer" >1</multiplicator>
          </arguments>
          <output flags="hidden" type="string" >(specification, coefficients, rm_index)</output>
        </prepare_for_run>
        <estimate type="dictionary" >
          <arguments type="dictionary" >
            <specification flags="hidden" type="string" >specification</specification>
            <dataset type="string" >fill in</dataset>
            <dependent_variable config_name="outcome_attribute" type="quoted_string" >fill in</dependent_variable>
            <index flags="hidden" parser_action="blank_to_None" type="string" >rm_index</index>
            <procedure type="quoted_string" >opus_core.estimate_linear_regression</procedure>
            <data_objects flags="hidden" type="string" >datasets</data_objects>
          </arguments>
          <output flags="hidden" type="string" >(coefficients, dummy)</output>
        </estimate>
        <prepare_for_estimate type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_estimate</name>
          <arguments type="dictionary" >
            <dataset parser_action="blank_to_None" type="string" />
            <dataset_filter parser_action="blank_to_None" type="quoted_string" />
            <specification_storage type="string" >base_cache_storage</specification_storage>
            <specification_table type="quoted_string" >regression_model_template_specification</specification_table>
          </arguments>
          <output flags="hidden" type="string" >(specification, rm_index)</output>
        </prepare_for_estimate>
      </regression_model_template>
      <allocation_model_template copyable="True" type="dictionary" >
        <import flags="hidden" type="dictionary" >
          <opus_core.allocation_model type="string" >AllocationModel</opus_core.allocation_model>
        </import>
        <init type="dictionary" >
          <name flags="hidden" type="string" >AllocationModel</name>
        </init>
        <run type="dictionary" >
          <arguments type="dictionary" >
            <dataset type="string" >fill in</dataset>
            <outcome_attribute type="quoted_string" >fill in</outcome_attribute>
            <weight_attribute type="quoted_string" >fill in</weight_attribute>
            <control_totals flags="hidden" type="string" >cts</control_totals>
            <current_year flags="hidden" type="string" >year</current_year>
            <control_total_attribute type="quoted_string" >fill in</control_total_attribute>
            <year_attribute type="quoted_string" >year</year_attribute>
            <capacity_attribute parser_action="blank_to_None" type="quoted_string" />
            <dataset_pool flags="hidden" type="string" >dataset_pool</dataset_pool>
          </arguments>
        </run>
        <prepare_for_run type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_run</name>
          <arguments type="dictionary" >
            <storage type="string" >base_cache_storage</storage>
            <control_totals_table_name type="quoted_string" >fill in</control_totals_table_name>
            <control_totals_id_name type="list" >['year']</control_totals_id_name>
            <control_totals_dataset_name type="quoted_string" >control_totals</control_totals_dataset_name>
          </arguments>
          <output flags="hidden" type="string" >cts</output>
        </prepare_for_run>
      </allocation_model_template>
      <agent_location_choice_model_template copyable="True" type="dictionary" >
        <import flags="hidden" type="dictionary" >
          <urbansim.models.agent_location_choice_model type="string" >AgentLocationChoiceModel</urbansim.models.agent_location_choice_model>
        </import>
        <init type="dictionary" >
          <name flags="hidden" type="string" >AgentLocationChoiceModel</name>
          <arguments type="dictionary" >
            <location_set type="string" >fill in</location_set>
            <sampler type="quoted_string" >opus_core.samplers.weighted_sampler</sampler>
            <utilities type="quoted_string" >opus_core.linear_utilities</utilities>
            <probabilities type="quoted_string" >opus_core.mnl_probabilities</probabilities>
            <choices type="quoted_string" >urbansim.lottery_choices</choices>
            <filter parser_action="blank_to_None" type="quoted_string" />
            <submodel_string parser_action="blank_to_None" type="quoted_string" />
            <location_id_string parser_action="blank_to_None" type="quoted_string" />
            <dataset_pool flags="hidden" type="string" >dataset_pool</dataset_pool>
            <model_name type="quoted_string" >AgentLocationChoiceModel</model_name>
            <short_name type="quoted_string" >ALCM</short_name>
            <variable_package type="quoted_string" >urbansim</variable_package>
            <debuglevel flags="hidden" type="string" >debuglevel</debuglevel>
            <run_config type="dictionary" >
              <sample_size_locations type="integer" >30</sample_size_locations>
              <sample_proportion_locations parser_action="blank_to_None" type="integer" />
              <compute_capacity_flag type="boolean" >True</compute_capacity_flag>
              <capacity_string parser_action="blank_to_None" type="quoted_string" />
              <number_of_units_string parser_action="blank_to_None" type="quoted_string" />
              <number_of_agents_string parser_action="blank_to_None" type="quoted_string" />
              <lottery_max_iterations type="integer" >3</lottery_max_iterations>
            </run_config>
            <estimate_config type="dictionary" >
              <weights_for_estimation_string parser_action="blank_to_None" type="quoted_string" />
              <sample_size_locations type="integer" >30</sample_size_locations>
              <sample_proportion_locations parser_action="blank_to_None" type="integer" />
              <estimation_size_agents type="float" >1.0</estimation_size_agents>
            </estimate_config>
          </arguments>
        </init>
        <prepare_for_estimate type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_estimate</name>
          <output flags="hidden" type="string" >(alcm_specification, alcm_index)</output>
          <arguments type="dictionary" >
            <specification_storage type="string" >base_cache_storage</specification_storage>
            <specification_table type="quoted_string" >agent_location_choice_model_specification</specification_table>
            <agent_set type="string" >fill in</agent_set>
            <agents_for_estimation_storage type="string" >base_cache_storage</agents_for_estimation_storage>
            <agents_for_estimation_table type="quoted_string" >fill in</agents_for_estimation_table>
            <data_objects flags="hidden" type="string" >datasets</data_objects>
            <index_to_unplace flags="hidden" parser_action="blank_to_None" type="string" />
            <join_datasets type="boolean" choices="True|False" >True</join_datasets>
            <portion_to_unplace flags="hidden" type="string" >1.0</portion_to_unplace>
            <filter parser_action="blank_to_None" type="quoted_string" />
            <location_id_variable parser_action="blank_to_None" type="quoted_string" />
          </arguments>
        </prepare_for_estimate>
        <estimate type="dictionary" >
          <output flags="hidden" type="string" >(alcm_coefficients, dummy)</output>
          <arguments type="dictionary" >
            <agent_set type="string" >fill in</agent_set>
            <agents_index flags="hidden" type="string" >alcm_index</agents_index>
            <procedure type="quoted_string" >opus_core.bhhh_mnl_estimation</procedure>
            <data_objects flags="hidden" type="string" >datasets</data_objects>
            <debuglevel flags="hidden" type="string" >debuglevel</debuglevel>
            <specification flags="hidden" type="string" >alcm_specification</specification>
          </arguments>
        </estimate>
        <prepare_for_run type="dictionary" >
          <name flags="hidden" type="string" >prepare_for_run</name>
          <output flags="hidden" type="string" >(alcm_specification, alcm_coefficients)</output>
          <arguments type="dictionary" >
            <coefficients_storage type="string" >base_cache_storage</coefficients_storage>
            <coefficients_table type="quoted_string" >agent_location_choice_model_coefficients</coefficients_table>
            <specification_storage type="string" >base_cache_storage</specification_storage>
            <specification_table type="quoted_string" >agent_location_choice_model_specification</specification_table>
          </arguments>
        </prepare_for_run>
        <run type="dictionary" >
          <arguments type="dictionary" >
            <agent_set type="string" >fill in</agent_set>
            <agents_index flags="hidden" parser_action="blank_to_None" type="string" />
            <chunk_specification type="string" >{'records_per_chunk':50000}</chunk_specification>
            <coefficients flags="hidden" type="string" >alcm_coefficients</coefficients>
            <data_objects flags="hidden" type="string" >datasets</data_objects>
            <debuglevel flags="hidden" type="string" >debuglevel</debuglevel>
            <specification flags="hidden" type="string" >alcm_specification</specification>
            <maximum_runs type="integer" >10</maximum_runs>
          </arguments>
        </run>
      </agent_location_choice_model_template>
    </model_system>
'''