import sys
import numpy as np
from phonopy.phonon.degeneracy import degenerate_sets
from phonopy.harmonic.force_constants import similarity_transformation
from phonopy.units import THz, Angstrom
from phono3py.phonon3.conductivity import Conductivity, unit_to_WmK
from phono3py.phonon3.collision_matrix import CollisionMatrix
from phono3py.phonon3.triplets import (get_grid_points_by_rotations,
                                       get_BZ_grid_points_by_rotations)
from phono3py.file_IO import (write_kappa_to_hdf5,
                              write_collision_to_hdf5,
                              read_collision_from_hdf5,
                              write_collision_eigenvalues_to_hdf5)
from phonopy.units import THzToEv, Kb

def get_thermal_conductivity_LBTE(
        interaction,
        symmetry,
        temperatures=np.arange(0, 1001, 10, dtype='double'),
        sigmas=None,
        is_isotope=False,
        mass_variances=None,
        grid_points=None,
        boundary_mfp=None, # in micrometre
        is_reducible_collision_matrix=False,
        is_kappa_star=True,
        gv_delta_q=1e-4, # for group velocity
        is_full_pp=False,
        pinv_cutoff=1.0e-8,
        write_collision=False,
        read_collision=False,
        write_kappa=False,
        input_filename=None,
        output_filename=None,
        log_level=0):

    if sigmas is None:
        sigmas = []
    if log_level:
        print("-------------------- Lattice thermal conducitivity (LBTE) "
              "--------------------")
        print("Cutoff frequency of pseudo inversion of collision matrix: %s" %
              pinv_cutoff)

    if read_collision:
        temps = None
    else:
        temps = temperatures

    lbte = Conductivity_LBTE(
        interaction,
        symmetry,
        grid_points=grid_points,
        temperatures=temps,
        sigmas=sigmas,
        is_isotope=is_isotope,
        mass_variances=mass_variances,
        boundary_mfp=boundary_mfp,
        is_reducible_collision_matrix=is_reducible_collision_matrix,
        is_kappa_star=is_kappa_star,
        gv_delta_q=gv_delta_q,
        is_full_pp=is_full_pp,
        pinv_cutoff=pinv_cutoff,
        log_level=log_level)

    if read_collision:
        read_from = _set_collision_from_file(
            lbte,
            indices=read_collision,
            filename=input_filename,
            log_level=log_level)
        if not read_from:
            print("Reading collisions failed.")
            return False
        if log_level:
            temperatures = lbte.get_temperatures()
            if len(temperatures) > 5:
                text = (" %.1f " * 5 + "...") % tuple(temperatures[:5])
                text += " %.1f" % temperatures[-1]
            else:
                text = (" %.1f " * len(temperatures)) % tuple(temperatures)
            print("Temperature: " + text)

    for i in lbte:
        if write_collision:
            _write_collision(lbte, i=i, filename=output_filename)

    if (not read_collision) or (read_collision and read_from == "grid_points"):
        if grid_points is None:
            _write_collision(lbte, filename=output_filename)

    if write_kappa and grid_points is None:
        lbte.set_kappa_at_sigmas()
        _write_kappa(
            lbte,
            interaction.get_primitive().get_volume(),
            is_reducible_collision_matrix=is_reducible_collision_matrix,
            filename=output_filename,
            log_level=log_level)

    return lbte

def _write_collision(lbte, i=None, filename=None):
    temperatures = lbte.get_temperatures()
    sigmas = lbte.get_sigmas()
    gamma = lbte.get_gamma()
    gamma_isotope = lbte.get_gamma_isotope()
    collision_matrix = lbte.get_collision_matrix()
    mesh = lbte.get_mesh_numbers()

    if i is not None:
        gp = lbte.get_grid_points()[i]
        for j, sigma in enumerate(sigmas):
            if gamma_isotope is not None:
                gamma_isotope_at_sigma = gamma_isotope[j, i]
            else:
                gamma_isotope_at_sigma = None
            write_collision_to_hdf5(temperatures,
                                    mesh,
                                    gamma=gamma[j, :, i],
                                    gamma_isotope=gamma_isotope_at_sigma,
                                    collision_matrix=collision_matrix[j, :, i],
                                    grid_point=gp,
                                    sigma=sigma,
                                    filename=filename)
    else:
        for j, sigma in enumerate(sigmas):
            if gamma_isotope is not None:
                gamma_isotope_at_sigma = gamma_isotope[j]
            else:
                gamma_isotope_at_sigma = None
            write_collision_to_hdf5(temperatures,
                                    mesh,
                                    gamma=gamma[j],
                                    gamma_isotope=gamma_isotope_at_sigma,
                                    collision_matrix=collision_matrix[j],
                                    sigma=sigma,
                                    filename=filename)

