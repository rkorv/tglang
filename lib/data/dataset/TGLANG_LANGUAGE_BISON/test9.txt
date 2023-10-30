%{
    #include <stdio.h>
%}

/* declare tokens (flex)*/

%token NUMBER 
%token PLUS MINUS MULTI DIV ABS
%token CP OP
%token EOL

%% 
/* BNF-GRAMMER */

statement: /* nothing */
    | statement exp EOL { printf("= %d\n", $2); }
;

exp: factor 
    | exp PLUS factor   { $$ = $1 + $3; } 
    | exp MINUS factor  { $$ = $1 - $3; } 
;

factor: term
    | factor MULTI term { $$ = $1 * $3; }
    | factor DIV term   { $$ = $1 / $3; }
;

term: NUMBER 
    | ABS term  { $$ = ($2 >= 0 ? $2 : -$2); }
    | OP exp CP { $$ = $2; }
%%

main(int argc, char **argv){
    yyparse();
}

yyerror(char *error){
    fprintf(stderr,"error: %s\n",error);
}
