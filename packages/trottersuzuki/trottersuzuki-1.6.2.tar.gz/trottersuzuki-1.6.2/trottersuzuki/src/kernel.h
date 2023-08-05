/**
 * Massively Parallel Trotter-Suzuki Solver
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef __KERNEL_H
#define __KERNEL_H
#include <string>
#include "trottersuzuki.h"
#ifdef _OPENMP
#include <omp.h>
#endif
#ifdef CUDA
#include <cuda_runtime.h>
#include <cublas_v2.h>
#endif

//These are for the MPI NEIGHBOURS
#define UP    0
#define DOWN  1
#define LEFT  2
#define RIGHT 3

#define BLOCK_WIDTH_CACHE 128u
#define BLOCK_HEIGHT_CACHE 128u

/** Functions defining Euclidean geometry
 */
void block_kernel_vertical(size_t start_offset, size_t stride, size_t width, size_t height, double a, double b, double * p_real, double * p_imag);
void block_kernel_vertical_imaginary(size_t start_offset, size_t stride, size_t width, size_t height, double a, double b, double * p_real, double * p_imag);
void block_kernel_horizontal(size_t start_offset, size_t stride, size_t width, size_t height, double a, double b, double * p_real, double * p_imag);
void block_kernel_horizontal_imaginary(size_t start_offset, size_t stride, size_t width, size_t height, double a, double b, double * p_real, double * p_imag);
void block_kernel_radial_kinetic(size_t start_offset, size_t stride, size_t width, size_t height, double offset_x, double _kin_radial, double * p_real, double * p_imag);
void block_kernel_radial_kinetic_imaginary(size_t start_offset, size_t stride, size_t width, size_t height, double offset_x, double _kin_radial, double * p_real, double * p_imag);
void block_kernel_potential(bool two_wavefunctions, size_t stride, size_t width, size_t height, double coupling_a, double coupling_b, double coupling_aa, size_t tile_width, const double *external_pot_real, const double *external_pot_imag, const double *pb_real, const double *pb_imag, double * p_real, double * p_imag);
void block_kernel_potential_imaginary(bool two_wavefunctions, size_t stride, size_t width, size_t height, double coupling_a, double coupling_b, double coupling_aa, size_t tile_width, const double *external_pot_real, const double *external_pot_imag, const double *pb_real, const double *pb_imag, double * p_real, double * p_imag);
void block_kernel_rotation(size_t stride, size_t width, size_t height, int offset_x, int offset_y, double alpha_x, double alpha_y, double * p_real, double * p_imag);
void block_kernel_rotation_imaginary(size_t stride, size_t width, size_t height, int offset_x, int offset_y, double alpha_x, double alpha_y, double * p_real, double * p_imag);
void rabi_coupling_real(size_t stride, size_t width, size_t height, double cc, double cs_r, double cs_i, double *p_real, double *p_imag, double *pb_real, double *pb_imag);
void rabi_coupling_imaginary(size_t stride, size_t width, size_t height, double cc, double cs_r, double cs_i, double *p_real, double *p_imag, double *pb_real, double *pb_imag);
/**
 * \brief This class defines the CPU kernel.
 *
 * This kernel provides real time and imaginary time evolution of a quantum state, using CPUs.
 * It implements a solver for a single or two wave functions, whose evolution is governed by nonlinear Schrodinger equation (Gross Pitaevskii equation). The Hamiltonian of the physical system includes:
 *  - time-dependent external potential
 *  - rotating system of reference
 *  - intra species interaction
 *  - extra species interaction
 *  - Rabi coupling
 */

class CPUBlock: public ITrotterKernel {
public:
    CPUBlock(Lattice *grid, State *state, Hamiltonian *hamiltonian,
             double *_external_pot_real, double *_external_pot_imag,
             double delta_t, double _norm, bool _imag_time);    ///< Instantiate the kernel for single wave functions state evolution.


    CPUBlock(Lattice *grid, State *state1, State *state2,
             Hamiltonian2Component *hamiltonian,
             double **_external_pot_real, double **_external_pot_imag,
             double delta_t, double *_norm, bool _imag_time);    ///< Instantiate the kernel for two wave functions state evolution.

