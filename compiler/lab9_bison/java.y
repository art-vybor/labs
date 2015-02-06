%{
#include <stdio.h>
#include <string.h>

int yydebug=1;

void yyerror(const char *str) {
    fprintf(stderr, "error %s\n", str);
}

int yywrap() {
    return 1;
}

main() {
    yyparse();
}

int tab = 0;

void print_tab() {
    int n = tab;
    printf("\n");
    while (n > 0) {
        printf(" ");
        n--;
    }
}

%}

%token LBRACE RBRACE LBRACKET RBRACKET
%token SEMICOLON COMMA EQUAL

%union
{
    char *string;
}

%token <string> STRING NUMBER IDENT

%%

class:
    ident ident lbrace rows rbrace

rows:
    row
    | rows row

row: 
    ident ident ident ident row_suffix

row_suffix:
    equal value semicolon
    | lbracket args rbracket lbrace rbrace

value:
    string
    | number

args:
    |arg
    | args comma arg

arg:
    ident ident

//------------------
//------print-------
//------------------

ident:
    IDENT
    {
        printf("%s ", $1);
        
    }

string:
    STRING {
        printf("%s ", $1);
    }

lbrace:
    LBRACE {
        printf("{");
        tab += 4;
        print_tab();
    }

rbrace:
    RBRACE {
        printf("\b\b\b\b}");
        tab -= 4;
        print_tab();
    }

lbracket:
    LBRACKET {
        printf("( ");
    }

rbracket:
    RBRACKET {
        printf("\b) ");
    }

number:
    NUMBER {
        printf("%s ", $1);
    }

comma:
    COMMA {
        printf("\b, ");
    }

semicolon:
    SEMICOLON {
        printf("\b;");
        print_tab();
    }

equal:
    EQUAL {
        printf("= ");
    }