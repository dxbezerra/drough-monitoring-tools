    # -*- coding: UTF-8 -*-
'''
Created on Dec 21 2018

Georreferenciamento das figuras CPTEC/INMET/NOAA

@author: Diego Xavier - Modelagem Numerica/FUNCEME


'''
# Import modules
import subprocess, time, os, shutil
from os import path as osp
from glob import glob as glb
import argparse

def arguments():
    """
    Function to insert parameters from external environment (example: shell)

    In this function is possible to insert the following parameters:
    Diretorio do monitor atual estruturado (-src)
    
    Ex1: Georeferenciamento das figuras baixadas:
         python figs_georef.py -src=-src=/home/funceme/monitor/55_MAPAS_JAN2019/QGIS_INICIAL_FINAL
    """

    __description__ = "Script de georreferenciamento das figuras do CPTEC, INMET e NOAA"
 
    global args
    
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-src', help='Diretorio estruturado do monitor atual')
    
    args = parser.parse_args()

    return args

arguments()

def ckdir(path):
    """
    Check if a path exist.
    Return: True (path ok) of False (path missing).
    """
    if osp.exists(path): 
        return True
    elif not osp.exists(path):
        os.mkdir(path)

source = args.src

# Glob files and set outpath
fls     = sorted(glb(osp.join(source, 'FIGS') + '/*'))
outpath = osp.join(source, 'FIGS', 'georef')
ckdir(outpath)

# fls = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/*"))
# outpath = "/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/georef"

# GCPs points
    # Prec_Acum_Inmet.points
gcp1 = "-gcp 427.478 407.278 -48.1994 -15.4995 -gcp 538.503 206.552 -41.323 -2.92061 -gcp 83.4304 142.64 -69.8442 1.08723 -gcp 279.444 640.548 -57.6431 -30.1899 -gcp 269.588 277.345 -58.1386 -7.35115 -gcp 563.485 451.601 -39.666 -18.3387 -gcp 606.444 292.564 -36.9907 -8.3032 -gcp 423.541 242.383 -48.7508 -5.35211"
    # Prec_Acum_Cptec_Anom_Inmet.points
gcp2 = "-gcp 379.35 167.341 -41.3217 -2.91736 -gcp 422.483 241.427 -36.9907 -8.3019 -gcp 395.325 382.559 -39.6621 -18.34 -gcp 215.753 549.401 -57.6392 -30.1834 -gcp 309.408 350.608 -48.2787 -16.0516 -gcp 306.413 198.543 -48.7547 -5.3469 -gcp 210.511 228.397 -58.1386 -7.35115 -gcp 53.5536 226.5 -73.7915 -7.11704 -gcp 90.3468 110.479 -69.8442 1.08528 -gcp 276.409 63.5518 -51.5133 4.43566"
    # Prec_Clim_Cptec.points
gcp3 = "-gcp 340.611 147.481 -41.3268 -2.92032 -gcp 381.419 206.558 -36.9761 -8.29867 -gcp 355.024 318.091 -39.6672 -18.3454 -gcp 186.467 450.279 -57.6388 -30.1851 -gcp 181.356 196.041 -58.135 -7.35225 -gcp 272.778 171.405 -48.7536 -5.34885 -gcp 31.6118 193.36 -73.7962 -7.11437 -gcp 69.5296 102.483 -69.8442 1.08789 -gcp 244.601 67.3513 -51.4753 4.4238 -gcp 298.524 230.649 -45.952 -10.2579 -gcp 316.414 271.291 -43.7924 -14.3391"
    # Prec_Clim_Inmet_61-90.points
gcp4 = "-gcp 1595.72 594.134 -41.3281 -2.92078 -gcp 1785.26 830.431 -36.997 -8.30099 -gcp 1666.66 1274.2 -39.669 -18.3478 -gcp 876.521 1799.49 -57.6416 -30.187 -gcp 1291.47 1149.49 -48.2007 -15.5011 -gcp 1390.97 920.337 -45.9473 -10.2575 -gcp 1267.46 700.994 -48.7526 -5.34652 -gcp 1201.79 899.812 -50.2264 -9.84118 -gcp 853.498 788.624 -58.1378 -7.35179 -gcp 166.38 779.701 -73.8017 -7.11205 -gcp 339.141 416.51 -69.8442 1.08742 -gcp 1144.23 269.27 -51.5357 4.43821 -gcp 1591.84 849.84 -41.3532 -8.7066"
    # Prec_Clim_Inmet_81-10.points
