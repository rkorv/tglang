%{
#include <cstdio>
#include <iostream>
using namespace std;

int yylex();
extern "C" int yyparse();
extern "C" FILE *yyin;
 
void yyerror(char *s);
%}

%union {
    int ival;
    float fval;
    char *sval;
}

%token ENDL PLUS MINUS MUL DIV LPAREN RPAREN

%token <ival> INT
%token <sval> IDENT

%type <ival> expression1
%type <ival> expression

%left PLUS MINUS
%left MUL DIV

%%
start:
        expressions;
expressions:
    expressions expression1 ENDL
    | expression1 ENDL;
expression1:
    expression { cout<<$1<<endl; }; 
expression: 
    expression PLUS expression { $$ = $1 + $3; }
    |expression MINUS expression { $$ = $1 - $3; }
    |expression MUL expression { $$ = $1 * $3; }
    |expression DIV expression { $$ = $1 / $3; }
    |LPAREN expression RPAREN { $$ = $2; }
    | INT { $$ = $1; };
%%

int main(int argc, char *argv[]) {
    if (argc!= 2) {
        cout <<"Usage: <command> filename"<<endl;
        return 1;
    }
    FILE *myfile = fopen(argv[1], "r");
    if (!myfile) {
        cout << "I can't open "<<argv[1]<< endl;
        return -1;
    }
    yyin = myfile;

    do {
        yyparse();
    } while (!feof(yyin));
    
}

void yyerror(char *s) {
    cout << "Parse error: " << s << endl;
    exit(-1);
}
