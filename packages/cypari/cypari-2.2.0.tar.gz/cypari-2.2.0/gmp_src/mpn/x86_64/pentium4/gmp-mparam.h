/* Pentium 4-64 gmp-mparam.h -- Compiler/machine parameter header file.

Copyright 1991, 1993, 1994, 2000-2010, 2014 Free Software Foundation, Inc.

This file is part of the GNU MP Library.

The GNU MP Library is free software; you can redistribute it and/or modify
it under the terms of either:

  * the GNU Lesser General Public License as published by the Free
    Software Foundation; either version 3 of the License, or (at your
    option) any later version.

or

  * the GNU General Public License as published by the Free Software
    Foundation; either version 2 of the License, or (at your option) any
    later version.

or both in parallel, as here.

The GNU MP Library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received copies of the GNU General Public License and the
GNU Lesser General Public License along with the GNU MP Library.  If not,
see https://www.gnu.org/licenses/.  */

#define GMP_LIMB_BITS 64
#define GMP_LIMB_BYTES 8

/* These routines exists for all x86_64 chips, but they are slower on Pentium4
   than separate add/sub and shift.  Make sure they are not really used.  */
#undef HAVE_NATIVE_mpn_rsblsh1_n
#undef HAVE_NATIVE_mpn_rsblsh2_n
#undef HAVE_NATIVE_mpn_addlsh_n
#undef HAVE_NATIVE_mpn_rsblsh_n

/* 3400 MHz Pentium4 Nocona / 1024 Kibyte cache */
/* FFT tuning limit = 25000000 */
/* Generated by tuneup.c, 2014-03-12, gcc 4.5 */

#define MOD_1_NORM_THRESHOLD                 0  /* always */
#define MOD_1_UNNORM_THRESHOLD               0  /* always */
#define MOD_1N_TO_MOD_1_1_THRESHOLD          4
#define MOD_1U_TO_MOD_1_1_THRESHOLD          3
#define MOD_1_1_TO_MOD_1_2_THRESHOLD        16
#define MOD_1_2_TO_MOD_1_4_THRESHOLD        32
#define PREINV_MOD_1_TO_MOD_1_THRESHOLD     11
#define USE_PREINV_DIVREM_1                  1  /* native */
#define DIV_QR_1_NORM_THRESHOLD              1
#define DIV_QR_1_UNNORM_THRESHOLD        MP_SIZE_T_MAX  /* never */
#define DIV_QR_2_PI2_THRESHOLD           MP_SIZE_T_MAX  /* never */
#define DIVEXACT_1_THRESHOLD                 0  /* always (native) */
#define BMOD_1_TO_MOD_1_THRESHOLD           20

#define MUL_TOOM22_THRESHOLD                12
#define MUL_TOOM33_THRESHOLD                41
#define MUL_TOOM44_THRESHOLD               112
#define MUL_TOOM6H_THRESHOLD               157
#define MUL_TOOM8H_THRESHOLD               236

#define MUL_TOOM32_TO_TOOM43_THRESHOLD      73
#define MUL_TOOM32_TO_TOOM53_THRESHOLD      91
#define MUL_TOOM42_TO_TOOM53_THRESHOLD      81
#define MUL_TOOM42_TO_TOOM63_THRESHOLD      78
#define MUL_TOOM43_TO_TOOM54_THRESHOLD     106

#define SQR_BASECASE_THRESHOLD               5
#define SQR_TOOM2_THRESHOLD                 30
#define SQR_TOOM3_THRESHOLD                 53
#define SQR_TOOM4_THRESHOLD                154
#define SQR_TOOM6_THRESHOLD                197
#define SQR_TOOM8_THRESHOLD                296

#define MULMID_TOOM42_THRESHOLD             22

#define MULMOD_BNM1_THRESHOLD                9
#define SQRMOD_BNM1_THRESHOLD                9

