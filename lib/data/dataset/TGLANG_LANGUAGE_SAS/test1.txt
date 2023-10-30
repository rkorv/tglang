TITLE2 "e20125dc0074000";
DATA work.SFe0074dc;
 
	LENGTH FILEID   $6
		   FILETYPE $6
		   STUSAB   $2
		   CHARITER $3
		   SEQUENCE $4
		   LOGRECNO $7;
 
INFILE "L:\Libraries\ACS\Raw\SF_2008_12\dc_Tracts_Block_Groups_Only\e20125dc0074000.txt" DSD TRUNCOVER DELIMITER =',' LRECL=3000;
 
LABEL FILEID  ='File Identification'
      FILETYPE='File Type'  
 	   STUSAB  ='State/U.S.-Abbreviation (USPS)'
 	   CHARITER='Character Iteration'
 	   SEQUENCE='Sequence Number'
 	   LOGRECNO='Logical Record Number'
 
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY PRESENCE OF PEOPLE 60 YEARS AND OVER FOR HOUSEHOLDS */
/*Universe:  Households */
 
B22001e1='Total:'
B22001e2='Household received Food Stamps/SNAP in the past 12 months:'
B22001e3='At least one person in household 60 years or over'
B22001e4='No people in household 60 years or over'
B22001e5='Household did not receive Food Stamps/SNAP in the past 12 months:'
B22001e6='At least one person in household 60 years or over'
B22001e7='No people in household 60 years or over'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY PRESENCE OF CHILDREN UNDER 18 YEARS BY HOUSEHOLD TYPE FOR HOUSEHOLDS */
/*Universe:  Households */
 
B22002e1='Total:'
B22002e2='Household received Food Stamps/SNAP in the past 12 months:'
B22002e3='With children under 18 years:'
B22002e4='Married-couple family'
B22002e5='Other family:'
B22002e6='Male householder, no wife present'
B22002e7='Female householder, no husband present'
B22002e8='Nonfamily households'
B22002e9='No children under 18 years:'
B22002e10='Married-couple family'
B22002e11='Other family:'
B22002e12='Male householder, no wife present'
B22002e13='Female householder, no husband present'
B22002e14='Nonfamily households'
B22002e15='Household did not receive Food Stamps/SNAP in the past 12 months:'
B22002e16='With children under 18 years:'
B22002e17='Married-couple family'
B22002e18='Other family:'
B22002e19='Male householder, no wife present'
B22002e20='Female householder, no husband present'
B22002e21='Nonfamily households'
B22002e22='No children under 18 years:'
B22002e23='Married-couple family'
B22002e24='Other family:'
B22002e25='Male householder, no wife present'
B22002e26='Female householder, no husband present'
B22002e27='Nonfamily households'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY POVERTY STATUS IN THE PAST 12 MONTHS FOR HOUSEHOLDS */
/*Universe:  Households */
 
B22003e1='Total:'
B22003e2='Household received Food Stamps/SNAP in the past 12 months:'
B22003e3='Income in the past 12 months below poverty level'
B22003e4='Income in the past 12 months at or above poverty level'
B22003e5='Household did not receive Food Stamps/SNAP in the past 12 months:'
B22003e6='Income in the past 12 months below poverty level'
B22003e7='Income in the past 12 months at or above poverty level'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (WHITE ALONE) */
/*Universe:  Households with a householder who is White alone */
 
B22005Ae1='Total:'
B22005Ae2='Household received Food Stamps/SNAP in the past 12 months'
B22005Ae3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (BLACK OR AFRICAN AMERICAN ALONE) */
/*Universe:  Households with a householder who is Black or African American alone */
 
B22005Be1='Total:'
B22005Be2='Household received Food Stamps/SNAP in the past 12 months'
B22005Be3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (AMERICAN INDIAN AND ALASKA NATIVE ALONE) */
/*Universe:  Households with a householder who is American Indian and Alaska Native alone */
 
B22005Ce1='Total:'
B22005Ce2='Household received Food Stamps/SNAP in the past 12 months'
B22005Ce3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (ASIAN ALONE) */
/*Universe:  Households with a householder who is Asian alone */
 
B22005De1='Total:'
B22005De2='Household received Food Stamps/SNAP in the past 12 months'
B22005De3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE) */
/*Universe:  Households with a householder who is Native Hawaiian and Other Pacific Islander alone */
 
B22005Ee1='Total:'
B22005Ee2='Household received Food Stamps/SNAP in the past 12 months'
B22005Ee3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (SOME OTHER RACE ALONE) */
/*Universe:  Households with a householder who is Some other race alone */
 
B22005Fe1='Total:'
B22005Fe2='Household received Food Stamps/SNAP in the past 12 months'
B22005Fe3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (TWO OR MORE RACES) */
/*Universe:  Households with a householder who is Two or more races */
 
B22005Ge1='Total:'
B22005Ge2='Household received Food Stamps/SNAP in the past 12 months'
B22005Ge3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (WHITE ALONE, NOT HISPANIC OR LATINO) */
/*Universe:  Households with a householder who is White alone, not Hispanic or Latino */
 
