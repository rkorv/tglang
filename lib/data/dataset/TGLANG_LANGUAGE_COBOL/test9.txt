       IDENTIFICATION DIVISION.
       PROGRAM-ID. BUSQUEDATARIFA.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
        SELECT TARIFAS        ASSIGN TO DISK
                              ORGANIZATION IS INDEXED
                              ACCESS MODE IS SEQUENTIAL
                              RECORD KEY TAR-SVD
                              FILE STATUS IS FS-TAR.
       DATA DIVISION.
       FILE SECTION.
       FD TARIFAS     LABEL RECORD IS STANDARD
                      VALUE OF FILE-ID IS "TARind2.DAT".
       01 REG-TARIFAS.
          03 TAR-SVD.
              05 TAR-SRT PIC X(2).
              05 TAR-VIG-DES PIC 9(8).
          03 TAR-TARIFA        PIC 9(5)V99.
       WORKING-STORAGE SECTION.
       01 FS-TAR PIC XX.
           88 OK-TAR VALUE '00'.
           88 NO-TAR VALUE '23'.
           88 EOF-TAR VALUE '10'.
       01 TARIFA-ANT.
           03 ANT-SRT PIC X(2).
           03 ANT-VIG-DES PIC 9(8).
           03 ANT-TARIFA   PIC 9(5)V99.

       LINKAGE SECTION.
       01 CATEGORIA-SRT PIC X(2).
       01 REG-RELEASE-TIM-FECHA PIC 9(8).
       01 REG-RELEASE-TIM-HORAS PIC 9(2)V99.
       01 REG-RELEASE-IMPORTE PIC 9(7)V99.
       PROCEDURE DIVISION USING CATEGORIA-SRT,REG-RELEASE-TIM-FECHA
       ,REG-RELEASE-TIM-HORAS,REG-RELEASE-IMPORTE.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       MAIN-PROCEDURE.
      **
      * The main procedure of the program
      **
            DISPLAY "BUSQ TAR".
            OPEN INPUT TARIFAS.
           PERFORM LEER-TARIFAS UNTIL TAR-SRT EQUAL CATEGORIA-SRT.
           PERFORM UNTIL TAR-VIG-DES > REG-RELEASE-TIM-FECHA
             OR TAR-SRT <> CATEGORIA-SRT OR EOF-TAR
             MOVE REG-TARIFAS TO TARIFA-ANT
             PERFORM LEER-TARIFAS
           END-PERFORM.
           COMPUTE REG-RELEASE-IMPORTE = REG-RELEASE-TIM-HORAS
           * ANT-TARIFA.
           CLOSE TARIFAS.
      ** add other procedures here
       LEER-TARIFAS.
         READ TARIFAS RECORD.
       END PROGRAM BUSQUEDATARIFA.