    ~CPUBlock();
    void run_kernel_on_halo();          ///< Evolve blocks of wave function at the edge of the tile. This comprises the halos.
    void run_kernel();              ///< Evolve the remaining blocks in the inner part of the tile.
    void wait_for_completion();         ///< Synchronize all the processes at the end of halos communication. Perform normalization for imaginary time evolution in the case of single wave-function evolution.
    void get_sample(size_t dest_stride, size_t x, size_t y, size_t width, size_t height, double * dest_real, double * dest_imag, double * dest_real2 = 0, double * dest_imag2 = 0) const; ///< Copy the wave function from the two buffers pointed by p_real and p_imag, without halos, to dest_real and dest_imag.
    void normalization();    ///< Normalize the state when performing an imaginary time evolution (only two wave-function evolution).
    void rabi_coupling(double var, double delta_t);    ///< Evolution corresponding to the Rabi coupling term of the Hamiltonian (only two wave-function evolution).
    double calculate_squared_norm(bool global = true) const;  ///< Calculate squared norm of the state.
    void update_potential(double *_external_pot_real, double *_external_pot_imag, int which);    ///< Update memory pointed by external_potential_real and external_potential_imag (only non static external potential).
    void cpy_first_positive_to_first_negative();    ///< Copy first points with positive radial coordinates to first points with negative coordinates.
    bool runs_in_place() const {
        return false;
    }
    /// Get kernel name.
    string get_name() const {
        return "CPU";
    };

    void start_halo_exchange();         ///< Start vertical halos exchange.
    void finish_halo_exchange();        ///< Start horizontal halos exchange.



private:
    double *p_real[2][2];       ///< Array of two pointers that point to two buffers used to store the real part of the wave function at i-th time step and (i+1)-th time step.
    double *p_imag[2][2];       ///< Array of two pointers that point to two buffers used to store the imaginary part of the wave function at i-th time step and (i+1)-th time step.
    double *external_pot_real[2];   ///< Points to the matrix representation (real entries) of the operator given by the exponential of external potential.
    double *external_pot_imag[2];   ///< Points to the matrix representation (immaginary entries) of the operator given by the exponential of external potential.
    double *aH;            ///< Diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *bH;            ///< Off diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *aV;            ///< Diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *bV;            ///< Off diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *kin_radial;   ///< Kinetic costant for the radial coordinate.
    double delta_x;         ///< Physical length between two neighbour along x axis dots of the lattice.
    double delta_y;         ///< Physical length between two neighbour along y axis dots of the lattice.
    double *norm;         ///< Squared norm of the single wave functions.
    double tot_norm;    ///< Squared norm of the total state.
    double *coupling_const;     ///< Coupling constant of the density self-interacting term.
    double *LeeHuangYang_coupling;     ///< Coupling constant of the Lee-Huang-Yang terms.
    int sense;            ///< Takes values 0 or 1 and tells which of the two buffers pointed by p_real and p_imag is used to calculate the next time step.
    int state_index;    ///< Takes values 0 or 1 and tells which wave function is pointed by p_real and p_imag, and is being evolved.
    size_t halo_x;          ///< Thickness of the vertical halos (number of lattice's dots).
    size_t halo_y;          ///< Thickness of the horizontal halos (number of lattice's dots).
    size_t tile_width;        ///< Width of the tile (number of lattice's dots).
    size_t tile_height;       ///< Height of the tile (number of lattice's dots).
    bool imag_time;         ///< True: imaginary time evolution; False: real time evolution.
    static const size_t block_width = BLOCK_WIDTH_CACHE;      ///< Width of the lattice block which is cached (number of lattice's dots).
    size_t block_height;     ///< Height of the lattice block which is cached (number of lattice's dots).
    bool two_wavefunctions;    ///< Flag parameter to distinguish whether the kernel is evolving a two-wave-function or a single-wave-function
    int angular_momentum[2];   ///< Angular momentum when cylindrical coordinates are used.

