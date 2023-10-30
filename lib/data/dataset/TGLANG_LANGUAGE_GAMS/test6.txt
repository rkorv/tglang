* This file should be included in the master.gms (for the place of the
* INCLUDE see the master_old.gms

* Declarations of the outcome variables and the corresponding relations.
* The names of the outcome variables will be available in the interactive
* MCMA (Multiple-Criteria Model Analysis) application, where the user
* will select those outcome variables that will serve as criteria.
* The declarations of the variables and the relations, together with
* the provided definitions (specifications) of relations will be
* integrated with the core model defined in model_core.gms
*
*
* Declarations of the outcome variables (to be available as criteria)
Variables
	CO2_CUM		Total CO2
	COST_CUM		Total cost
	;
*
* Declarations of the relations defining outcome variables
Equations
	CO2_CUM_DEF		definition of total CO2 emission
	COST_CUM_DEF	definition of the total cost
	;
* Ad-hoc scaling parameter (assumes scaled parameters; therefore it
* scales on;u COST_CUM to have the cost values of the same order of
* of magnitude as the CO2_CUM values
Parameter
	scal_cost  / 1.e-6 / 
	scal_emm   /0.5/ ;
*
* Definitions of the outcome variables
* NOTE: the definitions use parameters and variables of the core model
COST_CUM_DEF..
	COST_CUM =E= scal_cost *
		SUM( (node,year), df_period(year) * COST_NODAL(node,year) ) ;
CO2_CUM_DEF..
	CO2_CUM =E= SUM( (node,emission,type_tec,year),
		EMISS(node,emission,type_tec,year) )*scal_emm ;

