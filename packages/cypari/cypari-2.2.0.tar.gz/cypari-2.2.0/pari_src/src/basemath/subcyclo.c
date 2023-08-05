/* Copyright (C) 2000  The PARI group.

This file is part of the PARI/GP package.

PARI/GP is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation. It is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY WHATSOEVER.

Check the License for details. You should have received a copy of it, along
with the package; see the file 'COPYING'. If not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. */

#include "pari.h"
#include "paripriv.h"

/*************************************************************************/
/**                                                                     **/
/**              Routines for handling subgroups of (Z/nZ)^*            **/
/**              without requiring discrete logarithms.                 **/
/**                                                                     **/
/*************************************************************************/
/* Subgroups are [gen,ord,bits] where
 * gen is a vecsmall of generators
 * ord is theirs relative orders
 * bits is a bit vector of the elements, of length(n). */

/*The algorithm is similar to testpermutation*/
static void
znstar_partial_coset_func(long n, GEN H, void (*func)(void *data,long c)
    , void *data, long d, long c)
{
  GEN gen, ord, cache;
  long i, j, card;

  if (!d) { (*func)(data,c); return; }

  cache = const_vecsmall(d,c);
  (*func)(data,c);  /* AFTER cache: may contain gerepileupto statement */
  gen = gel(H,1);
  ord = gel(H,2);
  card = ord[1]; for (i = 2; i <= d; i++) card *= ord[i];
  for(i=1; i<card; i++)
  {
    long k, m = i;
    for(j=1; j<d && m%ord[j]==0 ;j++) m /= ord[j];
    cache[j] = Fl_mul(cache[j],gen[j],n);
    for (k=1; k<j; k++) cache[k] = cache[j];
    (*func)(data, cache[j]);
  }
}

static void
znstar_coset_func(long n, GEN H, void (*func)(void *data,long c)
    , void *data, long c)
{
  znstar_partial_coset_func(n, H, func,data, lg(gel(H,1))-1, c);
}

/* Add the element of the bitvec of the coset c modulo the subgroup of H
 * generated by the first d generators to the bitvec bits.*/

static void
znstar_partial_coset_bits_inplace(long n, GEN H, GEN bits, long d, long c)
{
  pari_sp av = avma;
  znstar_partial_coset_func(n,H, (void (*)(void *,long)) &F2v_set,
      (void *) bits, d, c);
  avma = av;
}

static void
znstar_coset_bits_inplace(long n, GEN H, GEN bits, long c)
{
  znstar_partial_coset_bits_inplace(n, H, bits, lg(gel(H,1))-1, c);
}

static GEN
znstar_partial_coset_bits(long n, GEN H, long d, long c)
{
  GEN bits = zero_F2v(n);
  znstar_partial_coset_bits_inplace(n,H,bits,d,c);
  return bits;
}

/* Compute the bitvec of the elements of the subgroup of H generated by the
 * first d generators.*/
static GEN
znstar_partial_bits(long n, GEN H, long d)
{
  return znstar_partial_coset_bits(n, H, d, 1);
}

/* Compute the bitvec of the elements of H. */
GEN
znstar_bits(long n, GEN H)
{
  return znstar_partial_bits(n,H,lg(gel(H,1))-1);
}

/* Compute the subgroup of (Z/nZ)^* generated by the elements of
 * the vecsmall V */
GEN
znstar_generate(long n, GEN V)
{
  pari_sp av = avma;
  GEN gen = cgetg(lg(V),t_VECSMALL);
  GEN ord = cgetg(lg(V),t_VECSMALL), res = mkvec2(gen,ord);
  GEN bits = znstar_partial_bits(n,NULL,0);
  long i, r = 0;
  for(i=1; i<lg(V); i++)
  {
    ulong v = uel(V,i), g = v;
    long o = 0;
    while (!F2v_coeff(bits, (long)g)) { g = Fl_mul(g, v, (ulong)n); o++; }
    if (!o) continue;
    r++;
    gen[r] = v;
    ord[r] = o+1;
    cgiv(bits); bits = znstar_partial_bits(n,res,r);
  }
  setlg(gen,r+1);
  setlg(ord,r+1); return gerepilecopy(av, mkvec3(gen,ord,bits));
}

static ulong
znstar_order(GEN H) { return zv_prod(gel(H,2)); }

/* Return the lists of element of H.
 * This can be implemented with znstar_coset_func instead. */
GEN
znstar_elts(long n, GEN H)
{
  long card = znstar_order(H);
  GEN gen = gel(H,1), ord = gel(H,2);
  GEN sg = cgetg(1 + card, t_VECSMALL);
  long k, j, l;
  sg[1] = 1;
  for (j = 1, l = 1; j < lg(gen); j++)
  {
    long c = l * (ord[j]-1);
    for (k = 1; k <= c; k++) sg[++l] = Fl_mul(sg[k], gen[j], n);
  }
  vecsmall_sort(sg); return sg;
}

