drop table if exists distsml2_2030;
create table distsml2_2030
     select * from distsml_2030;

create index distsml2_2030_distsml on distsml2_2030 (distsml);
     
update distsml2_2030 as a, WFRC_1997_output_2030_LRP2.distsml_2030 as LRP
     set  a.dur_dl    = a.dur_z    - LRP.dur_z,
          a.sf_tot_dl = a.sf_tot_z - LRP.sf_tot_z,
          a.hhs_dl    = a.hhs_z    - LRP.hhs_z,
          a.pop_dl    = a.pop_z    - LRP.pop_z,
          a.jobs_dl   = a.jobs_z   - LRP.jobs_z,
          a.pop_Change_percent = (a.pop_d-LRP.pop_d)/LRP.pop_d,
          a.pop_Absolute_percent = (a.pop_z-LRP.pop_z)/LRP.pop_z,
          a.hhs_Change_percent = (a.hhs_d-LRP.hhs_d)/LRP.hhs_d,
          a.hhs_Absolute_percent = (a.hhs_z-LRP.hhs_z)/LRP.hhs_z,
          a.dur_Change_percent = (a.dur_d-LRP.dur_d)/LRP.dur_d,
          a.dur_Absolute_percent = (a.dur_z-LRP.dur_z)/LRP.dur_z,
          a.jobs_Change_percent = (a.jobs_d-LRP.jobs_d)/LRP.jobs_d,
          a.jobs_Absolute_percent = (a.jobs_z-LRP.jobs_z)/LRP.jobs_z,
          a.sf_tot_Change_percent = (a.sf_tot_d-LRP.sf_tot_d)/LRP.sf_tot_d,
          a.sf_tot_Absolute_percent = (a.sf_tot_z-LRP.sf_tot_z)/LRP.sf_tot_z
     where a.distsml = LRP.distsml;
