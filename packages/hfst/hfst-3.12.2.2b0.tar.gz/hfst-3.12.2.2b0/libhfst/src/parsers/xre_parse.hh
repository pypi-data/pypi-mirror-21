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

#ifndef YY_XRE_XRE_PARSE_HH_INCLUDED
# define YY_XRE_XRE_PARSE_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif
#if YYDEBUG
extern int xredebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    WEIGHT = 258,
    SYMBOL = 259,
    MULTICHAR_SYMBOL = 260,
    CURLY_BRACKETS = 261,
    CROSS_PRODUCT = 262,
    COMPOSITION = 263,
    LENIENT_COMPOSITION = 264,
    INTERSECTION = 265,
    MERGE_RIGHT_ARROW = 266,
    MERGE_LEFT_ARROW = 267,
    CENTER_MARKER = 268,
    MARKUP_MARKER = 269,
    SHUFFLE = 270,
    LEFT_RESTRICTION = 271,
    LEFT_ARROW = 272,
    RIGHT_ARROW = 273,
    LEFT_RIGHT_ARROW = 274,
    REPLACE_RIGHT = 275,
    REPLACE_LEFT = 276,
    OPTIONAL_REPLACE_RIGHT = 277,
    OPTIONAL_REPLACE_LEFT = 278,
    REPLACE_LEFT_RIGHT = 279,
    OPTIONAL_REPLACE_LEFT_RIGHT = 280,
    RTL_LONGEST_MATCH = 281,
    RTL_SHORTEST_MATCH = 282,
    LTR_LONGEST_MATCH = 283,
    LTR_SHORTEST_MATCH = 284,
    REPLACE_CONTEXT_UU = 285,
    REPLACE_CONTEXT_LU = 286,
    REPLACE_CONTEXT_UL = 287,
    REPLACE_CONTEXT_LL = 288,
    UNION = 289,
    MINUS = 290,
    UPPER_MINUS = 291,
    LOWER_MINUS = 292,
    UPPER_PRIORITY_UNION = 293,
    LOWER_PRIORITY_UNION = 294,
    IGNORING = 295,
    IGNORE_INTERNALLY = 296,
    LEFT_QUOTIENT = 297,
    COMMACOMMA = 298,
    COMMA = 299,
    BEFORE = 300,
    AFTER = 301,
    SUBSTITUTE_LEFT = 302,
    TERM_COMPLEMENT = 303,
    COMPLEMENT = 304,
    CONTAINMENT = 305,
    CONTAINMENT_ONCE = 306,
    CONTAINMENT_OPT = 307,
    REVERSE = 308,
    INVERT = 309,
    XRE_UPPER = 310,
    XRE_LOWER = 311,
    STAR = 312,
    PLUS = 313,
    CATENATE_N_TO_K = 314,
    CATENATE_N = 315,
    CATENATE_N_PLUS = 316,
    CATENATE_N_MINUS = 317,
    READ_BIN = 318,
    READ_TEXT = 319,
    READ_SPACED = 320,
    READ_PROLOG = 321,
    READ_RE = 322,
    FUNCTION_NAME = 323,
    LEFT_BRACKET = 324,
    RIGHT_BRACKET = 325,
    LEFT_PARENTHESIS = 326,
    RIGHT_PARENTHESIS = 327,
    LEFT_BRACKET_DOTTED = 328,
    RIGHT_BRACKET_DOTTED = 329,
    SUBVAL = 330,
    EPSILON_TOKEN = 331,
    ANY_TOKEN = 332,
    BOUNDARY_MARKER = 333,
    LEXER_ERROR = 334,
    END_OF_EXPRESSION = 335,
    PAIR_SEPARATOR = 336,
    QUOTED_LITERAL = 337,
    QUOTED_MULTICHAR_LITERAL = 338
  };
