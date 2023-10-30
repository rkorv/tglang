;-------------------------------------------------------------
;+
; NAME:
;       EVENT_LOG
; PURPOSE:
;       Enter an event into the latest event log file.
; CATEGORY:
; CALLING SEQUENCE:
;       event_log, txt
; INPUTS:
;       txt = Short text string to enter into event log.   in
; KEYWORD PARAMETERS:
;       Keywords:
;         /TWOLINE  Use two lines: time and txt (def=one line).
;         /ADD means add given text to entry for last time tag.
;            Any number of additional lines may be added.
;         /SCREEN means also display given text on terminal screen.
;         /LIST means display current event log.
;         /FILE means display log file name.
;         /NEW  means start a new event log.
;         SETFILE=file  Optionally specified event file name.
;         DIRECTORY=dir  Event log directory (def=current).
;         /DIFFERENCE gives time difference between last two entries.
;         /LOG Enter the time difference in log file (with /DIFF).
;         TAG=tag  Look for the first occurance of TAG in the last
;           line of the log file.  Return the matching word in VALUE.
;         VALUE=val First word in last log file line containing TAG.
;           Example: if last log line is:
;              DK processing complete: dk_191_1.res
;           and TAG='dk_' then VALUE returns 'dk_191_1.res'
;           TAG could also have been '.res' with same results.
; OUTPUTS:
; COMMON BLOCKS:
; NOTES:
;       Notes: To have an event entered into the latest event
;         log just call with the desired event text.  If an event
;         log file does not exist one will be created.
;         To start a new event file just use the keyword /NEW.
;         The event file names are always of the form:
;           yymmmdd_hhmm.event_log like 95May15_1242.event_log
; MODIFICATION HISTORY:
;       R. Sterner, 1995 May 15
;       R. Sterner, 1995 Jul 10 --- Added /DIFFERENCE keyword.
;       R. Sterner, 1995 Aug  7 --- Added SETFILE keyword.
;
; Copyright (C) 1995, Johns Hopkins University/Applied Physics Laboratory
; This software may be used, copied, or redistributed as long as it is not
; sold and this copyright notice is reproduced on each copy made.  This
; routine is provided as is without any express or implied warranties
; whatsoever.  Other limitations apply as described in the file disclaimer.txt.
;-
;-------------------------------------------------------------
	pro event_log_new, dir=dir, setfile=set
 
	tm = systime()
	js = dt_tm_tojs(tm)
	file = dt_tm_fromjs(js,form='y$n$0d$_h$m$.event_log')
	if n_elements(set) ne 0 then file=set+'.event_log'
	name = filename(dir,file,/nosym)
	openw,lun,name,/get_lun
	printf,lun,'Event log started '+tm
	close, lun
	free_lun, lun
 
	return
	end
 
;-------  event_log.pro = Enter an event into the latest event log file  -----
 
	pro event_log, text, new=new, list=list, file=lfile, screen=screen, $
	  directory=dir, twoline=twoline, difference=diff, log=log, $
	  tag=tag, value=value, setfile=set, add=add, help=hlp
 
	if keyword_set(hlp) then begin
