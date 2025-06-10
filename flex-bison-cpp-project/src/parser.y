%{
#include <iostream>
#include <string>
#include <memory>
#include "lexer.h" // Flex header

// Forward declarations for AST nodes (implement separately)
class Node;
using NodePtr = std::shared_ptr<Node>;
NodePtr make_binop(const std::string&, NodePtr, NodePtr);
NodePtr make_unop(const std::string&, NodePtr);
NodePtr make_int(int);
NodePtr make_float(float);
NodePtr make_string(const std::string&);
NodePtr make_identifier(const std::string&);
NodePtr make_print(NodePtr);
NodePtr make_assignment(NodePtr, NodePtr);
NodePtr make_block();
NodePtr make_vardec(const std::string&, std::vector<NodePtr>);
NodePtr make_if(NodePtr, NodePtr, NodePtr);
NodePtr make_while(NodePtr, NodePtr);
NodePtr make_start(std::vector<NodePtr>);
NodePtr make_stop(std::vector<NodePtr>);
NodePtr make_finish(std::vector<NodePtr>);
NodePtr make_read();
void yyerror(const char* s);
int yylex();
%}

%union {
    int intval;
    float floatval;
    char* strval;
    NodePtr node;
    std::vector<NodePtr>* nodelist;
}

%token <intval> INT
%token <floatval> FLOAT
%token <strval> STRING
%token <strval> IDENTIFIER

%token PRINTLOG BREAK IF ELSE WHILE SCANF SQRT SIN COS TAN LOG EXP POW PI
%token INT_TYPE FLOAT_TYPE STR_TYPE BOOL_TYPE
%token STOP START FINISH NAME ID_KW STATION SPEED REGION ROTATION

%token ASSIGNMENT EQUAL ARROW AND OR NOT GT LT
%token PLUS MINUS MULT DIV
%token LP RP LCB RCB SC C COMMA

%type <node> program block statement expression relative_expression term factor
%type <nodelist> statement_list

%%

program
    : block { /* Evaluate or process AST here */ }
    ;

block
    : LCB statement_list RCB { /* $$ = make_block($2); */ }
    ;

statement_list
    : /* empty */ { $$ = new std::vector<NodePtr>(); }
    | statement_list statement { /* $$ = $1; $1->push_back($2); */ }
    ;

statement
    : SC { /* $$ = nullptr; */ }
    | BREAK SC { /* $$ = nullptr; */ }
    | type ARROW IDENTIFIER assignment_list SC { /* $$ = make_vardec($1, ...); */ }
    | IDENTIFIER ASSIGNMENT expression SC { /* $$ = make_assignment(make_identifier($1), $3); */ }
    | START LP ID_KW C relative_expression COMMA STATION C relative_expression COMMA REGION C relative_expression RP SC
        { /* $$ = make_start({$5, $9, $13}); */ }
    | STOP LP NAME C relative_expression COMMA SPEED C relative_expression COMMA ROTATION C relative_expression RP SC
        { /* $$ = make_stop({$5, $9, $13}); */ }
    | FINISH LP ID_KW C relative_expression COMMA STATION C relative_expression COMMA REGION C relative_expression RP SC
        { /* $$ = make_finish({$5, $9, $13}); */ }
    | PRINTLOG LP relative_expression RP SC { /* $$ = make_print($3); */ }
    | WHILE LP relative_expression RP statement { /* $$ = make_while($3, $5); */ }
    | IF LP relative_expression RP statement else_clause { /* $$ = make_if($3, $5, $6); */ }
    | block { /* $$ = $1; */ }
    ;

else_clause
    : /* empty */ { /* $$ = nullptr; */ }
    | ELSE statement { /* $$ = $2; */ }
    ;

type
    : INT_TYPE { /* $$ = "int"; */ }
    | FLOAT_TYPE { /* $$ = "float"; */ }
    | STR_TYPE { /* $$ = "str"; */ }
    | BOOL_TYPE { /* $$ = "bool"; */ }
    ;

assignment_list
    : /* empty */ { /* ... */ }
    | assignment_list COMMA ARROW IDENTIFIER assignment { /* ... */ }
    ;

assignment
    : ASSIGNMENT expression { /* ... */ }
    | /* empty */ { /* ... */ }
    ;

relative_expression
    : expression
      { /* $$ = $1; */ }
    | relative_expression EQUAL expression
      { /* $$ = make_binop("==", $1, $3); */ }
    | relative_expression GT expression
      { /* $$ = make_binop(">", $1, $3); */ }
    | relative_expression LT expression
      { /* $$ = make_binop("<", $1, $3); */ }
    ;

expression
    : term
      { /* $$ = $1; */ }
    | expression PLUS term
      { /* $$ = make_binop("+", $1, $3); */ }
    | expression MINUS term
      { /* $$ = make_binop("-", $1, $3); */ }
    | expression OR term
      { /* $$ = make_binop("||", $1, $3); */ }
    ;

term
    : factor
      { /* $$ = $1; */ }
    | term MULT factor
      { /* $$ = make_binop("*", $1, $3); */ }
    | term DIV factor
      { /* $$ = make_binop("/", $1, $3); */ }
    | term AND factor
      { /* $$ = make_binop("&&", $1, $3); */ }
    ;

factor
    : INT { /* $$ = make_int($1); */ }
    | FLOAT { /* $$ = make_float($1); */ }
    | STRING { /* $$ = make_string($1); */ }
    | PLUS factor { /* $$ = make_unop("+", $2); */ }
    | MINUS factor { /* $$ = make_unop("-", $2); */ }
    | NOT factor { /* $$ = make_unop("!", $2); */ }
    | LP relative_expression RP { /* $$ = $2; */ }
    | SQRT LP expression RP { /* $$ = ...; */ }
    | SIN LP expression RP { /* $$ = ...; */ }
    | COS LP expression RP { /* $$ = ...; */ }
    | TAN LP expression RP { /* $$ = ...; */ }
    | LOG LP expression RP { /* $$ = ...; */ }
    | EXP LP expression RP { /* $$ = ...; */ }
    | POW LP expression RP { /* $$ = ...; */ }
    | PI LP RP { /* $$ = ...; */ }
    | SCANF LP RP { /* $$ = make_read(); */ }
    | IDENTIFIER { /* $$ = make_identifier($1); */ }
    ;

%%

void yyerror(const char* s) {
    std::cerr << "Error: " << s << std::endl;
}

int main() {
    yyparse();
    return 0;
}