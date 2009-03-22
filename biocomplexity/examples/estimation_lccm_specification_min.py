# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

specification = {}

specification = {
2:
    {
    "equation_ids":(1,2),
    "constant":(0, "act_2_2"),
    "aai":("aai_2_1", 0),
   "amps":("amps_2_1", 0),
      "pmf":("pmf_2_1", 0),
    "pmu":("pmu_2_1", 0),
    "psg":("psg_2_1", 0),
   "tiv":("tiv_2_1", 0),
    "ugl":("ugl_2_1", 0)
    },
 3:
    {
    "equation_ids":(1,2,3),
    "constant":(0,"act_3_2","act_3_3"),
    "aai":("aai_3_1","aai_3_2", 0),
     "ugl":("ugl_3_1","ugl_3_2", 0)
    },
4:
    {
    "equation_ids":(1,2,3),  # note: this is the to_id's
    "constant":(0, "act_4_2", "act_4_3"),   #there is no constant term in the equation for to_id 1
    "aai":(0, "aai_4_2","aai_4_3"),
    "amps":(0, "amps_4_2","amps_4_3"),
    "ugl":(0, "ugl_4_2","ugl_4_3")
    }, 
5:
    {
    "equation_ids":(1,2,3,5,6,7),  # note: this is the to_id's
    "constant":("act_5_1","act_5_2","act_5_3","act_5_5","act_5_6",0),
    "ugl":("ugl_5_1","ugl_5_2","ugl_5_3", 0,"ugl_5_6","ugl_5_7")
    }, 
6:
    {
    "equation_ids":(1,2,3,4,5,6,8),  # note: this is the to_id's
    "constant":("act_6_1","act_6_2","act_6_3","act_6_4","act_6_5","act_6_6",0),
    "cd1":("cd1_6_1","cd1_6_2","cd1_6_3","cd1_6_4","cd1_6_5", 0,"cd1_6_8"),
    }, 
7:
   {
    "equation_ids":(1,2,3,4,5,7,8),  # note: this is the to_id's
    "constant":("act_7_1","act_7_2","act_7_3","act_7_4","act_7_5","act_7_7",0),
    "aai":("aai_7_1","aai_7_2","aai_7_3","aai_7_4","aai_7_5", 0,"aai_7_8"),
    }, 
10:
   {
    "equation_ids":(1,2,3,10),  # note: this is the to_id's
    "constant":("constant_10_1","constant_10_2",0, "constant_10_10"),
    "aai":("aai_10_1","aai_10_2","aai_10_3",0),
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
    