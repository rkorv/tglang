;+
; NAME:
;     TVIMAGE
;
; PURPOSE:
;     This purpose of TVIMAGE is to allow you to display an image
;     on the display or in a PostScript file in a particular position.
;     The position is specified by means of the POSITION keyword. In
;     this respect, TVIMAGE works like other IDL graphics commands.
;     Moreover, the TVIMAGE command works identically on the display
;     and in a PostScript file. You don't have to worry about how to
;     "size" the image in PostScript. The output on your display and
;     in the PostScript file will be identical. The major advantage of
;     TVIMAGE is that it can be used in a natural way with other IDL
;     graphics commands in resizeable IDL graphics windows. TVIMAGE
;     is a replacement for TV and assumes the image has been scaled
;     correctly when it is passed as an argument.
;
; AUTHOR:
;       FANNING SOFTWARE CONSULTING:
;       David Fanning, Ph.D.
;       2642 Bradbury Court
;       Fort Collins, CO 80521 USA
;       Phone: 970-221-0438
;       E-mail: davidf@dfanning.com
;       Coyote's Guide to IDL Programming: http://www.dfanning.com
;
; CATEGORY:
;     Graphics display.
;
; CALLING SEQUENCE:
;
;     TVIMAGE, image
;
; INPUTS:
;     image:    A 2D or 3D image array. It should be byte data.
;
;       x  :    The X position of the lower-left corner of the image.
;               This parameter is only recognized if the TV keyword is set.
;
;       y  :    The Y position of the lower-left corner of the image.
;               This parameter is only recognized if the TV keyword is set.
;
; KEYWORD PARAMETERS:
;     ERASE:    If this keyword is set an ERASE command is issued
;               before the image is displayed. Note that the ERASE
;               command puts the image on a new page in PostScript
;               output.
;
;     _EXTRA:   This keyword picks up any TV keywords you wish to use.
;
;     KEEP_ASPECT_RATIO: Normally, the image will be resized to fit the
;               specified position in the window. If you prefer, you can
;               force the image to maintain its aspect ratio in the window
;               (although not its natural size) by setting this keyword.
;               The image width is fitted first. If, after setting the
;               image width, the image height is too big for the window,
;               then the image height is fitted into the window. The
;               appropriate values of the POSITION keyword are honored
;               during this fitting process. Once a fit is made, the
;               POSITION coordiates are re-calculated to center the image
;               in the window. You can recover these new position coordinates
;               as the output from the POSITION keyword.
;
;     MARGIN:   A single value, expressed as a normalized coordinate, that
;               can easily be used to calculate a position in the window.
;               The margin is used to calculate a POSITION that gives
;               the image an equal margin around the edge of the window.
;               The margin must be a number in the range 0.0 to 0.333. This
;               keyword is ignored if the POSITION keyword is used.
;
;     MINUS_ONE: The value of this keyword is passed along to the CONGRID
;               command. It prevents CONGRID from adding an extra row and
;               column to the resulting array, which can be a problem with
;               small image arrays.
;
;     MULTI:    If this keyword is set, the image output honors the
;               !P.MULTI system variable.
;
;     NORMAL:   Setting this keyword means image position coordinates x and y
;               are interpreted as being in normalized coordinates. This keyword
;               is only valid if the TV keyword is set.
;
;     POSITION: The location of the image in the output window. This is
;               a four-element floating array of normalized coordinates of
;               the type given by !P.POSITION or the POSITION keyword to
;               other IDL graphics commands. The form is [x0, y0, x1, y1].
;               The default is [0.0, 0.0, 1.0, 1.0]. Note that this can
;               be an output parameter if the KEEP_ASPECT_RATIO keyword is
;               used.
;
;     TV:       Setting this keyword makes the TVIMAGE command work much
;               like the TV command, although better. That is to say, it
;               will still set the correct DECOMPOSED state depending upon
;               the kind of image to be displayed (8-bit or 24-bit). It will
;               also allow the image to be "positioned" in the window by
;               specifying the coordinates of the lower-left corner of the
;               image. The NORMAL keyword is activated when the TV keyword
;               is set, which will indicate that the position coordinates
;               are given in normalized coordinates rather than device
;               coordinates.
;
;               Setting this keyword will ensure that the keywords
;               KEEP_ASPECT_RATIO, MARGIN, MINUS_ONE, MULTI, and POSITION
;               are ignored.
;
; OUTPUTS:
;     None.
;
; SIDE EFFECTS:
;     Unless the KEEP_ASPECT_RATIO keyword is set, the displayed image
;     may not have the same aspect ratio as the input data set.
;
; RESTRICTIONS:
;     If the POSITION keyword and the KEEP_ASPECT_RATIO keyword are
;     used together, there is an excellent chance the POSITION
;     parameters will change. If the POSITION is passed in as a
;     variable, the new positions will be returned as an output parameter.
;
;     If the image is 2D then color decomposition is turned OFF
;     for the current graphics device (i.e., DEVICE, DECOMPOSED=0).
;
;     If outputting to the PRINTER device, the aspect ratio of the image
;     is always maintained and the POSITION coordinates are ignored.
;     The image always printed in portrait mode.
;
; EXAMPLE:
;     To display an image with a contour plot on top of it, type:
;
;        filename = FILEPATH(SUBDIR=['examples','data'], 'worldelv.dat')
;        image = BYTARR(360,360)
;        OPENR, lun, filename, /GET_LUN
;        READU, image
;        FREE_LUN, lun
;
;        TVIMAGE, image, POSITION=thisPosition, /KEEP_ASPECT_RATIO
;        CONTOUR, image, POSITION=thisPosition, /NOERASE, XSTYLE=1, $
;            YSTYLE=1, XRANGE=[0,360], YRANGE=[0,360], NLEVELS=10
;
; MODIFICATION HISTORY:
;      Written by:     David Fanning, 20 NOV 1996.
;      Fixed a small bug with the resizing of the image. 17 Feb 1997. DWF.
;      Removed BOTTOM and NCOLORS keywords. This reflects my growing belief
;         that this program should act more like TV and less like a "color
;         aware" application. I leave "color awareness" to the program
;         using TVIMAGE. Added 24-bit image capability. 15 April 1997. DWF.
;      Fixed a small bug that prevented this program from working in the
;          Z-buffer. 17 April 1997. DWF.
;      Fixed a subtle bug that caused me to think I was going crazy!
;          Lession learned: Be sure you know the *current* graphics
;          window! 17 April 1997. DWF.
;      Added support for the PRINTER device. 25 June 1997. DWF.
;      Extensive modifications. 27 Oct 1997. DWF
;          1) Removed PRINTER support, which didn't work as expected.
;          2) Modified Keep_Aspect_Ratio code to work with POSITION keyword.
;          3) Added check for window-able devices (!D.Flags AND 256).
;          4) Modified PostScript color handling.
;      Craig Markwart points out that Congrid adds an extra row and column
;          onto an array. When viewing small images (e.g., 20x20) this can be
;          a problem. Added a Minus_One keyword whose value can be passed
;          along to the Congrid keyword of the same name. 28 Oct 1997. DWF
;      Changed default POSITION to fill entire window. 30 July 1998. DWF.
;      Made sure color decomposition is OFF for 2D images. 6 Aug 1998. DWF.
;      Added limited PRINTER portrait mode support. The correct aspect ratio
;          of the image is always maintained when outputting to the
;          PRINTER device and POSITION coordinates are ignored. 6 Aug 1998. DWF
;      Removed 6 August 98 fixes (Device, Decomposed=0) after realizing that
;          they interfere with operation in the Z-graphics buffer. 9 Oct 1998. DWF
;      Added a MARGIN keyword. 18 Oct 1998. DWF.
;      Re-established Device, Decomposed=0 keyword for devices that
;         support it. 18 Oct 1998. DWF.
;      Added support for the !P.Multi system variable. 3 March 99. DWF
;      Added DEVICE, DECOMPOSED=1 command for all 24-bit images. 2 April 99. DWF.
;      Added ability to preserve DECOMPOSED state for IDL 5.2 and higher. 4 April 99. DWF.
;      Added TV keyword to allow TVIMAGE to work like the TV command. 11 May 99. DWF.
;-

