       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       REPOSITORY.
           FUNCTION ALL INTRINSIC.
       INPUT-OUTPUT SECTION.

       FILE-CONTROL.
           SELECT IN-FILE ASSIGN TO '/home/nosferatu/workspace/gnucobol-
      -                             'playground/fixed_record_file.txt'
               ORGANIZATION IS LINE SEQUENTIAL
               ACCESS MODE IS SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  IN-FILE.
       01  IN-RECORD.
           05  F-RID                          PIC 9(06).
           05  F-FIRST-NM                     PIC X(16).
           05  F-LAST-NM                      PIC X(18).
           05  F-SSN                          PIC 9(09).
           05  F-REG-TS.
               10  F-REG-YYYY                 PIC 9(04).
               10  FILLER                     PIC X(01).
               10  F-REG-MM                   PIC 9(02).
               10  FILLER                     PIC X(01).
               10  F-REG-DD                   PIC 9(02).
               10  FILLER                     PIC X(01).
               10  F-REG-HH                   PIC 9(02).
               10  FILLER                     PIC X(01).
               10  F-REG-MIN                  PIC 9(02).
               10  FILLER                     PIC X(01).
               10  F-REG-SS                   PIC 9(02).
               10  FILLER                     PIC X(01).
               10  F-REG-MS                   PIC 9(06).

       WORKING-STORAGE SECTION.

           COPY FILEDEF.

       01  W02-SW-EOF                         PIC X(01) VALUE 'N'.
           88  END-OF-FILE                    VALUE 'Y'.
           88  NOT-END-OF-FILE                VALUE 'N'.

       PROCEDURE DIVISION.

       0000-MAINLINE.
           DISPLAY "HELLO".

           OPEN INPUT IN-FILE.
           PERFORM 0100-READ-FILE THRU 0100-READ-FILE-EXIT
               UNTIL END-OF-FILE.
           CLOSE IN-FILE.

           SET NOT-END-OF-FILE TO TRUE.

       0000-MAINLINE-EXIT. EXIT.
       STOP RUN.

       0100-READ-FILE.
           READ IN-FILE NEXT RECORD
               INTO W01-RECORD WITH NO LOCK
                   AT END SET END-OF-FILE TO TRUE
                   NOT AT END DISPLAY W01-RECORD
           END-READ.
       0100-READ-FILE-EXIT. EXIT.
