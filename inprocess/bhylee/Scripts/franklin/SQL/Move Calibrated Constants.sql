# This short script replaces the developer model constant coefficients
# in the WFRC base year database with the calibrated constants contained, 
# in this case, in "WFRC_1997_output_franklin".

USE WFRC_1997_baseyear;

DELETE FROM developer_model_coefficients 
     WHERE coefficient_name LIKE "constant%";

DELETE FROM developer_model_coefficients 
     WHERE coefficient_name LIKE "act%";

INSERT INTO developer_model_coefficients 
     SELECT * FROM WFRC_1997_output_gfu.developer_model_coefficients;
     