PRO TVIMAGE, image, x, y, KEEP_ASPECT_RATIO=keep, POSITION=position, $
   MARGIN=margin, MINUS_ONE=minusOne, _EXTRA=extra, ERASE=eraseit, $
   MULTI=multi, TV=tv, NORMAL=normal

ON_ERROR, 1

   ; Check for image parameter.


IF N_Elements(image) EQ 0 THEN MESSAGE, 'You must pass a valid image argument.'

   ; Check image size.

s = SIZE(image)
IF s(0) LT 2 OR s(0) GT 3 THEN $
   MESSAGE, 'Argument does not appear to be an image. Returning...'

   ; Which release of IDL is this?

thisRelease = Float(!Version.Release)

   ; 2D image.

IF s(0) EQ 2 THEN BEGIN
   imgXsize = FLOAT(s(1))
   imgYsize = FLOAT(s(2))
   true = 0

        ; Decomposed color off if device supports it.

   CASE  StrUpCase(!D.NAME) OF
        'X': BEGIN
            IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
            Device, Decomposed=0
            ENDCASE
        'WIN': BEGIN
            IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
            Device, Decomposed=0
            ENDCASE
        'MAC': BEGIN
            IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
            Device, Decomposed=0
            ENDCASE
        ELSE:
   ENDCASE
