%option noyywrap
%option c++

%{
#include "parser.y"
#include <cstring>
#include <cstdlib>
%}

%%

"printlog"      { return PRINTLOG; }
"BREAK"         { return BREAK; }
"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }
"scanf"         { return SCANF; }
"sqrt"          { return SQRT; }
"sin"           { return SIN; }
"cos"           { return COS; }
"tan"           { return TAN; }
"log"           { return LOG; }
"exp"           { return EXP; }
"pow"           { return POW; }
"pi"            { return PI; }
"int"           { return INT_TYPE; }
"float"         { return FLOAT_TYPE; }
"str"           { return STR_TYPE; }
"bool"          { return BOOL_TYPE; }
"STOP"          { return STOP; }
"START"         { return START; }
"FINISH"        { return FINISH; }
"name"          { return NAME; }
"id"            { return ID_KW; }
"station"       { return STATION; }
"speed"         { return SPEED; }
"region"        { return REGION; }
"rotation"      { return ROTATION; }

[0-9]+"."[0-9]+ {
    yylval.floatval = atof(yytext);
    return FLOAT;
}
[0-9]+ {
    yylval.intval = atoi(yytext);
    return INT;
}
\"([^\\\"]|\\.)*\" {
    yylval.strval = strdup(yytext + 1); // remove quotes
    yylval.strval[strlen(yylval.strval) - 1] = '\0';
    return STRING;
}

"=="            { return EQUAL; }
"=>"            { return ARROW; }
"="             { return ASSIGNMENT; }
"&&"            { return AND; }
"\|\|"          { return OR; }
"!"             { return NOT; }
">"             { return GT; }
"<"             { return LT; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MULT; }
"/"             { return DIV; }
"("             { return LP; }
")"             { return RP; }
"{"             { return LCB; }
"}"             { return RCB; }
";"             { return SC; }
":"             { return C; }
","             { return COMMA; }

[a-zA-Z_][a-zA-Z0-9_]* {
    yylval.strval = strdup(yytext);
    return IDENTIFIER;
}

[ \t\r\n]+      { /* skip whitespace */ }
"/*"([^*]|\*+[^*/])*\*+ "/" { /* skip block comments */ }

.               { return yytext[0]; }

%%