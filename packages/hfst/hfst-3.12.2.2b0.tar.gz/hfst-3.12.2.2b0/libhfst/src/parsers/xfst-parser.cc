/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1


/* Substitute the variable and function names.  */
#define yyparse         hxfstparse
#define yylex           hxfstlex
#define yyerror         hxfsterror
#define yydebug         hxfstdebug
#define yynerrs         hxfstnerrs

#define yylval          hxfstlval
#define yychar          hxfstchar
#define yylloc          hxfstlloc

/* Copy the first part of user declarations.  */
#line 1 "xfst-parser.yy" /* yacc.c:339  */

// Copyright (c) 2016 University of Helsinki
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 3 of the License, or (at your option) any later version.
// See the file COPYING included with this distribution for more
// information.

//! @file xfst-parser.yy
//!
//! @brief A parser for xfst
//!
//! @author Tommi A. Pirinen

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <cstdlib>
#include <cstdio>

#include <string>
using std::string;

namespace hfst {
  class HfstTransducer;
}

#include "XfstCompiler.h"
#include "xfst-utils.h"

#define CHECK if (hfst::xfst::xfst_->get_fail_flag()) { YYABORT; }

// obligatory yacc stuff
extern int hxfstlineno;
void hxfsterror(const char *text);
int hxfstlex(void);


#line 117 "xfst-parser.cc" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 1
#endif

/* In a future release of Bison, this section will be replaced
   by #include "y.tab.h".  */
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
#line 51 "xfst-parser.yy" /* yacc.c:355  */

    char* name;
    char* text;
    char** list;
    char* file;
    void* nothing;

#line 469 "xfst-parser.cc" /* yacc.c:355  */
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

/* Copy the second part of user declarations.  */

#line 500 "xfst-parser.cc" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL \
             && defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
  YYLTYPE yyls_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE) + sizeof (YYLTYPE)) \
      + 2 * YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  348
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   918

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  153
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  10
/* YYNRULES -- Number of rules.  */
#define YYNRULES  262
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  539

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   407

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124,
     125,   126,   127,   128,   129,   130,   131,   132,   133,   134,
     135,   136,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149,   150,   151,   152
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    98,    98,    99,   102,   103,   106,   115,   119,   124,
     127,   130,   134,   143,   147,   150,   153,   157,   166,   170,
     174,   183,   187,   190,   194,   198,   202,   207,   212,   217,
     222,   229,   233,   238,   243,   247,   251,   255,   260,   264,
     268,   271,   274,   278,   281,   284,   287,   291,   295,   300,
     303,   307,   311,   315,   319,   324,   328,   333,   337,   343,
     352,   356,   359,   363,   366,   369,   372,   375,   378,   381,
     384,   387,   390,   393,   396,   399,   403,   406,   409,   412,
     415,   418,   421,   424,   427,   430,   433,   436,   440,   445,
     450,   456,   465,   468,   477,   487,   490,   499,   502,   511,
     515,   524,   527,   536,   539,   548,   551,   555,   564,   567,
     576,   579,   588,   592,   601,   604,   614,   619,   629,   634,
     643,   646,   656,   661,   671,   676,   680,   691,   700,   703,
     718,   728,   732,   743,   751,   754,   768,   778,   782,   793,
     801,   804,   817,   826,   830,   840,   848,   851,   864,   873,
     877,   887,   895,   898,   911,   920,   924,   934,   942,   945,
     958,   967,   971,   980,   983,   987,   990,   999,  1003,  1012,
    1015,  1024,  1027,  1037,  1046,  1049,  1053,  1062,  1065,  1074,
    1077,  1087,  1091,  1100,  1103,  1107,  1111,  1115,  1119,  1122,
    1125,  1129,  1138,  1147,  1150,  1159,  1162,  1171,  1175,  1184,
    1187,  1196,  1199,  1203,  1212,  1216,  1220,  1224,  1228,  1232,
    1236,  1240,  1244,  1248,  1251,  1255,  1258,  1267,  1276,  1287,
    1290,  1293,  1296,  1299,  1302,  1305,  1308,  1311,  1314,  1317,
    1320,  1323,  1326,  1329,  1332,  1335,  1338,  1341,  1344,  1347,
    1350,  1353,  1356,  1359,  1362,  1365,  1368,  1371,  1374,  1377,
    1388,  1388,  1390,  1412,  1415,  1420,  1442,  1447,  1473,  1492,
    1496,  1501,  1523
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 1
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "APROPOS", "DESCRIBE", "ECHO_", "SYSTEM",
  "QUIT", "HFST", "NAMETOKEN", "NAMECHAR", "GLOB", "PROTOTYPE",
  "DEFINE_NAME", "DEFINE_FUNCTION", "RANGE", "REDIRECT_IN", "REDIRECT_OUT",
  "SAVE_PROLOG", "FOR", "REVERSE", "VIEW", "LOADD", "PRINT_LABEL_COUNT",
  "TEST_OVERLAP", "TEST_NONNULL", "CONCATENATE", "LOADS", "INVERT",
  "PRINT_ALIASES", "PRINT_LABELS", "XFST_OPTIONAL",
  "PRINT_SHORTEST_STRING_SIZE", "READ_PROPS", "TEST_FUNCT",
  "PRINT_LABELMAPS", "SUBSTRING", "COMPOSE", "READ_SPACED",
  "TEST_UPPER_UNI", "COLLECT_EPSILON_LOOPS", "ZERO_PLUS", "INSPECT",
  "ROTATE", "PRINT_WORDS", "POP", "SAVE_SPACED", "DEFINE", "SHOW",
  "PRINT_LONGEST_STRING_SIZE", "TEST_EQ", "SORT", "SAVE_DEFINITIONS",
  "SAVE_DOT", "TEST_UPPER_BOUNDED", "COMPLETE", "PRINT_FILE_INFO",
  "INTERSECT", "END_SUB", "TURN", "PRINT_LIST", "SUBSTITUTE_SYMBOL",
  "APPLY_UP", "ONE_PLUS", "UNDEFINE", "EPSILON_REMOVE",
  "PRINT_RANDOM_WORDS", "CTRLD", "EXTRACT_UNAMBIGUOUS", "SEMICOLON",
  "PRINT_LOWER_WORDS", "READ_PROLOG", "CLEAR", "PRINT_SIGMA_COUNT",
  "SUBSTITUTE_NAMED", "PRINT_FLAGS", "SET", "NEGATE", "APPLY_DOWN",
  "PRINT_STACK", "SAVE_STACK", "PUSH", "TEST_LOWER_BOUNDED",
  "PRINT_DEFINED", "APPLY_MED", "SHOW_ALL", "PRINT_ARCCOUNT", "PRINT_SIZE",
  "TEST_NULL", "PRINT_RANDOM_UPPER", "PRINT_LONGEST_STRING", "UPPER_SIDE",
  "XFST_IGNORE", "TEST_UNAMBIGUOUS", "PRINT", "READ_TEXT", "UNLIST",
  "SUBSTITUTE_LABEL", "SAVE_DEFINITION", "ELIMINATE_FLAG", "EDIT_PROPS",
  "PRINT_UPPER_WORDS", "NAME", "EXTRACT_AMBIGUOUS", "DEFINE_ALIAS",
  "PRINT_RANDOM_LOWER", "CROSSPRODUCT", "COMPACT_SIGMA", "SOURCE",
  "AMBIGUOUS", "ELIMINATE_ALL", "PRINT_SIGMA", "PRINT_SHORTEST_STRING",
  "LEFT_PAREN", "PRINT_PROPS", "READ_REGEX", "DEFINE_LIST", "TEST_ID",
  "PRINT_LISTS", "TEST_SUBLANGUAGE", "TEST_LOWER_UNI",
  "COMPILE_REPLACE_UPPER", "CLEANUP", "ADD_PROPS",
  "PRINT_SIGMA_WORD_COUNT", "SHUFFLE", "COLON", "SAVE_TEXT", "DETERMINIZE",
  "SIGMA", "COMPILE_REPLACE_LOWER", "UNION", "PRINT_DIR", "LIST",
  "LOWER_SIDE", "MINIMIZE", "MINUS", "PRINT_NAME", "PRUNE_NET",
  "PUSH_DEFINED", "READ_LEXC", "READ_ATT", "TWOSIDED_FLAGS", "WRITE_ATT",
  "ASSERT", "LABEL_NET", "LOOKUP_OPTIMIZE", "REMOVE_OPTIMIZATION",
  "TEST_INFINITELY_AMBIGUOUS", "XFST_ERROR", "NEWLINE", "REGEX",
  "APPLY_INPUT", "$accept", "XFST_SCRIPT", "COMMAND_LIST", "COMMAND",
  "END_COMMAND", "COMMAND_SEQUENCE", "NAMETOKEN_LIST",
  "QUOTED_NAMETOKEN_LIST", "LABEL", "LABEL_LIST", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377,   378,   379,   380,   381,   382,   383,   384,
     385,   386,   387,   388,   389,   390,   391,   392,   393,   394,
     395,   396,   397,   398,   399,   400,   401,   402,   403,   404,
     405,   406,   407
};
# endif

#define YYPACT_NINF -264

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-264)))

