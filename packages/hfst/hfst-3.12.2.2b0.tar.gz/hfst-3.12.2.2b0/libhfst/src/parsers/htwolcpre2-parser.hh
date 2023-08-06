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

#ifndef YY_HTWOLCPRE2_HTWOLCPRE_PARSER_HH_INCLUDED
# define YY_HTWOLCPRE2_HTWOLCPRE_PARSER_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int htwolcpre2debug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    FREELY_INSERT = 258,
    DIFFERENCE = 259,
    INTERSECTION = 260,
    UNION = 261,
    STAR = 262,
    PLUS = 263,
    CONTAINMENT = 264,
    CONTAINMENT_ONCE = 265,
    TERM_COMPLEMENT = 266,
    COMPLEMENT = 267,
    POWER = 268,
    RIGHT_SQUARE_BRACKET = 269,
    RIGHT_PARENTHESIS = 270,
    LEFT_SQUARE_BRACKET = 271,
    LEFT_PARENTHESIS = 272,
    LEFT_RESTRICTION_ARROW = 273,
    LEFT_ARROW = 274,
    RIGHT_ARROW = 275,
    LEFT_RIGHT_ARROW = 276,
    RE_LEFT_RESTRICTION_ARROW = 277,
    RE_LEFT_ARROW = 278,
    RE_RIGHT_ARROW = 279,
    RE_LEFT_RIGHT_ARROW = 280,
    RE_RIGHT_SQUARE_BRACKET = 281,
    RE_LEFT_SQUARE_BRACKET = 282,
    ALPHABET_DECLARATION = 283,
    DIACRITICS_DECLARATION = 284,
    SETS_DECLARATION = 285,
    DEFINITION_DECLARATION = 286,
    RULES_DECLARATION = 287,
    PAIR_SEPARATOR = 288,
    SYMBOL = 289,
    SEMI_COLON = 290,
    SET_NAME = 291,
    DEFINITION_NAME = 292,
    EQUALS = 293,
    CENTER_MARKER = 294,
    RULE_NAME = 295,
    NUMBER = 296,
    QUESTION_MARK = 297,
    EXCEPT = 298
  };
#endif
/* Tokens.  */
#define FREELY_INSERT 258
#define DIFFERENCE 259
#define INTERSECTION 260
#define UNION 261
#define STAR 262
#define PLUS 263
#define CONTAINMENT 264
#define CONTAINMENT_ONCE 265
#define TERM_COMPLEMENT 266
#define COMPLEMENT 267
#define POWER 268
#define RIGHT_SQUARE_BRACKET 269
#define RIGHT_PARENTHESIS 270
#define LEFT_SQUARE_BRACKET 271
#define LEFT_PARENTHESIS 272
#define LEFT_RESTRICTION_ARROW 273
#define LEFT_ARROW 274
#define RIGHT_ARROW 275
#define LEFT_RIGHT_ARROW 276
#define RE_LEFT_RESTRICTION_ARROW 277
#define RE_LEFT_ARROW 278
#define RE_RIGHT_ARROW 279
#define RE_LEFT_RIGHT_ARROW 280
#define RE_RIGHT_SQUARE_BRACKET 281
#define RE_LEFT_SQUARE_BRACKET 282
#define ALPHABET_DECLARATION 283
#define DIACRITICS_DECLARATION 284
#define SETS_DECLARATION 285
#define DEFINITION_DECLARATION 286
#define RULES_DECLARATION 287
#define PAIR_SEPARATOR 288
#define SYMBOL 289
#define SEMI_COLON 290
#define SET_NAME 291
#define DEFINITION_NAME 292
#define EQUALS 293
#define CENTER_MARKER 294
#define RULE_NAME 295
#define NUMBER 296
#define QUESTION_MARK 297
#define EXCEPT 298

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 71 "htwolcpre2-parser.yy" /* yacc.c:1909  */
 int symbol_number; 

#line 143 "htwolcpre2-parser.hh" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE htwolcpre2lval;

int htwolcpre2parse (void);

#endif /* !YY_HTWOLCPRE2_HTWOLCPRE_PARSER_HH_INCLUDED  */