/* Take a znstar H and n dividing the modulus of H.
 * Output H reduced to modulus n */
GEN
znstar_reduce_modulus(GEN H, long n)
{
  pari_sp ltop=avma;
  GEN gen=cgetg(lgcols(H),t_VECSMALL);
  long i;
  for(i=1; i < lg(gen); i++)
    gen[i] = mael(H,1,i)%n;
  return gerepileupto(ltop, znstar_generate(n,gen));
}

/* Compute conductor of H */
long
znstar_conductor(long n, GEN H)
{
  pari_sp av = avma;
  long i, j, cnd = n;
  GEN F = factoru(n), P = gel(F,1), E = gel(F,2);
  for (i = lg(P)-1; i > 0; i--)
  {
    long p = P[i], e = E[i], q = n;
    if (DEBUGLEVEL>=4) err_printf("SubCyclo: testing %ld^%ld\n",p,e);
    for (  ; e >= 1; e--)
    {
      long z = 1;
      q /= p;
      for (j = 1; j < p; j++)
      {
        z += q;
        if (!F2v_coeff(gel(H,3),z) && ugcd(z,n)==1) break;
      }
      if (j < p)
      {
        if (DEBUGLEVEL>=4) err_printf("SubCyclo: %ld not found\n",z);
        break;
      }
      cnd /= p;
      if (DEBUGLEVEL>=4) err_printf("SubCyclo: new conductor:%ld\n",cnd);
    }
  }
  if (DEBUGLEVEL>=6) err_printf("SubCyclo: conductor:%ld\n",cnd);
  avma = av; return cnd;
}

/* Compute the orbits of a subgroups of Z/nZ given by a generator
 * or a set of generators given as a vector.
 */
GEN
znstar_cosets(long n, long phi_n, GEN H)
{
  long    k;
  long    c = 0;
  long    card   = znstar_order(H);
  long    index  = phi_n/card;
  GEN     cosets = cgetg(index+1,t_VECSMALL);
  pari_sp ltop = avma;
  GEN     bits   = zero_F2v(n);
  for (k = 1; k <= index; k++)
  {
    for (c++ ; F2v_coeff(bits,c) || ugcd(c,n)!=1; c++);
    cosets[k]=c;
    znstar_coset_bits_inplace(n, H, bits, c);
  }
  avma=ltop;
  return cosets;
}


/*************************************************************************/
/**                                                                     **/
/**                     znstar/HNF interface                            **/
/**                                                                     **/
/*************************************************************************/
static GEN
vecmod_to_vecsmall(GEN z)
{
  long i, l = lg(z);
  GEN x = cgetg(l, t_VECSMALL);
  for (i=1; i<l; i++) {
    GEN c = gel(z,i);
    if (typ(c) == t_INTMOD) c = gel(c,2);
    x[i] = itos(c);
  }
  return x;
}
/* Convert a true znstar output by znstar to a `small znstar' */
GEN
znstar_small(GEN zn)
{
  GEN Z = cgetg(4,t_VEC);
  gel(Z,1) = icopy(gmael3(zn,3,1,1));
  gel(Z,2) = vec_to_vecsmall(gel(zn,2));
  gel(Z,3) = vecmod_to_vecsmall(gel(zn,3)); return Z;
}

/* Compute generators for the subgroup of (Z/nZ)* given in HNF. */
GEN
znstar_hnf_generators(GEN Z, GEN M)
{
  long j, h, l = lg(M);
  GEN gen = cgetg(l, t_VECSMALL);
  pari_sp ltop = avma;
  GEN zgen = gel(Z,3);
  ulong n = itou(gel(Z,1));
  for (j = 1; j < l; j++)
  {
    GEN Mj = gel(M,j);
    gen[j] = 1;
    for (h = 1; h < l; h++)
    {
      ulong u = itou(gel(Mj,h));
      if (!u) continue;
      gen[j] = Fl_mul(uel(gen,j), Fl_powu(uel(zgen,h), u, n), n);
    }
  }
  avma = ltop; return gen;
}

GEN
znstar_hnf(GEN Z, GEN M)
{
  return znstar_generate(itos(gel(Z,1)),znstar_hnf_generators(Z,M));
}

GEN
znstar_hnf_elts(GEN Z, GEN H)
{
  pari_sp ltop = avma;
  GEN G = znstar_hnf(Z,H);
  long n = itos(gel(Z,1));
  return gerepileupto(ltop, znstar_elts(n,G));
}

/*************************************************************************/
/**                                                                     **/
/**                     polsubcyclo                                     **/
/**                                                                     **/
/*************************************************************************/

static GEN
gscycloconductor(GEN g, long n, long flag)
{
  if (flag==2) retmkvec2(gcopy(g), stoi(n));
  return g;
}

