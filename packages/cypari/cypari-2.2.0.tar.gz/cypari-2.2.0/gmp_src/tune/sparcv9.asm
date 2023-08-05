dnl  Sparc v9 32-bit time stamp counter access routine.

dnl  Copyright 2000, 2005 Free Software Foundation, Inc.

dnl  This file is part of the GNU MP Library.
dnl
dnl  The GNU MP Library is free software; you can redistribute it and/or modify
dnl  it under the terms of either:
dnl
dnl    * the GNU Lesser General Public License as published by the Free
dnl      Software Foundation; either version 3 of the License, or (at your
dnl      option) any later version.
dnl
dnl  or
dnl
dnl    * the GNU General Public License as published by the Free Software
dnl      Foundation; either version 2 of the License, or (at your option) any
dnl      later version.
dnl
dnl  or both in parallel, as here.
dnl
dnl  The GNU MP Library is distributed in the hope that it will be useful, but
dnl  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
dnl  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
dnl  for more details.
dnl
dnl  You should have received copies of the GNU General Public License and the
dnl  GNU Lesser General Public License along with the GNU MP Library.  If not,
dnl  see https://www.gnu.org/licenses/.

include(`../config.m4')


C void speed_cyclecounter (unsigned p[2]);
C
C Get the sparc v9 tick counter.

ASM_START()
PROLOGUE(speed_cyclecounter)
	rd	%tick,%g1
	st	%g1,[%o0]		C low 32 bits
	srlx	%g1,32,%g4
	retl
	st	%g4,[%o0+4]		C high 32 bits
EPILOGUE(speed_cyclecounter)
