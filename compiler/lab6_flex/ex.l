%option noyywrap bison-bridge bison-locations

%{

#include <stdio.h>
#include <stdlib.h>

#define TAG_STRING 1
#define TAG_NUMBER 2
#define TAG_HEXNUMBER 3
#define TAG_IDENT  4



char *tag_names[] = 
{
    "END_OF_PROGRAM", "STRING", "NUMBER",
    "HEXNUMBER", "IDENT"
};


struct Position
{
    int line, pos, index;
};

void print_pos(struct Position *p)
{
    printf("(%d, %d)", p->line, p->pos);
}

struct Fragment
{
    struct  Position starting, following;
};

typedef struct Fragment YYLTYPE;

void print_frag(struct Fragment *f)
{
    print_pos(&(f->starting));
    printf("-");
    print_pos(&(f->following));
    printf(": ");
}

union Token
{
    char *string;
};

typedef union Token YYSTYPE;

int continued ;
struct Position cur ;

# define YY_USER_ACTION                    \
    {                                       \
        int i ;                             \
        if (!continued)                   \
           yylloc -> starting = cur ;      \
        continued = 0;                      \
                                            \
        for ( i = 0; i < yyleng ; i++)     \
        {                                   \
            if ( yytext[i] == '\n')     \
            {                               \
                cur.line++;              \
                cur.pos = 1;              \
            }                               \
            else                            \
                cur.pos++;               \
            cur.index++;                 \
        }                                   \
        yylloc -> following = cur ;        \
    }                                       \


void init_scanner(char *program)
{
    continued = 0;
    cur.line = 1;
    cur.pos = 1;
    cur.index = 0;
    yy_scan_string(program);
}

void err(char *msg)
{
    printf("ERROR ");
    print_pos(&cur);
    printf(": %s\n", msg);
}

%}

LETTER [a-zA-Z]
DIGIT [0-9]
HEXDIGIT [A-Fa-f0-9]
NUMBER {DIGIT}+
HEXNUMBER [$]{HEXDIGIT}+
IDENT {LETTER}([$]|{LETTER}|{DIGIT})*

%x STRING

%%

[\n\t ]+

\"                              {
                                    BEGIN (STRING);
                                    continued = 1;
                                }
<STRING>([^\"\n]|\"\"|\\\n)*    {
                                    yylval->string = malloc(strlen(yytext));
                                    strcpy(yylval->string, yytext);
                                    char *ptr;
                                    while (ptr = strstr(yylval->string, "\"\""))
                                        strcpy(ptr,ptr+1);

                                    while (ptr = strstr(yylval->string, "\\\n"))
                                        strcpy(ptr,ptr+2);

                                    continued = 1;
                                }
<STRING>\n                      {
                                    err("Incorrect \\n in STRING.");
                                    BEGIN(0);
                                }
<STRING>\"                      {
                                    BEGIN(0);
                                    return TAG_STRING;
                                }
<STRING><<EOF>>                 {
                                    err("End of program found, \" expected");
                                    return 0;
                                }

{NUMBER}                        {
                                    yylval->string = yytext;
                                    return TAG_NUMBER;
                                }

{HEXNUMBER}                     {
                                    yylval->string = (yytext+1);
                                    return TAG_HEXNUMBER;
                                }

{IDENT}                         {
                                    yylval->string = yytext;
                                    return TAG_IDENT;
                                }
.                               {
                                    char s[20];
                                    sprintf(s, "unexpected symbol %s", yytext);
                                    err(s);
                                }

%%

#define PROGRAM "123\n $D+EAD123 abc1$1 $ \n\"sa\"\"dhghg \\\nasd\" \"a\n\""

int main()
{
    int tag;
    YYSTYPE value;
    YYLTYPE coords;

    init_scanner(PROGRAM);

    do
    {
        tag = yylex(&value, &coords);
        if (tag != 0)
        {
            printf("%s ", tag_names[tag]);
            print_frag(&coords);

            printf(": ");

            if (tag == TAG_NUMBER || tag == TAG_IDENT || tag == TAG_STRING)
                printf("%s", value.string);
            else if (tag == TAG_HEXNUMBER) 
                printf("0x%s", value.string);

            printf("\n");
        }
    }
    while (tag != 0);

    return 0;
}