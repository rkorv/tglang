;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
; display_status - display a message in the status display
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

; last modified: 28-Feb-2001

pro display_status, message

@euv_imtool-commons

widget_control, statw, set_value=message

end
