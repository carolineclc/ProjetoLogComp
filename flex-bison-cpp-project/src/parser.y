%{
#include "ast.h"   // This must come BEFORE the %union!
#include <cstdio>
#include <cstdlib>
void yyerror(const char *s);
int yylex(void);
Node* root = nullptr;
%}

%union {
    int intval;
    float floatval;
    char* strval;
    Node* node;
}

%token PRINTLOG BREAK IF ELSE WHILE SCANF SQRT SIN COS TAN LOG EXP POW PI
%token INT_TYPE FLOAT_TYPE STR_TYPE BOOL_TYPE STOP START FINISH NAME ID_KW STATION SPEED REGION ROTATION
%token INT FLOAT STRING IDENTIFIER
%token EQUAL ARROW ASSIGNMENT AND OR NOT GT LT PLUS MINUS MULT DIV LP RP LCB RCB SC C COMMA

%type <node> program

%%

program:
    /* Minimal rule for now */
    /* You should expand this with your language's grammar */
    { root = nullptr; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}