static long
lift_check_modulus(GEN H, long n)
{
  long h;
  switch(typ(H))
  {
    case t_INTMOD:
      if (!equalsi(n, gel(H,1)))
        pari_err_MODULUS("galoissubcyclo", stoi(n), gel(H,1));
      H = gel(H,2);
    case t_INT:
      h = smodis(H,n);
      if (ugcd(h,n) != 1) pari_err_COPRIME("galoissubcyclo", H,stoi(n));
      return h;
  }
  pari_err_TYPE("galoissubcyclo [subgroup]", H);
  return 0;/*not reached*/
}

/* Compute z^ex using the baby-step/giant-step table powz
 * with only one multiply.
 * In the modular case, the result is not reduced. */
static GEN
polsubcyclo_powz(GEN powz, long ex)
{
  long m = lg(gel(powz,1))-1, q = ex/m, r = ex%m; /*ex=m*q+r*/
  GEN g = gmael(powz,1,r+1), G = gmael(powz,2,q+1);
  return (lg(powz)==4)? mulreal(g,G): gmul(g,G);
}

static GEN
polsubcyclo_complex_bound(pari_sp av, GEN V, long prec)
{
  GEN pol = real_i(roots_to_pol(V,0));
  return gerepileuptoint(av, ceil_safe(gsupnorm(pol,prec)));
}

/* Newton sums mod le. if le==NULL, works with complex instead */
static GEN
polsubcyclo_cyclic(long n, long d, long m ,long z, long g, GEN powz, GEN le)
{
  GEN V = cgetg(d+1,t_VEC);
  ulong base = 1;
  long i,k;
  pari_timer ti;
  if (DEBUGLEVEL >= 6) timer_start(&ti);
  for (i=1; i<=d; i++, base = Fl_mul(base,z,n))
  {
    pari_sp av = avma;
    long ex = base;
    GEN s = gen_0;
    for (k=0; k<m; k++, ex = Fl_mul(ex,g,n))
    {
      s = gadd(s, polsubcyclo_powz(powz,ex));
      if ((k&0xff)==0) s = gerepileupto(av,s);
    }
    if (le) s = modii(s, le);
    gel(V,i) = gerepileupto(av, s);
  }
  if (DEBUGLEVEL >= 6) timer_printf(&ti, "polsubcyclo_cyclic");
  return V;
}

struct _subcyclo_orbits_s
{
  GEN powz;
  GEN *s;
  ulong count;
  pari_sp ltop;
};

static void
_subcyclo_orbits(struct _subcyclo_orbits_s *data, long k)
{
  GEN powz = data->powz;
  GEN *s = data->s;

  if (!data->count) data->ltop = avma;
  *s = gadd(*s, polsubcyclo_powz(powz,k));
  data->count++;
  if ((data->count & 0xffUL) == 0) *s = gerepileupto(data->ltop, *s);
}

/* Newton sums mod le. if le==NULL, works with complex instead */
static GEN
polsubcyclo_orbits(long n, GEN H, GEN O, GEN powz, GEN le)
{
  long i, d = lg(O);
  GEN V = cgetg(d,t_VEC);
  struct _subcyclo_orbits_s data;
  long lle = le?lg(le)*2+1: 2*lg(gmael(powz,1,2))+3;/*dvmdii uses lx+ly space*/
  data.powz = powz;
  for(i=1; i<d; i++)
  {
    GEN s = gen_0;
    pari_sp av = avma;
    (void)new_chunk(lle);
    data.count = 0;
    data.s     = &s;
    znstar_coset_func(n, H, (void (*)(void *,long)) _subcyclo_orbits,
      (void *) &data, O[i]);
    avma = av; /* HACK */
    gel(V,i) = le? modii(s,le): gcopy(s);
  }
  return V;
}

static GEN
polsubcyclo_start(long n, long d, long o, GEN borne, long *ptr_val,long *ptr_l)
{
  pari_sp av;
  GEN le, z, gl;
  long i, l, e, val;
  l = n+1; e = 1;
  while(!uisprime(l)) { l += n; e++; }
  if (DEBUGLEVEL >= 4) err_printf("Subcyclo: prime l=%ld\n",l);
  gl = utoipos(l); av = avma;
  if (!borne)
  { /* Use vecmax(Vec((x+o)^d)) = max{binomial(d,i)*o^i ;1<=i<=d} */
    i = d-(1+d)/(1+o);
    borne = mulii(binomial(utoipos(d),i),powuu(o,i));
  }
  if (DEBUGLEVEL >= 4) err_printf("Subcyclo: bound=2^%ld\n",expi(borne));
  val = logint(shifti(borne,2), gl) + 1;
  avma = av;
  if (DEBUGLEVEL >= 4) err_printf("Subcyclo: val=%ld\n",val);
  le = powiu(gl,val);
  z = utoipos( Fl_powu(pgener_Fl(l), e, l) );
  z = Zp_sqrtnlift(gen_1,utoipos(n),z,gl,val);
  *ptr_val = val;
  *ptr_l = l;
  return gmodulo(z,le);
}

