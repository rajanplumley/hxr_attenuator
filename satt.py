import logging
from ophyd.device import Device, Component as Cpt, FormattedComponent as FCpt
from ophyd import EpicsSignal, EpicsSignalRO
import numpy as np
import h5py
from pcdsdevices.inout import TwinCATInOutPositioner

logger = logging.getLogger(__name__)


class HXRFilter(Device):
    """
    A single attenuation blade.

    Parameters:
    -----------
    prefix : ``str``
    filter_data : ``file``
    index : ``int``
    """
    _transmission = {} # TODO: this would be good to be dynamically set.
    # TODO: Implement an ENABLED/ALLOWED signal    

    blade = FCpt(TwinCATInOutPositioner,
                 '{prefix}:MMS:{self.index_str}', kind='normal')
    material = FCpt(EpicsSignalRO,
                    '{prefix}:FILTER:{self.index_str}:MATERIAL',
                    string=True, kind='hinted')
    thickness = FCpt(EpicsSignalRO,
                     '{prefix}:FILTER:{self.index_str}:THICKNESS',
                     kind='hinted')

    tab_whitelist = ['inserted', 'removed', 'insert', 'remove', 'transmission']
    
    def __init__(self,
                 prefix,
                 h5file=None,
                 index=None,
                 name='hxr_filter',
                 **kwargs):
        self.index_str = f'{index}'.zfill(2)
        self.index = index
        super().__init__(prefix, name=name, **kwargs)
        self.constants, self._data = self.load_data(h5file) # These physical constants should not be mutable! 
        self.Z = self.atomic_number = int(self.constants[0]) # atomic number
        self.A = self.atomic_weight = self.constants[1] # atomic weight [g]
        self.p = self.density = self.constants[2] # density [g/cm^3]
        self.d = 1
        self.table = self._T_table()
        self.d = self.thickness.get()


    def load_data(self, h5file):
        """
        Loads HDF5 physics data into tables.
        """
        table = np.asarray(h5file['{}_table'.format(self.material.get())])
        constants = np.asarray(h5file['{}_constants'.format(self.material.get())])
        return constants, table

    def _T_table(self):
        """
        Creates table of transmissions based on filter thickness `d`.
        """
        print('generating table for FILTER:{}...'.format(self.index_str))
        t_table = np.zeros([self._data.shape[0],2])
        for i in range(self._data.shape[0]):
            t_table[i] = self._data[i,0], np.exp(-self._data[i,2]*self.d*10) 
        self.T_table = t_table
        print('done generating table for FILTER:{}!'.format(self.index_str))
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
        return self.blade.inserted

    def removed(self):
        """
        True if filter is removed (out).
        """
        return self.blade.removed


class HXRSatt(Device):
    """
    """
    
    tab_component_names = True
    tab_whitelist = []


    def __init__(self, prefix, eV=None, name='HXRSatt', **kwargs):
        super().__init__(prefix, name=name, **kwargs)

    def startup(self):
        self.N_filters = len(self.filters)
        self.config = self._curr_config()
        self.config_table = self._load_configs()

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
        for f in self.filters:
            if self.filters.get(f).inserted():
                state = 1
            elif self.filters.get(f).removed():
                state = np.nan
                _curr_config.update({f : state})
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

    def attenuate(self):
        pass

class AT2L0(HXRSatt):

    absorption_data = h5py.File('absorption_data.h5', 'r')
    configs = h5py.File('configs.h5', 'r')

    f0 = FCpt(HXRFilter, '{prefix}', h5file=absorption_data, 
             index=1, kind='normal')
    f1 = FCpt(HXRFilter, '{prefix}', h5file=absorption_data,
             index=2, kind='normal')
    f2 = FCpt(HXRFilter, '{prefix}', h5file=absorption_data,
             index=3, kind='normal')
    f3 = FCpt(HXRFilter, '{prefix}', h5file=absorption_data,
             index=4, kind='normal')

    def __init__(self, prefix, name='at2l0', **kwargs):
        self.prefix = prefix
        super().__init__(prefix, name=name, **kwargs)
        self.filters = {
            str(self.f0.index) : self.f0,
            str(self.f1.index) : self.f1,
            str(self.f2.index) : self.f2,
            str(self.f3.index) : self.f3
        }
#        super().startup() # this will try to connect to motor signals


