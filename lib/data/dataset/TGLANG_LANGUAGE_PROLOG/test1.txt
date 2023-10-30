

pro SDIControl_Cleanup, id

	common SDIControl

	widget_control, get_uval = uval, id

	if size(uval, /type) eq 8 then begin
		descr = uval.descr
		case descr of
			'plugin_base': begin
				;\\ Remove closed plugins from the timer/frame event lists
				if size(*sdic_misc.timer_list, /n_dimensions) ne 0 then begin
					tidxs = where(*sdic_misc.timer_list eq uval.object, ntimer)
					if ntimer gt 0 then *sdic_misc.timer_list = delete_elements(*sdic_misc.timer_list, tidxs)
				endif
				if size(*sdic_misc.frame_list, /n_dimensions) ne 0 then begin
					fidxs = where(*sdic_misc.frame_list eq uval.object, nframe)
					if nframe gt 0 then *sdic_misc.frame_list = delete_elements(*sdic_misc.frame_list, fidxs)
				endif
				obj_destroy, uval.object
			end

			'root_base': begin
				print, obj_valid()
			end

			else:
		endcase
	endif

end