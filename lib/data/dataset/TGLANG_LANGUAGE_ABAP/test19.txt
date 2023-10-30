*&---------------------------------------------------------------------*
*& Report  Z_CALC
*&---------------------------------------------------------------------*
REPORT  z_calc.

DATA: vg_okcode(4)   TYPE c,
wc_display(38) TYPE c,
wc_dismem(5)   TYPE c,
wc_memoria(38) TYPE c,
wc_oper(1)     TYPE c,
wc_aux(38)     TYPE c,
wc_aux2(38)    TYPE c,
wc_aux3(2)     TYPE c.

*&---------------------------------------------------------------------*
*&      Module  STATUS_0100  OUTPUT
*&---------------------------------------------------------------------*
MODULE status_0100 OUTPUT.
SET PF-STATUS 'STATUS_0'.
SET TITLEBAR '001'.
ENDMODULE. "STATUS_0100  OUTPUT

*&---------------------------------------------------------------------*
*&      Module  USER_COMMAND_0100  INPUT
*&---------------------------------------------------------------------*
MODULE user_command_0100 INPUT.

CASE vg_okcode.
*&---------------------------------------------------------------------*
* Comandos do programa, sair, voltar, etc.
*&---------------------------------------------------------------------*
WHEN 'EXIT' OR 'BACK' OR 'UP'.
CLEAR vg_okcode.
LEAVE PROGRAM.

*&---------------------------------------------------------------------*
* Botões Numéricos
*&---------------------------------------------------------------------*
WHEN 'BT0'.
IF wc_display NE 0.
CONCATENATE wc_display '0' INTO wc_display.
ENDIF.
WHEN 'BT1'.
CONCATENATE wc_display '1' INTO wc_display.
WHEN 'BT2'.
CONCATENATE wc_display '2' INTO wc_display.
WHEN 'BT3'.
CONCATENATE wc_display '3' INTO wc_display.
WHEN 'BT4'.
CONCATENATE wc_display '4' INTO wc_display.
WHEN 'BT5'.
CONCATENATE wc_display '5' INTO wc_display.
WHEN 'BT6'.
CONCATENATE wc_display '6' INTO wc_display.
WHEN 'BT7'.
CONCATENATE wc_display '7' INTO wc_display.
WHEN 'BT8'.
CONCATENATE wc_display '8' INTO wc_display.
WHEN 'BT9'.
CONCATENATE wc_display '9' INTO wc_display.

*&---------------------------------------------------------------------*
* Botões de Operação
*&---------------------------------------------------------------------*
* Botão Somar
WHEN 'BTSM'.
wc_aux = wc_display.
wc_oper = '+'.
CLEAR wc_display.

* Botão Subtrair
WHEN 'BTSB'.
wc_aux = wc_display.
wc_oper = '-'.
CLEAR wc_display.

* Botão Multiplicar
WHEN 'BTMT'.
wc_aux = wc_display.
wc_oper = '*'.
CLEAR wc_display.

* Botão Dividir
WHEN 'BTDV'.
wc_aux = wc_display.
wc_oper = '/'.
CLEAR wc_display.

* Botão Raiz Quadrada
WHEN 'BTSQ'.
IF wc_display IS NOT INITIAL.
TRY.
wc_display = SQRT( wc_display ).
CATCH cx_sy_conversion_no_number.
wc_display = 'ERROR'.
CATCH cx_sy_arithmetic_error.
wc_display = 'ERROR'.
CATCH cx_sy_conversion_error.
wc_display = 'ERROR'.
ENDTRY.
ENDIF.

* Botão Porcentagem
WHEN 'BTPR'.
IF wc_oper = '*' AND wc_display IS NOT INITIAL.
wc_aux2 = ( wc_aux * wc_display ) / 100.
wc_display = wc_aux2.
CLEAR: wc_aux, wc_aux2.
ENDIF.

* Botão Divide por 1.
WHEN 'BTD1'.
IF wc_display IS NOT INITIAL.
wc_display = 1 / wc_display.
ENDIF.

*&---------------------------------------------------------------------*
* Botões de Funcionais
*&---------------------------------------------------------------------*
* Botão casa Decimal.
WHEN 'BTPT'.
IF wc_display IS INITIAL.
CONCATENATE wc_display '0.' INTO wc_display.
ENDIF.
* Só permite um ponto decimal.
IF wc_display NA '.'.
CONCATENATE wc_display '.' INTO wc_display.
ENDIF.

