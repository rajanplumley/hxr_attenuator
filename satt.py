import numpy as np
import matplotlib as plt
import itertools

class satt:
    """
    Solid attenuator system.  A sequence of x-ray filters for reduction of XFEL pulse intensity.
    Each filter, or 'blade', can occupy two states: '1' for in, or '0' for out.
    
    Filter objects are accessible via the `blade()` method.
    """ 
    def __init__(self, filters, eV = None):
        self.filters = filters
        self.N_filters = len(filters)
        self.config = self._config()
        self.eV = None
        if eV:
            self.set_eV(eV)
        
    def blade(self, index):
        """
        Returns the filter object at `index`.
        """
        return self.filters[index]
    
    def _config(self):
        """
        Get the current configuration of filter blade states.
        """
        self.config = [ blade.state for blade in self.filters ]
        return self.config
    
    def set_config(self, config):
        """
        Moves filters to match arrangement given in `config`.
        """
        for blade in range(len(config)):
            self.filters[blade].state = config[blade]
        self._config()
    
    def _reset_blades(self):
        """
        Sets all filter blades to their default `in` position.
        """
        self.set_config(np.ones_like(self.config))

    def all_in(self):
        """
        Move all filter blades in.
        """
        self._reset_blades()
    
    def all_out(self):
        """
        Move all filter blades out.
        """
        self.set_config(np.zeros_like(self.config))
    
    def insert(self, index):
        """
        Insert a filter at `index`.
        """
        self.blade(index).state = 1
        self._config()

    def retract(self, index):
        """
        Retract a filter at `index`.
        """
        self.blade(index).state = 0
        self._config()

    def T(self, eV=None):
        """
        Calculates and returns transmission at 
        photon energy `eV` through current filter configuration.
        """
        if not eV and not self.eV:
            print("Photon energy not set.  Transmission undefined")
            return np.nan
        else:
            if not eV:
                eV = self.eV
        T = 1.0
        for f in self.filters:
            if f.is_in():
                T*=f.get_vals(eV)[1]
        return T

    def _calc_T(self, eV, config, filters):
        """
        Calculates and returns transmission at
        photon energy `eV` given an arbitrary configuration.
        """
        T = 1.0
        for i in range(len(config)):
            if config[i] == 1:
                T*=filters[i].get_vals(eV)[1]
        return T
         
    def _create_lookup(self, eV):
        """
        Find all possible configurations and calculate
        their transmissions at photon energy `eV`.
        """
        dtype=[('config',int),('T',float)]
        data = []
        configs = map(list, itertools.product([0, 1], repeat=self.N_filters))
        for i in range(2**self.N_filters):
            pair = (configs[i], self._calc_T(eV, configs[i], self.filters))
            data.append(pair)
        self.T_lookup_table = sorted(data, key=lambda x: x[1])
        return np.asarray(self.T_lookup_table)
    
    def set_eV(self, eV):
        """
        Sets the working photon energy and creates 
        a transmission lookup table.
        """
        self.eV = eV
        self.T_lookup_table = self._create_lookup(self.eV)
        
        
    def set_attenuation(self, T_desired, eV=None):
        """
        Find and set the configuration that has transmission closest (upper bound)
        to `T_desired` at photon energy `eV`. 
        """
        if self.eV:
            T_table = self.T_lookup_table
        if eV:
            T_table = self._create_configs(eV)
        new_config = None
        for i in range(1,len(T_table)):
            if T_table[i-1,1] < T_desired <= T_table[i,1]:
                new_config = T_table[i,0]
        if not new_config:
            print("Requested transmission not possible at this energy.")
        else:
            self._reset_blades()
            self.set_config(new_config)

class filter:
    def __init__(self, formula, d, index, h5file):
        self.formula = formula # chemical formula
        self.d = d # filter thickness
        self.index = index 
        self.constants, self._table = self.load_data(h5file)
        self.Z = int(self.constants[0]) # atomic number
        self.A = self.constants[1] # atomic weight [g]
        self.p = self.constants[2] # density [g/cm^3]
        self.table = self._T_table()
        self.state = 1
        
    def load_data(self, h5file):
        """
        Loads HDF5 physics data into tables.
        """
        self.table = np.asarray(h5file['{}_scatter_table'.format(self.formula)])
        self.constants = np.asarray(h5file['{}_constants'.format(self.formula)])
        return self.constants, self.table
    
    def _T_table(self):
        """
        Creates table of transmissions based on filter thickness `d`.
        """
        t_table = np.zeros([self._table.shape[0],2])
        for i in range(self._table.shape[0]):
            t_table[i] = self._table[i,0], np.exp(-self._table[i,2]*self.d*10) 
        self.T_table = t_table
        return self.T_table
        
    def plot_T(self,xmin=0,xmax=8000):
        """
        Plot this filter's transmission vs photon energy.
        """
        plt.plot(self.T_table[:,0],self.T_table[:,1], c='black', linewidth=0.7)
        plt.ylabel("Transmission")
        plt.xlabel("Photon Energy (eV)")
        plt.xlim(xmin,xmax)
        plt.title("{0}(Z = {1}): {2}um thickness".format(self.formula, self.Z, self.d*1E6))
        
    def get_vals(self, eV):
        """
        Return closest photon energy to eV and its transmission
        """
        T  = np.nan
        closest_eV = (min(self.T_table[:,0], key=lambda data_eV:abs(data_eV-eV)))
        i = np.argwhere(self.T_table[:,0]==closest_eV).flatten()[0]
        eV, T = self.T_table[i]
        return closest_eV, T
    
    def is_in(self):
        """
        Filter state as a boolean.
        """
        if int(self.state) == 1:
            return True
        else:
            return False
