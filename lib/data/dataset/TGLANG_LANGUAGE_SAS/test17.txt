TITLE2 "m20125md0116000";
DATA work.SFm0116md;
 
	LENGTH FILEID   $6
		   FILETYPE $6
		   STUSAB   $2
		   CHARITER $3
		   SEQUENCE $4
		   LOGRECNO $7;
 
INFILE "L:\Libraries\ACS\Raw\SF_2008_12\md_Tracts_Block_Groups_Only\m20125md0116000.txt" DSD TRUNCOVER DELIMITER =',' LRECL=3000;
 
LABEL FILEID  ='File Identification'
      FILETYPE='File Type'  
 	   STUSAB  ='State/U.S.-Abbreviation (USPS)'
 	   CHARITER='Character Iteration'
 	   SEQUENCE='Sequence Number'
 	   LOGRECNO='Logical Record Number'
 
/*UNWEIGHTED HOUSING UNIT SAMPLE */
/*Universe: Housing Units */
 
B98001m1='Initial addresses selected'
B98001m2='Final number of housing unit interviews'
/*UNWEIGHTED GROUP QUARTERS POPULATION SAMPLE */
/*Universe: Population in Group Quarters */
 
B98002m1='Initial sample selected'
B98002m2='Final actual interviews'
B98002m3='Final synthetic interviews'
/*HOUSING UNIT COVERAGE RATE */
/*Universe: Housing Units */
 
B98011m1='Total'
/*TOTAL POPULATION COVERAGE RATE BY SEX */
/*Universe: Total Population */
 
B98012m1='Total:'
B98012m2='Male'
B98012m3='Female'
/*TOTAL POPULATION COVERAGE RATE BY WEIGHTING RACE AND HISPANIC OR LATINO GROUPS */
/*Universe: Total Population */
 
B98013m1='Total:'
/*Not Hispanic or Latino: */
B98013m2='White'
B98013m3='Black or African American'
B98013m4='American Indian and Alaska Native'
B98013m5='Asian'
B98013m6='Native Hawaiian and Other Pacific Islander'
B98013m7='Hispanic or Latino'
/*GROUP QUARTERS POPULATION COVERAGE RATE */
/*Universe: Population in Group Quarters */
 
B98014m1='Total'
/*HOUSING UNIT RESPONSE AND NONRESPONSE RATES WITH REASONS FOR NONINTERVIEWS */
/*Universe: Housing Units */
 
B98021m1='Response Rate'
B98021m2='Nonresponse Rate:'
B98021m3='Refusal'
B98021m4='Unable To Locate'
B98021m5='No One Home'
B98021m6='Temporarily Absent'
B98021m7='Language Problem'
B98021m8='Insufficient Data'
B98021m9='Other Reason'
/*GROUP QUARTERS POPULATION RESPONSE AND NONRESPONSE RATES WITH REASONS FOR NONINTERVIEWS */
/*Universe: Population in Group Quarters */
 
B98022m1='Response Rate'
B98022m2='Nonresponse Rate:'
B98022m3='Group Quarters Person Refusal'
B98022m4='Unable To Locate Group Quarters Person'
B98022m5='Resident Temporarily Absent'
B98022m6='Language Problem'
B98022m7='Insufficient Data'
B98022m8='Group Quarters Person Other Reason'
B98022m9='Whole Group Quarters Refusal'
B98022m10='Whole Group Quarters Other Reason'
/*OVERALL PERSON CHARACTERISTIC IMPUTATION RATE */
/*Universe: Total Population */
 
B98031m1='Total'
/*OVERALL HOUSING UNIT CHARACTERISTIC IMPUTATION RATE */
/*Universe: Total Population */
 
B98032m1='Total'
;
 
 
INPUT
 
FILEID   $ 
FILETYPE $ 
STUSAB   $ 
CHARITER $ 
SEQUENCE $ 
LOGRECNO $ 
 
B98001m1
B98001m2
 
B98002m1
B98002m2
B98002m3
 
B98011m1
 
B98012m1
B98012m2
B98012m3
 
B98013m1
B98013m2
B98013m3
B98013m4
B98013m5
B98013m6
B98013m7
 
B98014m1
 
B98021m1
B98021m2
B98021m3
B98021m4
B98021m5
B98021m6
B98021m7
B98021m8
B98021m9
 
B98022m1
B98022m2
B98022m3
B98022m4
B98022m5
B98022m6
B98022m7
B98022m8
B98022m9
B98022m10
 
B98031m1
 
B98032m1
;
RUN;
TITLE2;
