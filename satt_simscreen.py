from pcdsdevices.inout import TwinCATInOutPositioner
from ophyd.device import Device
from ophyd.device import Component as Cpt
from pcdsdevices.doc_stubs import basic_positioner_init
import typhon
import sys
from qtpy.QtWidgets import QApplication
import typhos


# class AT2L0(Device):
#     """
#     This is a quick-and-dirty Ophyd device for
#     controlling AT2L0 motion and generating
#     a PyDM control screen.
#     """
    
#     blade_01 = Cpt(TwinCATInOutPositioner, ':MMS:01', kind='hinted')
#     blade_02 = Cpt(TwinCATInOutPositioner, ':MMS:02', kind='hinted')
#     blade_03 = Cpt(TwinCATInOutPositioner, ':MMS:03', kind='hinted')
#     blade_04 = Cpt(TwinCATInOutPositioner, ':MMS:04', kind='hinted')
#     blade_05 = Cpt(TwinCATInOutPositioner, ':MMS:05', kind='hinted')
#     blade_06 = Cpt(TwinCATInOutPositioner, ':MMS:06', kind='hinted')
#     blade_07 = Cpt(TwinCATInOutPositioner, ':MMS:07', kind='hinted')
#     blade_08 = Cpt(TwinCATInOutPositioner, ':MMS:08', kind='hinted')
#     blade_09 = Cpt(TwinCATInOutPositioner, ':MMS:09', kind='hinted')
#     blade_10 = Cpt(TwinCATInOutPositioner, ':MMS:10', kind='hinted')
#     blade_11 = Cpt(TwinCATInOutPositioner, ':MMS:11', kind='hinted')
#     blade_12 = Cpt(TwinCATInOutPositioner, ':MMS:12', kind='hinted')
#     blade_13 = Cpt(TwinCATInOutPositioner, ':MMS:13', kind='hinted')
#     blade_14 = Cpt(TwinCATInOutPositioner, ':MMS:14', kind='hinted')
#     blade_15 = Cpt(TwinCATInOutPositioner, ':MMS:15', kind='hinted')
#     blade_16 = Cpt(TwinCATInOutPositioner, ':MMS:16', kind='hinted')
#     blade_17 = Cpt(TwinCATInOutPositioner, ':MMS:17', kind='hinted')
#     blade_18 = Cpt(TwinCATInOutPositioner, ':MMS:18', kind='hinted')
    
#     def __init__(self, prefix, name='AT2L0_SIM', **kwargs):
#         super().__init__(prefix, name=name, **kwargs)


import satt
print(satt.__file__)
att = satt.AT2L0('AT2L0:SIM')
app = QApplication.instance() or QApplication(sys.argv)
suite = typhos.TyphosSuite.from_device(att)
suite.show()
app.exec_()
