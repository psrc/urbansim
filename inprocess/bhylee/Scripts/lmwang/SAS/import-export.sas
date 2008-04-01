proc import datafile="h:\pfaz_01.tab"
out=f01
dbms=tab
replace;
getnames=yes;
run;

proc export data=f01
outfile="C:\eclipse\workspace\Scripts\lmwang\dispersal\pf01.dbf"
replace;
run;

/*
proc print data=thob.gridcells_exported;
   where grid_id = 971327;
run;

libname thob odbc
   noprompt="uid=urbansim;pwd=UrbAnsIm4Us;dsn=trondheim-hlc-output;"
   stringdates=yes;
*/

libname output odbc datasrc="trondheim-hlc-output"
user=urbansim password=UrbAnsIm4Us
DBCREATE_TABLE_OPTS='TYPE=MyISAM';

libname baseyear odbc datasrc="trondheim-hlc-baseyear"
user=urbansim password=UrbAnsIm4Us
DBCREATE_TABLE_OPTS='TYPE=MyISAM';

proc sql;
create table pf30 as
select f.faz_id, hh.year, count(*) as counts
from output.households_exported as hh
      left outer join baseyear.gridcells as gc
        on hh.grid_id = gc.grid_id
      left outer join baseyear.zones_in_faz f
        on gc.zone_id = f.zone_id
where hh.year= 2030
group by faz_id
;

quit;
