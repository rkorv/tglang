*&---------------------------------------------------------------------*
*& Report ZABO_ABAP2XLSX_BUG_977
*&---------------------------------------------------------------------*
*& Author: Sandra Rossi
*& Source: https://github.com/abap2xlsx/abap2xlsx/issues/977#issuecomment-1023340193
*&---------------------------------------------------------------------*
REPORT zabo_abap2xlsx_bug_977.

DATA: gc_save_file_name TYPE string VALUE 'test.xlsx'.
INCLUDE zdemo_excel_outputopt_incl.

START-OF-SELECTION.
  TRY.
      DATA(lo_excel) = NEW zcl_excel( ).
      DATA(lo_worksheet) = lo_excel->get_active_worksheet( ).
      lo_worksheet->set_cell( ip_column = 'A' ip_row = 1 ip_value = CONV int8( 33400000000 ) ).
      lcl_output=>output( cl_excel = lo_excel ).
    CATCH cx_root INTO DATA(lx_root).
      MESSAGE lx_root TYPE 'I' DISPLAY LIKE 'E'.
  ENDTRY.
