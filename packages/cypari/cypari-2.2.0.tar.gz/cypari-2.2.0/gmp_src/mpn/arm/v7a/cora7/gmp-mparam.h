/* gmp-mparam.h -- Compiler/machine parameter header file.

Copyright 1991, 1993, 1994, 1999-2003, 2009, 2010, 2012, 2015 Free Software
Foundation, Inc.

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

#define GMP_LIMB_BITS 32
#define GMP_LIMB_BYTES 4

/* 900 MHz Cortex-A7 (raspberry pi2) */
/* FFT tuning limit = 25 M */
/* Generated by tuneup.c, 2015-05-15, gcc 4.6 */

#define MOD_1_NORM_THRESHOLD                 0  /* always */
#define MOD_1_UNNORM_THRESHOLD               0  /* always */
#define MOD_1N_TO_MOD_1_1_THRESHOLD          3
#define MOD_1U_TO_MOD_1_1_THRESHOLD          6
#define MOD_1_1_TO_MOD_1_2_THRESHOLD         7
#define MOD_1_2_TO_MOD_1_4_THRESHOLD     MP_SIZE_T_MAX
#define PREINV_MOD_1_TO_MOD_1_THRESHOLD     18
#define USE_PREINV_DIVREM_1                  1  /* native */
#define DIV_QR_1N_PI1_METHOD                 1
#define DIV_QR_1_NORM_THRESHOLD             16
#define DIV_QR_1_UNNORM_THRESHOLD            1
#define DIV_QR_2_PI2_THRESHOLD           MP_SIZE_T_MAX  /* never */
#define DIVEXACT_1_THRESHOLD                 0  /* always (native) */
#define BMOD_1_TO_MOD_1_THRESHOLD           47

#define MUL_TOOM22_THRESHOLD                39
#define MUL_TOOM33_THRESHOLD               129
#define MUL_TOOM44_THRESHOLD               195
#define MUL_TOOM6H_THRESHOLD               414
#define MUL_TOOM8H_THRESHOLD               478

#define MUL_TOOM32_TO_TOOM43_THRESHOLD     129
#define MUL_TOOM32_TO_TOOM53_THRESHOLD     183
#define MUL_TOOM42_TO_TOOM53_THRESHOLD     129
#define MUL_TOOM42_TO_TOOM63_THRESHOLD     145
#define MUL_TOOM43_TO_TOOM54_THRESHOLD     191

#define SQR_BASECASE_THRESHOLD               0  /* always (native) */
#define SQR_TOOM2_THRESHOLD                 52
#define SQR_TOOM3_THRESHOLD                162
#define SQR_TOOM4_THRESHOLD                280
#define SQR_TOOM6_THRESHOLD                399
#define SQR_TOOM8_THRESHOLD                567

#define MULMID_TOOM42_THRESHOLD             58

#define MULMOD_BNM1_THRESHOLD               22
#define SQRMOD_BNM1_THRESHOLD               27

#define MUL_FFT_MODF_THRESHOLD             636  /* k = 5 */
#define MUL_FFT_TABLE3                                      \
  { {    636, 5}, {     28, 6}, {     15, 5}, {     31, 6}, \
    {     29, 7}, {     15, 6}, {     33, 7}, {     17, 6}, \
    {     35, 7}, {     19, 6}, {     39, 7}, {     29, 8}, \
    {     15, 7}, {     35, 8}, {     19, 7}, {     43, 8}, \
    {     23, 7}, {     49, 8}, {     27, 7}, {     55, 8}, \
    {     31, 7}, {     63, 8}, {     43, 9}, {     23, 8}, \
    {     55, 9}, {     31, 8}, {     67, 9}, {     39, 8}, \
    {     83, 9}, {     47, 8}, {     95, 9}, {     55,10}, \
    {     31, 9}, {     79,10}, {     47, 9}, {    103,11}, \
    {     31,10}, {     63, 9}, {    135,10}, {     79, 9}, \
    {    159,10}, {     95, 9}, {    191,10}, {    111,11}, \
    {     63,10}, {    159,11}, {     95,10}, {    191,12}, \
    {     63,11}, {    127,10}, {    255, 9}, {    511,10}, \
    {    271, 9}, {    543,11}, {    159,10}, {    319, 9}, \
    {    639,10}, {    335, 9}, {    671,11}, {    191,10}, \
    {    383, 9}, {    767,10}, {    399, 9}, {    799,11}, \
    {    223,12}, {    127,11}, {    255,10}, {    543,11}, \
    {    287,10}, {    607,11}, {    319,10}, {    671,11}, \
    {    351,12}, {    191,11}, {    383,10}, {    799,11}, \
    {    415,13}, {    127,12}, {    255,11}, {    543,10}, \
    {   1087,11}, {    607,12}, {    319,11}, {    735,12}, \
    {    383,11}, {    863,12}, {    447,11}, {    959,13}, \
    {    255,12}, {    511,11}, {   1087,12}, {    575,11}, \
    {   1215,12}, {    703,13}, {    383,12}, {    767,11}, \
    {   1535,12}, {    959,14}, {    255,13}, {    511,12}, \
    {   1215,13}, {    639,12}, {   1471,13}, {    767,12}, \
    {   1663,13}, {    895,12}, {   1855,14}, {    511,13}, \
    {   1023,12}, {   2111,13}, {   1151,12}, {   2431,13}, \
    {   1407,14}, {    767,13}, {   1663,12}, {   3327,13}, \
    {   1791,15}, {    511,14}, {   1023,13}, {   2431,14}, \
    {   1279,13}, {   2815,14}, {  16384,15}, {  32768,16} }
