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
#define YYPURE 1

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1


/* Substitute the variable and function names.  */
#define yyparse         xreparse
#define yylex           xrelex
#define yyerror         xreerror
#define yydebug         xredebug
#define yynerrs         xrenerrs


/* Copy the first part of user declarations.  */
#line 1 "xre_parse.yy" /* yacc.c:339  */

// Copyright (c) 2016 University of Helsinki
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 3 of the License, or (at your option) any later version.
// See the file COPYING included with this distribution for more
// information.

#define YYDEBUG 1

#include <stdio.h>
#include <assert.h>
#include <iostream>

#include "HfstTransducer.h"
#include "HfstInputStream.h"
#include "HfstXeroxRules.h"

using namespace hfst;
using hfst::HfstTransducer;
using namespace hfst::xeroxRules;
using namespace hfst::implementations;

#include "xre_utils.h"

namespace hfst {
  namespace xre {
    // number of characters read, used for scanning function definition xre for argument symbols
    extern unsigned int cr;
    extern bool harmonize_;
    extern bool harmonize_flags_;
    extern bool allow_extra_text_at_end;

    bool has_weight_been_zeroed = false; // to control how many times a warning is given
    float zero_weights(float f)
    {
        if ((! has_weight_been_zeroed) && (f != 0))
        {
            hfst::xre::warn("warning: ignoring weights in rule context\n");
            has_weight_been_zeroed = true;
        }
        return 0;
    }

    bool is_weighted()
    {
        return (hfst::xre::format == hfst::TROPICAL_OPENFST_TYPE ||
                hfst::xre::format == hfst::LOG_OPENFST_TYPE);
    }
  }
}

using hfst::xre::harmonize_;
using hfst::xre::harmonize_flags_;

union YYSTYPE;
struct yy_buffer_state;
typedef yy_buffer_state * YY_BUFFER_STATE;
typedef void * yyscan_t;

extern int xreparse(yyscan_t);
extern int xrelex_init (yyscan_t*);
extern YY_BUFFER_STATE xre_scan_string (const char *, yyscan_t);
extern void xre_delete_buffer (YY_BUFFER_STATE, yyscan_t);
extern int xrelex_destroy (yyscan_t);

extern int xreerror(yyscan_t, const char*);
extern int xreerror(const char*);
int xrelex ( YYSTYPE * , yyscan_t );


#line 146 "xre_parse.cc" /* yacc.c:339  */

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
#line 82 "xre_parse.yy" /* yacc.c:355  */


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


#line 378 "xre_parse.cc" /* yacc.c:355  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif



int xreparse (void * scanner);

#endif /* !YY_XRE_XRE_PARSE_HH_INCLUDED  */

/* Copy the second part of user declarations.  */

#line 394 "xre_parse.cc" /* yacc.c:358  */

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
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

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
#define YYFINAL  59
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   646

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  84
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  35
/* YYNRULES -- Number of rules.  */
#define YYNRULES  135
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  214

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   338

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
      75,    76,    77,    78,    79,    80,    81,    82,    83
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   174,   174,   176,   182,   189,   196,   200,   225,   229,
     233,   247,   252,   257,   335,   336,   337,   339,   346,   347,
     386,   399,   411,   420,   432,   448,   461,   470,   479,   489,
     499,   509,   516,   524,   534,   540,   548,   556,   589,   611,
     634,   640,   644,   648,   652,   658,   662,   666,   670,   674,
     678,   682,   686,   693,   694,   700,   704,   711,   713,   719,
     727,   736,   744,   753,   758,   768,   774,   782,   783,   787,
     792,   796,   802,   808,   812,   822,   823,   829,   830,   836,
     842,   850,   851,   865,   878,   888,   894,   900,   901,   904,
     907,   910,   913,   916,   919,   922,   926,   929,   935,   936,
     951,   952,   956,   961,   968,   975,   982,   988,   991,   997,
    1008,  1026,  1027,  1030,  1046,  1071,  1096,  1121,  1167,  1181,
    1186,  1194,  1202,  1206,  1212,  1262,  1263,  1267,  1271,  1274,
    1283,  1286,  1289,  1294,  1298,  1305
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 1
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "WEIGHT", "SYMBOL", "MULTICHAR_SYMBOL",
  "CURLY_BRACKETS", "CROSS_PRODUCT", "COMPOSITION", "LENIENT_COMPOSITION",
  "INTERSECTION", "MERGE_RIGHT_ARROW", "MERGE_LEFT_ARROW", "CENTER_MARKER",
  "MARKUP_MARKER", "SHUFFLE", "LEFT_RESTRICTION", "LEFT_ARROW",
  "RIGHT_ARROW", "LEFT_RIGHT_ARROW", "REPLACE_RIGHT", "REPLACE_LEFT",
  "OPTIONAL_REPLACE_RIGHT", "OPTIONAL_REPLACE_LEFT", "REPLACE_LEFT_RIGHT",
  "OPTIONAL_REPLACE_LEFT_RIGHT", "RTL_LONGEST_MATCH", "RTL_SHORTEST_MATCH",
  "LTR_LONGEST_MATCH", "LTR_SHORTEST_MATCH", "REPLACE_CONTEXT_UU",
  "REPLACE_CONTEXT_LU", "REPLACE_CONTEXT_UL", "REPLACE_CONTEXT_LL",
  "UNION", "MINUS", "UPPER_MINUS", "LOWER_MINUS", "UPPER_PRIORITY_UNION",
  "LOWER_PRIORITY_UNION", "IGNORING", "IGNORE_INTERNALLY", "LEFT_QUOTIENT",
  "COMMACOMMA", "COMMA", "BEFORE", "AFTER", "SUBSTITUTE_LEFT",
  "TERM_COMPLEMENT", "COMPLEMENT", "CONTAINMENT", "CONTAINMENT_ONCE",
  "CONTAINMENT_OPT", "REVERSE", "INVERT", "XRE_UPPER", "XRE_LOWER", "STAR",
  "PLUS", "CATENATE_N_TO_K", "CATENATE_N", "CATENATE_N_PLUS",
  "CATENATE_N_MINUS", "READ_BIN", "READ_TEXT", "READ_SPACED",
  "READ_PROLOG", "READ_RE", "FUNCTION_NAME", "LEFT_BRACKET",
  "RIGHT_BRACKET", "LEFT_PARENTHESIS", "RIGHT_PARENTHESIS",
  "LEFT_BRACKET_DOTTED", "RIGHT_BRACKET_DOTTED", "SUBVAL", "EPSILON_TOKEN",
  "ANY_TOKEN", "BOUNDARY_MARKER", "LEXER_ERROR", "END_OF_EXPRESSION",
  "PAIR_SEPARATOR", "QUOTED_LITERAL", "QUOTED_MULTICHAR_LITERAL",
  "$accept", "XRE", "REGEXP1", "REGEXP2", "SUB1", "SUB2", "SUB3",
  "REPLACE", "PARALLEL_RULES", "RULE", "MAPPINGPAIR_VECTOR", "MAPPINGPAIR",
  "CONTEXTS_WITH_MARK", "CONTEXTS_VECTOR", "CONTEXT", "CONTEXT_MARK",
  "REPLACE_ARROW", "REGEXP3", "REGEXP4", "RESTR_CONTEXTS_VECTOR",
  "RESTR_CONTEXT", "REGEXP5", "REGEXP6", "REGEXP7", "REGEXP8", "REGEXP9",
  "REGEXP10", "REGEXP11", "SYMBOL_LIST", "REGEXP12", "LABEL",
  "SYMBOL_OR_QUOTED", "HALFARC", "REGEXP_LIST", "FUNCTION", YY_NULLPTR
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
     335,   336,   337,   338
};
# endif

#define YYPACT_NINF -124

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-124)))

