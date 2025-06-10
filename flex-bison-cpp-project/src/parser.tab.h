/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_HPP_INCLUDED
# define YY_YY_PARSER_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    PRINTLOG = 258,                /* PRINTLOG  */
    BREAK = 259,                   /* BREAK  */
    IF = 260,                      /* IF  */
    ELSE = 261,                    /* ELSE  */
    WHILE = 262,                   /* WHILE  */
    SCANF = 263,                   /* SCANF  */
    SQRT = 264,                    /* SQRT  */
    SIN = 265,                     /* SIN  */
    COS = 266,                     /* COS  */
    TAN = 267,                     /* TAN  */
    LOG = 268,                     /* LOG  */
    EXP = 269,                     /* EXP  */
    POW = 270,                     /* POW  */
    PI = 271,                      /* PI  */
    INT_TYPE = 272,                /* INT_TYPE  */
    FLOAT_TYPE = 273,              /* FLOAT_TYPE  */
    STR_TYPE = 274,                /* STR_TYPE  */
    BOOL_TYPE = 275,               /* BOOL_TYPE  */
    STOP = 276,                    /* STOP  */
    START = 277,                   /* START  */
    FINISH = 278,                  /* FINISH  */
    NAME = 279,                    /* NAME  */
    ID_KW = 280,                   /* ID_KW  */
    STATION = 281,                 /* STATION  */
    SPEED = 282,                   /* SPEED  */
    REGION = 283,                  /* REGION  */
    ROTATION = 284,                /* ROTATION  */
    INT = 285,                     /* INT  */
    FLOAT = 286,                   /* FLOAT  */
    STRING = 287,                  /* STRING  */
    IDENTIFIER = 288,              /* IDENTIFIER  */
    EQUAL = 289,                   /* EQUAL  */
    ARROW = 290,                   /* ARROW  */
    ASSIGNMENT = 291,              /* ASSIGNMENT  */
    AND = 292,                     /* AND  */
    OR = 293,                      /* OR  */
    NOT = 294,                     /* NOT  */
    GT = 295,                      /* GT  */
    LT = 296,                      /* LT  */
    PLUS = 297,                    /* PLUS  */
    MINUS = 298,                   /* MINUS  */
    MULT = 299,                    /* MULT  */
    DIV = 300,                     /* DIV  */
    LP = 301,                      /* LP  */
    RP = 302,                      /* RP  */
    LCB = 303,                     /* LCB  */
    RCB = 304,                     /* RCB  */
    SC = 305,                      /* SC  */
    C = 306,                       /* C  */
    COMMA = 307                    /* COMMA  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 10 "src/parser.y"

    int intval;
    float floatval;
    char* strval;
    Node* node;

#line 123 "parser.hpp"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_HPP_INCLUDED  */
