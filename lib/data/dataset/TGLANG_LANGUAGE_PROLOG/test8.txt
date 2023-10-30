;***************************************************************************
function make_2darr,x,y,nx,ny,xaxis,yaxis,xlim=xlim,ylim=ylim,scale=scale, $
   stp=stp,helpme=helpme,silent=silent,quiet=quiet
; x,y are indices
if n_params() lt 2 then helpme=1
if n_elements(x) eq 0 then helpme=1
if n_elements(y) eq 0 then helpme=1
if keyword_set(helpme) then begin
   print,' '
   print,'* function MAKE_2DARR : make 2-D array out of list of coordinates'
   print,'* calling sequence: ARRAY=MAKE_2DARR(X,Y,NX,XY)'
   print,'*    X: list of X coordinates of events'
   print,'*    Y: list of Y coordinates of events'
   print,'*    NX,NY: size of array'
   print,'*    XAXIS,YAXIS: X, Y axes corresponding to binned events'
   print,'* '
   print,'* KEYWORDS:'
   print,'*    SCALE: if set, scale to max, min values
   print,'*    SILENT: if not set, number of point in image is printed'
   print,'*    XLIM,YLIM: optional 2D vectors giving maximum, minimum X,Y '
   print,' '
   return,-1
   endif
if keyword_set(quiet) then silent=1
;
cutxy=0
if (n_elements(xlim) eq 2) and (n_elements(ylim) eq 2) then cutxy=1
if cutxy then begin
;   print,min(x),max(x)
   kg=where((x ge xlim(0)) and (x le xlim(1)) and (y ge ylim(0)) and $
      (y le ylim(1)),np)
   x=x(kg) & y=y(kg)
;   print,min(x),max(x)
   endif
;
mx=min(x) & my=min(y)
x=x-mx
y=y-my
;print,mx,max(x)
;
if (n_elements(ny) eq 0) and (n_elements(nx) eq 1) then ny=nx
;print,nx,ny
;if (n_elements(nx) eq 0) or (n_elements(ny) eq 0) then scale=0
if n_elements(nx) ne 1 then nx=long(max(x)-min(x)+0.5)+1L else nx=long(nx)
if n_elements(ny) ne 1 then ny=long(max(y)-min(y)+0.5)+1L else ny=long(ny)
xlim=[min(x),max(x)] 
ylim=[min(y),max(y)]
;if (fix(max(xlim)+0.5) ne nx) or (fix(max(ylim)+0.5) ne ny) then scale=1
xaxis=mx+findgen(nx)*(xlim(1)-xlim(0))/float(nx)
yaxis=my+findgen(ny)*(ylim(1)-ylim(0))/float(ny)
;
;if keyword_set(scale) then begin
   iy=fix((ny-1)*(y-ylim(0))/(ylim(1)-ylim(0)))
   ix=fix((nx-1)*(x-xlim(0))/(xlim(1)-xlim(0)))
   iy=(iy>0)<(ny-1)
   ix=(ix>0)<(nx-1)
   array=lonarr(nx,ny)     ;1-d
;
   case 1 of
      nx le ny: begin
         for i=0L,nx-1 do begin
            k=where(ix eq i,nk)
            if nk gt 0 then begin
               z=histogram(iy(k),min=0,bin=1)
               array(0,i)=z
               endif
            endfor
         end
      else: begin
         for i=0L,ny-1 do begin
            k=where(iy eq i,nk)
            if nk gt 0 then begin
               z=histogram(ix(k),min=0,bin=1)
               array(0,i)=z
               endif
            endfor
         end
      endcase
if not keyword_set(silent) then print,np,total(array),' events'
if keyword_set(stp) then stop,'MAKE_2DARR>>>'
return,array
end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;array=intarr(nx*ny)     ;1-d
;index=((y*nx+x)>0)<(long(nx)*long(ny))
;index=index(sort(index))
;nk=n_elements(index)     ;number of points
;np=nk
;if not keyword_set(silent) then print,np,' events in image'
;while nk gt 0 do begin
;   k=uniq(index)
;   ik=index(k)
;   array(ik)=array(ik)+1             ;increment array
;   index(k)=-1
;   kk=where(index ge 0,nk)
;   if nk gt 0 then index=index(kk)
;   endwhile
;array=reform(array,nx,ny)
;if long(total(array)) ne np then begin
;   bell
;   print,'*** MAKE_2DARR WARNING: only ',total(array),' events in image'
;   endif
;if keyword_set(stp) then stop,'MAKE_2DARR>>>'
;return,array
;end
