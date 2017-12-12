"""
 The contents of this file are subject to the MIT License (MIT)
 You may not use this file except in compliance with the License. 
 The Initial Developer of this Original Code is Dr. Yong Tian at SUSTech
 Created 03/22/2017 20:28 PM
 Contact tiany@sustc.edu.cn
"""
import sys, os, math, time 
import arcpy
from arcpy import env
from arcpy.sa import *

#===========================Reference=====================
#https://en.wikipedia.org/wiki/Ordinary_least_squares#Estimation
#=========================================================

#===========================Arguments=====================
arcpy.CheckOutExtension("spatial")
# set the work directory
work_dic = ".\\"
# set the input file which contains the filename of raster
raser_list_filename = ".\\trend_raster_list.txt"
# set the number of rasters
n = 14
# set the output trend raster
trend_raster = work_dic + "trend.tif"
#=========================================================

env.overwrite = True
env.workspace = work_dic
rasters = open(raser_list_filename)
# setup index
i=1
# define division
d1 = 0
s1 = 0
for j in range(1,n+1):
    d1 += j*j
    s1 += j
seed = n*d1 - s1*s1
seed = float(seed)
s1 = float(s1)
print s1
print 'the global seed is {0}'.format(seed)

for raster in rasters:
    raster = raster.replace('\n','')
    if os.path.exists(raster):
        print i
        coef= (i*n-s1)/seed

        print 'Raster {0} is {1}:'.format(i,raster)
        print 'the coef for raster {0} is {1}'.format(i,coef)

        # Multiple raster by coefficient
        if i==1:
            outSlope=(Raster(raster)*coef)
            i+=1  # same as saying i=i+1
        else:
            print 'adding {0} to outSlope'.format(raster)
            outSlope=outSlope+(Raster(raster)*coef)
            i+=1

# Save final slope grid
print 'saving final trend raster'
outSlope.save(trend_raster)

print 'script is complete'
