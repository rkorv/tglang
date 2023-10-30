%{

using namespace std;
#include "../src/commun.h"
#include <iostream>
#include <cstring>
#include <stack>

#define YYERROR_VERBOSE

//int yywrap(void);
void yyerror(DocumentXML *doc, char const *msg);
int yylex(void);

extern int xmllineno;

stack<string> nodesStack;

int err = 0;

%}

%parse-param {DocumentXML * documentXML}

%union {
   char * s;
   NodeList * nl;
   Data * d;
   list<Node*> * listN;
   DocumentXML * doc;
   map<string,string> * m;
   ElementName * en;  /* le nom d'un element avec son namespace */
}

%token EQ SLASH CLOSE CLOSESPECIAL DOCTYPE
%token <s> ENCODING STRING DATA COMMENT IDENT NSIDENT
%token <en> NSSTART START STARTSPECIAL END NSEND
%type <nl> xml_element start
%type <doc> document
%type <m> attributs_opt
%type <s> declarations_opt declaration attributs_sp_opt
%type <listN> content_opt close_content_and_end empty_or_content

%%

document
 : misc_seq_opt special_dec_opt misc_seq_opt declarations_opt misc_seq_opt xml_element misc_seq_opt
    {
      $$ = documentXML;
      $$->setActiveRootNode(*$6);
      if(documentXML->dtdNameIsSet == false) {
        $$->dtd = $4;
        $$->dtdNameIsSet = true;
      };
    };

special_dec_opt
 : STARTSPECIAL attributs_sp_opt CLOSESPECIAL
   {
    if(strcmp($1->second.c_str(), "?xml-stylesheet") == 0) {
      if(documentXML->xslNameIsSet == false) {
        documentXML->xsl = $2;
        documentXML->xslNameIsSet = true;
      }
    };
   }
 | /*empty*/
 ;

attributs_sp_opt
 : attributs_sp_opt IDENT EQ STRING
   {
    if(strcmp($2,"href") == 0) {
      $$ = $4;
    };
   }
 | {/* empty */};

misc_seq_opt
 : misc_seq_opt COMMENT
 | /*empty*/
 ;

declarations_opt
 : declaration {$$ = $1;}
 | /*empty*/ {$$ = NULL;}
 ;
 
declaration
 : DOCTYPE IDENT IDENT STRING CLOSE {$$ = $4;}
 ;

xml_element
 : start attributs_opt empty_or_content
   {
    $$ = $1; $$->attributes = *$2;
    if($3 != NULL) {
      $$->isAutoClosing = false;
      $$->setChildNodeList(*$3);
      $$->childNodeList = *$3;
    } else {
      $$->isAutoClosing = true;
      nodesStack.pop();
    }
   }
   | start error CLOSE
   {
     //printf("reprise erreur\n");
     nodesStack.pop();
     err++;
   };


start
 : START
   {
    $$ = new NodeList();
    $$->tagName = $1->second;
    $$->nameSpace = $1->first;
    nodesStack.push($$->tagName);
    //cout << "push  " << nodesStack.top() << endl;
   }
 | NSSTART
 {
  $$ = new NodeList();
  $$->tagName = $1->second;
  $$->nameSpace = $1->first;
  nodesStack.push($$->nameSpace + ":" + $$->tagName);
  //cout << "push  " << nodesStack.top() << endl;
 };

empty_or_content
 : SLASH CLOSE {$$ = NULL;}
 | close_content_and_end CLOSE {$$ = $1;}
 ;

close_content_and_end
 : CLOSE content_opt END
  {
    if($3->second != nodesStack.top()) {
      yyerror(NULL, string("Balise fermante non correspondante !! : " + $3->second + " au lieu de " + nodesStack.top()).c_str());
      //return 1;
      YYERROR;
      $$ = $2;
      nodesStack.pop();
    } else {
      $$ = $2;
      nodesStack.pop();
    }
  }
 | CLOSE content_opt NSEND
 {
   if($3->first + ":" + $3->second != nodesStack.top().c_str()) {
     yyerror(NULL, string("Balise fermante non correspondante !! : " + $3->first + ":" + $3->second + " au lieu de " + nodesStack.top()).c_str());
     //return 1;
     YYERROR;
     $$ = $2;
     nodesStack.pop();
   } else {
     $$ = $2;
     nodesStack.pop();
   }
 };

attributs_opt
 : attributs_opt IDENT EQ STRING {$$ = $1; (*$$)[$2] = $4;}
 | /*empty*/ {$$ = new map<string,string>;}
 ;

content_opt 
 : content_opt DATA    {$$ = $1; Data* temp = new Data; temp->value = string($2); $$->push_back((Node*)temp); free($2);} //TODO: Check cast
 | content_opt COMMENT {$$ = $1;}
 | content_opt xml_element  {$$ = $1; $$->push_back($2);} //TODO: cast?
 | /*empty*/ {$$ = new list<Node*>;}
 ;

%%

void xmlrestart(FILE * );

int parseXMLFile(char * file, DocumentXML * documentXML)
{
  
  //yydebug = 1; // pour enlever l'affichage de l'éxécution du parser, commenter cette ligne

  printf("Trying to Parse %s\n", file);
  FILE * f;
  if((f = fopen(file, "r")) == NULL)
  {
    fprintf(stderr, "ERROR: No file named %s\n", file);
    exit(-1);
  }
  xmlrestart(f);
   xmlparse(documentXML);
  fclose(f);

  if(nodesStack.size() != 0){
    err += 1;
    cout << "Il reste des balises non fermees !!" << endl;
  }
  
  if (err != 0) printf("Parse ended with %d error(s)\n", err);
    else  printf("Parse ended with success\n");
  
  return err;
}

/*int yywrap(void)
{
  return 1;
}*/

void yyerror(DocumentXML * doc, char const *msg)
{
  fprintf(stderr, "Error at line : %d : %s\n", xmllineno, msg);
}

