# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

specification = {}

specification = {
2:
    {
        "equation_ids":(1,2),
    "constant":(0, "act_2_2"),
    "blmz":("blmz_2_1", 0),
    "c750":("c750_2_1", 0),
    "cd1":("cd1_2_1", 0),
    "dcbd":("dcbd_2_1", 0),
    "dprd":("dprd_2_1", 0),
   "dtim":("dtim_2_1", 0),
    "h750":("h750_2_1", 0),
    "hai":("hai_2_1", 0),
    "hd1":("hd1_2_1", 0),
    "hmps":("hmps_2_1", 0),
#    "pcd":("pcd_2_1", 0),    - Jeff removed PCD from all Feb 22 2006
    "pgr":("pgr_2_1", 0),
    "phu":("phu_2_1", 0),
    "pwa":("pwa_2_1", 0),
    "shei":("shei_2_1", 0),
    },
 3:
    {
    "equation_ids":(1,2,3),
    "constant":(0,"act_3_2","act_3_3"),
    "amps":("amps_3_1",0, 0),
    "blmz":("blmz_3_1",0, 0),
    "c750":("c750_3_1",0, 0),
    "dloc":(0,"dloc_3_2", 0),
    "dmu":("dmu_3_1",0, 0),
    "dnlr":("dnlr_3_1",0, 0),
    "dprd":("dprd_3_1",0, 0),
    "dres":("dres_3_1",0, 0),
    "dtim":("dtim_3_1",0, 0),
    "dwet":("dwet_3_1",0, 0),
    "gai":(0,"gai_3_2", 0),
    "h750":("h750_3_1",0, 0),
    "hd1":("hd1_3_1",0, 0),
    "hmps":("hmps_3_1",0, 0),
    "pag":("pag_3_1",0, 0),
    "pcc":(0,"pcc_3_2", 0),
#    "pcd":("pcd_3_1",0, 0),
    "pgr":("pgr_3_1",0, 0),
    "phu":("phu_3_1","phu_3_2", 0),
    "pmf":("pmf_3_1","pmf_3_2", 0),
    "pmu":(0,"pmu_3_2", 0),
    "pslp":("pslp_3_1","pslp_3_2", 0),
    "pstr":("pstr_3_1","pstr_3_2", 0),
    "tiv":("tiv_3_1",0, 0),
    "ugl":("ugl_3_1","ugl_3_2", 0)
    },
4:
    {
    }, 
5:
    {
    "equation_ids":(2,3,5,6,7),  # note: this is the to_id's
    "constant":("act_5_2","act_5_3","act_5_5","act_5_6",0),
    "aai":("aai_5_2",0, 0,"aai_5_6","aai_5_7"),
    "amps":("amps_5_2",0, 0,0,0),
    "blmz":(0,"blmz_5_3", 0,0,0),
    "crit":("crit_5_2",0, 0,"crit_5_6",0),
    "dag":(0,0, 0,"dag_5_6",0),
    "dcri":("dcri_5_2",0, 0,"dcri_5_6",0),
    "dloc":("dloc_5_2","dloc_5_3", 0,0,0),
    "dnlr":("dnlr_5_2","dnlr_5_3", 0,0,0),
    "dprd":("dprd_5_2",0, 0,0,0),
    "dpub":("dpub_5_2",0, 0,0,"dpub_5_7"),
    "dtim":("dtim_5_2","dtim_5_3", 0,0,"dtim_5_7"),
    "gmps":(0,0, 0,0,"gmps_5_7"),
    "h750":(0,0, 0,"h750_5_6",0),
    "mai":(0,"mai_5_3", 0,0,0),
    "pcc":("pcc_5_2",0, 0,0,"pcc_5_7"),
#    "pcd":("pcd_5_2","pcd_5_3", 0,0,0),
    "pcf":("pcf_5_2",0, 0,0,"pcf_5_7"),
    "pcri":(0,"pcri_5_3", 0,"pcri_5_6",0),
    "pes":(0,0, 0,"pes_5_6",0),
    "pfld":(0,0, 0,0,"pfld_5_7"),
    "pgr":(0,0, 0,"pgr_5_6",0),
    "plu":(0,"plu_5_3", 0,"plu_5_6","plu_5_7"),
    "pmf":("pmf_5_2",0, 0,"pmf_5_6","pmf_5_7"),
    "pmu":("pmu_5_2",0, 0,0,0),
    "psg":(0,0, 0,0,"psg_5_7"),
    "pstr":("pstr_5_2",0, 0,0,0),
    "pwa":(0,0, 0,"pwa_5_6",0),
    "pwet":(0,0, 0,0,"pwet_5_7"),
    "shei":("shei_5_2",0, 0,0,0),
    "tiv":(0,0, 0,0,"tiv_5_7"),
    "ugl":("ugl_5_2",0, 0,0,0)
    }, 
6:
    {
    "equation_ids":(2,3,5,6,8),  # note: this is the to_id's
    "constant":("act_6_2","act_6_3","act_6_5","act_6_6",0),
    "aai":(0,"aai_6_3",0, 0,0),
    "amps":("amps_6_2",0,0, 0,0),    
    "blmz":(0,0,0, 0,"blmz_6_8"),
    "c450":("c450_6_2","c450_6_3","c450_6_5",0,0),
    "c750":("c750_6_2","c750_6_3","c750_6_5", 0,0),
    "crit":("crit_6_2",0,0, 0,0),
    "dcri":("dcri_6_2",0,0, 0,0),
    "dloc":("dloc_6_2","dloc_6_3",0, 0,"dloc_6_8"),
    "dnlr":("dnlr_6_2","dnlr_6_3",0, 0,0),
    "dos":(0,"dos_6_3",0, 0,"dos_6_8"),
    "dres":("dres_6_2",0,0, 0,0),
    "dtim":("dtim_6_2","dtim_6_3",0, 0,0),
    "dwat":("dwat_6_2",0,0, 0,0),
   "gai":(0,0,"gai_6_5", 0,0),
    "hd1":(0,0,0, 0,"hd1_6_8"),
    "mai":("mai_6_2",0,0, 0,0),
    "pcc":("pcc_6_2","pcc_6_3",0, 0,"pcc_6_8"),
#    "pcd":("pcd_6_2","pcd_6_3","pcd_6_5", 0,0),
    "pcf":("pcf_6_2","pcf_6_3",0, 0,"pcf_6_8"),
    "pgr":("pgr_6_2",0,"pgr_6_5", 0,0),
    "plu":("plu_6_2","plu_6_3","plu_6_5", 0,0),
    "pmu":("pmu_6_2",0,0, 0,"pmu_6_8"),
    "psg":("psg_6_2","psg_6_3",0, 0,0),
    "pslp":("pslp_6_2",0,0, 0,0),
    "pstr":("pstr_6_2","pstr_6_3",0, 0,"pstr_6_8"),
    "pub":(0,0,0, 0,"pub_6_8"),
    "ugl":("ugl_6_2",0,0, 0,"ugl_6_8")
    }, 
7:
   {
    "equation_ids":(2,3,5,7,8),  # note: this is the to_id's
    "constant":("act_7_2","act_7_3","act_7_5","act_7_7",0),
    "aai":("aai_7_2","aai_7_3",0,0,0),
    "blmz":("blmz_7_2","blmz_7_3",0,0,"blmz_7_8"),
    "crit":("crit_7_2",0, 0,0,0),
    "dcbd":("dcbd_7_2","dcbd_7_3", 0,0,0),
    "dcri":("dcri_7_2","dcri_7_3",0,0,0),
    "dloc":("dloc_7_2","dloc_7_3", 0,0,0),
    "dnlr":("dnlr_7_2","dnlr_7_3",0,0,0),
    "dprd":(0,"dprd_7_3", 0,0,0),
    "dpub":(0,0, "dpub_7_5",0,"dpub_7_8"),
    "dres":(0,0,0,0,"dres_7_8"),
    "dwat":("dwat_7_2","dwat_7_3",0,0,0),
    "dwet":(0,"dwet_7_3", 0,0,0),
    "fmps":(0,"fmps_7_3", "fmps_7_5",0,"fmps_7_8"),
    "h450":("h450_7_2",0,0,0,0),
    "h750":("h750_7_2",0,0,0,0),
    "mai":("mai_7_2",0,0,0,0),
    "pcc":(0,0, "pcc_7_5",0,"pcc_7_8"),
    "pcri":(0,"pcri_7_3",0,0,0),
    "pes":(0,0, "pes_7_5",0,0),
    "pgr":(0,0, "pgr_7_5",0,0),
    "plu":(0,"plu_7_3",0,0,0),
    "pmf":(0,0, "pmf_7_5",0,0),
    "pmu":("pmu_7_2","pmu_7_3", 0,0,0),
    "psg":(0,"psg_7_3",0,0,0),
    "pslp":("pslp_7_2",0,0,0,0),
    "pstr":("pstr_7_2",0,0,0,0),
    "pub":(0,0,0,0,"pub_7_8"),
    "shei":(0,"shei_7_3",0,0,"shei_7_8"),
    "ugl":("ugl_7_2",0, 0,0,0)
    }, 
10:
   {
        "equation_ids":(2,3,5,6,10),  # note: this is the to_id's
    "constant":("act_10_2","act_10_3","act_10_5",0,"act_10_10"),
    "aai":("aai_10_2","aai_10_3",0,0,0),
    "crit":(0,0, "crit_10_5","crit_10_6",0),
    "dag":("dag_10_2","dag_10_3", "dag_10_5","dag_10_6",0),
    "dcri":(0,0, "dcri_10_5","dcri_10_6",0),
    "dfre":("dfre_10_2","dfre_10_3", "dfre_10_5","dfre_10_6",0),
    "dloc":("dloc_10_2","dloc_10_3", 0,0,0),
    "dnlr":("dnlr_10_2","dnlr_10_3",0,"dnlr_10_6",0),
    "dpub":(0,0,0,"dpub_10_6",0),
    "dres":("dres_10_2",0, "dres_10_5",0,0),
    "dtim":("dtim_10_2",0, "dtim_10_5","dtim_10_6",0),
    "dwet":("dwet_10_2",0, 0,"dwet_10_6",0),
    "fmps":(0,0, "fmps_10_5",0,0),
    "gmps":("gmps_10_2","gmps_10_3", "gmps_10_5","gmps_10_6",0),
    "h450":("h450_10_2",0,0,0,0),
    "h750":(0,0, "h750_10_5",0,0),
    "pcc":("pcc_10_2",0,0,0,0),
    "pcf":("pcf_10_2",0,0,0,0),
    "pcri":("pcri_10_2","pcri_10_3",0,0,0),
    "pfld":("pfld_10_2",0, "pfld_10_5",0,0),
    "pgr":("pgr_10_2","pgr_10_3", "pgr_10_5",0,0),
    "plu":("plu_10_2","plu_10_3", "plu_10_5",0,0),
    "pmf":(0,"pmf_10_3", "pmf_10_5","pmf_10_6",0),
    "pmu":("pmu_10_2","pmu_10_3", 0,0,0),
    "psg":(0,"psg_10_3", 0,"psg_10_6",0),
    "pslp":("pslp_10_2",0,0,0,0),
    "pub":("pub_10_2",0,0,0,0),
    "pwet":("pwet_10_2","pwet_10_3", "pwet_10_5",0,0),
    "tiv":(0,0,0,"tiv_10_6",0),
    "ugl":("ugl_10_2","ugl_10_3", "ugl_10_5",0,0)    
     },  
8:
     {
    "equation_ids": (9,),   # note the comma after "9"
    "constant":("act_8_9",),
    },  
11:
    {
    "equation_ids": (11,),   # note the comma after "9"
    "constant":("act_11_11",),
    },  
12:
     {
    "equation_ids": (12,),   # note the comma after "9"
    "constant":("act_12_12",),    
     },
13:
     {
    "equation_ids": (13,),   # note the comma after "9"
    "constant":("act_13_13",),
    },  
14:
     {
    "equation_ids": (14,),   # note the comma after "9"
    "constant":("act_14_14",),
      }
 }
    