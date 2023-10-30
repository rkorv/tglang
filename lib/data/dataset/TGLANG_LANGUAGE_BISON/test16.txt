%{

using namespace std;
#include <cstring>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include "commun.h"
#include "element.hpp"
#include "text_node.hpp"
#include "xml.tab.h"
#include "dtd.h"
#include "xmlparse.h"

int xmlwrap(void);
void xmlerror(char *msg);
int xmllex(void);

/// Cette variable globale va recevoir le nom de la DTD, pour initier l'analyse
/// du fichier référencer dans le fichier xml.
std::string dtd_name;

xml::Document* document_ = 0;
xml::Element* current_ = 0;

%}

%union {
   char * s;
   ElementName * en;  /* le nom d'un element avec son namespace */
}

%token EQ SLASH CLOSE END CLOSESPECIAL DOCTYPE
%token <s> ENCODING VALUE DATA COMMENT NAME NSNAME 
%token <en> NSSTART STARTSPECIAL START 

%%

document
 : declarations element misc_seq_opt 
 ;
misc_seq_opt
 : misc_seq_opt misc
 | /*empty*/
 ;
misc
 : COMMENT		
 ;

declarations
 : declaration
 | /*empty*/
 ;
 
declaration
 /* Déclaration de la DTD trouvée : le 4e token est le chemin de la DTD.
  * Il faut maintenant valider la DTD à l'aide de la fonction handle_dtd
  * L'analyse du document XML continue après l'analyse de la DTD.
  */
 : DOCTYPE NAME NAME VALUE CLOSE
{
	dtd_name = $4;
	// create doctype before parsing dtd cause dtd parser relies on doctype
	document_->setDoctype(new xml::Doctype(dtd_name));
	handle_dtd(dtd_name);
}
 ;

element
 : start attributes empty_or_content 
 | start empty_or_content 
 ;

start
 : START	{
cout << "$1:" << $1 << ":" << endl;
 xml::Element * node = new xml::Element(current_, $1->second);
if(current_ == 0)
{
  document_->setRoot(node);
}
else
{
	current_->appendChild(node);
}
  current_ = node; 
}
	
 | NSSTART {
cerr << "not implemented yet" << endl;

exit(EXIT_FAILURE);
 //xml::Element * node = new xml::Element(current_, $1);
//if(current_ == 0) { cerr << __LINE__ << endl; document_->setRoot(node); }
//current_->appendChild(node); current_ = node; 
}

 ;

empty_or_content
 : SLASH CLOSE	
 | close_content_and_end name_or_nsname_opt CLOSE 
 ;

name_or_nsname_opt
 : NAME   
 | NSNAME  
 | /* empty */
 ;
close_content_and_end
 : CLOSE content END 
 {
  current_ = current_->parent(); 
 }
 ;
content 
 : content DATA	
{
  xml::TextNode * node = new xml::TextNode(current_, $2);
  current_->appendChild(node);
}
 | content misc
 | content element
 | /*empty*/
 ;

attributes
: attributes attribut 
| attribut
;

attribut
: NAME EQ VALUE { current_->addAttribute(new xml::Attribute($1, $3));}
;
%%

// Cette fonction permet de pouvoir parser plusieurs fichiers
int xmlwrap(void)
{
  return 1;
}

void xmlerror(char *msg)
{
  fprintf(stderr, "%s\n", msg);
}

