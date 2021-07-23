import h5py
import matplotlib.pyplot as plt
import numpy

from functional import *


DAMP = 0.001

def read_dataset(fname, path):
    f = h5py.File(fname)
    return numpy.array(f[path])

# Raw data
time = read_dataset('water_RT_x.bin', "RT/TIME")

ux = read_dataset('water_RT_x.bin', "RT/LEN_ELEC_DIPOLE")[:,0]
uy = read_dataset('water_RT_y.bin', "RT/LEN_ELEC_DIPOLE")[:,1]
uz = read_dataset('water_RT_z.bin', "RT/LEN_ELEC_DIPOLE")[:,2]

dt = time[1] - time[0]

signals = [ux, uy, uz]

# Fourier transformed spectra
spects = []
freq = None
for s in signals:
    s -= s[0]
    s *= np.exp(-DAMP*time)
    #w, f = fourier_tx(s, dt, 0)
    w, f = pade_tx(s, dt, (0,5))
    freq = w
    spects.append(f)

total = sum([f.imag for f in spects]) / 3
total *= freq

# Plotting
plt.plot(freq*27.2114, total, c='k')
plt.xlim(0,50)
#plt.ylim(0,0.175)
plt.ylabel("Intensity", fontsize=12)
plt.xlabel("Energy (eV)", fontsize=12)
plt.tight_layout()
plt.savefig("water_fourier_thin.pdf")
plt.show()