help:	  print,' Enter an event into the latest event log file.'
	  print,' event_log, txt'
	  print,'   txt = Short text string to enter into event log.   in'
	  print,' Keywords:'
	  print,'   /TWOLINE  Use two lines: time and txt (def=one line).'
	  print,'   /ADD means add given text to entry for last time tag.'
	  print,'      Any number of additional lines may be added.'
	  print,'   /SCREEN means also display given text on terminal screen.'
	  print,'   /LIST means display current event log.'
	  print,'   /FILE means display log file name.'
	  print,'   /NEW  means start a new event log.'
	  print,'   SETFILE=file  Optionally specified event file name.'
	  print,'   DIRECTORY=dir  Event log directory (def=current).'
	  print,'   /DIFFERENCE gives time difference between last two entries.'
	  print,'   /LOG Enter the time difference in log file (with /DIFF).'
	  print,'   TAG=tag  Look for the first occurance of TAG in the last'
	  print,'     line of the log file.  Return the matching word in VALUE.'
	  print,'   VALUE=val First word in last log file line containing TAG.'
	  print,'     Example: if last log line is:'
	  print,'        DK processing complete: dk_191_1.res'
	  print,"     and TAG='dk_' then VALUE returns 'dk_191_1.res'"
	  print,"     TAG could also have been '.res' with same results."
	  print,' Notes: To have an event entered into the latest event'
	  print,'   log just call with the desired event text.  If an event'
	  print,'   log file does not exist one will be created.'
	  print,'   To start a new event file just use the keyword /NEW.'
	  print,'   The event file names are always of the form:'
	  print,'     yymmmdd_hhmm.event_log like 95May15_1242.event_log'
	  return
	endif
 
	time = systime()	; Get current time.
 
	if n_elements(dir) eq 0 then cd, curr=dir
 
	;-----  New log requested  -----------------
	if keyword_set(new) then event_log_new, dir=dir, setfile=set
 
	;------  Find latest event log file  -------
	if n_elements(set) gt 0 then begin	; Given event file name.
	  file = set+'.event_log'
	endif else begin			; Find event file name.
	  wild = filename(dir,'*.event_log',/nosym)
	  f = findfile(wild,count=nf)	; List of all *.event_log files.
	  if nf eq 0 then begin
	    event_log_new, dir=dir
	    f = findfile(wild,count=nf)
	  endif
	  ff = strarr(nf)
	  for i=0,nf-1 do begin
	    filebreak,f(i),name=tmp
	    ff(i) = tmp
	  endfor
	  yr = strmid(ff,0,2)			; Deal with 2 digit year.
	  yr2 = '20'+yr				; Assume 20xx.
	  w = where((yr+0) gt 50, cnt)		; Find 19xx.
	  if cnt gt 0 then yr2(w)='19'+yr(w)	; Fix 19xx.
	  tm = yr2+' '+strmid(ff,2,3)+' '+strmid(ff,5,2)+' '+$	; Form date.
	       strmid(ff,8,2)+':'+strmid(ff,10,2)
	  js = dt_tm_tojs(tm)			; Convert dates to JS.
	  w = where(js eq max(js))		; Find latest file.
	  file = f(w(0))			; Get its name.
	endelse
 
	;-------  Display log file name  --------
	if keyword_set(lfile) then print,' Event log file: '+file
 
	;-------  Add new log entry (if text given) -----------
	if n_elements(text) ne 0 then begin
	  if keyword_set(screen) then print,' '+text  ; Display text on screen.
	  openu,lun,file,/append,/get_lun	; Open log file.
	  if keyword_set(add) then begin	; Add a line (no time tag).
	    printf,lun,'  '+text		;   Write added entry.
	  endif else begin			; Normal 1 or 2 line log entry.
	    if keyword_set(twoline) then begin		; Two line format.
	      printf,lun,time				;   Write time.
	      printf,lun,'  '+text			;   Write entry.
	    endif else begin				; One line format.
	      printf,lun,time+' --- '+text		;   Write time & entry.
	    endelse
	  endelse
	  close, lun
	  free_lun, lun
	endif
 
	;------  List  ----------
	if keyword_set(list) then begin
	  txt = getfile(file)
	  more,txt
	endif
 
	;------  Difference  ----------
	if keyword_set(diff) then begin
	  txt = getfile(file)
	  one = strmid(txt,0,1)
	  w = where(one ne ' ', cnt)
	  if cnt eq 0 then return
	  txt = txt(w)
	  n = n_elements(txt)
	  t1 = dt_tm_tojs(strmid(txt(n-2),0,24))
	  t2 = dt_tm_tojs(strmid(txt(n-1),0,24))
	  d = long(t2-t1)
	  s = strtrim(d,2)
	  m = strtrim(string(d/60.,form='(G13.4)'),2)
	  h = strtrim(string(d/3600.,form='(G13.4)'),2)
	  dy = strtrim(string(d/86400.,form='(G13.6)'),2)
	  print,' Time difference between last two entries:'
	  print,' '+s+' seconds = '+m+' minutes = '+$
	    h+' hours = '+dy+' days.' 
	  if keyword_set(log) then begin
	    openu,lun,file,/append,/get_lun		; Open log file.
	    printf,lun,' Time difference between last two entries:'
	    printf,lun,' '+s+' seconds = '+m+' minutes = '+$
	      h+' hours = '+dy+' days.' 
	    free_lun, lun
	  endif
	endif
 
	;------  TAG/VALUE  ----------
	if n_elements(tag) then begin
	  txt = getfile(file)
	  txt = txt(n_elements(txt)-1)	; Last line.
	  wordarray,txt,ww
	  w=where(strpos(ww,tag) ge 0, cnt)
	  if cnt eq 0 then value='' else value=ww(w(0))
	endif
 
	return
	end
