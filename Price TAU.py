# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:22:31 2023

@author: tangy
"""

import numpy as np
import pandas as pd
from scipy.stats import norm




# Create a 12x10 sheet with random values

data = np.random.rand(12, 10)
ω = norm.ppf(data, loc=0, scale=1)
Time0 = np.full((1,10),0.08)
ωnew=np.vstack([Time0,ω])

sheet = pd.DataFrame(ωnew)

# Get the dimensions of the matrix
rows, cols = ωnew.shape

# Create an empty result matrix of the same shape
result = np.zeros((12, 10))
rsn=np.vstack([Time0,result])

# Multiply each pair of rows

kappa=0.16
mu=0.06
sigma=0.018


for i in range(1, rows):
    #result[i] = ωnew[i-1] + ωnew[i]
   rsn[i] = kappa*mu*0.25+(1-mu*0.25)*rsn[i-1]+sigma*0.5*ωnew[i]



shortrate= rsn.flatten(order='F')
shortrate1= shortrate.reshape(-1, 1)


# Create a row from 0.25 to 3 with a step of 0.25
tau = np.arange(0.25, 3.25, 0.25)


kappa=0.16
mu=0.06
sigma=0.018


OUB = (1 - np.exp(-kappa * tau)) / kappa
kappa2 = kappa * kappa
sigma2 = sigma * sigma
OUB2 = np.square(OUB)

oua_rtn1 = OUB - tau
oua_rtn2 = oua_rtn1 * (mu * kappa2 - sigma2 / 2) / kappa2
oua_rtn3 = OUB2 * sigma2 / (4 * kappa)
oua_rtnp = oua_rtn2 - oua_rtn3
OUA = np.exp(oua_rtnp)

PriceTAU=np.exp(-shortrate1 * OUB)*OUA

result = np.insert(PriceTAU, 0, shortrate, axis=1)

print(result)


#calculated_data = norm.ppf(random_data)

# Create the DataFrame
#sheet = pd.DataFrame(calculated_data)


# Print the sheet