#endif
/* Tokens.  */
#define WEIGHT 258
#define SYMBOL 259
#define MULTICHAR_SYMBOL 260
#define CURLY_BRACKETS 261
#define CROSS_PRODUCT 262
#define COMPOSITION 263
#define LENIENT_COMPOSITION 264
#define INTERSECTION 265
#define MERGE_RIGHT_ARROW 266
#define MERGE_LEFT_ARROW 267
#define CENTER_MARKER 268
#define MARKUP_MARKER 269
#define SHUFFLE 270
#define LEFT_RESTRICTION 271
#define LEFT_ARROW 272
#define RIGHT_ARROW 273
#define LEFT_RIGHT_ARROW 274
#define REPLACE_RIGHT 275
#define REPLACE_LEFT 276
#define OPTIONAL_REPLACE_RIGHT 277
#define OPTIONAL_REPLACE_LEFT 278
#define REPLACE_LEFT_RIGHT 279
#define OPTIONAL_REPLACE_LEFT_RIGHT 280
#define RTL_LONGEST_MATCH 281
#define RTL_SHORTEST_MATCH 282
#define LTR_LONGEST_MATCH 283
#define LTR_SHORTEST_MATCH 284
#define REPLACE_CONTEXT_UU 285
#define REPLACE_CONTEXT_LU 286
#define REPLACE_CONTEXT_UL 287
#define REPLACE_CONTEXT_LL 288
#define UNION 289
#define MINUS 290
#define UPPER_MINUS 291
#define LOWER_MINUS 292
#define UPPER_PRIORITY_UNION 293
#define LOWER_PRIORITY_UNION 294
#define IGNORING 295
#define IGNORE_INTERNALLY 296
#define LEFT_QUOTIENT 297
#define COMMACOMMA 298
#define COMMA 299
#define BEFORE 300
#define AFTER 301
#define SUBSTITUTE_LEFT 302
#define TERM_COMPLEMENT 303
#define COMPLEMENT 304
#define CONTAINMENT 305
#define CONTAINMENT_ONCE 306
#define CONTAINMENT_OPT 307
#define REVERSE 308
#define INVERT 309
#define XRE_UPPER 310
#define XRE_LOWER 311
#define STAR 312
#define PLUS 313
#define CATENATE_N_TO_K 314
#define CATENATE_N 315
#define CATENATE_N_PLUS 316
#define CATENATE_N_MINUS 317
#define READ_BIN 318
#define READ_TEXT 319
#define READ_SPACED 320
#define READ_PROLOG 321
#define READ_RE 322
#define FUNCTION_NAME 323
#define LEFT_BRACKET 324
#define RIGHT_BRACKET 325
#define LEFT_PARENTHESIS 326
#define RIGHT_PARENTHESIS 327
#define LEFT_BRACKET_DOTTED 328
#define RIGHT_BRACKET_DOTTED 329
#define SUBVAL 330
#define EPSILON_TOKEN 331
#define ANY_TOKEN 332
#define BOUNDARY_MARKER 333
#define LEXER_ERROR 334
#define END_OF_EXPRESSION 335
#define PAIR_SEPARATOR 336
#define QUOTED_LITERAL 337
#define QUOTED_MULTICHAR_LITERAL 338

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 82 "xre_parse.yy" /* yacc.c:1909  */


    int value;
    int* values;
    double weight;
    char* label;
    
    char *subval1, *subval2;
    
    hfst::HfstTransducer* transducer;
    hfst::HfstTransducerPair* transducerPair;
    hfst::HfstTransducerPairVector* transducerPairVector;
    hfst::HfstTransducerVector* transducerVector;

   std::pair<hfst::xeroxRules::ReplaceArrow, std::vector<hfst::xeroxRules::Rule> >* replaceRuleVectorWithArrow;
   std::pair< hfst::xeroxRules::ReplaceArrow, hfst::xeroxRules::Rule>* replaceRuleWithArrow;
   std::pair< hfst::xeroxRules::ReplaceArrow, hfst::HfstTransducerPairVector>* mappingVectorWithArrow;
   std::pair< hfst::xeroxRules::ReplaceArrow, hfst::HfstTransducerPair>* mappingWithArrow;
       
   std::pair<hfst::xeroxRules::ReplaceType, hfst::HfstTransducerPairVector>* contextWithMark;
   
   hfst::xeroxRules::ReplaceType replType;
   hfst::xeroxRules::ReplaceArrow replaceArrow;


#line 246 "xre_parse.hh" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif



int xreparse (void * scanner);

#endif /* !YY_XRE_XRE_PARSE_HH_INCLUDED  */