B22005He1='Total:'
B22005He2='Household received Food Stamps/SNAP in the past 12 months'
B22005He3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY RACE OF HOUSEHOLDER (HISPANIC OR LATINO) */
/*Universe:  Households with a householder who is Hispanic or Latino */
 
B22005Ie1='Total:'
B22005Ie2='Household received Food Stamps/SNAP in the past 12 months'
B22005Ie3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY FAMILY TYPE BY NUMBER OF WORKERS IN FAMILY IN THE PAST 12 MONTHS */
/*Universe:  Families */
 
B22007e1='Total:'
B22007e2='Household received Food Stamps/SNAP in the past 12 months:'
B22007e3='Married-couple family:'
B22007e4='No workers'
B22007e5='1 worker'
B22007e6='2 workers:'
B22007e7='Husband and wife worked'
B22007e8='Other'
B22007e9='3 or more workers:'
B22007e10='Husband and wife worked'
B22007e11='Other'
B22007e12='Other family:'
B22007e13='Male householder, no wife present:'
B22007e14='No workers'
B22007e15='1 worker'
B22007e16='2 workers'
B22007e17='3 or more workers'
B22007e18='Female householder, no husband present:'
B22007e19='No workers'
B22007e20='1 worker'
B22007e21='2 workers'
B22007e22='3 or more workers'
B22007e23='Household did not receive Food Stamps/SNAP in the past 12 months:'
B22007e24='Married-couple family:'
B22007e25='No workers'
B22007e26='1 worker'
B22007e27='2 workers:'
B22007e28='Husband and wife worked'
B22007e29='Other'
B22007e30='3 or more workers:'
B22007e31='Husband and wife worked'
B22007e32='Other'
B22007e33='Other family:'
B22007e34='Male householder, no wife present:'
B22007e35='No workers'
B22007e36='1 worker'
B22007e37='2 workers'
B22007e38='3 or more workers'
B22007e39='Female householder, no husband present:'
B22007e40='No workers'
B22007e41='1 worker'
B22007e42='2 workers'
B22007e43='3 or more workers'
/*MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2012 INFLATION-ADJUSTED DOLLARS) BY RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS */
/*Universe:  Households */
/*Median household income in the past 12 months (in 2012 inflation-adjusted dollars)-- */
 
B22008e1='Total:'
B22008e2='Household received Food Stamps/SNAP in the past 12 months'
B22008e3='Household did not receive Food Stamps/SNAP in the past 12 months'
/*RECEIPT OF FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY DISABILITY STATUS FOR HOUSEHOLDS */
/*Universe:  Households */
 
B22010e1='Total:'
B22010e2='Household received Food Stamps/SNAP in the past 12 months:'
B22010e3='Households with 1 or more persons with a disability'
B22010e4='Households with no persons with a disability'
B22010e5='Household did not receive Food Stamps/SNAP in the past 12 months:'
B22010e6='Households with 1 or more persons with a disability'
B22010e7='Households with no persons with a disability'
;
 
 
INPUT
 
FILEID   $ 
FILETYPE $ 
STUSAB   $ 
CHARITER $ 
SEQUENCE $ 
LOGRECNO $ 
 
B22001e1
B22001e2
B22001e3
B22001e4
B22001e5
B22001e6
B22001e7
 
B22002e1
B22002e2
B22002e3
B22002e4
B22002e5
B22002e6
B22002e7
B22002e8
B22002e9
B22002e10
B22002e11
B22002e12
B22002e13
B22002e14
B22002e15
B22002e16
B22002e17
B22002e18
B22002e19
B22002e20
B22002e21
B22002e22
B22002e23
B22002e24
B22002e25
B22002e26
B22002e27
 
B22003e1
B22003e2
B22003e3
B22003e4
B22003e5
B22003e6
B22003e7
 
B22005Ae1
B22005Ae2
B22005Ae3
 
B22005Be1
B22005Be2
B22005Be3
 
B22005Ce1
B22005Ce2
B22005Ce3
 
B22005De1
B22005De2
B22005De3
 
B22005Ee1
B22005Ee2
B22005Ee3
 
B22005Fe1
B22005Fe2
B22005Fe3
 
B22005Ge1
B22005Ge2
B22005Ge3
 
B22005He1
B22005He2
B22005He3
 
B22005Ie1
B22005Ie2
B22005Ie3
 
B22007e1
B22007e2
B22007e3
B22007e4
B22007e5
B22007e6
B22007e7
B22007e8
B22007e9
B22007e10
B22007e11
B22007e12
B22007e13
B22007e14
B22007e15
B22007e16
B22007e17
B22007e18
B22007e19
B22007e20
B22007e21
B22007e22
B22007e23
B22007e24
B22007e25
B22007e26
B22007e27
B22007e28
B22007e29
B22007e30
B22007e31
B22007e32
B22007e33
B22007e34
B22007e35
B22007e36
B22007e37
B22007e38
B22007e39
B22007e40
B22007e41
B22007e42
B22007e43
 
B22008e1
B22008e2
B22008e3
 
B22010e1
B22010e2
B22010e3
B22010e4
B22010e5
B22010e6
B22010e7
;
RUN;
TITLE2;
