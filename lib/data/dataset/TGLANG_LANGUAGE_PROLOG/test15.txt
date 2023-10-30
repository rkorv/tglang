;******************************************************************************
pro rw,lu
if n_params(0) eq 0 then begin
   print,' '
   print,'* RW - rewind disk file '
   print,'*   calling sequence: RW,lun'
   print,' '
   return
   endif
;
point_lun,lu,0
return
end
