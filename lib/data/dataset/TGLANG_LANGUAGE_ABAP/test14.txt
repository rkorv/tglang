class ZCL_BOPF_UI_NODE definition
  public
  final
  create public

  global friends ZCL_EUI_EVENT_CALLER .

public section.

  methods CONSTRUCTOR
    importing
      !IV_BOPF_NAME type CSEQUENCE
      !IV_TECH type ABAP_BOOL optional
      !IV_NODE type /BOBF/OBM_NODE_KEY optional
    raising
      /BOBF/CX_FRW .
  methods SHOW_ALV
    importing
      !IR_TABLE type ref to DATA
    returning
      value(RV_CMD) type SYUCOMM
    raising
      /BOBF/CX_FRW .
  methods SHOW_SELECTION_SCREEN
    returning
      value(RR_TABLE) type ref to DATA
    raising
      /BOBF/CX_FRW .
protected section.
private section.

  types:
    BEGIN OF ts_copy_map,
      src  TYPE string,
      dest TYPE string,
    END OF ts_copy_map .
  types:
    BEGIN OF ts_bo_info,
      bo_name          TYPE string,
      bind_attribute   TYPE /bobf/obm_assocb-attribute,
      copy_map         TYPE STANDARD TABLE OF ts_copy_map WITH DEFAULT KEY,
    END OF ts_bo_info .
  types:
    BEGIN OF ts_assoc,
      _name             TYPE /bobf/obm_assoc-name,
      _assoc_key        TYPE /bobf/obm_assoc-assoc_key,
      _assoc_type       TYPE /bobf/obm_assoc-assoc_type,
      _assoc_cat        TYPE /bobf/obm_assoc-assoc_cat,
      _assoc_name       TYPE /bobf/obm_assoc-assoc_name,
      _assoc_class      TYPE /bobf/obm_assoc-assoc_class,
      _attr_name_source TYPE /bobf/obm_assoc-attr_name_source,
      _assoc_resolve    TYPE /bobf/obm_assoc-assoc_resolve,
      _target_node_key  TYPE /bobf/obm_assoc-target_node_key,
      _param_data_type  TYPE /bobf/obm_assoc-param_data_type,
      _cardinality      TYPE /bobf/obm_assoc-cardinality,
      _seckeyname       TYPE /bobf/obm_assoc-seckeyname,
      _change_resolve   TYPE /bobf/obm_assoc-change_resolve,
      desc              TYPE /bobf/obm_assoct-description,
      count             TYPE count_kk,
      _bo               TYPE ts_bo_info,
    END OF ts_assoc .
  types:
    BEGIN OF ts_create_info,
      assoc_key         TYPE /bobf/s_frw_modification-association,
      source_key        TYPE /bobf/s_frw_modification-source_key,
      source_node       TYPE /bobf/s_frw_modification-source_node,
      target_node       TYPE /bobf/obm_node_key,
    END OF ts_create_info .
  types:
    BEGIN OF ts_table_ext,
      T_LOGS        TYPE zcl_eui_logger=>tt_msg,
      V_LOG_ICON    TYPE ICON_D,
      T_CELL_STYLES TYPE LVC_T_STYL,
      T_CELL_COLORS TYPE LVC_T_SCOL,
      V_ASSOC_ICON  TYPE ICON_D,
    END OF ts_table_ext .

  constants:
    BEGIN OF MC_CMD,
     save     TYPE syucomm VALUE 'SAVE',
     pick_one TYPE syucomm VALUE 'PICK_ONE',
     create   TYPE syucomm VALUE 'CREATE',
     delete   TYPE syucomm VALUE 'DELETE',
   END OF MC_CMD .
  data MO_MANAGER type ref to ZCL_BOPF_MANAGER .
  data MO_METADATA type ref to ZCL_BOPF_METADATA .
  data MO_ACTION type ref to LCL_ACTION .
  data MO_ASSOC type ref to LCL_ASSOC .
  data MO_TAB_INFO type ref to LCL_TAB_INFO .
  data MV_NODE type /BOBF/OBM_NODE_KEY .
  data MV_NODE_NAME type STRING .
  data MS_CREATE_INFO type TS_CREATE_INFO .
  data MO_PARENT type ref to ZCL_BOPF_UI_NODE .
  data MS_ASSOC type TS_ASSOC .
  data MV_EDIT_MODE type /BOBF/CONF_EDIT_MODE .
  data MV_TECH type ABAP_BOOL .
  data MT_SELECTED_ROW_NO type LVC_T_ROID .

  methods _GET_TITLE
    returning
      value(RV_TITLE) type STRING .
  methods _EXECUTE_CHECK_EXIT
    importing
      !IO_GRID type ref to CL_GUI_ALV_GRID
    changing
      !CV_CLOSE type ABAP_BOOL .
  methods _EXECUTE_SAVE .
  methods _EXECUTE_CREATE
    importing
      !IO_GRID type ref to CL_GUI_ALV_GRID .
  methods _EXECUTE_DELETE
    importing
      !IO_GRID type ref to CL_GUI_ALV_GRID .
  methods _GET_NODE_INFO
    exporting
      !ER_DATA_TABLE type ref to DATA
      !ER_DATA type ref to DATA
      !ET_CATALOG type LVC_T_FCAT .
  methods _GET_CONTROL
    exporting
      !EO_MANAGER type ref to ZCL_BOPF_MANAGER
      !EO_METADATA type ref to ZCL_BOPF_METADATA
      !EV_ACT_NODE type /BOBF/OBM_NODE_KEY .
  methods _ON_HOTSPOT_CLICK   ##RELAX
    for event HOTSPOT_CLICK of CL_GUI_ALV_GRID
    importing
      !SENDER
      !E_ROW_ID
      !E_COLUMN_ID .
  methods _ON_PBO_EVENT   ##RELAX
    for event PBO_EVENT of ZIF_EUI_MANAGER
    importing
      !SENDER .
  methods _ON_PAI_EVENT   ##RELAX
    for event PAI_EVENT of ZIF_EUI_MANAGER
    importing
      !SENDER
      !IV_COMMAND
      !CV_CLOSE .
  methods _ON_TOOLBAR   ##RELAX
    for event TOOLBAR of CL_GUI_ALV_GRID
    importing
      !SENDER
      !E_OBJECT .
  methods _ON_USER_COMMAND   ##RELAX
    for event USER_COMMAND of CL_GUI_ALV_GRID
    importing
      !SENDER
      !E_UCOMM .
  methods _ON_DATA_CHANGED_FINISHED   ##RELAX
    for event DATA_CHANGED_FINISHED of CL_GUI_ALV_GRID
    importing
      !SENDER
      !ET_GOOD_CELLS .
  methods _ON_ONF4
    for event ONF4 of CL_GUI_ALV_GRID
    importing
      !E_FIELDNAME
      !ES_ROW_NO
      !ER_EVENT_DATA
      !E_DISPLAY .
  methods _ON_DELAYED_CHANGED_SELECTION
    for event DELAYED_CHANGED_SEL_CALLBACK of CL_GUI_ALV_GRID
    importing
      !SENDER .
  methods _REFRESH_LINE
    importing
      !IR_BOPF_LINE type ref to DATA optional
      !IV_KEY type /BOBF/CONF_KEY optional
      !IO_MESSAGE type ref to /BOBF/IF_FRW_MESSAGE optional
      value(IV_NEW_INDEX) type SYTABIX optional
    changing
      !CS_LINE type ANY optional .
  class-methods _ONE_ITEM_CARDINALITY
    importing
      !IS_ASSOC type TS_ASSOC
    returning
      value(RV_1_ALLOWED) type ABAP_BOOL .
  methods _UPDATE_ROOT_NODE
    importing
      !IO_GRID type ref to CL_GUI_ALV_GRID .
  methods _GET_CHANGE_MESSAGES
    importing
      !IV_SEVERITY type CSEQUENCE optional
      !CV_HAS_CHANGE type ref to ABAP_BOOL optional
    returning
      value(RO_MESSAGES) type ref to ZCL_BOPF_MESSAGES .
