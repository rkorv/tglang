; Created	14-04-11	to gather the plots_yyyymmdd.sav from gail

pro gather_plots, fls

window, xs=1024, ys=1024

restore,'c2mask.sav'
restore,'c3mask.sav'

for i=0,n_elements(fls)-1 do begin

	loadct, 0
	restore, fls[i]

	if strmid(fls[i],strpos(fls[i],'plots_')+19,1) eq '0' then begin
		case strmid(fls[i],strpos(fls[i],'plots_')+21,2) of
			'C2':	tvscl, sigrange(da*c2mask)
			'C3':	tvscl, sigrange(da*c3mask)
		endcase
	endif

	set_line_color
	plots,res[0,*],res[1,*],psym=3,/device,color=5
	plots,xf_out,yf_out,psym=1,color=3,/device
	plots,[xc,flank1x],[yc,flank1y],psym=-3,/device
	plots,[xc,flank2x],[yc,flank2y],psym=-3,/device

	if i ne n_elements(fls)-1 then begin
		if strmid(fls[i+1],strpos(fls[i+1],'plots_')+19,1) eq '0' then begin
			case strmid(fls[i],strpos(fls[i],'plots_')+21,2) of
				'C2':   x2png, strmid(fls[i],strpos(fls[i],'plots_')+6,12)+'C2'
				'C3':   x2png, strmid(fls[i],strpos(fls[i],'plots_')+6,12)+'C3'
			endcase
		endif
	endif

endfor


end