/*Fill in the powz table:
 *  powz[1]: baby-step
 *  powz[2]: giant-step
 *  powz[3] exists only if the field is real (value is ignored). */
static GEN
polsubcyclo_complex_roots(long n, long real, long prec)
{
  long i, m = (long)(1+sqrt((double) n));
  GEN bab, gig, powz = cgetg(real?4:3, t_VEC);

  bab = cgetg(m+1,t_VEC);
  gel(bab,1) = gen_1;
  gel(bab,2) = rootsof1u_cx(n, prec); /* = e_n(1) */
  for (i=3; i<=m; i++) gel(bab,i) = gmul(gel(bab,2),gel(bab,i-1));
  gig = cgetg(m+1,t_VEC);
  gel(gig,1) = gen_1;
  gel(gig,2) = gmul(gel(bab,2),gel(bab,m));;
  for (i=3; i<=m; i++) gel(gig,i) = gmul(gel(gig,2),gel(gig,i-1));
  gel(powz,1) = bab;
  gel(powz,2) = gig;
  if (real) gel(powz,3) = gen_0;
  return powz;
}

static GEN
muliimod_sz(GEN x, GEN y, GEN l, long siz)
{
  pari_sp av = avma;
  GEN p1;
  (void)new_chunk(siz); /* HACK */
  p1 = mulii(x,y);
  avma = av; return modii(p1,l);
}

static GEN
polsubcyclo_roots(long n, GEN zl)
{
  GEN le = gel(zl,1), z = gel(zl,2);
  long i, lle = lg(le)*3; /*Assume dvmdii use lx+ly space*/
  long m = (long)(1+sqrt((double) n));
  GEN bab, gig, powz = cgetg(3,t_VEC);
  pari_timer ti;
  if (DEBUGLEVEL >= 6) timer_start(&ti);
  bab = cgetg(m+1,t_VEC);
  gel(bab,1) = gen_1;
  gel(bab,2) = icopy(z);
  for (i=3; i<=m; i++) gel(bab,i) = muliimod_sz(z,gel(bab,i-1),le,lle);
  gig = cgetg(m+1,t_VEC);
  gel(gig,1) = gen_1;
  gel(gig,2) = muliimod_sz(z,gel(bab,m),le,lle);;
  for (i=3; i<=m; i++) gel(gig,i) = muliimod_sz(gel(gig,2),gel(gig,i-1),le,lle);
  if (DEBUGLEVEL >= 6) timer_printf(&ti, "polsubcyclo_roots");
  gel(powz,1) = bab;
  gel(powz,2) = gig; return powz;
}

GEN
galoiscyclo(long n, long v)
{
  ulong av = avma;
  GEN grp, G, z, le, L, elts;
  long val, l, i, j, k;
  GEN zn = znstar(stoi(n));
  long card = itos(gel(zn,1));
  GEN gen = vec_to_vecsmall(lift_shallow(gel(zn,3)));
  GEN ord = gtovecsmall(gel(zn,2));

  z = polsubcyclo_start(n,card/2,2,NULL,&val,&l);
  le = gel(z,1); z = gel(z,2);
  L = cgetg(1+card,t_VEC);
  gel(L,1) = z;
  for (j = 1, i = 1; j < lg(gen); j++)
  {
    long c = i * (ord[j]-1);
    for (k = 1; k <= c; k++) gel(L,++i) = Fp_powu(gel(L,k), gen[j], le);
  }
  G = abelian_group(ord);
  elts = group_elts(G, card); /*not stack clean*/
  grp = cgetg(9, t_VEC);
  gel(grp,1) = polcyclo(n,v);
  gel(grp,2) = mkvec3(stoi(l), stoi(val), icopy(le));
  gel(grp,3) = gcopy(L);
  gel(grp,4) = FpV_invVandermonde(L,  NULL, le);
  gel(grp,5) = gen_1;
  gel(grp,6) = gcopy(elts);
  gel(grp,7) = gcopy(gel(G,1));
  gel(grp,8) = gcopy(gel(G,2));
  return gerepileupto(av, grp);
}

/* Convert a bnrinit(Q,n) to a znstar(n)
 * complex is set to 0 if the bnr is real and to 1 if it is complex.
 * Not stack clean */
