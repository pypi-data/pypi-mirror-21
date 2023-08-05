/* Copyright (C) 2000  The PARI group.

This file is part of the PARI/GP package.

PARI/GP is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation. It is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY WHATSOEVER.

Check the License for details. You should have received a copy of it, along
with the package; see the file 'COPYING'. If not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. */

/* output of get_nf and get_bnf */
enum {
  typ_NULL = 0,
  typ_POL,
  typ_Q,
  typ_NF,
  typ_BNF,
  typ_BNR,
  typ_ELL, /* elliptic curve */
  typ_QUA, /* quadclassunit  */
  typ_GAL, /* galoisinit     */
  typ_BID,
  typ_PRID,
  typ_MODPR,
  typ_RNF
};

/* types of algebras */
enum  {
  al_NULL = 0,
  al_TABLE,
  al_CSA,
  al_CYCLIC
};

/* models for elements of algebras */
enum {
  al_INVALID = 0,
  al_TRIVIAL,
  al_ALGEBRAIC,
  al_BASIS,
  al_MATRIX
};

/* idealtyp */
enum {
  id_PRINCIPAL = 0,
  id_PRIME,
  id_MAT
};

typedef struct {
  GEN T, dT; /* defining polynomial (monic ZX), disc(T) */
  GEN T0; /* original defining polynomial (ZX) */
  GEN unscale; /* T = C*T0(x / unscale), rational */
  GEN dK; /* disc(K) */
  GEN index; /* [O_K : Z[X]/(T)] */
  GEN basis;  /* Z-basis of O_K (t_VEC of t_POL) */

  long r1; /* number of real places of K */
  GEN basden; /* [nums(bas), dens(bas)] */
  GEN dTP, dTE; /* (possibly partial) factorization of dT, primes / exponents */
  GEN dKP, dKE; /* (possibly partial) factorization of dK, primes / exponents */
} nfmaxord_t;

/* qfr3 / qfr5 */
struct qfr_data { GEN D, sqrtD, isqrtD; };

/* various flags for nf/bnf routines */
enum {
  nf_ORIG = 1,
  nf_GEN = 1,
  nf_ABSOLUTE = 2,
  nf_FORCE = 2,
  nf_ALL = 4,
  nf_GENMAT = 4,
  nf_INIT = 4,
  nf_RAW = 8,
  nf_RED = 8,
  nf_PARTIALFACT = 16,
  nf_ROUND2 = 64, /* obsolete */
  nf_ADDZK =  256,
  nf_GEN_IF_PRINCIPAL = 512
};

enum {
  rnf_REL = 1,
  rnf_COND = 2
};

/* LLL */
enum {
  LLL_KER  = 1, /* only kernel */
  LLL_IM   = 2, /* only image */
  LLL_ALL  = 4, /* kernel & image */
  LLL_GRAM       = 0x100,
  LLL_KEEP_FIRST = 0x200,
  LLL_INPLACE    = 0x400,
  LLL_COMPATIBLE = 0x800 /* attempt same behaviour on 32/64bit kernels */
};

/* HNF */
enum { hnf_MODID = 1, hnf_PART = 2, hnf_CENTER = 4 };

/* for fincke_pohst() */
typedef struct FP_chk_fun {
  GEN (*f)(void *,GEN);
  /* f_init allowed to permute the columns of u and r */
  GEN (*f_init)(struct FP_chk_fun*,GEN,GEN);
  GEN (*f_post)(struct FP_chk_fun*,GEN,GEN);
  void *data;
  long skipfirst;
} FP_chk_fun;

/* for ideallog / zlog */
typedef struct {
  GEN sprk; /* sprk[i] = zprimestar(P[i]^e[i])*/
  GEN sarch; /* nfarchstar */
  GEN ind;  /* ind[i] = start of vector */
  GEN P, e; /* finit part of conductor = prod P^e */
  GEN archp; /* archimedean part of conductor, in permutation form */
  long n;  /* total number of generators for all (O_K/P^e)^* and (O_K/f_oo) */
  GEN U; /* base change matrix from generators to bid.gen */
} zlog_S;
