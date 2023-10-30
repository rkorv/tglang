* LABEL STATEMENT is in the data step;
DATA QUEST;
input ID        $ 1-3
      AGE         4-5
      GENDER    $   6
      RACE      $   7
      MARITAL   $   8
      EDUCATION $   9
      PRESIDENT    10
      ARMS         11
      CITIES       12;
LABEL MARITAL      ="Marital Status"
      EDUCATION    ="Education Level"
      PRESIDENT    ="President Doing a Good Job"
      ARMS         ="Arms Budget Increase"
      CITIES       ="Federal Aid to Cities";
DATALINES;
001091111232
002452222422
003351324442
004271111121
005682132333
006651243425
;
PROC MEANS DATA=QUEST MAXDEC=2 N MEAN STD CLM;
TITLE "Questionnaire Analysis";
VAR AGE;
RUN:
PROC FREQ DATA=QUEST;
TITLE "Frequency Counts for categorical Variables";
TABLES GENDER RACE MARITAL EDUCATION PRESIDENT ARMS CITIES;
RUN;
