REPORT demo_db_writer.

CLASS demo DEFINITION.
  PUBLIC SECTION.
    CLASS-METHODS:  class_constructor,
                    main.
  PRIVATE SECTION.
    TYPES:
      pict_line TYPE x LENGTH 1022,
      pict_tab  TYPE STANDARD TABLE OF pict_line WITH EMPTY KEY.
    CLASS-DATA:
      name TYPE c LENGTH 255
           VALUE '/SAP/PUBLIC/BC/ABAP/mime_demo/ABAP_Docu_Logo.gif',
      pict TYPE pict_tab.
    CLASS-METHODS get_pict_tab
     IMPORTING
       mime_url TYPE csequence
     EXPORTING
       pict_tab TYPE pict_tab.
ENDCLASS.

CLASS demo IMPLEMENTATION.
  METHOD main.

    DATA wa TYPE demo_blob_table WRITER FOR COLUMNS picture.

    cl_demo_input=>request( CHANGING field = demo=>name ).

    TRY.
        wa-name = name.
        INSERT demo_blob_table FROM @wa.
        IF sy-subrc = 4.
          DATA(subrc) = sy-subrc.
        ELSE.

          DATA(stmnt) = wa-picture->get_statement_handle( ).
          LOOP AT pict INTO DATA(xline).
            wa-picture->write( CONV #( xline ) ).
          ENDLOOP.
          wa-picture->close( ).

          IF stmnt->get_db_count( ) <> 1.
            subrc = 4.
          ENDIF.

        ENDIF.
      CATCH cx_stream_io_exception cx_close_resource_error.
        subrc = 4.
    ENDTRY.

    IF subrc = 0.
      cl_demo_output=>display(
        'One line inserted, you can run DEMO_DB_READER now' ).
    ELSE.
      cl_demo_output=>display(
        'Error during insertion' ).
    ENDIF.

  ENDMETHOD.
  METHOD class_constructor.
    get_pict_tab(
     EXPORTING
       mime_url = name
     IMPORTING
       pict_tab = pict ).
    DELETE FROM demo_blob_table WHERE name = @name.
  ENDMETHOD.
  METHOD get_pict_tab.
    cl_mime_repository_api=>get_api( )->get(
      EXPORTING i_url = mime_url
      IMPORTING e_content = DATA(pict_wa)
      EXCEPTIONS OTHERS = 4 ).
    IF sy-subrc = 4.
      RETURN.
    ENDIF.
    pict_tab =
      VALUE #( LET l1 = xstrlen( pict_wa ) l2 = l1 - 1022 IN
               FOR j = 0 THEN j + 1022  UNTIL j >= l1
                 ( COND #( WHEN j <= l2 THEN
                                pict_wa+j(1022)
                           ELSE pict_wa+j ) ) ).
  ENDMETHOD.
ENDCLASS.


START-OF-SELECTION.
  demo=>main( ).