GEN
bnr_to_znstar(GEN bnr, long *complex)
{
  GEN gen, cond, v, bid;
  long l2, i;
  checkbnr(bnr);
  bid = bnr_get_bid(bnr);
  gen = bnr_get_gen(bnr);
  if (nf_get_degree(bnr_get_nf(bnr)) != 1)
    pari_err_DOMAIN("bnr_to_znstar", "bnr", "!=", strtoGENstr("Q"), bnr);
  /* cond is the finite part of the conductor,
   * complex is the infinite part*/
  cond = gcoeff(bid_get_ideal(bid), 1, 1);
  *complex = signe(gel(bid_get_arch(bid), 1));
  l2 = lg(gen);
  v = cgetg(l2, t_VEC);
  for (i = 1; i < l2; ++i)
  {
    GEN x = gel(gen,i);
    switch(typ(x))
    {
      case t_MAT: x = gcoeff(x,1,1); break;
      case t_COL: x = gel(x,1); break;
    }
    gel(v,i) = gmodulo(absi(x), cond);
  }
  return mkvec3(bnr_get_no(bnr), bnr_get_cyc(bnr), v);
}

GEN
galoissubcyclo(GEN N, GEN sg, long flag, long v)
{
  pari_sp ltop= avma, av;
  GEN H, V, B, zl, L, T, le, powz, O, Z = NULL;
  long i, card, phi_n, val,l, n, cnd, complex=1;
  pari_timer ti;

  if (flag<0 || flag>2) pari_err_FLAG("galoissubcyclo");
  if (v < 0) v = 0;
  if (!sg) sg = gen_1;
  switch(typ(N))
  {
    case t_INT:
      n = itos(N);
      if (n < 1)
        pari_err_DOMAIN("galoissubcyclo", "degree", "<=", gen_0, stoi(n));
      break;
    case t_VEC:
      if (lg(N)==7) N = bnr_to_znstar(N,&complex);
      if (lg(N)==4)
      { /* znstar */
        GEN gen = gel(N,3);
        Z = N;
        if (typ(gen)!=t_VEC) pari_err_TYPE("galoissubcyclo",gen);
        if (lg(gen) == 1) n = 1;
        else if (typ(gel(gen,1)) == t_INTMOD)
        {
          GEN z = gel(gen,1);
          n = itos(gel(z,1));
        } else
        {
          pari_err_TYPE("galoissubcyclo",N);
          return NULL;/*Not reached*/
        }
        break;
      }
    default: /*fall through*/
      pari_err_TYPE("galoissubcyclo",N);
      return NULL;/*Not reached*/
  }
  if (n==1) { avma = ltop; return deg1pol_shallow(gen_1,gen_m1,v); }

  switch(typ(sg))
  {
     case t_INTMOD: case t_INT:
      V = mkvecsmall( lift_check_modulus(sg,n) );
      break;
    case t_VECSMALL:
      V = gcopy(sg);
      for (i=1; i<lg(V); i++) { V[i] %= n; if (V[i] < 0) V[i] += n; }
      break;
    case t_VEC:
    case t_COL:
      V = cgetg(lg(sg),t_VECSMALL);
      for(i=1;i<lg(sg);i++) V[i] = lift_check_modulus(gel(sg,i),n);
      break;
    case t_MAT:
      if (lg(sg) == 1 || lg(sg) != lgcols(sg))
        pari_err_TYPE("galoissubcyclo [H not in HNF]", sg);
      if (!Z) pari_err_TYPE("galoissubcyclo [N not a bnrinit or znstar]", sg);
      if ( lg(gel(Z,2)) != lg(sg) ) pari_err_DIM("galoissubcyclo");
      V = znstar_hnf_generators(znstar_small(Z),sg);
      break;
    default:
      pari_err_TYPE("galoissubcyclo",sg);
      return NULL;/*Not reached*/
  }
  if (!complex) V = vecsmall_append(V,n-1); /*add complex conjugation*/
  H = znstar_generate(n,V);
  if (DEBUGLEVEL >= 6)
  {
    err_printf("Subcyclo: elements:");
    for (i=1;i<n;i++)
      if (F2v_coeff(gel(H,3),i)) err_printf(" %ld",i);
    err_printf("\n");
  }
  /* field is real iff z -> conj(z) = z^-1 = z^(n-1) is in H */
  complex = !F2v_coeff(gel(H,3),n-1);
  if (DEBUGLEVEL >= 6) err_printf("Subcyclo: complex=%ld\n",complex);
  if (DEBUGLEVEL >= 1) timer_start(&ti);
  cnd = znstar_conductor(n,H);
  if (DEBUGLEVEL >= 1) timer_printf(&ti, "znstar_conductor");
  if (flag == 1)  { avma=ltop; return stoi(cnd); }
  if (cnd == 1)
  {
    avma = ltop;
    return gscycloconductor(deg1pol_shallow(gen_1,gen_m1,v),1,flag);
  }
  if (n != cnd)
  {
    H = znstar_reduce_modulus(H, cnd);
    n = cnd;
  }
  card = znstar_order(H);
  phi_n = eulerphiu(n);
  if (card == phi_n)
  {
    avma = ltop;
    return gscycloconductor(polcyclo(n,v),n,flag);
  }
  O = znstar_cosets(n, phi_n, H);
  if (DEBUGLEVEL >= 1) timer_printf(&ti, "znstar_cosets");
  if (DEBUGLEVEL >= 6) err_printf("Subcyclo: orbits=%Ps\n",O);
  if (DEBUGLEVEL >= 4)
    err_printf("Subcyclo: %ld orbits with %ld elements each\n",phi_n/card,card);
  av = avma;
  powz = polsubcyclo_complex_roots(n,!complex,LOWDEFAULTPREC);
  L = polsubcyclo_orbits(n,H,O,powz,NULL);
  B = polsubcyclo_complex_bound(av,L,LOWDEFAULTPREC);
  zl = polsubcyclo_start(n,phi_n/card,card,B,&val,&l);
  powz = polsubcyclo_roots(n,zl);
  le = gel(zl,1);
  L = polsubcyclo_orbits(n,H,O,powz,le);
  if (DEBUGLEVEL >= 6) timer_start(&ti);
  T = FpV_roots_to_pol(L,le,v);
  if (DEBUGLEVEL >= 6) timer_printf(&ti, "roots_to_pol");
  T = FpX_center(T,le,shifti(le,-1));
  return gerepileupto(ltop, gscycloconductor(T,n,flag));
}