ENDIF

   ; 3D image.

IF s(0) EQ 3 THEN BEGIN
IF (s(1) NE 3L) AND (s(2) NE 3L) AND (s(3) NE 3L) THEN $
   MESSAGE, 'Argument does not appear to be a 24-bit image. Returning...'
   IF s(1) EQ 3 THEN true = 1 ; Pixel interleaved
   IF s(2) EQ 3 THEN true = 2 ; Row interleaved
   IF s(3) EQ 3 THEN true = 3 ; Band interleaved

        ; Decomposed color on if device supports it.


   CASE StrUpCase(!D.NAME) OF
        'X': BEGIN
            Device, Get_Visual_Depth=thisDepth
            IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
            IF thisDepth GT 8 THEN Device, Decomposed=1
            ENDCASE
        'WIN': BEGIN
            Device, Get_Visual_Depth=thisDepth
            IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
            IF thisDepth GT 8 THEN Device, Decomposed=1
            ENDCASE
        'MAC': BEGIN
            Device, Get_Visual_Depth=thisDepth
            IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
            IF thisDepth GT 8 THEN Device, Decomposed=1
            ENDCASE
        ELSE:
   ENDCASE
   CASE true OF
      1: BEGIN
         imgXsize = FLOAT(s(2))
         imgYsize = FLOAT(s(3))
         END
      2: BEGIN
         imgXsize = FLOAT(s(1))
         imgYsize = FLOAT(s(3))
         END
      3: BEGIN
         imgXsize = FLOAT(s(1))
         imgYsize = FLOAT(s(2))
         END
   ENDCASE
ENDIF

   ; Check for TV keyword. If present, then act like a TV command.

IF Keyword_Set(tv) THEN BEGIN
   IF Keyword_Set(eraseit) THEN Erase
   IF N_Elements(x) EQ 0 THEN x = 0
   IF N_Elements(y) EQ 0 THEN y = 0
   IF Keyword_Set(normal) THEN TV, image, x, y, True=true, _Extra=extra, /Normal ELSE $
                               TV, image, x, y, True=true, _Extra=extra, /Device
   GoTo, restoreDecomposed
ENDIF

   ; Check for keywords.

IF N_ELEMENTS(position) EQ 0 THEN BEGIN
   IF Keyword_Set(multi) THEN BEGIN
      Plot, Findgen(11), XStyle=4, YStyle=4, /NoData
      position = [!X.Window[0], !Y.Window[0], !X.Window[1], !Y.Window[1]]
   ENDIF ELSE BEGIN
      position = [0.0, 0.0, 1.0, 1.0]
   ENDELSE
ENDIF ELSE BEGIN
   IF Keyword_Set(multi) THEN BEGIN
      Plot, Findgen(11), XStyle=4, YStyle=4, /NoData
      position = [!X.Window[0], !Y.Window[0], !X.Window[1], !Y.Window[1]]
   ENDIF ELSE BEGIN
      position = Float(position)
   ENDELSE
ENDELSE


IF N_Elements(margin) NE 0 THEN BEGIN
        margin = 0.0 > margin < 0.33
        position = [position[0] + margin, position[1] + margin, $
                    position[2] - margin, position[3] - margin]
