data tq84_ds;
  x = 'eggs';
  y = 'why';

proc /* Implicit step boundary: dataset tq84_ds
        will be created */
     print data=tq84_ds;
run; /* Explicit step boundary: tq84_ds will
        be printed; */