#define YYTABLE_NINF -1

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
     671,  -143,  -143,  -264,  -264,  -264,  -264,  -143,  -123,  -114,
      -5,  -143,  -143,    40,   -15,  -143,  -143,  -143,   171,  -143,
     -12,   114,  -143,    35,     1,  -143,    -9,  -143,  -143,   203,
    -143,  -143,  -143,  -143,  -143,   131,  -143,   115,    73,   215,
    -143,  -143,   219,   156,  -143,  -143,   226,  -143,  -143,   124,
     135,   121,  -143,   147,  -143,   159,  -143,   162,    39,  -143,
     229,   166,   235,   188,  -143,   127,   251,   197,  -143,   261,
      90,  -143,   165,   196,  -143,   207,   281,  -143,  -143,  -143,
     209,   365,   245,   287,   290,   309,  -143,   230,   363,  -143,
     364,   244,  -143,  -143,   374,  -143,  -143,   246,   293,   273,
      71,  -143,   304,  -143,  -143,  -143,  -143,   366,   276,  -143,
     305,  -143,  -143,  -143,  -143,   181,   375,  -143,  -143,  -143,
     307,  -143,    51,   380,   381,  -143,   285,   798,  -143,  -143,
    -143,  -264,  -264,   393,   523,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -143,  -143,  -264,  -264,  -264,  -143,  -143,  -264,
    -264,  -264,  -264,    12,  -143,  -264,  -143,  -264,  -143,  -143,
    -264,  -264,  -143,  -264,  -143,  -264,  -264,  -143,  -264,  -264,
    -143,  -143,    16,  -264,  -264,  -264,  -264,  -264,   288,  -143,
    -264,  -264,  -143,  -264,  -143,  -143,  -264,  -264,  -264,  -143,
    -264,  -143,  -143,  -264,  -264,  -264,  -143,  -264,  -264,  -264,
     327,  -264,   140,  -143,  -143,  -143,   147,  -264,  -264,    75,
    -264,   299,  -143,  -264,  -264,   302,  -143,  -264,  -143,  -264,
    -264,  -143,  -264,   376,  -143,  -264,   388,  -264,  -143,  -143,
    -143,   147,  -143,  -264,  -143,  -264,  -143,  -264,  -143,  -143,
     147,  -264,  -143,  -143,  -264,  -143,  -143,  -264,  -264,   336,
    -143,  -264,  -143,  -264,  -264,  -264,  -264,  -143,  -143,  -264,
    -143,  -143,   191,  -143,   272,  -264,   141,   137,  -143,  -264,
     338,  -143,  -264,  -143,  -264,    80,   343,  -143,  -264,  -264,
    -264,  -143,  -264,  -264,  -143,  -143,  -264,  -143,  -264,  -143,
    -143,  -264,  -143,  -264,    53,  -264,  -143,  -264,  -264,  -264,
    -264,  -264,  -143,   291,  -143,  -143,  -264,  -264,  -143,  -264,
    -264,  -264,  -264,  -264,   331,  -143,  -264,   362,  -264,  -264,
    -264,  -143,  -264,  -264,  -143,  -264,    46,   319,  -143,  -264,
      84,  -143,  -264,  -143,  -143,  -143,  -143,  -143,  -143,  -143,
    -143,  -143,  -143,  -143,  -143,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -143,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,   332,  -143,
    -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -143,
    -264,  -264,   391,  -264,  -264,  -264,   163,  -264,   333,  -143,
    -264,  -264,   334,  -143,  -264,  -264,  -264,  -264,   395,  -264,
    -143,  -264,  -264,  -264,   347,  -264,  -264,  -264,  -264,  -264,
     352,  -264,  -264,  -264,  -264,   345,  -143,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,   397,   287,  -264,  -143,
     346,  -264,  -264,   349,  -143,  -264,  -264,  -264,  -264,   147,
      57,   353,  -143,  -264,  -264,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -143,  -264,  -264,  -264,  -264,  -264,  -264,  -143,
    -264,  -264,  -143,   125,  -264,  -264,  -143,  -264,  -264,  -264,
     398,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,  -143,  -264,  -264,  -264,
    -143,  -264,  -143,  -264,  -264,  -143,  -264,  -264,  -143,  -264,
    -264,  -264,  -143,  -264,  -264,  -264,  -143,  -264,  -143,  -264,
    -143,  -264,  -264,   355,  -264,  -264,  -264,  -143,  -264,  -264,
    -264,  -264,  -264,  -143,  -264,  -143,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint16 yydefact[] =
{
     251,   251,   251,    53,    57,    54,    55,   251,    31,     0,
     251,   251,   251,     0,   251,   251,   251,   251,     0,   251,
     251,   251,   251,   251,   251,   251,     0,   251,   251,     0,
     251,   251,   251,   251,   251,   251,   251,   251,     0,   251,
     251,   251,   251,   251,   251,   251,   251,   251,   251,     0,
       0,   251,   251,     0,   251,   251,   251,   251,   251,   251,
     251,     0,   251,     0,   251,   251,   251,     0,   251,   251,
       0,   251,   251,   251,   251,   251,   251,   251,   251,   251,
     251,     0,     0,     0,     0,     0,   251,   251,     0,   251,
       0,   251,   251,   251,     0,   251,   251,   251,   251,   251,
       0,   251,   251,   251,   251,   251,   251,     0,   251,   251,
     251,   251,   251,   251,   251,   251,     0,   251,   251,   251,
     251,   251,   251,     0,     0,   251,   251,     0,   251,   251,
     251,    66,   250,     0,     2,     5,   248,    38,    39,   249,
      32,    33,   251,   251,   193,   239,    58,   251,   251,   110,
      73,    71,   222,   251,   251,   232,   251,    92,   251,   251,
     108,   238,   251,   124,   251,   199,    64,   251,   243,   221,
     251,   251,     0,    70,    49,   237,   231,    45,   251,   251,
     152,    41,   251,   195,   251,   251,   118,    63,   242,   251,
     189,   251,   251,   183,    69,   220,   251,   103,   230,    44,
     251,   258,     0,   251,   251,   251,     9,   236,   256,   251,
     227,   251,   251,   158,    26,   251,   251,   128,   251,   201,
      40,   251,   171,     0,   251,   105,     0,   235,   251,   251,
     251,    14,   251,   179,   251,    67,   251,    97,   251,   251,
       0,    61,   251,   251,    95,   251,   251,   177,    72,   251,
     251,   146,   251,   116,   234,   229,    75,   251,   251,   163,
     251,   251,     0,   251,   260,   262,     0,   251,   251,     8,
     251,   251,   140,   251,    25,     0,   251,   251,   134,   224,
      50,   251,    24,    52,   251,   251,   169,   251,   122,   251,
     251,   165,   251,   202,     0,    65,   251,   114,    74,    68,
     247,   219,   251,     0,   251,   251,   174,   240,   251,   197,
     226,   241,   246,   244,   251,   251,   101,     0,   233,   225,
     223,   251,   120,   228,   251,    43,   251,     0,   251,    62,
     251,   251,   215,   251,   251,   251,   251,   251,   251,   251,
     251,   251,   251,   251,   251,   245,    22,    23,     1,     3,
       4,   192,   191,    37,   109,   251,    47,    46,    91,   106,
     107,   123,   198,   180,   206,   205,   255,   207,   251,   251,
     151,   154,   194,    60,   117,   188,   181,   182,   102,   251,
     112,   257,     0,    11,    12,    10,     0,    34,   251,   251,
     157,   160,   251,   251,   127,   130,   200,   170,     0,   104,
     251,    16,    17,    15,     0,   178,   190,    96,    19,    20,
       0,    94,    93,   175,   176,   251,   251,   145,   148,   115,
     161,   162,   209,   208,   210,    35,     0,     0,   261,   251,
     251,   187,    51,   251,   251,   139,   142,    36,   254,     0,
     251,   251,   251,   133,   136,    56,   167,   168,   121,   164,
     166,   203,   251,   113,     6,     7,   172,   173,   196,   251,
      99,   100,   251,     0,   119,    42,   251,   211,   213,   214,
       0,   217,   216,    85,    83,    77,    82,    76,    81,    79,
      84,    87,    78,    86,    80,    48,   251,   149,   153,   111,
     251,    13,   251,   155,   159,   251,   125,   129,   251,    59,
      18,    21,   251,   143,   147,   259,   251,   186,   251,   185,
     251,   137,   141,     0,   252,   253,    27,   251,   131,   135,
     204,    98,    30,   251,   212,   251,   150,    90,   156,   126,
      88,   144,    89,   184,   138,    28,   132,    29,   218
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -264,  -264,  -264,   268,    -1,  -264,    86,  -264,  -263,  -264
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,   133,   134,   135,   136,   440,   172,   202,   265,   266
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_uint16 yytable[] =
{
     137,   138,   148,   428,   142,   156,   139,   132,   167,   144,
     145,   146,   143,   149,   150,   151,   152,   164,   155,   157,
     160,   161,   163,   165,   166,   366,   168,   169,   140,   173,
     174,   175,   176,   177,   180,   181,   183,   141,   186,   187,
     188,   190,   193,   194,   195,   197,   198,   199,   218,   147,
     206,   207,   162,   210,   213,   214,   217,   219,   220,   222,
     324,   225,   366,   227,   231,   233,   514,   235,   237,   240,
     241,   244,   247,   248,   251,   253,   254,   255,   256,   259,
     208,   355,   184,   367,   366,   269,   272,   292,   274,   438,
     278,   279,   280,   470,   282,   283,   286,   288,   291,   238,
     295,   297,   298,   299,   300,   301,   239,   306,   307,   309,
     310,   311,   312,   313,   316,   466,   318,   319,   320,   322,
     323,   325,   452,   158,   329,   332,   515,   345,   346,   347,
     203,   159,   182,   200,   366,   132,   228,   204,   132,   209,
     178,   351,   352,   229,   201,   132,   353,   354,   179,   381,
     264,   132,   356,   357,   429,   358,   208,   359,   360,   382,
     427,   361,   132,   362,   506,   191,   363,   262,   211,   364,
     365,   215,   366,   192,   242,   223,   212,   370,   371,   216,
     153,   372,   243,   373,   374,   132,   294,   154,   375,   132,
     376,   377,   314,   303,   523,   378,   132,   226,   315,   380,
     366,   132,   383,   384,   385,   245,   234,   132,   387,   327,
     390,   391,   170,   246,   394,   395,   249,   396,   257,   171,
     397,   491,   293,   399,   250,   132,   258,   401,   402,   403,
     132,   405,   185,   406,   132,   407,   189,   408,   409,   270,
     132,   411,   412,   196,   413,   414,   221,   271,   417,   418,
     430,   419,   224,   276,   263,   284,   420,   421,   424,   422,
     423,   277,   425,   285,   132,   132,   431,   432,   232,   435,
     436,   132,   437,   205,   439,   443,   444,   132,   236,   230,
     445,   132,   289,   446,   447,   304,   448,   132,   449,   450,
     290,   451,   386,   305,   330,   453,   264,   368,   252,   267,
     366,   454,   331,   456,   457,   369,   132,   458,   388,   132,
     287,   392,   132,   460,   461,   132,   389,   404,   268,   393,
     464,   296,   308,   465,   321,   467,   410,   469,   366,   471,
     472,   132,   473,   474,   475,   476,   477,   478,   479,   480,
     481,   482,   483,   484,   379,   415,   132,   433,   459,   486,
     492,   495,   441,   416,   485,   434,   366,   132,   455,   132,
     442,   366,   502,   508,   366,   132,   510,   487,   488,   132,
     517,   208,   273,   275,   260,   208,   132,   462,   489,   132,
     132,   261,   302,   281,   317,   132,   468,   493,   494,   326,
     328,   496,   497,   348,   132,   398,   132,   400,   426,   499,
     490,   132,   350,   463,   498,   500,   505,   525,     0,     0,
     501,   132,     0,   535,   503,   504,     0,     0,     0,     0,
       0,     0,     0,   132,     0,     0,   132,     0,   507,   509,
       0,   132,   511,   512,     0,   132,     0,     0,   132,   516,
     518,   519,     0,   132,     0,     0,     0,     0,     0,   132,
       0,   520,   132,     0,   132,   132,     0,   132,   521,     0,
       0,   522,     0,     0,     0,   524,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   132,     0,     0,
       0,   132,   132,   132,   132,   526,   132,     0,   132,   527,
       0,   528,     0,   132,   529,   132,   132,   530,     0,   132,
       0,   531,     0,   132,     0,   532,     0,   533,     0,   534,
       0,     0,     0,     0,     0,     0,   536,     0,     0,     0,
       0,     0,   537,     0,   538,   513,     1,     2,     3,     4,
       5,     6,     7,     0,     0,     0,     8,     9,     0,     0,
       0,    10,     0,    11,    12,    13,    14,    15,    16,    17,
      18,    19,    20,    21,    22,    23,    24,    25,    26,    27,
      28,    29,    30,    31,    32,    33,    34,    35,    36,    37,
       0,    38,    39,    40,    41,    42,    43,    44,    45,    46,
      47,     0,    48,    49,    50,    51,    52,    53,    54,    55,
     349,    56,     0,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    66,    67,     0,    68,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      93,    94,    95,    96,    97,    98,     0,    99,   100,     0,
     101,   102,   103,   104,   105,   106,   107,   108,   109,     0,
     110,   111,   112,   113,   114,   115,   116,   117,   118,   119,
     120,   121,   122,   123,   124,   125,   126,   127,   128,   129,
     130,   131,     0,   132,     1,     2,     3,     4,     5,     6,
       7,     0,     0,     0,     8,     9,     0,     0,     0,    10,
       0,    11,    12,    13,    14,    15,    16,    17,    18,    19,
      20,    21,    22,    23,    24,    25,    26,    27,    28,    29,
      30,    31,    32,    33,    34,    35,    36,    37,     0,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    47,     0,
      48,    49,    50,    51,    52,    53,    54,    55,     0,    56,
       0,    57,    58,    59,    60,    61,    62,    63,    64,    65,
      66,    67,     0,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,     0,    99,   100,     0,   101,   102,
     103,   104,   105,   106,   107,   108,   109,     0,   110,   111,
     112,   113,   114,   115,   116,   117,   118,   119,   120,   121,
     122,   123,   124,   125,   126,   127,   128,   129,   130,   131,
       0,   132,   333,   334,     0,     0,     0,     0,     0,     0,
       0,     0,   335,     0,     0,     0,     0,   336,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   337,     0,
       0,     0,   338,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     339,     0,     0,     0,     0,     0,   340,     0,     0,     0,
       0,   341,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,   342,     0,   343,   344
};

static const yytype_int16 yycheck[] =
{
       1,     2,    17,   266,     9,    17,     7,   150,    17,    10,
      11,    12,    17,    14,    15,    16,    17,    16,    19,    20,
      21,    22,    23,    24,    25,     9,    27,    28,   151,    30,
      31,    32,    33,    34,    35,    36,    37,   151,    39,    40,
      41,    42,    43,    44,    45,    46,    47,    48,     9,     9,
      51,    52,    17,    54,    55,    56,    57,    58,    59,    60,
       9,    62,     9,    64,    65,    66,     9,    68,    69,    70,
      71,    72,    73,    74,    75,    76,    77,    78,    79,    80,
       9,    69,     9,    67,     9,    86,    87,    16,    89,     9,
      91,    92,    93,     9,    95,    96,    97,    98,    99,     9,
     101,   102,   103,   104,   105,   106,    16,   108,   109,   110,
     111,   112,   113,   114,   115,    69,   117,   118,   119,   120,
     121,   122,    69,     9,   125,   126,    69,   128,   129,   130,
       9,    17,    17,     9,     9,   150,     9,    16,   150,    53,
       9,   142,   143,    16,     9,   150,   147,   148,    17,     9,
       9,   150,   153,   154,    17,   156,     9,   158,   159,    19,
      19,   162,   150,   164,   427,     9,   167,    81,     9,   170,
     171,     9,     9,    17,     9,     9,    17,   178,   179,    17,
       9,   182,    17,   184,   185,   150,   100,    16,   189,   150,
     191,   192,    11,   107,    69,   196,   150,     9,    17,   200,
       9,   150,   203,   204,   205,     9,     9,   150,   209,   123,
     211,   212,     9,    17,   215,   216,     9,   218,     9,    16,
     221,    58,   151,   224,    17,   150,    17,   228,   229,   230,
     150,   232,    17,   234,   150,   236,    17,   238,   239,     9,
     150,   242,   243,    17,   245,   246,    17,    17,   249,   250,
     113,   252,    17,     9,     9,     9,   257,   258,    67,   260,
     261,    17,   263,    17,   150,   150,   267,   268,    17,   270,
     271,   150,   273,   152,   275,   276,   277,   150,    17,   152,
     281,   150,     9,   284,   285,     9,   287,   150,   289,   290,
      17,   292,   206,    17,     9,   296,     9,     9,    17,     9,
       9,   302,    17,   304,   305,    17,   150,   308,     9,   150,
      17,     9,   150,   314,   315,   150,    17,   231,     9,    17,
     321,    17,    17,   324,    17,   326,   240,   328,     9,   330,
     331,   150,   333,   334,   335,   336,   337,   338,   339,   340,
     341,   342,   343,   344,    17,     9,   150,     9,    17,    17,
      17,    17,     9,    17,   355,    17,     9,   150,    67,   150,
      17,     9,    17,    17,     9,   150,    17,   368,   369,   150,
      17,     9,     9,     9,     9,     9,   150,    15,   379,   150,
     150,    16,    16,     9,     9,   150,    67,   388,   389,     9,
       9,   392,   393,     0,   150,    19,   150,     9,   126,   400,
       9,   150,   134,   317,     9,    58,     9,     9,    -1,    -1,
      58,   150,    -1,    58,   415,   416,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,   150,    -1,    -1,   150,    -1,   429,   430,
      -1,   150,   433,   434,    -1,   150,    -1,    -1,   150,   440,
     441,   442,    -1,   150,    -1,    -1,    -1,    -1,    -1,   150,
      -1,   452,   150,    -1,   150,   150,    -1,   150,   459,    -1,
      -1,   462,    -1,    -1,    -1,   466,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,   150,    -1,    -1,
      -1,   150,   150,   150,   150,   486,   150,    -1,   150,   490,
      -1,   492,    -1,   150,   495,   150,   150,   498,    -1,   150,
      -1,   502,    -1,   150,    -1,   506,    -1,   508,    -1,   510,
      -1,    -1,    -1,    -1,    -1,    -1,   517,    -1,    -1,    -1,
      -1,    -1,   523,    -1,   525,   439,     3,     4,     5,     6,
       7,     8,     9,    -1,    -1,    -1,    13,    14,    -1,    -1,
      -1,    18,    -1,    20,    21,    22,    23,    24,    25,    26,
      27,    28,    29,    30,    31,    32,    33,    34,    35,    36,
      37,    38,    39,    40,    41,    42,    43,    44,    45,    46,
      -1,    48,    49,    50,    51,    52,    53,    54,    55,    56,
      57,    -1,    59,    60,    61,    62,    63,    64,    65,    66,
      67,    68,    -1,    70,    71,    72,    73,    74,    75,    76,
      77,    78,    79,    80,    -1,    82,    83,    84,    85,    86,
      87,    88,    89,    90,    91,    92,    93,    94,    95,    96,
      97,    98,    99,   100,   101,   102,   103,   104,   105,   106,
     107,   108,   109,   110,   111,   112,    -1,   114,   115,    -1,
     117,   118,   119,   120,   121,   122,   123,   124,   125,    -1,
     127,   128,   129,   130,   131,   132,   133,   134,   135,   136,
     137,   138,   139,   140,   141,   142,   143,   144,   145,   146,
     147,   148,    -1,   150,     3,     4,     5,     6,     7,     8,
       9,    -1,    -1,    -1,    13,    14,    -1,    -1,    -1,    18,
      -1,    20,    21,    22,    23,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    -1,    48,
      49,    50,    51,    52,    53,    54,    55,    56,    57,    -1,
      59,    60,    61,    62,    63,    64,    65,    66,    -1,    68,
      -1,    70,    71,    72,    73,    74,    75,    76,    77,    78,
      79,    80,    -1,    82,    83,    84,    85,    86,    87,    88,
      89,    90,    91,    92,    93,    94,    95,    96,    97,    98,
      99,   100,   101,   102,   103,   104,   105,   106,   107,   108,
     109,   110,   111,   112,    -1,   114,   115,    -1,   117,   118,
     119,   120,   121,   122,   123,   124,   125,    -1,   127,   128,
     129,   130,   131,   132,   133,   134,   135,   136,   137,   138,
     139,   140,   141,   142,   143,   144,   145,   146,   147,   148,
      -1,   150,    24,    25,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    34,    -1,    -1,    -1,    -1,    39,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    50,    -1,
      -1,    -1,    54,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      82,    -1,    -1,    -1,    -1,    -1,    88,    -1,    -1,    -1,
      -1,    93,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,   117,    -1,   119,   120
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     3,     4,     5,     6,     7,     8,     9,    13,    14,
      18,    20,    21,    22,    23,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    48,    49,
      50,    51,    52,    53,    54,    55,    56,    57,    59,    60,
      61,    62,    63,    64,    65,    66,    68,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    82,    83,
      84,    85,    86,    87,    88,    89,    90,    91,    92,    93,
      94,    95,    96,    97,    98,    99,   100,   101,   102,   103,
     104,   105,   106,   107,   108,   109,   110,   111,   112,   114,
     115,   117,   118,   119,   120,   121,   122,   123,   124,   125,
     127,   128,   129,   130,   131,   132,   133,   134,   135,   136,
     137,   138,   139,   140,   141,   142,   143,   144,   145,   146,
     147,   148,   150,   154,   155,   156,   157,   157,   157,   157,
     151,   151,     9,    17,   157,   157,   157,     9,    17,   157,
     157,   157,   157,     9,    16,   157,    17,   157,     9,    17,
     157,   157,    17,   157,    16,   157,   157,    17,   157,   157,
       9,    16,   159,   157,   157,   157,   157,   157,     9,    17,
     157,   157,    17,   157,     9,    17,   157,   157,   157,    17,
     157,     9,    17,   157,   157,   157,    17,   157,   157,   157,
       9,     9,   160,     9,    16,   152,   157,   157,     9,   159,
     157,     9,    17,   157,   157,     9,    17,   157,     9,   157,
     157,    17,   157,     9,    17,   157,     9,   157,     9,    16,
     152,   157,    17,   157,     9,   157,    17,   157,     9,    16,
     157,   157,     9,    17,   157,     9,    17,   157,   157,     9,
      17,   157,    17,   157,   157,   157,   157,     9,    17,   157,
       9,    16,   159,     9,     9,   161,   162,     9,     9,   157,
       9,    17,   157,     9,   157,     9,     9,    17,   157,   157,
     157,     9,   157,   157,     9,    17,   157,    17,   157,     9,
      17,   157,    16,   151,   159,   157,    17,   157,   157,   157,
     157,   157,    16,   159,     9,    17,   157,   157,    17,   157,
     157,   157,   157,   157,    11,    17,   157,     9,   157,   157,
     157,    17,   157,   157,     9,   157,     9,   159,     9,   157,
       9,    17,   157,    24,    25,    34,    39,    50,    54,    82,
      88,    93,   117,   119,   120,   157,   157,   157,     0,    67,
     156,   157,   157,   157,   157,    69,   157,   157,   157,   157,
     157,   157,   157,   157,   157,   157,     9,    67,     9,    17,
     157,   157,   157,   157,   157,   157,   157,   157,   157,    17,
     157,     9,    19,   157,   157,   157,   159,   157,     9,    17,
     157,   157,     9,    17,   157,   157,   157,   157,    19,   157,
       9,   157,   157,   157,   159,   157,   157,   157,   157,   157,
     159,   157,   157,   157,   157,     9,    17,   157,   157,   157,
     157,   157,   157,   157,    67,   157,   126,    19,   161,    17,
     113,   157,   157,     9,    17,   157,   157,   157,     9,   157,
     158,     9,    17,   157,   157,   157,   157,   157,   157,   157,
     157,   157,    69,   157,   157,    67,   157,   157,   157,    17,
     157,   157,    15,   159,   157,   157,    69,   157,    67,   157,
       9,   157,   157,   157,   157,   157,   157,   157,   157,   157,
     157,   157,   157,   157,   157,   157,    17,   157,   157,   157,
       9,    58,    17,   157,   157,    17,   157,   157,     9,   157,
      58,    58,    17,   157,   157,     9,   161,   157,    17,   157,
      17,   157,   157,   159,     9,    69,   157,    17,   157,   157,
     157,   157,   157,    69,   157,     9,   157,   157,   157,   157,
     157,   157,   157,   157,   157,    58,   157,   157,   157
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,   153,   154,   154,   155,   155,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     157,   157,   158,   158,   158,   159,   159,   160,   160,   161,
     161,   162,   162
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     2,     2,     1,     3,     3,     2,     2,
       3,     3,     3,     4,     2,     3,     3,     3,     4,     3,
       3,     4,     2,     2,     2,     2,     2,     4,     5,     5,
       4,     1,     2,     2,     3,     3,     3,     3,     2,     2,
       2,     2,     3,     2,     2,     2,     3,     3,     4,     2,
       2,     3,     2,     1,     1,     1,     3,     1,     2,     4,
       3,     2,     2,     2,     2,     2,     1,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     5,     5,
       5,     3,     2,     3,     3,     2,     3,     2,     4,     3,
       3,     2,     3,     2,     3,     2,     3,     3,     2,     3,
       2,     4,     3,     3,     2,     3,     2,     3,     2,     3,
       2,     3,     2,     3,     2,     4,     5,     3,     2,     4,
       3,     4,     5,     3,     2,     4,     3,     4,     5,     3,
       2,     4,     3,     4,     5,     3,     2,     4,     3,     4,
       5,     3,     2,     4,     3,     4,     5,     3,     2,     4,
       3,     3,     3,     2,     3,     2,     3,     3,     3,     2,
       3,     2,     3,     3,     2,     3,     3,     2,     3,     2,
       3,     3,     3,     2,     5,     4,     4,     3,     3,     2,
       3,     3,     3,     2,     3,     2,     3,     2,     3,     2,
       3,     2,     2,     3,     4,     3,     3,     3,     3,     3,
       3,     3,     4,     3,     3,     2,     3,     3,     5,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     1,     2,
       1,     0,     2,     2,     1,     2,     1,     2,     1,     3,
       1,     2,     1
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)                                \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;        \
          (Current).first_column = YYRHSLOC (Rhs, 1).first_column;      \
          (Current).last_line    = YYRHSLOC (Rhs, N).last_line;         \
          (Current).last_column  = YYRHSLOC (Rhs, N).last_column;       \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).first_line   = (Current).last_line   =              \
            YYRHSLOC (Rhs, 0).last_line;                                \
          (Current).first_column = (Current).last_column =              \
            YYRHSLOC (Rhs, 0).last_column;                              \
        }                                                               \
    while (0)
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K])


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL

/* Print *YYLOCP on YYO.  Private, do not rely on its existence. */

YY_ATTRIBUTE_UNUSED
static unsigned
yy_location_print_ (FILE *yyo, YYLTYPE const * const yylocp)
{
  unsigned res = 0;
  int end_col = 0 != yylocp->last_column ? yylocp->last_column - 1 : 0;
  if (0 <= yylocp->first_line)
    {
      res += YYFPRINTF (yyo, "%d", yylocp->first_line);
      if (0 <= yylocp->first_column)
        res += YYFPRINTF (yyo, ".%d", yylocp->first_column);
    }
  if (0 <= yylocp->last_line)
    {
      if (yylocp->first_line < yylocp->last_line)
        {
          res += YYFPRINTF (yyo, "-%d", yylocp->last_line);
          if (0 <= end_col)
            res += YYFPRINTF (yyo, ".%d", end_col);
        }
      else if (0 <= end_col && yylocp->first_column < end_col)
        res += YYFPRINTF (yyo, "-%d", end_col);
    }
  return res;
 }

#  define YY_LOCATION_PRINT(File, Loc)          \
  yy_location_print_ (File, &(Loc))

# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value, Location); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  YYUSE (yylocationp);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  YY_LOCATION_PRINT (yyoutput, *yylocationp);
  YYFPRINTF (yyoutput, ": ");
  yy_symbol_value_print (yyoutput, yytype, yyvaluep, yylocationp);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, YYLTYPE *yylsp, int yyrule)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                       , &(yylsp[(yyi + 1) - (yynrhs)])                       );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, yylsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep, YYLTYPE *yylocationp)
{
  YYUSE (yyvaluep);
  YYUSE (yylocationp);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Location data for the lookahead symbol.  */
YYLTYPE yylloc
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
  = { 1, 1, 1, 1 }
# endif
;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.
       'yyls': related to locations.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    /* The location stack.  */
    YYLTYPE yylsa[YYINITDEPTH];
    YYLTYPE *yyls;
    YYLTYPE *yylsp;

    /* The locations where the error started and ended.  */
    YYLTYPE yyerror_range[3];

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;
  YYLTYPE yyloc;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N), yylsp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yylsp = yyls = yylsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  yylsp[0] = yylloc;
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;
        YYLTYPE *yyls1 = yyls;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yyls1, yysize * sizeof (*yylsp),
                    &yystacksize);

        yyls = yyls1;
        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
        YYSTACK_RELOCATE (yyls_alloc, yyls);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;
      yylsp = yyls + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END
  *++yylsp = yylloc;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];

  /* Default location.  */
  YYLLOC_DEFAULT (yyloc, (yylsp - yylen), yylen);
  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 6:
