import numpy as np
from scipy.interpolate import interp1d
import h5py

"""
Program for populating photoabsorption datasets for
X-FEL solid attenuator transmission calculations using
public data availabe from LBNL CXRO.

REFERENCES:
----------------
B.L. Henke, E.M. Gullikson, and J.C. Davis,
X-ray interactions: photoabsorption, scattering, transmission,
and reflection at E=50-30000 eV, Z=1-92,
Atomic Data and Nuclear Data Tables 54 no.2, 181-342 (July 1993).

B.D. Cullity, Elements of X-Ray Diffraction (Second Edition),
11-20, (1978).
"""

# TODO: Read these from a config file.
Si_data = {
    'formula'      : 'Si',
    'atomic_number': 14,         # Z
    'atomic_weight': 4.6637E-23, # grams
    'density'      : 2.329,      # grams/cm^3
}
C_data = {    
    'formula'      : 'C',
    'atomic_number': 6,          # Z
    'atomic_weight': 1.9926E-23, # grams
    'density'      : 3.51,       # grams/cm^3
}

# physical constants
r0 = 2.8719E-15   # [m]      classical electron radius
h = 6.626176E-34  # [j s]    plancks constant
c = 2.9979E8      # [m s^-1] Speed of light
NA = 6.022E23     # []       Avagadros number 

data_dicts = [Si_data, C_data]

def nff_to_npy(element):
    """
    Opens the .nff file containing scattering factors / energies for
    an atomic element and writes the data to a numpy array.

    Parameters:
    ---------------
    element : ``str``
       Formula of the element to open e.g. "Si", "si", "C", "Au"

    """
    element = element.lower()
    raw_data = open('CXRO/{}.nff'.format(element), 'r')
    data_lines = raw_data.readlines()
    npy_data = np.zeros([len(data_lines)-2,3])
    for i in range(1,len(data_lines)-1):
        nums = data_lines[i].split('\t')
        npy_data[i-1]= float(nums[0]), float(nums[1]), float(nums[2])
    return npy_data


def eV_linear(eV_range, res=10, dec=2):
    """
    Return a linear range of photon energies.

    Parameters:
    ---------------
    eV_range : ``tuple``
       Upper and lower bounds of photon energy range. 

    res : ``float``
       Magnitude of resolution.  Default of 10 yields 0.1 eV resolution.

    dec : ``int``
       Decimal places.
    """
    return np.around(np.linspace(eV_range[0],
                                 eV_range[1],
                                 (eV_range[1]-eV_range[0])*res+1), dec)


def fill_data_linear(element, eV_range, res=10):
    """
    Interpolates data to add more samples.

    Parameters:
    ---------------
    element : ``str``
       Formula of the element to open e.g. "Si", "si", "C", "Au"

    eV_range : ``tuple``
       Upper and lower bounds of photon energy range. 

    res : ``float``
       Magnitude of resolution.  Default of 10 yields 0.1 eV resolution.
    """
    raw_data = nff_to_npy(element)
    new_range = eV_linear(eV_range=eV_range, res=10)
    fill_func = interp1d(raw_data[:,0], raw_data[:,2])
    return fill_func(new_range)


def abs_data(material, eV_range):
    """
    Data table for photoabsorption calculations.
    """
    fs = fill_data_linear(material.get('formula'), eV_range=eV_range)
    table = np.zeros([fs.shape[0], 3])
    A = material.get('atomic_weight')
    p = material.get('density')
    eV_space = eV_linear(eV_range=eV_range) # eV
    table[:,0] = eV_space[:]
    table[:,1] = fs # scattering factor f_2
    table[:,2] = (2*r0*h*c*fs/eV_space)*p*(NA/A) # absorption constant \mu
    return table


def gen_table(data_dicts, eV_range=(1000,25000), res=10, dec=2):
    h5 = h5py.File('./absorption_data.h5','w')
    for data in data_dicts:
        element = data.get('formula')
        table = abs_data(data, eV_range)
        data_table = h5.create_dataset('{}_table'.format(element),
                                        table.shape,
                                        dtype='f')
        data_consts = h5.create_dataset('{}_constants'.format(element),
                                    (3,),
                                    dtype=float)
        data_table[:] = table[:]
        data_consts[0] = data.get('atomic_number')
        data_consts[1] = data.get('atomic_weight')
        data_consts[2] = data.get('density')
    h5.close()


if __name__ == '__main__':
    gen_table(data_dicts)
