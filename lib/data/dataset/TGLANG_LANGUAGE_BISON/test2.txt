%{
#include<stdio.h>
%}

%token ID NUMBER
%left '+' '-'
%left '*' '/'

%%
expr: expr '+' expr | expr '-' expr | expr '*' expr | expr '/' expr | '(' expr ')' | NUMBER | ID ; 
%%

int main(void)
{
printf("Enter expression : ");
yyparse();
printf("Valid\n");
return 1;
}

int yyerror()
{
printf("Invalid Expression\n");
}