def _write_kappa(lbte,
                 volume,
                 is_reducible_collision_matrix=False,
                 filename=None,
                 log_level=0):
    temperatures = lbte.get_temperatures()
    sigmas = lbte.get_sigmas()
    mesh = lbte.get_mesh_numbers()
    weights = lbte.get_grid_weights()
    frequencies = lbte.get_frequencies()
    ave_pp = lbte.get_averaged_pp_interaction()
    qpoints = lbte.get_qpoints()
    kappa = lbte.get_kappa()
    coleigs = lbte.get_collision_eigenvalues()

    if is_reducible_collision_matrix:
        ir_gp = lbte.get_grid_points()
        # frequencies = lbte.get_frequencies_all()
        gamma = lbte.get_gamma()[:, :, ir_gp, :]
        gamma_isotope = lbte.get_gamma_isotope()
        if gamma_isotope is not None:
            gamma_isotope = gamma_isotope[:, ir_gp, :]
        gv = lbte.get_group_velocities()[ir_gp]
        gv_by_gv = lbte.get_gv_by_gv()[ir_gp]
        mode_cv = lbte.get_mode_heat_capacities()[:, ir_gp, :]
        mode_kappa = lbte.get_mode_kappa()[:, :, ir_gp, :, :]
        for i, w in enumerate(weights):
            mode_kappa[:, :, i, :, :] *= w
        mfp = lbte.get_mean_free_path()[:, :, ir_gp, :, :]
    else:
        frequencies = lbte.get_frequencies()
        gamma = lbte.get_gamma()
        gamma_isotope = lbte.get_gamma_isotope()
        gv = lbte.get_group_velocities()
        gv_by_gv = lbte.get_gv_by_gv()
        mode_cv = lbte.get_mode_heat_capacities()
        mode_kappa = lbte.get_mode_kappa()
        mfp = lbte.get_mean_free_path()

    for i, sigma in enumerate(sigmas):
        if gamma_isotope is not None:
            gamma_isotope_at_sigma = gamma_isotope[i]
        else:
            gamma_isotope_at_sigma = None
        write_kappa_to_hdf5(temperatures,
                            mesh,
                            frequency=frequencies,
                            group_velocity=gv,
                            gv_by_gv=gv_by_gv,
                            mean_free_path=mfp[i],
                            heat_capacity=mode_cv,
                            kappa=kappa[i],
                            mode_kappa=mode_kappa[i],
                            gamma=gamma[i],
                            gamma_isotope=gamma_isotope_at_sigma,
                            averaged_pp_interaction=ave_pp,
                            qpoint=qpoints,
                            weight=weights,
                            sigma=sigma,
                            kappa_unit_conversion=unit_to_WmK / volume,
                            filename=filename,
                            verbose=log_level)
        
        if coleigs is not None:
            write_collision_eigenvalues_to_hdf5(temperatures,
                                                mesh,
                                                coleigs[i],
                                                sigma=sigma,
                                                filename=filename,
                                                verbose=log_level)


def _set_collision_from_file(lbte,
                             indices='all',
                             filename=None,
                             log_level=0):
    sigmas = lbte.get_sigmas()
    mesh = lbte.get_mesh_numbers()
    grid_points = lbte.get_grid_points()

    gamma = []
    collision_matrix = []

    read_from = None

    if log_level:
        print("---------------------- Reading collision data from file "
              "----------------------")
        sys.stdout.flush()

    for j, sigma in enumerate(sigmas):
        collisions = read_collision_from_hdf5(mesh,
                                              sigma=sigma,
                                              filename=filename,
                                              verbose=(log_level > 0))
        if log_level:
            sys.stdout.flush()
        if collisions is False:
            gamma_of_gps = []
            collision_matrix_of_gps = []
            for i, gp in enumerate(grid_points):
                collision_gp = read_collision_from_hdf5(
                    mesh,
                    grid_point=gp,
                    sigma=sigma,
                    filename=filename,
                    verbose=(log_level > 0))
                if log_level:
                    sys.stdout.flush()

                if collision_gp is False:
                    print("Gamma at grid point %d doesn't exist." % gp)
                    return False

                (collision_matrix_at_gp,
                 gamma_at_gp,
                 temperatures_at_gp) = collision_gp
                if indices == 'all':
                    gamma_of_gps.append(gamma_at_gp)
                    collision_matrix_of_gps.append(collision_matrix_at_gp)
                    temperatures = temperatures_at_gp
                else:
                    gamma_of_gps.append(gamma_at_gp[indices])
                    collision_matrix_of_gps.append(
                        collision_matrix_at_gp[indices])
                    temperatures = temperatures_at_gp[indices]

            gamma_at_sigma = np.zeros((len(temperatures),
                                       len(grid_points),
                                       len(gamma_of_gps[0][0])),
                                       dtype='double')
            collision_matrix_at_sigma = np.zeros((len(temperatures),
                                                  len(grid_points),
                                                  len(gamma_of_gps[0][0]),
                                                  3,
                                                  len(grid_points),
                                                  len(gamma_of_gps[0][0]),
                                                  3),
                                                  dtype='double')
            for k in range(len(temperatures)):
                for l in range(len(grid_points)):
                    gamma_at_sigma[k, l] = gamma_of_gps[l][k]
                    collision_matrix_at_sigma[
                        k, l] = collision_matrix_of_gps[l][k]

            gamma.append(gamma_at_sigma)
            collision_matrix.append(collision_matrix_at_sigma)

            read_from = "grid_points"
        else:
            (collision_matrix_at_sigma,
             gamma_at_sigma,
             temperatures_at_sigma) = collisions

            if indices == 'all':
                collision_matrix.append(collision_matrix_at_sigma)
                gamma.append(gamma_at_sigma)
                temperatures = temperatures_at_sigma
            else:
                collision_matrix.append(collision_matrix_at_sigma[indices])
                gamma.append(gamma_at_sigma[indices])
                temperatures = temperatures_at_sigma[indices]

            read_from = "full_matrix"

    temperatures = np.array(temperatures, dtype='double', order='C')
    gamma = np.array(gamma, dtype='double', order='C')
    collision_matrix = np.array(collision_matrix, dtype='double', order='C')

    lbte.set_temperatures(temperatures)
    lbte.set_gamma(gamma)
    lbte.set_collision_matrix(collision_matrix)

    return read_from

