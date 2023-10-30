options ls = 100 nocenter;
libname c90 '/home/groups/sorkin/quadros/data/1990/';

proc import out= c90.all90 
			datafile = "/home/groups/sorkin/quadros/data/raw/all90.dta"
			replace;
run;
proc contents data= c90.all90;
run;

proc datasets lib= c90  memtype=data;
   modify all90;
     attrib _all_ label=' ';
     attrib _all_ format=;
run;

proc contents data= c90.all90;
run;
