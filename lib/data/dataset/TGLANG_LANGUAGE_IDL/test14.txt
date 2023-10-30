	PRO GET_TV_SCALE, SX0, SY0, MX0, MY0, JX0, JY0, DT, DISABLE=DISABLE
;+
; Project     : SOHO - CDS
;
; Name        : 
;	GET_TV_SCALE
; Purpose     : 
;	Retrieves information about displayed images.
; Explanation : 
;	Retrieves information about images displayed by EXPTV, PUT, and other
;	routines, as stored by STORE_TV_SCALE.
; Use         : 
;	GET_TV_SCALE, SX, SY, MX, MY, JX, JY  [, DATA ]
; Inputs      : 
;	None.
; Opt. Inputs : 
;	None.
; Outputs     : 
;	SX, SY	= Image size, in data pixels
;	MX, MY	= Image size, in screen pixels
;	JX, JY	= Position of lower left-hand corner of displayed
;			  image, in screen pixels.
; Opt. Outputs: 
;	DATA	= Structure variable containing the parameters needed to
;		  convert pixel coordinates into data coordinates.
; Keywords    : 
;	DISABLE  = If set, then TVSELECT not used.
; Calls       : 
;	TVSELECT, TVUNSELECT
; Common      : 
;	TV_SCALE contains the passed parameters as a function of graphics
;	device, window, and SETIMAGE settings.
;
;	IMAGE_AREA contains switch IMAGE_SET and position IX, NX, IY, NY, from
;	SETIMAGE.
;
; Restrictions: 
;	In general, the SERTS image display routines use several non-standard
;	system variables.  These system variables are defined in the procedure
;	IMAGELIB.  It is suggested that the command IMAGELIB be placed in the
;	user's IDL_STARTUP file.
;
;	Some routines also require the SERTS graphics devices software,
;	generally found in a parallel directory at the site where this software
;	was obtained.  Those routines have their own special system variables.
;
; Side effects: 
;	None.
; Category    : 
;	Utilities, Image_display.
; Prev. Hist. : 
;	William Thompson, May 1992.
; Written     : 
;	William Thompson, GSFC, May 1992.
; Modified    : 
;	Version 1, William Thompson, GSFC, 13 May 1993.
;		Incorporated into CDS library.
;       Version 2, Zarro, GSFC, 17 Feb 1997, Added /CONT to MESSAGE
; Version     : 
;	Version 2
;-
;
	ON_ERROR,2
	COMMON TV_SCALE, NAME,WINDOW,IX,NX,IY,NY,SX,SY,MX,MY,JX,JY,DATA
	COMMON IMAGE_AREA, IMAGE_SET, IX0, NX0, IY0, NY0
;
;  Check the number of parameters.
;
	IF N_PARAMS() LT 6 THEN BEGIN
          MESSAGE,'Syntax:  GET_TV_SCALE, SX, SY, MX, MY, JX, JY  [, DATA]',/CONT
          RETURN
        ENDIF
;
;  Make sure that the common block parameters are defined.
;
	IF N_ELEMENTS(IMAGE_SET)*N_ELEMENTS(NAME) EQ 0 THEN BEGIN
         MESSAGE,'No information for current device/window and SETIMAGE settings',/CONT
         RETURN
        ENDIF
;
;  Select the image display device or window.
;
	TVSELECT, DISABLE=DISABLE
;
;  Search for the current settings in the database.
;
	W = WHERE((NAME EQ !D.NAME) AND (WINDOW EQ !D.WINDOW) AND (IX EQ IX0) $
		AND (NX EQ NX0) AND (IY EQ IY0) AND (NY EQ NY0), N_FOUND)
;
;  Unselect the image display device or window.
;
	TVUNSELECT, DISABLE=DISABLE
;
;  If not found, then return an error message.
;
	IF N_FOUND EQ 0 THEN BEGIN
         MESSAGE,'No information for current device/window and SETIMAGE settings',/CONT
         RETURN
        ENDIF
;
;  Otherwise, extract the data from the appropriate place in the common block
;  arrays.
;
	W = W(0)
	SX0	= SX(W)
	SY0	= SY(W)
	MX0	= MX(W)
	MY0	= MY(W)
	JX0	= JX(W)
	JY0	= JY(W)
	DT	= DATA(W)
;
	RETURN
	END