#define YYTABLE_NINF -1

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
     177,  -124,  -124,   -70,   -53,    13,   457,   137,   457,   457,
    -124,  -124,  -124,  -124,  -124,  -124,   177,   177,   217,  -124,
    -124,  -124,  -124,  -124,    26,  -124,    21,    83,   610,   -22,
    -124,   124,  -124,    28,   130,   277,   457,   150,  -124,   566,
    -124,  -124,  -124,    24,  -124,   -47,   177,   467,   377,  -124,
    -124,   457,  -124,  -124,  -124,    33,    46,   610,   490,  -124,
     377,   377,   377,   377,   377,  -124,   274,   -35,  -124,  -124,
    -124,  -124,  -124,  -124,  -124,  -124,   257,   377,  -124,  -124,
    -124,  -124,   377,  -124,   297,   457,   457,   457,   457,   417,
     457,   457,   457,   457,   457,   457,   457,   457,   150,   457,
     457,   457,  -124,  -124,  -124,  -124,  -124,  -124,  -124,  -124,
    -124,  -124,  -124,   485,   265,   -34,  -124,   177,  -124,   100,
    -124,    12,  -124,   377,   610,   610,   610,   610,   610,   610,
    -124,  -124,   314,  -124,  -124,    83,   377,   337,   589,   610,
    -124,  -124,   377,   579,    -9,  -124,   130,   130,   130,   399,
     457,    81,    -7,  -124,   559,   457,   457,   457,   457,   457,
     457,   457,  -124,  -124,  -124,  -124,   177,  -124,   177,  -124,
     167,  -124,  -124,   497,   610,   377,  -124,  -124,     3,   610,
     610,   561,   377,   610,   377,   297,   457,   130,   457,   417,
     457,   186,   265,  -124,  -124,   177,  -124,   610,    83,   610,
     610,   610,  -124,   277,   130,  -124,   277,  -124,   227,   -25,
    -124,    83,   -11,  -124
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       3,   125,   126,   122,     0,     0,     0,     0,     0,     0,
     113,   114,   115,   116,   117,   135,     0,     0,     0,   130,
     131,   132,   128,   127,     0,     2,     5,     0,     6,    19,
      21,    22,    25,    18,    53,    57,    67,    75,    77,    81,
      87,    98,   100,   111,   129,   118,     0,     0,     0,    99,
      82,     0,    83,    85,    86,     0,     0,     0,     0,     1,
       0,     0,     0,     0,     0,     4,     0,     0,    45,    51,
      46,    52,    47,    48,    49,    50,     0,     0,    41,    42,
      43,    44,     0,    23,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    76,     0,
       0,     0,    90,    91,    92,    93,    88,    89,    97,    94,
      95,    96,   112,     0,   134,     0,   123,     0,   121,     0,
      84,   101,   108,     0,     0,     8,     7,     9,    10,    11,
      17,    13,     0,   109,    15,     0,     0,     0,    26,     0,
      20,    24,    40,     0,    34,    35,    54,    55,    56,     0,
      66,     0,    58,    61,     0,    69,    68,    70,    71,    72,
      73,    74,    78,    79,    80,   120,     0,   119,     0,   124,
       0,    14,   107,     0,    30,     0,    16,   110,     0,    29,
      32,     0,    28,    39,    38,     0,     0,    65,    64,     0,
       0,     0,   133,   104,   103,     0,   105,    31,     0,    33,
      27,    37,    36,    59,    63,    62,    60,   106,     0,     0,
     102,     0,     0,    12
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -124,  -124,  -124,   -15,  -124,  -124,  -124,   -12,  -124,   -17,
    -124,   -20,  -124,  -124,  -122,  -124,   -49,  -124,   -82,  -124,
    -123,   -76,   549,   -23,    16,  -124,    64,  -124,  -124,  -124,
    -124,  -124,   -27,  -124,  -124
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,    24,    25,    26,    27,    66,   131,    28,    29,    30,
      31,    32,    83,   144,   145,    84,    76,    33,    34,   152,
     153,    35,    36,    37,    38,    39,    40,    41,   132,    42,
      43,    44,    45,   115,    46
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_uint8 yytable[] =
{
      67,    55,    56,   146,   147,   148,    58,   151,   123,   134,
     168,    47,   149,    98,   154,   172,    48,     1,     2,     3,
     118,    77,    50,    52,    53,    54,    59,   112,    60,    61,
      62,   114,    63,    64,   113,   185,   119,   189,   169,   133,
      60,    61,    62,    85,    63,    64,   135,   198,   125,   126,
     127,   128,   129,    60,    61,    62,   211,    63,    64,   213,
     140,     5,   141,   202,   138,   139,   205,   120,   187,    49,
     139,     0,   143,    86,    87,   175,    10,    11,    12,    13,
      14,    15,    16,     0,    17,     0,   167,     1,     2,    19,
      20,    21,     0,   173,   188,    22,    23,     0,    88,    89,
      90,    65,   170,   121,     0,   177,   204,   151,   178,     0,
     203,   174,     0,     0,   206,   162,   163,   164,   122,     0,
      68,    69,    70,    71,   179,   181,    72,    73,    74,    75,
     183,   123,    98,    98,    98,    98,    98,    98,    98,     0,
      51,     1,     2,     3,   171,     0,   196,    88,    89,    90,
     175,   191,     0,   192,    78,    79,    80,    81,     0,    19,
      20,    21,     0,   197,     0,    22,    23,     0,    82,     0,
     200,   209,   201,   143,    60,    61,    62,     0,    63,    64,
     208,     1,     2,     3,   212,     5,     6,     7,     8,     9,
      99,   100,   101,    60,    61,    62,     0,    63,    64,     0,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     0,
       0,     0,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     1,     2,     3,     4,     5,     6,     7,     8,     9,
       0,     0,     0,     0,    60,    61,    62,   193,    63,    64,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     0,
      18,     0,     0,    19,    20,    21,   207,     0,     0,    22,
      23,     1,     2,     3,     0,     5,     6,     7,     8,     9,
       0,   136,    60,    61,    62,     0,    63,    64,     1,     2,
      10,    11,    12,    13,    14,    15,    16,    91,    17,     0,
      18,    57,     0,    19,    20,    21,     0,   210,     0,    22,
      23,     1,     2,     3,     0,     5,     6,     7,     8,     9,
     142,    92,    93,    94,    95,    96,    97,     0,     1,     2,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     0,
     137,     0,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     1,     2,     3,   130,     5,     6,     7,     8,     9,
      19,    20,    21,     0,     0,     0,    22,    23,     0,     0,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     0,
      18,     0,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     1,     2,     3,   176,     5,     6,     7,     8,     9,
      19,    20,    21,     0,     0,     0,    22,    23,     0,     0,
      10,    11,    12,    13,    14,    15,    16,     0,    17,    91,
      18,   180,   186,    19,    20,    21,     0,     0,     0,    22,
      23,     1,     2,     3,     0,     5,     6,     7,     8,     9,
     150,     0,     0,    92,    93,    94,    95,    96,    97,     0,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     0,
      18,     0,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     1,     2,     3,     0,     5,     6,     7,     8,     9,
       0,     1,     2,   116,     0,     0,     0,     0,     0,     0,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     1,
       2,   165,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     1,     2,   194,     0,     5,     6,     7,     8,     9,
      68,    69,    70,    71,     0,     0,    72,    73,    74,    75,
      10,    11,    12,    13,    14,    15,    16,     0,    17,     0,
       0,     0,     0,    19,    20,    21,   117,     0,     0,    22,
      23,     0,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     0,     0,     0,   166,     0,     0,     0,     0,     0,
       0,    19,    20,    21,   124,     0,   195,    22,    23,    91,
       0,     0,   190,    19,    20,    21,     0,     0,     0,    22,
      23,    68,    69,    70,    71,     0,     0,    72,    73,    74,
      75,     0,   184,    92,    93,    94,    95,    96,    97,    68,
      69,    70,    71,   182,     0,    72,    73,    74,    75,    68,
      69,    70,    71,     0,     0,    72,    73,    74,    75,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,     0,
      68,    69,    70,    71,     0,   199,    72,    73,    74,    75,
     155,   156,   157,   158,   159,   160,   161
};

