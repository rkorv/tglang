;+
; Project     : SOHO-CDS
;
; Name        : GET_SUB_REGION
;
; Purpose     : get coordinate range in an image
;
; Category    : imaging
;
; Syntax      : sub=get_sub_region()
;
; Inputs      : None (but a plot must already exist)
;
; Opt. Inputs : None
;
; Outputs     : SUB=[xmin,xmax,ymin,ymax] = selected region
;
; Opt. Outputs: None
;
; Keywords    : PIXEL = return limits in pixel units
;               RUBBER = use rubber band in place of BOX_CURSOR
;
; History     : Written 22 November 1997, D. Zarro, SAC/GSFC
;               5 December 2014, Zarro (ADNET)
;               - changed () to []
;
; Contact     : dzarro@solar.stanford.edu
;-

function get_sub_region,rubber=rubber,pixel=pixel,err=err
err=''
rubber=keyword_set(rubber)
pixel=keyword_set(pixel)

if rubber then message,'Use LEFT cursor to select sub-region',/cont else $
 message,'Use MIDDLE cursor to size sub-region and RIGHT to select',/cont

wshow
if rubber then begin
 dregion=drawbox()
 sx=dregion[0] & sy=dregion[1]
 dx=dregion[2] & dy=dregion[3]
endif else begin
 box_cursor2,sx,sy,nx,ny
 dx=sx+nx & dy=sy+ny
endelse

if ~pixel then begin
 coords =  Convert_Coord([sx, dx], [sy, dy], /Device, /To_Data)
 return,[coords[0,0], coords[0,1], coords[1,0], coords[1,1]]
endif else return,[sx,dx,sy,dy]
 
end

