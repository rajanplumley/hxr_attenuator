import logging
from ophyd import FormattedComponent as FCpt
import numpy as np
from .inout import InOutRecordPositioner

logger = logging.getLogger(__name__)


class HXRFilter(InOutRecordPositioner):
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
                 h5file=None,
                 formula=None,
                 thickness=None,
                 index=None,
                 name='HXRFilter',
                 **kwargs):
        self.formula = formula
        self.d = self.thickness = thickness
        self.index = index # filter index (upstream to downstream)
        self.constants, self._table = self.load_data(h5file)
        self.Z = int(self.constants[0]) # atomic number
        self.A = self.constants[1] # atomic weight [g]
        self.p = self.constants[2] # density [g/cm^3]
        self.table = self._T_table()
        super().__init__(prefix, name=name, **kwargs)
        

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

        
    def plot_T(self, xmin=0, xmax=8000):
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

    @property
    def inserted(self):
        """
        True if filter is inserted (in).
        """
        return super().inserted()


    @property
    def removed(self):
        """
        True if filter is removed (out).
        """
        return super().removed()

class HXRSatt(Devce, BaseInterface):
    """
    """
    absorption_data = h5py.File('absorption_data.h5', 'r')
    configs = h5py.File('configs.h5', 'r')

    # some placehoders for testing and stuff
    Si1 = Cpt(':MMS:01',
              h5file=absorption_data,
              formula='Si',
              thickness=0.5,
              index=0
        )
    Si2 = Cpt(':MMS:02',
              h5file=absorption_data,
              formula='Si',
              thickness=0.5,
              index=1
        )
    Si3 = Cpt(':MMS:03',
              h5file=absorption_data,
              formula='Si',
              thickness=0.5,
              index=2
        )    
    filters = {
        Si1.index : Si1,
        Si2.index : Si2,
        Si3.index : Si3
        }

    def __init__(self, prefix, eV=None, name='HXRSatt'):
        self.filters = filters
        self.N_filters = len(filters)
        self.config = self._config() # TODO: this should be a dict now keyed by index similar to `filters`.
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
        self._config()
        return inserted


    def remove(self, index):
        """
        Insert filter at `index`.
        """
        removed = self.blade(index).remove()
        self._config()
        return removed


    def _config(self):
        """
        Return the configuration of filter states.
        """
        config = {}
        for f in filters: 
            if filters.get(f).inserted(): # TODO: What if filter is in unknown state?
                state = 1
            elif:
                filters.get(f).removed():
                state = 0
            _config.update({f : state}}
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
        return self._calc_T(eV, self._config)


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