#line 106 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].file), "r"); CHECK;
              hfst::xfst::xfst_->add_props(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].file));
	    }
	    CHECK;
       }
#line 2152 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 7:
#line 115 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->add_props((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2161 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 8:
#line 119 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hxfsterror("NETWORK PROPERTY EDITOR unimplemented\n");
            return EXIT_FAILURE;
       }
#line 2170 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 9:
#line 124 "xfst-parser.yy" /* yacc.c:1646  */
    {
       	    hfst::xfst::xfst_->apply_up(stdin); CHECK;
       }
#line 2178 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 10:
#line 127 "xfst-parser.yy" /* yacc.c:1646  */
    {
       	    hfst::xfst::xfst_->apply_up((yyvsp[-1].text)); CHECK; free((yyvsp[-1].text));
       }
#line 2186 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 11:
#line 130 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_up((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2195 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 12:
#line 134 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].file), "r"); CHECK;
              hfst::xfst::xfst_->apply_up(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].file));
	    }
	    CHECK;
       }
#line 2209 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 13:
#line 143 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_up((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2218 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 14:
#line 147 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_down(stdin); CHECK;
       }
#line 2226 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 15:
#line 150 "xfst-parser.yy" /* yacc.c:1646  */
    {
       	    hfst::xfst::xfst_->apply_down((yyvsp[-1].text)); CHECK; free((yyvsp[-1].text));
       }
