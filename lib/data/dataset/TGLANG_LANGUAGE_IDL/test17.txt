function keyword_setx, value
;
; This is a function very similar to the standard
; IDL function 'keyword_set'. It will return
; '1' (true) even if the keyword has been set to zero
; in which case 'keyword_set' returns '0' (false).
;
;  NJW  980520
;
sz = size(value)
if sz(0)+sz(1) eq 0 then return, 0 else return, 1
end
