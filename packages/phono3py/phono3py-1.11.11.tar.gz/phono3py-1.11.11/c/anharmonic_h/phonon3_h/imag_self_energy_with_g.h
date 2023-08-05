/* Copyright (C) 2015 Atsushi Togo */
/* All rights reserved. */

/* This file is part of phonopy. */

/* Redistribution and use in source and binary forms, with or without */
/* modification, are permitted provided that the following conditions */
/* are met: */

/* * Redistributions of source code must retain the above copyright */
/*   notice, this list of conditions and the following disclaimer. */

/* * Redistributions in binary form must reproduce the above copyright */
/*   notice, this list of conditions and the following disclaimer in */
/*   the documentation and/or other materials provided with the */
/*   distribution. */

/* * Neither the name of the phonopy project nor the names of its */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission. */

/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS */
/* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT */
/* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS */
/* FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE */
/* COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, */
/* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, */
/* BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; */
/* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER */
/* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT */
/* LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN */
/* ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE */
/* POSSIBILITY OF SUCH DAMAGE. */

#ifndef __imag_self_energy_with_g_H__
#define __imag_self_energy_with_g_H__

#include <phonoc_array.h>

void get_imag_self_energy_at_bands_with_g(double *imag_self_energy,
					  const Darray *fc3_normal_squared,
					  const double *frequencies,
					  const int *triplets,
					  const int *weights,
					  const double *g,
					  const char *g_zero,
					  const double temperature,
					  const double cutoff_frequency);
void get_detailed_imag_self_energy_at_bands_with_g
(double *detailed_imag_self_energy,
 double *imag_self_energy_N,
 double *imag_self_energy_U,
 const Darray *fc3_normal_squared,
 const double *frequencies,
 const int *triplets,
 const int *weights,
 const int *grid_address,
 const double *g,
 const char *g_zero,
 const double temperature,
 const double unit_conversion_factor,
 const double cutoff_frequency);
void imag_self_energy_at_triplet(double *imag_self_energy,
                                 const int num_band0,
                                 const int num_band,
                                 const double *fc3_normal_squared,
                                 const double *frequencies,
                                 const int *triplets,
                                 const int triplet_weight,
                                 const double *g1,
                                 const double *g2_3,
                                 const char *g_zero,
                                 const double temperature,
                                 const double cutoff_frequency,
                                 const int openmp_at_bands);

#endif
