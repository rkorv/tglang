
\ 
\ e.g.
\ 
\ 0 enum ZERO
\ enum ONE
\ enum TWO
\ drop

: enum 
    create 
        dup , 1+ 
    does> 
        @ 
;

