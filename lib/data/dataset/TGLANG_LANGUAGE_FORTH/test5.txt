\ TAP output

Variable test# 
0 test# !
Variable test-planned
test-planned off

\ Output a newline and flush the output stream
: cr-flush
  cr
  outfile-id flush-file throw
;

: 0.r ( n -- )
  0 .r
;

\ Use before any tests to declare the number of tests you intend to run
: plan ( n -- )
  ." 1.." 0.r cr-flush
  test-planned on
;

\ Use before tests to make it explicit that you don't know how many
\ tests will run. Currently a no-op but don't rely on this in future
: no-plan ( -- )

;

\ Called after testing to output a possible trailing plan.
: test-done ( -- )
  test-planned @ 0= if
    test# @ plan
  then
;

\ Redefine bye to output trailing plan
warnings @ warnings off
: bye ( -- )
  test-done
  bye
;
warnings !

\ Output a diagnostic to stderr
: diag ( c-addr u -- )
  >stderr
  ." # "
  type
;

\ Create quoting version
:NONAME \"-parse diag ;
:NONAME POSTPONE S\" POSTPONE diag ;
interpret/compile: diag"

: diag-out ( n c-addr u -- )
  >stderr
  diag
  0.r
  cr-flush
;

: diag-where ( c-addr u -- )
  >stderr
  diag
  sourcefilename type
  ." , line "
  sourceline# 0.r
  cr-flush
;

\ Report a test result. The supplied string should contain a description
\ of the test
: ok ( f c-addr u -- )
  rot 0= if
    s" Test failure at " diag-where
    ." not " 
  then
  ." ok "
  test# dup @ 1+ dup . swap !
  type cr-flush
;

\ Indicate test success
: pass ( c-addr u -- )
  true -rot ok
;

\ Indicate test failure
: fail ( c-addr u -- )
  false -rot ok
;

\ Output expected / got diagnostic
: exp-got ( n n -- n n )
  2dup
  s" expected: " diag-out
  s"      got: " diag-out
;

\ Output a list of values to stderr
: exp-list ( n0 .. nn u -- )
  >stderr
  0 ?do
      .
  loop
  cr-flush
;

\ Test that passes if two values are equal
: =ok ( n n c-addr u -- )
  2swap 2dup <> if
    exp-got
  then
  = -rot ok
;

\ Given two lists followed by a single count move the last elements of
\ each list to the top of stack
: expose-pair ( n0 ... nn m0 ... mn u -- n1 ... nn m1 ... nn u n0 m0 )
  dup 2* roll
  over 1+ roll
  rot 1- -rot
;

\ Compare the stack contents with a counted list of values. The test
\ passes if the values are equal
: =deeply ( n1 ... nn m1 ... mn n c-addr u -- )
  2>r true >r
  begin
    ?dup while
    expose-pair
    2dup <> if
      rot 1+ dup >r
      rot >r
      diag" expected: " exp-list
      r> r>
      diag"      got: " exp-list
      r> drop false >r
      0 0 0
    then
    2drop
  repeat
  
  r> 2r> ok
;

\ Create quoting versions
:NONAME \"-parse ok ;
:NONAME POSTPONE S\" POSTPONE ok ;
interpret/compile: ok"
:NONAME \"-parse pass ;
:NONAME POSTPONE S\" POSTPONE pass ;
interpret/compile: pass"
:NONAME \"-parse fail ;
:NONAME POSTPONE S\" POSTPONE fail ;
interpret/compile: fail"
:NONAME \"-parse =ok ;
:NONAME POSTPONE S\" POSTPONE =ok ;
interpret/compile: =ok"
:NONAME \"-parse =deeply ;
:NONAME POSTPONE S\" POSTPONE =deeply ;
interpret/compile: =deeply"

\ Create a stack frame in which tests can be run to verify they don't
\ pollute the stack

Variable frame 
0 frame !

: {sp ( -- )
  frame @
  sp@ frame !
;

: }sp ( -- )
  frame @ sp!
  frame !
;

: =sp ( n -- )
  >r sp@ frame @ swap - cell / r>
  2dup <> if
    exp-got
  then
  = ok" stack balanced"
;

: ?sp ( -- )
  0 =sp
;

\ Verify that an exception is thrown
: throw-ok ( xt u c-addr u -- )
  2swap swap
  {sp swap
  try
    execute         \ should fail
    0               \ in case of success
[undefined] recover [if]
  restore
[else]
  recover
[then]
    \ I'm not quite sure why but a failed execute
    \ leaves an extra value behind the exception code
    nip
  endtry
  swap }sp
  2swap 
  =ok
;

:NONAME \"-parse throw-ok ;
:NONAME POSTPONE S\" POSTPONE throw-ok ;
interpret/compile: throw-ok"