static const yytype_int16 yycheck[] =
{
      27,    16,    17,    85,    86,    87,    18,    89,    57,    44,
      44,    81,    88,    36,    90,     3,    69,     4,     5,     6,
      47,    43,     6,     7,     8,     9,     0,     3,     7,     8,
       9,    46,    11,    12,    81,    44,    48,    44,    72,    66,
       7,     8,     9,    15,    11,    12,    81,    44,    60,    61,
      62,    63,    64,     7,     8,     9,    81,    11,    12,    70,
      77,    48,    82,   185,    76,    77,   189,    51,   150,     5,
      82,    -1,    84,    45,    46,   124,    63,    64,    65,    66,
      67,    68,    69,    -1,    71,    -1,   113,     4,     5,    76,
      77,    78,    -1,    81,    13,    82,    83,    -1,    17,    18,
      19,    80,   117,    70,    -1,   132,   188,   189,   135,    -1,
     186,   123,    -1,    -1,   190,    99,   100,   101,    72,    -1,
      20,    21,    22,    23,   136,   137,    26,    27,    28,    29,
     142,   180,   155,   156,   157,   158,   159,   160,   161,    -1,
       3,     4,     5,     6,    44,    -1,   173,    17,    18,    19,
     199,   166,    -1,   168,    30,    31,    32,    33,    -1,    76,
      77,    78,    -1,   175,    -1,    82,    83,    -1,    44,    -1,
     182,   198,   184,   185,     7,     8,     9,    -1,    11,    12,
     195,     4,     5,     6,   211,    48,    49,    50,    51,    52,
      40,    41,    42,     7,     8,     9,    -1,    11,    12,    -1,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    -1,
      -1,    -1,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,     4,     5,     6,    47,    48,    49,    50,    51,    52,
      -1,    -1,    -1,    -1,     7,     8,     9,    70,    11,    12,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    -1,
      73,    -1,    -1,    76,    77,    78,    70,    -1,    -1,    82,
      83,     4,     5,     6,    -1,    48,    49,    50,    51,    52,
      -1,    14,     7,     8,     9,    -1,    11,    12,     4,     5,
      63,    64,    65,    66,    67,    68,    69,    10,    71,    -1,
      73,    74,    -1,    76,    77,    78,    -1,    70,    -1,    82,
      83,     4,     5,     6,    -1,    48,    49,    50,    51,    52,
      13,    34,    35,    36,    37,    38,    39,    -1,     4,     5,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    -1,
      73,    -1,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,     4,     5,     6,    70,    48,    49,    50,    51,    52,
      76,    77,    78,    -1,    -1,    -1,    82,    83,    -1,    -1,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    -1,
      73,    -1,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,     4,     5,     6,    70,    48,    49,    50,    51,    52,
      76,    77,    78,    -1,    -1,    -1,    82,    83,    -1,    -1,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    10,
      73,    74,    13,    76,    77,    78,    -1,    -1,    -1,    82,
      83,     4,     5,     6,    -1,    48,    49,    50,    51,    52,
      13,    -1,    -1,    34,    35,    36,    37,    38,    39,    -1,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    -1,
      73,    -1,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,     4,     5,     6,    -1,    48,    49,    50,    51,    52,
      -1,     4,     5,     6,    -1,    -1,    -1,    -1,    -1,    -1,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,     4,
       5,     6,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,     4,     5,     6,    -1,    48,    49,    50,    51,    52,
      20,    21,    22,    23,    -1,    -1,    26,    27,    28,    29,
      63,    64,    65,    66,    67,    68,    69,    -1,    71,    -1,
      -1,    -1,    -1,    76,    77,    78,    69,    -1,    -1,    82,
      83,    -1,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,    -1,    -1,    -1,    69,    -1,    -1,    -1,    -1,    -1,
      -1,    76,    77,    78,    74,    -1,    69,    82,    83,    10,
      -1,    -1,    13,    76,    77,    78,    -1,    -1,    -1,    82,
      83,    20,    21,    22,    23,    -1,    -1,    26,    27,    28,
      29,    -1,    13,    34,    35,    36,    37,    38,    39,    20,
      21,    22,    23,    14,    -1,    26,    27,    28,    29,    20,
      21,    22,    23,    -1,    -1,    26,    27,    28,    29,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    -1,
      20,    21,    22,    23,    -1,    74,    26,    27,    28,    29,
      91,    92,    93,    94,    95,    96,    97
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     4,     5,     6,    47,    48,    49,    50,    51,    52,
      63,    64,    65,    66,    67,    68,    69,    71,    73,    76,
      77,    78,    82,    83,    85,    86,    87,    88,    91,    92,
      93,    94,    95,   101,   102,   105,   106,   107,   108,   109,
     110,   111,   113,   114,   115,   116,   118,    81,    69,   110,
     108,     3,   108,   108,   108,    87,    87,    74,    91,     0,
       7,     8,     9,    11,    12,    80,    89,   116,    20,    21,
      22,    23,    26,    27,    28,    29,   100,    43,    30,    31,
      32,    33,    44,    96,    99,    15,    45,    46,    17,    18,
      19,    10,    34,    35,    36,    37,    38,    39,   107,    40,
      41,    42,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,     3,    81,    87,   117,     6,    69,   116,    91,
     108,    70,    72,   100,    74,    91,    91,    91,    91,    91,
      70,    90,   112,   116,    44,    81,    14,    73,    91,    91,
      93,    95,    13,    91,    97,    98,   102,   102,   102,   105,
      13,   102,   103,   104,   105,   106,   106,   106,   106,   106,
     106,   106,   108,   108,   108,     6,    69,   116,    44,    72,
      87,    44,     3,    81,    91,   100,    70,   116,   116,    91,
      74,    91,    14,    91,    13,    44,    13,   102,    13,    44,
      13,    87,    87,    70,     6,    69,   116,    91,    44,    74,
      91,    91,    98,   105,   102,   104,   105,    70,    87,   116,
      70,    81,   116,    70
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    84,    85,    85,    86,    86,    87,    87,    87,    87,
      87,    87,    87,    87,    88,    89,    90,    90,    91,    91,
      92,    92,    93,    93,    94,    94,    95,    95,    95,    95,
      95,    95,    95,    95,    96,    97,    97,    98,    98,    98,
      98,    99,    99,    99,    99,   100,   100,   100,   100,   100,
     100,   100,   100,   101,   101,   101,   101,   102,   102,   102,
     102,   103,   103,   104,   104,   104,   104,   105,   105,   105,
     105,   105,   105,   105,   105,   106,   106,   107,   107,   107,
     107,   108,   108,   108,   108,   108,   108,   109,   109,   109,
     109,   109,   109,   109,   109,   109,   109,   109,   110,   110,
     111,   111,   111,   111,   111,   111,   111,   111,   111,   112,
     112,   113,   113,   113,   113,   113,   113,   113,   114,   114,
     114,   114,   114,   114,   114,   115,   115,   115,   115,   116,
     116,   116,   116,   117,   117,   118
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     0,     2,     1,     1,     3,     3,     3,
       3,     3,     9,     3,     4,     2,     2,     1,     1,     1,
       3,     1,     1,     2,     3,     1,     3,     5,     4,     4,
       4,     5,     4,     5,     2,     1,     3,     3,     2,     2,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     1,     3,     5,
       5,     1,     3,     3,     2,     2,     1,     1,     3,     3,
       3,     3,     3,     3,     3,     1,     2,     1,     3,     3,
       3,     1,     2,     2,     3,     2,     2,     1,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     1,     2,
       1,     3,     7,     5,     5,     5,     5,     4,     3,     1,
       2,     1,     2,     1,     1,     1,     1,     1,     1,     3,
       3,     3,     1,     3,     3,     1,     1,     1,     1,     1,
       1,     1,     1,     3,     1,     1
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
      yyerror (scanner, YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



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

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value, scanner); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, void * scanner)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  YYUSE (scanner);
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
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, void * scanner)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep, scanner);
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
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, int yyrule, void * scanner)
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
                                              , scanner);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule, scanner); \
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
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep, void * scanner)
{
  YYUSE (yyvaluep);
  YYUSE (scanner);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/*----------.
| yyparse.  |
`----------*/

int
yyparse (void * scanner)
{
/* The lookahead symbol.  */
int yychar;


/* The semantic value of the lookahead symbol.  */
/* Default value used for initialization, for pacifying older GCCs
   or non-GCC compilers.  */
YY_INITIAL_VALUE (static YYSTYPE yyval_default;)
YYSTYPE yylval YY_INITIAL_VALUE (= yyval_default);

    /* Number of syntax errors so far.  */
    int yynerrs;

    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

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

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
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

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yystacksize);

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
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

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
      yychar = yylex (&yylval, scanner);
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


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 2:
#line 174 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 1743 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 3:
#line 176 "xre_parse.yy" /* yacc.c:1646  */
    {
       // only comments
       hfst::xre::contains_only_comments = true;
       return 0;
     }
#line 1753 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 4:
#line 182 "xre_parse.yy" /* yacc.c:1646  */
    {
       hfst::xre::last_compiled = (yyvsp[-1].transducer);
       (yyval.transducer) = hfst::xre::last_compiled;
       if (hfst::xre::allow_extra_text_at_end) {
         return 0;
       }
   }
#line 1765 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 5:
#line 189 "xre_parse.yy" /* yacc.c:1646  */
    {
        hfst::xre::last_compiled = (yyvsp[0].transducer);
        (yyval.transducer) = hfst::xre::last_compiled;
   }
#line 1774 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 6:
#line 197 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[0].transducer)->optimize();
         }
#line 1782 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 7:
#line 201 "xre_parse.yy" /* yacc.c:1646  */
    {
        if ((yyvsp[-2].transducer)->has_flag_diacritics() && (yyvsp[0].transducer)->has_flag_diacritics())
          {
            if (! harmonize_flags_) {
                 hfst::xre::warn("warning: both composition arguments contain flag diacritics that are not harmonized\n");
            }
            else {
                (yyvsp[-2].transducer)->harmonize_flag_diacritics(*(yyvsp[0].transducer));
            }
          }

         try {
            (yyval.transducer) = & (yyvsp[-2].transducer)->compose(*(yyvsp[0].transducer), harmonize_).optimize();
         }
         catch (const FlagDiacriticsAreNotIdentitiesException & e)
             {
               (void)e;
               xreerror("Error: flag diacritics must be identities in composition if flag-is-epsilon is ON.\n"
               "I.e. only FLAG:FLAG is allowed, not FLAG1:FLAG2, FLAG:bar or foo:FLAG\n"
               "Apply twosided flag-diacritics (tfd) before composition.\n");
               YYABORT;
             }
            delete (yyvsp[0].transducer);
        }
