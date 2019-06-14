import requests
import numpy as np
##############################################################################

formula = 'C' # chemical formula of attenuating material
thickness = 0.1 # material thickness (um)
evMin = 10 # minimum photon eneryg
evMax = 30000 # maximum photon energy
Npts = 500 # number of data points
plotType = 'Linear' # Log, LogLin, LinLog, Linear

##############################################################################
payload = {'Material': '', # leave this string empty
           'Formula' : str(formula), # chemical formula of attenuating material
           'Density' : '-1', # -1 for tabulated value
           'Thickness' : str(thickness), # material thickness (um)
           'Min': str(evMin), # minimum photon energy
           'Max': str(evMax), # maximum photon energy
           'Npts': str(Npts), # number of data points (<1000)
           'Scan':'Energy', # Leave this as Energy
           'Plot': str(plotType), # Log, LogLin, LinLog, Linear
           'Output':'Plot'} # Leave this as Plot

r = requests.post('http://henke.lbl.gov/cgi-bin/filter.pl',data=payload)
filename = str(r.text.split('HREF="')[1].split('">data')[0]) # Parse the data file name from the HTML source
q = requests.get('http://henke.lbl.gov'+filename) 

datalines = q.text.rsplit('\n')
npdata = np.zeros([Npts+1,2])
for i in range(Npts+1):
    npdata[i] = float(datalines[i+2].split('     ')[0]), float(datalines[i+2].split('     ')[1]) # Extract values from raw text.

np.save('tables/'+'{0}_{1:E}um_{2}-{3}ev_{4}pts_{5}.npy'.format(formula,thickness,evMin,evMax,Npts,plotType), npdata)