/* Z = znstar(n) cyclic. n = 1,2,4,p^a or 2p^a,
 * and d | phi(n) = 1,1,2,(p-1)p^(a-1) */
static GEN
polsubcyclo_g(long n, long d, GEN Z, long v)
{
  pari_sp ltop = avma;
  long o, p, r, g, gd, l , val;
  GEN zl, L, T, le, B, powz;
  pari_timer ti;
  if (d==1) return deg1pol_shallow(gen_1,gen_m1,v); /* get rid of n=1,2 */
  if ((n & 3) == 2) n >>= 1;
  /* n = 4 or p^a, p odd */
  o = itos(gel(Z,1));
  g = itos(gmael3(Z,3,1,2));
  p = n / ugcd(n,o); /* p^a / gcd(p^a,phi(p^a)) = p*/
  r = ugcd(d,n); /* = p^(v_p(d)) < n */
  n = r*p; /* n is now the conductor */
  o = n-r; /* = phi(n) */
  if (o == d) return polcyclo(n,v);
  o /= d;
  gd = Fl_powu(g%n, d, n);
  /*FIXME: If degree is small, the computation of B is a waste of time*/
  powz = polsubcyclo_complex_roots(n,(o&1)==0,LOWDEFAULTPREC);
  L = polsubcyclo_cyclic(n,d,o,g,gd,powz,NULL);
  B = polsubcyclo_complex_bound(ltop,L,LOWDEFAULTPREC);
  zl = polsubcyclo_start(n,d,o,B,&val,&l);
  le = gel(zl,1);
  powz = polsubcyclo_roots(n,zl);
  L = polsubcyclo_cyclic(n,d,o,g,gd,powz,le);
  if (DEBUGLEVEL >= 6) timer_start(&ti);
  T = FpV_roots_to_pol(L,le,v);
  if (DEBUGLEVEL >= 6) timer_printf(&ti, "roots_to_pol");
  return gerepileupto(ltop, FpX_center(T,le,shifti(le,-1)));
}

GEN
polsubcyclo(long n, long d, long v)
{
  pari_sp ltop = avma;
  GEN L, Z;
  if (v<0) v = 0;
  if (d<=0) pari_err_DOMAIN("polsubcyclo","d","<=",gen_0,stoi(d));
  if (n<=0) pari_err_DOMAIN("polsubcyclo","n","<=",gen_0,stoi(n));
  Z = znstar(stoi(n));
  if (!dvdis(gel(Z,1), d)) { avma = ltop; return cgetg(1, t_VEC); }
  if (lg(gel(Z,2)) == 2)
  { /* faster but Z must be cyclic */
    avma = ltop;
    return polsubcyclo_g(n, d, Z, v);
  }
  L = subgrouplist(gel(Z,2), mkvec(stoi(d)));
  if (lg(L) == 2)
    return gerepileupto(ltop, galoissubcyclo(Z, gel(L,1), 0, v));
  else
  {
    GEN V = cgetg(lg(L),t_VEC);
    long i;
    for (i=1; i< lg(V); i++) gel(V,i) = galoissubcyclo(Z, gel(L,i), 0, v);
    return gerepileupto(ltop, V);
  }
}

struct aurifeuille_t {
  GEN z, le;
  ulong l;
  long e;
};