ENDCLASS.



CLASS ZCL_BOPF_UI_NODE IMPLEMENTATION.


METHOD constructor.
  mo_manager    = zcl_bopf_manager=>create( iv_bopf_name = iv_bopf_name
                                            iv_log       = iv_tech ).
  mo_metadata   = mo_manager->mo_metadata.

  mv_tech       = iv_tech.
  mv_node       = COND #( WHEN iv_node IS NOT INITIAL THEN iv_node
                          ELSE mo_metadata->mv_root_node ).
  SELECT SINGLE description INTO mv_node_name
  FROM /bobf/obm_nodet
  WHERE langu    = sy-langu
    AND name     = iv_bopf_name
    AND node_key = mv_node
    AND bo_key   = mo_metadata->mv_bo_key.

  IF sy-subrc <> 0.
    zcx_eui_no_check=>raise_sys_error( iv_message = |Check parameters: { sy-langu }, { iv_bopf_name }, { mv_node }, { mo_metadata->mv_bo_key }| ).
  ENDIF.

  mo_assoc    = NEW #( me ).
  mo_tab_info = NEW #( me ).
  mo_action   = NEW #( me ).
  mo_tab_info->make_table( mo_assoc ).
ENDMETHOD.


METHOD show_alv.
  " add_batch( ir_table ).
  FIELD-SYMBOLS: <lt_src>  TYPE ANY TABLE.
  ASSIGN ir_table->* TO <lt_src>.
  LOOP AT <lt_src> ASSIGNING FIELD-SYMBOL(<ls_src>).
    _refresh_line( ir_bopf_line = REF #( <ls_src> )
                   iv_new_index = 0 ).
  ENDLOOP.
**********************************************************************

  _get_node_info( IMPORTING et_catalog = DATA(lt_catalog) ).
  DATA(lv_nbsp_title) = repeat( val = cl_abap_conv_in_ce=>uccp( '00A0' )  occ = 5 ).
  INSERT VALUE #( fieldname = 'V_LOG_ICON'
                  col_pos   = 1
                  coltext   = lv_nbsp_title
                  hotspot   = abap_true )
                  INTO lt_catalog INDEX 1.
  INSERT VALUE #( fieldname = 'V_ASSOC_ICON'
                  col_pos   = 1
                  coltext   = lv_nbsp_title
                  hotspot   = abap_true
                  tech      = COND #( WHEN mo_assoc->mt_assoc IS INITIAL THEN abap_true ) )
                  INTO lt_catalog INDEX 2.

  DATA(lo_alv) = NEW zcl_eui_alv(
     ir_table       = mo_tab_info->mr_table
     it_mod_catalog = lt_catalog
     is_layout      = VALUE lvc_s_layo( grid_title = mv_node_name
                                        smalltitle = abap_true
                                        stylefname = 'T_CELL_STYLES'
                                        ctab_fname = 'T_CELL_COLORS'
                                        no_rowins  = 'X' ) ).

  DATA(ls_status) = VALUE zif_eui_manager=>ts_status( title = _get_title( ) ).
  IF mo_parent IS INITIAL.
    ls_status-prog = 'Z_BOPF_TEST_UI'.
    ls_status-name = 'EDIT_STATUS'.
  ELSE.
    lo_alv->popup( iv_row_end = 21 ).
    IF mo_tab_info->is_editable( ) = abap_true.
      IF _one_item_cardinality( ms_assoc ) = abap_true.
        ls_status-prog = 'Z_BOPF_TEST_UI'.
        ls_status-name = 'PICK_BO_STATUS'.
      ENDIF.
      ls_status-exclude[] = VALUE #( ( zif_eui_manager=>mc_cmd-cancel ) ).
    ENDIF.
  ENDIF.

  rv_cmd = lo_alv->set_status( ls_status )->show( io_handler = me ).
ENDMETHOD.


