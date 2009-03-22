# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

specification = {}

specification = {
2:
    {
       "equation_ids":(1,2),
    "constant":(0, "act_2_2"),
    "amps":("amps_2_1", 0),
    "dcbd":("dcbd_2_1", 0),
    "dfre":("dfre_2_1", 0),
    "dwat":("dwat_2_1", 0),
    "dwet":("dwet_2_1", 0),
    "hai":("hai_2_1", 0),
    "hd1":("hd1_2_1", 0),
    "mmps":("mmps_2_1", 0),
    "pes":("pes_2_1", 0),
   "plu":("plu_2_1", 0),
    "pmu":("pmu_2_1", 0),
    "psg":("psg_2_1", 0),
    "pub":("pub_2_1", 0),
    "pwa":("pwa_2_1", 0),
    "shei":("shei_2_1", 0),
    

    },
 3:
    {
   "equation_ids":(2,3),
    "constant":(0, "act_3_3"),
    "amps":("amps__3_2", 0),
    "dcbd":("dcbd__3_2", 0),
    "dres":("dres__3_2", 0),
    "fmps":("fmps__3_2", 0),
    "gmps":("gmps__3_2", 0),
    "h450":("h450__3_2", 0),
    "h750":("h750__3_2", 0),
    "hai":("hai__3_2", 0),
    "mmps":("mmps__3_2", 0),
    "pag":("pag__3_2", 0),
    "pgr":("pgr__3_2", 0),
    "pmu":("pmu__3_2", 0),
    "pwa":("pwa__3_2", 0),
    },
4:
    {
    }, 
5:
    {
    "equation_ids":(2,3,5,6,7),  # note: this is the to_id's
    "constant":("act_5_2","act_5_3","act_5_5",0,"act_5_7"),
    "aai":("aai_5_2","aai_5_3",0,0,0),
    "amps":("amps_5_2",0,0,0,0),
    "dag":(0,"dag_5_3",0,0,"dag_5_7"),
    "dcbd":("dcbd_5_2",0,0,0,0),
    "dfre":("dfre_5_2",0,0,0,0),
    "dloc":(0,"dloc_5_3",0,"dloc_5_6",0),
    "dtim":(0,0,0,"dtim_5_6",0),
    "dwet":("dwet_5_2",0,0,0,0),
    "fmps":("fmps_5_2",0,0,0,0),
    "gai":(0,0,0,"gai_5_6","gai_5_7"),
    "gmps":("gmps_5_2","gmps_5_3",0,0,0),
    "mai":("mai_5_2",0,0,0,0),
    "mmps":("mmps_5_2",0,0,0,0),
    "pag":("pag_5_2",0,0,"pag_5_6",0),
    "pcc":(0,"pcc_5_3",0,0,"pcc_5_7"),
    "pes":(0,"pes_5_3",0,0,"pes_5_7"),
    "pfld":("pfld_5_2",0,0,0,0),
    "pgr":(0,"pgr_5_3",0,0,"pgr_5_7"),
    "plu":(0,"plu_5_3",0,"plu_5_6",0),
    "pmu":("pmu_5_2","pmu_5_3",0,"pmu_5_6",0),
    "psg":(0,0,0,"psg_5_6","psg_5_7"),
    "shei":(0,"shei_5_3",0,"shei_5_6",0),
    }, 
6:
    {
    "equation_ids":(2,3,5,6,8),  # note: this is the to_id's
    "constant":("act_6_2","act_6_3","act_6_5","act_6_6",0),
    "aai":("aai_6_2","aai_6_3",0,0,0),
    "amps":("amps_6_2","amps_6_3",0,0,0),
    "blmz":(0,0,0,0,"blmz_6_8"),
    "cd1":("cd1_6_2",0,0,0,0),
    "dag":("dag_6_2",0,0,0,0),
    "dfre":("dfre_6_2","dfre_6_3",0,0,"dfre_6_8"),
    "dloc":("dloc_6_2","dloc_6_3",0,0,0),
    "dmu":("dmu_6_2",0,0,0,0),
    "dprd":(0,0,0,0,"dprd_6_8"),
    "dres":("dres_6_2",0,0,0,0),
    "dtim":("dtim_6_2","dtim_6_3",0,0,0),
    "fmps":("fmps_6_2","fmps_6_3",0,0,0),
    "mai":("mai_6_2","mai_6_3",0,0,0),
    "mmps":("mmps_6_2","mmps_6_3",0,0,0),
    "pag":("pag_6_2",0,0,0,0),
    "pcc":("pcc_6_2","pcc_6_3","pcc_6_5",0,0),
    "pcf":("pcf_6_2",0,"pcf_6_5",0,"pcf_6_8"),
    "pes":("pes_6_2","pes_6_3","pes_6_5",0,0),
    "pgr":("pgr_6_2","pgr_6_3",0,0,0),
    "plu":("plu_6_2",0,0,0,"plu_6_8"),
    "pmu":("pmu_6_2","pmu_6_3",0,0,0),
    "psg":("psg_6_2","psg_6_3",0,0,"psg_6_8"),
    "pslp":("pslp_6_2","pslp_6_3",0,0,0),
    "pstr":("pstr_6_2",0,0,0,0),
    "pub":("pub_6_2",0,0,0,0),
    "shei":(0,0,0,0,"shei_6_8"),
    }, 
7:
   {
"equation_ids":(2,3,5,7,8),  # note: this is the to_id's
    "constant":("act_7_2","act_7_3","act_7_5","act_7_7",0),
    "aai":("aai_7_2","aai_7_3",0,0,0),
    "amps":("amps_7_2",0,0,0,0),
    "blmz":("blmz_7_2","blmz_7_3",0,0,"blmz_7_8"),
     "dag":("dag_7_2",0,"dag_7_5",0,0),
    "dcbd":("dcbd_7_2","dcbd_7_3",0,0,0),
    "dfre":(0,0,0,0,"dfre_7_8"),
    "dloc":("dloc_7_2",0,0,0,"dloc_7_8"),
    "dnlr":("dnlr_7_2","dnlr_7_3",0,0,0),
    "dpub":(0,0,0,0,"dpub_7_8"),
    "dres":("dres_7_2",0,0,0,0),
    "dtim":("dtim_7_2","dtim_7_3",0,0,0),
    "dwat":("dwat_7_2",0,0,0,"dwat_7_8"),
    "dwet":(0,"dwet_7_3",0,0,0),
    "fmps":("fmps_7_2","fmps_7_3","fmps_7_5",0,0),
    "gai":(0,0,"gai_7_5",0,0),
    "pcc":("pcc_7_2","pcc_7_3",0,0,"pcc_7_8"),
   "pcf":(0,0,"pcf_7_5",0,0),
    "pes":(0,0,0,0,"pes_7_8"),
    "pfld":("pfld_7_2","pfld_7_3",0,0,0),
    "pgr":("pgr_7_2",0,"pgr_7_5",0,0),
    "plu":("plu_7_2","plu_7_3",0,0,0),
    "psg":("psg_7_2","psg_7_3",0,0,0),
    "pstr":("pstr_7_2",0,0,0,0),
    "pub":("pub_7_2",0,0,0,0),
   "shei":(0,0,"shei_7_5",0,"shei_7_8"),
    }, 
10:
   {
    "equation_ids":(3,5,6,10),  # note: this is the to_id's
    "constant":("constant_10_3","constant_10_5",0, "constant_10_30"),
    "aai":("aai_10_3","aai_10_5",0,0),
    "cd1":(0,0,"cd1_10_6",0),
    "dag":(0,"dag_10_5","dag_10_6",0),
    "dcbd":("dcbd_10_3","dcbd_10_5","dcbd_10_6",0),
    "di":(0,"di_10_5",0,0),
    "dmu":("dmu_10_3",0,0,0),
    "dres":(0,"dres_10_5","dres_10_6",0),
    "dtim":(0,"dtim_10_5","dtim_10_6",0),
    "dwet":(0,"dwet_10_5","dwet_10_6",0),
    "gmps":("gmps_10_3","gmps_10_5","gmps_10_6",0),
    "hd1":("hd1_10_3",0,0,0),
    "mai":("mai_10_3","mai_10_5",0,0),
    "pag":("pag_10_3",0,0,0),
    "pcc":(0,"pcc_10_5","pcc_10_6",0),
    "pfld":("pfld_10_3",0,0,0),
    "pgr":("pgr_10_3","pgr_10_5",0,0),
    "plu":("plu_10_3",0,"plu_10_6",0),
    "pwet":(0,"pwet_10_5","pwet_10_6",0),
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
    