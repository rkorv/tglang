$title write_solution_worst_case
$ontext
write solution1.txt and solution2.txt files for
worst case solution
$offtext

$if not set solution1 $set solution1 solution1.txt
file solution1 /'%solution1%'/;

put solution1;
put '--bus section' /;
put 'I, VM, VA, B' /;
loop(i$Bus(i),
  put
    i.tl:0 ', '
    1.0:0:10 ', '
    0.0:0:10 ', '
    0.0:0:10 /;
    #busVoltMagSol(i):0:10 ', '
    #busVoltAngSol(i):0:10 ', '
    #busSwshAdmImagSol(i):0:10 /;
);
put '--generator section' /;
put 'I, ID, P, Q' /;
loop((i,j)$Gen(i,j),
  put
    i.tl:0 ', '
    j.tl:0 ', '
    (0.5*(genPMin(i,j) + genPMax(i,j))$GenActive(i,j)):0:10 ', '
    (0.5*(genQMin(i,j) + genQMax(i,j))$GenActive(i,j)):0:10 /
    #genPowRealSol(i,j):0:10 ', '
    #genPowImagSol(i,j):0:10 /;
);
putclose;

$if not set solution2 $set solution2 solution2.txt
file solution2 /'%solution2%'/;
solution2.ap = 0;
put solution2;
putclose;
solution2.ap = 1;

loop(k$ctg(k),
  put solution2;
  put '--contingency ' /
  put 'LABEL' /;
  put k.tl:0 /;
  put '--bus section' /;
  put 'I, VM, VA, B' /;
  loop(i$Bus(i),
    put
      i.tl:0 ', '
      #busCtgVoltMagSol(i,k):0:10 ', '
      #busCtgVoltAngSol(i,k):0:10 /;
      1.0:0:10 ', '
      0.0:0:10 ', '
      0.0:0:10 /;
      #busVoltMagSol(i):0:10 ', '
      #busVoltAngSol(i):0:10 ', '
      #busSwshAdmImagSol(i):0:10 /;
  );
  put '--generator section' /;
  put 'I, ID, P, Q' /;
  loop((i,j)$Gen(i,j),
    put
      i.tl:0 ', '
      j.tl:0 ', '
      #genCtgPowImagSol(i,j,k):0:10 /;
      (0.5*(genPMin(i,j) + genPMax(i,j))$(GenActive(i,j) and not GenCtgInactive(i,j,k))):0:10 ', '
      (0.5*(genQMin(i,j) + genQMax(i,j))$(GenActive(i,j) and not GenCtgInactive(i,j,k))):0:10 /
      #genPowRealSol(i,j):0:10 ', '
      #genPowImagSol(i,j):0:10 /;
  );
  put '--delta section' /;
  put 'DELTA' /;
  put
    0.0:0:10 /;
    #ctgPowRealChangeSol(i,k):0:10 /;
  putclose;
);
