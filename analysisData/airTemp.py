#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 19:25:51 2022

@author: massonnetf
"""

import csv 
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy import stats

matplotlib.rcParams['font.family'] = "Arial Narrow"

#Source: https://www.ecad.eu/
fileIn = "./TX_STAID011249.txt"

fileCsv = open(fileIn, mode  = "r")

csvReader = csv.reader(fileCsv)

nSkip = 20 # Nb rows in header
[next(csvReader) for _ in  range(nSkip)]
dates = list()
TMax = list()


# Read data in

for row in csvReader:
    if float(row[3]) == 0: # Quality check of data
        dates.append(datetime.datetime.strptime(row[1], "%Y%m%d"))
        TMax.append(float(row[2])/ 10) # given as T * 10
    
    
    
# Filter data
yearSeparation = int((dates[0].year + dates[-1].year) / 2)
subSetTMax_1 = [TMax[j] for j, d in enumerate(dates) if d <= \
                datetime.datetime(yearSeparation, 1, 1) and d.month == 6  ]
n_1 = len(subSetTMax_1)

subSetTMax_2 = [TMax[j] for j, d in enumerate(dates) if d > \
                datetime.datetime(yearSeparation, 1, 1) and d.month == 6  ]
n_2 = len(subSetTMax_2)   
    
# Value 2022
# Source: https://prevision-meteo.ch/climat/horaire/paris-orly/2022-06-18
#         https://www.infoclimat.fr/climatologie/globale/18-juin/orly-athis-mons/07149.html
TMax2022 = (35.9 + 36.1)  / 2
    
fig, ax = plt.subplots(1, 2, figsize = (8, 4))


xpdf = np.linspace(5.0, 40.0)
kernel_1 = stats.gaussian_kde(subSetTMax_1)
fit_1 = kernel_1(xpdf).T
kernel_2 = stats.gaussian_kde(subSetTMax_2)
fit_2 = kernel_2(xpdf).T

pdf = kernel_1(xpdf).T
fig.suptitle("Distribution des températures maximales\njournalières à Orly (France)" + \
             " en juin")
for a in ax:

    a.legend()
    a.set_xlabel("$^\circ$C")
    a.set_ylabel("Densité de probabilité")
    a.hist(subSetTMax_1, color = "#1E22AE", label = str(dates[0].year) \
                             + "-" + str(yearSeparation) + " (n = " + str(n_1) +")", alpha = 1, \
                                 bins =  np.arange(10, 40, 1), density = True)    
    a.hist(subSetTMax_2, color = "#D81F2A", label = str(yearSeparation + 1) + \
        "-" + str(dates[-1].year) + " (n = " + str(n_2) +")", alpha = 0.5, \
            bins =  np.arange(10, 40, 1), density = True)
    
    
    a.plot((TMax2022, TMax2022), (0, 10000), color = "orange", zorder = 1000, \
              label = "18 Juin 2022 (estim.)", linestyle = "--")
    a.legend(loc = "upper left")

    a.plot(xpdf, fit_1, color = "blue")
    a.plot(xpdf, fit_2, color = "red")
    
ax[0].set_title("Toutes les données")
ax[1].set_title("Zoom > 30$^\circ$ C")
ax[0].set_ylim(0.0, 0.15) 
ax[1].set_ylim(0.0, 0.03) 
ax[1].set_xlim(30.0, 40.0)
fig.tight_layout()

plt.savefig("./fig1.png", dpi = 300)
