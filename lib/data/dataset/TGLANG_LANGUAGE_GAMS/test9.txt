execseed =         9;
set      d               dimensions                    /1*10/ 
         n               data points                   /1*20/ 
;
scalar sigma standard deviation /2/; 

alias(n,nn);

* To generate random points of n-dimensions to be classified, we choose to
* generate 2 clusters being at a Mahalanobis distance such that the points are
* at most sigma standard deviations away from the center of the distributions
* This is computed via an inverse Chi-squared distribution with d degrees of
* freedom computed at probabilities (0.68,0.95,0.99) correspondind to
* Mahalanobis distances of 1, 2 and 3 sigmas in the 1d case.
* This distance is then divided in 2 and in the square root of d, such that we
* place the centers of the distributions centered at opposite corners of the
* d-dimensional hypercube.
set dims /1*10/;
set sigmas /1*3/;

table distances(dims,sigmas)
	1		2			3
1	0.5		1			1.5
2	0.535694518	0.878925075		1.215995378
3	0.542120864	0.817765337		1.086140476
4	0.543108786	0.77924752		1.007823795
5	0.542567758	0.752125518		0.954078456
6	0.541541047	0.731688538		0.914286748
7	0.540378059	0.715569459		0.883309153
8	0.539209861	0.70243089		0.858315775
9	0.538087228	0.691452356		0.83760349
10	0.537028438	0.68209872		0.820078036
;

scalar distance;
loop(dims,
	loop(sigmas,
	        if(card(d) = ord(dims) and sigma = ord(sigmas),
	                distance = distances(dims,sigmas);
		);
	);
);
display distance;



binary variable y(n), z(n);

equation discrete_vars(n);

discrete_vars(n).. z(n) =e= 1-y(n);

* Data points
parameter x(n,d);

* The first half of the points are generated from a n-dimensional Gaussian
* distribution with standard deviation 1 and centered in the point
* (distance,distance,...,distance)
x(n,d) = normal(distance,1);

* The second half of the points are generated from a n-dimensional Gaussian
* distribution with standard deviation 1 and centered in the point
* (-distance,-distance,...,-distance)
loop(n,
	if(ord(n) <= card(n)/2,
		x(n,d) = normal(-distance,1);
	);
);


* Objective variable
variable obj;

* Coefficients of the linear decision
variables theta(d), theta0;

positive variable t(n), u_n(n), v_n(n), e_n1(n), e_n2(n), u_p(n), v_p(n), e_p1(n), e_p2(n), s_p(n), s_n(n);

* Dummy variables added for conic reformulation of Big-M
negative variables exp_n1(n), exp_p1(n), exp_p2(n)
variable exp_n2(n);
e_n1.fx(n) = 1;
e_n2.fx(n) = 1;
e_p1.fx(n) = 1;
e_p2.fx(n) = 1;


* Parameters used to compute big-M, not directly enforced though
parameters theta_min, theta_max, theta0_min, theta0_max;
theta_min = -1000;
theta_max = 1000;
theta0_min = -1000;
theta0_max = 1000;


parameter M;
M(n) = log(1 + exp(max(
sum(d,theta_min*x(n,d))-theta0_min ,
sum(d,theta_max*x(n,d))+theta0_max)
));

display M;

* General problem constraints
equations fobj, cons_extra, cons_pextra, cons_nextra, cons_logic1, cons_logic2;

* Objective function
fobj.. sum(n,t(n)) =e= obj;

* Absolute value reformulation: Disaggregation of term in positive and negative
cons_extra(n).. sum(d,theta(d)*x(n,d))+theta0 =e= s_p(n) - s_n(n);

* Absolute value reformulation: Positive part = 0 if y = 1
cons_nextra(n).. s_p(n) =l= M(n)*(1-y(n));

* Absolute value reformulation: Negative part = 0 if y = 0
cons_pextra(n).. s_n(n) =l= M(n)*(y(n));

* Logic constraints, support of y has to be within 45-55% of number of points
cons_logic1.. sum(n,y(n)) =l= card(n)*0.55;
cons_logic2.. sum(n,y(n)) =g= card(n)*0.45;

* Big-M constraints
equations cons_p, cons_n;

*cons_n(n).. log(1+exp(sum(d,theta(d)*x(n,d))+theta0)) - t(n) =l= M(n)*(y(n));
cons_n(n).. log(1+exp(s_p(n) + s_n(n))) - t(n) =l= M(n)*(y(n));
*cons_p(n).. log(1+exp(-(sum(d,theta(d)*x(n,d))+theta0))) - t(n) =l= M(n)*(1-y(n));
cons_p(n).. log(1+exp(-(s_p(n) + s_n(n)))) - t(n) =l= M(n)*(1-y(n));

