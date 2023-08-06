/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

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

#ifndef YY_SFST_SFST_COMPILER_HH_INCLUDED
# define YY_SFST_SFST_COMPILER_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int sfstdebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    NEWLINE = 258,
    ALPHA = 259,
    COMPOSE = 260,
    PRINT = 261,
    POS = 262,
    INSERT = 263,
    SUBSTITUTE = 264,
    SWITCH = 265,
    ARROW = 266,
    REPLACE = 267,
    SYMBOL = 268,
    VAR = 269,
    SVAR = 270,
    RVAR = 271,
    RSVAR = 272,
    STRING = 273,
    STRING2 = 274,
    UTF8CHAR = 275,
    CHARACTER = 276,
    SEQ = 277
  };
#endif
/* Tokens.  */
#define NEWLINE 258
#define ALPHA 259
#define COMPOSE 260
#define PRINT 261
#define POS 262
#define INSERT 263
#define SUBSTITUTE 264
#define SWITCH 265
#define ARROW 266
#define REPLACE 267
#define SYMBOL 268
#define VAR 269
#define SVAR 270
#define RVAR 271
#define RSVAR 272
#define STRING 273
#define STRING2 274
#define UTF8CHAR 275
#define CHARACTER 276
#define SEQ 277

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 56 "sfst-compiler.yy" /* yacc.c:1909  */

  int        number;
  hfst::Twol_Type  type;
  hfst::Repl_Type  rtype;
  char       *name;
  char       *value;
  unsigned char uchar;
  unsigned int  longchar;
  hfst::Character  character;
  hfst::HfstTransducer   *expression;
  hfst::Range      *range;
  hfst::Ranges     *ranges;
  hfst::Contexts   *contexts;

#line 113 "sfst-compiler.hh" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE sfstlval;

int sfstparse (void);

#endif /* !YY_SFST_SFST_COMPILER_HH_INCLUDED  */
