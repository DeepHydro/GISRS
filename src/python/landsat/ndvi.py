import sys, os, math, time 
import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")

#Metadata exists in one of two standard formats (finds the correct name for each field)
def acquireMetadata(metadata, band):
    
    band = str(band)
    metadatalist = []
    
    if ("RADIANCE_MAXIMUM_BAND_" + band) in metadata.keys(): 
        BANDFILE = "FILE_NAME_BAND_" + band
        LMAX = "RADIANCE_MAXIMUM_BAND_" + band
        LMIN = "RADIANCE_MINIMUM_BAND_" + band
        QCALMAX = "QUANTIZE_CAL_MAX_BAND_" + band
        QCALMIN = "QUANTIZE_CAL_MIN_BAND_" + band
        DATE = "DATE_ACQUIRED"
        metadatalist = [BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, DATE]

    elif ("LMAX_BAND" + band) in metadata.keys():
        BANDFILE = "BAND" + band + "_FILE_NAME"
        LMAX = "LMAX_BAND" + band
        LMIN = "LMIN_BAND" + band
        QCALMAX = "QCALMAX_BAND" + band
        QCALMIN = "QCALMIN_BAND" + band
        DATE ="ACQUISITION_DATE"
        metadatalist = [BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, DATE]

    else:
        arcpy.AddError('There was a problem reading the metadata for this file. Please make sure the _MTL.txt is in Level 1 data format')
        
    return metadatalist

#Calculate the radiance from metadata on band.
def calcRadiance (LMAX, LMIN, QCALMAX, QCALMIN, QCAL, band):
    
    LMAX = float(LMAX)
    LMIN = float(LMIN)
    QCALMAX = float(QCALMAX)
    QCALMIN = float(QCALMIN)
    gain = (LMAX - LMIN)/(QCALMAX-QCALMIN)
    inraster = Raster(QCAL)
    outname = 'RadianceB'+str(band)+'.tif'

    arcpy.AddMessage('Band'+str(band))
    arcpy.AddMessage('LMAX ='+str(LMAX))
    arcpy.AddMessage('LMIN ='+str(LMIN))
    arcpy.AddMessage('QCALMAX ='+str(QCALMAX))
    arcpy.AddMessage('QCALMIN ='+str(QCALMIN))
    arcpy.AddMessage('gain ='+str(gain))
    
    outraster = (gain * (inraster-QCALMIN)) + LMIN
    #outraster.save(outname)
    
    return outraster

def calcReflectance(solarDist, ESUN, solarElevation, radiance, scaleFactor):
    
    #Value for solar zenith is 90 degrees minus solar elevation (angle from horizon to the center of the sun)
    # See Landsat7_Handbook 11.3.2 Radiance to Reflectance
    solarZenith = ((90.0 - (float(solarElevation)))*math.pi)/180 #Converted from degrees to radians
    solarDist = float(solarDist)
    ESUN = float(ESUN)
    outname = 'ReflectanceB'+str(band)+'.tif'
    
    arcpy.AddMessage('Band'+str(band))
    arcpy.AddMessage('solarDist ='+str(solarDist))
    arcpy.AddMessage('solarDistSquared ='+str(math.pow(solarDist, 2)))
    arcpy.AddMessage('ESUN ='+str(ESUN))
    arcpy.AddMessage('solarZenith ='+str(solarZenith))

    outraster = (math.pi * radiance * math.pow(solarDist, 2)) / (ESUN * math.cos(solarZenith)) * scaleFactor
    
    return outraster

#Calculate the solar distance based on julian day    
def calcSolarDist (jday):

    #Values taken from d.csv file which is a formatted version of the d.xls file
    #associated with the Landsat7 handbook, representing the distance of the sun
    #for each julian day (1-366).
    #this line keeps the relative path were this script is executing
    filepath = os.path.join(os.path.dirname(sys.argv[0]), 'd.csv')
    
    f = open(filepath, "r")
    lines = f.readlines()[2:]

    distances = []
    for x in range(len(lines)):
        distances.append(float(lines[x].strip().split(',')[1]))
    f.close()

    jday = int(jday)
    dist = distances[jday - 1]

    return dist 

def calcJDay (date):
    
    #Seperate date aspects into list (check for consistnecy in formatting of all
    #Landsat7 metatdata) YYYY-MM-DD
    dt = date.rsplit("-")

    #Cast each part of the date as a in integer in the 9 int tuple mktime
    t = time.mktime((int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0, 0, 0, 0))

    #As part of the time package the 7th int in mktime is calulated as Julian Day
    #from the completion of other essential parts of the tuple
    jday = time.gmtime(t)[7]

    return jday

