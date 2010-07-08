# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

specification = {}

specification = {
2:
    {
    "equation_ids":(1,2),
    "constant":(0, "act_2_2"),
    "blmz":("blmz_2_1", 0),
    "c750":("c750_2_1", 0),
    "dfre":("dfre_2_1", 0),
    "dmu":("dmu_2_1", 0),
    "dprd":("dprd_2_1", 0),
    "dres":("dres_2_1", 0),
    "dwat":("dwat_2_1", 0),
    "gai":("gai_2_1", 0),
    "hd1":("hd1_2_1", 0),
    "pcf":("pcf_2_1", 0),
    "phu":("phu_2_1", 0),
    "ugl":("ugl_2_1", 0),
    "crit":("crit_2_1", 0),
#    "dcri":("dcri_2_1", 0),
#    "pcri":("pcri_2_1", 0)
    },
 3:
    {
    "equation_ids":(1,2,3),
    "constant":(0,"act_3_2","act_3_3"),
    "amps":("amps_3_1","amps_3_2", 0),
    "dloc":(0,"dloc_3_2", 0),
    "dmu":("dmu_3_1",0, 0),
    "dnlr":("dnlr_3_1",0, 0),
    "dpub":("dpub_3_1",0, 0),
    "dres":("dres_3_1","dres_3_2", 0),
    "mai":("mai_3_1",0, 0),
    "pes":("pes_3_1","pes_3_2", 0),
    "pgr":("pgr_3_1","pgr_3_2", 0),
    "phu":("phu_3_1","phu_3_2", 0),
    "pmf":("pmf_3_1","pmf_3_2", 0),
    "pslp":("pslp_3_1",0, 0),
#    "crit":("crit_3_1","crit_3_2",0),
#    "dcri":("dcri_3_1","dcri_3_2",0),
#    "pcri":("pcri_3_1","pcri_3_2",0)
#    "crit":(0,"crit_3_2",0),
    "pcri":("pcri_3_1",0,0)
    },
4:
    {
    }, 
5:
    {
    "equation_ids":(1,2,3,5,6,7),  # note: this is the to_id's
    "constant":("act_5_1","act_5_2","act_5_3","act_5_5","act_5_6",0),
    "aai":("aai_5_1","aai_5_2","aai_5_3", 0,0,0),
    "amps":("amps_5_1","amps_5_2",0, 0,0,0),
    "blmz":("blmz_5_1","blmz_5_2",0, 0,0,0),
    "c750":("c750_5_1",0,0,0,0,0),
#    "crit":("crit_5_1","crit_5_2","crit_5_3",0,"crit_5_6","crit_5_7"),
    "crit":(0,0,0,0,"crit_5_6",0),
    "dag":(0,"dag_5_2","dag_5_3", 0,0,"dag_5_7"),
    "dcbd":(0,0,0, 0,0,"dcbd_5_7"),
#    "dcri":("dcri_5_1","dcri_5_2","dcri_5_3",0,"dcri_5_6","dcri_5_7"),
    "dcri":(0,"dcri_5_2",0,0,0,0),
    "dfre":(0,0,0,0,0,"dfre_5_7"),
    "dloc":("dloc_5_1",0,0,0,0,0),
    "dos":("dos_5_1",0,0,0,0,0),
    "dres":("dres_5_1","dres_5_2",0,0,0,0),
    "dwat":("dwat_5_1",0,0,0,0,0),
    "gai":(0,0,"gai_5_3", 0,0,"gai_5_7"), 
    "gmps":(0,0,"gmps_5_3", 0,0,0),
    "h750":(0,"h750_5_2",0,0,0,0),
    "pcf":(0,0,0, 0,0,"pcf_5_7"),
#    "pcri":("pcri_5_1","pcri_5_2","pcri_5_3",0,"pcri_5_6","pcri_5_7"),
    "pcri":(0,"pcri_5_2",0,0,"pcri_5_6","pcri_5_7"),
    "pes":(0,"pes_5_2",0,0,0,0),
    "pgr":(0,"pgr_5_2",0,0,0,0),
    "phu":(0,"phu_5_2","phu_5_3", 0,"phu_5_6",0),
    "pmf":("pmf_5_1","pmf_5_2",0, 0,"pmf_5_6",0),
    "pslp":("pslp_5_1","pslp_5_2","pslp_5_3", 0,0,0),
    "pub":("pub_5_1",0,0,0,0,0),
    "pwet":("pwet_5_1",0,0,0,0,0),
    "ugl":("ugl_5_1","ugl_5_2",0,0,0,0)
    }, 
6:
    {
    "equation_ids":(1,2,3,5,6,8),  # note: this is the to_id's
    "constant":("act_6_1","act_6_2","act_6_3","act_6_5","act_6_6",0),
    "aai":("aai_6_1","aai_6_2","aai_6_3",0,0,0),
    "blmz":(0,0,0,0,0,"blmz_6_8"),
#    "crit":("crit_6_1","crit_6_2","crit_6_3","crit_6_5",0,"crit_6_8"),
    "crit":(0,"crit_6_2","crit_6_3","crit_6_5",0,0),
    "dag":("dag_6_1",0,0,0,0,0),
    "dcbd":("dcbd_6_1","dcbd_6_2","dcbd_6_3",0,0,0),
#    "dcri":("dcri_6_1","dcri_6_2","dcri_6_3","dcri_6_5",0,"dcri_6_8"),
    "dcri":(0,"dcri_6_2","dcri_6_3",0,0,0),
    "de":(0,0,0,0,0,"de_6_8"),
    "di":("di_6_1",0,0,0,0,0),
    "dloc":("dloc_6_1","dloc_6_2","dloc_6_3",0,0,"dloc_6_8"),
    "dnlr":(0,"dnlr_6_2","dnlr_6_3",0,0,0),
    "dos":("dos_6_1",0,0,0,0,0),
    "dprd":(0,0,0,0,0,"dprd_6_8"),
    "dpub":("dpub_6_1","dpub_6_2","dpub_6_3",0,0,"dpub_6_8"),
    "dtim":("dtim_6_1","dtim_6_2",0,"dtim_6_5",0,0),
    "dwet":(0,0,0,"dwet_6_5",0,0),
    "gai":(0,"gai_6_2",0,"gai_6_5",0,0),
    "gmps":("gmps_6_1","gmps_6_2","gmps_6_3",0,0,0),
    "pag":("pag_6_1",0,0,0,0,0),
    "pcf":(0,"pcf_6_2",0,"pcf_6_5",0,"pcf_6_8"),
#    "pcri":("pcri_6_1","pcri_6_2","pcri_6_3","pcri_6_5",0,"pcri_6_8"),
    "pcri":(0,0,"pcri_6_3",0,0,0),
    "pes":(0,0,"pes_6_3","pes_6_5",0,0),
    "pfld":(0,"pfld_6_2",0,0,0,0),
    "pgr":("pgr_6_1","pgr_6_2","pgr_6_3",0,0,0),
    "plu":("plu_6_1","plu_6_2","plu_6_3",0,0,"plu_6_8"),
    "pmf":(0,"pmf_6_2",0,0,0,0),
    "pmu":("pmu_6_1","pmu_6_2","pmu_6_3",0,0,"pmu_6_8"),
    "psg":(0,"psg_6_2","psg_6_3",0,0,"psg_6_8"),
    "pslp":("pslp_6_1","pslp_6_2","pslp_6_3",0,0,0),
    "pstr":("pstr_6_1","pstr_6_2",0,0,0,"pstr_6_8"),
    "pub":("pub_6_1",0,"pub_6_3",0,0,"pub_6_8"),
    "pwet":("pwet_6_1","pwet_6_2",0,"pwet_6_5",0,0),
    "shei":(0,0,"shei_6_3",0,0,0),
    "sslp":("sslp_6_1",0,0,0,0,0),
    "tiv":(0,0,0,0,0,"tiv_6_8"),
    "ugl":("ugl_6_1","ugl_6_2",0,0,0,"ugl_6_8")
    }, 
7:
   {
    "equation_ids":(3,5,7,8),  # note: this is the to_id's
    "constant":("constant_7_3","constant_7_5","constant_7_7",0),
    "amps":(0,0,0,"amps_7_8"),
    "blmz":(0,0,0,"blmz_7_8"),
#    "crit":("crit_7_3","crit_7_5",0,"crit_7_8"),
    "crit":("crit_7_3",0,0,0),
    "dag":(0,"dag_7_5",0,0),
    "dcbd":("dcbd_7_3",0,0,0),
    "dcri":("dcri_7_3",0,0,0),
#    "dcri":("dcri_7_3","dcri_7_5",0,"dcri_7_8"),
    "dloc":("dloc_7_3",0,0,0),
    "dnlr":("dnlr_7_3",0,0,0),
    "dos":(0,"dos_7_5",0,0),
    "dpub":(0,0,0,"dpub_7_8"),
    "dres":(0,"dres_7_5",0,0),
    "dtim":("dtim_7_3",0,0,0),
    "dwat":(0,0,0,"dwat_7_8"),
    "dwet":(0,"dwet_7_5",0,0),
    "gai":(0,"gai_7_5",0,0),
    "pcc":(0,0,0,"pcc_7_8"),
#    "pcri":("pcri_7_3","pcri_7_5",0,"pcri_7_8"),
    "pcri":(0,"pcri_7_5",0,0),
    "pfld":("pfld_7_3",0,0,0),
    "pgr":("pgr_7_3","pgr_7_5",0,0),
    "plu":("plu_7_3",0,0,0),
    "pmu":("pmu_7_3",0,0,0),
    "psg":("psg_7_3",0,0,0),
    "pslp":("pslp_7_3",0,0,"pslp_7_8"),
    "pub":(0,0,0,"pub_7_8"),
    "pwet":(0,0,0,"pwet_7_8"),
    "shei":(0,"shei_7_5",0,"shei_7_8"),
    "tiv":("tiv_7_3",0,0,0),
    }, 
10:
   {
    "equation_ids":(2,3,5,6,10),  # note: this is the to_id's
    "constant":("act_10_2","act_10_3","act_10_5",0,"act_10_10"),
    "aai":("aai_10_2","aai_10_3",0,0,0),
    "cd1":("cd1_10_2",0,0,0,0),
#    "crit":("crit_10_2",0,"crit_10_5","crit_10_6",0),
    "dag":(0,0,"dag_10_5","dag_10_6",0),
    "dcbd":(0,0,"dcbd_10_5","dcbd_10_6",0),
#    "dcri":("dcri_10_2",0,"dcri_10_5","dcri_10_6",0),
    "dcri":("dcri_10_2",0,0,0,0),
    "dloc":(0,0,"dloc_10_5","dloc_10_6",0),
    "dmu":("dmu_10_2",0,0,0,0),
    "dprd":("dprd_10_2",0,0,0,0),
    "dpub":(0,0,0,"dpub_10_6",0),
    "dtim":(0,0,"dtim_10_5","dtim_10_6",0),
    "fmps":(0,0,0,"fmps_10_6",0),
    "gmps":("gmps_10_2",0,"gmps_10_5","gmps_10_6",0),
    "h450":("h450_10_2","h450_10_3",0,0,0),
    "h750":("h750_10_2","h750_10_3",0,0,0),
    "mai":("mai_10_2","mai_10_3",0,0,0),
    "mmps":(0,0,0,"mmps_10_6",0),
    "pcc":(0,0,"pcc_10_5","pcc_10_6",0),
    "pcf":("pcf_10_2",0,0,"pcf_10_6",0),
#    "pcri":("pcri_10_2",0,"pcri_10_5","pcri_10_6",0),
    "pcri":("pcri_10_2",0,"pcri_10_5","pcri_10_6",0),
    "pes":("pes_10_2",0,0,0,0),
    "pfld":(0,0,0,"pfld_10_6",0),
    "pgr":("pgr_10_2","pgr_10_3","pgr_10_5",0,0),
    "plu":("plu_10_2","plu_10_3",0,0,0),
    "pmf":(0,0,"pmf_10_5","pmf_10_6",0),
    "pmu":("pmu_10_2",0,0,"pmu_10_6",0),
    "psg":("psg_10_2",0,"psg_10_5","psg_10_6",0),
    "pslp":("pslp_10_2","pslp_10_3",0,0,0),
    "pub":(0,0,0,"pub_10_6",0),
    "shei":("shei_10_2",0,0,0,0),
    "tiv":(0,0,"tiv_10_5","tiv_10_6",0),
    "ugl":("ugl_10_2",0,0,0,0)
     },  
8:
     {
    "equation_ids": (9,),   # note the comma after "9"
    "constant":("act_8_9",),
    },  
11:
    {
    "equation_ids": (11,),   # note the comma after "11"
    "constant":("act_11_11",),
    },  
12:
     {
    "equation_ids": (12,),   # note the comma after "12"
    "constant":("act_12_12",),    
     },
13:
     {
    "equation_ids": (13,),   # note the comma after "13"
    "constant":("act_13_13",),
    },  
14:
     {
    "equation_ids": (14,),   # note the comma after "14"
    "constant":("act_14_14",),
      }
 }
    