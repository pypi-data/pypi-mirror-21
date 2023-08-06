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

#ifndef YY_PMATCH_PMATCH_PARSE_HH_INCLUDED
# define YY_PMATCH_PMATCH_PARSE_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int pmatchdebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    END_OF_WEIGHTED_EXPRESSION = 258,
    WEIGHT = 259,
    CHARACTER_RANGE = 260,
    CROSS_PRODUCT = 261,
    COMPOSITION = 262,
    LENIENT_COMPOSITION = 263,
    INTERSECTION = 264,
    MERGE_RIGHT_ARROW = 265,
    MERGE_LEFT_ARROW = 266,
    CENTER_MARKER = 267,
    MARKUP_MARKER = 268,
    SHUFFLE = 269,
    BEFORE = 270,
    AFTER = 271,
    LEFT_ARROW = 272,
    RIGHT_ARROW = 273,
    LEFT_RIGHT_ARROW = 274,
    LEFT_RESTRICTION = 275,
    REPLACE_RIGHT = 276,
    REPLACE_LEFT = 277,
    OPTIONAL_REPLACE_RIGHT = 278,
    OPTIONAL_REPLACE_LEFT = 279,
    REPLACE_LEFT_RIGHT = 280,
    OPTIONAL_REPLACE_LEFT_RIGHT = 281,
    RTL_LONGEST_MATCH = 282,
    RTL_SHORTEST_MATCH = 283,
    LTR_LONGEST_MATCH = 284,
    LTR_SHORTEST_MATCH = 285,
    REPLACE_CONTEXT_UU = 286,
    REPLACE_CONTEXT_LU = 287,
    REPLACE_CONTEXT_UL = 288,
    REPLACE_CONTEXT_LL = 289,
    UNION = 290,
    MINUS = 291,
    UPPER_MINUS = 292,
    LOWER_MINUS = 293,
    UPPER_PRIORITY_UNION = 294,
    LOWER_PRIORITY_UNION = 295,
    IGNORING = 296,
    IGNORE_INTERNALLY = 297,
    LEFT_QUOTIENT = 298,
    COMMA = 299,
    COMMACOMMA = 300,
    SUBSTITUTE_LEFT = 301,
    TERM_COMPLEMENT = 302,
    COMPLEMENT = 303,
    CONTAINMENT = 304,
    CONTAINMENT_ONCE = 305,
    CONTAINMENT_OPT = 306,
    STAR = 307,
    PLUS = 308,
    REVERSE = 309,
    INVERT = 310,
    UPPER_PROJECT = 311,
    LOWER_PROJECT = 312,
    READ_BIN = 313,
    READ_TEXT = 314,
    READ_SPACED = 315,
    READ_PROLOG = 316,
    READ_RE = 317,
    READ_VEC = 318,
    READ_LEXC = 319,
    CATENATE_N_TO_K = 320,
    CATENATE_N = 321,
    CATENATE_N_PLUS = 322,
    CATENATE_N_MINUS = 323,
    LEFT_BRACKET = 324,
    RIGHT_BRACKET = 325,
    LEFT_PARENTHESIS = 326,
    RIGHT_PARENTHESIS = 327,
    LEFT_BRACKET_DOTTED = 328,
    RIGHT_BRACKET_DOTTED = 329,
    PAIR_SEPARATOR = 330,
    PAIR_SEPARATOR_SOLE = 331,
    PAIR_SEPARATOR_WO_RIGHT = 332,
    PAIR_SEPARATOR_WO_LEFT = 333,
    EPSILON_TOKEN = 334,
    ANY_TOKEN = 335,
    BOUNDARY_MARKER = 336,
    LEXER_ERROR = 337,
    SYMBOL = 338,
    SYMBOL_WITH_LEFT_PAREN = 339,
    QUOTED_LITERAL = 340,
    CURLY_LITERAL = 341,
    ALPHA = 342,
    LOWERALPHA = 343,
    UPPERALPHA = 344,
    NUM = 345,
    PUNCT = 346,
    WHITESPACE = 347,
    VARIABLE_NAME = 348,
    DEFINE = 349,
    SET_VARIABLE = 350,
    LIT_LEFT = 351,
    INS_LEFT = 352,
    REGEX = 353,
    DEFINS = 354,
    DEFINED_LIST = 355,
    CAP_LEFT = 356,
    OPTCAP_LEFT = 357,
    OPT_TOLOWER_LEFT = 358,
    TOLOWER_LEFT = 359,
    OPT_TOUPPER_LEFT = 360,
    TOUPPER_LEFT = 361,
    ANY_CASE_LEFT = 362,
    IMPLODE_LEFT = 363,
    EXPLODE_LEFT = 364,
    DEFINE_LEFT = 365,
    ENDTAG_LEFT = 366,
    LIKE_LEFT = 367,
    LC_LEFT = 368,
    RC_LEFT = 369,
    NLC_LEFT = 370,
    NRC_LEFT = 371,
    OR_LEFT = 372,
    AND_LEFT = 373,
    TAG_LEFT = 374,
    LST_LEFT = 375,
    EXC_LEFT = 376,
    INTERPOLATE_LEFT = 377,
    SIGMA_LEFT = 378,
    COUNTER_LEFT = 379
  };