#define MUL_FFT_MODF_THRESHOLD             252  /* k = 5 */
#define MUL_FFT_TABLE3                                      \
  { {    252, 5}, {     11, 6}, {      6, 5}, {     13, 6}, \
    {     13, 7}, {      7, 6}, {     15, 7}, {      8, 6}, \
    {     17, 7}, {      9, 6}, {     19, 7}, {     13, 8}, \
    {      7, 7}, {     17, 8}, {      9, 7}, {     20, 8}, \
    {     11, 7}, {     23, 8}, {     13, 9}, {      7, 8}, \
    {     21, 9}, {     11, 8}, {     25,10}, {      7, 9}, \
    {     15, 8}, {     33, 9}, {     19, 8}, {     39, 9}, \
    {     23, 8}, {     47,10}, {     15, 9}, {     39,10}, \
    {     23, 9}, {     51,11}, {     15,10}, {     31, 9}, \
    {     67,10}, {     39, 9}, {     79,10}, {     47, 9}, \
    {     95,10}, {     55,11}, {     31,10}, {     63, 9}, \
    {    127, 8}, {    255,10}, {     71, 9}, {    143, 8}, \
    {    287,10}, {     79,11}, {     47,10}, {     95, 9}, \
    {    191,10}, {    103,12}, {     31,11}, {     63,10}, \
    {    127, 9}, {    255,10}, {    143, 9}, {    287,11}, \
    {     79,10}, {    159, 9}, {    319,10}, {    175, 9}, \
    {    351,11}, {     95,10}, {    191, 9}, {    383,10}, \
    {    223,12}, {     63,11}, {    127,10}, {    255,11}, \
    {    143,10}, {    287, 9}, {    575, 8}, {   1151,11}, \
    {    159,10}, {    319,11}, {    175,10}, {    351,12}, \
    {     95,11}, {    191,10}, {    383,11}, {    207,10}, \
    {    415,11}, {    223,13}, {     63,12}, {    127,11}, \
    {    255,10}, {    511,11}, {    287,10}, {    575, 9}, \
    {   1151,12}, {    159,11}, {    319,10}, {    639,11}, \
    {    351,10}, {    703,12}, {    191,11}, {    383,10}, \
    {    767,11}, {    415,12}, {    223,11}, {    447,13}, \
    {    127,12}, {    255,11}, {    511,12}, {    287,11}, \
    {    575,10}, {   1151,12}, {    319,11}, {    639,12}, \
    {    351,11}, {    703,13}, {    191,12}, {    383,11}, \
    {    767,12}, {    415,11}, {    831,12}, {    447,11}, \
    {    895,14}, {    127,13}, {    255,12}, {    511,11}, \
    {   1023,12}, {    543,11}, {   1087,10}, {   2175,12}, \
    {    575,11}, {   1151,13}, {    319,12}, {    639,11}, \
    {   1279,12}, {    703,11}, {   1407,10}, {   2815,13}, \
    {    383,12}, {    767,11}, {   1535,12}, {    831,11}, \
    {   1663,13}, {    447,12}, {    895,14}, {    255,13}, \
    {    511,12}, {   1023,11}, {   2047,12}, {   1087,11}, \
    {   2175,13}, {    575,12}, {   1151,11}, {   2303,12}, \
    {   1215,11}, {   2431,10}, {   4863,13}, {    639,12}, \
    {   1279,11}, {   2559,13}, {    703,12}, {   1407,11}, \
    {   2815,14}, {    383,13}, {    767,12}, {   1535,13}, \
    {    831,12}, {   1663,13}, {    895,15}, {    255,14}, \
    {    511,13}, {   1023,12}, {   2047,13}, {   1087,12}, \
    {   2175,13}, {   1151,12}, {   2303,13}, {   1215,12}, \
    {   2431,11}, {   4863,14}, {    639,13}, {   1279,12}, \
    {   2559,13}, {   1407,12}, {   2815,14}, {    767,13}, \
    {   1663,14}, {    895,13}, {   1791,12}, {   3583,13}, \
    {   1919,12}, {   3839,15}, {    511,14}, {   1023,13}, \
    {   2175,14}, {   1151,13}, {   2303,12}, {   4607,13}, \
    {   2431,12}, {   4863,14}, {   1279,13}, {   2559,14}, \
    {   1407,13}, {   2815,15}, {  32768,16}, {  65536,17}, \
    { 131072,18}, { 262144,19}, { 524288,20}, {1048576,21}, \
    {2097152,22}, {4194304,23}, {8388608,24} }
#define MUL_FFT_TABLE3_SIZE 211
#define MUL_FFT_THRESHOLD                 2240