#line 1811 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 8:
#line 225 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-2].transducer)->cross_product(*(yyvsp[0].transducer)).optimize();
            delete (yyvsp[0].transducer);
        }
#line 1820 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 9:
#line 229 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-2].transducer)->lenient_composition(*(yyvsp[0].transducer)).optimize();
            delete (yyvsp[0].transducer);
        }
#line 1829 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 10:
#line 233 "xre_parse.yy" /* yacc.c:1646  */
    {
          try {
            (yyval.transducer) = & hfst::xre::merge_first_to_second((yyvsp[-2].transducer), (yyvsp[0].transducer))->optimize();
          }
          catch (const TransducersAreNotAutomataException & e)
          {
            (void)e;
            xreerror("Error: transducers must be automata in merge operation.");
            delete (yyvsp[-2].transducer);
            delete (yyvsp[0].transducer);
            YYABORT;
          }
          delete (yyvsp[-2].transducer);
       }
#line 1848 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 11:
#line 247 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & hfst::xre::merge_first_to_second((yyvsp[0].transducer), (yyvsp[-2].transducer))->optimize();
            delete (yyvsp[0].transducer);
       }
#line 1857 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 12:
#line 252 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyvsp[-8].transducer)->substitute(StringPair((yyvsp[-7].label),(yyvsp[-5].label)), StringPair((yyvsp[-3].label),(yyvsp[-1].label)));
            (yyval.transducer) = & (yyvsp[-8].transducer)->optimize();
            free((yyvsp[-7].label)); free((yyvsp[-5].label)); free((yyvsp[-3].label)); free((yyvsp[-1].label));
       }
#line 1867 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 13:
#line 257 "xre_parse.yy" /* yacc.c:1646  */
    {

            StringSet alpha = (yyvsp[-2].transducer)->get_alphabet();
            if (hfst::xre::is_definition((yyvsp[-1].label)))
            {
                hfst::xre::warn("warning: using definition as an ordinary label, cannot substitute\n");
                (yyval.transducer) = & (yyvsp[-2].transducer)->optimize();
            }
            else if (alpha.find((yyvsp[-1].label)) == alpha.end())
            {
                (yyval.transducer) = & (yyvsp[-2].transducer)->optimize();
            }
            else
            {
                alpha = (yyvsp[0].transducer)->get_alphabet();

                StringPair tmp((yyvsp[-1].label), (yyvsp[-1].label));
                HfstTransducer * tmpTr = new HfstTransducer(*(yyvsp[-2].transducer));

	        bool empty_replace_transducer=false;
	        HfstTransducer empty(hfst::xre::format);
	        if (empty.compare(*(yyvsp[0].transducer)))
	        {
                        empty_replace_transducer=true;
	        }

	        if (empty_replace_transducer)
	        {
                        // substitute all transitions {b:a, a:b, b:b} with b:b
		        // as they will be removed anyway
		        hfst::xre::set_substitution_function_symbol((yyvsp[-1].label));
		        tmpTr->substitute(&hfst::xre::substitution_function);
	        }

                // `[ a:b, b, x y ]
                // substitute b with x | y
                tmpTr->substitute(tmp, *(yyvsp[0].transducer), false); // no harmonization

	        if (!empty_replace_transducer)
                {
                        // a:b .o. b -> x | y
                        // [[a:b].i .o. b -> x | y].i - this is for cases when b is on left side

	                // build Replace transducer
                        HfstTransducerPair mappingPair(HfstTransducer((yyvsp[-1].label), (yyvsp[-1].label), hfst::xre::format), *(yyvsp[0].transducer));
                        HfstTransducerPairVector mappingPairVector;
                        mappingPairVector.push_back(mappingPair);
                        Rule rule(mappingPairVector);
                        HfstTransducer replaceTr(hfst::xre::format);
                        replaceTr = replace(rule, false);

                        // if we are replacing with flag diacritics, the rule must allow
                        // flags to be replaced with themselves
                        StringSet alpha = (yyvsp[0].transducer)->get_alphabet();
                        for (StringSet::const_iterator it = alpha.begin(); it != alpha.end(); it++)
                        {
                          if (FdOperation::is_diacritic(*it))
                          {
                            replaceTr.insert_freely(StringPair(*it, *it), false);
                          }
                        }
                        replaceTr.optimize();

                        tmpTr->compose(replaceTr).optimize();
                        tmpTr->invert().compose(replaceTr).invert();
	        }
            
                if (alpha.find((yyvsp[-1].label)) == alpha.end())
                {
                  tmpTr->remove_from_alphabet((yyvsp[-1].label));
                }
                tmpTr->optimize();
                (yyval.transducer) = tmpTr;
                delete (yyvsp[-2].transducer); delete (yyvsp[-1].label); delete (yyvsp[0].transducer);
            }
         }
#line 1948 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 14:
#line 335 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[-1].transducer); }
#line 1954 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 15:
#line 336 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.label) = (yyvsp[-1].label); }
#line 1960 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 16:
#line 337 "xre_parse.yy" /* yacc.c:1646  */
    {  (yyval.transducer) = (yyvsp[-1].transducer);  }
#line 1966 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 17:
#line 339 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = new HfstTransducer(hfst::xre::format); }
#line 1972 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 18:
#line 346 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 1978 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 19:
#line 348 "xre_parse.yy" /* yacc.c:1646  */
    {
            switch ( (yyvsp[0].replaceRuleVectorWithArrow)->first )
            {
               case E_REPLACE_RIGHT:
                 (yyval.transducer) = new HfstTransducer( replace( (yyvsp[0].replaceRuleVectorWithArrow)->second, false ) );
                 break;
               case E_OPTIONAL_REPLACE_RIGHT:
                 (yyval.transducer) = new HfstTransducer( replace( (yyvsp[0].replaceRuleVectorWithArrow)->second, true ) );
                 break;
              case E_REPLACE_LEFT:
                 (yyval.transducer) = new HfstTransducer( replace_left( (yyvsp[0].replaceRuleVectorWithArrow)->second, false ) );
                 break;
               case E_OPTIONAL_REPLACE_LEFT:
                 (yyval.transducer) = new HfstTransducer( replace_left( (yyvsp[0].replaceRuleVectorWithArrow)->second, true ) );
                 break;
               case E_RTL_LONGEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_rightmost_longest_match( (yyvsp[0].replaceRuleVectorWithArrow)->second ) );
                 break;
               case E_RTL_SHORTEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_rightmost_shortest_match((yyvsp[0].replaceRuleVectorWithArrow)->second) );
                 break;
               case E_LTR_LONGEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_leftmost_longest_match( (yyvsp[0].replaceRuleVectorWithArrow)->second ) );
                 break;
               case E_LTR_SHORTEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_leftmost_shortest_match( (yyvsp[0].replaceRuleVectorWithArrow)->second ) );
                 break;
               case E_REPLACE_RIGHT_MARKUP:
               default:
                xreerror("Unhandled arrow stuff I suppose");
                YYABORT;
                break;
            }
       
            delete (yyvsp[0].replaceRuleVectorWithArrow);
         }
#line 2019 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 20:
#line 387 "xre_parse.yy" /* yacc.c:1646  */
    {
           //std::cerr << "parallel_rules: parallel_rules ,, rule"<< std::endl;
           if ((yyvsp[0].replaceRuleWithArrow)->first != (yyvsp[-2].replaceRuleVectorWithArrow)->first)
           {
             xreerror("Replace type mismatch in parallel rules");
             YYABORT;
           }
            Rule tmpRule((yyvsp[0].replaceRuleWithArrow)->second);
            (yyvsp[-2].replaceRuleVectorWithArrow)->second.push_back(tmpRule);
            (yyval.replaceRuleVectorWithArrow) =  new std::pair< ReplaceArrow, std::vector<Rule> > ((yyvsp[0].replaceRuleWithArrow)->first, (yyvsp[-2].replaceRuleVectorWithArrow)->second);
            delete (yyvsp[-2].replaceRuleVectorWithArrow); delete (yyvsp[0].replaceRuleWithArrow);
         }
