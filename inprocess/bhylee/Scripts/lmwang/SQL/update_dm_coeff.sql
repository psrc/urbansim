
update developer_model_coefficients d1
	inner join
	PSRC_2000_baseyear_const_calib_output.developer_model_coefficients d2
	on d1.sub_model_id = d2.sub_model_id and
	d1.coefficient_name = d2.coefficient_name
set
	d1.estimate = d2.estimate,
	d1.standard_error = d2.standard_error,
	d1.t_statistic = d2.t_statistic,
	d1.p_value = d2.p_value
;
