Set
  InitStr1       Streams used in calculation of FcPen and XcPen
  InitStr2       Streams used in calculation of FPen;

Parameters
  FTarget(Str)
  FcTarget(Str,Comp)
  PTarget(Str)
  Ttarget(Str)
  XcTarget(Str,Comp);

Variables
  FPen
  FcPen
  TPen
  PPen
  XcPen;

Equation
  EqInitCscObj2
  EqFPen
  EqFcPen
  EqTPen
  EqPPen
  EqXcPen;

EqFPen..
  FPen =e= SUM(Str$InitStr2(Str), (F(Str) - FTarget(Str))*(F(Str) - FTarget(Str)));

EqFcPen..
  FcPen =e= SUM(Comp, SUM(Str$InitStr1(Str), (Fc(Str,Comp) - FcTarget(Str,Comp))*(Fc(Str,Comp) - FcTarget(Str,Comp))));

EqTPen..
  TPen =e= SUM(Str$(InitStr1(Str) OR InitStr2(Str)), (Ttarget(Str) - Tscaled(Str))*(Ttarget(Str) - Tscaled(Str)) );

EqPPen..
  PPen =e= SUM(Str$(InitStr1(Str) OR InitStr2(Str)), (PTarget(Str) - P(Str))*(PTarget(Str) - P(Str)));

EqXcPen..
  XcPen =e= SUM(Comp, SUM(Str$InitStr1(Str), (XcTarget(Str,Comp) - Xc(Str,Comp))*(XcTarget(Str,Comp) - Xc(Str,Comp)) ));

EqInitCscObj2..
  Z =e= SUM(Str$InitStr2(Str), sL(Str) + sV(Str)) + FPen
        + 0.1*FcPen
        + 0.1*TPen
        + 0.1*PPen;

FcTarget(Str,Comp) = Fc.l(Str,Comp);

Model InitCscObjs /EqFPen, EqFcPen, EqTPen, EqPPen, EqInitCscObj2/;

Model InitCscNewObj /MassBalEqns - EqTotCompMolBalEd1, EqSumFrac, SimpleThermo, EqCascade, EqCsdSimple, InitCscObjs/;
* EqSumFrac

Model InitMassBal /MassBalEqns, EqSumFrac, EqFcPen/;

***** CEOS Initialization *****


Equation
  InitObj2
  EqInitShdwL(Str,Str2,Str3)
  EqInitShdwV(Str,Str2,Str3)
  EqInitObjShdw;

InitObj2..
  Z =e= SUM(Str$fEOSStr(Str), sL(Str)) + SUM(Str, sV(Str)) + TPen + 1000*XcPen + PPen;

EqInitShdwL(Str,Str2,Str3)$(DewPoint(Str) AND ComMap(Str,Str3,Str2))..
  P(Str2) =e= Pd(Str2);

EqInitShdwV(Str,Str2,Str3)$(BubPoint(Str) AND ComMap(Str,Str2,Str3))..
  P(Str2) =e= Pb(Str2);

EqInitObjShdw..
  Z =e= TPen + PPen + XcPen;

Model InitShdwXc /EqInitObjShdw, EqPBub, EqPDew, EqPvap, EqTPen, EqPPen, EqXcPen, EqT1SumMF, EqT1cpyT, EqT1cpyP/;

Model InitCEOS /InitObj2, BasicCEOSEqns/;
*Model TPequal /EqTRelThrmE,EqPRelThrmE,EqTRelCmpr,EqPRelCmpr,EqPRel1Sptr,EqTRel1Sptr/;

Model InitCEOS1 /InitObj2, BasicCEOSEqns, EqSumFrac, EqTPen, EqPPen, EqXcPen/;

Model InitCEOS2 /InitObj2, CubicEOSEqns, EqSumFrac, EqTPen, EqPPen, EqXcPen/;

Parameter XcTarget(Str,Comp), Ttarget(Str);