#line 2234 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 16:
#line 153 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_down((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2243 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 17:
#line 157 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].file), "r"); CHECK;
              hfst::xfst::xfst_->apply_down(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].file));
	    }
	    CHECK;
       }
#line 2257 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 18:
#line 166 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_down((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2266 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 19:
#line 170 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_med((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2275 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 20:
#line 174 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].file), "r"); CHECK;
              hfst::xfst::xfst_->apply_med(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].file));
	    }
	    CHECK;
       }
#line 2289 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 21:
#line 183 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apply_med((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2298 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 22:
#line 187 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->lookup_optimize(); CHECK;
       }
#line 2306 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 23:
#line 190 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->remove_optimization(); CHECK;
       }
#line 2314 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 24:
#line 194 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hxfsterror("unimplemetend ambiguous\n");
            return EXIT_FAILURE;
       }
#line 2323 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 25:
#line 198 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hxfsterror("unimplemetend ambiguous\n");
            return EXIT_FAILURE;
       }
#line 2332 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 26:
#line 202 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hxfsterror("unimplemetend ambiguous\n");
            return EXIT_FAILURE;
       }
#line 2341 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 27:
#line 207 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define_alias((yyvsp[-2].name), (yyvsp[-1].text));
            free((yyvsp[-2].name));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2351 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 28:
#line 212 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define_alias((yyvsp[-3].name), (yyvsp[-1].text));
            free((yyvsp[-3].name));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2361 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 29:
#line 217 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define_list((yyvsp[-3].name), (yyvsp[-2].text));
            free((yyvsp[-3].name));
            free((yyvsp[-2].text)); CHECK;
       }
#line 2371 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 30:
#line 222 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define_list((yyvsp[-2].name), (yyvsp[-1].list)[0], (yyvsp[-1].list)[1]);
            free((yyvsp[-2].name));
            free((yyvsp[-1].list)[0]);
            free((yyvsp[-1].list)[1]);
            free((yyvsp[-1].list)); CHECK;
       }
#line 2383 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 31:
#line 229 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define((yyvsp[0].name));
            free((yyvsp[0].name)); CHECK;
       }
#line 2392 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 32:
#line 233 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define((yyvsp[-1].name), (yyvsp[0].text));
            free((yyvsp[-1].name));
            free((yyvsp[0].text)); CHECK;
       }
#line 2402 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 33:
#line 238 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->define_function((yyvsp[-1].name), (yyvsp[0].text));
            free((yyvsp[-1].name));
            free((yyvsp[0].text)); CHECK;
       }
#line 2412 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 34:
#line 243 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->undefine((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2421 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 35:
#line 247 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->unlist((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2430 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 36:
#line 251 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->name_net((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2439 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 37:
#line 255 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->load_definitions((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2448 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 38:
#line 260 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->apropos((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2457 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 39:
#line 264 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->describe((yyvsp[-1].text)); CHECK;
       }
#line 2465 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 40:
#line 268 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->clear(); CHECK;
       }
#line 2473 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 41:
#line 271 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->pop(); CHECK;
       }
#line 2481 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 42:
#line 274 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->push((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2490 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 43:
#line 278 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->push(); CHECK;
       }
#line 2498 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 44:
#line 281 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->turn(); CHECK;
       }
#line 2506 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 45:
#line 284 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->rotate(); CHECK;
       }
#line 2514 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 46:
#line 287 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->load_stack((yyvsp[-1].file));
            free((yyvsp[-1].file)); CHECK;
       }
#line 2523 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 47:
#line 291 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->load_stack((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2532 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 48:
#line 295 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->load_stack((yyvsp[-2].name));
            free((yyvsp[-2].name)); CHECK;
       }
#line 2541 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 49:
#line 300 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->collect_epsilon_loops(); CHECK;
       }
#line 2549 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 50:
#line 303 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->compact_sigma(); CHECK;
       }
#line 2557 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 51:
#line 307 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->eliminate_flag((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2566 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 52:
#line 311 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->eliminate_flags(); CHECK;
       }
#line 2574 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 53:
#line 315 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->echo((yyvsp[0].text));
            free((yyvsp[0].text)); CHECK;
       }
#line 2583 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 54:
#line 319 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->quit((yyvsp[0].text));
            free((yyvsp[0].text));
            return EXIT_SUCCESS;
       }
#line 2593 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 55:
#line 324 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->hfst((yyvsp[0].text));
            free((yyvsp[0].text)); CHECK;
       }
#line 2602 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 56:
#line 328 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hxfsterror("source not implemented yywrap\n");
            free((yyvsp[-1].name));
            return EXIT_FAILURE;
       }
#line 2612 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 57:
#line 333 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->system((yyvsp[0].text));
            free((yyvsp[0].text)); CHECK;
       }
#line 2621 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 58:
#line 337 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->view_net(); CHECK;
            //hxfsterror("view not implemented\n");
            //return EXIT_FAILURE;
       }
#line 2631 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 59:
#line 343 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->set((yyvsp[-2].name), i);
            else
              hfst::xfst::xfst_->set((yyvsp[-2].name), (yyvsp[-1].name));
            free((yyvsp[-2].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2645 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 60:
#line 352 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->show((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2654 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 61:
#line 356 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->show(); CHECK;
       }
#line 2662 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 62:
#line 359 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->twosided_flags(); CHECK;
       }
