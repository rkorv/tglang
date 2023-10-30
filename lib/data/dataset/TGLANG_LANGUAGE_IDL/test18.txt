;;
;; xyouts along line-segments
;;
PRO jwxyouts,xu,yu,text,spacing=spacing,alignment=alignment, $
             show_path=show_path,charsize=charsize,charthick=charthick, $
             text_axes=txtax,clip=sclip,color=color,font=font, $
             noclip=noclip,z=z,normal=normal,device=device,data=data, $
             orientation=orientation,xyouts=xyouts,size=size,offset=offset
   ;;
   ;; Plot the text text along a path defined by the arrays xu,yu. 
   ;;
   ;; Parameters:
   ;;    spacing  : insert an extra amount of spacing*!p.charsize
   ;;               between subsequent characters.
   ;;    alignment: aligns the string with the polygon as in xyouts.
   ;;    charsize : size of the characters
   ;;    offset   : offset of characters (array with 2 elements)
   ;;
   ;; Keywords:
   ;;    show_path: if set, show the polygon
   ;;    xyouts   : if set, behave like xyouts
   ;;
   ;; All other options are just given to xyouts.
   ;;
   ;; Joern Wilms, 1996.10.07
   ;; wilms@astro.uni-tuebingen.de
   ;;

   ;;
   ;; Set all keywords to values that make sense
   ;;
   IF (n_elements(font) EQ 0) THEN  font=!p.font
   IF (n_elements(txtax) EQ 0) THEN txtax=0
   IF (n_elements(z) EQ 0) THEN z=0.
   IF (n_elements(color) EQ 0) THEN color=!p.color
   IF (n_elements(spacing) EQ 0) THEN spacing=1.
   IF (n_elements(alignment) EQ 0) THEN alignment=0.
   IF (n_elements(orientation) EQ 0) THEN orientation=0.
   ;;
   IF (n_elements(charthick) EQ 0) THEN BEGIN 
       charthick=1.
       IF (!p.charthick NE 0.) THEN charthick=!p.charthick
   ENDIF 
   ;;
   IF (n_elements(charsize) EQ 0) THEN BEGIN 
       charsize=1.
       IF (!p.charsize NE 0.) THEN charsize=!p.charsize
       IF (n_elements(size) NE 0) THEN charsize=size
   END
   ;;
   ;; Ensure that one type of coordinate system is used; if none is
   ;; given, use data coordinate system
   ;;
   IF (keyword_set(data)) THEN BEGIN 
       normal=0
       device=0
   END ELSE BEGIN 
       IF (n_elements(data) EQ 0) THEN data=1
   END
   IF (keyword_set(normal)) THEN BEGIN 
       device=0
       data=0
   ENDIF 
   IF (keyword_set(device)) THEN BEGIN 
       normal=0
       data=0
   ENDIF 
   ;;
   ;; Deal with clipping
   ;;
   IF (n_elements(noclip) EQ 0) THEN noclip=1
   IF (n_elements(sclip) EQ 0) THEN BEGIN 
       clip=!p.clip
   END ELSE BEGIN 
       clip=fltarr(4)
       tmp=convert_coord(sclip(0),sclip(1),data=data,normal=normal, $
                         device=device,/to_normal)
       clip(0)=tmp(0,0) & clip(1)=tmp(1,0)
       tmp=convert_coord(sclip(2),sclip(3),data=data,normal=normal, $
                         device=device,/to_normal)
       clip(2)=tmp(0,0) & clip(3)=tmp(1,0)
   END            
   ;;
   ;; Behave like xyouts if /xyouts is given or if array is only one
   ;; point
   ;;
   IF (keyword_set(xyouts) OR (n_elements(xu) LE 1)) THEN BEGIN
       IF (n_elements(xu)*n_elements(yu) EQ 0) THEN BEGIN 
           message,'Need at least one point in jwxyouts'
       ENDIF 
       tmp=convert_coord(xu,yu,data=data,normal=normal, $
                         device=device,/to_normal)
       xyouts,tmp(0,*),tmp(1,*),text,orientation=orientation,$
         alignment=alignment,charsize=charsize,charthick=charthick,$
         text_axes=txtax,color=color,font=font,noclip=noclip,z=z, $
         clip=clip,/normal
       return  
   ENDIF 
   ;;
   ;; Plot Polygon if desired
   ;;
   IF (keyword_set(show_path)) THEN BEGIN 
       tmp=convert_coord(xu,yu,data=data,normal=normal,device=device,/to_data)
       oplot,tmp(0,*),tmp(1,*)
   ENDIF 
   ;;
   ;; Build up the array pos(5,nseg) which contains (in device coordinates!)
   ;;    pos(0,*): x-coordinate of point in polygon
   ;;    pos(1,*): y-coordinate
   ;;    pos(2,*): length of each segment (pos(2,i) is the length of the
   ;;              segment from pos(0,i-1) to pos(0,i)
   ;;    pos(3,*): length from beginning of line to the current point
   ;;
   nseg=n_elements(xu)
   pos=fltarr(4,nseg)
   ;;
   ;; Convert (x,y) into device coordinates
   ;;
   tmp=convert_coord(xu,yu,normal=normal,data=data,device=device,/to_normal)
   pos(0:1,*)=tmp(0:1,*)

   IF (n_elements(offset) NE 0) THEN BEGIN 
       IF (n_elements(offset) EQ 1) THEN BEGIN 
           pos(0:1,*)=pos(0:1,*)+offset(0)
       END ELSE BEGIN 
           pos(0,*)=pos(0,*)+offset(0)
           pos(1,*)=pos(1,*)+offset(1)
       END
   END 

   ;;
   ;; Length of each segment
   ;;
   pos(2,0)=0.
   pos(3,0)=0.
   FOR i=1,nseg-1 DO BEGIN
       dx=pos(0,i)-pos(0,i-1)
       dy=pos(1,i)-pos(1,i-1)
       pos(2,i)=sqrt(dx*dx+dy*dy)
       pos(3,i)=pos(3,i-1)+pos(2,i)
   ENDFOR 
   ;;
   ;; Find starting position from alignment
   ;;
   xyouts,-50.,-50.,text,charsize=charsize,width=stl
   stl=stl*spacing
   stretch=stl*(spacing-1.)/(strlen(text)-1)
   po=alignment*(pos(3,nseg-1)-stl)
   ;;
   ;; Loop over String, outputting characters
   ;;
   i=0
   seg=1
   ;;
   WHILE (i LT strlen(text)) DO BEGIN 
       ;;
       ;; Character to be output
       ;;
       a=strmid(text,i,1)
       ;;
       ;; Advance by half the size of the character
       ;;
       xyouts,-50.,-50.,a,charsize=charsize,width=dp,/normal
       po=po+0.5*dp
       ;;
       ;; Line-segment where to output character
       ;;
       IF (po LT pos(3,nseg-1)) THEN BEGIN 
           WHILE (pos(3,seg) LT po) DO seg=seg+1
       END ELSE BEGIN 
           seg=nseg-1
       END 
       ;;
       ;; Position on line where to output character
       ;;
       p=(po-pos(3,seg-1))/pos(2,seg)
       ;;
       ;; Normal-coordinates to output character
       ;;
       dx=pos(0,seg)-pos(0,seg-1)
       dy=pos(1,seg)-pos(1,seg-1)
       xx=pos(0,seg-1)+p*(pos(0,seg)-pos(0,seg-1))
       yy=pos(1,seg-1)+p*(pos(1,seg)-pos(1,seg-1))

       ;;
       ;; Orientation of character
       ;;
       angle=atan(!d.y_size*dy/!d.x_size,dx)
       angle=angle*180./!pi
       ;;
       ;; Output character
       ;;
       xyouts,xx,yy,a,/normal,orientation=angle,alignment=0.5, $
         charsize=charsize,charthick=charthick,text_axes=txtax, $
         clip=clip,color=color,font=font,noclip=noclip,z=z, $
         width=wi
       ;;
;       po=po+spacing*wi
       po=po+dp*0.5+stretch
       ;;
       i=i+1
   ENDWHILE 
END 