METHOD show_selection_screen.
  DATA(lo_screen) = lcl_dynamic_screen=>create_node_based( me ).

  DATA(lt_pbo) = VALUE zcl_eui_screen=>tt_customize(
    ( name     = 'V_MAX_ROW'                                "#EC NOTEXT
      required = '1'
      label    = 'Maximum row count'(mrc) )
    ( name     = 'V_EDIT_MODE'                              "#EC NOTEXT
     required = '1' ) ).

  _get_node_info( IMPORTING et_catalog = DATA(lt_catalog) ).
  LOOP AT lt_catalog ASSIGNING FIELD-SYMBOL(<ls_catalog>) WHERE domname = '/BOBF/CONF_KEY'.
    IF <ls_catalog>-coltext(1) = '*'.
      CHECK <ls_catalog>-coltext = '*KEY' AND mv_tech = abap_true.
    ENDIF.

    APPEND VALUE #( name  = <ls_catalog>-fieldname
                    label = <ls_catalog>-coltext ) TO lt_pbo[].
  ENDLOOP.

  lo_screen->show(
    EXPORTING it_pbo     = lt_pbo
    IMPORTING ev_cancel  = DATA(lv_cancel) ).
  CHECK lv_cancel <> abap_true.

  lo_screen->get_node_screen_info(
    EXPORTING io_owner     = me
    IMPORTING ev_edit_mode = mv_edit_mode
              ev_max_row   = DATA(lv_max_row)
              et_sel_param = DATA(lt_sel_param) ).
  lcl_dynamic_screen=>set_default_edit_mode( mv_edit_mode ).

  DATA(lt_key) = mo_manager->query_tab(
     it_sel_param     = lt_sel_param
     is_query_options = VALUE #( maximum_rows = lv_max_row ) ).

  rr_table = mo_manager->retrieve_tab(
    it_key       = lt_key
    iv_edit_mode = mv_edit_mode ).
ENDMETHOD.


METHOD _execute_check_exit.
  " popup for sub nodes
  DO 1 TIMES.
    CHECK mo_parent IS NOT INITIAL.

    FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
    DATA(lr_alv_table) = zcl_eui_conv=>get_grid_table( io_grid ).
    ASSIGN lr_alv_table->* TO <lt_table>.

    READ TABLE <lt_table> WITH KEY ('v_log_icon') = icon_protocol "#EC CI_ANYSEQ
      TRANSPORTING NO FIELDS.
    IF sy-subrc = 0.
      cv_close = abap_false.
      MESSAGE 'Please fix warnings'(fix) TYPE 'S' DISPLAY LIKE 'E'.
    ENDIF.

    RETURN.
  ENDDO.

  DATA(lv_has_change) = NEW abap_bool( ).
  DATA(lo_messages) = NEW zcl_bopf_messages( iv_severity = 'AXE' ).
  LOOP AT zcl_bopf_manager=>mt_all_managers ASSIGNING FIELD-SYMBOL(<ls_cache>).
    lo_messages->add_from_manager(
      io_manager    = <ls_cache>-manager
      cv_has_change = lv_has_change ).
  ENDLOOP.
  CHECK lv_has_change->* = abap_true.

  DATA(lv_choice) = zcl_eui_screen=>confirm(
    iv_title          = 'Confirmation'(cnf)
    iv_question       = 'Save data before exit?'(sdb)
    iv_icon_1         = 'ICON_SYSTEM_SAVE'
    iv_icon_2         = 'ICON_SYSTEM_END'
    iv_text_2         = 'Discards all changes'(dis)
    iv_display_cancel = abap_true ).

  CASE lv_choice.
    WHEN abap_true.
      IF lo_messages->mt_logs[] IS NOT INITIAL.
        cv_close = abap_false.
      ENDIF.
      zcl_eui_screen=>top_pai( mc_cmd-save ).

    WHEN abap_false. " Exit without saving data
      cv_close = abap_true.

    WHEN abap_undefined. " Cancel
      cv_close = abap_false.
  ENDCASE.
ENDMETHOD.


METHOD _execute_create.
  " cardinality_is_ok ?
  FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
  DATA(lr_alv_table) = zcl_eui_conv=>get_grid_table( io_grid ).
  ASSIGN lr_alv_table->* TO <lt_table>.

  IF lines( <lt_table> ) > 0 AND _one_item_cardinality( ms_assoc ) = abap_true.
    MESSAGE 'Only 1 item allowed'(on1) TYPE 'S' DISPLAY LIKE 'E'.
    RETURN.
  ENDIF.

  _get_control( IMPORTING eo_manager  = DATA(lo_manager)
                          eo_metadata = DATA(lo_metadata)
                          ev_act_node = DATA(lv_act_node) ).
  lo_metadata->get_node(
   EXPORTING iv_node_type  = lv_act_node
   IMPORTING es_node       = DATA(ls_node)
             er_data       = DATA(lr_line)
             er_data_table = DATA(lr_table) ).

  FIELD-SYMBOLS <lt_node> TYPE INDEX TABLE.
  ASSIGN lr_line->*  TO FIELD-SYMBOL(<ls_node>).
  ASSIGN lr_table->* TO <lt_node>.

  ASSIGN COMPONENT 'KEY' OF STRUCTURE <ls_node> TO FIELD-SYMBOL(<lv_key>) CASTING TYPE /bobf/conf_key.
  <lv_key> = /bobf/cl_frw_factory=>get_new_key( ).

  INSERT <ls_node> INTO TABLE <lt_node>.

  " TODO  Lo_metadata OR Mo_metadata ???
  DATA(ls_create_info) = COND #( WHEN lv_act_node <> Lo_metadata->mv_root_node " ms_create_info-_info-_assoc_cat <> /bobf/if_conf_c=>sc_assoccat_xbo.
                                 THEN ms_create_info ).
  lo_manager->mo_service->retrieve_default_node_values(
        EXPORTING iv_node_key   = lv_act_node
                  iv_assoc_key  = ls_create_info-assoc_key
                  iv_source_key = ls_create_info-source_key
        CHANGING  ct_data      = <lt_node> ).
  READ TABLE <lt_node> INTO <ls_node> INDEX 1.

  " fill the modify container
  DATA(ls_modification)  = VALUE /bobf/s_frw_modification(
   key         = <lv_key>
   change_mode = /bobf/if_frw_c=>sc_modify_create
   node        = lv_act_node
   data        = REF #( <ls_node> ) ).

  IF ls_create_info IS NOT INITIAL.
    ls_modification-association = ls_create_info-assoc_key.
    ls_modification-source_key  = ls_create_info-source_key.
    ls_modification-source_node = ls_create_info-source_node.
  ENDIF.

  TRY.
      lo_manager->modify(
          EXPORTING it_modification = VALUE #( ( ls_modification ) )
          IMPORTING eo_change       = DATA(lo_change)
                    eo_message      = DATA(lo_message) ).

      " check, if the instance has been created successfully
      lo_change->get_bo_changes(
        EXPORTING iv_bo_key = lo_metadata->mv_bo_key
        IMPORTING eo_change = DATA(lo_frw_change) ).

      IF lo_frw_change IS NOT INITIAL.
        lo_frw_change->get_changes(
          EXPORTING iv_change_mode  = /bobf/if_frw_c=>sc_modify_create
                    iv_failed       = abap_false
                    iv_node_key     = lv_act_node
          IMPORTING et_changed_key  = DATA(lt_created_key) ).
      ENDIF.

      IF lt_created_key IS INITIAL OR lo_frw_change IS INITIAL.
        DATA(lv_message) = |{ 'Create: Creation failed, no instance has been created'(crf) }|.
        DATA(lv_msgty)   = 'E'.
      ELSE.
        lv_message = 'Create: Instance has been successfully created'(cro).
        lv_msgty   = 'S'.

        lo_manager->retrieve_tab(
          iv_node_type  = lv_act_node
          it_key        = lt_created_key
          iv_edit_mode  = /bobf/if_conf_c=>sc_edit_exclusive " just lock
          iv_fill_data  = abap_false ).
      ENDIF.

      " refresh grid data (necessary, due to determination, which are triggered on create and change some attribute data)
      _refresh_line( iv_key       = <lv_key>
                     io_message   = lo_message
                     iv_new_index = 1 ).
    CATCH /bobf/cx_frw INTO DATA(lo_error).
      MESSAGE lo_error TYPE 'S' DISPLAY LIKE 'E'.
      RETURN.
  ENDTRY.

  lcl_tab_info=>refresh_grid( io_grid    = io_grid
                              iv_message = lv_message
                              iv_msgty   = lv_msgty  ).
ENDMETHOD.


METHOD _execute_delete.
  io_grid->get_selected_rows( IMPORTING et_row_no = DATA(lt_row_no) ).
  IF lt_row_no[] IS INITIAL.
    MESSAGE 'Nothing selected'(nsl) TYPE 'S' DISPLAY LIKE 'W'.
    RETURN.
  ENDIF.

  CHECK zcl_eui_screen=>confirm(
   iv_title    = 'Warning'
   iv_question = |Delete { lines( lt_row_no ) } items?| ) = abap_true.

  FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
  DATA(lr_alv_table) = zcl_eui_conv=>get_grid_table( io_grid ).
  ASSIGN lr_alv_table->* TO <lt_table>.

  _get_control( IMPORTING eo_manager  = DATA(lo_manager)
                          ev_act_node = DATA(lv_act_node) ).

  DATA(lv_del_count) = 0.
  DATA(lv_message)   = ||.
  DATA(lv_msgty)     = 'S'.
  " Delete from the bottom
  SORT lt_row_no BY row_id DESCENDING.
  LOOP AT lt_row_no ASSIGNING FIELD-SYMBOL(<ls_row_no>).
    ASSIGN <lt_table>[ <ls_row_no>-row_id ] TO FIELD-SYMBOL(<ls_line>).
    CHECK sy-subrc = 0.
    ASSIGN COMPONENT 'KEY' OF STRUCTURE <ls_line> TO FIELD-SYMBOL(<lv_key>) CASTING TYPE /bobf/conf_key.

    TRY.
        lo_manager->modify(
            EXPORTING it_modification = VALUE #(
                        ( key         = <lv_key>
                          change_mode = /bobf/if_frw_c=>sc_modify_delete
                          node        = lv_act_node ) )
            IMPORTING " eo_change       = DATA(lo_change)
                      eo_message      = DATA(lo_message)
                      ev_ok           = DATA(lv_ok) ).
      CATCH /bobf/cx_frw INTO DATA(lo_error).
        lv_message = lo_error->get_text( ).
        lv_msgty   = 'E'.
        EXIT.
    ENDTRY.

    IF lv_ok <> abap_true.
      _refresh_line( EXPORTING iv_key     = <lv_key>
                               io_message = lo_message
                     CHANGING  cs_line    = <ls_line> ).
      CONTINUE.
    ENDIF.

    DELETE <lt_table> INDEX <ls_row_no>-row_id.
    lv_del_count = lv_del_count + 1.
  ENDLOOP.

  lv_message = |{ lv_message } { lv_del_count } items were deleted|.
  lcl_tab_info=>refresh_grid( io_grid    = io_grid
                              iv_message = lv_message
                              iv_msgty   = lv_msgty ).