class Conductivity_LBTE(Conductivity):
    def __init__(self,
                 interaction,
                 symmetry,
                 grid_points=None,
                 temperatures=None,
                 sigmas=None,
                 is_isotope=False,
                 mass_variances=None,
                 boundary_mfp=None, # in micrometre
                 is_reducible_collision_matrix=False,
                 is_kappa_star=True,
                 gv_delta_q=None, # finite difference for group veolocity
                 is_full_pp=False,
                 pinv_cutoff=1.0e-8,
                 log_level=0):
        self._pp = None
        self._temperatures = None
        self._sigmas = None
        self._is_kappa_star = None
        self._gv_delta_q = None
        self._is_full_pp = None
        self._log_level = None
        self._primitive = None
        self._dm = None
        self._frequency_factor_to_THz = None
        self._cutoff_frequency = None
        self._boundary_mfp = None

        self._symmetry = None
        self._point_operations = None
        self._rotations_cartesian = None

        self._grid_points = None
        self._grid_weights = None
        self._grid_address = None
        self._ir_grid_points = None
        self._ir_grid_weights = None

        self._read_gamma = False
        self._read_gamma_iso = False

        self._frequencies = None
        self._cv = None
        self._gv = None
        self._gv_sum2 = None
        self._mfp = None
        self._gamma = None
        self._gamma_iso = None
        self._averaged_pp_interaction = None

        self._mesh = None
        self._conversion_factor = None

        self._is_isotope = None
        self._isotope = None
        self._mass_variances = None
        self._grid_point_count = None

        self._collision_eigenvalues = None

        Conductivity.__init__(self,
                              interaction,
                              symmetry,
                              grid_points=grid_points,
                              temperatures=temperatures,
                              sigmas=sigmas,
                              is_isotope=is_isotope,
                              mass_variances=mass_variances,
                              boundary_mfp=boundary_mfp,
                              is_kappa_star=is_kappa_star,
                              gv_delta_q=gv_delta_q,
                              is_full_pp=is_full_pp,
                              log_level=log_level)

        self._is_reducible_collision_matrix = is_reducible_collision_matrix
        if not self._is_kappa_star:
            self._is_reducible_collision_matrix = True
        self._collision_matrix = None
        self._pinv_cutoff = pinv_cutoff

        if self._temperatures is not None:
            self._allocate_values()

    def set_kappa_at_sigmas(self):
        if len(self._grid_points) != len(self._ir_grid_points):
            print("Collision matrix is not well created.")
            import sys
            sys.exit(1)
        else:
            self._set_kappa_at_sigmas()

    def set_collision_matrix(self, collision_matrix):
        self._collision_matrix = collision_matrix

    def get_collision_matrix(self):
        return self._collision_matrix

    def get_collision_eigenvalues(self):
        return self._collision_eigenvalues

    def get_mean_free_path(self):
        return self._mfp

    def get_frequencies_all(self):
        return self._frequencies[:np.prod(self._mesh)]

    def _run_at_grid_point(self):
        i = self._grid_point_count
        self._show_log_header(i)
        grid_point = self._grid_points[i]

        if not self._read_gamma:
            self._collision.set_grid_point(grid_point)

            if self._log_level:
                print("Number of triplets: %d" %
                      len(self._pp.get_triplets_at_q()[0]))
                print("Calculating ph-ph interaction...")

            self._set_collision_matrix_at_sigmas(i)

        if self._is_reducible_collision_matrix:
            gp = self._ir_grid_points[i]
            self._set_harmonic_properties(i, gp)
            if self._isotope is not None:
                self._gamma_iso[:, gp, :] = self._get_gamma_isotope_at_sigmas(i)
        else:
            self._set_harmonic_properties(i, i)
            if self._isotope is not None:
                self._gamma_iso[:, i, :] = self._get_gamma_isotope_at_sigmas(i)

        if self._log_level:
            self._show_log(i)

    def _allocate_values(self):
        num_band0 = len(self._pp.get_band_indices())
        num_band = self._primitive.get_number_of_atoms() * 3
        num_ir_grid_points = len(self._ir_grid_points)
        num_temp = len(self._temperatures)
        num_mesh_points = np.prod(self._mesh)

        if self._is_reducible_collision_matrix:
            num_grid_points = num_mesh_points
        else:
            num_grid_points = len(self._grid_points)

        self._kappa = np.zeros((len(self._sigmas),
                                num_temp,
                                6), dtype='double')
        self._gv = np.zeros((num_grid_points, num_band0, 3), dtype='double')
        self._gv_sum2 = np.zeros((num_grid_points, num_band0, 6),
                                 dtype='double')
        self._mfp = np.zeros((len(self._sigmas),
                              num_temp,
                              num_grid_points,
                              num_band0,
                              3), dtype='double')
        self._cv = np.zeros((num_temp, num_grid_points, num_band0),
                            dtype='double')
        if self._is_full_pp:
            self._averaged_pp_interaction = np.zeros(
                (num_grid_points, num_band0), dtype='double')
        self._gamma = np.zeros((len(self._sigmas),
                                num_temp,
                                num_grid_points,
                                num_band0), dtype='double')
        if self._isotope is not None:
            self._gamma_iso = np.zeros((len(self._sigmas),
                                        num_grid_points,
                                        num_band0), dtype='double')

        if self._is_reducible_collision_matrix:
            self._mode_kappa = np.zeros((len(self._sigmas),
                                         num_temp,
                                         num_mesh_points,
                                         num_band0,
                                         6), dtype='double')
            self._collision = CollisionMatrix(
                self._pp,
                is_reducible_collision_matrix=True)
            self._collision_matrix = np.empty(
                (len(self._sigmas),
                 num_temp,
                 num_mesh_points, num_band, num_mesh_points, num_band),
                dtype='double')
            self._collision_matrix[:] = 0
        else:
            self._mode_kappa = np.zeros((len(self._sigmas),
                                         num_temp,
                                         num_grid_points,
                                         num_band0,
                                         6), dtype='double')
            self._rot_grid_points = np.zeros(
                (len(self._ir_grid_points), len(self._point_operations)),
                dtype='intc')
            self._rot_BZ_grid_points = np.zeros(
                (len(self._ir_grid_points), len(self._point_operations)),
                dtype='intc')
            for i, ir_gp in enumerate(self._ir_grid_points):
                self._rot_grid_points[i] = get_grid_points_by_rotations(
                    self._grid_address[ir_gp],
                    self._point_operations,
                    self._mesh)
                self._rot_BZ_grid_points[i] = get_BZ_grid_points_by_rotations(
                    self._grid_address[ir_gp],
                    self._point_operations,
                    self._mesh,
                    self._pp.get_bz_map())
            self._collision = CollisionMatrix(
                self._pp,
                point_operations=self._point_operations,
                ir_grid_points=self._ir_grid_points,
                rotated_grid_points=self._rot_BZ_grid_points)
            self._collision_matrix = np.empty(
                (len(self._sigmas),
                 num_temp,
                 num_grid_points, num_band, 3,
                 num_ir_grid_points, num_band, 3),
                dtype='double')
            self._collision_matrix[:] = 0
            self._collision_eigenvalues = np.zeros(
                (len(self._sigmas),
                 num_temp,
                 num_ir_grid_points * num_band * 3),
                dtype='double')

    def _set_collision_matrix_at_sigmas(self, i):
        for j, sigma in enumerate(self._sigmas):
            if self._log_level:
                text = "Calculating collision matrix with "
                if sigma is None:
                    text += "tetrahedron method"
                else:
                    text += "sigma=%s" % sigma
                print(text)
            self._collision.set_sigma(sigma)
            self._collision.set_integration_weights()

            if self._is_full_pp and j != 0:
                pass
            else:
                self._collision.run_interaction(is_full_pp=self._is_full_pp)
            if self._is_full_pp and j == 0:
                self._averaged_pp_interaction[i] = (
                    self._pp.get_averaged_interaction())

            for k, t in enumerate(self._temperatures):
                self._collision.set_temperature(t)
                self._collision.run()
                if self._is_reducible_collision_matrix:
                    i_data = self._ir_grid_points[i]
                else:
                    i_data = i
                self._gamma[j, k, i_data] = (
                    self._collision.get_imag_self_energy())
                self._collision_matrix[j, k, i_data] = (
                    self._collision.get_collision_matrix())

        self._collision.delete_integration_weights()
        self._pp.delete_interaction_strength()

    def _set_kappa_at_sigmas(self):
        if self._log_level:
            print("Symmetrizing collision matrix...")
            sys.stdout.flush()

        if self._is_reducible_collision_matrix:
            if self._is_kappa_star:
                self._expand_collisions()
            self._combine_reducible_collisions()
            weights = np.ones(np.prod(self._mesh), dtype='intc')
            self._symmetrize_reducible_collision_matrix()
        else:
            self._combine_collisions()
            weights = self._get_weights()
            for i, w_i in enumerate(weights):
                for j, w_j in enumerate(weights):
                    self._collision_matrix[:, :, i, :, :, j, :, :] *= w_i * w_j
            self._symmetrize_collision_matrix()

        for j, sigma in enumerate(self._sigmas):
            if self._log_level:
                text = "----------- Thermal conductivity (W/m-k) "
                if sigma:
                    text += "for sigma=%s -----------" % sigma
                else:
                    text += "with tetrahedron method -----------"
                print(text)
                print(("#%6s       " + " %-10s" * 6) %
                      ("T(K)", "xx", "yy", "zz", "yz", "xz", "xy"))
                sys.stdout.flush()
            for k, t in enumerate(self._temperatures):
                if t > 0:
                    if self._is_reducible_collision_matrix:
                        self._set_inv_reducible_collision_matrix(j, k)
                    else:
                        self._set_inv_collision_matrix(j, k)
                    self._set_kappa(j, k, weights)

                if self._log_level:
                    print(("%7.1f " + " %10.3f" * 6) %
                          ((t,) + tuple(self._kappa[j, k])))
                    sys.stdout.flush()

        if self._log_level:
            print('')

    def _combine_collisions(self):
        num_band = self._primitive.get_number_of_atoms() * 3
        for j, k in list(np.ndindex((len(self._sigmas),
                                     len(self._temperatures)))):
            for i, ir_gp in enumerate(self._ir_grid_points):
                multi = ((self._rot_grid_points == ir_gp).sum() //
                         (self._rot_BZ_grid_points == ir_gp).sum())
                for r, r_BZ_gp in zip(self._rotations_cartesian,
                                      self._rot_BZ_grid_points[i]):
                    if ir_gp != r_BZ_gp:
                        continue

                    main_diagonal = self._get_main_diagonal(i, j, k)
                    main_diagonal *= multi
                    for l in range(num_band):
                        self._collision_matrix[
                            j, k, i, l, :, i, l, :] += main_diagonal[l] * r

    def _combine_reducible_collisions(self):
        num_band = self._primitive.get_number_of_atoms() * 3
        num_mesh_points = np.prod(self._mesh)

        for j, k in list(
                np.ndindex((len(self._sigmas), len(self._temperatures)))):
            for i in range(num_mesh_points):
                main_diagonal = self._get_main_diagonal(i, j, k)
                for l in range(num_band):
                    self._collision_matrix[
                        j, k, i, l, i, l] += main_diagonal[l]

    def _expand_collisions(self):
        num_mesh_points = np.prod(self._mesh)
        num_rot = len(self._point_operations)
        num_band = self._primitive.get_number_of_atoms() * 3
        rot_grid_points = np.zeros(
            (num_rot, num_mesh_points), dtype='intc')

        for i in range(num_mesh_points):
            rot_grid_points[:, i] = get_grid_points_by_rotations(
                self._grid_address[i],
                self._point_operations,
                self._mesh)

        for i, ir_gp in enumerate(self._ir_grid_points):
            colmat_irgp = self._collision_matrix[:, :, ir_gp, :, :, :].copy()
            self._collision_matrix[:, :, ir_gp, :, :, :] = 0
            gv_irgp = self._gv[ir_gp].copy()
            self._gv[ir_gp] = 0
            cv_irgp = self._cv[:, ir_gp, :].copy()
            self._cv[:, ir_gp, :] = 0
            gamma_irgp = self._gamma[:, :, ir_gp, :].copy()
            self._gamma[:, :, ir_gp, :] = 0
            multi = (rot_grid_points[:, ir_gp] == ir_gp).sum()
            if self._gamma_iso is not None:
                gamma_iso_irgp = self._gamma_iso[:, ir_gp, :].copy()
                self._gamma_iso[:, ir_gp, :] = 0
            for j, r in enumerate(self._rotations_cartesian):
                gp_r = rot_grid_points[j, ir_gp]
                self._gamma[:, :, gp_r, :] += gamma_irgp / multi
                if self._gamma_iso is not None:
                    self._gamma_iso[:, gp_r, :] += gamma_iso_irgp / multi
                for k in range(num_mesh_points):
                    gp_c = rot_grid_points[j, k]
                    self._collision_matrix[:, :, gp_r, :, gp_c, :] += (
                        colmat_irgp[:, :, :, k, :] / multi)
                self._gv[gp_r] += np.dot(gv_irgp, r.T) / multi
                self._cv[:, gp_r, :] += cv_irgp / multi

    def _get_weights(self):
        """Weights used for collision matrix and |X> and |f>

           r_gps: grid points on k-star with duplicates
                  len(r_gps) == order of crystallographic point group
                  len(unique(r_gps)) == # of arms of the k-star
           self._rot_grid_points contains r_gps for ir-grid points

        """
        weights = []
        for r_gps in self._rot_grid_points:
            weights.append(np.sqrt(len(np.unique(r_gps))) / np.sqrt(len(r_gps)))
        return weights

    def _symmetrize_collision_matrix(self):
        import phono3py._phono3py as phono3c
        phono3c.symmetrize_collision_matrix(self._collision_matrix)

        # Average matrix elements belonging to degenerate bands
        col_mat = self._collision_matrix
        for i, gp in enumerate(self._ir_grid_points):
            freqs = self._frequencies[gp]
            deg_sets = degenerate_sets(freqs)
            for dset in deg_sets:
                bi_set = []
                for j in range(len(freqs)):
                    if j in dset:
                        bi_set.append(j)
                sum_col = (col_mat[:, :, i, bi_set, :, :, :, :].sum(axis=2) /
                           len(bi_set))
                for j in bi_set:
                    col_mat[:, :, i, j, :, :, :, :] = sum_col

        for i, gp in enumerate(self._ir_grid_points):
            freqs = self._frequencies[gp]
            deg_sets = degenerate_sets(freqs)
            for dset in deg_sets:
                bi_set = []
                for j in range(len(freqs)):
                    if j in dset:
                        bi_set.append(j)
                sum_col = (col_mat[:, :, :, :, :, i, bi_set, :].sum(axis=5) /
                           len(bi_set))
                for j in bi_set:
                    col_mat[:, :, :, :, :, i, j, :] = sum_col

    def _symmetrize_reducible_collision_matrix(self):
        import phono3py._phono3py as phono3c
        phono3c.symmetrize_collision_matrix(self._collision_matrix)

        # Average matrix elements belonging to degenerate bands
        col_mat = self._collision_matrix
        for i, gp in enumerate(self._ir_grid_points):
            freqs = self._frequencies[gp]
            deg_sets = degenerate_sets(freqs)
            for dset in deg_sets:
                bi_set = []
                for j in range(len(freqs)):
                    if j in dset:
                        bi_set.append(j)
                sum_col = (col_mat[:, :, i, bi_set, :, :].sum(axis=2) /
                           len(bi_set))
                for j in bi_set:
                    col_mat[:, :, i, j, :, :] = sum_col

        for i, gp in enumerate(self._ir_grid_points):
            freqs = self._frequencies[gp]
            deg_sets = degenerate_sets(freqs)
            for dset in deg_sets:
                bi_set = []
                for j in range(len(freqs)):
                    if j in dset:
                        bi_set.append(j)
                sum_col = (col_mat[:, :, :, :, i, bi_set].sum(axis=4) /
                           len(bi_set))
                for j in bi_set:
                    col_mat[:, :, :, :, i, j] = sum_col

    def _get_X(self, i_temp, weights, gv):
        num_band = self._primitive.get_number_of_atoms() * 3
        X = gv.copy()
        if self._is_reducible_collision_matrix:
            num_mesh_points = np.prod(self._mesh)
            freqs = self._frequencies[:num_mesh_points]
        else:
            freqs = self._frequencies[self._ir_grid_points]

        t = self._temperatures[i_temp]
        sinh = np.where(freqs > self._cutoff_frequency,
                        np.sinh(freqs * THzToEv / (2 * Kb * t)),
                        -1.0)
        inv_sinh = np.where(sinh > 0, 1.0 / sinh, 0)
        freqs_sinh = freqs * THzToEv * inv_sinh / (4 * Kb * t ** 2)

        for i, f in enumerate(freqs_sinh):
            X[i] *= weights[i]
            for j in range(num_band):
                X[i, j] *= f[j]

        if t > 0:
            return X.reshape(-1, 3)
        else:
            return np.zeros_like(X.reshape(-1, 3))

    def _set_inv_collision_matrix(self,
                                  i_sigma,
                                  i_temp,
                                  method=1):
        num_ir_grid_points = len(self._ir_grid_points)
        num_band = self._primitive.get_number_of_atoms() * 3

        if method == 0: # np.eigh depends on dsyevd
            col_mat = self._collision_matrix[i_sigma, i_temp].reshape(
                num_ir_grid_points * num_band * 3,
                num_ir_grid_points * num_band * 3)
            w, col_mat[:] = np.linalg.eigh(col_mat)
            e = np.zeros_like(w)
            v = col_mat
            for l, val in enumerate(w):
                if val > self._pinv_cutoff:
                    e[l] = 1 / np.sqrt(val)
            v[:] = e * v
            v[:] = np.dot(v, v.T) # inv_col
        elif method == 1: # dsyev: safer and slower than dsyevd and
                          #        smallest memory usage
            import phono3py._phono3py as phono3c
            w = np.zeros(num_ir_grid_points * num_band * 3, dtype='double')
            phono3c.inverse_collision_matrix(self._collision_matrix,
                                             w,
                                             i_sigma,
                                             i_temp,
                                             self._pinv_cutoff,
                                             0)
        elif method == 2: # dsyevd: faster than dsyev and lagest memory usage
            import phono3py._phono3py as phono3c
            w = np.zeros(num_ir_grid_points * num_band * 3, dtype='double')
            phono3c.inverse_collision_matrix(self._collision_matrix,
                                             w,
                                             i_sigma,
                                             i_temp,
                                             self._pinv_cutoff,
                                             1)
        # elif method == 3:
        #     import phono3py._phono3py as phono3c
        #     w = np.zeros(num_ir_grid_points * num_band * 3, dtype='double')
        #     phono3c.inverse_collision_matrix_libflame(
        #         self._collision_matrix, w, i_sigma, i_temp, self._pinv_cutoff)

        self._collision_eigenvalues[i_sigma, i_temp] = w

    def _set_inv_reducible_collision_matrix(self, i_sigma, i_temp):
        t = self._temperatures[i_temp]
        num_mesh_points = np.prod(self._mesh)
        num_band = self._primitive.get_number_of_atoms() * 3
        col_mat = self._collision_matrix[i_sigma, i_temp].reshape(
            num_mesh_points * num_band, num_mesh_points * num_band)
        w, col_mat[:] = np.linalg.eigh(col_mat)
        v = col_mat
        e = np.zeros(len(w), dtype='double')
        for l, val in enumerate(w):
            if val > self._pinv_cutoff:
                e[l] = 1 / np.sqrt(val)
        v[:] = e * v
        v[:] = np.dot(v, v.T) # inv_col

    def _set_kappa(self, i_sigma, i_temp, weights):
        X = self._get_X(i_temp, weights, self._gv)
        num_band = self._primitive.get_number_of_atoms() * 3

        if self._is_reducible_collision_matrix:
            num_mesh_points = np.prod(self._mesh)
            inv_col_mat = np.kron(
                self._collision_matrix[i_sigma, i_temp].reshape(
                    num_mesh_points * num_band,
                    num_mesh_points * num_band), np.eye(3))
            Y = np.dot(inv_col_mat, X.ravel()).reshape(-1, 3)
            self._set_mean_free_path(i_sigma, i_temp, weights, Y)
            # Putting self._rotations_cartesian is to symmetrize kappa.
            # None can be put instead for watching pure information.
            self._set_mode_kappa(X,
                                 Y,
                                 num_mesh_points,
                                 self._rotations_cartesian,
                                 i_sigma,
                                 i_temp)
            self._mode_kappa[i_sigma, i_temp] /= len(self._rotations_cartesian)
            self._kappa[i_sigma, i_temp] = (
                self._mode_kappa[i_sigma, i_temp].sum(axis=0).sum(axis=0))
        else:
            num_ir_grid_points = len(self._ir_grid_points)
            inv_col_mat = self._collision_matrix[i_sigma, i_temp].reshape(
                num_ir_grid_points * num_band * 3,
                num_ir_grid_points * num_band * 3)
            Y = np.dot(inv_col_mat, X.ravel()).reshape(-1, 3)
            self._set_mean_free_path(i_sigma, i_temp, weights, Y)
            self._set_mode_kappa(X,
                                 Y,
                                 num_ir_grid_points,
                                 self._rotations_cartesian,
                                 i_sigma,
                                 i_temp)
            # self._set_mode_kappa_from_mfp(weights,
            #                               num_ir_grid_points,
            #                               self._rotations_cartesian,
            #                               i_sigma,
            #                               i_temp)

            self._kappa[i_sigma, i_temp] = (
                self._mode_kappa[i_sigma, i_temp].sum(axis=0).sum(axis=0))

    def _set_mode_kappa(self,
                        X,
                        Y,
                        num_grid_points,
                        rotations_cartesian,
                        i_sigma,
                        i_temp):
        num_band = self._primitive.get_number_of_atoms() * 3
        for i, (v_gp, f_gp) in enumerate(zip(X.reshape(num_grid_points,
                                                       num_band, 3),
                                             Y.reshape(num_grid_points,
                                                       num_band, 3))):
            for j, (v, f) in enumerate(zip(v_gp, f_gp)):
                if rotations_cartesian is None:
                    sum_k = np.outer(v, f)
                else:
                    sum_k = np.zeros((3, 3), dtype='double')
                    for r in rotations_cartesian:
                        sum_k += np.outer(np.dot(r, v), np.dot(r, f))
                sum_k = sum_k + sum_k.T
                for k, vxf in enumerate(
                        ((0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1))):
                    self._mode_kappa[i_sigma, i_temp, i, j, k] = sum_k[vxf]

        t = self._temperatures[i_temp]
        # Collision matrix is half of that defined in Chaput's paper.
        # Therefore here 2 is not necessary multiplied.
        self._mode_kappa[i_sigma, i_temp] *= (
            self._conversion_factor * Kb * t ** 2 / np.prod(self._mesh))

    def _set_mode_kappa_from_mfp(self,
                                 weights,
                                 num_grid_points,
                                 rotations_cartesian,
                                 i_sigma,
                                 i_temp):
        for i, (v_gp, mfp_gp, cv_gp) in enumerate(
                zip(self._gv, self._mfp[i_sigma, i_temp], self._cv[i_temp])):
            for j, (v, mfp, cv) in enumerate(zip(v_gp, mfp_gp, cv_gp)):
                sum_k = np.zeros((3, 3), dtype='double')
                for r in rotations_cartesian:
                    sum_k += np.outer(np.dot(r, v), np.dot(r, mfp))
                sum_k = (sum_k + sum_k.T) / 2 * cv * weights[i] ** 2 * 2 * np.pi
                for k, vxf in enumerate(
                        ((0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1))):
                    self._mode_kappa[i_sigma, i_temp, i, j, k] = sum_k[vxf]
        self._mode_kappa *= - self._conversion_factor / np.prod(self._mesh)

    def _set_mean_free_path(self, i_sigma, i_temp, weights, Y):
        if self._is_reducible_collision_matrix:
            num_grid_points = np.prod(self._mesh)
        else:
            num_grid_points = len(self._ir_grid_points)
        t = self._temperatures[i_temp]
        num_band = self._primitive.get_number_of_atoms() * 3
        # Collision matrix is half of that defined in Chaput's paper.
        # Therefore Y is divided by 2.
        for i, f_gp in enumerate((Y / 2).reshape(num_grid_points, num_band, 3)):
            for j, f in enumerate(f_gp):
                cv = self._cv[i_temp, i, j]
                if cv < 1e-10:
                    continue
                self._mfp[i_sigma, i_temp, i, j] = (
                    - 2 * t * np.sqrt(Kb / cv) / weights[i] * f / (2 * np.pi))

    def _show_log(self, i):
        q = self._qpoints[i]
        gp = self._grid_points[i]
        frequencies = self._frequencies[gp]
        gv = self._gv[i]
        if self._is_full_pp:
            ave_pp = self._averaged_pp_interaction[i]
            text = "Frequency     group velocity (x, y, z)     |gv|       Pqj"
        else:
            text = "Frequency     group velocity (x, y, z)     |gv|"

        if self._gv_delta_q is None:
            pass
        else:
            text += "  (dq=%3.1e)" % self._gv_delta_q
        print(text)
        if self._is_full_pp:
            for f, v, pp in zip(frequencies, gv, ave_pp):
                print("%8.3f   (%8.3f %8.3f %8.3f) %8.3f %11.3e" %
                      (f, v[0], v[1], v[2], np.linalg.norm(v), pp))
        else:
            for f, v in zip(frequencies, gv):
                print("%8.3f   (%8.3f %8.3f %8.3f) %8.3f" %
                      (f, v[0], v[1], v[2], np.linalg.norm(v)))

        sys.stdout.flush()

    def _py_symmetrize_collision_matrix(self):
        num_band = self._primitive.get_number_of_atoms() * 3
        num_ir_grid_points = len(self._ir_grid_points)
        for i in range(num_ir_grid_points):
            for j in range(num_band):
                for k in range(3):
                    for l in range(num_ir_grid_points):
                        for m in range(num_band):
                            for n in range(3):
                                self._py_set_symmetrized_element(
                                    i, j, k, l, m, n)

    def _py_set_symmetrized_element(self, i, j, k, l, m, n):
        sym_val = (self._collision_matrix[:, :, i, j, k, l, m, n] +
                   self._collision_matrix[:, :, l, m, n, i, j, k]) / 2
        self._collision_matrix[:, :, i, j, k, l, m, n] = sym_val
        self._collision_matrix[:, :, l, m, n, i, j, k] = sym_val

    def _py_symmetrize_collision_matrix_no_kappa_stars(self):
        num_band = self._primitive.get_number_of_atoms() * 3
        num_ir_grid_points = len(self._ir_grid_points)
        for i in range(num_ir_grid_points):
            for j in range(num_band):
                for k in range(num_ir_grid_points):
                    for l in range(num_band):
                        self._py_set_symmetrized_element_no_kappa_stars(
                            i, j, k, l)

    def _py_set_symmetrized_element_no_kappa_stars(self, i, j, k, l):
        sym_val = (self._collision_matrix[:, :, i, j, k, l] +
                   self._collision_matrix[:, :, k, l, i, j]) / 2
        self._collision_matrix[:, :, i, j, k, l] = sym_val
        self._collision_matrix[:, :, k, l, i, j] = sym_val
