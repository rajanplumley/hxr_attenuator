import requests
import numpy as np
import sys
##############################################################################
formula = sys.argv[1]
url = 'http://henke.lbl.gov/optical_constants/sf/'+formula.lower()+'.nff'
newfile = './scattering_factors/'+formula.lower()+'.npy'

print("Downloading atomic scattering factor file for {0} from {1}".format(formula, url))
q = requests.get(url)
datalines = q.text.rsplit('\n')
npdata = np.zeros([len(datalines)-2,3])
for i in range(1,len(datalines)-1):
    nums = datalines[i].split('\t')
    npdata[i-1]= float(nums[0]), float(nums[1]), float(nums[2])
print('Saving file as '+newfile)
np.save(newfile,npdata)