def getESUN(bandNum, SIType):
    SIType = SIType
    ESUN = {}

    #from NASA's Landsat7_Handbook Table 11.3
    #ETM+ Solar Spectral Irradiances (generated using the combined Chance-Kurucz Solar Spectrum within MODTRAN 5)
    if SIType == 'ETM+ ChKur':
        ESUN = {'b1':1970,'b2':1842,'b3':1547,'b4':1044,'b5':225.7,'b7':82.06,'b8':1369}

    #from NASA's Landsat7_Handbook Table 9.1
    #from the LPS ACCA algorith to correct for cloud cover
    if SIType == 'LPS ACAA Algorithm':
        ESUN = {'b1':1969,'b2':1840,'b3':1551,'b4':1044,'b5':225.7,'b7':82.06,'b8':1368}

    #from Revised Landsat-5 TM Radiometric Calibration Procedures and Postcalibration, Table-2
    #Gyanesh Chander and Brian Markham. Nov 2003. 
    #Landsat 5 ChKur
    if SIType == 'Landsat 5 ChKur':
        ESUN = {'b1':1957,'b2':1826,'b3':1554,'b4':1036,'b5':215,'b7':80.67}
    
    #from Revised Landsat-5 TM Radiometric Calibration Procedures and Postcalibration, Table-2
    #Gyanesh Chander and Brian Markham. Nov 2003.
    #Landsat 4 ChKur
    if SIType == 'Landsat 4 ChKur':
       ESUN = {'b1':1957,'b2':1825,'b3':1557,'b4':1033,'b5':214.9,'b7':80.72} 

    bandNum = str(bandNum)
    
    return ESUN[bandNum]

def readMetadata(metadataFile):

    f = metadataFile
    
    #Create an empty dictionary with which to populate all the metadata fields.
    metadata = {}

    #Each item in the txt document is seperated by a space and each key is
    #equated with '='. This loop strips and seperates then fills the dictonary.

    for line in f:
        if not line.strip() == "END":
            val = line.strip().split('=')
            metadata [val[0].strip()] = val[1].strip().strip('"')      
        else:
            break

    return metadata

#Takes the unicode parameter input from Arc and turns it into a nice python list
def cleanList(bandList):
    
    bandList = list(bandList)
    
    for x in range(len(bandList)):
        bandList[x] = str(bandList[x])
        
    while ';' in bandList:
        bandList.remove(';')
        
    return bandList

#////////////////////////////////////MAIN LOOP///////////////////////////////////////
# TM5
work_dic = 'F:\\Data\\HRB\\RS\\Landsat\\Landsat5\\TM\\132_32\\LT51320322011318IKR01\\'
metadataPath = work_dic + 'LT51320322011318IKR01_MTL.txt'
out_dic = 'F:\\Data\\HRB\\RS\\Landsat\\Landsat5\\TM\\132_32\\LT51320322011318IKR01\\'
SIType = 'Landsat 5 ChKur'


keepRad = 'false'
keepRef = 'true'
scaleFactor = 1.0
min_ndvi = 0.15

env.workspace = work_dic
arcpy.env.overwriteOutput = True
ref_file_exit = 'false'

arcpy.AddMessage(scaleFactor)
if SIType =='Landsat 4 ChKur' :
    bandList = cleanList(['5','7'])
else:
    bandList = cleanList(['3','4'])

metadataFile = open(metadataPath)
metadata = readMetadata(metadataFile)
metadataFile.close()

successful = []
failed = []

if SIType =='Landsat 4 ChKur' :
# from http://landsat.gsfc.nasa.gov/the-multispectral-scanner-system/
# band 5 and 7 of MSS are equivalent to 3 and 4 of TM
   ref_file_exit = os.path.exists(work_dic + "ReflectanceB5.tif")
   ref_file_exit = os.path.exists(work_dic + "ReflectanceB7.tif")
else:
   ref_file_exit = os.path.exists(work_dic + "ReflectanceB3.tif")
   ref_file_exit = os.path.exists(work_dic + "ReflectanceB4.tif")      

if ref_file_exit:
    metlist = acquireMetadata(metadata, '5')
    print 'Reflectance files existed'
else:
    print 'Calculating reflectances' 
    for band in bandList:   
        bandstr = str(band)
        print bandstr
        metlist = acquireMetadata(metadata, band)
        BANDFILE = metlist[0]
        LMAX = metlist[1]
        LMIN = metlist[2]
        QCALMAX = metlist[3]
        QCALMIN = metlist[4]
        DATE = metlist[5]
        ESUNVAL = "b" + band
        #try:
        radianceRaster = calcRadiance(metadata[LMAX], metadata[LMIN], metadata[QCALMAX], metadata[QCALMIN], metadata[BANDFILE], band)
        reflectanceRaster = calcReflectance(calcSolarDist(calcJDay(metadata[DATE])), getESUN(ESUNVAL, SIType), metadata['SUN_ELEVATION'], radianceRaster, scaleFactor)
        outname = 'ReflectanceB'+ bandstr
        reflectanceRaster.save(outname)
        successful.append(BANDFILE)

DATE = metlist[5]
day = metadata[DATE]

if SIType =='Landsat 4 ChKur' :
    nir = Raster('ReflectanceB7.tif')
    red = Raster('ReflectanceB5.tif')
else:
    nir = Raster('ReflectanceB4.tif')
    red = Raster('ReflectanceB3.tif')

ndvi_out_ras = out_dic + "ndvi_" + day + ".tif"

print 'Calculating NDVI' 
raw_ndvi = (nir-red)/(nir+red)
ndvi = Con((raw_ndvi < min_ndvi) | (raw_ndvi > 1.0), 0, raw_ndvi)
arcpy.gp.SetNull_sa(ndvi, ndvi, ndvi_out_ras, "value = 0")
print 'NDVI file saved'

if keepRef != 'true':
    arcpy.Delete_management(nir)
    arcpy.Delete_management(red)
    print 'Reflectance files deleted'           