#define SQR_FFT_MODF_THRESHOLD             212  /* k = 5 */
#define SQR_FFT_TABLE3                                      \
  { {    212, 5}, {     11, 6}, {      6, 5}, {     13, 6}, \
    {     13, 7}, {      7, 6}, {     15, 7}, {      9, 6}, \
    {     19, 7}, {     13, 8}, {      7, 7}, {     17, 8}, \
    {      9, 7}, {     20, 8}, {     11, 7}, {     24, 8}, \
    {     13, 9}, {      7, 8}, {     21, 9}, {     11, 8}, \
    {     25,10}, {      7, 9}, {     15, 8}, {     33, 9}, \
    {     19, 8}, {     39, 9}, {     23, 8}, {     47,10}, \
    {     15, 9}, {     39,10}, {     23, 9}, {     47,11}, \
    {     15,10}, {     31, 9}, {     63, 8}, {    127, 9}, \
    {     67,10}, {     39, 9}, {     79,10}, {     55,11}, \
    {     31,10}, {     63, 9}, {    127, 8}, {    255,10}, \
    {     71, 9}, {    143, 8}, {    287,10}, {     79, 9}, \
    {    159,11}, {     47, 9}, {    191,12}, {     31,11}, \
    {     63,10}, {    127, 9}, {    255,10}, {    143, 9}, \
    {    287,11}, {     79,10}, {    159, 9}, {    319,10}, \
    {    175, 9}, {    351,10}, {    191, 9}, {    383,10}, \
    {    207,11}, {    111,10}, {    223,12}, {     63,11}, \
    {    127,10}, {    255,11}, {    143,10}, {    287, 9}, \
    {    575,11}, {    159,10}, {    319,11}, {    175,10}, \
    {    351,11}, {    191,10}, {    383,11}, {    223,13}, \
    {     63,12}, {    127,11}, {    255,10}, {    511,11}, \
    {    287,10}, {    575,12}, {    159,11}, {    351,12}, \
    {    191,11}, {    383,12}, {    223,11}, {    447,13}, \
    {    127,12}, {    255,11}, {    511,12}, {    287,11}, \
    {    575,10}, {   1151,12}, {    319,11}, {    639,12}, \
    {    351,13}, {    191,12}, {    383,11}, {    767,12}, \
    {    415,11}, {    831,12}, {    447,14}, {    127,13}, \
    {    255,12}, {    511,11}, {   1023,10}, {   2047,11}, \
    {   1087,12}, {    575,11}, {   1151,13}, {    319,12}, \
    {    639,11}, {   1279,12}, {    703,11}, {   1407,13}, \
    {    383,12}, {    767,11}, {   1535,12}, {    831,13}, \
    {    447,14}, {    255,13}, {    511,12}, {   1023,11}, \
    {   2047,13}, {    575,12}, {   1151,11}, {   2303,12}, \
    {   1215,13}, {    639,12}, {   1279,11}, {   2559,13}, \
    {    703,14}, {    383,13}, {    767,12}, {   1535,13}, \
    {    831,12}, {   1663,13}, {    895,15}, {    255,14}, \
    {    511,13}, {   1023,12}, {   2047,13}, {   1087,12}, \
    {   2175,13}, {   1151,12}, {   2303,13}, {   1215,12}, \
    {   2431,14}, {    639,13}, {   1279,12}, {   2687,13}, \
    {   1407,12}, {   2815,14}, {    767,13}, {   1663,14}, \
    {    895,13}, {   1791,12}, {   3583,15}, {    511,14}, \
    {   1023,13}, {   2175,14}, {   1151,13}, {   2303,12}, \
    {   4607,13}, {   2431,12}, {   4863,14}, {   1279,13}, \
    {   2559,14}, {   1407,13}, {   2815,15}, {  32768,16}, \
    {  65536,17}, { 131072,18}, { 262144,19}, { 524288,20}, \
    {1048576,21}, {2097152,22}, {4194304,23}, {8388608,24} }
#define SQR_FFT_TABLE3_SIZE 184
#define SQR_FFT_THRESHOLD                 1984

#define MULLO_BASECASE_THRESHOLD             0  /* always */
#define MULLO_DC_THRESHOLD                  33
#define MULLO_MUL_N_THRESHOLD             4392

#define DC_DIV_QR_THRESHOLD                 35
#define DC_DIVAPPR_Q_THRESHOLD              68
#define DC_BDIV_QR_THRESHOLD                32
#define DC_BDIV_Q_THRESHOLD                 56

#define INV_MULMOD_BNM1_THRESHOLD           22
#define INV_NEWTON_THRESHOLD               195
#define INV_APPR_THRESHOLD                 116

#define BINV_NEWTON_THRESHOLD              199
#define REDC_1_TO_REDC_2_THRESHOLD           4
#define REDC_2_TO_REDC_N_THRESHOLD          42

#define MU_DIV_QR_THRESHOLD                979
#define MU_DIVAPPR_Q_THRESHOLD             979
#define MUPI_DIV_QR_THRESHOLD               91
#define MU_BDIV_QR_THRESHOLD               855
#define MU_BDIV_Q_THRESHOLD                942

#define POWM_SEC_TABLE  1,16,175,692,1603

#define MATRIX22_STRASSEN_THRESHOLD         17
#define HGCD_THRESHOLD                     109
#define HGCD_APPR_THRESHOLD                119
#define HGCD_REDUCE_THRESHOLD             1679
#define GCD_DC_THRESHOLD                   222
#define GCDEXT_DC_THRESHOLD                238
#define JACOBI_BASE_METHOD                   4

#define GET_STR_DC_THRESHOLD                12
#define GET_STR_PRECOMPUTE_THRESHOLD        24
#define SET_STR_DC_THRESHOLD               537
#define SET_STR_PRECOMPUTE_THRESHOLD      1430

#define FAC_DSC_THRESHOLD                 1127
#define FAC_ODD_THRESHOLD                    0  /* always */
