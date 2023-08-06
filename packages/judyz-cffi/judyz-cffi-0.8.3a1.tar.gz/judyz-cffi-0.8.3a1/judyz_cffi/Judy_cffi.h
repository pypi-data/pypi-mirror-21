// This is the core of Judy.h, without things unsupported by CFFI
// and with some strong typing.

// _________________
//
// Copyright (C) 2000 - 2002 Hewlett-Packard Company
//
// This program is free software; you can redistribute it and/or modify it
// under the term of the GNU Lesser General Public License as published by the
// Free Software Foundation; either version 2 of the License, or (at your
// option) any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
// FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
// for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program; if not, write to the Free Software Foundation,
// Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
// _________________

// @(#) $Revision: 4.52 $ $Source: /judy/src/Judy.h $
//
// HEADER FILE FOR EXPORTED FEATURES IN JUDY LIBRARY, libJudy.*
//
// See the manual entries for details.
//
// Note:  This header file uses old-style comments on #-directive lines and
// avoids "()" on macro names in comments for compatibility with older cc -Aa
// and some tools on some platforms.


// ****************************************************************************
// DECLARE SOME BASE TYPES IN CASE THEY ARE MISSING:
//
// These base types include "const" where appropriate, but only where of
// interest to the caller.  For example, a caller cares that a variable passed
// by reference will not be modified, such as, "const void * Pindex", but not
// that the called function internally does not modify the pointer itself, such
// as, "void * const Pindex".
//
// Note that its OK to pass a Pvoid_t to a Pcvoid_t; the latter is the same,
// only constant.  Callers need to do this so they can also pass & Pvoid_t to
// PPvoid_t (non-constant).

// ****************************************************************************
// YB: Mostly removed void*, use typed pointers.

typedef struct _Judy1 Judy1;
typedef struct _JudyL JudyL;
typedef struct _JudySL JudySL;
typedef struct _JudyHS JudyHS;

typedef const Judy1  *   PcJudy1_t;
typedef Judy1  *   PJudy1_t;
typedef Judy1  ** PPJudy1_t;

typedef const JudyL  *   PcJudyL_t;
typedef JudyL  *   PJudyL_t;
typedef JudyL  ** PPJudyL_t;

typedef const JudySL  *   PcJudySL_t;
typedef JudySL  *   PJudySL_t;
typedef JudySL  ** PPJudySL_t;

typedef const void * Pcvoid_t;
typedef void *   Pvoid_t;
typedef void ** PPvoid_t;
typedef signed long    Word_t, * PWord_t;  // expect 32-bit or 64-bit words.

// ****************************************************************************
// SUPPORT FOR ERROR HANDLING:
//
// Judy error numbers:
//
// Note:  These are an enum so there's a related typedef, but the numbers are
// spelled out so you can map a number back to its name.

typedef enum            // uint8_t -- but C does not support this type of enum.
{

// Note:  JU_ERRNO_NONE and JU_ERRNO_FULL are not real errors.  They specify
// conditions which are otherwise impossible return values from 32-bit
// Judy1Count, which has 2^32 + 1 valid returns (0..2^32) plus one error
// return.  These pseudo-errors support the return values that cannot otherwise
// be unambiguously represented in a 32-bit word, and will never occur on a
// 64-bit system.

        JU_ERRNO_NONE           = 0,
        JU_ERRNO_FULL           = 1,
        JU_ERRNO_NFMAX          = 1,

// JU_ERRNO_NOMEM comes from malloc(3C) when Judy cannot obtain needed memory.
// The system errno value is also set to ENOMEM.  This error can be recoverable
// if the calling application frees other memory.
//
// TBD:  Currently there is no guarantee the Judy array has no memory leaks
// upon JU_ERRNO_NOMEM.

        JU_ERRNO_NOMEM          = 2,

// Problems with parameters from the calling program:
//
// JU_ERRNO_NULLPPARRAY means PPArray was null; perhaps PArray was passed where
// &PArray was intended.  Similarly, JU_ERRNO_NULLPINDEX means PIndex was null;
// perhaps &Index was intended.  Also, JU_ERRNO_NONNULLPARRAY,
// JU_ERRNO_NULLPVALUE, and JU_ERRNO_UNSORTED, all added later (hence with
// higher numbers), mean:  A non-null array was passed in where a null pointer
// was required; PValue was null; and unsorted indexes were detected.

        JU_ERRNO_NULLPPARRAY    = 3,    // see above.
        JU_ERRNO_NONNULLPARRAY  = 10,   // see above.
        JU_ERRNO_NULLPINDEX     = 4,    // see above.
        JU_ERRNO_NULLPVALUE     = 11,   // see above.
        JU_ERRNO_NOTJUDY1       = 5,    // PArray is not to a Judy1 array.
        JU_ERRNO_NOTJUDYL       = 6,    // PArray is not to a JudyL array.
        JU_ERRNO_NOTJUDYSL      = 7,    // PArray is not to a JudySL array.
        JU_ERRNO_UNSORTED       = 12,   // see above.

// Errors below this point are not recoverable; further tries to access the
// Judy array might result in EFAULT and a core dump:
//
// JU_ERRNO_OVERRUN occurs when Judy detects, upon reallocation, that a block
// of memory in its own freelist was modified since being freed.

        JU_ERRNO_OVERRUN        = 8,

// JU_ERRNO_CORRUPT occurs when Judy detects an impossible value in a Judy data
// structure:
//
// Note:  The Judy data structure contains some redundant elements that support
// this type of checking.

        JU_ERRNO_CORRUPT        = 9

// Warning:  At least some C or C++ compilers do not tolerate a trailing comma
// above here.  At least we know of one case, in aCC; see JAGad58928.

} JU_Errno_t;


