%define parse.error verbose

%{
#include<iostream>
#include<cstdlib>
#include<cstring>
#include<cmath>
#include "1505033_SymbolTable.h"

//#define YYSTYPE SymbolInfo*

using namespace std;

int yyparse(void);
int yylex(void);
extern int yylineno;
extern char *yytext;
extern FILE *yyin;
 FILE *fp;
 FILE *logout;
 FILE *errorFile;
int error_count=0;
int syntax_error=0;

SymbolTable table(100);

string globalType;
string func_ret_Type;
int arrayIndex=0;
vector <parameter> list;
vector <string> arg_type_list;


string type1, type2, type3, type4;
string name1, name2;


void yyerror(const char *s)
{
	//write your code
	fprintf(errorFile, "%s at Line no. : %d\n\n ",s,yylineno);
}


%}
%union{
SymbolInfo * symbolinfo;

}
%token <symbolinfo> ID
%token <symbolinfo> INT
%token <symbolinfo> FLOAT
%token <symbolinfo> VOID
%token <symbolinfo> SEMICOLON
%token <symbolinfo> COMMA
%token <symbolinfo> LPAREN
%token <symbolinfo> RPAREN
%token <symbolinfo> ADDOP
%token <symbolinfo> CONST_INT
%token <symbolinfo> CONST_CHAR
%token <symbolinfo> CONST_FLOAT
%token <symbolinfo> RETURN
%token <symbolinfo> LCURL
%token <symbolinfo> RCURL
%token <symbolinfo> ASSIGNOP
%token <symbolinfo> LTHIRD
%token <symbolinfo>  RTHIRD
%token <symbolinfo> IF 
%token <symbolinfo> ELSE
%token <symbolinfo> FOR
%token <symbolinfo> WHILE
%token <symbolinfo> DO
%token <symbolinfo> BREAK
%token <symbolinfo> CHAR
%token <symbolinfo> DOUBLE
%token <symbolinfo> SWITCH
%token <symbolinfo> CASE
%token <symbolinfo> DEFAULT
%token <symbolinfo> CONTINUE
%token <symbolinfo> MULOP
%token <symbolinfo> INCOP
%token <symbolinfo> RELOP
%token <symbolinfo> LOGICOP
%token <symbolinfo> BITOP
%token <symbolinfo> NOT
%token <symbolinfo> COMMENT
%token <symbolinfo> STRING
%token <symbolinfo> DECOP
%token <symbolinfo> PRINTLN 
%token LOWER_THAN_ELSE

%type <symbolinfo> start
%type <symbolinfo> program
%type <symbolinfo> unit
%type <symbolinfo> type_specifier
%type <symbolinfo> declaration_list
%type <symbolinfo> var_declaration
%type <symbolinfo> func_declaration
%type <symbolinfo> func_definition
%type <symbolinfo> compound_statement
%type <symbolinfo> parameter_list
%type <symbolinfo> statements
%type <symbolinfo> expression_statement
%type <symbolinfo> statement
%type <symbolinfo> expression
%type <symbolinfo> variable
%type <symbolinfo> logic_expression
%type <symbolinfo> rel_expression
%type <symbolinfo> simple_expression
%type <symbolinfo> unary_expression
%type <symbolinfo> term
%type <symbolinfo> factor
%type <symbolinfo> argument_list
%type <symbolinfo> arguments

/*%left 
%right
*/
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE


%%

start : program
	{
		//write your code in this block in all the similar blocks below
		{fprintf(logout,"At line no: %d start: program\n\n",yylineno);}
		table.PrintAllScopeTables(logout);
	}
	;

program : program unit {fprintf(logout,"At line no: %d program: program unit\n\n",yylineno);
	//$1->next=$2;
	//$$=$1;
	string str=$1->getname();
	str+=$2->getname();
	fprintf(logout,"%s",str.c_str());
	$$->setname(str);
	
	}
	| unit	{fprintf(logout,"At line no: %d program: unit\n\n",yylineno);

		string str=$1->getname();
	        fprintf(logout,"%s",str.c_str());
		$$->setname(str);
		}
	;
	
unit : var_declaration 
	{	
		fprintf(logout,"At line no: %d unit: var_declaration\n\n",yylineno);

		string str=$1->getname();
	        fprintf(logout,"%s",str.c_str());
		$$->setname(str);
		  	
		
		
		
	}
     | func_declaration {fprintf(logout,"At line no: %d unit: func_declaration\n\n",yylineno);

		string str=$1->getname();
	        fprintf(logout,"%s",str.c_str());
		$$->setname(str);
     
     }
     | func_definition {fprintf(logout,"At line no: %d unit: func_definition\n\n",yylineno);
     		string str=$1->getname();
	        fprintf(logout,"%s",str.c_str());
		$$->setname(str);
     }
     ;
     
