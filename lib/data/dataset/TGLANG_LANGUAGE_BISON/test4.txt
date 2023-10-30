%{
	// Includes
	#include <iostream>
	#include <map>
	#include <stack>
	#include <vector>

	// Externs
	extern "C" int yylex();
	extern "C" int yyparse();

	// Functions
	void yyerror(const char*);
	double eval(std::vector<int>, double=0);
	void operate(std::stack<double> &, char);

	for(int a=0; a<5; a++)
	{
		int x;
	}

	// Variables
	std::map< char* , std::vector<int>    > list;
	std::map< char* , std::vector<double> > values;
	std::vector<int>    postfixe;
	std::vector<double> valeurs;
	double min=-1, max=1, pas=0.1;
%}

// Union
%union {
	double number;
	char* name;
}

// Tokens
%token <number>	NUM
%token <name>	VAR
%token SIN

// Types
%type <number> expr

// Operators
%left '+' '-'
%left '*' '/'

// Rules
%%
program:
	%empty
|	program line
;

line:
	'\n'
|	VAR '=' expr '\n'	{
							list.insert  ( std::pair< char* , std::vector<int>    > ($1, postfixe) ); postfixe.clear();
							values.insert( std::pair< char* , std::vector<double> > ($1, valeurs)  ); valeurs.clear();
						}
;

expr:
	NUM					{ postfixe.push_back(NUM); valeurs.push_back($1); }
|	VAR					{ postfixe.push_back(VAR); valeurs.push_back(0); }
|	expr '+' expr		{ postfixe.push_back('+'); valeurs.push_back(0); }
|	expr '-' expr		{ postfixe.push_back('-'); valeurs.push_back(0); }
|	expr '*' expr		{ postfixe.push_back('*'); valeurs.push_back(0); }
|	expr '/' expr		{ postfixe.push_back('/'); valeurs.push_back(0); }
|	SIN '(' expr ')'	{ }
|	'(' expr ')'		{ $$ = $2; }
;

// C++ Code
%%
int main(int argc, char** argv)
{
	yyparse();

	for(auto it : list)
	{
		std::cout << it.first << " [";
		for(double x=min; x < max-pas; x+=pas)
			std::cout << x << " " << eval(it.second, x) << ";";
		std::cout << max << " " << eval(it.second, max) << "]" << std::endl;
	}
}

void yyerror(const char* s)
{

}

double eval(std::vector<int> postfixe, double x)
{
	std::stack<double> pile;
	double tmp1, tmp2;

	for(int i=0; i < postfixe.size(); i++)
	{
		if(postfixe[i] == NUM) pile.push(valeurs[i]);
		if(postfixe[i] == VAR) pile.push(x);
		if(postfixe[i] == '+') operate(pile, '+');
		if(postfixe[i] == '-') operate(pile, '-');
		if(postfixe[i] == '*') operate(pile, '*');
		if(postfixe[i] == '/') operate(pile, '/');
	}

	return pile.top();
}

void operate(std::stack<double> & pile, char op)
{
	double tmp1 = pile.top(); pile.pop();
	double tmp2 = pile.top(); pile.pop();
	switch(op)
	{
		case '+': pile.push(tmp1 + tmp2); break;
		case '-': pile.push(tmp1 - tmp2); break;
		case '*': pile.push(tmp1 * tmp2); break;
		case '/': pile.push(tmp1 / tmp2); break;
	}
}
