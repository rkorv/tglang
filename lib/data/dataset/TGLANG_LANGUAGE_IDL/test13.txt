PRO cafe_setplot, env, item, panel, quiet=quiet, report=report, $
                  help=help, shorthelp=shorthelp
;+
; NAME:
;           setplot
;
; PURPOSE:
;           Change common plot appearance
;
; CATEGORY:
;           cafe
;
; SYNTAX:
;           setplot [, plotparam[=value]][,panel]
;
; INPUTS:
;           plotparam- The plot parameter to change. This may be any
;                      IDL plot option which will be applied to all
;                      plot styles defined. Some also will apply to
;                      different commands, e.g. contour.
;
;                      Some plot styles (and commands) define
;                      additional plot parameters to control the plot
;                      appearance, e.g. the plot style "data" adds a
;                      "noerror" flag which inhibits the plotting of
;                      the error bars. 
;                      
;                      Care must be taken for:
;                        - X/YRANGE (computed explicitely)
;                        - NOERASE  (is used to allow several panel plot)
;                        - POSITION (is used to plot at defined positions)
;
;                      If no plot parameter is given the current
;                      settings are reported. 
;                        
;            value   - The value to set. This may be a number, a
;                      string (need not be enclosed in "") or a vector
;                      in brackets ([a,b,c]).
;                       
;                      Former settings of values will be overridden. 
;
;                      If the value is an empty string the entry will
;                      be deleted.  (e.g. setplot,title="" deletes the
;                      title entry). 
;                      If no value is given ("="  must be omitted) an existing
;                      parameter is removed from the setplot list. If
;                      for missing values the parameter is not defined
;                      it will be set at 1.This allows
;                      simple settings of flags:
;                      Example: setplot, noerror
;                               -> equals setplot,noerror=1 provided
;                               the setting "noerror" was still not
;                               defined.  
;                      
;            panel   - Defines for which panel to set the value. If
;                      not defined the value applies to all panels.
;
; OPTIONS:
;            /quiet  - Do not update plot when setting is finished. 
;            /report - Report setting performed (usefull for log file).
;
; SETPLOT KEYWORDS:
;
;           All IDL plot keywords can be used. Some reasonable
;           keywords are: 
;            - xlog=1, ylog=1 : plot logarithmically
;            - ynozero=1      : do not extend y axis to 0
;            - xtitle, ytitle : Text of x/y axis
;            - title          : Text above plot
;
; SIDE EFFECTS:
;           Changes environment in respect of plot appearance.
;
; EXAMPLE:
;
;             > setplot, xtitle=time
;              -> x axis title will show the word "time" for all panels.
;
; HISTORY:
;           $Id: cafe_setplot.pro,v 1.12 2003/04/24 09:51:01 goehler Exp $
;-
;
; $Log: cafe_setplot.pro,v $
; Revision 1.12  2003/04/24 09:51:01  goehler
; added option /report in which case the setting will be saved in log file
; (via cafereport procedure).
;
; Revision 1.11  2003/04/03 10:02:41  goehler
; /quiet option not to plot
;
; Revision 1.10  2003/04/03 07:53:23  goehler
; silent plot
;
; Revision 1.9  2003/03/20 17:20:05  goehler
; update of plot when setplot performed
;
; Revision 1.8  2003/03/17 14:11:35  goehler
; review/documentation updated.
;
; Revision 1.7  2003/03/03 11:18:26  goehler
; major change: environment struct has become a pointer -> support of wplot/command line
; in common.
; Branch to be able to maintain the former line also.
;
; Revision 1.6  2002/09/09 17:36:11  goehler
; public version: updated help matching aitlib html structure.
; common version: 3.0
;
;
;

    ;; command name of this source (needed for automatic help)
    name="setplot"

    ;; ------------------------------------------------------------
    ;; HELP
    ;; ------------------------------------------------------------
    ;; if help given -> print the specification above (from this file)
    IF keyword_set(help) THEN BEGIN
        cafe_help,env, name
        return
    ENDIF 

  ;; ------------------------------------------------------------
  ;; SHORT HELP
  ;; ------------------------------------------------------------
  IF keyword_set(shorthelp) THEN BEGIN  
    cafereport,env, "setplot  - change plot appearence"
    return
  ENDIF


  ;; no item given -> exit
  IF n_elements(item) EQ 0 THEN return



  ;; ------------------------------------------------------------
  ;; STORE ITEM
  ;; ------------------------------------------------------------

  ;; set item value for given panels, if top item defined
  IF n_elements(item) NE 0 THEN BEGIN 
      IF n_elements(panel) NE 0 THEN  BEGIN 
          cafesetplotparam,env,item, panel

      ;; no panel specified -> all panels
      ENDIF ELSE BEGIN 
          FOR i = 0,n_elements((*env).plot.panels)-1 DO  cafesetplotparam,env,item, i
      ENDELSE  

      ;; update plot:
      IF NOT keyword_set(quiet) THEN $
        cafe_plot,env,/quiet

      ;; report setting:
      IF keyword_set(report) THEN BEGIN 
          IF n_elements(panel) NE 0 THEN  $
            cafereport, env, "setplot,"+item+","+string(panel,format="(I0)"),$
                       /nocomment,/silent $
          ELSE                            $
            cafereport, env, "setplot,"+item,/nocomment,/silent
      ENDIF 
  ENDIF 



  RETURN  
END