ENDMETHOD.


METHOD _execute_save.
  DATA(lo_messages) = _get_change_messages( iv_severity = 'AXE' ).
  IF lo_messages->mt_logs[] IS NOT INITIAL.
    lo_messages->show( ).
    RETURN.
  ENDIF.

  TRY.
      mo_manager->save(
        IMPORTING ev_ok      = DATA(lv_ok)
                  eo_message = DATA(lo_message) ).
    CATCH /bobf/cx_frw INTO DATA(lo_error).
      MESSAGE lo_error TYPE 'S' DISPLAY LIKE 'E'.
      RETURN.
  ENDTRY.

  CHECK NEW zcl_bopf_messages( iv_severity = 'AXE'
          )->add_from_message( lo_message
          )->show( ) <> abap_true.

  CHECK lv_ok = abap_true.
  MESSAGE |'{ mv_node_name }' saved| TYPE 'S'.
ENDMETHOD.


METHOD _get_change_messages.
  ro_messages = NEW #( iv_severity = iv_severity ).
  LOOP AT zcl_bopf_manager=>mt_all_managers ASSIGNING FIELD-SYMBOL(<ls_cache>).
    ro_messages->add_from_manager( io_manager    = <ls_cache>-manager
                                   cv_has_change = cv_has_change ).
  ENDLOOP.
ENDMETHOD.


METHOD _get_control.
  CLEAR eo_manager.
  CLEAR eo_metadata.

  ev_act_node = COND #( WHEN ms_create_info-target_node IS NOT INITIAL
                         AND ms_assoc-_assoc_cat <> /bobf/if_conf_c=>sc_assoccat_xbo
                        THEN ms_create_info-target_node
                        ELSE mv_node ).

  IF mo_manager->mo_service IS NOT INITIAL.
    eo_manager    = mo_manager.
    eo_metadata   = mo_metadata.
  ELSEIF mo_parent IS NOT INITIAL.
    mo_parent->_get_control(
     IMPORTING eo_manager    = eo_manager
               eo_metadata   = eo_metadata ).
  ENDIF.
ENDMETHOD.