#define MUL_FFT_TABLE3_SIZE 124
#define MUL_FFT_THRESHOLD                 5760

#define SQR_FFT_MODF_THRESHOLD             555  /* k = 5 */
#define SQR_FFT_TABLE3                                      \
  { {    555, 5}, {     28, 6}, {     15, 5}, {     31, 6}, \
    {     29, 7}, {     15, 6}, {     33, 7}, {     17, 6}, \
    {     36, 7}, {     19, 6}, {     39, 7}, {     29, 8}, \
    {     15, 7}, {     35, 8}, {     19, 7}, {     43, 8}, \
    {     23, 7}, {     49, 8}, {     31, 7}, {     63, 8}, \
    {     43, 9}, {     23, 8}, {     55, 9}, {     31, 8}, \
    {     67, 9}, {     39, 8}, {     79, 9}, {     47, 8}, \
    {     95, 9}, {     55,10}, {     31, 9}, {     79,10}, \
    {     47, 9}, {     95,11}, {     31,10}, {     63, 9}, \
    {    135,10}, {     79, 9}, {    159,10}, {     95, 9}, \
    {    191,10}, {    111,11}, {     63,10}, {    143, 9}, \
    {    287,10}, {    159,11}, {     95,10}, {    191,12}, \
    {     63,11}, {    127,10}, {    255, 9}, {    511, 8}, \
    {   1023, 9}, {    543,10}, {    287,11}, {    159,10}, \
    {    319, 9}, {    639,10}, {    335, 9}, {    671,10}, \
    {    351,11}, {    191,10}, {    383, 9}, {    767,10}, \
    {    399, 9}, {    799,10}, {    415,12}, {    127,11}, \
    {    255,10}, {    511, 9}, {   1023,10}, {    543,11}, \
    {    287,10}, {    607,11}, {    319,10}, {    671,11}, \
    {    351,12}, {    191,11}, {    383,10}, {    799,11}, \
    {    415,10}, {    831,13}, {    127,12}, {    255,11}, \
    {    511,10}, {   1023,11}, {    543,10}, {   1087,11}, \
    {    607,12}, {    319,11}, {    735,12}, {    383,11}, \
    {    863,12}, {    447,11}, {    991,12}, {    511,11}, \
    {   1087,12}, {    575,11}, {   1215,12}, {    639,11}, \
    {   1279,12}, {    703,13}, {    383,12}, {    959,13}, \
    {    511,12}, {   1215,13}, {    639,12}, {   1471,13}, \
    {    767,12}, {   1663,13}, {    895,12}, {   1855,14}, \
    {    511,13}, {   1023,12}, {   2111,13}, {   1151,12}, \
    {   2431,13}, {   1407,14}, {    767,13}, {   1663,12}, \
    {   3327,13}, {   1791,15}, {    511,14}, {   1023,13}, \
    {   2431,14}, {   1279,13}, {   2815,14}, {  16384,15}, \
    {  32768,16} }
#define SQR_FFT_TABLE3_SIZE 129
#define SQR_FFT_THRESHOLD                 4736

#define MULLO_BASECASE_THRESHOLD             0  /* always */
#define MULLO_DC_THRESHOLD                  27
#define MULLO_MUL_N_THRESHOLD            11278
#define SQRLO_BASECASE_THRESHOLD             5
#define SQRLO_DC_THRESHOLD                  30
#define SQRLO_SQR_THRESHOLD               8907

#define DC_DIV_QR_THRESHOLD                 32
#define DC_DIVAPPR_Q_THRESHOLD              89
#define DC_BDIV_QR_THRESHOLD                39
#define DC_BDIV_Q_THRESHOLD                112

#define INV_MULMOD_BNM1_THRESHOLD           76
#define INV_NEWTON_THRESHOLD               110
#define INV_APPR_THRESHOLD                  98

#define BINV_NEWTON_THRESHOLD              214
#define REDC_1_TO_REDC_2_THRESHOLD           4
#define REDC_2_TO_REDC_N_THRESHOLD         122

#define MU_DIV_QR_THRESHOLD               1718
#define MU_DIVAPPR_Q_THRESHOLD            1685
#define MUPI_DIV_QR_THRESHOLD               54
#define MU_BDIV_QR_THRESHOLD              1470
#define MU_BDIV_Q_THRESHOLD               1685

#define POWM_SEC_TABLE  1,16,102,615,2016

#define GET_STR_DC_THRESHOLD                29
#define GET_STR_PRECOMPUTE_THRESHOLD        57
#define SET_STR_DC_THRESHOLD               272
#define SET_STR_PRECOMPUTE_THRESHOLD       788

#define FAC_DSC_THRESHOLD                  360
#define FAC_ODD_THRESHOLD                   55

#define MATRIX22_STRASSEN_THRESHOLD         27
#define HGCD_THRESHOLD                      55
#define HGCD_APPR_THRESHOLD                 51
#define HGCD_REDUCE_THRESHOLD             3389
#define GCD_DC_THRESHOLD                   168
#define GCDEXT_DC_THRESHOLD                189
#define JACOBI_BASE_METHOD                   1
