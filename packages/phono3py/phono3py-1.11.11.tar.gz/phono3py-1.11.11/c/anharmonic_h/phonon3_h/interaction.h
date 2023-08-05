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

#ifndef __interaction_H__
#define __interaction_H__

#include <lapacke.h>
#include <phonoc_array.h>

void get_interaction(Darray *fc3_normal_squared,
		     const char *g_zero,
		     const Darray *frequencies,
		     const Carray *eigenvectors,
		     const Iarray *triplets,
		     const int *grid_address,
		     const int *mesh,
		     const Darray *fc3,
		     const Darray *shortest_vectors,
		     const Iarray *multiplicity,
		     const double *masses,
		     const int *p2s_map,
		     const int *s2p_map,
		     const int *band_indices,
		     const int is_sym_q,
		     const double cutoff_frequency);
void get_interaction_at_triplet(double *fc3_normal_squared,
                                const int num_band0,
                                const int num_band,
                                const char *g_zero,
                                const double *frequencies,
                                const lapack_complex_double *eigenvectors,
                                const int *triplet,
                                const int *grid_address,
                                const int *mesh,
                                const double *fc3,
                                const Darray *shortest_vectors,
                                const int *multiplicity,
                                const double *masses,
                                const int *p2s_map,
                                const int *s2p_map,
                                const int *band_indices,
                                const int symmetrize_fc3_q,
                                const double cutoff_frequency,
                                const int triplet_index,
                                const int num_triplets,
                                const int openmp_at_bands);
#endif