METHOD _get_node_info.
  mo_metadata->get_node( EXPORTING iv_node_type  = mv_node
                         IMPORTING er_data_table = er_data_table
                                   er_data       = er_data ).
  et_catalog = zcl_eui_type=>get_catalog( ir_table = er_data_table ).

  SELECT attribute_name, property_name INTO TABLE @DATA(lt_property)
  FROM /bobf/obm_propty
  WHERE name     = @mo_metadata->mv_bopf_name
    AND bo_key   = @mo_metadata->mv_bo_key
    AND node_key = @mv_node
    AND ( property_name = 'R' OR property_name = 'M' )
    AND property_value = @abap_true.

  DATA(lv_index) = 0.
  DATA(lv_editable) = mo_tab_info->is_editable( ).
  LOOP AT et_catalog ASSIGNING FIELD-SYMBOL(<ls_catalog>).
    <ls_catalog>-edit = lv_editable.
    "<ls_catalog>-tech = COND #( WHEN <ls_catalog>-DOMNAME = '/BOBF/CONF_KEY' THEN 'X' ).

    " Previous filedname
    <ls_catalog>-parameter0 = <ls_catalog>-fieldname.

    <ls_catalog>-fieldname = COND #( WHEN <ls_catalog>-fieldname = 'KEY'
                                       OR <ls_catalog>-fieldname = 'PARENT_KEY'
                                       OR <ls_catalog>-fieldname = 'ROOT_KEY'
                                     THEN <ls_catalog>-fieldname ).
    IF <ls_catalog>-fieldname IS NOT INITIAL.
      <ls_catalog>-tech      = xsdbool( mv_tech <> abap_true ).
      <ls_catalog>-coltext   = |*{ <ls_catalog>-parameter0 }|.
      <ls_catalog>-col_pos   = 2.
      <ls_catalog>-edit      = abap_false.
    ELSE.
      lv_index               = lv_index + 1.
      <ls_catalog>-fieldname = |C{ lv_index }|.
    ENDIF.

    IF <ls_catalog>-domname = '/BOBF/CONF_KEY' AND <ls_catalog>-fieldname CP 'C*'.
      <ls_catalog>-coltext = |({ <ls_catalog>-parameter0 })|.
      <ls_catalog>-col_pos = <ls_catalog>-col_pos + lines( et_catalog ).
    ENDIF.

    LOOP AT lt_property ASSIGNING FIELD-SYMBOL(<ls_property>) WHERE attribute_name = <ls_catalog>-parameter0.

      CASE <ls_property>-property_name.
        WHEN 'R'. " READ-ONLY
          <ls_catalog>-edit = abap_false.

        WHEN 'M'. " Mandatory
          <ls_catalog>-parameter1 = abap_true.
          IF lv_editable <> abap_true.
            <ls_catalog>-emphasize = 'C001'.
          ENDIF.
      ENDCASE.
    ENDLOOP.

    READ TABLE ms_assoc-_bo-copy_map TRANSPORTING NO FIELDS
     WITH KEY dest = <ls_catalog>-parameter0.
    IF sy-subrc = 0 AND lv_editable <> abap_true.
      <ls_catalog>-emphasize = 'C101'.
    ENDIF.
  ENDLOOP.

  " Ref to WAERS
  LOOP AT et_catalog ASSIGNING <ls_catalog> WHERE cfieldname IS NOT INITIAL.
    ASSIGN et_catalog[ parameter0 = <ls_catalog>-cfieldname ] TO FIELD-SYMBOL(<ls_ref>).
    CHECK sy-subrc = 0.
    <ls_catalog>-cfieldname = <ls_ref>-fieldname.
  ENDLOOP.
ENDMETHOD.


METHOD _get_title.
  DATA(lt_langu) = VALUE efg_tab_langu( ( sy-langu ) ( 'E' ) ).

  SELECT langu, description INTO TABLE @DATA(lt_objt)
  FROM /bobf/obm_objt
  FOR ALL ENTRIES IN @lt_langu
  WHERE langu EQ @lt_langu-table_line
    AND name  EQ @mo_metadata->mv_bopf_name.

  " 1-st by proirity
  LOOP AT lt_langu INTO DATA(lv_langu).
    ASSIGN lt_objt[ langu = lv_langu ] TO FIELD-SYMBOL(<ls_objt>).
    CHECK sy-subrc = 0.
    rv_title = <ls_objt>-description.
    EXIT.
  ENDLOOP.

  DATA(lv_add_text) = COND string( WHEN mo_tab_info->is_editable( )
                                   THEN 'Edit'(edt)
                                   ELSE 'View'(vew) ).
  rv_title = |{ rv_title } - { lv_add_text }|.
ENDMETHOD.


METHOD _one_item_cardinality.
  CHECK is_assoc-_cardinality = /bobf/if_conf_c=>sc_card_zero_to_one
     OR is_assoc-_cardinality = /bobf/if_conf_c=>sc_card_one.
  rv_1_allowed = abap_true.
ENDMETHOD.


