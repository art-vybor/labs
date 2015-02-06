%{
#include <stdio.h>
#include "y.tab.h"
%}

LETTER [a-zA-Z]
DIGIT [0-9]
NUMBER {DIGIT}+
IDNT {LETTER}({LETTER}|{DIGIT})*

%x STR

%%

[\n\t ]+
{DIGIT}+        yylval.string = yytext; return NUMBER;
\;              return SEMICOLON;
\{              return LBRACE;
\}              return RBRACE;
\(              return LBRACKET;
\)              return RBRACKET;
\=              return EQUAL;
\,              return COMMA;
{IDNT}          yylval.string = yytext;return IDENT;
\"              BEGIN(STR);
<STR>[^\"]*     yylval.string=strdup(yytext);
<STR>\"         BEGIN(0); return STRING;
%%
