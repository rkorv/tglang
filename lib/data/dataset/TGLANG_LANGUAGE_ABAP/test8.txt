CLASS ycl_advent2020_day09 DEFINITION
  PUBLIC
  FINAL
  CREATE PUBLIC.

  PUBLIC SECTION.
    TYPES:
      BEGIN OF ty_result,
        number TYPE int8,
        index  TYPE i,
      END OF ty_result.

    METHODS solve_part_one
      IMPORTING
        input         TYPE string_table
        preamble_len  TYPE i
      RETURNING
        VALUE(result) TYPE ty_result.

    METHODS solve_part_two
      IMPORTING
        input         TYPE string_table
        preamble_len  TYPE i
      RETURNING
        VALUE(result) TYPE int8.

  PROTECTED SECTION.
  PRIVATE SECTION.
    DATA preamble TYPE STANDARD TABLE OF int8 WITH EMPTY KEY.
    DATA faulty TYPE ty_result.
    DATA tab TYPE STANDARD TABLE OF int8 WITH EMPTY KEY.

    METHODS is_valid
      IMPORTING
        elem          TYPE int8
      RETURNING
        VALUE(result) TYPE abap_bool.

    METHODS find_sequence
      RETURNING
        VALUE(result) TYPE int8.

    METHODS sequence
      IMPORTING
        start_index   TYPE i
      RETURNING
        VALUE(result) TYPE int8.
ENDCLASS.



CLASS YCL_ADVENT2020_DAY09 IMPLEMENTATION.


  METHOD find_sequence.
    LOOP AT tab ASSIGNING FIELD-SYMBOL(<t>).
      DATA(index) = sy-tabix.
      result = sequence( index ).
      IF result IS NOT INITIAL.
        RETURN.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.


  METHOD is_valid.
    DATA(check) = preamble.
    DELETE check WHERE table_line > elem.
    IF line_exists( check[ table_line = elem ] ).
      result = abap_true.
      RETURN.
    ENDIF.

    LOOP AT check ASSIGNING FIELD-SYMBOL(<c>).
      IF line_exists( check[ table_line = elem - <c> ] ).
        result = abap_true.
        RETURN.
      ENDIF.
    ENDLOOP.

    result = abap_false.
  ENDMETHOD.


  METHOD sequence.
    DATA(sum) = 0.
    DATA(min) = tab[ start_index ].
    DATA(max) = min.

    LOOP AT tab ASSIGNING FIELD-SYMBOL(<t>) FROM start_index TO faulty-index - 1 .
      ADD <t> TO sum.
      IF <t> < min.
        min = <t>.
      ENDIF.
      IF <t> > max.
        max = <t>.
      ENDIF.
      IF sum = faulty-number.
        result = min + max.
        RETURN.
      ELSEIF sum > faulty-number.
        RETURN.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.


  METHOD solve_part_one.
    LOOP AT input ASSIGNING FIELD-SYMBOL(<i>).
      IF sy-tabix > preamble_len.
        IF NOT is_valid( CONV #( <i> ) ).
          result-number = <i>.
          result-index = sy-tabix.
          RETURN.
        ENDIF.
        DELETE preamble INDEX 1.
      ENDIF.
      APPEND <i> TO preamble.
    ENDLOOP.
  ENDMETHOD.


  METHOD solve_part_two.
    faulty = solve_part_one( input = input preamble_len = preamble_len ).
    tab = input.
    result = find_sequence(  ).
  ENDMETHOD.
ENDCLASS.
