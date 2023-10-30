FUNCTION demo_update_insert.
*"----------------------------------------------------------------------
*"*"Verbuchungsfunktionsbaustein:
*"
*"*"Lokale Schnittstelle:
*"  IMPORTING
*"     VALUE(VALUES) TYPE  DEMO_UPDATE_TAB
*"----------------------------------------------------------------------

  INSERT demo_update FROM TABLE values.

ENDFUNCTION.