gcp5 = "-gcp 1074.5 290.154 -41.3232 -2.92173 -gcp 1213.33 462.883 -36.9899 -8.30102 -gcp 1126.13 787.457 -39.6652 -18.3415 -gcp 547.552 1170.32 -57.6363 -30.1859 -gcp 850.299 695.583 -48.2007 -15.5001 -gcp 922.812 525.478 -45.9485 -10.2573 -gcp 829.941 368.806 -48.7497 -5.35675 -gcp 1075.71 475.213 -41.3567 -8.70805 -gcp 23.071 425.682 -73.8001 -7.11266 -gcp 150.046 138.886 -69.847 1.7186 -gcp 741.688 52.7315 -51.5213 4.4338 -gcp 528.559 432.293 -58.141 -7.35077"
    # SPI_Quantis_Inmet.points
gcp6 = "-gcp 459.932 224.928 -37.252 -4.82972 -gcp 263.868 519.863 -57.6424 -30.1863 -gcp 107.269 252.06 -73.8029 -7.1118 -gcp 362.372 349.619 -47.4154 -15.4985 -gcp 321.858 118.604 -51.5518 4.42487 -gcp 258.777 254.894 -58.1391 -7.35101 -gcp 349.252 231.488 -48.7544 -5.35189 -gcp 436.526 381.527 -39.6695 -18.3496 -gcp 427.657 254.657 -40.5493 -7.39169 -gcp 462.503 267.2 -37.0004 -8.29811"
    # Soil_Moist.points
gcp7 = "-gcp 414.537 364.537 -57.6476 -30.1893 -gcp 337.454 133.148 -69.8446 1.09393 -gcp 454.537 109.491 -51.5222 4.43542 -gcp 331.435 211.389 -70.5601 -9.43418 -gcp 506.759 158.333 -43.6461 -2.23827 -gcp 534.676 235.556 -38.5651 -12.9206 -gcp 559.583 196.991 -34.8389 -7.54414"

# Georef
for f in fls:
    bname = osp.basename(f)
    split = osp.splitext(bname)[0]

    if "Prec_Acum_30d" in f or "Prec_Acum_90d" in f:
        print(bname, 1)

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp1, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 1 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)

    if "Prec_Acum_Cptec" in f or "Prec_Anom" in f:
        print(bname, 2)

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp2, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 1 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)

    if "Prec_Clim_Cptec" in f and "61-90" in f:
        print(bname, 3)             

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp3, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 1 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)

    if "Clim_Inmet" in f and "61-90" in f:
        print(bname, 4)             

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp4, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 1 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)

    if "Prec_Clim_Inmet" in f and "81-10" in f:
        print(bname, 5)             

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp5, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 1 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)

    if "SPI" in f or "Prec_Quantis" in f:
        print(bname, 6)

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp6, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 2 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)

    if "Soil_Moist" in f:
        print(bname, 7)

        translate_cmd = "gdal_translate -q -of GTiff {0} {1} {2}".format(gcp7, f, "/tmp/"+bname)
        translate     = subprocess.call(translate_cmd, shell=True)
        warp_cmd      = "gdalwarp -q -overwrite -r near -order 1 -co COMPRESS=NONE  {0} {1}".format("/tmp/"+bname, outpath+"/"+split+".tif")
        warp          = subprocess.call(warp_cmd, shell=True)


# Copy to structure
print 'moving files...'

path    = osp.join(source, 'FIGS', 'georef', '*')
fls     = sorted(glb(path))
outpath = osp.join(source, 'Produtos_apoio', 'Precipitacao')

for f in fls:
    
    if 'Prec_Acum' in f:
        shutil.copy(f, osp.join(outpath, 'Acumulado', osp.basename(f)))

    if 'Prec_Clim' in f:
        shutil.copy(f, osp.join(outpath, 'Climatologia', osp.basename(f)))

    if 'Prec_Anom' in f:
        shutil.copy(f, osp.join(outpath, 'Anomalia', osp.basename(f)))

    if 'Prec_Quantis' in f:
        shutil.copy(f, osp.join(outpath, 'Quantis', osp.basename(f)))

    if 'SPI_' in f:
        shutil.copy(f, osp.join(outpath, 'SPI_outros', osp.basename(f)))