METHOD _on_data_changed_finished.
  " does the user has changed anything at all?
  CHECK et_good_cells IS NOT INITIAL AND et_good_cells IS SUPPLIED.

  " get changed rows out of the et_good_ells
  DATA lt_changed_rows TYPE SORTED TABLE OF sytabix WITH UNIQUE KEY table_line.
  LOOP AT et_good_cells INTO DATA(ls_good_cells).
    INSERT ls_good_cells-row_id INTO TABLE lt_changed_rows.
  ENDLOOP.

  _get_control( IMPORTING eo_manager  = DATA(lo_manager)
                          eo_metadata = DATA(lo_metadata)
                          ev_act_node = DATA(lv_act_node) ).

  " get alv outtab
  FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
  DATA(lr_alv_table) = zcl_eui_conv=>get_grid_table( sender ).
  ASSIGN lr_alv_table->* TO <lt_table>.

  DATA(lv_grid_refresh_needed) = abap_false.
  LOOP AT lt_changed_rows INTO DATA(lv_tabix).
    ASSIGN <lt_table>[ lv_tabix ] TO FIELD-SYMBOL(<ls_line>).
    CHECK sy-subrc = 0.

    " remember the key of the instances, which have been changed directly by the user input
    ASSIGN COMPONENT 'KEY' OF STRUCTURE <ls_line> TO FIELD-SYMBOL(<lv_key>) CASTING TYPE /bobf/conf_key.

    DATA(lr_bopf_row) = mo_tab_info->ui_to_bopf( ir_src        = REF #( <ls_line> )
                                                 it_good_cells = et_good_cells
                                                 ir_refresh    = REF #( lv_grid_refresh_needed ) ).
    TRY.
        " Data before update
        DATA(lr_table) = lo_manager->retrieve_tab(
               iv_node_type = lv_act_node
               iv_edit_mode = /bobf/if_conf_c=>sc_edit_read_only
               it_key       = VALUE #( ( key = <lv_key> ) ) ).
        FIELD-SYMBOLS <lt_table_prev> TYPE INDEX TABLE.
        ASSIGN lr_table->* TO <lt_table_prev>.

        lo_manager->modify(
              EXPORTING it_modification = VALUE #(
                            ( node        = lv_act_node " mv_node
                              change_mode = /bobf/if_frw_c=>sc_modify_update
                              key         = <lv_key>
                              data        = lr_bopf_row ) )
              IMPORTING eo_change       = DATA(lo_change)
                        eo_message      = DATA(lo_message) ).
      CATCH /bobf/cx_frw INTO DATA(lo_error).
        MESSAGE lo_error TYPE 'S' DISPLAY LIKE 'E'.
        RETURN.
    ENDTRY.

    DATA(ls_prev_ext) = CORRESPONDING ts_table_ext( <ls_line> ).
    DATA(ls_new_ext)  = lcl_tab_info=>create_ext_fieds( lo_message ).
    IF ls_prev_ext <> ls_new_ext.
      MOVE-CORRESPONDING ls_new_ext TO <ls_line>.
      lv_grid_refresh_needed = abap_true.
      CONTINUE.
    ENDIF.

    " evaluate changes
    DATA(lt_change) = lo_change->get_changes( ).
    READ TABLE lt_change WITH KEY bo_key = lo_metadata->mv_bo_key INTO DATA(ls_change).
    CHECK sy-subrc = 0.

    " current bo was changed
    ls_change-change_object->get( IMPORTING et_change = DATA(lt_changed_nodes) ).
    READ TABLE lt_changed_nodes WITH KEY key1 COMPONENTS node_key = lv_act_node " mv_node
                                              TRANSPORTING NO FIELDS.
    CHECK sy-subrc = 0.

    " yes, the current change is related to a row, which has been changed by the user
    LOOP AT lt_changed_nodes INTO DATA(ls_changed_node) WHERE key = <lv_key>.
      TRY.
          lr_table = lo_manager->retrieve_tab(
                 iv_node_type = lv_act_node
                 iv_edit_mode = mv_edit_mode
                 it_key       = VALUE #( ( key = ls_changed_node-key ) ) ).
        CATCH /bobf/cx_frw INTO lo_error.
          MESSAGE lo_error TYPE 'S' DISPLAY LIKE 'E'.
          RETURN.
      ENDTRY.

      FIELD-SYMBOLS <lt_data> TYPE INDEX TABLE.
      ASSIGN lr_table->* TO <lt_data>.
      IF <lt_data> IS INITIAL OR lines( <lt_data> ) > 1.
        lv_grid_refresh_needed = abap_true.
      ELSE.
        ASSIGN: <lt_table_prev>[ 1 ] TO FIELD-SYMBOL(<ls_data_prev>),
                <lt_data>[ 1 ]       TO FIELD-SYMBOL(<ls_data>).

        " compare new value <ls_data> with data after users change
        LOOP AT <lt_table> ASSIGNING <ls_line>.
          ASSIGN COMPONENT 'KEY' OF STRUCTURE <ls_line> TO <lv_key>.
          CHECK <lv_key> = ls_changed_node-key.

          DATA(ls_data_user) = mo_tab_info->ui_to_bopf( ir_src = REF #( <ls_line> ) ).
          ASSIGN ls_data_user->* TO FIELD-SYMBOL(<ls_data_user>).

          " compare. refresh needed ?
          CHECK <ls_data_user> NE <ls_data>
             OR <ls_data_user> NE <ls_data_prev>.
          lv_grid_refresh_needed = abap_true.
          EXIT.
        ENDLOOP.
      ENDIF.
    ENDLOOP.
  ENDLOOP.

  CHECK lv_grid_refresh_needed = abap_true.
  lcl_tab_info=>refresh_grid( io_grid    = sender
                              iv_message = 'Data changed'(dch) ).
ENDMETHOD.


METHOD _on_delayed_changed_selection.
  sender->get_selected_rows( IMPORTING et_row_no = mt_selected_row_no ).
  sender->set_toolbar_interactive( ).
ENDMETHOD.


METHOD _on_hotspot_click.
  FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
  DATA(lr_alv_table) = zcl_eui_conv=>get_grid_table( sender ).
  ASSIGN lr_alv_table->* TO <lt_table>.

  ASSIGN <lt_table>[ e_row_id-index ] TO FIELD-SYMBOL(<ls_line>).
  CHECK sy-subrc = 0.

  CASE e_column_id-fieldname.
    WHEN 'V_LOG_ICON'.
      DATA(ls_ext) = CORRESPONDING ts_table_ext( <ls_line> ).
      NEW zcl_bopf_messages(
      )->add_from_table( ls_ext-t_logs[]
      )->show( ).

    WHEN 'V_ASSOC_ICON'.
      mo_assoc->show_all_assoc( is_line = <ls_line>
                                io_grid = sender ).

      lcl_tab_info=>refresh_grid( io_grid    = sender
                                  iv_message = ''
                                  iv_refresh = abap_false ).
  ENDCASE.
ENDMETHOD.


METHOD _on_onf4.
  CHECK er_event_data IS NOT INITIAL.
  " Where write result
  FIELD-SYMBOLS <lt_modi> TYPE lvc_t_modi.
  ASSIGN er_event_data->m_data->* TO <lt_modi>.
  CHECK sy-subrc = 0.

  _get_node_info( IMPORTING et_catalog = DATA(lt_catalog) ).
  ASSIGN lt_catalog[ fieldname = e_fieldname ] TO FIELD-SYMBOL(<ls_catalog>).
  CHECK sy-subrc = 0.

  DATA(ls_shlp) = VALUE shlp_descr( ).
  CALL FUNCTION 'F4IF_DETERMINE_SEARCHHELP'
    EXPORTING
      tabname   = <ls_catalog>-ref_table
      fieldname = <ls_catalog>-ref_field
    IMPORTING
      shlp      = ls_shlp
    EXCEPTIONS
      OTHERS    = 1.
  CHECK sy-subrc = 0.

  " Is there a BO connection?
  LOOP AT mo_assoc->mt_assoc ASSIGNING FIELD-SYMBOL(<ls_assoc>).
    CHECK mo_assoc->is_name_match( iv_name1 = <ls_catalog>-parameter0
                                   iv_name2 = <ls_assoc>-_assoc_name ).
    DATA(ls_bo_info) = mo_assoc->get_bo_info( <ls_assoc> ).
    EXIT.
  ENDLOOP.
  CHECK ls_bo_info IS NOT INITIAL.

  LOOP AT ls_shlp-fieldprop ASSIGNING FIELD-SYMBOL(<ls_prop>) WHERE shlpinput  = abap_true " <-- Passed only 1 key from ALV! Usually is empty
                                                                AND shlpoutput = abap_true
                                                                AND fieldname CP '*KEY'.
    ASSIGN ls_shlp-fielddescr[ fieldname = <ls_prop>-fieldname ] TO FIELD-SYMBOL(<ls_descr>).
    CHECK sy-subrc = 0
      AND <ls_descr>-domname = '/BOBF/CONF_KEY'.

    " Handle by our self
    er_event_data->m_event_handled = abap_true.

    DATA lt_return TYPE STANDARD TABLE OF ddshretval WITH DEFAULT KEY.
    CALL FUNCTION 'F4IF_START_VALUE_REQUEST'
      EXPORTING
        shlp          = ls_shlp
        disponly      = e_display
      TABLES
        return_values = lt_return.
    CHECK lt_return[] IS NOT INITIAL.

    INSERT VALUE #( src  = <ls_descr>-fieldname
                    dest = ls_bo_info-bind_attribute ) INTO ls_bo_info-copy_map INDEX 1.

    LOOP AT lt_return ASSIGNING FIELD-SYMBOL(<ls_return>).
      ASSIGN ls_bo_info-copy_map[ src = <ls_return>-fieldname ] TO FIELD-SYMBOL(<ls_copy_map>).
      CHECK sy-subrc = 0.

      ASSIGN lt_catalog[ parameter0 = <ls_copy_map>-dest ] TO <ls_catalog>.
      CHECK sy-subrc = 0.

      APPEND VALUE #( row_id    = es_row_no-row_id
                      fieldname = <ls_catalog>-fieldname
                      value     = <ls_return>-fieldval ) TO <lt_modi>.
    ENDLOOP.

    RETURN.
  ENDLOOP.
ENDMETHOD.


METHOD _on_pai_event.
  DATA(lo_grid) = CAST zcl_eui_alv( sender )->get_grid( ).

  CASE iv_command.
    WHEN zif_eui_manager=>mc_cmd-cancel OR zif_eui_manager=>mc_cmd-ok.
      _execute_check_exit( EXPORTING io_grid  = lo_grid
                           CHANGING  cv_close = cv_close->* ).

    WHEN mc_cmd-save.
      _execute_save( ).

    WHEN mc_cmd-pick_one.
      _update_root_node( lo_grid ).
      cv_close->* = abap_true.

  ENDCASE.
ENDMETHOD.


METHOD _on_pbo_event.
  DATA(lo_alv)  = CAST zcl_eui_alv( sender ).
  DATA(lo_grid) = lo_alv->get_grid( ).
  IF lo_grid IS NOT INITIAL.
    lo_grid->set_toolbar_interactive( ).
  ENDIF.

  DATA(lr_has_change) = NEW abap_bool( ).
  _get_change_messages( cv_has_change = lr_has_change ).
  lo_alv->ms_status-exclude = COND #( WHEN lr_has_change->* <> abap_true
                                      THEN VALUE #( ( 'SAVE' ) ) ).
ENDMETHOD.


METHOD _on_toolbar.
  TYPES tr_ui_func TYPE RANGE OF ui_func.
  DATA(lr_ok_buttons) = VALUE tr_ui_func( sign = 'I' option = 'EQ'
   ( low = cl_gui_alv_grid=>mc_fc_sort_asc   )
   ( low = cl_gui_alv_grid=>mc_fc_sort_dsc   )
   ( low = cl_gui_alv_grid=>mc_fc_find       )
   ( low = cl_gui_alv_grid=>mc_fc_find_more  )
   ( low = cl_gui_alv_grid=>mc_mb_filter     )
   ( low = '&&SEP04'     )
   ( low = cl_gui_alv_grid=>mc_mb_sum        )
   ( low = cl_gui_alv_grid=>mc_mb_subtot     )
   ( low = '&&SEP05'     )
   ( low = cl_gui_alv_grid=>mc_fc_print_back )
   ( low = cl_gui_alv_grid=>mc_mb_view       )
   ( low = cl_gui_alv_grid=>mc_mb_export     )
   ( low = cl_gui_alv_grid=>mc_mb_variant    )
   ( low = '&&SEP06'     ) ).
  DELETE e_object->mt_toolbar[] WHERE function NOT IN lr_ok_buttons.

  DATA(lv_ins_disabled) = xsdbool( mo_tab_info->is_editable( ) <> abap_true ).
  INSERT VALUE #(
     function = mc_cmd-create
     icon     = icon_insert_row
     disabled = lv_ins_disabled
     text     = 'Add item'(ani) ) INTO TABLE e_object->mt_toolbar.

  DATA(lv_del_disabled) = COND #( WHEN lv_ins_disabled = abap_true
                                    OR mt_selected_row_no[] IS INITIAL
                                  THEN abap_true ).
  INSERT VALUE #(
     function = mc_cmd-delete
     icon     = icon_delete_row
     disabled = lv_del_disabled
     text     = 'Delete items'(dei) ) INTO TABLE e_object->mt_toolbar.

  mo_action->add_functions(
   EXPORTING iv_bopf_name = mo_metadata->mv_bopf_name
             iv_bo_key    = mo_metadata->mv_bo_key
             io_grid      = sender
             iv_disabled  = lv_del_disabled
   CHANGING  ct_toolbar   = e_object->mt_toolbar ).