#line 2670 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 63:
#line 363 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_eq(); CHECK;
       }
#line 2678 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 64:
#line 366 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_funct(); CHECK;
       }
#line 2686 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 65:
#line 369 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_id(); CHECK;
       }
#line 2694 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 66:
#line 372 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_infinitely_ambiguous(); CHECK;
       }
#line 2702 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 67:
#line 375 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_lower_bounded(); CHECK;
       }
#line 2710 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 68:
#line 378 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_lower_uni(); CHECK;
       }
#line 2718 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 69:
#line 381 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_upper_bounded(); CHECK;
       }
#line 2726 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 70:
#line 384 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_upper_uni(); CHECK;
       }
#line 2734 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 71:
#line 387 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_nonnull(); CHECK;
       }
#line 2742 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 72:
#line 390 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_null(); CHECK;
       }
#line 2750 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 73:
#line 393 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_overlap(); CHECK;
       }
#line 2758 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 74:
#line 396 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_sublanguage(); CHECK;
       }
#line 2766 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 75:
#line 399 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_unambiguous(); CHECK;
       }
#line 2774 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 76:
#line 403 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_eq(true); CHECK;
       }
#line 2782 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 77:
#line 406 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_funct(true); CHECK;
       }
#line 2790 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 78:
#line 409 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_id(true); CHECK;
       }
#line 2798 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 79:
#line 412 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_lower_bounded(true); CHECK;
       }
#line 2806 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 80:
#line 415 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_lower_uni(true); CHECK;
       }
#line 2814 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 81:
#line 418 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_upper_bounded(true); CHECK;
       }
#line 2822 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 82:
#line 421 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_upper_uni(true); CHECK;
       }
#line 2830 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 83:
#line 424 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_nonnull(true); CHECK;
       }
#line 2838 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 84:
#line 427 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_null(true); CHECK;
       }
#line 2846 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 85:
#line 430 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_overlap(true); CHECK;
       }
#line 2854 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 86:
#line 433 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_sublanguage(true); CHECK;
       }
#line 2862 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 87:
#line 436 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->test_unambiguous(true); CHECK;
       }
#line 2870 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 88:
#line 440 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->substitute_named((yyvsp[-3].name), (yyvsp[-1].name)); // TODO!
            free((yyvsp[-3].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2880 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 89:
#line 445 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->substitute_label((yyvsp[-3].text), (yyvsp[-1].text));
            free((yyvsp[-3].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 2890 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 90:
#line 450 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->substitute_symbol((yyvsp[-3].text), (yyvsp[-1].name));
            free((yyvsp[-3].text));
            free((yyvsp[-1].name)); CHECK;
       }
#line 2900 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 91:
#line 456 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_aliases(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 2914 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 92:
#line 465 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_aliases(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 2922 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 93:
#line 468 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_arc_count(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 2936 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 94:
#line 477 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (strcmp((yyvsp[-1].name), "upper") && strcmp((yyvsp[-1].name), "lower"))
            {
                hxfsterror("should be upper or lower");
                free((yyvsp[-1].name));
                return EXIT_FAILURE;
            }
            hfst::xfst::xfst_->print_arc_count((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 2951 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 95:
#line 487 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_arc_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 2959 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 96:
#line 490 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
	      std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_defined(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 2973 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 97:
#line 499 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_defined(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 2981 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 98:
#line 502 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
	      std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_dir((yyvsp[-2].name), &oss);
              oss.close();
	    }
            free((yyvsp[-1].file)); CHECK;
       }
#line 2995 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 99:
#line 511 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_dir((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3004 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 100:
#line 515 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_dir("*", &oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3018 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 101:
#line 524 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_dir("*", &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3026 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 102:
#line 527 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
	      std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_file_info(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3040 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 103:
#line 536 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_file_info(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3048 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 104:
#line 539 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_flags(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3062 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 105:
#line 548 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_flags(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3070 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 106:
#line 551 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_labels((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3079 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 107:
#line 555 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
	      std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_labels(&oss);
              oss.close();
	      }
	      CHECK;
       }
#line 3093 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 108:
#line 564 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_labels(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3101 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 109:
#line 567 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_label_count(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3115 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 110:
#line 576 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_label_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3123 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 111:
#line 579 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_list((yyvsp[-2].name), &oss);
              oss.close();
	    }
            free((yyvsp[-2].name)); CHECK;
       }
#line 3137 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 112:
#line 588 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_list((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3146 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 113:
#line 592 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
	      std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_list(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3160 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 114:
#line 601 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_list(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3168 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 115:
#line 604 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_longest_string(&oss);
              //hfst::xfst::xfst_fclose(f, $2);
              oss.close();
	    }
            CHECK;
       }
#line 3183 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 116:
#line 614 "xfst-parser.yy" /* yacc.c:1646  */
    {
            //hfst::xfst::xfst_->print_longest_string(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_longest_string(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
#line 3193 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 117:
#line 619 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_longest_string_size(&oss);
              //hfst::xfst::xfst_fclose(f, $2);
              oss.close();
	    }
            CHECK;
       }
#line 3208 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 118:
#line 629 "xfst-parser.yy" /* yacc.c:1646  */
    {
            //hfst::xfst::xfst_->print_longest_string_size(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_longest_string_size(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
#line 3218 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 119:
#line 634 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_name(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3232 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 120:
#line 643 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_name(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3240 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 121:
#line 646 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_shortest_string(&oss);
              //hfst::xfst::xfst_fclose(f, $2);
              oss.close();
	    }
            CHECK;
       }
#line 3255 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 122:
#line 656 "xfst-parser.yy" /* yacc.c:1646  */
    {
            //hfst::xfst::xfst_->print_shortest_string(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_shortest_string(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
#line 3265 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 123:
#line 661 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_shortest_string_size(&oss);
              //hfst::xfst::xfst_fclose(f, $2);
              oss.close();
	    }
            CHECK;
       }
#line 3280 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 124:
#line 671 "xfst-parser.yy" /* yacc.c:1646  */
    {
            //hfst::xfst::xfst_->print_shortest_string_size(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_shortest_string_size(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
#line 3290 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 125:
#line 676 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_lower_words((yyvsp[-2].name), hfst::xfst::nametoken_to_number((yyvsp[-1].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-2].name)); free((yyvsp[-1].name)); CHECK;
       }
#line 3299 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 126:
#line 680 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_lower_words((yyvsp[-3].name), hfst::xfst::nametoken_to_number((yyvsp[-2].name)), &oss);
              //hfst::xfst::xfst_fclose(f, $4);
              oss.close();
	    }
	    free((yyvsp[-3].name)); free((yyvsp[-2].name));
            CHECK;
       }
#line 3315 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 127:
#line 691 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->print_lower_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_lower_words((yyvsp[-1].name), 0, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name));
            CHECK;
       }
#line 3329 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 128:
#line 700 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_lower_words(NULL, 0, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3337 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 129:
#line 703 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              int i = hfst::xfst::nametoken_to_number((yyvsp[-2].name));
              if (i != -1)
                hfst::xfst::xfst_->print_lower_words(NULL, i, &oss);
              else
                hfst::xfst::xfst_->print_lower_words((yyvsp[-2].name), 0, &oss);
              //hfst::xfst::xfst_fclose(f, $3);
              oss.close();
	    }
            free((yyvsp[-2].name));
            CHECK;
       }
#line 3357 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 130:
#line 718 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_lower_words(NULL, 0, &oss);
              //hfst::xfst::xfst_fclose(f, $2);
              oss.close();
	    }
            CHECK;
       }
#line 3372 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 131:
#line 728 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_random_lower((yyvsp[-2].name), hfst::xfst::nametoken_to_number((yyvsp[-1].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-2].name)); free((yyvsp[-1].name)); CHECK;
       }
#line 3381 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 132:
#line 732 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_random_lower((yyvsp[-3].name), hfst::xfst::nametoken_to_number((yyvsp[-2].name)), &oss);
              oss.close();
	      //hfst::xfst::xfst_fclose(f, $4);
	    }
	    free((yyvsp[-3].name)); free((yyvsp[-2].name));
            CHECK;
       }
#line 3397 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 133:
#line 743 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_lower(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_random_lower((yyvsp[-1].name), 15, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name));CHECK;
       }
#line 3410 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 134:
#line 751 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_random_lower(NULL, 15, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3418 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 135:
#line 754 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              int i = hfst::xfst::nametoken_to_number((yyvsp[-2].name));
              if (i != -1)
                hfst::xfst::xfst_->print_random_lower(NULL, i, &oss);
              else
                hfst::xfst::xfst_->print_random_lower((yyvsp[-2].name), 15, &oss);
              //hfst::xfst::xfst_fclose(f, $3);
              oss.close();
	    }
            free((yyvsp[-2].name)); CHECK;
       }
#line 3437 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 136:
#line 768 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_random_lower(NULL, 15, &oss);
              //hfst::xfst::xfst_fclose(f, $2);
              oss.close();
	    }
            CHECK;
       }
#line 3452 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 137:
#line 778 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_upper_words((yyvsp[-2].name), hfst::xfst::nametoken_to_number((yyvsp[-1].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-2].name)); CHECK;
       }
