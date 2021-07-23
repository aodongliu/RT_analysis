import numpy as np
import h5py
from numpy.fft import fft, fftfreq, ifft
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# Locate the data stored in the HDF5 groups, and put them into arrays
with h5py.File('water_RT_x.bin', 'r') as f_x:
    base_items = list(f_x.items())
    print('Items in the base directory: \n', base_items)
    RT = f_x.get('RT')
    RT_items = list(RT.items())
    print('\n Items in RT: ', RT_items)
    energy_x = np.array(RT.get('ENERGY')) 
    dipole_x = np.array(RT.get('LEN_ELEC_DIPOLE')) 
    time =  np.array(RT.get('TIME')) 
    
# Locate the data stored in the HDF5 groups, and put them into arrays
with h5py.File('water_RT_y.bin', 'r') as f_y:
    base_items = list(f_y.items())
    print('Items in the base directory: \n', base_items)
    RT = f_y.get('RT')
    RT_items = list(RT.items())
    print('\n Items in RT: ', RT_items)
    energy_y = np.array(RT.get('ENERGY')) 
    dipole_y = np.array(RT.get('LEN_ELEC_DIPOLE')) 
    
# Locate the data stored in the HDF5 groups, and put them into arrays
with h5py.File('water_RT_z.bin', 'r') as f_z:
    base_items = list(f_z.items())
    print('Items in the base directory: \n', base_items)
    RT = f_z.get('RT')
    RT_items = list(RT.items())
    print('\n Items in RT: ', RT_items)
    energy_z = np.array(RT.get('ENERGY')) 
    dipole_z = np.array(RT.get('LEN_ELEC_DIPOLE')) 
    
# Getting the ground state dipoles
gs_x = dipole_x[0][0]
gs_y = dipole_y[0][1]
gs_z = dipole_z[0][2]

# Subtracting off the ground state dipoles
D_t_x = np.array([i[0]-gs_x for i in dipole_x])
D_t_y = np.array([i[1]-gs_y for i in dipole_y])
D_t_z = np.array([i[2]-gs_z for i in dipole_z])

# This part is to add the damping factor. I will look into 
# more efficient ways of doing this
x_t_combined = np.vstack((D_t_x, time)).T
y_t_combined = np.vstack((D_t_y, time)).T
z_t_combined = np.vstack((D_t_z, time)).T

damping_factor = 0.005
D_t_x_damped = np.array([np.exp(-damping_factor*i[1]) * i[0] for i in x_t_combined])
D_t_y_damped = np.array([ np.exp(-damping_factor*i[1]) * i[0] for i in y_t_combined])
D_t_z_damped = np.array([ np.exp(-damping_factor*i[1]) * i[0] for i in z_t_combined])

n = D_t_x_damped.size
timestep = 0.05
FT_x = np.fft.fft(D_t_x_damped)
D_omega_x = np.fft.fftfreq(n, d=timestep)

FT_y = np.fft.fft(D_t_y_damped)
D_omega_y = np.fft.fftfreq(n, d=timestep)

FT_z = np.fft.fft(D_t_z_damped)
D_omega_z = np.fft.fftfreq(n, d=timestep)

figure(figsize=(8, 6), dpi=300)
plt.plot(D_omega_x, FT_x, label = 'FT_x')
plt.plot(D_omega_x, FT_y, label = 'FT_y')
plt.plot(D_omega_x, FT_z, label = 'FT_z')
plt.legend()
#plt.xlim()

abs = []
for i in range(D_omega_x.size):
    signal = (4 * np.pi * D_omega_x[i])/ 3 * (FT_x[i].imag + FT_y[i].imag + FT_z[i].imag)
    abs.append(signal)
    
figure(figsize=(8, 6), dpi=300)
plt.plot(D_omega_x, abs)
plt.xlim(0,0.7)