* Big-M conic reformulation constraints
equations cons_p1, cons_p2, cons_p3, cons_n1, cons_n2, cons_n3, extra_p1, extra_p2, extra_n1, extra_n2;

* First side of the disjunction disaggregation. Negative deviation.
cons_n1(n).. u_n(n) + v_n(n) - 1 =l= M(n)*(y(n));
cons_n2(n).. v_n(n) =g= e_n1(n)*exp(exp_n1(n)/e_n1(n));
cons_n3(n).. u_n(n) =g= e_n2(n)*exp(exp_n2(n)/e_n2(n));
extra_n1(n).. exp_n1(n) =e= -t(n) - M(n)*(y(n));
extra_n2(n).. exp_n2(n) =e= (s_p(n) + s_n(n))-t(n) - M(n)*(y(n));

* Second side of the disjunction disaggregation. Positive deviation.
cons_p1(n).. u_p(n) + v_p(n) - 1 =l= M(n)*(1-y(n));
cons_p2(n).. v_p(n) =g= e_p1(n)*exp(exp_p1(n)/e_p1(n));
cons_p3(n).. u_p(n) =g= e_p2(n)*exp(exp_p2(n)/e_p2(n));
extra_p1(n).. exp_p1(n) =e= -t(n) - M(n)*(1-y(n));
extra_p2(n).. exp_p2(n) =e= -(s_p(n) + s_n(n))-t(n) - M(n)*(1-y(n));

* General hull reformulation constraints
equations disagg_n, disagg_p, disagg_t, bound_n1, bound_p1, bound_t1, bound_n0, bound_p0, bound_t0;

* Hull reformulation variables
positive variables s_p_1, s_n_1, t_1, s_p_0, s_n_0, t_0;

* Disaggregation constraints
* Negative deviation
disagg_n(n).. s_n_1(n) + s_n_0(n) =e= s_n(n);
* Positive deviation
disagg_p(n).. s_p_1(n) + s_p_0(n) =e= s_p(n);
* Margin
disagg_t(n).. t_1(n) + t_0(n) =e= t(n);

*Bounds constraints
* y = 0 -> Positive deviations accounted
bound_n0(n).. s_p_0(n) =l= M(n)*(1-y(n));
bound_p0(n).. s_n_0(n) =l= M(n)*(1-y(n));
bound_t0(n).. t_0(n) =l= M(n)*(1-y(n));
* y = 1 -> Negative deviations accounted
bound_n1(n).. s_p_1(n) =l= M(n)*(y(n));
bound_p1(n).. s_n_1(n) =l= M(n)*(y(n));
bound_t1(n).. t_1(n) =l= M(n)*(y(n));

* Different reformulation constraints
equation cons_n_HRE, cons_p_HRE, cons_n_HRL, cons_p_HRL, cons_n_HRS, cons_p_HRS;

* Epsilon parameter for hull reformulation
parameter epsilon /1e-4/;

* Exact reformulation
cons_n_HRE(n).. ((1-y(n)))*log(1+exp(s_p_0(n)/((1-y(n))) + s_n_0(n)/((1-y(n))))) - t_0(n) =l= 0;
cons_p_HRE(n).. (y(n))*log(1+exp(-(s_p_1(n)/(y(n)) + s_n_1(n)/(y(n))))) - t_1(n) =l= 0;


* Lee reformulation
cons_n_HRL(n).. ((1-y(n))+epsilon)*log(1+exp(s_p_0(n)/((1-y(n))+epsilon) + s_n_0(n)/((1-y(n))+epsilon))) - t_0(n) =l= 0;
cons_p_HRL(n).. (y(n)+epsilon)*log(1+exp(-(s_p_1(n)/(y(n)+epsilon) + s_n_1(n)/(y(n)+epsilon)))) - t_1(n) =l= 0;


* Sawaya reformulation
cons_n_HRS(n).. (((1-y(n))*(1-epsilon)+epsilon))*log(1+exp(s_p_0(n)/(((1-y(n))*(1-epsilon)+epsilon)) + s_n_0(n)/(((1-y(n))*(1-epsilon)+epsilon))))  - epsilon*y(n)*log(2) - t_0(n) =l= 0;
cons_p_HRS(n).. ((y(n)*(1-epsilon)+epsilon))*log(1+exp(-(s_p_1(n)/((y(n)*(1-epsilon)+epsilon)) + s_n_1(n)/((y(n)*(1-epsilon)+epsilon))))) - epsilon*(1-y(n))*log(2) - t_1(n) =l= 0;

