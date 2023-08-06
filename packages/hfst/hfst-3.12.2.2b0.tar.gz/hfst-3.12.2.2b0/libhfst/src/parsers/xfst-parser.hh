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

#ifndef YY_HXFST_XFST_PARSER_HH_INCLUDED
# define YY_HXFST_XFST_PARSER_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int hxfstdebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    APROPOS = 258,
    DESCRIBE = 259,
    ECHO_ = 260,
    SYSTEM = 261,
    QUIT = 262,
    HFST = 263,
    NAMETOKEN = 264,
    NAMECHAR = 265,
    GLOB = 266,
    PROTOTYPE = 267,
    DEFINE_NAME = 268,
    DEFINE_FUNCTION = 269,
    RANGE = 270,
    REDIRECT_IN = 271,
    REDIRECT_OUT = 272,
    SAVE_PROLOG = 273,
    FOR = 274,
    REVERSE = 275,
    VIEW = 276,
    LOADD = 277,
    PRINT_LABEL_COUNT = 278,
    TEST_OVERLAP = 279,
    TEST_NONNULL = 280,
    CONCATENATE = 281,
    LOADS = 282,
    INVERT = 283,
    PRINT_ALIASES = 284,
    PRINT_LABELS = 285,
    XFST_OPTIONAL = 286,
    PRINT_SHORTEST_STRING_SIZE = 287,
    READ_PROPS = 288,
    TEST_FUNCT = 289,
    PRINT_LABELMAPS = 290,
    SUBSTRING = 291,
    COMPOSE = 292,
    READ_SPACED = 293,
    TEST_UPPER_UNI = 294,
    COLLECT_EPSILON_LOOPS = 295,
    ZERO_PLUS = 296,
    INSPECT = 297,
    ROTATE = 298,
    PRINT_WORDS = 299,
    POP = 300,
    SAVE_SPACED = 301,
    DEFINE = 302,
    SHOW = 303,
    PRINT_LONGEST_STRING_SIZE = 304,
    TEST_EQ = 305,
    SORT = 306,
    SAVE_DEFINITIONS = 307,
    SAVE_DOT = 308,
    TEST_UPPER_BOUNDED = 309,
    COMPLETE = 310,
    PRINT_FILE_INFO = 311,
    INTERSECT = 312,
    END_SUB = 313,
    TURN = 314,
    PRINT_LIST = 315,
    SUBSTITUTE_SYMBOL = 316,
    APPLY_UP = 317,
    ONE_PLUS = 318,
    UNDEFINE = 319,
    EPSILON_REMOVE = 320,
    PRINT_RANDOM_WORDS = 321,
    CTRLD = 322,
    EXTRACT_UNAMBIGUOUS = 323,
    SEMICOLON = 324,
    PRINT_LOWER_WORDS = 325,
    READ_PROLOG = 326,
    CLEAR = 327,
    PRINT_SIGMA_COUNT = 328,
    SUBSTITUTE_NAMED = 329,
    PRINT_FLAGS = 330,
    SET = 331,
    NEGATE = 332,
    APPLY_DOWN = 333,
    PRINT_STACK = 334,
    SAVE_STACK = 335,
    PUSH = 336,
    TEST_LOWER_BOUNDED = 337,
    PRINT_DEFINED = 338,
    APPLY_MED = 339,
    SHOW_ALL = 340,
    PRINT_ARCCOUNT = 341,
    PRINT_SIZE = 342,
    TEST_NULL = 343,
    PRINT_RANDOM_UPPER = 344,
    PRINT_LONGEST_STRING = 345,
    UPPER_SIDE = 346,
    XFST_IGNORE = 347,
    TEST_UNAMBIGUOUS = 348,
    PRINT = 349,
    READ_TEXT = 350,
    UNLIST = 351,
    SUBSTITUTE_LABEL = 352,
    SAVE_DEFINITION = 353,
    ELIMINATE_FLAG = 354,
    EDIT_PROPS = 355,
    PRINT_UPPER_WORDS = 356,
    NAME = 357,
    EXTRACT_AMBIGUOUS = 358,
    DEFINE_ALIAS = 359,
    PRINT_RANDOM_LOWER = 360,
    CROSSPRODUCT = 361,
    COMPACT_SIGMA = 362,
    SOURCE = 363,
    AMBIGUOUS = 364,
    ELIMINATE_ALL = 365,
    PRINT_SIGMA = 366,
    PRINT_SHORTEST_STRING = 367,
    LEFT_PAREN = 368,
    PRINT_PROPS = 369,
    READ_REGEX = 370,
    DEFINE_LIST = 371,
    TEST_ID = 372,
    PRINT_LISTS = 373,
    TEST_SUBLANGUAGE = 374,
    TEST_LOWER_UNI = 375,
    COMPILE_REPLACE_UPPER = 376,
    CLEANUP = 377,
    ADD_PROPS = 378,
    PRINT_SIGMA_WORD_COUNT = 379,
    SHUFFLE = 380,
    COLON = 381,
    SAVE_TEXT = 382,
    DETERMINIZE = 383,
    SIGMA = 384,
    COMPILE_REPLACE_LOWER = 385,
    UNION = 386,
    PRINT_DIR = 387,
    LIST = 388,
    LOWER_SIDE = 389,
    MINIMIZE = 390,
    MINUS = 391,
    PRINT_NAME = 392,
    PRUNE_NET = 393,
    PUSH_DEFINED = 394,
    READ_LEXC = 395,
    READ_ATT = 396,
    TWOSIDED_FLAGS = 397,
    WRITE_ATT = 398,
    ASSERT = 399,
    LABEL_NET = 400,
    LOOKUP_OPTIMIZE = 401,
    REMOVE_OPTIMIZATION = 402,
    TEST_INFINITELY_AMBIGUOUS = 403,
    XFST_ERROR = 404,
    NEWLINE = 405,
    REGEX = 406,
    APPLY_INPUT = 407
  };