#line 2036 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 21:
#line 400 "xre_parse.yy" /* yacc.c:1646  */
    {
         //std::cerr << "parallel_rules:rule"<< std::endl;
            std::vector<Rule> * ruleVector = new std::vector<Rule>();
            ruleVector->push_back((yyvsp[0].replaceRuleWithArrow)->second);
            
            (yyval.replaceRuleVectorWithArrow) =  new std::pair< ReplaceArrow, std::vector<Rule> > ((yyvsp[0].replaceRuleWithArrow)->first, *ruleVector);
            delete ruleVector;
            delete (yyvsp[0].replaceRuleWithArrow);
         }
#line 2050 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 22:
#line 412 "xre_parse.yy" /* yacc.c:1646  */
    {
         // std::cerr << "rule: mapping_vector"<< std::endl;
        // HfstTransducer allMappingsDisjuncted = disjunctVectorMembers($1->second);
         
         Rule rule( (yyvsp[0].mappingVectorWithArrow)->second );;
         (yyval.replaceRuleWithArrow) =  new std::pair< ReplaceArrow, Rule> ((yyvsp[0].mappingVectorWithArrow)->first, rule);
         delete (yyvsp[0].mappingVectorWithArrow);
      }
#line 2063 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 23:
#line 421 "xre_parse.yy" /* yacc.c:1646  */
    {
       //  std::cerr << "rule: mapping_vector contextsWM"<< std::endl;
     //   HfstTransducer allMappingsDisjuncted = disjunctVectorMembers($1->second);
        
        Rule rule( (yyvsp[-1].mappingVectorWithArrow)->second, (yyvsp[0].contextWithMark)->second, (yyvsp[0].contextWithMark)->first );
        (yyval.replaceRuleWithArrow) =  new std::pair< ReplaceArrow, Rule> ((yyvsp[-1].mappingVectorWithArrow)->first, rule);
        delete (yyvsp[-1].mappingVectorWithArrow); delete (yyvsp[0].contextWithMark);
      }
#line 2076 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 24:
#line 433 "xre_parse.yy" /* yacc.c:1646  */
    {
        // std::cerr << "mapping_vector : mapping_vector comma mapping"<< std::endl;
         // check if new Arrow is the same as the first one

         if ((yyvsp[-2].mappingVectorWithArrow)->first != (yyvsp[0].mappingWithArrow)->first)
         {
            hfst::xre::warn("Replace arrows should be the same. Calculated as if all replacements had the first arrow.");
         }
 
         (yyvsp[-2].mappingVectorWithArrow)->second.push_back((yyvsp[0].mappingWithArrow)->second);
         (yyval.mappingVectorWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPairVector> ((yyvsp[-2].mappingVectorWithArrow)->first, (yyvsp[-2].mappingVectorWithArrow)->second);
         delete (yyvsp[-2].mappingVectorWithArrow); delete (yyvsp[0].mappingWithArrow);
            
      }
#line 2095 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 25:
#line 449 "xre_parse.yy" /* yacc.c:1646  */
    {
         // std::cerr << "mapping_vector : mapping"<< std::endl;
         HfstTransducerPairVector * mappingPairVector = new HfstTransducerPairVector();
         mappingPairVector->push_back( (yyvsp[0].mappingWithArrow)->second );
         (yyval.mappingVectorWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPairVector> ((yyvsp[0].mappingWithArrow)->first, * mappingPairVector);
         delete mappingPairVector;
         delete (yyvsp[0].mappingWithArrow);
      }
#line 2108 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 26:
#line 462 "xre_parse.yy" /* yacc.c:1646  */
    {
	  hfst::xre::warn_about_special_symbols_in_replace((yyvsp[-2].transducer));
	  hfst::xre::warn_about_special_symbols_in_replace((yyvsp[0].transducer));
          HfstTransducerPair mappingPair(*(yyvsp[-2].transducer), *(yyvsp[0].transducer));
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-1].replaceArrow), mappingPair);

          delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
      }
#line 2121 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 27:
#line 471 "xre_parse.yy" /* yacc.c:1646  */
    {
          HfstTransducerPair marks(*(yyvsp[-2].transducer), *(yyvsp[0].transducer));
          HfstTransducerPair tmpMappingPair(*(yyvsp[-4].transducer), HfstTransducer(hfst::xre::format));
          HfstTransducerPair mappingPair = create_mapping_for_mark_up_replace( tmpMappingPair, marks );
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-3].replaceArrow), mappingPair);
          delete (yyvsp[-4].transducer); delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
      }
#line 2134 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 28:
#line 480 "xre_parse.yy" /* yacc.c:1646  */
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          HfstTransducerPair marks(*(yyvsp[-1].transducer), epsilon);
          HfstTransducerPair tmpMappingPair(*(yyvsp[-3].transducer), HfstTransducer(hfst::xre::format));
          HfstTransducerPair mappingPair = create_mapping_for_mark_up_replace( tmpMappingPair, marks );
                   
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-2].replaceArrow), mappingPair);
          delete (yyvsp[-3].transducer); delete (yyvsp[-1].transducer);
      }
#line 2148 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 29:
#line 490 "xre_parse.yy" /* yacc.c:1646  */
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          HfstTransducerPair marks(epsilon, *(yyvsp[0].transducer));
          HfstTransducerPair tmpMappingPair(*(yyvsp[-3].transducer), HfstTransducer(hfst::xre::format));
          HfstTransducerPair mappingPair = create_mapping_for_mark_up_replace( tmpMappingPair, marks );
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-2].replaceArrow), mappingPair);
          delete (yyvsp[-3].transducer); delete (yyvsp[0].transducer);
      }
#line 2162 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 30:
#line 500 "xre_parse.yy" /* yacc.c:1646  */
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          //HfstTransducer mappingTr(epsilon);
          //mappingTr.cross_product(*$4);
          HfstTransducerPair mappingPair(epsilon, *(yyvsp[0].transducer));
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-1].replaceArrow), mappingPair);
          delete (yyvsp[0].transducer);
      }
#line 2176 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 31:
#line 510 "xre_parse.yy" /* yacc.c:1646  */
    {
	  HfstTransducerPair mappingPair(*(yyvsp[-3].transducer), *(yyvsp[0].transducer));
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-1].replaceArrow), mappingPair);
          delete (yyvsp[-3].transducer); delete (yyvsp[0].transducer);
      }
#line 2186 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 32:
#line 517 "xre_parse.yy" /* yacc.c:1646  */
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          HfstTransducerPair mappingPair(*(yyvsp[-3].transducer), epsilon);
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-2].replaceArrow), mappingPair);
          delete (yyvsp[-3].transducer);
      }
#line 2198 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 33:
#line 525 "xre_parse.yy" /* yacc.c:1646  */
    {
          HfstTransducerPair mappingPair(*(yyvsp[-4].transducer), *(yyvsp[-1].transducer));
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[-3].replaceArrow), mappingPair);
          delete (yyvsp[-4].transducer); delete (yyvsp[-1].transducer);
      }
#line 2208 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 34:
#line 535 "xre_parse.yy" /* yacc.c:1646  */
    {
         (yyval.contextWithMark) =  new std::pair< ReplaceType, HfstTransducerPairVector> ((yyvsp[-1].replType), *(yyvsp[0].transducerPairVector));
         delete (yyvsp[0].transducerPairVector);
         }
#line 2217 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 35:
#line 541 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducerPairVector * ContextVector = new HfstTransducerPairVector();
            ContextVector->push_back(*(yyvsp[0].transducerPair));
            (yyval.transducerPairVector) = ContextVector;
            delete (yyvsp[0].transducerPair);
         }
#line 2228 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 36:
#line 549 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyvsp[-2].transducerPairVector)->push_back(*(yyvsp[0].transducerPair));
            (yyval.transducerPairVector) = (yyvsp[-2].transducerPairVector);
            delete (yyvsp[0].transducerPair);
         }
