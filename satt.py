import logging
from ophyd.device import Device, Component as Cpt, FormattedComponent as FCpt
import numpy as np
import h5py
from pcdsdevices.inout import TwinCATInOutPositioner

logger = logging.getLogger(__name__)


class HXRFilter(TwinCATInOutPositioner):
    """
    A single attenuation blade.

    Parameters:
    -----------
    prefix : ``str``
    filter_data : ``file``
    formula : ``str``
    thickness : ``str``
    index : ``int``
    """
    _transmission = {} # TODO: this would be good to be dynamically set.

    tab_whitelist = ['inserted', 'removed', 'insert', 'remove', 'transmission']

    # TODO: Implement an ENABLED/ALLOWED signal

    def __init__(self,
                 prefix,
                 h5file,
                 formula,
                 thickness,
                 index,
                 name='hxr_filter',
                 **kwargs):
        self.formula = formula 
        self.d = self.thickness = thickness
        self.index = index # filter index (upstream to downstream)
        self.constants, self._data = self.load_data(h5file) # These physical constants should not be mutable! 
        self.Z = self.atomic_number = int(self.constants[0]) # atomic number
        self.A = self.atomic_weight = self.constants[1] # atomic weight [g]
        self.p = self.density = self.constants[2] # density [g/cm^3]
        self.table = self._T_table()
#        super().__init__(prefix, name=name, **kwargs)

    def stage(self):
        """
        Save the original position to be restored on `unstage`.
        """
        self._original_vals[self.state] = self.state.value
        return super().stage()

    def load_data(self, h5file):
        """
        Loads HDF5 physics data into tables.
        """
        self.table = np.asarray(h5file['{}_table'.format(self.formula)])
        self.constants = np.asarray(h5file['{}_constants'.format(self.formula)])
        return self.constants, self.table

    def _T_table(self):
        """
        Creates table of transmissions based on filter thickness `d`.
        """
        t_table = np.zeros([self._data.shape[0],2])
        for i in range(self._data.shape[0]):
            t_table[i] = self._data[i,0], np.exp(-self._data[i,2]*self.d*10) 
        self.T_table = t_table
        return self.T_table

    def _closest_eV(self, eV):
        """
        Return the closest photon energy from the absorption data table.
        """
        closest_eV = (min(self.T_table[:,0], key=lambda data_eV:abs(data_eV-eV)))
        i = np.argwhere(self.T_table[:,0]==closest_eV).flatten()[0]
        return closest_eV

    def get_vals(self, eV):
        """
        Return closest photon energy to eV and its transmission.
        """
        close_eV = self._closest_eV(eV)
        i = np.argwhere(self.T_table[:,0]==close_eV).flatten()[0]
        eV, T = self.T_table[i]
        return close_eV, T

    def transmission(self, eV):
        """
        Return beam transmission at photon energy closest ``eV``.
        """
        return self.get_vals(eV)[1]

    def inserted(self):
        """
        True if filter is inserted (in).
        """
        return super().inserted

    def removed(self):
        """
        True if filter is removed (out).
        """
        return super().removed