* Botão Limpar
WHEN 'BTC'.
CLEAR: wc_display, wc_aux, wc_aux2, wc_oper.

* Botão Backspace.
WHEN 'BTBK'.
IF wc_display+1(1) IS INITIAL.
CLEAR wc_display.
ELSE.
wc_aux3 = 37.
DO 37 TIMES.
IF wc_display+wc_aux3(1) IS NOT INITIAL.
CLEAR wc_display+wc_aux3(1).
CLEAR wc_aux3.
EXIT.
ENDIF.
wc_aux3 = wc_aux3 - 1.
ENDDO.
ENDIF.

* Botão de alteração do sinal.
WHEN 'BTSN'.
IF wc_display IS NOT INITIAL AND wc_display NE 0.
IF wc_display NA '-'.
wc_aux = wc_display.
CLEAR wc_display.
wc_display = '-'.
CONCATENATE wc_display wc_aux INTO wc_display.
CLEAR wc_aux.
ELSE.
REPLACE '-' WITH '' INTO wc_display.
CONDENSE wc_display NO-GAPS.
ENDIF.
ENDIF.

*&---------------------------------------------------------------------*
* Botões de memória
*&---------------------------------------------------------------------*
* Botão para adicionar valor a memória MS
WHEN 'BTAD'.
IF wc_display IS NOT INITIAL.
wc_memoria = wc_display.
wc_dismem = '  M  '.
ENDIF.

* Botão para limpar valor da memória
WHEN 'BTCL'.
CLEAR: wc_memoria, wc_dismem.

* Botão para exibir valor memorizado.
WHEN 'BTEX'.
wc_display = wc_memoria.

* Botão para adicionar valor da tela ao valor memorizado
WHEN 'BTSO'.
TRY.
wc_memoria = wc_memoria + wc_display.
CATCH cx_sy_conversion_overflow.
wc_display = 'ERROR'.
CATCH cx_sy_arithmetic_overflow.
wc_display = 'ERROR'.
CATCH cx_sy_conversion_no_number.
wc_display = 'ERROR'.
ENDTRY.

*&---------------------------------------------------------------------*
* Botão Resultado '='.
*&---------------------------------------------------------------------*
WHEN 'BTEQ'.
CASE wc_oper.

* Operação de Soma
WHEN '+'.
wc_aux2 = wc_display.
CLEAR wc_display.

TRY.
wc_display = wc_aux + wc_aux2.
CATCH cx_sy_conversion_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_arithmetic_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_conversion_no_number.
wc_display = 'ERROR'.
ENDTRY.

CLEAR: wc_aux, wc_aux2, wc_oper.

* Operação de subtração
WHEN '-'.
CONDENSE wc_aux.
wc_aux2 = wc_display.
CLEAR wc_display.

TRY.
wc_display = wc_aux - wc_aux2.
CATCH cx_sy_conversion_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_arithmetic_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_conversion_no_number.
wc_display = 'ERROR'.
ENDTRY.

IF wc_aux < wc_aux2 AND wc_aux IS NOT INITIAL AND wc_aux2 IS NOT INITIAL.
CONCATENATE wc_display '-' INTO wc_display.
ENDIF.
CLEAR: wc_aux, wc_aux2, wc_oper.

* Operação de Multiplicação
WHEN '*'.
wc_aux2 = wc_display.
CLEAR wc_display.

TRY.
wc_display = wc_aux * wc_aux2.
CATCH cx_sy_conversion_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_arithmetic_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_conversion_no_number.
wc_display = 'ERROR'.
ENDTRY.

CLEAR: wc_aux, wc_aux2, wc_oper.

* Operação de Divisão
WHEN '/'.
wc_aux2 = wc_display.
CLEAR wc_display.

TRY.
wc_display = wc_aux / wc_aux2.
CATCH cx_sy_conversion_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_arithmetic_overflow.
CLEAR: wc_aux, wc_aux2.
wc_display = 'ERROR'.
CATCH cx_sy_conversion_no_number.
wc_display = 'ERROR'.
ENDTRY.

CLEAR: wc_aux, wc_aux2, wc_oper.

ENDCASE.
ENDCASE.
ENDMODULE. "USER_COMMAND_0100  INPUT