#endif
/* Tokens.  */
#define END_OF_WEIGHTED_EXPRESSION 258
#define WEIGHT 259
#define CHARACTER_RANGE 260
#define CROSS_PRODUCT 261
#define COMPOSITION 262
#define LENIENT_COMPOSITION 263
#define INTERSECTION 264
#define MERGE_RIGHT_ARROW 265
#define MERGE_LEFT_ARROW 266
#define CENTER_MARKER 267
#define MARKUP_MARKER 268
#define SHUFFLE 269
#define BEFORE 270
#define AFTER 271
#define LEFT_ARROW 272
#define RIGHT_ARROW 273
#define LEFT_RIGHT_ARROW 274
#define LEFT_RESTRICTION 275
#define REPLACE_RIGHT 276
#define REPLACE_LEFT 277
#define OPTIONAL_REPLACE_RIGHT 278
#define OPTIONAL_REPLACE_LEFT 279
#define REPLACE_LEFT_RIGHT 280
#define OPTIONAL_REPLACE_LEFT_RIGHT 281
#define RTL_LONGEST_MATCH 282
#define RTL_SHORTEST_MATCH 283
#define LTR_LONGEST_MATCH 284
#define LTR_SHORTEST_MATCH 285
#define REPLACE_CONTEXT_UU 286
#define REPLACE_CONTEXT_LU 287
#define REPLACE_CONTEXT_UL 288
#define REPLACE_CONTEXT_LL 289
#define UNION 290
#define MINUS 291
#define UPPER_MINUS 292
#define LOWER_MINUS 293
#define UPPER_PRIORITY_UNION 294
#define LOWER_PRIORITY_UNION 295
#define IGNORING 296
#define IGNORE_INTERNALLY 297
#define LEFT_QUOTIENT 298
#define COMMA 299
#define COMMACOMMA 300
#define SUBSTITUTE_LEFT 301
#define TERM_COMPLEMENT 302
#define COMPLEMENT 303
#define CONTAINMENT 304
#define CONTAINMENT_ONCE 305
#define CONTAINMENT_OPT 306
#define STAR 307
#define PLUS 308
#define REVERSE 309
#define INVERT 310
#define UPPER_PROJECT 311
#define LOWER_PROJECT 312
#define READ_BIN 313
#define READ_TEXT 314
#define READ_SPACED 315
#define READ_PROLOG 316
#define READ_RE 317
#define READ_VEC 318
#define READ_LEXC 319
#define CATENATE_N_TO_K 320
#define CATENATE_N 321
#define CATENATE_N_PLUS 322
#define CATENATE_N_MINUS 323
#define LEFT_BRACKET 324
#define RIGHT_BRACKET 325
#define LEFT_PARENTHESIS 326
#define RIGHT_PARENTHESIS 327
#define LEFT_BRACKET_DOTTED 328
#define RIGHT_BRACKET_DOTTED 329
#define PAIR_SEPARATOR 330
#define PAIR_SEPARATOR_SOLE 331
#define PAIR_SEPARATOR_WO_RIGHT 332
#define PAIR_SEPARATOR_WO_LEFT 333
#define EPSILON_TOKEN 334
#define ANY_TOKEN 335
#define BOUNDARY_MARKER 336
#define LEXER_ERROR 337
#define SYMBOL 338
#define SYMBOL_WITH_LEFT_PAREN 339
#define QUOTED_LITERAL 340
#define CURLY_LITERAL 341
#define ALPHA 342
#define LOWERALPHA 343
#define UPPERALPHA 344
#define NUM 345
#define PUNCT 346
#define WHITESPACE 347
#define VARIABLE_NAME 348
#define DEFINE 349
#define SET_VARIABLE 350
#define LIT_LEFT 351
#define INS_LEFT 352
#define REGEX 353
#define DEFINS 354
#define DEFINED_LIST 355
#define CAP_LEFT 356
#define OPTCAP_LEFT 357
#define OPT_TOLOWER_LEFT 358
#define TOLOWER_LEFT 359
#define OPT_TOUPPER_LEFT 360
#define TOUPPER_LEFT 361
#define ANY_CASE_LEFT 362
#define IMPLODE_LEFT 363
#define EXPLODE_LEFT 364
#define DEFINE_LEFT 365
#define ENDTAG_LEFT 366
#define LIKE_LEFT 367
#define LC_LEFT 368
#define RC_LEFT 369
#define NLC_LEFT 370
#define NRC_LEFT 371
#define OR_LEFT 372
#define AND_LEFT 373
#define TAG_LEFT 374
#define LST_LEFT 375
#define EXC_LEFT 376
#define INTERPOLATE_LEFT 377
#define SIGMA_LEFT 378
#define COUNTER_LEFT 379

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 36 "pmatch_parse.yy" /* yacc.c:1909  */

         int value;
         int* values;
         double weight;
         char* label;
         hfst::pmatch::PmatchObject* pmatchObject;
         std::pair<std::string, hfst::pmatch::PmatchObject*>* pmatchDefinition;
         std::vector<hfst::pmatch::PmatchObject *>* pmatchObject_vector;
         std::vector<std::string>* string_vector;

         hfst::pmatch::PmatchParallelRulesContainer * replaceRules;
         hfst::pmatch::PmatchReplaceRuleContainer * replaceRule;
         hfst::pmatch::PmatchMappingPairsContainer * mappings;
         hfst::pmatch::PmatchContextsContainer * parallelContexts;
         hfst::pmatch::PmatchObjectPair * restrictionContext;
         hfst::pmatch::MappingPairVector * restrictionContexts;
         hfst::xeroxRules::ReplaceType replType;
         hfst::xeroxRules::ReplaceArrow replaceArrow;
     

#line 323 "pmatch_parse.hh" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE pmatchlval;

int pmatchparse (void);

#endif /* !YY_PMATCH_PMATCH_PARSE_HH_INCLUDED  */