#line 2238 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 37:
#line 557 "xre_parse.yy" /* yacc.c:1646  */
    {
            if (hfst::xre::has_non_identity_pairs((yyvsp[-2].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }
            if (hfst::xre::has_non_identity_pairs((yyvsp[0].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }
            
            HfstTransducer t1(*(yyvsp[-2].transducer));
            HfstTransducer t2(*(yyvsp[0].transducer));

             if (hfst::xre::is_weighted())
             {
               hfst::xre::has_weight_been_zeroed=false;
               t1.transform_weights(&hfst::xre::zero_weights);
             }
             t1.optimize().prune_alphabet(false);

             if (hfst::xre::is_weighted())
             {
               t2.transform_weights(&hfst::xre::zero_weights);
               hfst::xre::has_weight_been_zeroed=false;
             }
             t2.optimize().prune_alphabet(false);

            (yyval.transducerPair) = new HfstTransducerPair(t1, t2);
            delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
         }
#line 2275 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 38:
#line 590 "xre_parse.yy" /* yacc.c:1646  */
    {
            if (hfst::xre::has_non_identity_pairs((yyvsp[-1].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }

            HfstTransducer t1(*(yyvsp[-1].transducer));
            
            if (hfst::xre::is_weighted())
            {
              hfst::xre::has_weight_been_zeroed=false;
              t1.transform_weights(&hfst::xre::zero_weights);
              hfst::xre::has_weight_been_zeroed=false;
            }
            t1.optimize().prune_alphabet(false);

            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(t1, epsilon);
            delete (yyvsp[-1].transducer);
         }
#line 2301 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 39:
#line 612 "xre_parse.yy" /* yacc.c:1646  */
    {

            if (hfst::xre::has_non_identity_pairs((yyvsp[0].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }
            
            HfstTransducer t1(*(yyvsp[0].transducer));

            if (hfst::xre::is_weighted())
            {
              hfst::xre::has_weight_been_zeroed=false;
              t1.transform_weights(&hfst::xre::zero_weights);
              hfst::xre::has_weight_been_zeroed=false;
            }
            t1.optimize().prune_alphabet(false);
             
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(epsilon, t1);
            delete (yyvsp[0].transducer);
         }
#line 2328 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 40:
#line 635 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(epsilon, epsilon);
          }
#line 2337 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 41:
#line 641 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replType) = REPL_UP;
         }
#line 2345 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 42:
#line 645 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replType) = REPL_RIGHT;
         }
#line 2353 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 43:
#line 649 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replType) = REPL_LEFT;
         }
#line 2361 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 44:
#line 653 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replType) = REPL_DOWN;
         }
#line 2369 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 45:
#line 659 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replaceArrow) = E_REPLACE_RIGHT;
         }
#line 2377 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 46:
#line 663 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replaceArrow) = E_OPTIONAL_REPLACE_RIGHT;
         }
#line 2385 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 47:
#line 667 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replaceArrow) = E_RTL_LONGEST_MATCH;
         }
#line 2393 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 48:
#line 671 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replaceArrow) = E_RTL_SHORTEST_MATCH;
         }
#line 2401 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 49:
#line 675 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replaceArrow) = E_LTR_LONGEST_MATCH;
         }
#line 2409 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 50:
#line 679 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.replaceArrow) = E_LTR_SHORTEST_MATCH;
         }
#line 2417 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 51:
#line 683 "xre_parse.yy" /* yacc.c:1646  */
    {
        	 (yyval.replaceArrow) =  E_REPLACE_LEFT;
         }
#line 2425 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 52:
#line 687 "xre_parse.yy" /* yacc.c:1646  */
    {
        	 (yyval.replaceArrow) = E_OPTIONAL_REPLACE_LEFT;
         }
#line 2433 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 53:
#line 693 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2439 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 54:
#line 694 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No shuffle");
            //$$ = $1;
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2450 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 55:
#line 700 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = new HfstTransducer( before (*(yyvsp[-2].transducer), *(yyvsp[0].transducer)) );
            delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
        }
#line 2459 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 56:
#line 704 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = new HfstTransducer( after (*(yyvsp[-2].transducer), *(yyvsp[0].transducer)) );
            delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
        }
#line 2468 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 57:
#line 711 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2474 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 58:
#line 713 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = new HfstTransducer( restriction(*(yyvsp[-2].transducer), *(yyvsp[0].transducerPairVector)) ) ;
            delete (yyvsp[-2].transducer);
            delete (yyvsp[0].transducerPairVector);
        }
#line 2484 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 59:
#line 719 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No Arrows");
            //$$ = $1;
            delete (yyvsp[-2].transducer);
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2496 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 60:
#line 727 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No Arrows");
            //$$ = $1;
            delete (yyvsp[-2].transducer);
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2508 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 61:
#line 737 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducerPairVector * ContextVector = new HfstTransducerPairVector();
            ContextVector->push_back(*(yyvsp[0].transducerPair));
            (yyval.transducerPairVector) = ContextVector;
            delete (yyvsp[0].transducerPair);
         }
#line 2519 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 62:
#line 745 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyvsp[-2].transducerPairVector)->push_back(*(yyvsp[0].transducerPair));
            (yyval.transducerPairVector) = (yyvsp[-2].transducerPairVector);
            delete (yyvsp[0].transducerPair);
         }
#line 2529 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 63:
#line 754 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducerPair) = new HfstTransducerPair(*(yyvsp[-2].transducer), *(yyvsp[0].transducer));
            delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
         }
#line 2538 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 64:
#line 759 "xre_parse.yy" /* yacc.c:1646  */
    {
           // std::cerr << "Mapping: \n" << *$1  << std::endl;
            
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            
           // std::cerr << "Epsilon: \n" << epsilon  << std::endl;
            (yyval.transducerPair) = new HfstTransducerPair(*(yyvsp[-1].transducer), epsilon);
            delete (yyvsp[-1].transducer);
         }
#line 2552 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 65:
#line 769 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(epsilon, *(yyvsp[0].transducer));
            delete (yyvsp[0].transducer);
         }
#line 2562 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 66:
#line 775 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer empty(hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(empty, empty);
         }
#line 2571 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 67:
#line 782 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2577 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 68:
#line 783 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-2].transducer)->disjunct(*(yyvsp[0].transducer), harmonize_);
            delete (yyvsp[0].transducer);
        }
#line 2586 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 69:
#line 787 "xre_parse.yy" /* yacc.c:1646  */
    {
        // std::cerr << "Intersection: \n"  << std::endl;
            (yyval.transducer) = & (yyvsp[-2].transducer)->intersect(*(yyvsp[0].transducer), harmonize_).optimize().prune_alphabet(false);
            delete (yyvsp[0].transducer);
        }
#line 2596 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 70:
#line 792 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-2].transducer)->subtract(*(yyvsp[0].transducer), harmonize_).prune_alphabet(false);
            delete (yyvsp[0].transducer);
        }
#line 2605 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 71:
#line 796 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No upper minus");
            //$$ = $1;
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2616 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 72:
#line 802 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No lower minus");
            //$$ = $1;
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2627 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 73:
#line 808 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-2].transducer)->priority_union(*(yyvsp[0].transducer));
            delete (yyvsp[0].transducer);
        }
#line 2636 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 74:
#line 812 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer* left = new HfstTransducer(*(yyvsp[-2].transducer));
            HfstTransducer* right =  new HfstTransducer(*(yyvsp[0].transducer));
            right->invert();
            left->invert();
            (yyval.transducer) = & (left->priority_union(*right).invert());
            delete (yyvsp[-2].transducer); delete (yyvsp[0].transducer);
        }
#line 2649 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 75:
#line 822 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2655 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 76:
#line 823 "xre_parse.yy" /* yacc.c:1646  */
    {
        (yyval.transducer) = & (yyvsp[-1].transducer)->concatenate(*(yyvsp[0].transducer), harmonize_);
        delete (yyvsp[0].transducer);
        }
#line 2664 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 77:
#line 829 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2670 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 78:
#line 830 "xre_parse.yy" /* yacc.c:1646  */
    {
            // this is how ignoring is done in foma and xfst
            (yyvsp[-2].transducer)->harmonize(*(yyvsp[0].transducer), true /*force harmonization also for foma type*/);
            (yyval.transducer) = & (yyvsp[-2].transducer)->insert_freely(*(yyvsp[0].transducer), false); // no harmonization
            delete (yyvsp[0].transducer);
        }
#line 2681 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 79:
#line 836 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No ignoring internally");
            //$$ = $1;
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2692 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 80:
#line 842 "xre_parse.yy" /* yacc.c:1646  */
    {
            xreerror("No left quotient");
            //$$ = $1;
            delete (yyvsp[0].transducer);
            YYABORT;
        }
#line 2703 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 81:
#line 850 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2709 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 82:
#line 851 "xre_parse.yy" /* yacc.c:1646  */
    {
       		// forbid pair complement (ie ~a:b)
		if (! (yyvsp[0].transducer)->is_automaton())
		{
		  xreerror("Complement operator ~ is defined only for automata\n"
		           "Use expression [[?:?] - A]] instead where A is the relation to be complemented.");
		  YYABORT;
		}
       		HfstTransducer complement = HfstTransducer::identity_pair( hfst::xre::format );
       		complement.repeat_star().optimize();
       		complement.subtract(*(yyvsp[0].transducer)).prune_alphabet(false);
       		(yyval.transducer) = new HfstTransducer(complement);
   			delete (yyvsp[0].transducer);
        }
