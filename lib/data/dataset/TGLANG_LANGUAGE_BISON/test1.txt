%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE * yyin;
int line;
char character;
char token[1000];

void yyerror(char* msg);
%}

%token IDENTIFIER INTEGER
	
%%

start: expression
;

expression: INTEGER
| IDENTIFIER
| expression '+' expression
| expression '-' expression
| expression '*' expression
| expression '/' expression
| '(' expression ')'
;

%%

void yyerror(char* msg) 
{
	printf("%s: line %d\n", msg, line);
	exit(0);
}

void getch()
{
	character=getc(yyin);
	if(character=='\n')  line++;
}

void getnbc()
{
	while((character==' ') || (character=='\t') || (character=='\r') || (character=='\n')) 
		getch();	
}

void concat()
{
	int len=strlen(token);
	token[len]=character;
	token[len+1]='\0';	
}

int letter()
{
	if(((character>='a') && (character<='z')) || ((character>='A') && (character<='Z')))
		return 1;
	else 
		return 0;
}

int digit()
{
	if((character>='0') && (character<='9'))
		return 1;
	else 
		return 0;
}

void retract()
{
	ungetc(character,yyin);
	if(character=='\n') line--;
	character='\0';
}

int yylex()
{
	int num;
	char *lexeme;
		
	strcpy(token,"");
	getch();
	getnbc();

	if(letter())
	{
		while(letter() || digit())
		{
			concat();
			getch();
		}
		retract();
		return IDENTIFIER;
	}

	if(digit())
	{
		while(digit())
		{
			concat();
			getch();
		}
		retract();
		return INTEGER;	
	}

	switch(character)
	{
		case '+':
		case '-':
		case '*':
		case '/':
		case '(':
		case ')':
		case EOF:
			return character;			
	}
	
	printf("lexical error: line %d\n", line);
	exit(0);
}

int main(int argc, char *argv[]) {
	if(argc!=2) {
		printf("usage: %s filename\n", argv[0]);
		exit(0);
	}			

	if( (yyin=fopen(argv[1], "r")) ==NULL )
	{
		printf("open file %s failed\n", argv[1]);
		exit(0);
	}

	/* Give values to global variables */
	line=1;
	character=0;
	token[0]=0;

	yyparse();

	fclose(yyin);
	return 0;
}