    double alpha_x;         ///< Real coupling constant associated to the X*P_y operator, part of the angular momentum.
    double alpha_y;         ///< Real coupling constant associated to the Y*P_x operator, part of the angular momentum.
    double rot_coord_x;        ///< X axis coordinate of the center of rotation.
    double rot_coord_y;        ///< Y axis coordinate of the center of rotation.
    int start_x;          ///< X axis coordinate of the first dot of the processed tile.
    int start_y;          ///< Y axis coordinate of the first dot of the processed tile.
    int end_x;            ///< X axis coordinate of the last dot of the processed tile.
    int end_y;            ///< Y axis coordinate of the last dot of the processed tile.
    int inner_start_x;        ///< X axis coordinate of the first dot of the processed tile, which is not in the halo.
    int inner_start_y;        ///< Y axis coordinate of the first dot of the processed tile, which is not in the halo.
    int inner_end_x;        ///< X axis coordinate of the last dot of the processed tile, which is not in the halo.
    int inner_end_y;        ///< Y axis coordinate of the last dot of the processed tile, which is not in the halo.
    int *periods;         ///< Two dimensional array which takes entries 0 or 1. 1: periodic boundary condition along the corresponding axis; 0: closed boundary condition along the corresponding axis.
    string coordinate_system;  ///< Type of the coordinate system used.
#ifdef HAVE_MPI
    MPI_Comm cartcomm;        ///< Ensemble of processes communicating the halos and evolving the tiles.
    int neighbors[4];       ///< Array that stores the processes' rank neighbour of the current process.
    MPI_Request req[8];       ///< Variable to manage MPI communication.
    MPI_Status statuses[8];     ///< Variable to manage MPI communication.
    MPI_Datatype horizontalBorder;  ///< Datatype for the horizontal halos.
    MPI_Datatype verticalBorder;  ///< Datatype for the vertical halos.
#endif
};

#ifdef CUDA

//#define DISABLE_FMA

// NOTE: NEVER USE ODD NUMBERS FOR BLOCK DIMENSIONS
// thread block / shared memory block width
#define BLOCK_X 32
// shared memory block height
#define BLOCK_Y  (sizeof(double) == 8 ? 32 : 96)

#define STRIDE_Y 16

/**
 * \brief This class defines the GPU kernel.
 *
 * This kernel provides real time and imaginary time evolution exploiting GPUs.
 * It implements a solver for a single wave function, whose evolution is governed by linear Schrodinger equation. The Hamiltonian of the physical system includes:
 *  - static external potential
 */

class CC2Kernel: public ITrotterKernel {
public:
    CC2Kernel(Lattice *grid, State *state, Hamiltonian *hamiltonian,
              double *_external_pot_real, double *_external_pot_imag,
              double delta_t, double _norm, bool _imag_time);    ///< Instantiate the kernel for single wave functions state evolution.
    CC2Kernel(Lattice *grid, State *state1, State *state2,
              Hamiltonian2Component *hamiltonian,
              double **_external_pot_real, double **_external_pot_imag,
              double delta_t, double *_norm, bool _imag_time);   ///< Instantiate the kernel for two wave functions state evolution.

    ~CC2Kernel();
    void run_kernel_on_halo();				    ///< Evolve blocks of wave function at the edge of the tile. This comprises the halos.
    void run_kernel();							///< Evolve the remaining blocks in the inner part of the tile.
    void wait_for_completion();					///< Sincronize all the processes at the end of halos communication. Perform normalization for imaginary time evolution.
    void get_sample(size_t dest_stride, size_t x, size_t y, size_t width, size_t height, double * dest_real, double * dest_imag, double * dest_real2 = 0, double * dest_imag2 = 0) const; ///< Copy the wave function from the two buffers pointed by pdev_real and pdev_imag, without halos, to dest_real and dest_imag.
    void normalization();    ///<Normalize the state when performing an imaginary time evolution (only two wave-function evolution).
    void rabi_coupling(double var, double delta_t);    ///< Evolution corresponding to the Rabi coupling term of the Hamiltonian (only two wave-function evolution).
    double calculate_squared_norm(bool global = true) const;  ///< Calculate squared norm of the state.
    void update_potential(double *_external_pot_real, double *_external_pot_imag, int which);    ///< Update memory pointed by external_potential_real and external_potential_imag (only non static external potential).
    void cpy_first_positive_to_first_negative();    ///< Copy first points with positive radial coordinates to first points with negative coordinates.
    bool runs_in_place() const {
        return false;
    }
    /// Get kernel name.
    string get_name() const {
        return "CUDA";
    }

    void start_halo_exchange();		///< Empty function.
    void finish_halo_exchange();	///< Exchange halos.

private:
    dim3 numBlocks;						///< Number of blocks exploited in the lattice.
    dim3 threadsPerBlock;				///< Number of lattice dots in a block.
    cudaStream_t stream1;				///< Stream of sequential instructions performing evolution and communication on the halos blocks.
    cudaStream_t stream2;				///< Stream of sequential instructions performing evolution on the inner blocks.
    cublasHandle_t handle;

    bool imag_time;						///< True: imaginary time evolution; False: real time evolution.
    double *p_real[2];						///< Point to  the real part of the wave function (stored in Host).
    double *p_imag[2];						///< Point to  the imaginary part of the wave function (stored in Host).
    double *external_pot_real[2];			///< Points to the matrix representation (real entries) of the operator given by the exponential of external potential (stored in Host).
    double *external_pot_imag[2];			///< Points to the matrix representation (imaginary entries) of the operator given by the exponential of external potential (stored in Host).
    double *dev_external_pot_real[2];		///< Points to the matrix representation (real entries) of the operator given by the exponential of external potential (stored in Device).
    double *dev_external_pot_imag[2];		///< Points to the matrix representation (imaginary entries) of the operator given by the exponential of external potential (stored in Device).
    double *pdev_real[2][2];				///< Array of two pointers that point to two buffers used to store the real part of the wave function at i-th time step and (i+1)-th time step (stored in Device).
    double *pdev_imag[2][2];				///< Array of two pointers that point to two buffers used to store the imaginary part of the wave function at i-th time step and (i+1)-th time step (stored in Device).
    double *aH;							///< Diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *bH;							///< Off diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *aV;							///< Diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double *bV;							///< Off diagonal value of the matrix representation of the operator given by the exponential of kinetic operator.
    double delta_x;						///< Physical length between two neighbour along x axis dots of the lattice.
    double delta_y;						///< Physical length between two neighbour along y axis dots of the lattice.
    double *norm;						///< Squared norm of the wave function.
    double tot_norm;    ///< Squared norm of the total state.
    double *coupling_const;     ///< Coupling constant of the density self-interacting term.
    double alpha_x;         ///< Real coupling constant associated to the X*P_y operator, part of the angular momentum.
    double alpha_y;         ///< Real coupling constant associated to the Y*P_x operator, part of the angular momentum.
    int state_index;    ///< Takes values 0 or 1 and tells which wave function is pointed by p_real and p_imag, and is being evolved.
    int sense;							///< Takes values 0 or 1 and tells which of the two buffers pointed by p_real and p_imag is used to calculate the next time step.
    bool two_wavefunctions;    ///< Flag parameter to distinguish whether the kernel is evolving a two-wave-function or a single-wave-function
    size_t halo_x;						///< Thickness of the vertical halos (number of lattice's dots).
    size_t halo_y;						///< Thickness of the horizontal halos (number of lattice's dots).
    size_t tile_width;					///< Width of the tile (number of lattice's dots).
    size_t tile_height;					///< Height of the tile (number of lattice's dots).
    int *periods;						///< Two dimensional array which takes entries 0 or 1. 1: periodic boundary condition along the corresponding axis; 0: closed boundary condition along the corresponding axis.

#ifdef HAVE_MPI
    MPI_Comm cartcomm;
#endif
    int neighbors[4];					///< Array that stores the processes' rank neighbour of the current process.
    int start_x;						///< X axis coordinate of the first dot of the processed tile.
    int start_y;						///< Y axis coordinate of the first dot of the processed tile.
    int end_x;							///< X axis coordinate of the last dot of the processed tile.
    int end_y;							///< Y axis coordinate of the last dot of the processed tile.
    int inner_start_x;					///< X axis coordinate of the first dot of the processed tile, which is not in the halo.
    int inner_start_y;					///< Y axis coordinate of the first dot of the processed tile, which is not in the halo.
    int inner_end_x;					///< X axis coordinate of the last dot of the processed tile, which is not in the halo.
    int inner_end_y;					///< Y axis coordinate of the last dot of the processed tile, which is not in the halo.
    double *left_real_receive;			///< Point to the buffer used to receive the real left vertical halo from the corresponding neighbour.
    double *left_real_send;				///< Point to the buffer used to send the real left vertical halo to the corresponding neighbour.
    double *right_real_receive;			///< Point to the buffer used to receive the real right vertical halo from the corresponding neighbour.
    double *right_real_send;			///< Point to the buffer used to send the real right vertical halo to the corresponding neighbour.
    double *left_imag_receive;			///< Point to the buffer used to receive the imaginary left vertical halo from the corresponding neighbour.
    double *left_imag_send;				///< Point to the buffer used to send the imaginary left vertical halo to the corresponding neighbour.
    double *right_imag_receive;			///< Point to the buffer used to receive the imaginary right vertical halo from the corresponding neighbour.
    double *right_imag_send;			///< Point to the buffer used to send the imaginary right vertical halo to the corresponding neighbour.
    double *bottom_real_receive;		///< Point to the buffer used to receive the real bottom horizontal halo from the corresponding neighbour.
    double *bottom_real_send;			///< Point to the buffer used to send the real bottom horizontal halo to the corresponding neighbour.
    double *top_real_receive;			///< Point to the buffer used to receive the real top horizontal halo from the corresponding neighbour.
    double *top_real_send;				///< Point to the buffer used to send the real top horizontal halo to the corresponding neighbour.
    double *bottom_imag_receive;		///< Point to the buffer used to receive the imaginary bottom horizontal halo from the corresponding neighbour.
    double *bottom_imag_send;			///< Point to the buffer used to send the imaginary bottom horizontal halo to the corresponding neighbour.
    double *top_imag_receive;			///< Point to the buffer used to receive the real top horizontal halo from the corresponding neighbour.
    double *top_imag_send;				///< Point to the buffer used to send the real bottom horizontal halo to the corresponding neighbour.

};

