# -*- coding: utf-8 -*-
"""
Created on Nov 19 2018

Indicadores de Curto e Longo Prazo

@author: Diego Xavier/Modelagem Numerica - FUNCEME

http://www3.funceme.br/web/storage/obs/monitor_secas/52_MAPAS_OUT2018/QGIS_INICIAL_FINAL/Monitor_Outubro2018_template_enviado_autores/201810_Template/SPEI/

"""

# Import modules
import numpy as np
import os, subprocess
from os import path as osp
from glob import glob as glb
from os.path import basename as bn
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import argparse

def arguments():
    """
    Function to insert parameters from external environment (example: shell)

    In this function is possible to insert the following parameters:
    Ano atual do Monitor (-ano), Mes atual do Monitor'(-mes),
    Diretorio do monitor atual estruturado - gerado pelo structure.py (-src)
    
    Ex1: Create blend 01/2019:
         python blend.py -ano='2019' -mes='01' -src='/home/funceme/monitor/55_MAPAS_JAN2019/QGIS_INICIAL_FINAL'
    """
    
    __description__ = "Script que gera os Indicadores Combinados de Curto e Longo prazo"
 
    global args
    
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-ano', help='Ano atual do Monitor - str')
    parser.add_argument('-mes', help='Mes atual do Monitor - str')
    parser.add_argument('-src', help='Diretorio estruturado - str')
    
    args = parser.parse_args()

    return args

arguments()

def ckdir(path):
    """
    Check if a path exist.
    Return: True (path ok) of False (path missing).
    """
    if os.path.exists(path): 
        return True
    elif not os.path.exists(path):
        os.mkdir(path)

yyyy, mm  = args.ano, args.mes
source    = args.src
f_spi     = sorted(glb(osp.join(source, 'Indicadores', 'SPI') + '/*.tif'))
f_spei    = sorted(glb(osp.join(source, 'Indicadores', 'SPEI') + '/*.tif'))

# yyyy, mm = '2018', '11'

# SPI SPEI glob files
# f_spi  = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/QGIS_INICIAL_FINAL/Monitor_Dezembro2018_template_enviado_autores/Indicadores/SPI/*.tif"))
# f_spei = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/QGIS_INICIAL_FINAL/Monitor_Dezembro2018_template_enviado_autores/Indicadores/SPEI/*.tif"))

# Blend combinations
curto = [i for i in f_spi if '03.tif' in i or '04.tif' in i] + \
        [i for i in f_spei if '03.tif' in i or '04.tif' in i]
print 'Curto'
print("\n".join(curto))

print ' '

longo = [i for i in f_spi if '12.tif' in i or '18.tif' in i or '24.tif' in i] + \
        [i for i in f_spei if '12.tif' in i or '18.tif' in i or '24.tif' in i]
print 'Longo'
print("\n".join(longo))

# curto  = [f_spi[1], f_spi[2], f_spei[0], f_spei[1]]
# longo  = [f_spi[4], f_spi[5], f_spi[6], f_spei[3], f_spei[4], f_spei[5]]
loop   = [curto, longo]

# Destination path
outpath = osp.join(source, 'Indicadores', 'Indicador_combinado')

# Create 3D array
for i, l in enumerate(loop):

    blend_arr = np.full((len(l), 300, 300), np.nan)
    for j, f in enumerate(l):
        # Open the dataset
        ds1 = gdal.Open(f, GA_ReadOnly)
        band1 = ds1.GetRasterBand(1)
        # Read the data into numpy arrays
        data1 = BandReadAsArray(band1)
        geoTransform = ds1.GetGeoTransform()
        print(bn(f), geoTransform[1], geoTransform[5])
        print(geoTransform)
        print(data1.shape)
        blend_arr[j, ...] = data1

    # Retrieve min
    indic  = np.min(blend_arr, axis=0)
    
    # Write outfile
    driver = gdal.GetDriverByName("GTiff")
    
    if i == 0: # curto
        outFile = "Blend_MIN_{0}{1}_SPI03e04_SPEI03e04.tif".format(yyyy, mm)
    if i == 1: # longo
        outFile = "Blend_MIN_{0}{1}_SPI12-18-24_SPEI12-18-24.tif".format(yyyy, mm)
    
    dsOut = driver.Create(osp.join(outpath, outFile), ds1.RasterXSize, ds1.RasterYSize, 1, GDT_Float32)
    CopyDatasetInfo(ds1,dsOut)
    bandOut=dsOut.GetRasterBand(1)
    
    print 'Creating {0}'.format(outFile)
    BandWriteArray(bandOut, indic)
    
    # Close datasets
    band1   = None
    ds1     = None
    bandOut = None
    dsOut   = None
