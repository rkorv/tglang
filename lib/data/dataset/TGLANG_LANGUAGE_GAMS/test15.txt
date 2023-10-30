execseed =         6;
set      k               disjunctions                    /1*5/ 
         i               disjunctive terms               /1*10/ 
         j               original variable dimension     /1*10/ 
;


**** END USER INPUT

* Generate random problem
* Random disjunctive program with constraints in disjunctions of the form
* a1(k,i)*exp(sum(j,a4(k,i,j)*x(j))) <= a2(k,i)*z + a3(k,i)
* log(a1(k,i)) + sum(j,a4(k,i,j)*x(j)) <= log(a2(k,i)*z + a3(k,i))
* Kexp((a2(k,i)*z + a3(k,i))/a1(k,i),1,sum(j,a4(k,i,j)*x(j)))

parameters       c(j)            cost coefficient for variable j
                 a1(k,i)         coefficient for exponential term
                 a2(k,i)         coefficient for linear term
                 a3(k,i)         constant coefficient
                 a4(k,i,j)       linear coefficient for exponent for var j
                 x_up(j)         upper bound for var j
                 x_lo(j)         lower bound for var j
                 z_up            upper bound for z
                 z_lo            lower bound for z
                 M(k,i)
                 M2(k,i)
                 lambda(k,j)
;

c(j)       = -uniform(.01,1);
a1(k,i)    = uniform(.01,1);
a2(k,i)    = uniform(.01,1);
a3(k,i)    = uniform(.01,1);
a4(k,i,j)  = uniform(.01,1);
x_up(j)    = 10;
x_lo(j)    = 0;


* Begin problem

variables        obj             "Objective variable"
                 x(j)            "Variables"
                 ni(k,i,j)       "Disaggregated variables x"
                 mu(k,i)         "Disaggregated variables z"
                 x_cone2(k,i)  "Disaggregated variables x for Big-M conic reformulation"
                 ni_cone2(k,i)  "Disaggregated variables x for hull conic reformulation"
;

binary variable  y(k,i)
;

positive variable t(k,i)           "Dummy variable equal to one for Big-M conic reformulation"
                 x_cone(k,i)  "Disaggregated variables x for Big-M conic reformulation"
                 ni_cone(k,i)  "Disaggregated variables x for hull conic reformulation"
                 z               "Extra variable z >= exp(sum(x's))"
                 z_cone(k,i)  "Disaggregated variables z for Big-M log conic reformulation"
                 z_cone2(k,i)  "Disaggregated variables z for Big-M log conic reformulation"
                 mu_cone(k,i)  "Disaggregated variables z for hull log conic reformulation"
                 mu_cone2(k,i)  "Disaggregated variables z for hull log conic reformulation"
;
t.fx(k,i) = 1;

equations        objective
                 disj_BM
                 disj_BMc
                 disj_BMlog
                 disj_BMlogc
                 sum_bin
                 disag
                 disag2
                 disj_HRLee
                 disj_HRLeelog
                 disj_HR
                 disj_HRlog
                 disj_HRlogc
                 bound_up
                 bound_lo
                 disj_HRc
                 extr_HRc
                 cone_HRc
                 extr_HRlogc
                 cone_HRlogc
                 extr_BMc
                 cone_BMc
                 extr_BMlogc
                 cone_BMlogc
                 bound2_up
                 bound2_lo
;

*Variable bounds

x.up(j) = x_up(j) ;
x.lo(j) = x_lo(j) ;
ni.up(k,i,j) = x_up(j) ;
ni.lo(k,i,j) = x_lo(j) ;
ni_cone2.up(k,i) = sum(j,a4(k,i,j)*x_up(j)) ;
ni_cone2.lo(k,i) = sum(j,a4(k,i,j)*x_lo(j)) ;
ni_cone.up(k,i) = exp(sum(j,a4(k,i,j)*x_up(j))) ;
ni_cone.lo(k,i) = exp(sum(j,a4(k,i,j)*x_lo(j))) ;

*z_up       = 20;
z_up       = ( smax( (k,i),( a1(k,i)*exp( sum(j,a4(k,i,j)*x_lo(j)) ) + a3(k,i) )/(sqr(a2(k,i))) ) );
z_lo       = 0;
display z_up;

z.up = z_up ;
z.lo = z_lo ;
mu.up(k,i) = z_up ;
mu.lo(k,i) = z_lo ;

*Calculation M parameter
M(k,i) = a1(k,i)*exp(sum(j,max(a4(k,i,j)*x_up(j),a4(k,i,j)*x_lo(j)))) - (a2(k,i)*z_lo + a3(k,i));
M2(k,i) =log(a1(k,i)) + sum(j,max(a4(k,i,j)*x_up(j),a4(k,i,j)*x_lo(j))) - log(a2(k,i)*z_lo + a3(k,i));
*M2(k,i) = log(a1(k,i)*exp(sum(j,max(a4(k,i,j)*x_up(j),a4(k,i,j)*x_lo(j)))) - (a2(k,i)*z_lo + a3(k,i)));

scalar epsilon /1e-8/;

objective ..               obj =e= sum(j,c(j)*x(j));

sum_bin(k)..               sum(i,y(k,i)) =e= 1;

disj_BM(k,i)..             a1(k,i)*exp(sum(j,a4(k,i,j)*x(j))) =l= a2(k,i)*z + a3(k,i) + M(k,i)*(1-y(k,i));

disj_BMc(k,i)..            a1(k,i)*x_cone(k,i) =l= a2(k,i)*z + a3(k,i) + M(k,i)*(1-y(k,i));

disj_BMlog(k,i)..          log(a1(k,i)) + sum(j,a4(k,i,j)*x(j)) =l= log(a2(k,i)*z + a3(k,i)) + M2(k,i)*(1-y(k,i));