#line 2728 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 83:
#line 865 "xre_parse.yy" /* yacc.c:1646  */
    {
            // std::cerr << "Containment: \n" << std::endl;
            if (hfst::xre::has_non_identity_pairs((yyvsp[0].transducer))) // if non-identity symbols present..
            {
              hfst::xre::warn("warning: using transducer that is non an automaton in containment\n");
              (yyval.transducer) = hfst::xre::contains((yyvsp[0].transducer)); // ..resort to simple containment
            }
            else
            {
              (yyval.transducer) = hfst::xre::contains_with_weight((yyvsp[0].transducer), 0);
            }
            delete (yyvsp[0].transducer);
        }
#line 2746 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 84:
#line 878 "xre_parse.yy" /* yacc.c:1646  */
    {
            // std::cerr << "Containment: \n" << std::endl;
            if (hfst::xre::has_non_identity_pairs((yyvsp[0].transducer))) // if non-identity symbols present..
            {
              xreerror("Containment with weight only works with automata");
              YYABORT;
            }
            (yyval.transducer) = hfst::xre::contains_with_weight((yyvsp[0].transducer), hfst::double_to_float((yyvsp[-1].weight)));
            delete (yyvsp[0].transducer);
        }
#line 2761 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 85:
#line 888 "xre_parse.yy" /* yacc.c:1646  */
    {
            //std::cerr << "Contain 1 \n"<< std::endl;

            (yyval.transducer) = hfst::xre::contains_once((yyvsp[0].transducer));
            delete (yyvsp[0].transducer);
        }
#line 2772 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 86:
#line 894 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = hfst::xre::contains_once_optional((yyvsp[0].transducer));
            delete (yyvsp[0].transducer);
        }
#line 2781 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 87:
#line 900 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2787 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 88:
#line 901 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->repeat_star();
        }
#line 2795 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 89:
#line 904 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->repeat_plus();
        }
#line 2803 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 90:
#line 907 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->reverse();
        }
#line 2811 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 91:
#line 910 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->invert();
        }
#line 2819 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 92:
#line 913 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->input_project();
        }
#line 2827 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 93:
#line 916 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->output_project();
        }
#line 2835 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 94:
#line 919 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->repeat_n((yyvsp[0].value));
        }
#line 2843 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 95:
#line 922 "xre_parse.yy" /* yacc.c:1646  */
    {
            //std::cerr << "value is ::::: \n"<< $2 << std::endl;
            (yyval.transducer) = & (yyvsp[-1].transducer)->repeat_n_plus((yyvsp[0].value)+1);
        }
#line 2852 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 96:
#line 926 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->repeat_n_minus((yyvsp[0].value)-1);
        }
#line 2860 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 97:
#line 929 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->repeat_n_to_k((yyvsp[0].values)[0], (yyvsp[0].values)[1]);
            free((yyvsp[0].values));
        }
#line 2869 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 98:
#line 935 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2875 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 99:
#line 936 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer* any = new HfstTransducer(hfst::internal_identity,
                                        hfst::xre::format);
            (yyval.transducer) = & ( any->subtract(*(yyvsp[0].transducer)));
            delete (yyvsp[0].transducer);
        }
#line 2886 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 100:
#line 951 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 2892 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 101:
#line 952 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->optimize();
        }
#line 2900 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 102:
#line 956 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-5].transducer)->cross_product(*(yyvsp[-1].transducer));
            delete (yyvsp[-1].transducer);
        }
#line 2909 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 103:
#line 961 "xre_parse.yy" /* yacc.c:1646  */
    {
     	    HfstTransducer * tmp = hfst::xre::xfst_curly_label_to_transducer((yyvsp[0].label),(yyvsp[0].label));
            free((yyvsp[0].label));
            (yyval.transducer) = & (yyvsp[-3].transducer)->cross_product(*tmp);
            delete tmp;
        }
#line 2920 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 104:
#line 968 "xre_parse.yy" /* yacc.c:1646  */
    {
     	    HfstTransducer * tmp = hfst::xre::xfst_curly_label_to_transducer((yyvsp[-4].label),(yyvsp[-4].label));
            free((yyvsp[-4].label));
            (yyval.transducer) = & (yyvsp[-1].transducer)->cross_product(*tmp);
            delete tmp;
        }
#line 2931 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 105:
#line 975 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer * tmp = hfst::xre::expand_definition((yyvsp[0].label));
            free((yyvsp[0].label));
            (yyval.transducer) = & (yyvsp[-3].transducer)->cross_product(*tmp);
            delete tmp;
        }
#line 2942 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 106:
#line 982 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = hfst::xre::expand_definition((yyvsp[-4].label));
            free((yyvsp[-4].label));
            (yyval.transducer) = & (yyval.transducer)->cross_product(*(yyvsp[-1].transducer));
            delete (yyvsp[-1].transducer);
        }
#line 2953 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 107:
#line 988 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-2].transducer)->set_final_weights(hfst::double_to_float((yyvsp[0].weight)), true).optimize();
        }
#line 2961 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 108:
#line 991 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->optionalize();
        }
#line 2969 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 109:
#line 997 "xre_parse.yy" /* yacc.c:1646  */
    {
            if (strcmp((yyvsp[0].label), hfst::internal_unknown.c_str()) == 0)
              {
                (yyval.transducer) = new HfstTransducer(hfst::internal_identity, hfst::xre::format);
              }
            else
              {
                (yyval.transducer) = new HfstTransducer((yyvsp[0].label), (yyvsp[0].label), hfst::xre::format);
              }
            free((yyvsp[0].label));
        }
#line 2985 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 110:
#line 1008 "xre_parse.yy" /* yacc.c:1646  */
    {
            HfstTransducer * tmp ;
            if (strcmp((yyvsp[0].label), hfst::internal_unknown.c_str()) == 0)
              {
                 tmp = new HfstTransducer(hfst::internal_identity, hfst::xre::format);
              }
            else
              {
                 tmp = new HfstTransducer((yyvsp[0].label), (yyvsp[0].label), hfst::xre::format);
              }

            (yyvsp[-1].transducer)->disjunct(*tmp, false); // do not harmonize
            (yyval.transducer) = & (yyvsp[-1].transducer)->optimize();
            free((yyvsp[0].label));
            delete tmp;
            }
#line 3006 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 111:
#line 1026 "xre_parse.yy" /* yacc.c:1646  */
    { (yyval.transducer) = (yyvsp[0].transducer); }
#line 3012 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 112:
#line 1027 "xre_parse.yy" /* yacc.c:1646  */
    {
            (yyval.transducer) = & (yyvsp[-1].transducer)->set_final_weights(hfst::double_to_float((yyvsp[0].weight)), true);
        }
#line 3020 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 113:
#line 1030 "xre_parse.yy" /* yacc.c:1646  */
    {
            try {
              hfst::HfstInputStream instream((yyvsp[0].label));
              (yyval.transducer) = new HfstTransducer(instream);
              instream.close();
              free((yyvsp[0].label));
            }
            catch (const HfstException & e) {
              (void) e; // todo handle the exception
              char msg [256];
              sprintf(msg, "Error reading transducer file '%s'.", (yyvsp[0].label));
              xreerror(msg);
              free((yyvsp[0].label));
              YYABORT;
            }
        }
#line 3041 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 114:
#line 1046 "xre_parse.yy" /* yacc.c:1646  */
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[0].label), "r");
            free((yyvsp[0].label));
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              YYABORT;
            }
            else {
              HfstBasicTransducer tmp;
              HfstTokenizer tok;
              char line [1000];

              while( fgets(line, 1000, f) != NULL )
              {
                hfst::xre::strip_newline(line);
                StringPairVector spv = tok.tokenize(line);
                tmp.disjunct(spv, 0);
              }
              fclose(f);
              HfstTransducer * retval = new HfstTransducer(tmp, hfst::xre::format);
              retval->optimize();
              (yyval.transducer) = retval;
            }
        }
#line 3071 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 115:
#line 1071 "xre_parse.yy" /* yacc.c:1646  */
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[0].label), "r");
            free((yyvsp[0].label));
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              YYABORT;
            }
            else {
              HfstTokenizer tok;
              HfstBasicTransducer tmp;
              char line [1000];

              while( fgets(line, 1000, f) != NULL )
              {
                hfst::xre::strip_newline(line);
                StringPairVector spv = HfstTokenizer::tokenize_space_separated(line);
                tmp.disjunct(spv, 0);
              }
              fclose(f);
              HfstTransducer * retval = new HfstTransducer(tmp, hfst::xre::format);
              retval->optimize();
              (yyval.transducer) = retval;
            }
        }