#line 3461 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 138:
#line 782 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_upper_words((yyvsp[-3].name), hfst::xfst::nametoken_to_number((yyvsp[-2].name)), &oss);
              //hfst::xfst::xfst_fclose(f, $4);
              oss.close();
	    }
	    free((yyvsp[-3].name)); free((yyvsp[-2].name));
            CHECK;
       }
#line 3477 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 139:
#line 793 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->print_upper_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_upper_words((yyvsp[-1].name), 0, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3490 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 140:
#line 801 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_upper_words(NULL, 0, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3498 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 141:
#line 804 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              int i = hfst::xfst::nametoken_to_number((yyvsp[-2].name));
              if (i != -1)
                hfst::xfst::xfst_->print_upper_words(NULL, i, &oss);
              else
                hfst::xfst::xfst_->print_upper_words((yyvsp[-2].name), 0, &oss);
              oss.close();
	    }
            free((yyvsp[-2].name)); CHECK;
       }
#line 3516 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 142:
#line 817 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_upper_words(NULL, 0, &oss);
              oss.close();
	    }
            CHECK;
       }
#line 3530 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 143:
#line 826 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_random_upper((yyvsp[-2].name), hfst::xfst::nametoken_to_number((yyvsp[-1].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-2].name)); free((yyvsp[-1].name)); CHECK;
       }
#line 3539 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 144:
#line 830 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_random_upper((yyvsp[-3].name), hfst::xfst::nametoken_to_number((yyvsp[-2].name)), &oss);
              oss.close();
	    }
	    free((yyvsp[-3].name)); free((yyvsp[-2].name));
            CHECK;
       }
#line 3554 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 145:
#line 840 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_upper(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_random_upper((yyvsp[-1].name), 15, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3567 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 146:
#line 848 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_random_upper(NULL, 15, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3575 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 147:
#line 851 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
            {
	      std::ofstream oss((yyvsp[-1].file));
              int i = hfst::xfst::nametoken_to_number((yyvsp[-2].name));
              if (i != -1)
                hfst::xfst::xfst_->print_random_upper(NULL, i, &oss);
              else
                hfst::xfst::xfst_->print_random_upper((yyvsp[-2].name), 15, &oss);
              oss.close();
	    }
            free((yyvsp[-2].name)); CHECK;
       }
#line 3593 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 148:
#line 864 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_random_upper(NULL, 15, &oss);
              oss.close();
	    }
            CHECK;
       }
#line 3607 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 149:
#line 873 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_words((yyvsp[-2].name), hfst::xfst::nametoken_to_number((yyvsp[-1].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-2].name)); free((yyvsp[-1].name)); CHECK;
       }
#line 3616 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 150:
#line 877 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_words((yyvsp[-3].name), hfst::xfst::nametoken_to_number((yyvsp[-2].name)), &oss);
              oss.close();
	    }
	    free((yyvsp[-3].name)); free((yyvsp[-2].name));
            CHECK;
       }
#line 3631 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 151:
#line 887 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->print_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_words((yyvsp[-1].name), 0, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3644 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 152:
#line 895 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_words(NULL, 0, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3652 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 153:
#line 898 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              int i = hfst::xfst::nametoken_to_number((yyvsp[-2].name));
              if (i != -1)
                hfst::xfst::xfst_->print_words(NULL, i, &oss);
              else
                hfst::xfst::xfst_->print_words((yyvsp[-2].name), 0, &oss);
              oss.close();
	    }
            free((yyvsp[-2].name)); CHECK;
       }
#line 3670 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 154:
#line 911 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_words(NULL, 0, &oss);
              oss.close();
	    }
            CHECK;
       }
#line 3684 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 155:
#line 920 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_random_words((yyvsp[-2].name), hfst::xfst::nametoken_to_number((yyvsp[-1].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-2].name)); free((yyvsp[-1].name)); CHECK;
       }
#line 3693 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 156:
#line 924 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_random_words((yyvsp[-3].name), hfst::xfst::nametoken_to_number((yyvsp[-2].name)), &oss);
              oss.close();
	    }
	    free((yyvsp[-3].name)); free((yyvsp[-2].name));
            CHECK;
       }
#line 3708 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 157:
#line 934 "xfst-parser.yy" /* yacc.c:1646  */
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[-1].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_random_words((yyvsp[-1].name), 15, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3721 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 158:
#line 942 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_random_words(NULL, 15, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3729 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 159:
#line 945 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              int i = hfst::xfst::nametoken_to_number((yyvsp[-2].name));
              if (i != -1)
                hfst::xfst::xfst_->print_random_words(NULL, i, &oss);
              else
                hfst::xfst::xfst_->print_random_words((yyvsp[-2].name), 15, &oss);
            oss.close();
	    }
            free((yyvsp[-2].name)); CHECK;
       }
#line 3747 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 160:
#line 958 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_random_words(NULL, 15, &oss);
              oss.close();
	    }
            CHECK;
       }
#line 3761 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 161:
#line 967 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_net((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3770 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 162:
#line 971 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_net(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3784 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 163:
#line 980 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_net(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3792 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 164:
#line 983 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_properties((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3801 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 165:
#line 987 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_properties(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3809 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 166:
#line 990 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_properties(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3823 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 167:
#line 999 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_sigma((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3832 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 168:
#line 1003 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_sigma(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3846 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 169:
#line 1012 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_sigma(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3854 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 170:
#line 1015 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_sigma_count(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3868 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 171:
#line 1024 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_sigma_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3876 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 172:
#line 1027 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (strcmp((yyvsp[-1].name), "upper") && strcmp((yyvsp[-1].name), "lower"))
            {
                free((yyvsp[-1].name));
                hxfsterror("must be upper or lower\n");
                return EXIT_FAILURE;
            }
            hfst::xfst::xfst_->print_sigma_word_count((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3891 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 173:
#line 1037 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_sigma_word_count(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3905 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 174:
#line 1046 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_sigma_word_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3913 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 175:
#line 1049 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_size((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3922 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 176:
#line 1053 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_size(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3936 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 177:
#line 1062 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_size(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3944 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 178:
#line 1065 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_stack(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3958 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 179:
#line 1074 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->print_stack(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 3966 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 180:
#line 1077 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->print_labelmaps(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 3980 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 181:
#line 1087 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_dot((yyvsp[-1].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[-1].name)); CHECK;
       }
#line 3989 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 182:
#line 1091 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->write_dot(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 4003 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 183:
#line 1100 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_dot(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 4011 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 184:
#line 1103 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_function((yyvsp[-3].name), (yyvsp[-1].file));
            free((yyvsp[-3].name)); CHECK;
       }
#line 4020 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 185:
#line 1107 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_function((yyvsp[-2].name), 0);
            free((yyvsp[-2].name)); CHECK;
       }
#line 4029 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 186:
#line 1111 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_definition((yyvsp[-2].name), (yyvsp[-1].file));
            free((yyvsp[-2].name)); CHECK;
       }
#line 4038 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 187:
#line 1115 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_definition((yyvsp[-1].name), 0);
            free((yyvsp[-1].name)); CHECK;
       }
#line 4047 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 188:
#line 1119 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_definitions((yyvsp[-1].file)); CHECK;
       }
#line 4055 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 189:
#line 1122 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_definitions(0); CHECK;
       }
#line 4063 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 190:
#line 1125 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_stack((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 4072 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 191:
#line 1129 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->write_prolog(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 4086 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 192:
#line 1138 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].name)))
	    {
              std::ofstream oss((yyvsp[-1].name));
              hfst::xfst::xfst_->write_prolog(&oss);
              oss.close();
	    }
	    free((yyvsp[-1].name)); CHECK;
       }
#line 4100 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 193:
#line 1147 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_prolog(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 4108 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 194:
#line 1150 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->write_spaced(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 4122 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 195:
#line 1159 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_spaced(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 4130 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 196:
#line 1162 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->write_text(&oss);
              oss.close();
	    }
	    CHECK;
       }
#line 4144 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 197:
#line 1171 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_text(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 4152 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 198:
#line 1175 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].file), "r"); CHECK;
              hfst::xfst::xfst_->read_props(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].file));
	    }
	    CHECK;
       }
#line 4166 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 199:
#line 1184 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_props(stdin); CHECK;
       }
#line 4174 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 200:
#line 1187 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].name)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].name), "r"); CHECK;
              hfst::xfst::xfst_->read_prolog(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].name));
	    }
	    free((yyvsp[-1].name)); CHECK;
       }
#line 4188 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 201:
#line 1196 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_prolog(stdin); CHECK;
       }
#line 4196 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 202:
#line 1199 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_regex((yyvsp[0].text));
            free((yyvsp[0].text)); CHECK;
       }
#line 4205 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 203:
#line 1203 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[-1].file), "r"); CHECK;
              hfst::xfst::xfst_->read_regex(f);
              hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[-1].file));
	    }
	    CHECK;
       }
#line 4219 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 204:
#line 1212 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_regex((yyvsp[-2].text));
            free((yyvsp[-2].text)); CHECK;
       }
#line 4228 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 205:
#line 1216 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_spaced_from_file((yyvsp[-1].file));
            free((yyvsp[-1].file)); CHECK;
       }
