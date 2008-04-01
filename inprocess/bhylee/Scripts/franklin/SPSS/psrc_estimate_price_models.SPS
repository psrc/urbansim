GET DATA  /TYPE = TXT
 /FILE = 'C:\urbansim_cache\buildings.csv'
 /DELCASE = LINE
 /DELIMITERS = ","
 /ARRANGEMENT = DELIMITED
 /FIRSTCASE = 2
 /IMPORTCASE = ALL
 /VARIABLES =
 parcsqft F5.2
 conditio A5
 bldg_id F2.1
 quality A6
 bldgsqft F4.2
 bldgtype A25
 bldgtyid F2.1
 bldguse A3
 bldgused A25
 county F3.2
 countyid F1.0
 ftprsqft F4.2
 gcdacbd F13.2
 gcwae_da F13.2
 gbgtyped A25
 gbgtype F1.0
 id_parc F13.2
 id_subp F13.2
 bath F4.2
 bedr F1.0
 outbldgf F1.0
 parcelid F6.2
 ptotsqft F5.2
 resunits F1.0
 retvals F6.2
 stories F1.0
 subp_fl F1.0
 tax_ex F1.0
 tot_val F6.2
 unitname A17
 unitpric F6.2
 units F1.0
 yrbuilt F4.2
 .
CACHE.
EXECUTE.

* Compute new variables

COMPUTE log_val = ln(tot_val) .
COMPUTE log_du = ln(resunits) .
COMPUTE log_bsf = ln(bldgsqft) .
COMPUTE log_psf = ln(parcsqft) .
COMPUTE log_gcb = ln(gcdacbd) .
COMPUTE log_gae = ln(gcwae_da) .
EXECUTE .

VARIABLE LABELS
	log_val 'Log of Total Value'
	log_du 'Log of Residential Units'
	log_bsf 'Log of Bldg. Square Feet'
	log_psf 'Log of Parcel Square Feet'
	log_gcb 'Log of Gen. Cost to CBD'
	log_gae 'Log of Empl. w/i 30 Min. GC'
.

* Compute ratio variables

COMPUTE bsf_du = bldgsqft / resunits .
COMPUTE psf_du = parcsqft / resunits .
COMPUTE lbsf_ldu = log_bsf / log_du .
COMPUTE lpsf_ldu = log_psf / log_du .
EXECUTE .

VARIABLE LABELS
	lbsf_ldu 'Log Bldg SF / Log Units'
	lpsf_ldu 'Log Parc SF / Log Units'
	bsf_du 'Bldg SF / Units'
	psf_du 'Parc SF / Units'
.

* Compute interactions among access var's

COMPUTE gcb_gae = 1 / (gcdacbd * gcwae_da) .
COMPUTE lgcblgae = 1 / (log_gcb * log_gae) .
EXECUTE .

VARIABLE LABELS
	gcb_gae 'CBD Addl Access'
	lgcblgae 'Log CBD Addl Access'
.

* Compute interactions with access var's

COMPUTE gcb_du = resunits * gcdacbd .
COMPUTE gae_du = resunits * gcwae_da .
COMPUTE gcb_psf = parcsqft * gcdacbd .
COMPUTE gae_psf = parcsqft * gcwae_da .
COMPUTE gcb_bsf = bldgsqft * gcdacbd .
COMPUTE gae_bsf = bldgsqft * gcwae_da .
COMPUTE gcb_bsu = bsf_du * gcdacbd .
COMPUTE gae_bsu = bsf_du * gcwae_da .
COMPUTE gcb_psu = psf_du * gcdacbd .
COMPUTE gae_psu = psf_du * gcwae_da .
COMPUTE cbae_du = resdus * gcb_gae .
COMPUTE cbae_psf = parcsqft * gcb_gae .
COMPUTE cbae_bsf = bldgsqft * gcb_gae .
COMPUTE cbae_bsu = bsf_du * gcb_gae .
COMPUTE cbae_psu = psf_du * gcb_gae .

COMPUTE lgcb_du = log_du * log_gcb .
COMPUTE lgae_du = log_du * log_gae .
COMPUTE lgcb_psf = log_psf * log_gcb .
COMPUTE lgae_psf = log_psf * log_gae .
COMPUTE lgcb_bsf = log_bsf * log_gcb .
COMPUTE lgae_bsf = log_bsf * log_gae .
COMPUTE lgcb_bsu = lbsf_ldu * log_gcb .
COMPUTE lgae_bsu = lbsf_ldu * log_gae .
COMPUTE lgcb_psu = lpsf_ldu * log_gcb .
COMPUTE lgae_psu = lpsf_ldu * log_gae .
COMPUTE lcbaedu = log_du  * lgcblgae .
COMPUTE lcbaepsf = log_psf  * lgcblgae .
COMPUTE lcbaebsf = log_bsf  * lgcblgae .
COMPUTE lcbaebsu = lbsf_ldu * lgcblgae .
COMPUTE lcbaepsu = lpsf_ldu * lgcblgae .