disj_BMlogc(k,i)..         log(a1(k,i)) + sum(j,a4(k,i,j)*x(j)) =l= z_cone(k,i) + M2(k,i)*(1-y(k,i));

disj_HR(k,i)..             a1(k,i)*((y(k,i)*(1-epsilon)+epsilon)*exp(sum(j,a4(k,i,j)*ni(k,i,j)/(y(k,i)*(1-epsilon)+epsilon))) - epsilon*(1-y(k,i)) ) =l= a2(k,i)*mu(k,i) + a3(k,i)*y(k,i);

disj_HRlog(k,i)..          y(k,i)*log(a1(k,i)) + sum(j,a4(k,i,j)*ni(k,i,j)) =l= (y(k,i)*(1-epsilon)+epsilon)*log(a2(k,i)*mu(k,i)/(y(k,i)*(1-epsilon)+epsilon) + a3(k,i)) - epsilon*log(0 + a3(k,i))*(1-y(k,i));

disag(k,j)..               sum(i,ni(k,i,j)) =e= x(j);
disag2(k)..                sum(i,mu(k,i)) =e= z;

bound_up(k,i,j)..          ni(k,i,j) =l= x_up(j)*y(k,i);
bound_lo(k,i,j)..          ni(k,i,j) =g= x_lo(j)*y(k,i);

bound2_up(k,i)..           mu(k,i) =l= z_up*y(k,i);
bound2_lo(k,i)..           mu(k,i) =g= z_lo*y(k,i);

disj_HRc(k,i)..            a1(k,i)*ni_cone(k,i) =l= a2(k,i)*mu(k,i) + a3(k,i)*y(k,i);

disj_HRlogc(k,i)..         y(k,i)*log(a1(k,i)) + sum(j,a4(k,i,j)*ni(k,i,j)) =l= mu_cone(k,i);

cone_HRc(k,i)..            ni_cone(k,i) =g= y(k,i)*exp(ni_cone2(k,i)/y(k,i));

extr_HRc(k,i)..            ni_cone2(k,i) =e= sum(j,a4(k,i,j)*ni(k,i,j));

cone_HRlogc(k,i)..         mu_cone2(k,i) =g= y(k,i)*exp(mu_cone(k,i)/y(k,i));

extr_HRlogc(k,i)..         mu_cone2(k,i) =e= a2(k,i)*mu(k,i) + a3(k,i);

cone_BMc(k,i)..            x_cone(k,i) =g= t(k,i)*exp(x_cone2(k,i)/t(k,i));

extr_BMc(k,i)..            x_cone2(k,i) =e= sum(j,a4(k,i,j)*x(j));

cone_BMlogc(k,i)..         z_cone2(k,i) =g= t(k,i)*exp(z_cone(k,i)/t(k,i));

extr_BMlogc(k,i)..         z_cone2(k,i) =e= a2(k,i)*z + a3(k,i);

disj_HRLee(k,i)..          a1(k,i)*((y(k,i)+epsilon)*exp(sum(j,a4(k,i,j)*ni(k,i,j)/(y(k,i)+epsilon))) ) =l= a2(k,i)*mu(k,i) + a3(k,i)*(y(k,i)+epsilon);

disj_HRLeelog(k,i)..       (y(k,i)+epsilon)*log(a1(k,i)) + sum(j,a4(k,i,j)*ni(k,i,j)) =l= (y(k,i)+epsilon)*log(a2(k,i)*mu(k,i)/(y(k,i)+epsilon) + a3(k,i));

model prob_BM /objective,disj_BM,sum_bin/;
model prob_BMc /objective,disj_BMc,sum_bin,cone_BMc,extr_BMc/;
model prob_BMlogc /objective,disj_BMlogc,sum_bin,cone_BMlogc,extr_BMlogc/;
model prob_BMlog /objective,disj_BMlog,sum_bin/;
model prob_HR /objective,disj_HR,sum_bin,disag,bound_up,bound_lo,disag2,bound2_up,bound2_lo/;
model prob_HRlog /objective,disj_HRlog,sum_bin,disag,bound_up,bound_lo,disag2,bound2_up,bound2_lo/;
model prob_HRlogc /objective,disj_HRlogc,sum_bin,disag,bound_up,bound_lo,disag2,bound2_up,bound2_lo,cone_HRlogc,extr_HRlogc/;
model prob_HRc /objective,disj_HRc,sum_bin,disag,bound_up,bound_lo,disag2,bound2_up,bound2_lo,cone_HRc,extr_HRc/;
model prob_HRL /objective,disj_HRLee,sum_bin,disag,bound_up,bound_lo,disag2,bound2_up,bound2_lo/;
model prob_HRLlog /objective,disj_HRLeelog,sum_bin,disag,bound_up,bound_lo,disag2,bound2_up,bound2_lo/;

prob_BM.nodLim = 1e8;
prob_HR.nodLim = 1e8;
prob_HRL.nodLim = 1e8;
prob_HRc.nodLim = 1e8;

option
         reslim = 3600
         iterlim = 1e9
         bratio = 1
         threads = 1
;
*Initialize variables

x.l(j) = 0;
ni.l(k,i,j) = 0;
ni_cone2.l(k,i) = sum(j,a4(k,i,j)*ni.l(k,i,j));
ni_cone.l(k,i) = exp(ni_cone2.l(k,i));

y.l(k,i) = 1;

z.l = z_up;
mu.l(k,i) = z.l;
mu_cone2.l(k,i) = a2(k,i)*mu.l(k,i) + a3(k,i);
mu_cone.l(k,i) = log(mu_cone2.l(k,i));
Solve prob_BMc using MINLP minimizing obj;