// Judy errno structure:
//
// WARNING:  For compatibility with possible future changes, the fields of this
// struct should not be referenced directly.  Instead use the macros supplied
// below.

// YB: removed the macros, unusable in languages other than C/C++

// This structure should be declared on the stack in a threaded process.

typedef struct J_UDY_ERROR_STRUCT
{
        JU_Errno_t je_Errno;            // one of the enums above.
        int        je_ErrID;            // often an internal source line number.
        Word_t     je_reserved[4];      // for future backward compatibility.

} JError_t, * PJError_t;


// ****************************************************************************
// JUDY FUNCTIONS:
//

// ****************************************************************************
// JUDY1 FUNCTIONS:

extern int      Judy1Test(       PcJudy1_t  PArray, Word_t   Index,   PJError_t PJError);
extern int      Judy1Set(        PPJudy1_t PPArray, Word_t   Index,   PJError_t PJError);
extern int      Judy1SetArray(   PPJudy1_t PPArray, Word_t   Count,
                                             const Word_t * const PIndex,
                                                                     PJError_t PJError);
extern int      Judy1Unset(      PPJudy1_t PPArray, Word_t   Index,   PJError_t PJError);
extern Word_t   Judy1Count(      PcJudy1_t  PArray, Word_t   Index1,
                                                   Word_t   Index2,  PJError_t PJError);
extern int      Judy1ByCount(    PcJudy1_t  PArray, Word_t   Count,
                                                   Word_t * PIndex,  PJError_t PJError);
extern Word_t   Judy1FreeArray(  PPJudy1_t PPArray,                   PJError_t PJError);
extern Word_t   Judy1MemUsed(    PcJudy1_t  PArray);
extern Word_t   Judy1MemActive(  PcJudy1_t  PArray);
extern int      Judy1First(      PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1Next(       PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1Last(       PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1Prev(       PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1FirstEmpty( PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1NextEmpty(  PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1LastEmpty(  PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      Judy1PrevEmpty(  PcJudy1_t  PArray, Word_t * PIndex,  PJError_t PJError);

// ****************************************************************************
// JUDYL FUNCTIONS:

extern PPvoid_t JudyLGet(        PcJudyL_t  PArray, Word_t    Index,  PJError_t PJError);
extern PPvoid_t JudyLIns(        PPJudyL_t PPArray, Word_t    Index,  PJError_t PJError);
extern int      JudyLInsArray(   PPJudyL_t PPArray, Word_t    Count,
                                             const Word_t * const PIndex,
                                             const Word_t * const PValue,
                                                                     PJError_t PJError);
extern int      JudyLDel(        PPJudyL_t PPArray, Word_t    Index,  PJError_t PJError);
extern Word_t   JudyLCount(      PcJudyL_t  PArray, Word_t    Index1,
                                                    Word_t    Index2, PJError_t PJError);
extern PPvoid_t JudyLByCount(    PcJudyL_t  PArray, Word_t    Count,
                                                    Word_t *  PIndex, PJError_t PJError);
extern Word_t   JudyLFreeArray(  PPJudyL_t PPArray,                   PJError_t PJError);
extern Word_t   JudyLMemUsed(    PcJudyL_t  PArray);
extern Word_t   JudyLMemActive(  PcJudyL_t  PArray);
extern PPvoid_t JudyLFirst(      PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern PPvoid_t JudyLNext(       PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern PPvoid_t JudyLLast(       PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern PPvoid_t JudyLPrev(       PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      JudyLFirstEmpty( PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      JudyLNextEmpty(  PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      JudyLLastEmpty(  PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);
extern int      JudyLPrevEmpty(  PcJudyL_t  PArray, Word_t * PIndex,  PJError_t PJError);

// ****************************************************************************
// JUDYSL FUNCTIONS:

extern PPvoid_t JudySLGet(       PcJudySL_t, const unsigned char* Index, PJError_t PJError);
extern PPvoid_t JudySLIns(       PPJudySL_t, const unsigned char* Index, PJError_t PJError);
extern int      JudySLDel(       PPJudySL_t, const unsigned char* Index, PJError_t PJError);
extern Word_t   JudySLFreeArray( PPJudySL_t,                     PJError_t PJError);
extern PPvoid_t JudySLFirst(     PcJudySL_t,       unsigned char* Index, PJError_t PJError);
extern PPvoid_t JudySLNext(      PcJudySL_t,       unsigned char* Index, PJError_t PJError);
extern PPvoid_t JudySLLast(      PcJudySL_t,       unsigned char* Index, PJError_t PJError);
extern PPvoid_t JudySLPrev(      PcJudySL_t,       unsigned char* Index, PJError_t PJError);

// ****************************************************************************
// JUDYHSL FUNCTIONS:

extern PPvoid_t JudyHSGet(       Pcvoid_t,  void *, Word_t);
extern PPvoid_t JudyHSIns(       PPvoid_t,  void *, Word_t, PJError_t PJError);
extern int      JudyHSDel(       PPvoid_t,  void *, Word_t, PJError_t PJError);
extern Word_t   JudyHSFreeArray( PPvoid_t,                  PJError_t PJError);

extern const char *Judy1MallocSizes;
extern const char *JudyLMallocSizes;

// ****************************************************************************
// JUDY memory interface to malloc() FUNCTIONS:

extern Word_t JudyMalloc(Word_t);               // words reqd => words allocd.
extern Word_t JudyMallocVirtual(Word_t);        // words reqd => words allocd.
extern void   JudyFree(Pvoid_t, Word_t);        // free, size in words.
extern void   JudyFreeVirtual(Pvoid_t, Word_t); // free, size in words.