func_declaration : type_specifier ID LPAREN parameter_list RPAREN SEMICOLON {fprintf(logout,"At line no: %d func_declaration : type_specifier ID LPAREN parameter_list RPAREN SEMICOLON\n\n",yylineno);
		int no_of_parameters=list.size();
		//table.InsertFunction( $2->getname(), $1->getname(),list,no_of_parameters,logout,"dec");	
		string n=$2->getname();
		SymbolInfo *ret=table.Lookup(n);
		if(ret==NULL){
		table.InsertFunction( $2->getname(), $1->getname(),list,no_of_parameters,logout,"dec");
		}
		else
		{
			string ind=ret->indicator;
			string flag=ret->func_dec_def;
			
			if(ind=="arr")
			{
				fprintf(errorFile,"Error at line %d: Array with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="var")
			{
				fprintf(errorFile,"Error at line %d: Variable with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="func" && flag=="dec")
			{
				fprintf(errorFile,"Error at line %d: Multiple declarations of the same function.\n\n",yylineno,ret->name);
				error_count++;
	
			}
			else if(ind=="func" && flag=="def")
			{
				fprintf(errorFile,"Error at line %d: Function already defined.Declaration should come before definition.\n\n",yylineno,ret->name);
				error_count++;
			}
		}
		list.clear();	
		table.PrintAllScopeTables(logout);
		
		string str=$1->getname();
		str+=" ";
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 		str+=$6->getname();
 		str+="\n\n";
 		fprintf(logout,"%s",str.c_str());
 		$$->setname(str);
		
		}
		| type_specifier ID LPAREN RPAREN SEMICOLON {fprintf(logout,"At line no: %d func_declaration : type_specifier ID LPAREN RPAREN SEMICOLON\n\n",yylineno);
		int no_of_parameters=list.size();
		string n=$2->getname();
		SymbolInfo *ret=table.Lookup(n);
		if(ret==NULL){
		table.InsertFunction( $2->getname(), $1->getname(),list,no_of_parameters,logout,"dec");
		}
		else
		{
			
			string ind=ret->indicator;
			string flag=ret->func_dec_def;
			
			if(ind=="arr")
			{
				fprintf(errorFile,"Error at line %d: Array with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="var")
			{
				fprintf(errorFile,"Error at line %d: Variable with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="func" && flag=="dec")
			{
				fprintf(errorFile,"Error at line %d: Multiple declarations of the same function.\n\n",yylineno,ret->name);
				error_count++;	
			}
			else if(ind=="func" && flag=="def")
			{
				fprintf(errorFile,"Error at line %d: Function already defined.Declaration should come before definition.\n\n",yylineno,ret->name);
				error_count++;
			}
		}
		list.clear();		
		table.PrintAllScopeTables(logout);

		string str=$1->getname();
		str+=" ";
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 		str+="\n\n";
 		fprintf(logout,"%s",str.c_str());
 		$$->setname(str);
		
		}
		|type_specifier ID LPAREN parameter_list RPAREN error{yyerror("Semicolon should end function declaration");
		syntax_error++;}
		|type_specifier ID LPAREN parameter_list RPAREN RPAREN  error SEMICOLON {yyerror("Too many )s"); syntax_error++;}
		|type_specifier ID LPAREN LPAREN parameter_list RPAREN error SEMICOLON {yyerror("Too many (s"); syntax_error++;}
		|type_specifier ID LPAREN RPAREN error{yyerror("Semicolon should end function declaration"); syntax_error++;}
		|type_specifier ID LPAREN RPAREN RPAREN  error SEMICOLON {yyerror("Too many )s"); syntax_error++;}
		|type_specifier ID LPAREN LPAREN RPAREN error SEMICOLON {yyerror("Too many (s"); syntax_error++;}
		;
		 
func_definition : type_specifier ID LPAREN parameter_list RPAREN {int no_of_parameters=list.size();
		string n=$2->getname();
		string returnType1=$1->getname();
		func_ret_Type=returnType1;
		SymbolInfo *ret=table.Lookup(n);
		if(ret==NULL){
		table.InsertFunction( $2->getname(), $1->getname(),list,no_of_parameters,logout,"def");
		}
		else
		{
			string ind=ret->indicator;
			string flag=ret->func_dec_def;
			string returnType2=ret->type;
			if(ind=="arr")
			{
				fprintf(errorFile,"Error at line %d: Array with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="var")
			{
				fprintf(errorFile,"Error at line %d: Variable with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="func" && flag=="dec")
			{
				ret->func_dec_def="def";
				vector <parameter> list2=ret->parameterList;
				if(returnType1!=returnType2)
				{
					fprintf(errorFile,"Error at line %d: Return types of function declaration (%s) and definition(%s) do not match\n\n",yylineno,returnType1.c_str(),
					returnType2.c_str());
					error_count++;
				}
				if(list.size()!=list2.size())
				{
					fprintf(errorFile,"Error at line %d: Number of parameters in function definition (%d) and function declaration(%d) do not match\n\n",yylineno,list.size(),
					list2.size());
					error_count++;
				}
				else{
				for(int i=0;i<list.size();i++)
				{
					parameter p1=list[i];
					parameter p2=list2[i];

					if(p2.flag!=p1.flag)
					{
						fprintf(errorFile,"Error at line %d: Parameter lists of function(%s) definition and declaration do not match\n\n",yylineno,ret->name.c_str());
						error_count++;
					}
					else if(p2.flag==2)
					{
						if(p1.type!=p2.type || p1.name!=p2.name)
						{
							fprintf(errorFile,"Error at line %d: Parameter lists of function(%s) definition and declaration do not match\n\n",yylineno,ret->name.c_str());
							error_count++;
						}
					}
					else if(p2.flag==1)
					{
						if(p1.type!=p2.type)
						{
							fprintf(errorFile,"Error at line %d: Parameter lists of function(%s) definition and declaration do not match\n\n",yylineno,ret->name.c_str());
							error_count++;
						}
					}
				}
				}
				
			}
			else if(ind=="func" && flag=="def")
			{
				fprintf(errorFile,"Error at line %d: Multiple definitions of the same function\n\n",yylineno);
				error_count++;
			}
		}
		}compound_statement {
		table.PrintAllScopeTables(logout);
		table.ExitScope(logout);
		
		fprintf(logout,"At line no: %d func_definition : type_specifier ID LPAREN parameter_list RPAREN compound_statement\n\n",yylineno);

		string str=$1->getname();
		str+=" ";
		str+=$2->getname();
		str+=$3->getname();
		str+=$4->getname();
		str+=$5->getname();
		str+=$7->getname();
		str+="\n\n";
 		fprintf(logout,"%s",str.c_str());
 		$$->setname(str);		
		
		}
		| type_specifier ID LPAREN RPAREN {
		string n=$2->getname();
		string returnType1=$1->getname();
		func_ret_Type=returnType1;
		SymbolInfo *ret=table.Lookup(n);
		if(ret==NULL){													
		table.InsertFunction( $2->getname(), $1->getname(),list,0,logout,"def");
		}
		else
		{
			string ind=ret->indicator;
			string flag=ret->func_dec_def;
			string returnType2=ret->type;
			//fprintf(errorFile,"Sure: %s %s\n\n",ind.c_str(),flag.c_str());
			if(ind=="arr")
			{
				fprintf(errorFile,"Error at line %d: Array with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="var")
			{
				fprintf(errorFile,"Error at line %d: Variable with name %s already exists in symbol table\n\n",yylineno,ret->name);
				error_count++;
			}
			else if(ind=="func" && flag=="dec")
			{
				vector <parameter> list2=ret->parameterList;
				//fprintf(errorFile,"Here: %d %d\n\n",list.size(),list2.size());
				ret->func_dec_def="def";
				if(returnType1!=returnType2)
				{
					fprintf(errorFile,"Error at line %d: Return types of function declaration (%s) and definition(%s) do not match\n\n",yylineno,returnType1.c_str(),
					returnType2.c_str());
					error_count++;
				}
				if(list2.size()!=0)
				{
					fprintf(errorFile,"Error at line %d: Number of parameters in function definition (%d) and function declaration(%d) do not match\n\n",yylineno,list.size(),
					list2.size());
					error_count++;
				}
				/*else{
				for(int i=0;i<list.size();i++)
				{
					parameter p1=list[i];
					parameter p2=list2[i];

					if(p2.flag!=p1.flag)
					{
						fprintf(errorFile,"Error at line %d: Parameter lists of function(%s) definition and declaration do not match\n\n",yylineno,ret->name.c_str());
						error_count++;
					}
					else if(p2.flag==2)
					{
						if(p1.type!=p2.type || p1.name!=p2.name)
						{
							fprintf(errorFile,"Error at line %d: Parameter lists of function(%s) definition and declaration do not match\n\n",yylineno,ret->name.c_str());
							error_count++;
						}
					}
					else if(p2.flag==1)
					{
						if(p1.type!=p2.type)
						{
							fprintf(errorFile,"Error at line %d: Parameter lists of function(%s) definition and declaration do not match\n\n",yylineno,ret->name.c_str());
							error_count++;
						}
					}
				}
				}*/
				
			}
			else if(ind=="func" && flag=="def")
			{
				fprintf(errorFile,"Error at line %d: Multiple definitions of the same function\n\n",yylineno);
				error_count++;
			}
		}
		} compound_statement {
		table.PrintAllScopeTables(logout);
		table.ExitScope(logout);
		fprintf(logout,"At line no: %d func_definition : type_specifier ID LPAREN RPAREN compound_statement\n\n",yylineno);
		string str=$1->getname();
		str+=" ";
		str+=$2->getname();
		str+=$3->getname();
		str+=$4->getname();
		str+=$6->getname();
		str+="\n\n";
 		fprintf(logout,"%s",str.c_str());
 		$$->setname(str);		
		
		}
 		;				


parameter_list  : parameter_list COMMA type_specifier ID {fprintf(logout,"At line no: %d parameter_list  : parameter_list COMMA type_specifier ID\n\n",yylineno);
		

		string str=$1->getname();
 		str+=$2->getname();
 		str+=" ";
 		str+=$3->getname();
 		str+=" ";
 		str+=$4->getname();
 		fprintf(logout,"%s\n\n",str.c_str());
 		$$->setname(str);
 		parameter p($3->getname(),$4->getname());
		list.push_back(p);
		}
		| parameter_list COMMA type_specifier {fprintf(logout,"At line no: %d parameter_list  : parameter_list COMMA type_specifier\n\n",yylineno);
		

		string str=$1->getname();
 		str+=$2->getname();
 		str+=" ";
 		str+=$3->getname();
 		fprintf(logout,"%s\n\n",str.c_str());
 		$$->setname(str);
 		parameter p($3->getname());
		list.push_back(p);
		}
 		| type_specifier ID {fprintf(logout,"At line no: %d parameter_list  : type_specifier ID \n\n",yylineno);
		string n=$2->getname();
		string t=$1->getname();
 		string str=$1->getname();
 		str+=" ";
 		str+=$2->getname();
 		fprintf(logout,"%s\n\n",str.c_str());
 		$$->setname(str);
 		parameter p(t,n);
 		
		list.push_back(p);
 		}
		| type_specifier {fprintf(logout,"At line no: %d parameter_list  : type_specifier\n\n",yylineno);
		$$=$1;
		fprintf(logout,"%s\n\n",$1->getname().c_str());
		
		parameter p($1->getname());
		
		list.push_back(p);
		}
 		;

 		
compound_statement : LCURL {table.EnterScope(logout);
			for(int i=0;i<list.size();i++)
			{
				parameter p=list[i];
				if(p.flag==2)
				{
					
					table.Insert("var",0,p.name,p.type,logout);
				}
			}
			list.clear();	
			} statements RCURL {fprintf(logout,"At line no: %d compound_statement : LCURL statements RCURL\n\n",yylineno);
		        string str=$1->getname();
			str+=$3->getname();
			str+=$4->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	
		  	
		    
		    }
 		    | LCURL{table.EnterScope(logout);} RCURL {fprintf(logout,"At line no: %d compound_statement : LCURL RCURL\n\n",yylineno);
 		        string str=$1->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	//table.EnterScope();
		  	
 		    }
 		    ;
 		    
var_declaration : type_specifier declaration_list SEMICOLON 
		{
			fprintf(logout,"At line no: %d var_declaration : type_specifier declaration_list SEMICOLON\n\n",yylineno);

		  	string str=$1->getname();
		  	str+=" ";
			str+=$2->getname();
			str+=$3->getname();
			str+="\n\n";
			fprintf(logout,"%s",str.c_str());
			$$->setname(str);
			//fprintf(logout,"%s",$$->getname().c_str());

			
		} |type_specifier declaration_list error {yyerror("Semicolon required at the end of varibale declaration!"); syntax_error++;}
 		 ;
 		 
type_specifier	: INT {fprintf(logout,"At line no: %d type_specifier: INT\n\n",yylineno); 
			string str=$1->getname();
			fprintf(logout,"%s\n\n",str.c_str()); 
			$$->setname(str);
			$$->setType("int");
			globalType=str;
			}
 		| FLOAT {fprintf(logout,"At line no: %d type_specifier: FLOAT\n\n",yylineno);		
 			string str=$1->getname();
			fprintf(logout,"%s\n\n",str.c_str());
			$$->setname(str); 
			$$->setType("float");
			globalType=str;}
 		| VOID	{fprintf(logout,"At line no: %d type_specifier: VOID\n\n",yylineno);			
 			string str=$1->getname();
			fprintf(logout,"%s\n\n",str.c_str());
			$$->setname(str);
			$$->setType("void");
			globalType=str;}
 		;
		
declaration_list : declaration_list COMMA ID 
		  {
		  	fprintf(logout,"At line no: %d declaration_list : declaration_list COMMA ID\n\n",yylineno);
			
		  	string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	
		  	SymbolInfo *ret=table.Lookup_currentScope($3->getname());
			 if(ret==NULL) 
			 {
			 	
			 	table.Insert("var",0,$3->getname(),globalType,logout);
			 }
			 else
			 {
			 	fprintf(errorFile,"Error at line %d: 1 Multiple declarations of the same variable %s\n\n",yylineno,$3->getname().c_str());
			 	error_count++;
			 }
		  	
		  	
		  }
 		  | declaration_list COMMA ID LTHIRD CONST_INT RTHIRD 
 		  {
 		  	fprintf(logout,"At line no: %d declaration_list : declaration_list COMMA ID LTHIRD CONST_INT RTHIRD\n\n",yylineno);
 		  	string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			str+=$4->getname();
			str+=$5->getname();
			str+=$6->getname();
			fprintf(logout,"%s\n\n",str.c_str());
			$$->setname(str);
			const char *c=$5->getname().c_str();
			int ind=atoi(c);
			 SymbolInfo *ret=table.Lookup_currentScope($3->getname());
			 if(ret==NULL) 
			 {
			 	
			 	table.Insert("arr",ind,$3->getname(),globalType,logout);
			 }
			 else
			 {
			 	fprintf(errorFile,"Error at line %d: 2 Multiple declarations of the same variable %s\n",yylineno,$3->getname().c_str());
			 	error_count++;
			 }
			
		  }
 		  | ID { fprintf(logout,"At line no: %d declaration_list: ID\n\n",yylineno);
 		  	 string str=$1->getname();
			 fprintf(logout,"%s\n\n",str.c_str());
			 //$$=$1;
			 $$->setname(str);
			 SymbolInfo *ret=table.Lookup_currentScope(str);
			 if(ret==NULL) 
			 {
			 	table.Insert("var",0,str,globalType,logout);
			 }
			 else
			 {
			 	fprintf(errorFile,"Error at line %d: 3 Multiple declarations of the same variable %s\n\n",yylineno,str.c_str());
			 	error_count++;
			 }

			 }
 		  | ID LTHIRD CONST_INT RTHIRD {fprintf(logout,"At line no: %d declaration_list : ID LTHIRD CONST_INT RTHIRD \n\n",yylineno);
 		string name=$1->getname();  
 		string str=$1->getname();
		str+=$2->getname();
		str+=$3->getname();
		str+=$4->getname();
		fprintf(logout,"%s\n\n",str.c_str());
		$$->setname(str);
		const char *c=$3->getname().c_str();
		int ind=atoi(c);
		
		SymbolInfo *ret=table.Lookup_currentScope(name);
	        if(ret==NULL) 
		{
			 table.Insert("arr",ind,name,globalType,logout);
		}
		 else
		 {
			 fprintf(errorFile,"Error at line %d: 4 Multiple declarations of the same variable %s\n\n",yylineno,name.c_str());
			 error_count++;
		 }
		}
 		  ;		  
statements : statement {fprintf(logout,"At line no: %d statements : statement\n\n",yylineno);
		  	 string str=$1->getname();
			 fprintf(logout,"%s",str.c_str());
			 $$->setname(str);

}
	   | statements statement {fprintf(logout,"At line no: %d statements : statements statement\n\n",yylineno);
	   	string str=$1->getname();
		str+=$2->getname();
		fprintf(logout,"%s",str.c_str());
		$$->setname(str);
	   }
	   ;
	   
statement : var_declaration {fprintf(logout,"At line no: %d statement : var_declaration\n\n",yylineno);
		  	 string str=$1->getname();
			 fprintf(logout,"%s",str.c_str());
			 $$->setname(str);}
	  | expression_statement {fprintf(logout,"At line no: %d statement : expression_statement \n\n",yylineno);
	  		 string str=$1->getname();
			 fprintf(logout,"%s",str.c_str());
			 $$->setname(str);}
	  | compound_statement {fprintf(logout,"At line no: %d statement : compound_statement\n\n",yylineno);
	  		 string str=$1->getname();
			 fprintf(logout,"%s",str.c_str());
			 $$->setname(str);}
	  | FOR LPAREN expression_statement expression_statement expression RPAREN statement {fprintf(logout,"At line no: %d statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement\n\n",yylineno);
	  	string str=$1->getname();
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 	        str+=$6->getname();
 		str+=$7->getname();
 		str+="\n";
 		fprintf(logout,"%s",str.c_str());
		$$->setname(str);}
	  | IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE{fprintf(logout,"At line no: %d statement : IF LPAREN expression RPAREN statement \n\n",yylineno);	  	
	  	string str=$1->getname();
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 		str+="\n";
 		fprintf(logout,"%s",str.c_str());
		$$->setname(str);}
	  | IF LPAREN expression RPAREN statement ELSE statement {fprintf(logout,"At line no: %d statement : IF LPAREN expression RPAREN statement ELSE statement\n\n",yylineno);
	  	string str=$1->getname();
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 		str+=$6->getname();
 		str+=$7->getname();
 		str+="\n";
 		fprintf(logout,"%s",str.c_str());
		$$->setname(str);}//left!!!
	  | WHILE LPAREN expression RPAREN statement {fprintf(logout,"At line no: %d statement : WHILE LPAREN expression RPAREN statement\n\n",yylineno);
	   	string str=$1->getname();
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 		str+="\n";
 		fprintf(logout,"%s",str.c_str());
		$$->setname(str);	
	  }//left!!!
	  | PRINTLN LPAREN ID RPAREN SEMICOLON {fprintf(logout,"At line no: %d statement : PRINTLN LPAREN ID RPAREN SEMICOLON \n\n",yylineno);
	  	string str=$1->getname();
 		str+=$2->getname();
 		str+=$3->getname();
 		str+=$4->getname();
 		str+=$5->getname();
 		str+="\n";
 		fprintf(logout,"%s",str.c_str());
		$$->setname(str);
	  }//left!!!!
	  | RETURN expression SEMICOLON {fprintf(logout,"At line no: %d statement : RETURN expression SEMICOLON \n\n",yylineno);
	  
	  	string str=$1->getname();
		str+=" ";
 		str+=$2->getname();
 		str+=$3->getname();
 		str+="\n";
 		fprintf(logout,"%s",str.c_str());
		$$->setname(str);
		string t=$2->getType();
		if(t!=func_ret_Type)
		{
		fprintf(errorFile,"Error at line %d: Return expression does not match function return type.\n\n",yylineno);
		error_count++;
		}
		
	  }
	  ;
	  
expression_statement 	: SEMICOLON	{fprintf(logout,"At line no: %d expression_statement 	: SEMICOLON	\n\n",yylineno);
			 string str=$1->getname();
			 fprintf(logout,"%s",str.c_str());
			 $$->setname(str);
			}		
			| expression SEMICOLON {fprintf(logout,"At line no: %d expression_statement 	: expression SEMICOLON\n\n",yylineno);
			string str=$1->getname();
			str+=$2->getname();
			str+="\n\n";
			fprintf(logout,"%s",str.c_str());
			$$->setname(str);}
			;
	  
variable : ID 		{fprintf(logout,"At line no: %d variable : ID \n\n",yylineno);
	fprintf(logout,"%s\n\n",$1->getname().c_str());
	//$$=$1;
	name1=$1->getname();
	SymbolInfo *ret=table.Lookup(name1); 
	if(ret!=NULL){
	type2=ret->getType();
	
	if(ret->indicator=="arr")
	{
		fprintf(errorFile,"Error at line %d: Need array indexing\n\n",yylineno);
		error_count++;
	}
	}
	else 
	{	type2="not specified!!";
		fprintf(errorFile,"Error at line %d: Undeclared variable %s\n\n",yylineno,name1.c_str());
		error_count++;
		
	}
	
	//table.Insert("var",0,$1->getname(),globalType,logout);
	
	//fprintf(errorFile,"Checking here now : %s %s\n\n",name1.c_str(), type2.c_str());
	$$->setname(name1);
	$$->setType(type2);
	
	
	 }
	 | ID LTHIRD expression RTHIRD {fprintf(logout,"At line no: %d variable : ID LTHIRD expression RTHIRD \n\n",yylineno);
	 	name1=$1->getname();
		SymbolInfo *ret=table.Lookup(name1);
	        if(ret!=NULL)
		{
			type2=ret->getType();
			$$->setType(type2);
			string number=$3->getType();
			if(ret->indicator!="arr")
			{
				fprintf(errorFile,"Error at Line %d : No matching array declared for %s\n\n",yylineno,ret->getname().c_str());
				error_count++;
			}
			if(number!="int")
			{
				fprintf(errorFile,"Error at Line %d : Non-integer Array Index\n\n",yylineno);
				error_count++;
			}
		}
		else
		{
			type2="not specified!!";
			$$->setType(type2);
			fprintf(errorFile,"Error at line %d: Undeclared variable %s\n\n",yylineno,name1.c_str());
			error_count++;
		
		}
	 	string str=$1->getname();
		str+=$2->getname();
		str+=$3->getname();
		str+=$4->getname();
		fprintf(logout,"%s\n\n",str.c_str());
		$$->setname(str);
		//fprintf(logout,"HERE:%s\n\n",name1.c_str());
		}
	 //left!!!
	 ;
	 
 expression : logic_expression	{fprintf(logout,"At line no: %d expression : logic_expression	\n\n",yylineno);
 		string t=$1->getType();
	     fprintf(logout,"%s\n\n",$1->getname().c_str());
	      $$->setname($1->getname());
		$$->setType(t);
	 	 }
	   | variable ASSIGNOP logic_expression 
		{fprintf(logout,"At line no: %d expression :  variable ASSIGNOP logic_expression\n\n",yylineno);//= HERE!!!!
		type1=$1->getType();
		type2=$3->getType();
		string str=$1->getname();
		str+=$2->getname();
		str+=$3->getname();
		fprintf(logout,"%s\n\n",str.c_str());
		$$->setname(str);
		//SEMANTIC ERROR GENERATION!!
		if(type1=="int" && type2=="float")
		{
			fprintf(errorFile,"%s %s\n",type1.c_str(),type2.c_str());
			fprintf(errorFile,"Error at line %d : Type Mismatch \n\n",yylineno);
			error_count++;
		}
		else if(type2=="int" && type1=="float")
		{
			fprintf(errorFile,"%s %s\n",type1.c_str(),type2.c_str());
			fprintf(errorFile,"Error at line %d : Type Mismatch \n\n",yylineno);
			error_count++;
		}
		 else if( type2=="void")
     		{
     			     	fprintf(errorFile,"Here: Error at line: %d : Function returns void\n\n",yylineno);
     				error_count++;
     		}
		
		
		}
		
		
	   	
	   ;
			
logic_expression : rel_expression {fprintf(logout,"At line no: %d logic_expression : rel_expression\n\n",yylineno);
		string t=$1->getType();
		//fprintf(errorFile,"rel expression: %s\n\n",t.c_str());
	 	 fprintf(logout,"%s\n\n",$1->getname().c_str());
	 	 $$->setname($1->getname());
 		 $$->setType(t);
 		 //fprintf(errorFile,"rel expression: %s\n\n",$$->getType().c_str());
	 	 
	 	 }	
		 | rel_expression LOGICOP rel_expression {fprintf(logout,"At line no: %d logic_expression : rel_expression LOGICOP rel_expression \n\n",yylineno);
		 	string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
			$$->setType("int");
		        type3=$1->getType();
			type4=$3->getType();
		        if(type3=="void"||type4=="void")
		  	{
		  		fprintf(errorFile,"Error at line: %d : Void return type.\n\n",yylineno);
		  	}

}	
		 ;
			
rel_expression	: simple_expression {fprintf(logout,"At line no: %d rel_expression	: simple_expression \n\n",yylineno);

		//fprintf(errorFile,"simple expression: %s\n\n",$1->getType().c_str());
	 	 fprintf(logout,"%s\n\n",$1->getname().c_str());
	 	 $$->setname($1->getname());
	 	 $$->setType($1->getType());
	 	 
		}
		| simple_expression RELOP simple_expression {fprintf(logout,"At line no: %d rel_expression	:  simple_expression RELOP simple_expression \n\n",yylineno);
		        type3=$1->getType();
			type4=$3->getType();
			
			$$->setType("int");
		        if(type3=="void"||type4=="void")
		  	{
		  		fprintf(errorFile,"Error at line: %d : Void return type.\n\n",yylineno);
		  	}


			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	
		}	
		;
				
simple_expression : term {fprintf(logout,"At line no: %d simple_expression : term \n\n",yylineno);
//fprintf(errorFile,"term: %s\n\n",$1->getType().c_str());
	fprintf(logout,"%s\n\n",$1->getname().c_str());	
	$$->setname($1->getname());
	$$->setType($1->getType());
	}
		  | simple_expression ADDOP term {fprintf(logout,"At line no: %d simple_expression : simple_expression ADDOP term \n\n",yylineno);
		 	type3=$1->getType();
			type4=$3->getType();
			if(type3=="float"||type4=="float")
			{
				$$->setType("float");
			}
			else if(type3=="int" && type4=="int")
			{
				$$->setType("int");
			}
			else if(type3=="void" || type4=="void")
     			{
     			     	//fprintf(errorFile,"Error at line: %d : Function returns void\n\n",yylineno);
				$$->setType("void");
     				//error_count++;
     			}
			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);


	 	 }
		  ;
					
term :	unary_expression {fprintf(logout,"At line no: %d term : unary_expression \n\n",yylineno);
//fprintf(errorFile,"unary expression: %s\n\n",$1->getType().c_str());
	fprintf(logout,"%s\n\n",$1->getname().c_str());	
	$$->setname($1->getname());
	$$->setType($1->getType());	
	}
     |  term MULOP unary_expression {
     		type3=$1->getType();
		type4=$3->getType();
     		string mod=$2->getname();
     		
     		//fprintf(errorFile,"%s%s%s\n\n",type3.c_str(),mod.c_str(),type4.c_str());
     		if(type3=="void" || type4=="void")
     		{
     			     	//fprintf(errorFile,"Error at line: %d : Function returns void\n\n",yylineno);
     				//error_count++;
     				$$->setType("void");
     		}
     		else{
     		if(mod=="%")
     		{
     			if(type3=="int" && type4=="float")
     			{
     				fprintf(errorFile,"Error at line: %d : Integer operand on modulus operator\n\n",yylineno);
     				error_count++;
     			}
     			else if(type4=="int" && type3=="float")
     			{
     				fprintf(errorFile,"Error at line: %d : Integer operand on modulus operator\n\n",yylineno);
     				error_count++;
     			}
     			else if(type4=="float" && type3=="float")
     			{
     				fprintf(errorFile,"Error at line: %d : Integer operand on modulus operator\n\n",yylineno);
     				error_count++;
     			}
			$$->setType("int");
     		}
     		
		else if(mod=="*")
		{	if(type3=="float"||type4=="float")
			{
				$$->setType("float");
			}
			else if(type3=="int" && type4=="int")
			{
				$$->setType("int");
			}
			
     		}
     		}
		fprintf(logout,"At line no: %d term :  term MULOP unary_expression \n\n",yylineno);
     			
     			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
     
     }
     ;

unary_expression : ADDOP unary_expression  {fprintf(logout,"At line no: %d unary_expression : ADDOP unary_expression\n\n",yylineno);
			string str=$1->getname();
			str+=$2->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	
		  	$$->setType($2->getType());
		  	if($2->getType()=="void")
		  	{
		  		//fprintf(errorFile,"Error at line: %d : 3 Function returns void.\n\n",yylineno);
		  		$$->setType("void");
		  		//error_count++;
		  	}
		  	}
		 | NOT unary_expression {fprintf(logout,"At line no: %d unary_expression : NOT unary_expression\n\n",yylineno);
		 	string str=$1->getname();
			str+=$2->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	$$->setType($2->getType());
		  	if($2->getType()=="void")
		  	{
		  		//fprintf(errorFile,"Error at line: %d : Function returns void.\n\n",yylineno);
		  		$$->setType("void");
		  		//error_count++;
		  	}
		  	}
		 | factor {fprintf(logout,"At line no: %d unary_expression : factor\n\n",yylineno);
		 //fprintf(errorFile,"factor: %s\n\n",$1->getType().c_str());
		 	fprintf(logout,"%s \n\n",$1->getname().c_str());
		 	//$$=$1;
		 	$$->setname($1->getname());
		 	$$->setType($1->getType());
		 	
		 	}
		 ;
	
factor	: variable {fprintf(logout,"At line no: %d factor : variable\n\n",yylineno);
		//fprintf(errorFile,"variable: %s\n\n",$1->getType().c_str());
	fprintf(logout,"%s\n\n",$1->getname().c_str());	
	//$$=$1;
	$$->setname($1->getname());
	//SymbolInfo *ret=table.Lookup_currentScope(name1); type2=ret->getType();
	$$->setType(type2);
		}
	| ID LPAREN argument_list RPAREN {fprintf(logout,"At line no: %d factor : ID LPAREN argument_list RPAREN\n\n",yylineno);
			string name2=$1->getname();
			SymbolInfo *ret=table.Lookup(name2); 
			if(ret!=NULL)
			{
				type2=ret->getType();
				$$->setType(type2);
				//fprintf(errorFile,"%s\n\n",type2.c_str());
				if(ret->indicator=="var" )
				{
					fprintf(errorFile,"Error at line %d: No matching function found, %s is a variable\n\n",yylineno, name2.c_str());
					error_count++;
				}
				else if(ret->indicator=="arr" )
				{
					fprintf(errorFile,"Error at line %d: No matching function found, %s is an array.\n\n",yylineno,name2.c_str());
					error_count++;
				}
				
				else if(ret->indicator=="func" && ret->func_dec_def=="dec")
				{
					fprintf(errorFile,"Error at line %d: Function definition required\n\n",yylineno);
					error_count++;
				}
				else if(ret->indicator=="func" && ret->func_dec_def=="def")
				{
					vector <parameter> list3=ret->parameterList;
					//fprintf(errorFile,"Checking here: %d %d\n\n",list3.size(),arg_type_list.size());
					if(list3.size()!=arg_type_list.size())
					{
						fprintf(errorFile,"Error at line %d: Function call does not match function definition, incompatible number of parameters.\n\n",yylineno);
						error_count++;
					}
					else{
					//
					for(int i=0;i<arg_type_list.size();i++)
					{
						//fprintf(errorFile,"Checking: %s %s\n\n",list3[i].type.c_str(),arg_type_list[i].c_str());
						if(arg_type_list[i]!=list3[i].type)
						{
							//fprintf(errorFile,"%s\n\n",arg_type_list[i].c_str());
							fprintf(errorFile,"Error at line %d: Arguments do not match function declaration, incompatible parameter types\n\n",yylineno);
							error_count++;
						}
					}
					}
				}
			}
			else
			{
				$$->setType("not specified\n\n");
				fprintf(errorFile,"Error at line %d: Undeclared function\n\n",yylineno);
				error_count++;
			}
			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			str+=$4->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	
		  
		  	
		  	
		  	
		  	}
	|ID LPAREN RPAREN{ fprintf(logout,"At line no: %d factor : ID LPAREN RPAREN\n\n",yylineno);
string name2=$1->getname();
			SymbolInfo *ret=table.Lookup(name2); 
			if(ret!=NULL)
			{
				type2=ret->getType();
				$$->setType(type2);
				//fprintf(errorFile,"%s\n\n",type2.c_str());
				if(ret->indicator=="var" )
				{
					fprintf(errorFile,"Error at line %d: No matching function found, %s is a variable\n\n",yylineno, name2.c_str());
					error_count++;
				}
				else if(ret->indicator=="arr" )
				{
					fprintf(errorFile,"Error at line %d: No matching function found, %s is an array.\n\n",yylineno,name2.c_str());
					error_count++;
				}
				
				else if(ret->indicator=="func" && ret->func_dec_def=="dec")
				{
					fprintf(errorFile,"Error at line %d: Function definition required\n\n",yylineno);
					error_count++;
				}
				else if(ret->indicator=="func" && ret->func_dec_def=="def")
				{
					vector <parameter> list3=ret->parameterList;
					//fprintf(errorFile,"Checking here: %d \n\n",list3.size());
					if(list3.size()!=0)
					{
						fprintf(errorFile,"Error at line %d: Function call does not match function definition, incompatible number of parameters.\n\n",yylineno);
						error_count++;
					}
				}
			}
			else
			{
				$$->setType("not specified\n\n");
				fprintf(errorFile,"Error at line %d: Undeclared function\n\n",yylineno);
				error_count++;
			}
			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	
		  
		  	
		  	
}	
	
	| LPAREN expression RPAREN {fprintf(logout,"At line no: %d factor : LPAREN expression RPAREN\n\n",yylineno);
			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	$$->setType($2->getType());
			}
	| CONST_INT {fprintf(logout,"At line no: %d factor : CONST_INT\n\n",yylineno);
	fprintf(logout,"%s\n\n",$1->getname().c_str());
	$$=$1;
	$$->setType("int");
	}
	| CONST_FLOAT {fprintf(logout,"At line no: %d factor	: CONST_FLOAT \n\n",yylineno);
         fprintf(logout,"%s\n\n",$1->getname().c_str());	
	$$=$1;
	$$->setType("float");
	}
	| variable INCOP {fprintf(logout,"At line no: %d factor : variable INCOP \n\n",yylineno);
			
			string str=$1->getname();
			str+=$2->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	$$->setType(type2);
		  	
		  	
		  	

		  	}
	| variable DECOP {fprintf(logout,"At line no: %d factor : variable DECOP\n\n",yylineno);
			string str=$1->getname();
			str+=$2->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	$$->setType(type2);
		  	
}
	;
	
argument_list : arguments {fprintf(logout,"At line no: %d argument_list : arguments\n\n",yylineno);
		string str=$1->getname();
		fprintf(logout,"%s\n\n",str.c_str());
		$$->setname(str);
		};
			  
	
arguments : arguments COMMA logic_expression {fprintf(logout,"At line no: %d arguments : arguments COMMA logic_expression \n\n",yylineno);
			string t=$1->getType();
			string str=$1->getname();
			str+=$2->getname();
			str+=$3->getname();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	arg_type_list.push_back(t);
		  	}
	      | logic_expression {fprintf(logout,"At line no: %d arguments : logic_expression \n\n",yylineno);
	      		string str=$1->getname();
	      		string t=$1->getType();
			fprintf(logout,"%s\n\n",str.c_str());
		  	$$->setname(str);
		  	arg_type_list.clear();
		  	arg_type_list.push_back(t);
		  	}
	      ;
 

%%
int main(int argc,char *argv[])
{

	if((fp=fopen(argv[1],"r"))==NULL)
	{
		printf("Cannot Open Input File.\n");
		exit(1);
	}

	
	logout= fopen("log.txt","w");

	errorFile= fopen("error.txt","w");
	
	yyin=fp;
	yyparse();

	//fprintf(logout,"Total Lines: %d\nTotal Errors: %d\n",line_count,error_count);
	//table.PrintCurrentScopeTable();
	fprintf(logout,"Total Lines:%d\n\n",yylineno);
	fprintf(logout,"Total Semantic Errors:%d\n\n",error_count);
	fprintf(errorFile,"Total Semantic Errors:%d\n\n",error_count);
	fprintf(errorFile,"Total Syntax Errors:%d\n\n",syntax_error);
	fclose(yyin);
	fclose(errorFile);
	fclose(logout);
	return 0;
	
}



