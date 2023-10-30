      $set sourceformat(free)
       IDENTIFICATION DIVISION.
       PROGRAM-ID. mainentry.
*     * ========================================================
*     * entry points:
*     *  main entry    connection to database
*     *  do_connect    connect to database
*     *  do_disconnect disconnect from database
*     *  do_rollback   rollbacks database
*     *  do_commit     commits database 
*     *  dbm_init:     init uwa and currencies
*     *  dbm_clean:    close cursors and clean cursor info
*     * ========================================================
       DATA DIVISION.
*     *
*     * ========================================================
*     *
       WORKING-STORAGE SECTION.
       77  VERS-NB PIC X(80) value
          "@(#) VERSION: 1.1 Mar 25 2010: DB Access functions\".
*     *
       copy "mtdata".
       01 wcc-prog          pic x(80).
       01 prog-ret-code     pic s9(4) comp-5 value zero.
       01 mwlogin.
          02 mwlogin-len pic S9(4) comp-5.
          02 mwlogin-arr pic x(127).
      
       PROCEDURE DIVISION.
       MAIN-ENTRY section.
       DEBUT.
           if MT-CTX-DB-USE = "Y"
               display "mw_trace DBConn"
               call "mw_trace" using "DBConn"
               go to FIN
           end-if.
           if MT-CTX-DB-USE = "N"
*     * ORACLE database isn't used
               display "mw_trace DBNotConn"
               call "mw_trace" using "DBNotConn"
               go to FIN
           end-if.
       FIN.
          exit program.
*     *
       LOGDB SECTION.
       entry "mainentry".
       STRT-DO-CONNECT.
	DISPLAY "OK"
          exit program returning prog-ret-code.

