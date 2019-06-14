import h5py
import numpy as np

Si_data = {
    'formula'      : 'Si',
    'atomic_number': 14,
    'atomic_weight': 4.6637E-23, # grams
    'density'      : 2.329,      # grams/cm^3
    'f_scatter'    : './scattering_factors/si.npy', # atomic scattering factor data
}
C_data = {    
    'formula'      : 'C',
    'atomic_number': 6,
    'atomic_weight': 1.9926E-23,  # grams
    'density'      : 3.51,       # grams/cm^3
    'f_scatter'    : './scattering_factors/c.npy', # atomic scattering factor data
}
data_dicts = [Si_data, C_data]

# physical constants
r0 = 2.8719E-15   # [m]      classical electron radius
h = 6.626176E-34  # [j s]    plancks constant
c = 2.9979E8      # [m s^-1] Speed of light
NA = 6.022E23     # []       Avagadros number 

def abs_data(material):
    """
    Data table for photoabsorption calculations.
    """
    fs = np.load(material.get('f_scatter'))
    table = np.zeros([fs.shape[0], 3])
    A = material.get('atomic_weight')
    p = material.get('density')
    table[:,0] = fs[:,0]
    table[:,1] = fs[:,2]
    table[:,2] = (2*r0*h*c*fs[:,2]/fs[:,0])*p*(NA/A)
    return table

fout = h5py.File('filter_data.h5', 'w')
for material in data_dicts:
    table = abs_data(material)
    h5const = fout.create_dataset('{}_constants'.format(material.get('formula')),(3,),dtype=float)
    h5table = fout.create_dataset('{}_scatter_table'.format(material.get('formula')),(table.shape),dtype=float)
    h5table[:] = table[:]
    h5const[0] = material.get('atomic_number')
    h5const[1] = material.get('atomic_weight')
    h5const[2] = material.get('density')
fout.close()