EXECUTE .

VARIABLE LABELS
	gcb_du 'Gen. Cost to CBD * Units'
	gae_du 'Emp w/i 30-min GC * Units'
	gcb_psf 'Gen. Cost to CBD * Parcel SF'
	gae_psf 'Emp w/i 30-min GC * Parcel SF'
	gcb_bsf 'Gen. Cost to CBD * Bldg. SF'
	gae_bsf 'Emp w/i 30-min GC * Bldg. SF'
	gcb_bsu 'Gen. Cost to CBD * BSF/Unit'
	gae_bsu 'Emp w/i 30-min GC * BSF/Unit'
	gcb_psu 'Gen. Cost to CBD * PSF/Unit'
	gae_psu 'Emp w/i 30-min GC * PSF/Unit'

VARIABLE LABELS
	lgcb_du 'Log Gen. Cost to CBD * Log Units'
	lgae_du 'Log Emp w/i 30-min GC * Log Units'
	lgcb_psf 'Log Gen. Cost to CBD * Log Parcel SF'
	lgae_psf 'Log Emp w/i 30-min GC * Log Parcel SF'
	lgcb_bsf 'Log Gen. Cost to CBD * Log Bldg. SF'
	lgae_bsf 'Log Emp w/i 30-min GC * Log Bldg. SF'
	lgcb_bsu 'Log Gen. Cost to CBD * Log BSF/Unit'
	lgae_bsu 'Log Emp w/i 30-min GC * Log BSF/Unit'
	lgcb_psu 'Log Gen. Cost to CBD * Log PSF/Unit'
	lgae_psu 'Log Emp w/i 30-min GC * Log PSF/Unit'
.

VARIABLE LABELS
	cbae_du 'CBD Addl Access * Units'
	cbae_psf 'CBD Addl Access * Parcel SF'
	cbae_bsf 'CBD Addl Access * Bldg. SF'
	cbae_bsu 'CBD Addl Access * BSF/Unit'
	cbae_psu 'CBD Addl Access * PSF/Unit'
	lcbaedu 'Log CBD Addl Access * Log Units'
	lcbaepsf 'Log CBD Addl Access * Log Parcel SF'
	lcbaebsf 'Log CBD Addl Access * Log Bldg. SF'
	lcbaebsu 'Log CBD Addl Access * Log BSF/Unit'
	lcbaepsu 'Log CBD Addl Access * Log PSF/Unit'
.

FREQUENCIES
  VARIABLES= bldgtype bldgtyid
  /ORDER=  ANALYSIS .

* Single Family Residential

USE ALL.
COMPUTE filter_$=(bldgtyid=19).
VARIABLE LABEL filter_$ 'bldgtyid=19 (FILTER)'.
VALUE LABELS filter_$  0 'Not Selected' 1 'Selected'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .

*This one for comparing to OPUS:
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_psf log_bsf log_gae log_gcb
  .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_psf log_bsf log_gae lgcblgae
  .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_psf log_bsf log_gae
	lgae_bsf lcbaebsf
  .

* Multi-Family Residential

USE ALL.
COMPUTE filter_$=(bldgtyid=12).
VARIABLE LABEL filter_$ 'bldgtyid=12 (FILTER)'.
VALUE LABELS filter_$  0 'Not Selected' 1 'Selected'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_psf log_bsf log_gae lgcblgae
  .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_psf log_bsf log_gae
	lgae_bsf lcbaebsf
  .

* Condo Residential

USE ALL.
COMPUTE filter_$=(bldgtyid=4).
VARIABLE LABEL filter_$ 'bldgtyid=4). (FILTER)'.
VALUE LABELS filter_$  0 'Not Selected' 1 'Selected'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .

*This one for comparing to OPUS:
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_bsf log_gae 
  .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_bsf log_gae lgcblgae
  .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_du lbsf_ldu log_gae lgcblgae
  .

* Commercial

USE ALL.
COMPUTE filter_$=(bldgtyid=3).
VARIABLE LABEL filter_$ 'bldgtyid=3). (FILTER)'.
VALUE LABELS filter_$  0 'Not Selected' 1 'Selected'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER parcsqft bldgsqft gcb_psf
  .

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER parcsqft bldgsqft gae_psf gae_bsf
  .

* Vacant Land

USE ALL.
COMPUTE filter_$=(bldgtyid=23).
VARIABLE LABEL filter_$ 'bldgtyid=23 (FILTER)'.
VALUE LABELS filter_$  0 'Not Selected' 1 'Selected'.
FORMAT filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE .

EXAMINE
  VARIABLES=log_val log_psf log_gae lgcblgae /COMPARE VARIABLE/PLOT=BOXPLOT
 /STATISTICS=NONE/NOTOTAL
  /MISSING=LISTWISE .


REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT log_val
  /METHOD=ENTER log_psf log_gae lgcblgae
  .
