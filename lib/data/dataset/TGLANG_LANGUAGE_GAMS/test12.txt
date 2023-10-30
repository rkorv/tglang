execseed =         6;
set      k               number of clusters              /1*5/ 
         i               number of points                /1*20/ 
         j               number of dimensions            /1*2/ 
;
alias(i,ii);
alias(j,jj);
alias(k,kk);


**** END USER INPUT


* Generate random problem

parameters       a1(i,j)         quadratic coefficient for variable j
                 a2(i,j)         linear coefficient for variable j
                 a3(i,j)         constant coefficient
                 M(i,k)
                 p(i,j)          points positions
                 c_up            upper bound of centroid locations (defined by hypercube)
                 d_up            upper bound of distances (defined by hypercube)
;

p(i,j)     = uniform(0,1);
a1(i,j)    = 1;
a2(i,j)    = -2*p(i,j);
a3(i,j)    = sqr(p(i,j));
c_up(k,j)  = 1;
d_up(i)    = sqrt(card(j))*c_up('1','1');

* Begin problem

variables        obj
;

binary variable  y(i,k)  binary indicating if point i belongs to cluster k
;

positive variable d(i)   distance of each point to its centroid
                  c(k,j) position of the cluster's centroid
                  c1(i,k,j) disaggregation of the centroid variable while being active
                  c0(i,k,j) disaggregation of the centroid variable while being inactive
                  c1_cone(i,k,j) conic disaggregation of the centroid variable while being active
                  mu(i,k)    disaggregation of the distance variable
                  t(i,k)     extra constraint for conic disaggregation
;

equations        objective    objective function
                 disj_BM      Big-M disaggregation of constraints
                 sum_bin      Sum of binary variables being equal to zero
                 disj_HRLee   Lee formulation of Hull constraints
                 disj_HRE     Exact formulation of Hull constraints
                 disj_HR      Sawaya formulation of Hull constraints
                 bound_up0    bound constraint for centroid variable while being inactive
                 bound_up1    bound constraint for centroid variable while being active
                 bound_up2    bound constraint for distance variable
                 disag        disaggregation constraint for centroid variables
                 disag2       disaggregation constraint for distance variables
                 disj_HR2     Hull constraint using socp
                 disj_HR2conv convexification of socp for nonlinear constraints
                 extr_HR      Hull constraints includind extra socp variable
                 disj_HRc     Hull constraint using diaggregated socp
                 cone_HR      definition of conic extra variable
                 symmetry     centroids are ordered in ascending order (symmetry breaking)
                 logic_const  each cluster contains at least one point
;

*Variable bounds
c.up(k,j) = c_up(k,j);
c1.up(i,k,j) = c_up(k,j);
c0.up(i,k,j) = c_up(k,j);
d.up(i)   = d_up(i);
mu.up(i,k)   = d_up(i);
c1_cone.up(i,k,j) = sqrt(2*a1(i,j))*c1.up(i,k,j) ;
t.up(i,k) = sum(j,a1(i,j)*sqr(c1.up(i,k,j)));

*Calculation M parameter
M(i,k) = sum(j,a1(i,j)*sqr(c.up(k,j))) + sum(j,a3(i,j));

scalar epsilon /1e-4/;

symmetry(k)$(ord(k) > 1).. c(k-1,'1') =l= c(k,'1');
logic_const(k)..      sum(i,y(i,k)) =g= 1;


objective ..               obj =e= sum(i,d(i));
disj_BM(i,k)..             sum(j,a1(i,j)*sqr(c(k,j))) + sum(j,a2(i,j)*c(k,j)) + sum(j,a3(i,j)) - d(i) =l= M(i,k)*(1-y(i,k));
sum_bin(i)..               sum(k,y(i,k)) =e= 1;