#line 4237 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 206:
#line 1220 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_spaced_from_file((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 4246 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 207:
#line 1224 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_spaced((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 4255 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 208:
#line 1228 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_text_from_file((yyvsp[-1].file));
            free((yyvsp[-1].file)); CHECK;
       }
#line 4264 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 209:
#line 1232 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_text_from_file((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 4273 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 210:
#line 1236 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_text((yyvsp[-1].text));
            free((yyvsp[-1].text)); CHECK;
       }
#line 4282 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 211:
#line 1240 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_lexc_from_file((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 4291 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 212:
#line 1244 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_lexc_from_file((yyvsp[-2].name));
            free((yyvsp[-2].name)); CHECK;
       }
#line 4300 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 213:
#line 1248 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_lexc_from_file(""); free((yyvsp[-1].text)); CHECK;
       }
#line 4308 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 214:
#line 1251 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->read_att_from_file((yyvsp[-1].name));
            free((yyvsp[-1].name)); CHECK;
       }
#line 4317 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 215:
#line 1255 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->write_att(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
#line 4325 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 216:
#line 1258 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].file)))
	    {
              std::ofstream oss((yyvsp[-1].file));
              hfst::xfst::xfst_->write_att(&oss);
              oss.close();
	    }
            free((yyvsp[-1].file)); CHECK;
       }
#line 4339 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 217:
#line 1267 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if (hfst::xfst::xfst_->check_filename((yyvsp[-1].name)))
	    {
              std::ofstream oss((yyvsp[-1].name));
              hfst::xfst::xfst_->write_att(&oss);
              oss.close();
	    }
            free((yyvsp[-1].name)); CHECK;
       }
#line 4353 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 218:
#line 1276 "xfst-parser.yy" /* yacc.c:1646  */
    {
            // todo: handle input and output symbol tables
	    if (hfst::xfst::xfst_->check_filename((yyvsp[-3].name)))
	    {
              std::ofstream oss((yyvsp[-3].name));
              hfst::xfst::xfst_->write_att(&oss);
              oss.close();
	    }
            free((yyvsp[-3].name)); free((yyvsp[-2].name)); free((yyvsp[-1].name)); CHECK;
       }
#line 4368 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 219:
#line 1287 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->cleanup_net(); CHECK;
       }
#line 4376 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 220:
#line 1290 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->complete_net(); CHECK;
       }
#line 4384 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 221:
#line 1293 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->compose_net(); CHECK;
       }
#line 4392 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 222:
#line 1296 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->concatenate_net(); CHECK;
       }
#line 4400 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 223:
#line 1299 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->minus_net(); CHECK;
       }
#line 4408 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 224:
#line 1302 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->crossproduct_net(); CHECK;
       }
#line 4416 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 225:
#line 1305 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->minimize_net(); CHECK;
       }
#line 4424 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 226:
#line 1308 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->determinize_net(); CHECK;
       }
#line 4432 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 227:
#line 1311 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->epsilon_remove_net(); CHECK;
       }
#line 4440 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 228:
#line 1314 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->prune_net(); CHECK;
       }
#line 4448 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 229:
#line 1317 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->ignore_net(); CHECK;
       }
#line 4456 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 230:
#line 1320 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->intersect_net(); CHECK;
       }
#line 4464 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 231:
#line 1323 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->inspect_net(); CHECK;
       }
#line 4472 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 232:
#line 1326 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->invert_net(); CHECK;
       }
#line 4480 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 233:
#line 1329 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->lower_side_net(); CHECK;
       }
#line 4488 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 234:
#line 1332 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->upper_side_net(); CHECK;
       }
#line 4496 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 235:
#line 1335 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->negate_net(); CHECK;
       }
#line 4504 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 236:
#line 1338 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->one_plus_net(); CHECK;
       }
#line 4512 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 237:
#line 1341 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->zero_plus_net(); CHECK;
       }
#line 4520 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 238:
#line 1344 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->optional_net(); CHECK;
       }
#line 4528 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 239:
#line 1347 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->reverse_net(); CHECK;
       }
#line 4536 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 240:
#line 1350 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->shuffle_net(); CHECK;
       }
#line 4544 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 241:
#line 1353 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->sigma_net(); CHECK;
       }
#line 4552 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 242:
#line 1356 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->sort_net(); CHECK;
       }
#line 4560 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 243:
#line 1359 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->substring_net(); CHECK;
       }
#line 4568 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 244:
#line 1362 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->union_net(); CHECK;
       }
#line 4576 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 245:
#line 1365 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->label_net(); CHECK;
       }
#line 4584 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 246:
#line 1368 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->compile_replace_lower_net(); CHECK;
       }
#line 4592 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 247:
#line 1371 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->compile_replace_upper_net(); CHECK;
       }
#line 4600 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 248:
#line 1374 "xfst-parser.yy" /* yacc.c:1646  */
    {
            hfst::xfst::xfst_->prompt(); CHECK;
       }
#line 4608 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 249:
#line 1377 "xfst-parser.yy" /* yacc.c:1646  */
    {
            if ( hfst::xfst::xfst_->unknown_command((yyvsp[-1].name)) != 0)
              {
                hxfsterror("Command not recognized.\n");
                free((yyvsp[-1].name));
                YYABORT;
              }
            free((yyvsp[-1].name));
       }
#line 4622 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 252:
#line 1390 "xfst-parser.yy" /* yacc.c:1646  */
    {
                    (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[-1].text))+strlen((yyvsp[0].name))+2));
                    char* r = (yyval.text);
                    char* s = (yyvsp[-1].text);
                    while (*s != '\0')
                    {
                        *r = *s;
                        r++;
                        s++;
                    }
                    *r = ' ';
                    r++;
                    s = (yyvsp[0].name);
                    while (*s != '\0')
                    {
                        *r = *s;
                        r++;
                        s++;
                    }
                    *r = '\0';
                    free((yyvsp[0].name));
                }
#line 4649 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 253:
#line 1412 "xfst-parser.yy" /* yacc.c:1646  */
    {
                    (yyval.text) = (yyvsp[-1].text);
                }
#line 4657 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 254:
#line 1415 "xfst-parser.yy" /* yacc.c:1646  */
    {
                    (yyval.text) = (yyvsp[0].name);
                }
#line 4665 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 255:
#line 1420 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[-1].text))+strlen((yyvsp[0].name))+2));
                char* s = (yyvsp[-1].text);
                char* r = (yyval.text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = ' ';
                r++;
                s = (yyvsp[0].name);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '\0';
                free((yyvsp[-1].text)); free((yyvsp[0].name));
             }
#line 4692 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 256:
#line 1442 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = (yyvsp[0].name);
             }
#line 4700 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 257:
#line 1447 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[-1].text))+strlen((yyvsp[0].name))+4));
                char* s = (yyvsp[-1].text);
                char* r = (yyval.text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = ' ';
                r++;
                s = (yyvsp[0].name);
                *r = '"';
                r++;
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '"';
                r++;
                *r = '\0';
                free((yyvsp[-1].text)); free((yyvsp[0].name));
             }
#line 4731 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 258:
#line 1473 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[0].name))+3));
                char* s = (yyvsp[0].name);
                char* r = (yyval.text);
                *r = '"';
                r++;
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '"';
                r++;
                *r = '\0';
                free((yyvsp[0].name));
             }
#line 4753 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 259:
#line 1492 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = strdup((std::string((yyvsp[-2].name)) + std::string(":") + std::string((yyvsp[0].name))).c_str());
                free((yyvsp[-2].name)); free((yyvsp[0].name));
                }
#line 4762 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 260:
#line 1496 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = (yyvsp[0].name);
                }
#line 4770 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 261:
#line 1501 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[-1].text))+strlen((yyvsp[0].text))+2));
                char* s = (yyvsp[-1].text);
                char* r = (yyval.text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = ' ';
                r++;
                s = (yyvsp[0].text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '\0';
                free((yyvsp[-1].text)); free((yyvsp[0].text));
             }
#line 4797 "xfst-parser.cc" /* yacc.c:1646  */
    break;

  case 262:
#line 1523 "xfst-parser.yy" /* yacc.c:1646  */
    {
                (yyval.text) = (yyvsp[0].text);
             }
#line 4805 "xfst-parser.cc" /* yacc.c:1646  */
    break;


#line 4809 "xfst-parser.cc" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;
  *++yylsp = yyloc;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }

  yyerror_range[1] = yylloc;

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval, &yylloc);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  yyerror_range[1] = yylsp[1-yylen];
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;

      yyerror_range[1] = *yylsp;
      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp, yylsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  yyerror_range[2] = yylloc;
  /* Using YYLLOC is tempting, but would change the location of
     the lookahead.  YYLOC is available though.  */
  YYLLOC_DEFAULT (yyloc, yyerror_range, 2);
  *++yylsp = yyloc;

  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, &yylloc);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp, yylsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 1527 "xfst-parser.yy" /* yacc.c:1906  */


// oblig. declarations
extern FILE* hxfstin;
int hxfstparse(void);

// gah, bison/flex error mechanism here
void
hxfsterror(const char* text)
{
    hfst::xfst::xfst_->error() << text << std::endl;
    hfst::xfst::xfst_->flush(&hfst::xfst::xfst_->error());
    //fprintf(stderr,  "%s\n", text);
}


// vim: set ft=yacc:
