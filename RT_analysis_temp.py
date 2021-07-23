import numpy as np
import h5py
from numpy.fft import fft, fftfreq, ifft, rfft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import math


x_data = np.genfromtxt("calculated_dipole_x.txt", dtype=None)
y_data = np.genfromtxt("calculated_dipole_y.txt", dtype=None)
z_data = np.genfromtxt("calculated_dipole_z.txt", dtype=None)

time = x_data[:, 0]

energy_x = x_data[:, 1]
energy_y = y_data[:, 1]
energy_z = z_data[:, 1]

dipole_x = x_data[:, 2:5]
dipole_y = y_data[:, 2:5]
dipole_z = z_data[:, 2:5]

# Getting the ground state dipoles
gs_x = dipole_x[0][0]
gs_y = dipole_y[0][1]
gs_z = dipole_z[0][2]


# Subtracting off the ground state dipoles
D_t_x = np.array([ i[0] - gs_x for i in dipole_x])
D_t_y = np.array([ i[1] - gs_y for i in dipole_y])
D_t_z = np.array([ i[2] - gs_z for i in dipole_z])


# This part is to add the damping factor. I will look into 
# more efficient ways of doing this
x_t_combined = np.vstack((D_t_x, time)).T
y_t_combined = np.vstack((D_t_y, time)).T
z_t_combined = np.vstack((D_t_z, time)).T

damping_factor = 0.01
D_t_x_damped = np.array([ np.exp(-damping_factor*i[1]) * i[0] for i in x_t_combined])
D_t_y_damped = np.array([ np.exp(-damping_factor*i[1]) * i[0] for i in y_t_combined])
D_t_z_damped = np.array([ np.exp(-damping_factor*i[1]) * i[0] for i in z_t_combined])


n = D_t_x_damped.size
# convert atomic uni|t time to SI unit (fs) 
timestep = 0.05 * 2.4188843265857e-17 * 10e15
time_in_fs = np.arange(0, n*timestep, timestep)

# make sure the first element is not 0
time_in_fs[0] = timestep * 0.5

freq = [ 2 * np.pi / i for i in time_in_fs]
E_in_eV = [ 4.13567 * i for i in time_in_fs]


FT_x = np.fft.rfft(D_t_x_damped)
D_omega_x = np.fft.rfftfreq(n, d=timestep)

FT_y = np.fft.rfft(D_t_y_damped)


FT_z = np.fft.rfft(D_t_z_damped)


abs = []
for i in range(D_omega_x.size):
    signal = (4 * np.pi * D_omega_x[i])/ 3 * (FT_x[i].imag + FT_y[i].imag + FT_z[i].imag)
    abs.append(signal)
    
    
figure(figsize = (8, 6), dpi=300)
plt.plot(D_omega_x, abs)
plt.show()
#plt.xlim(0,1)