* Conic reformulation
equation cons_n_HRC, cons_n2_HRC, cons_n3_HRC, cons_n4_HRC,
cons_p_HRC, cons_p2_HRC, cons_p3_HRC, cons_p4_HRC
extra_n1_HRC, extra_n2_HRC, extra_p1_HRC, extra_p2_HRC;
binary variable z(n), z2(n), y2(n);
z.l(n) = 1;
y.l(n) = 1;
z2.l(n) = 1;
y2.l(n) = 1;
* First side of the disjunction disaggregation. Negative deviation.
cons_n_HRC(n).. u_n(n) + v_n(n) =l= z(n);
cons_n2_HRC(n).. v_n(n) =g= z(n)*exp(exp_n1(n)/z(n));
cons_n3_HRC(n).. u_n(n) =g= z2(n)*exp(exp_n2(n)/z2(n));
cons_n4_HRC(n).. z2(n) =e= 1-y(n);
extra_n1_HRC(n).. exp_n1(n) =e= -t_0(n);
extra_n2_HRC(n).. exp_n2(n) =e= (s_p_0(n) + s_n_0(n))-t_0(n);
* Second side of the disjunction disaggregation. Negative deviation.
cons_p_HRC(n).. u_p(n) + v_p(n) =l= y(n);
cons_p2_HRC(n).. v_p(n) =g= y(n)*exp(exp_p1(n)/y(n));
cons_p3_HRC(n).. u_p(n) =g= y2(n)*exp(exp_p2(n)/y2(n));
cons_p4_HRC(n).. y2(n) =e= y(n);
extra_p1_HRC(n).. exp_p1(n) =e= -t_1(n);
extra_p2_HRC(n).. exp_p2(n) =e= -(s_p_1(n) + s_n_1(n))-t_1(n);


* Variable initialization
theta0.l = 0;
theta.l(d) = 1;
t.l(n)$(y.l(n) = 0) = log(1+exp(sum(d,theta.l(d)*x(n,d))+theta0.l));
t.l(n)$(y.l(n) = 1) = log(1+exp(-(sum(d,theta.l(d)*x(n,d))+theta0.l)));

* Norm parameter to choose farthest points and assign them to different sides of classifier
parameter norm(n);
norm(n) = sign(sum(d,sign(x(n,d))*sqr(x(n,d))))*sqrt(abs(sum(d,sign(x(n,d))*sqr(x(n,d)))));
*Fix left-most component to belong to the negative group and right-most
* to belong to the positive group as symmetry breaking
parameter i /0/;
loop(n,
	i = i+1;
	if(norm(n) = smax(nn,norm(nn)),
		y.fx(n) = 1;
		y2.fx(n) = 1;
		display i;
	);
	if(norm(n) = smin(nn,norm(nn)),
		z.fx(n) = 1;
		z2.fx(n) = 1;
		display i;
	);
);

model logistic_BM /discrete_vars,cons_n,cons_p,cons_logic1,cons_logic2,fobj,cons_extra,cons_pextra,cons_nextra/;
model logistic_BMc /discrete_vars,cons_n1,cons_n2,cons_n3,extra_n1,extra_n2,cons_p1,cons_p2,cons_p3,
extra_p1,extra_p2,cons_logic1,cons_logic2,fobj,cons_extra,cons_pextra,cons_nextra/;
model logistic_HRL /discrete_vars,cons_n_HRL,cons_p_HRL,cons_logic1,cons_logic2,fobj,cons_extra,cons_pextra,cons_nextra,disagg_n,disagg_p,disagg_t, bound_n1, bound_p1, bound_t1, bound_n0, bound_p0, bound_t0/;
model logistic_HRE /discrete_vars,cons_n_HRL,cons_p_HRL,cons_logic1,cons_logic2,fobj,cons_extra,cons_pextra,cons_nextra,disagg_n,disagg_p,disagg_t, bound_n1, bound_p1, bound_t1, bound_n0, bound_p0, bound_t0/;
model logistic_HRS /discrete_vars,cons_n_HRS,cons_p_HRS,cons_logic1,cons_logic2,fobj,cons_extra,cons_pextra,cons_nextra,
disagg_n,disagg_p,disagg_t, bound_n1, bound_p1, bound_t1, bound_n0, bound_p0, bound_t0/;
model logistic_HRc /discrete_vars,cons_n_HRC,cons_p_HRC,cons_logic1,cons_logic2,fobj,cons_extra,cons_pextra,cons_nextra,
cons_n2_HRC,cons_n3_HRC,cons_n4_HRC,
disagg_n,disagg_p,disagg_t, bound_n1, bound_p1, bound_t1, bound_n0, bound_p0, bound_t0
extra_n1_HRC,extra_n2_HRC
,cons_p2_HRC,cons_p3_HRC,cons_p4_HRC,
extra_p1_HRC,extra_p2_HRC/;


solve logistic_BM using minlp min obj;