ENDIF

minusOne = Keyword_Set(minusOne)
IF Keyword_Set(eraseit) THEN Erase

   ; Maintain aspect ratio (ratio of height to width)?

IF KEYWORD_SET(keep) THEN BEGIN

      ; Find aspect ratio of image.

   ratio = FLOAT(imgYsize) / imgXSize

      ; Find the proposed size of the image in pixels without aspect
      ; considerations.

   xpixSize = (position(2) - position(0)) * !D.X_VSize
   ypixSize = (position(3) - position(1)) * !D.Y_VSize

      ; Try to fit the image width. If you can't maintain
      ; the aspect ratio, fit the image height.

   trialX = xpixSize
   trialY = trialX * ratio
   IF trialY GT ypixSize THEN BEGIN
      trialY = ypixSize
      trialX = trialY / ratio
   ENDIF

      ; Recalculate the position of the image in the window.

   position(0) = (((xpixSize - trialX) / 2.0) / !D.X_VSize) + position(0)
   position(2) = position(0) + (trialX/FLOAT(!D.X_VSize))
   position(1) = (((ypixSize - trialY) / 2.0) / !D.Y_VSize)  + position(1)
   position(3) = position(1) + (trialY/FLOAT(!D.Y_VSize))

ENDIF

   ; Calculate the image size and start locations.

xsize = (position(2) - position(0)) * !D.X_VSIZE
ysize = (position(3) - position(1)) * !D.Y_VSIZE
xstart = position(0) * !D.X_VSIZE
ystart = position(1) * !D.Y_VSIZE

   ; Display the image. Sizing different for PS device.

IF (!D.NAME EQ 'PS') THEN BEGIN

      ; Need a gray-scale color table if this is a true
      ; color image.

   IF true GT 0 THEN LOADCT, 0, /Silent
   TV, image, xstart, ystart, XSIZE=xsize, $
      YSIZE=ysize, _EXTRA=extra, True=true

ENDIF ELSE $

IF (!D.NAME EQ 'PRINTER') THEN BEGIN

      ; Reset the PRINTER for proper calculations.

   Device, Scale_Factor=1, Portrait=1

      ; Get the sizes of the PRINTER device.

   pxsize = !D.X_Size
   pysize = !D.Y_Size

      ; Calculate a scale factor for the printer.

   scalefactor = 1.0 / ((Float(imgXsize)/pxsize) > (Float(imgYsize)/pysize))
   xoffset = Fix((Float(pxsize)/scalefactor - imgXsize)/2.0)
   yoffset = Fix((Float(pysize)/scalefactor - imgYsize)/2.0)

      ; Print it.

   Device, Portrait=1, Scale_Factor=scalefactor
   TV, image, xoffset, yoffset, /Device, True=true
   Device, /Close_Document

ENDIF ELSE BEGIN ; All other devices.
   CASE true OF
      0: TV, CONGRID(image, CEIL(xsize), CEIL(ysize), /INTERP, $
            MINUS_ONE=minusOne), xstart, ystart, _EXTRA=extra
      1: TV, CONGRID(image, 3, CEIL(xsize), CEIL(ysize), /INTERP, $
            MINUS_ONE=minusOne), xstart, ystart, _EXTRA=extra, True=1
      2: TV, CONGRID(image, CEIL(xsize), 3, CEIL(ysize), /INTERP, $
            MINUS_ONE=minusOne), xstart, ystart, _EXTRA=extra, True=2
      3: TV, CONGRID(image, CEIL(xsize), CEIL(ysize), 3, /INTERP, $
            MINUS_ONE=minusOne), xstart, ystart, _EXTRA=extra, True=3
  ENDCASE
ENDELSE

   ; Restore Decomposed state if necessary.

RestoreDecomposed:

CASE StrUpCase(!D.NAME) OF
   'X': BEGIN
      IF thisRelease GE 5.2 THEN Device, Decomposed=thisDecomposed
      ENDCASE
   'WIN': BEGIN
      IF thisRelease GE 5.2 THEN Device, Decomposed=thisDecomposed
      ENDCASE
   'MAC': BEGIN
      IF thisRelease GE 5.2 THEN Device, Decomposed=thisDecomposed
      ENDCASE
   ELSE:
ENDCASE

END