extern "C" {
    __global__ void cc2kernel(size_t tile_width, size_t tile_height, size_t offset_x, size_t offset_y, size_t halo_x, size_t halo_y,
                              double aH, double bH, double aV, double bV, double coupling_a, double alpha_x, double alpha_y, const double * __restrict__ external_pot_real, const double * __restrict__ external_pot_imag,
                              const double * __restrict__ p_real, const double * __restrict__ p_imag,
                              double * __restrict__ p2_real, double * __restrict__ p2_imag,
                              int inner, int horizontal, int vertical);
    __global__ void imag_cc2kernel(size_t tile_width, size_t tile_height, size_t offset_x, size_t offset_y, size_t halo_x, size_t halo_y,
                                   double aH, double bH, double aV, double bV, double coupling_a, double alpha_x, double alpha_y, const double * __restrict__ external_pot_real, const double * __restrict__ external_pot_imag,
                                   const double * __restrict__ p_real, const double * __restrict__ p_imag,
                                   double * __restrict__ p2_real, double * __restrict__ p2_imag,
                                   int inner, int horizontal, int vertical);
    __global__ void gpu_rabi_coupling_real(size_t width, size_t height,
                                           double cc, double cs_r, double cs_i,
                                           double *p_real, double *p_imag,
                                           double *pb_real, double *pb_imag);
    __global__ void gpu_rabi_coupling_imag(size_t width, size_t height,
                                           double cc, double cs_r, double cs_i,
                                           double *p_real, double *p_imag,
                                           double *pb_real, double *pb_imag);
}

#endif // CUDA

#endif // __KERNEL_H