XcTarget(Str,Comp) = Xc.l(Str,Comp);

Ttarget(Str) = Tscaled.l(Str);

Equations InitObj3, InitObj4;

InitObj3..
*  Z =e= SUM(Str, F(Str)*sL(Str)) + SUM(Str, F(Str)*sV(Str))
*         + 1000*XcPen + TPen + 0.01*PPen;

  Z =e= SUM(Str$fEOSStr(Str), sL(Str)) + SUM(Str, sV(Str)) + TPen + 1000*XcPen + PPen;

InitObj4..
  Z =e= 10*(liqPen + vapPen) + 1000*XcPen + TPen + PPen;

*Model InitCEOS3 /InitObj3, EqXcPen, EqTPen, EqPPen, CubicEOSEqns, BubbleDewEqns, EqSumFrac, EqSpltrCEOSThermo, EqSpltr - EqMolBalSptr, EqTRelThrmE, EqPRelThrmE/;

Model InitCEOS3 /InitObj3, EqXcPen, EqTPen, EqPPen, CubicEOSEqns, BubbleDewEqns, EqSumFrac/;
* BubbleDewEqns

Model InitCscCEOS /MassBalEqns - EqTotCompMolBalEd1, EqSumFrac, CubicEOSEqns, BubbleDewEqns, EqCascade, EqCsdCEOS, InitCscObjs/;

Model InitCEOS4 /InitObj4, EqXcPen, EqTPen, EqPPen, EqLiqPen, EqVapPen CubicEOSEqns, BubbleDewEqns, EqSumFrac, EqSpltrCEOSThermo, EqSpltr - EqMolBalSptr, EqTRelThrmE, EqPRelThrmE, EqSplitFrac/;

Set
  MinSlacks(Str) Streams for which slacks should be minimized / /;

Equations InitCEOSObj;

InitCEOSObj..
  Z =e= SUM(MinSlacks, sV(MinSlacks) + sL(MinSlacks)) + 100*TPen+ 10*XcPen + 10*PPen;

Model InitCEOS5 /InitCEOSObj, EqXcPen, EqTPen, EqPPen, BasicCEOSEqns, EqSumFrac/;

Model InitCEOS6 /InitCEOSObj, EqXcPen, EqTPen, EqPPen, CubicEOSEqns, EqSumFrac, BubbleDewEqns, PhaseStabilityEqns/;


***** Initialize CEOS for MESH Model *****

Equation EqInitCEOSObj;

EqInitCEOSObj..
  Z =e= TPen + PPen + XcPen;

Model InitCEOSTrays /EqInitCEOSObj, BasicCEOSEqns, EqSumFrac, EqTPen, EqPPen, EqXcPen/;

Model InitCEOSTrays2 /EqInitCEOSObj, CubicEOSEqns, EqSumFrac, EqTPen, EqPPen, EqXcPen/;

***** MESH Model *****

Parameter
  effTarget(Trays);

Equation
  EqInitObj4
  EqInitObj5;

EqInitObj4..
  Z =e= FcPen + 100*XcPen + 0.1*SUM(Trays, Power(effTarget(Trays) - eff(Trays),2)) + PPen + 10*TPen;

EqInitObj5..
  Z =e= FcPen + SUM(Trays$ActvT(Trays), SUM(Comp, Power(Kslack(Trays,Comp),2)));

options NLP = GAMSCHK;

Model ASU_Init_TrayByTray1 /TrayEqnsWithBypass - EqTrayKCEOS2, EqTrayKCEOS2Alt, CubicEOSEqns, EqStreams - EqTscaled,EqInitObj5, EqFcPen/;
* MassBalancesForTrayModel

Model ASU_Init_TrayByTray2 /TrayEqnsWithBypass, CubicEOSEqns, EqStreams - EqTscaled, EqInitObj4, EqFcPen, EqXcPen, EqTPen, EqPPen/;
* BypassEffEqns
