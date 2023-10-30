%{

#include <stdio.h>
#include <ctype.h>
#include <math.h>

#define YYSTYPE double

int yylex(void);
void yyerror(const char* s);

%}

%token NUM
%left '+' '-'
%left '*' '/'
%left NEG
%right '^'

%%

input   :   /* empty */
        |   input line 
line    :   '\n'
        |   expr '\n'
            { printf("\t%.10g\n", $1); }
        |   error '\n'
            {yyerrok;}
expr    :   NUM
        |   expr '+' expr
            {$$ = $1 + $3;}
        |   expr '-' expr
            {$$ = $1 - $3;}
        |   expr '*' expr
            {$$ = $1 * $3;}
        |   expr '/' expr
            {$$ = $1 / $3;}
        |   expr '^' expr
            {$$ = pow($1, $3);}
        |   '-' expr
            %prec NEG
            {$$ = -$2;}
        |   '(' expr ')'
            {$$ = $2;}

%%

/* トークン解析関数 */
int yylex(void)
{
  int c;

  /* 空白、タブは飛ばす */
  while((c = getchar()) == ' ' || c == '\t')
    ;
  /* 数値を切り出す */
  if(c == '.' || isdigit(c))
  {
    ungetc(c, stdin);
    scanf("%lf", &yylval);
    return NUM;
  }
  /* EOF を返す */
  if(c == EOF)
    return 0;
  /* 文字を返す */
  return c;
}

/* エラー表示関数 */
void yyerror(const char* s)
{
  fprintf(stderr, "error: %s\n", s);
}

int main(void)
{
  /* 構文解析関数 yyparse */
  return yyparse();
}