/* Let z a primitive n-th root of 1, n > 1, A an integer such that
 * Aurifeuillian factorization of Phi_n(A) exists ( z.A is a square in Q(z) ).
 * Let G(p) the Gauss sum mod p prime:
 *      sum_x (x|p) z^(xn/p) for p odd,  i - 1 for p = 2 [ i := z^(n/4) ]
 * We have N(-1) = Nz = 1 (n != 1,2), and
 *      G^2 = (-1|p) p for p odd,  G^2 = -2i for p = 2
 * In particular, for odd A, (-1|A) A = g^2 is a square. If A = prod p^{e_p},
 * sigma_j(g) = \prod_p (sigma_j G(p)))^e_p = \prod_p (j|p)^e_p g = (j|A) g
 * n odd  : z^2 is a primitive root, A = g^2
 *   Phi_n(A) = N(A - z^2) = N(g - z) N(g + z)
 *
 * n = 2 (4) : -z^2 is a primitive root, -A = g^2
 *   Phi_n(A) = N(A - (-z^2)) = N(g^2 - z^2)  [ N(-1) = 1 ]
 *                            = N(g - z) N(g + z)
 *
 * n = 4 (8) : i z^2 primitive root, -Ai = g^2
 *   Phi_n(A) = N(A - i z^2) = N(-Ai -  z^2) = N(g - z) N(g + z)
 * sigma_j(g) / g =  (j|A)  if j = 1 (4)
 *                  (-j|A)i if j = 3 (4)
 *   */
/* factor Phi_n(A), Astar: A* = squarefree kernel of A, P = odd prime divisors
 * of n */
static GEN
factor_Aurifeuille_aux(GEN A, long Astar, long n, GEN P,
                       struct aurifeuille_t *S)
{
  pari_sp av;
  GEN f, a, b, s, powers, z = S->z, le = S->le;
  long j, k, maxjump, lastj, e = S->e;
  ulong l = S->l;
  char *invertible;

  if ((n & 7) == 4)
  { /* A^* even */
    GEN i = Fp_powu(z, n>>2, le), z2 = Fp_sqr(z, le);

    invertible = stack_malloc(n); /* even indices unused */
    for (j = 1; j < n; j+=2) invertible[j] = 1;
    for (k = 1; k < lg(P); k++)
    {
      long p = P[k];
      for (j = p; j < n; j += 2*p) invertible[j] = 0;
    }
    lastj = 1; maxjump = 2;
    for (j= 3; j < n; j+=2)
      if (invertible[j]) {
        long jump = j - lastj;
        if (jump > maxjump) maxjump = jump;
        lastj = j;
      }
    powers = cgetg(maxjump+1, t_VEC); /* powers[k] = z^k, odd indices unused */
    gel(powers,2) = z2;
    for (k = 4; k <= maxjump; k+=2)
      gel(powers,k) = odd(k>>1)? Fp_mul(gel(powers, k-2), z2, le)
                               : Fp_sqr(gel(powers, k>>1), le);

    if (Astar == 2)
    { /* important special case (includes A=2), split for efficiency */
      if (!equalis(A, 2))
      {
        GEN f = sqrti(shifti(A,-1)), mf = Fp_neg(f,le), fi = Fp_mul(f,i,le);
        a = Fp_add(mf, fi, le);
        b = Fp_sub(mf, fi, le);
      }
      else
      {
        a = addsi(-1,i);
        b = subsi(-1,i);
      }
      av = avma;
      s = z; f = subii(a, s); lastj = 1;
      for (j = 3, k = 0; j < n; j+=2)
        if (invertible[j])
        {
          s = Fp_mul(gel(powers, j-lastj), s, le); /* z^j */
          lastj = j;
          f = Fp_mul(f, subii((j & 3) == 1? a: b, s), le);
          if (++k == 0x1ff) { gerepileall(av, 2, &s, &f); k = 0; }
        }
    }
    else
    {
      GEN ma, mb, B = Fp_mul(A, i, le), gl = utoipos(l);
      long t;
      Astar >>= 1;
      t = Astar & 3; if (Astar < 0) t = 4-t; /* t = 1 or 3 */
      if (t == 1) B = Fp_neg(B, le);
      a = Zp_sqrtlift(B, Fp_sqrt(B, gl), gl, e);
      b = Fp_mul(a, i, le);
      ma = Fp_neg(a, le);
      mb = Fp_neg(b, le);
      av = avma;
      s = z; f = subii(a, s); lastj = 1;
      for (j = 3, k = 0; j<n; j+=2)
        if (invertible[j])
        {
          GEN t;
          if ((j & 3) == 1) t = (kross(j, Astar) < 0)? ma: a;
          else              t = (kross(j, Astar) < 0)? mb: b;
          s = Fp_mul(gel(powers, j-lastj), s, le); /* z^j */
          lastj = j;
          f = Fp_mul(f, subii(t, s), le);
          if (++k == 0x1ff) { gerepileall(av, 2, &s, &f); k = 0; }
        }
    }
  }
  else /* A^* odd */
  {
    ulong g;
    if ((n & 3) == 2)
    { /* A^* = 3 (mod 4) */
      A = negi(A); Astar = -Astar;
      z = Fp_neg(z, le);
      n >>= 1;
    }
    /* A^* = 1 (mod 4) */
    g = Fl_sqrt(umodiu(A,l), l);
    a = Zp_sqrtlift(A, utoipos(g), utoipos(l), e);
    b = negi(a);

    invertible = stack_malloc(n);
    for (j = 1; j < n; j++) invertible[j] = 1;
    for (k = 1; k < lg(P); k++)
    {
      long p = P[k];
      for (j = p; j < n; j += p) invertible[j] = 0;
    }
    lastj = 2; maxjump = 1;
    for (j= 3; j < n; j++)
      if (invertible[j]) {
        long jump = j - lastj;
        if (jump > maxjump) maxjump = jump;
        lastj = j;
      }
    powers = cgetg(maxjump+1, t_VEC); /* powers[k] = z^k */
    gel(powers,1) = z;
    for (k = 2; k <= maxjump; k++)
      gel(powers,k) = odd(k)? Fp_mul(gel(powers, k-1), z, le)
                            : Fp_sqr(gel(powers, k>>1), le);
    av = avma;
    s = z; f = subii(a, s); lastj = 1;
    for(j = 2, k = 0; j < n; j++)
      if (invertible[j])
      {
        s = Fp_mul(gel(powers, j-lastj), s, le);
        lastj = j;
        f = Fp_mul(f, subii(kross(j,Astar)==1? a: b, s), le);
        if (++k == 0x1ff) { gerepileall(av, 2, &s, &f); k = 0; }
      }
  }
  return f;
}

