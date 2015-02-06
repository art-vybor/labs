%option noyywrap bison-bridge bison-locations

%{

#include <stdio.h>
#include <stdlib.h>

#define TAG_STRING 1
#define TAG_NUMBER 2
#define TAG_LBRACE 3
#define TAG_RBRACE 4
#define TAG_LBRACKET 5
#define TAG_RBRACKET 6
#define TAG_SEMICOLON 7
#define TAG_IDENT  8
#define TAG_EQUAL 9
#define TAG_COMMA 10

char *tag_names[] = 
{
    "END_OF_PROGRAM", "STRING", "NUMBER",
    "LBRACE", "RBRACE", "LBRACKET", "RBRACKET",
    "SEMICOLON", "IDENT", "EQUAL", "COMMA" 
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
NUMBER {DIGIT}+
SEMICOLON \;
LBRACE "{"
RBRACE "}"
LBRACKET "("
RBRACKET ")"
EQUAL "="
COMMA ","
IDENT {LETTER}({LETTER}|{DIGIT})*

%x STRING

%%

[\n\t ]+

\"                              {
                                    BEGIN (STRING);
                                    continued = 1;
                                }
<STRING>[^\"]*    {
                                    yylval->string = yytext;
                                    continued = 1;
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

{IDENT}                         {
                                    yylval->string = yytext;
                                    return TAG_IDENT;
                                }

{SEMICOLON}                     return TAG_SEMICOLON;
{LBRACE}                        return TAG_LBRACE;
{RBRACE}                        return TAG_RBRACE;
{LBRACKET}                      return TAG_LBRACKET;
{RBRACKET}                      return TAG_RBRACKET;
{EQUAL}                         return TAG_EQUAL;
{COMMA}                         return TAG_COMMA;

.                               {
                                    char s[20];
                                    sprintf(s, "unexpected symbol %s", yytext);
                                    err(s);
                                }

%%

//#define PROGRAM "123\n $D+EAD123 abc1$1 $ \n\"sa\"\"dhghg \\\nasd\" \"a\n\""
/*
int main()
{
    //read PROGRAM

    char *PROGRAM;
    long file_size;
    FILE *file = fopen("test.java", "rb");
        fseek(file, 0, SEEK_END);
        file_size = ftell(file);
        rewind(file);
        PROGRAM = malloc((file_size+1) * (sizeof(char)));
        fread(PROGRAM, sizeof(char), file_size, file);
    fclose(file);

    puts(PROGRAM);

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

            if (tag == TAG_NUMBER || tag == TAG_IDENT || tag == TAG_STRING)
                printf("%s", value.string);

            printf("\n");
        }
    }
    while (tag != 0);

    return 0;
}*/