ENDMETHOD.


METHOD _on_user_command.
  CASE e_ucomm.
    WHEN mc_cmd-create.
      _execute_create( sender ).

    WHEN mc_cmd-delete.
      _execute_delete( sender ).

    WHEN OTHERS.
      CHECK mo_action->is_action(
         io_grid  = sender
         iv_ucomm = e_ucomm
      ) <> abap_true.
  ENDCASE.
ENDMETHOD.


METHOD _refresh_line.
**********************************************************************
  " Source
**********************************************************************
  IF    ir_bopf_line IS INITIAL
    AND iv_key       IS INITIAL.
    zcx_eui_no_check=>raise_sys_error( iv_message = 'Pass IR_BOPF_LINE or IV_KEY parameter' ).
  ENDIF.

  DATA(lr_bopf_line) = ir_bopf_line.
  IF lr_bopf_line IS INITIAL.
    TRY.
        _get_control( IMPORTING eo_manager  = DATA(lo_manager)
                                ev_act_node = DATA(lv_act_node) ).
        lr_bopf_line = lo_manager->retrieve_row(
                        iv_node_type = lv_act_node
                        iv_key       = iv_key
                        iv_edit_mode = mv_edit_mode ).
      CATCH /bobf/cx_frw INTO DATA(lo_error).
        zcx_eui_no_check=>raise_sys_error( io_error = lo_error ).
    ENDTRY.
  ENDIF.
  ASSIGN lr_bopf_line->* TO FIELD-SYMBOL(<ls_bopf>).

  DATA(lr_bopf_ui) = mo_tab_info->bopf_to_ui( <ls_bopf> ).
  ASSIGN lr_bopf_ui->* TO FIELD-SYMBOL(<ls_bopf_ui>).

