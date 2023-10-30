    5 CALL SHELL("cls")
   10 ON ERROR GOSUB 80
   20 C = 0
    : REM C will hold the number of data items
   25 PRINT "Reading data elements"
   30 READ N
   40 PRINT N
   50 C = C + 1
   70 GOTO 30
   80 print "Error line #, error number # ";erl;err
   90 PRINT "Read ";C;" data elements"
    : INPUT "Press enter :";w
  100 DIM A(C)
    : REM now we can allocate the array to hold all data
  110 RESTORE
    : REM MOVE data pointer to start
  120 FOR I=1 TO C
  130   READ A(I)
  140 NEXT
  150 print
    : print
  160 PRINT "Array:"
  170 FOR I=1 TO C
  180   PRINT A(I);" ";
  190 NEXT
  195 PRINT
  200 END
 1000 DATA 12,107,0,20,443,218,232,468,561
 1010 DATA 71,187,936,436,4,50,110,320,120