#line 3101 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 116:
#line 1096 "xre_parse.yy" /* yacc.c:1646  */
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[0].label), "r");
            free((yyvsp[0].label));
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              YYABORT;
            }
            else {
              try {
                unsigned int linecount = 0;
                HfstBasicTransducer tmp = HfstBasicTransducer::read_in_prolog_format(f, linecount);
                fclose(f);
                HfstTransducer * retval = new HfstTransducer(tmp, hfst::xre::format);
                retval->optimize();
                (yyval.transducer) = retval;
              }
              catch (const HfstException & e) {
                (void) e; // todo handle the exception
                fclose(f);
                xreerror("Error reading prolog file.\n");
                YYABORT;
              }
            }
        }
#line 3131 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 117:
#line 1121 "xre_parse.yy" /* yacc.c:1646  */
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[0].label), "r");
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              fclose(f);
              free((yyvsp[0].label));
              YYABORT;
            }
            else {
              fclose(f);
              // read the regex in a string
              std::ifstream ifs((yyvsp[0].label));
              free((yyvsp[0].label));
              std::stringstream buffer;
              buffer << ifs.rdbuf();
              char * regex_string = strdup(buffer.str().c_str());

              // create a new scanner for evaluating the regex
              yyscan_t scanner;
              xrelex_init(&scanner);
              YY_BUFFER_STATE bs = xre_scan_string(regex_string, scanner);

              unsigned int chars_read = hfst::xre::cr;
              hfst::xre::cr = 0;

              int parse_retval = xreparse(scanner);

              xre_delete_buffer(bs,scanner);
              xrelex_destroy(scanner);

              free(regex_string);

              hfst::xre::cr = chars_read;

              (yyval.transducer) = hfst::xre::last_compiled;

              if (parse_retval != 0)
              {
                xreerror("Error parsing regex.\n");
                YYABORT;
              }
            }
        }
#line 3180 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 118:
#line 1167 "xre_parse.yy" /* yacc.c:1646  */
    {
        if (strcmp((yyvsp[0].label), hfst::internal_unknown.c_str()) == 0)
          {
            (yyval.transducer) = new HfstTransducer(hfst::internal_identity, hfst::xre::format);
          }
        else
          {
            // HfstTransducer * tmp = new HfstTransducer($1, hfst::xre::format);
	    // $$ = hfst::xre::expand_definition(tmp, $1);
            (yyval.transducer) = hfst::xre::expand_definition((yyvsp[0].label));
          }
        free((yyvsp[0].label));
     }
#line 3198 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 119:
#line 1181 "xre_parse.yy" /* yacc.c:1646  */
    {
     	(yyval.transducer) = hfst::xre::xfst_label_to_transducer((yyvsp[-2].label),(yyvsp[0].label));
        free((yyvsp[-2].label));
        free((yyvsp[0].label));
     }
#line 3208 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 120:
#line 1186 "xre_parse.yy" /* yacc.c:1646  */
    {
        (yyval.transducer) = hfst::xre::xfst_label_to_transducer((yyvsp[-2].label),(yyvsp[-2].label));
        free((yyvsp[-2].label));
        HfstTransducer * tmp = hfst::xre::xfst_curly_label_to_transducer((yyvsp[0].label),(yyvsp[0].label));
        free((yyvsp[0].label));
        (yyval.transducer) = & (yyval.transducer)->cross_product(*tmp);
        delete tmp;
     }
#line 3221 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 121:
#line 1194 "xre_parse.yy" /* yacc.c:1646  */
    {
        HfstTransducer * tmp = hfst::xre::xfst_label_to_transducer((yyvsp[0].label),(yyvsp[0].label));
        free((yyvsp[0].label));
        (yyval.transducer) = hfst::xre::xfst_curly_label_to_transducer((yyvsp[-2].label),(yyvsp[-2].label));
        free((yyvsp[-2].label));
        (yyval.transducer) = & (yyval.transducer)->cross_product(*tmp);
        delete tmp;
     }
#line 3234 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 122:
#line 1202 "xre_parse.yy" /* yacc.c:1646  */
    {
     	(yyval.transducer) = hfst::xre::xfst_curly_label_to_transducer((yyvsp[0].label),(yyvsp[0].label));
        free((yyvsp[0].label));
     }
#line 3243 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 123:
#line 1206 "xre_parse.yy" /* yacc.c:1646  */
    {
     	(yyval.transducer) = hfst::xre::xfst_curly_label_to_transducer((yyvsp[-2].label),(yyvsp[0].label));
        free((yyvsp[-2].label));
	free((yyvsp[0].label));
     }
#line 3253 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 124:
#line 1212 "xre_parse.yy" /* yacc.c:1646  */
    {
            if (! hfst::xre::is_valid_function_call((yyvsp[-2].label), (yyvsp[-1].transducerVector))) {
              delete (yyvsp[-2].label); delete (yyvsp[-1].transducerVector);
              return EXIT_FAILURE;
            }
            else {
              // create a new scanner for evaluating the function
              yyscan_t scanner;
              xrelex_init(&scanner);
              YY_BUFFER_STATE bs = xre_scan_string(hfst::xre::get_function_xre((yyvsp[-2].label)),scanner);

              // define special variables so that function arguments get the values given in regexp list
              if (! hfst::xre::define_function_args((yyvsp[-2].label), (yyvsp[-1].transducerVector)))
              {
                xreerror("Could not define function args.\n");  // TODO: more informative message
                delete (yyvsp[-2].label); delete (yyvsp[-1].transducerVector);
                YYABORT;
              }

              delete (yyvsp[-1].transducerVector);
              // if we are scanning a function definition for argument symbols,
              // do not include the characters read when evaluating functions inside it
              unsigned int chars_read = hfst::xre::cr;

              int parse_retval = xreparse(scanner);

              hfst::xre::cr = chars_read;
              hfst::xre::undefine_function_args((yyvsp[-2].label));
              delete (yyvsp[-2].label);

              xre_delete_buffer(bs,scanner);
              xrelex_destroy(scanner);

              (yyval.transducer) = hfst::xre::last_compiled;

              if (parse_retval != 0)
              {
                YYABORT;
              }
            }
        }
#line 3299 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 126:
#line 1263 "xre_parse.yy" /* yacc.c:1646  */
    {
       hfst::xre::check_multichar_symbol((yyvsp[0].label));
       (yyval.label) = (yyvsp[0].label);
     }
#line 3308 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 127:
#line 1267 "xre_parse.yy" /* yacc.c:1646  */
    {
       hfst::xre::check_multichar_symbol((yyvsp[0].label));
       (yyval.label) = (yyvsp[0].label);
     }
#line 3317 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 129:
#line 1275 "xre_parse.yy" /* yacc.c:1646  */
    {
       // Symbols of form <foo> are not harmonized in xfst, that is why
       // they need to be escaped as @_<foo>_@.
       // $$ = hfst::xre::escape_enclosing_angle_brackets($1);
       hfst::xre::warn_about_hfst_special_symbol((yyvsp[0].label));
       hfst::xre::warn_about_xfst_special_symbol((yyvsp[0].label));
       (yyval.label) = (yyvsp[0].label);
     }
#line 3330 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 130:
#line 1283 "xre_parse.yy" /* yacc.c:1646  */
    {
        (yyval.label) = strdup(hfst::internal_epsilon.c_str());
     }
#line 3338 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 131:
#line 1286 "xre_parse.yy" /* yacc.c:1646  */
    {
        (yyval.label) = strdup(hfst::internal_unknown.c_str());
     }
#line 3346 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 132:
#line 1289 "xre_parse.yy" /* yacc.c:1646  */
    {
        (yyval.label) = strdup("@#@");
     }
#line 3354 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 133:
#line 1294 "xre_parse.yy" /* yacc.c:1646  */
    {
       (yyval.transducerVector)->push_back(*((yyvsp[0].transducer)));
       delete (yyvsp[0].transducer);
     }
#line 3363 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 134:
#line 1298 "xre_parse.yy" /* yacc.c:1646  */
    {
       (yyval.transducerVector) = new hfst::HfstTransducerVector();
       (yyval.transducerVector)->push_back(*((yyvsp[0].transducer)));
       delete (yyvsp[0].transducer);
     }
#line 3373 "xre_parse.cc" /* yacc.c:1646  */
    break;

  case 135:
#line 1305 "xre_parse.yy" /* yacc.c:1646  */
    {
        (yyval.label) = strdup((yyvsp[0].label));
    }
#line 3381 "xre_parse.cc" /* yacc.c:1646  */
    break;


#line 3385 "xre_parse.cc" /* yacc.c:1646  */
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
      yyerror (scanner, YY_("syntax error"));
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
        yyerror (scanner, yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



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
                      yytoken, &yylval, scanner);
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


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp, scanner);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


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
  yyerror (scanner, YY_("memory exhausted"));
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
                  yytoken, &yylval, scanner);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp, scanner);
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
#line 1309 "xre_parse.yy" /* yacc.c:1906  */