**********************************************************************
  " Where to write
**********************************************************************
  FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
  IF cs_line IS SUPPLIED.
    ASSIGN cs_line TO FIELD-SYMBOL(<ls_line>).
  ELSEIF iv_new_index IS SUPPLIED.
    ASSIGN mo_tab_info->mr_table->* TO <lt_table>.
    IF iv_new_index IS INITIAL.
      iv_new_index = lines( <lt_table> ) + 1.
    ENDIF.
    INSERT <ls_bopf_ui> INTO <lt_table> INDEX iv_new_index ASSIGNING <ls_line>.
  ELSE.
    ASSIGN mo_tab_info->mr_table->* TO <lt_table>.
    READ TABLE <lt_table> ASSIGNING <ls_line>       "#EC CI_ANYSEQ
      WITH KEY ('KEY') = iv_key.
    IF sy-subrc <> 0.
      zcx_eui_no_check=>raise_sys_error( iv_message = |{ iv_key } not found in ALV| ).
    ENDIF.
  ENDIF.

**********************************************************************
  "Write to UI
**********************************************************************

  " Ext fields
  DATA(ls_ext) = lcl_tab_info=>create_ext_fieds( io_message ).
  MOVE-CORRESPONDING: <ls_bopf_ui>  TO <ls_line>,
                      ls_ext        TO <ls_line>.
ENDMETHOD.


METHOD _update_root_node.
  CHECK mo_parent IS NOT INITIAL.

  DATA(lv_root_attr_name) = ms_assoc-_bo-bind_attribute.
  IF lv_root_attr_name IS INITIAL.
    MESSAGE 'Cannot create an association'(ccs) TYPE 'S' DISPLAY LIKE 'W'.
    RETURN.
  ENDIF.

  DATA(lo_manager) = mo_parent->mo_manager.
  TRY.
      DATA(lr_root) = lo_manager->retrieve_row(
                          iv_node_type = ms_create_info-source_node
                          iv_key       = ms_create_info-source_key
                          iv_edit_mode = mv_edit_mode ).
    CATCH /bobf/cx_frw INTO DATA(lo_error).
      MESSAGE lo_error TYPE 'S' DISPLAY LIKE 'E'.
      RETURN.
  ENDTRY.

  ASSIGN lr_root->* TO FIELD-SYMBOL(<ls_root>).
  ASSIGN COMPONENT: 'KEY' OF STRUCTURE <ls_root> TO FIELD-SYMBOL(<lv_key>) CASTING TYPE /bobf/conf_key,
        lv_root_attr_name OF STRUCTURE <ls_root> TO FIELD-SYMBOL(<lv_dest_attr>).
  IF sy-subrc <> 0.
    MESSAGE |The detected { lv_root_attr_name } is wrong| TYPE 'S' DISPLAY LIKE 'E'.
    RETURN.
  ENDIF.

  FIELD-SYMBOLS <lt_table> TYPE INDEX TABLE.
  DATA(lr_alv_table) = zcl_eui_conv=>get_grid_table( io_grid ).
  ASSIGN lr_alv_table->* TO <lt_table>.
  IF <lt_table> IS INITIAL.
    MESSAGE 'Nothing selected'(nsl) TYPE 'S' DISPLAY LIKE 'W'.
    RETURN.
  ENDIF.
  ASSIGN <lt_table>[ 1 ] TO FIELD-SYMBOL(<ls_src>).

**********************************************************************
  " № 1 - KEY to root
  ASSIGN COMPONENT 'KEY' OF STRUCTURE <ls_src> TO FIELD-SYMBOL(<lv_src_attr>).
  <lv_dest_attr> = <lv_src_attr>.

**********************************************************************
  " № 2 - Other fields to root
  _get_node_info( IMPORTING et_catalog = DATA(lt_catalog) ).
  LOOP AT ms_assoc-_bo-copy_map ASSIGNING FIELD-SYMBOL(<ls_map>).
    ASSIGN lt_catalog[ parameter0 = <ls_map>-src ] TO FIELD-SYMBOL(<ls_catalog>).
    IF sy-subrc <> 0.
      zcx_eui_no_check=>raise_sys_error( iv_message = |Wrong mapping for { <ls_map>-src }| ).
    ENDIF.

    UNASSIGN: <lv_src_attr>,
              <lv_dest_attr>.
    ASSIGN COMPONENT: <ls_catalog>-fieldname OF STRUCTURE <ls_src>  TO <lv_src_attr>,
                      <ls_map>-dest          OF STRUCTURE <ls_root> TO <lv_dest_attr>.
    <lv_dest_attr> = <lv_src_attr>.
  ENDLOOP.

**********************************************************************
  " Update & check
  DATA(lt_mod) = VALUE /bobf/t_frw_modification(
   ( node           = ms_create_info-source_node
     change_mode    = /bobf/if_frw_c=>sc_modify_update
     key            = <lv_key>
     data           = lr_root ) ).

  TRY.
      lo_manager->modify(
         EXPORTING it_modification = lt_mod
         IMPORTING eo_message      = DATA(lo_message)
                   ev_ok           = DATA(lv_ok) ).
    CATCH /bobf/cx_frw INTO lo_error.
      MESSAGE lo_error TYPE 'S' DISPLAY LIKE 'E'.
      RETURN.
  ENDTRY.
  CHECK lv_ok <> abap_true.
  NEW zcl_bopf_messages( )->add_from_message( lo_message )->show( ).
ENDMETHOD.
ENDCLASS.