class HXRSatt(Device):
    """
    """
    absorption_data = h5py.File('absorption_data.h5', 'r')
    configs = h5py.File('configs.h5', 'r')
    
    tab_component_names = True
    tab_whitelist = []

    # some placehoders for testing and stuff
    filters = {
        '0' : Cpt(HXRFilter, 
                  ':MMS:01',
                  h5file=absorption_data,
                  formula='C',
                  thickness=10E-6,
                  index=0,
                  kind='normal'
              ),
        '1' : Cpt(HXRFilter, 
                  ':MMS:02',
                  h5file=absorption_data,
                  formula='Si',
                  thickness=10E-6,
                  index=1,
                  kind='normal'
              )}


    def __init__(self, prefix, eV=None, name='HXRSatt'):
        self.N_filters = len(self.filters)
        self.config = self._curr_config()
        self.config_table = self._load_configs()
        self.eV = None
        if eV:
            self.set_eV(eV)
        super().__init__(prefix, name=name, **kwargs)

    def blade(self, index):
        """
        Returns the filter device at `index`.
        """
        return self.filters.get(str(index))

    def insert(self, index):
        """
        Insert filter at `index`.
        """
        inserted = self.blade(index).insert()
        self._curr_config()
        return inserted
    
    def remove(self, index):
        """
        Insert filter at `index`.
        """
        removed = self.blade(index).remove()
        self._curr_config()
        return removed

    def _load_configs(self):
        self._config_table = self.configs['configurations']
        return self._config_table

    def _curr_config(self):
        """
        Return the configuration of filter states.
        """
        config = {}
        for f in self.filters:  # commented out because it can't access HXRFilter attributes..
            # if self.filters.get(f).inserted(): # TODO: What if filter is in unknown state?
            #     state = 1
            # elif self.filters.get(f).removed():
            #     state = np.nan
            #     _curr_config.update({f : state})
        return config

    def _calc_T(self, eV, config):
        """
        Calculates and returns transmission at
        photon energy `eV` given an arbitrary configuration.
        """
        T = 1.0
        for i in range(len(config)):
            T*=config.get(str(i))*self.filters.get(str(i)).get_vals(eV)[1]
        return T

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
        return self._calc_T(eV, self._curr_config)

    def eV_callback(self):
        pass

        # old code
    # def _calc_config(self, T_des, T_vals, eV=None):
    #     """
    #     """
    #     new_config = {}
    #     for f in self.filters:
    #         new_config.update({ f : 0 })

    #     best_hi = 0
    #     best_lo = 0
    #     best_config_lo = new_config
    #     best_config_hi = new_config

    #     if T_des <= 0:
    #         return best_lo, best_hi, best_config_lo, best_config_hi

    #     for f in self.filters:
    #         new_config[f] = 1
    #         new_T = self._calc_T(eV, new_config)
    #         if new_T == T_des:
    #             best_hi = best_lo = new_T
    #             best_config_hi = best_config_lo = new_config
    #             break
    #         elif best_hi < T_des or (new_T < best_hi and new_T > T_des):
    #             best_hi = new_T
    #             best_config_hi = new_config
    #         elif best_lo == 0 or best_lo > T_des or (new_T > best_lo and new_T < T_des):
    #             best_lo = new_T
    #             best_config_lo = new_config
    #         if new_T > T_des:
    #             new_config.update({ f : 0})
    #             pass
            
            
    # def _create_lookup(self, eV):
    #     """
    #     Find all possible configurations and calculate
    #     their transmissions at photon energy `eV`.
    #     """
    #     dtype=[('config',int),('T',float)]
    #     data = []
    #     configs = map(list, itertools.product([0, 1], repeat=self.N_filters))
    #     for i in range(2**self.N_filters):
    #         pair = (configs[i], self._calc_T(eV, configs[i], self.filters))
    #         data.append(pair)
    #     self.T_lookup_table = sorted(data, key=lambda x: x[1])
    #     return np.asarray(self.T_lookup_table)

    
    # def set_eV(self, eV):
    #     """
    #     Sets the working photon energy and creates 
    #     a transmission lookup table.
    #     """
    #     self.eV = eV
    #     self.T_lookup_table = self._create_lookup(self.eV)

        
    # def set_attenuation(self, T_desired, eV=None):
    #     """
    #     Find and set the configuration that has transmission closest (upper bound)
    #     to `T_desired` at photon energy `eV`. 
    #     """
    #     if self.eV:
    #         T_table = self.T_lookup_table
    #     if eV:
    #         T_table = self._create_configs(eV)
    #     new_config = None
    #     for i in range(1,len(T_table)):
    #         if T_table[i-1,1] < T_desired <= T_table[i,1]:
    #             new_config = T_table[i,0]
    #     if not new_config:
    #         print("Requested transmission not possible at this energy.")
    #     else:
    #         self._reset_blades()
    #         self.set_config(new_config)