/* fd = factoru(odd part of d = d or d/4). Return eulerphi(d) */
static ulong
phi(long d, GEN fd)
{
  GEN P = gel(fd,1), E = gel(fd,2);
  long i, l = lg(P);
  ulong phi = 1;
  for (i = 1; i < l; i++)
  {
    ulong p = P[i], e = E[i];
    phi *= upowuu(p, e-1)*(p-1);
  }
  if (!odd(d)) phi <<= 1;
  return phi;
}

static void
Aurifeuille_init(GEN a, long d, GEN fd, struct aurifeuille_t *S)
{
  GEN sqrta = sqrtr_abs(itor(a, LOWDEFAULTPREC));
  GEN bound = ceil_safe(powru(addrs(sqrta,1), phi(d, fd)));
  GEN zl = polsubcyclo_start(d, 0, 0, bound, &(S->e), (long*)&(S->l));
  S->le = gel(zl,1);
  S->z  = gel(zl,2);
}

GEN
factor_Aurifeuille_prime(GEN p, long d)
{
  pari_sp av = avma;
  struct aurifeuille_t S;
  GEN fd;
  long pp;
  if ((d & 3) == 2) { d >>= 1; p = negi(p); }
  fd = factoru(odd(d)? d: d>>2);
  pp = itos(p);
  Aurifeuille_init(p, d, fd, &S);
  return gerepileuptoint(av, factor_Aurifeuille_aux(p, pp, d, gel(fd,1), &S));
}

/* an algebraic factor of Phi_d(a), a != 0 */
GEN
factor_Aurifeuille(GEN a, long d)
{
  pari_sp av = avma;
  GEN fd, P, A;
  long i, lP, va = vali(a), sa, astar, D;
  struct aurifeuille_t S;

  if (d <= 0)
    pari_err_DOMAIN("factor_Aurifeuille", "degre", "<=",gen_0,stoi(d));
  if ((d & 3) == 2) { d >>= 1; a = negi(a); }
  if ((va & 1) == (d & 1)) { avma = av; return gen_1; }
  sa = signe(a);
  if (odd(d))
  {
    long a4;
    if (d == 1)
    {
      if (!Z_issquareall(a, &A)) return gen_1;
      return gerepileuptoint(av, addis(A,1));
    }
    A = va? shifti(a, -va): a;
    a4 = mod4(A); if (sa < 0) a4 = 4 - a4;
    if (a4 != 1) { avma = av; return gen_1; }
  }
  else if ((d & 7) == 4)
    A = shifti(a, -va);
  else
  {
    avma = av; return gen_1;
  }
  /* v_2(d) = 0 or 2. Kill 2 from factorization (minor efficiency gain) */
  fd = factoru(odd(d)? d: d>>2); P = gel(fd,1); lP = lg(P);
  astar = sa;
  if (odd(va)) astar <<= 1;
  for (i = 1; i < lP; i++)
    if (odd( (Z_lvalrem(A, P[i], &A)) ) ) astar *= P[i];
  if (sa < 0)
  { /* negate in place if possible */
    if (A == a) A = icopy(A);
    setabssign(A);
  }
  if (!Z_issquare(A)) { avma = av; return gen_1; }

  D = odd(d)? 1: 4;
  for (i = 1; i < lP; i++) D *= P[i];
  if (D != d) { a = powiu(a, d/D); d = D; }

  Aurifeuille_init(a, d, fd, &S);
  return gerepileuptoint(av, factor_Aurifeuille_aux(a, astar, d, P, &S));
}