*HR
disj_HRLee(i,k)..          sum(j,a1(i,j)*sqr(c1(i,k,j)))/(y(i,k)+epsilon) + sum(j,a2(i,j)*c1(i,k,j)) + sum(j,a3(i,j))*(y(i,k)+epsilon) - mu(i,k) =l= 0;
disj_HR(i,k)..             sum(j,a1(i,j)*sqr(c1(i,k,j)))/(y(i,k)*(1-epsilon)+epsilon) + sum(j,a2(i,j)*c1(i,k,j)) + sum(j,a3(i,j))*y(i,k) - mu(i,k) =l= 0;
disj_HRE(i,k)..            sum(j,a1(i,j)*sqr(c1(i,k,j)))/y(i,k) + sum(j,a2(i,j)*c1(i,k,j)) + sum(j,a3(i,j))*y(i,k) - mu(i,k) =l= 0;
disag(i,k,j)..             c1(i,k,j) + c0(i,k,j) =e= c(k,j);
disag2(i)..                sum(k,mu(i,k)) =e= d(i);
bound_up0(i,k,j)..         c0(i,k,j) =l= c_up(k,j)*(1-y(i,k));
bound_up1(i,k,j)..         c1(i,k,j) =l= c_up(k,j)*y(i,k);
bound_up2(i,k)..           mu(i,k) =l= d_up(i)*y(i,k);

*HR2
disj_HR2(i,k)..            (y(i,k)*t(i,k)) =g= sum(j,a1(i,j)*sqr(c1(i,k,j)));
disj_HR2conv(i,k)..        sqr(y(i,k) + t(i,k)) =g= (sum(j,a1(i,j)*sqr(c1(i,k,j)))*4 + sqr(y(i,k) - t(i,k)));

extr_HR(i,k)..             t(i,k) + sum(j,a2(i,j)*c1(i,k,j)) + sum(j,a3(i,j))*y(i,k) - mu(i,k) =l= 0;

disj_HRc(i,k)..            2*(y(i,k)*t(i,k)) =g= sum(j,sqr(c1_cone(i,k,j)));
cone_HR(i,k,j)..           c1_cone(i,k,j) =e= sqrt(2*a1(i,j))*c1(i,k,j);

model prob_BM /objective,disj_BM,sum_bin,symmetry,logic_const/;
model prob_HR /objective,disj_HR,sum_bin,disag,disag2,bound_up0,bound_up1,bound_up2,symmetry,logic_const/;
model prob_HRL /objective,disj_HRLee,sum_bin,disag,disag2,bound_up0,bound_up1,bound_up2,symmetry,logic_const/;
model prob_HRE /objective,disj_HRE,sum_bin,disag,disag2,bound_up0,bound_up1,bound_up2,symmetry,logic_const/;
model prob_HR2 /objective,disj_HR2,sum_bin,disag,disag2,bound_up0,bound_up1,bound_up2,symmetry,logic_const,extr_HR/;
model prob_HR2conv /objective,disj_HR2conv,sum_bin,disag,disag2,bound_up0,bound_up1,bound_up2,symmetry,logic_const,extr_HR/;
model prob_HRc /objective,disj_HRc,sum_bin,disag,disag2,bound_up0,bound_up1,bound_up2,symmetry,logic_const,extr_HR,cone_HR/;

prob_BM.nodLim = 1e8;
prob_HR.nodLim = 1e8;
prob_HRL.nodLim = 1e8;
prob_HRE.nodLim = 1e8;
prob_HR2.nodLim = 1e8;
prob_HR2conv.nodLim = 1e8;
prob_HRc.nodLim = 1e8;

option   optcr = 1e-5
         reslim = 3600
         iterlim = 1e9
         solprint = off
         limrow = 0
         limcol = 0
         bratio = 1
         threads = 1
;
y.l(i,k) = 1;
c.l(k,j) = 0.5;
d.l(i) = sqrt(card(j))*c.l('1','1');
mu.l(i,k)   = d.l(i);
c1.l(i,k,j) = c.l(k,j);
c0.l(i,k,j) = c.l(k,j);
c1_cone.l(i,k,j) = sqrt(2*a1(i,j))*c1.l(i,k,j) ;
t.l(i,k) = sum(j,a1(i,j)*sqr(c1.l(i,k,j)));


$if not set TYPE $set TYPE MIQCP
Solve prob_HR2 using %TYPE% minimizing obj;