#endif
/* Tokens.  */
#define APROPOS 258
#define DESCRIBE 259
#define ECHO_ 260
#define SYSTEM 261
#define QUIT 262
#define HFST 263
#define NAMETOKEN 264
#define NAMECHAR 265
#define GLOB 266
#define PROTOTYPE 267
#define DEFINE_NAME 268
#define DEFINE_FUNCTION 269
#define RANGE 270
#define REDIRECT_IN 271
#define REDIRECT_OUT 272
#define SAVE_PROLOG 273
#define FOR 274
#define REVERSE 275
#define VIEW 276
#define LOADD 277
#define PRINT_LABEL_COUNT 278
#define TEST_OVERLAP 279
#define TEST_NONNULL 280
#define CONCATENATE 281
#define LOADS 282
#define INVERT 283
#define PRINT_ALIASES 284
#define PRINT_LABELS 285
#define XFST_OPTIONAL 286
#define PRINT_SHORTEST_STRING_SIZE 287
#define READ_PROPS 288
#define TEST_FUNCT 289
#define PRINT_LABELMAPS 290
#define SUBSTRING 291
#define COMPOSE 292
#define READ_SPACED 293
#define TEST_UPPER_UNI 294
#define COLLECT_EPSILON_LOOPS 295
#define ZERO_PLUS 296
#define INSPECT 297
#define ROTATE 298
#define PRINT_WORDS 299
#define POP 300
#define SAVE_SPACED 301
#define DEFINE 302
#define SHOW 303
#define PRINT_LONGEST_STRING_SIZE 304
#define TEST_EQ 305
#define SORT 306
#define SAVE_DEFINITIONS 307
#define SAVE_DOT 308
#define TEST_UPPER_BOUNDED 309
#define COMPLETE 310
#define PRINT_FILE_INFO 311
#define INTERSECT 312
#define END_SUB 313
#define TURN 314
#define PRINT_LIST 315
#define SUBSTITUTE_SYMBOL 316
#define APPLY_UP 317
#define ONE_PLUS 318
#define UNDEFINE 319
#define EPSILON_REMOVE 320
#define PRINT_RANDOM_WORDS 321
#define CTRLD 322
#define EXTRACT_UNAMBIGUOUS 323
#define SEMICOLON 324
#define PRINT_LOWER_WORDS 325
#define READ_PROLOG 326
#define CLEAR 327
#define PRINT_SIGMA_COUNT 328
#define SUBSTITUTE_NAMED 329
#define PRINT_FLAGS 330
#define SET 331
#define NEGATE 332
#define APPLY_DOWN 333
#define PRINT_STACK 334
#define SAVE_STACK 335
#define PUSH 336
#define TEST_LOWER_BOUNDED 337
#define PRINT_DEFINED 338
#define APPLY_MED 339
#define SHOW_ALL 340
#define PRINT_ARCCOUNT 341
#define PRINT_SIZE 342
#define TEST_NULL 343
#define PRINT_RANDOM_UPPER 344
#define PRINT_LONGEST_STRING 345
#define UPPER_SIDE 346
#define XFST_IGNORE 347
#define TEST_UNAMBIGUOUS 348
#define PRINT 349
#define READ_TEXT 350
#define UNLIST 351
#define SUBSTITUTE_LABEL 352
#define SAVE_DEFINITION 353
#define ELIMINATE_FLAG 354
#define EDIT_PROPS 355
#define PRINT_UPPER_WORDS 356
#define NAME 357
#define EXTRACT_AMBIGUOUS 358
#define DEFINE_ALIAS 359
#define PRINT_RANDOM_LOWER 360
#define CROSSPRODUCT 361
#define COMPACT_SIGMA 362
#define SOURCE 363
#define AMBIGUOUS 364
#define ELIMINATE_ALL 365
#define PRINT_SIGMA 366
#define PRINT_SHORTEST_STRING 367
#define LEFT_PAREN 368
#define PRINT_PROPS 369
#define READ_REGEX 370
#define DEFINE_LIST 371
#define TEST_ID 372
#define PRINT_LISTS 373
#define TEST_SUBLANGUAGE 374
#define TEST_LOWER_UNI 375
#define COMPILE_REPLACE_UPPER 376
#define CLEANUP 377
#define ADD_PROPS 378
#define PRINT_SIGMA_WORD_COUNT 379
#define SHUFFLE 380
#define COLON 381
#define SAVE_TEXT 382
#define DETERMINIZE 383
#define SIGMA 384
#define COMPILE_REPLACE_LOWER 385
#define UNION 386
#define PRINT_DIR 387
#define LIST 388
#define LOWER_SIDE 389
#define MINIMIZE 390
#define MINUS 391
#define PRINT_NAME 392
#define PRUNE_NET 393
#define PUSH_DEFINED 394
#define READ_LEXC 395
#define READ_ATT 396
#define TWOSIDED_FLAGS 397
#define WRITE_ATT 398
#define ASSERT 399
#define LABEL_NET 400
#define LOOKUP_OPTIMIZE 401
#define REMOVE_OPTIMIZATION 402
#define TEST_INFINITELY_AMBIGUOUS 403
#define XFST_ERROR 404
#define NEWLINE 405
#define REGEX 406
#define APPLY_INPUT 407

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 51 "xfst-parser.yy" /* yacc.c:1909  */

    char* name;
    char* text;
    char** list;
    char* file;
    void* nothing;

#line 366 "xfst-parser.hh" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


extern YYSTYPE hxfstlval;
extern YYLTYPE hxfstlloc;
int hxfstparse (void);

#endif /* !YY_HXFST_XFST_PARSER_HH_INCLUDED  */
