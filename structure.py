
# -*- coding: UTF-8 -*-
'''
Created on Jan 16 2019

Geracao da estrutura e obtencao dos dados da STARK

@author: Diego Xavier - Modelagem Numerica/FUNCEME


stark.funceme.br
Stark WEB: http://www3.funceme.br/web/storage/obs/monitor_secas/

'''

import os, subprocess, shutil, errno
from shutil import ignore_patterns
from os import path as osp
from glob2 import glob as glb2
import pandas as pd
from fnmatch import fnmatch, filter
from os.path import isdir, join
from shutil import copytree
from shutil import copyfile
import argparse

def arguments():
    """
    Function to insert parameters from external environment (example: shell)

    In this function is possible to insert the following parameters:
    Ano atual do Monitor (-ano), Mes atual do Monitor'(-mes),
    Diretorio do ultimo monitor (-src), Diretorio de saida (-outpath)
    
    Ex1: Create structure 01/2019:
         python structure.py -ano='2019' -mes='01' -src='/home/funceme/monitor/54_MAPAS_DEZ2018/QGIS_INICIAL_FINAL/Monitor_Dezembro2018_template_enviado_autores' -outpath='/home/funceme/monitor/55_MAPAS_JAN2019'
    """
    
    __description__ = "Script que gera a estrutura do projeto do Monitor de Secas"
 
    global args
    
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-ano',     help='Ano atual do Monitor - str')
    parser.add_argument('-mes',     help='Mes atual do Monitor - str')
    parser.add_argument('-src',     help='Diretorio do ultimo Monitor - str')
    parser.add_argument('-outpath', help='Diretorio de saida - str')
    
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


def include_patterns(*patterns):
    """
    Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """
    def _ignore_patterns(path, names):
        keep = set(name for pattern in patterns
                            for name in filter(names, pattern))
        ignore = set(name for name in names
                        if name not in keep and not isdir(join(path, name)))
        return ignore
    return _ignore_patterns


def fcopy(src, dst, incl_pattern=True, pattern='*.qml'):
	"""
	Function to copy all folders and its content from a directory 
	to a destination. Specific file formats can be assigned on the
	pattern argument.
	"""
	try:
		#if path already exists, remove it before copying with copytree()
		if os.path.exists(dst):
			shutil.rmtree(dst)
			if incl_pattern:
				shutil.copytree(src, dst, ignore=include_patterns(pattern))
			if not incl_pattern:
				shutil.copytree(src, dst)
		else:
			if incl_pattern:
				shutil.copytree(src, dst, ignore=include_patterns(pattern))
			if not incl_pattern:
				shutil.copytree(src, dst)
	except OSError as e:
		# If the error was caused because the source wasn't a directory
		if e.errno == errno.ENOTDIR:
			shutil.copy(source_dir_prompt, destination_dir_prompt)
		else:
			print('Directory not copied. Error: %s' % e)


# Current MS
yyyy, mm = args.ano, args.mes
# Previous MS folder
source   = args.src
# Current MS folder
outpath  = osp.join(args.outpath, 'QGIS_INICIAL_FINAL')
ckdir(outpath)


# Create dirs
ms1, ms2 = "MS_{0}{1}".format(yyyy, mm), "MS_{0}{1}".format(yyyy, str(int(mm)-1).zfill(2))
if ms2[-2:] == '00':
	ms2 = 'MS_' + str(int(yyyy)-1) + '12'

groups         = ['Base_cartografica', ms1, ms2, 'Indicadores', 'Produtos_apoio']
subgroups_ind  = ['SDSI', 'SPEI', 'SPI', 'SRI', 'Indicador_combinado']
subgroups_ap   = ['Precipitacao', 'Temperatura', 'VHI', 'ESI', 'Relevo']
subsubg_pr     = ['Acumulado', 'Anomalia', 'Climatologia', 'Estacoes', 'Quantis', 'SPI_outros']
subsubg_temp   = ['Anomalia', 'Climatologia', 'Maximas', 'Medias']

for g in groups:
	os.mkdir(osp.join(outpath, g))

for subg in subgroups_ind:
	os.mkdir(osp.join(outpath + '/' + groups[-2], subg))

for subg in subgroups_ap:
	os.mkdir(osp.join(outpath + '/' + groups[-1], subg))

for ssub in subsubg_pr:
	os.mkdir(osp.join(outpath + '/' + groups[-1] + '/' + subgroups_ap[0], ssub))	

for ssub in subsubg_temp:
	os.mkdir(osp.join(outpath + '/' + groups[-1] + '/' + subgroups_ap[1], ssub))

# Import .qml

fcopy(source, outpath, pattern='*.qml')
print 'qml imported...'

# Import Relevo

fcopy(osp.join(source, 'Produtos_apoio', 'Relevo'), osp.join(outpath, 'Produtos_apoio', 'Relevo'), incl_pattern=False)

# Import template

copyfile(osp.join(source, 'template_legenda_monitor.qpt'), osp.join(outpath, 'template_legenda_monitor.qpt'))
copyfile(osp.join(source, 'MS-leg_new.png'), osp.join(outpath, 'MS-leg_new.png'))

# Import Base cartografica

fcopy(osp.join(source, 'Base_cartografica'), osp.join(outpath, 'Base_cartografica'), incl_pattern=False)

# Download data from STARK
mm_d1 = {'01':'jan', '02':'fev', '03':'mar', '04':'abr', '05':'mai', '06': 'jun',
'07': 'jul', '08':'ago', '09':'set', '10':'out', '11':'nov', '12': 'dez'}

mm_d2 = {'01':'janeiro', '02':'fevereiro', '03':'marco', '04':'abril', '05':'maio', '06': 'junho',
'07': 'julho', '08':'agosto', '09':'setembro', '10':'outubro', '11':'novembro', '12': 'dezembro'}

date1 = pd.to_datetime('2014-06-01') 
date2 = pd.to_datetime('{0}-{1}-28'.format(yyyy, mm))
cnt   = abs(date1.to_period("M") - date2.to_period("M"))

pw = 'DDP7ViD'

# folder_loc ex.: /data/modelagem/obs/monitor_secas/54_MAPAS_DEZ2018/QGIS_INICIAL_FINAL/Monitor_Dezembro2018_template_enviado_autores/201812_Template
folder_loc = "/data/modelagem/obs/monitor_secas/{0}_MAPAS_{1}{2}/QGIS_INICIAL_FINAL/Monitor_{3}{4}_template_enviado_autores/{5}{6}_Template".format(cnt, mm_d1[mm].upper(), \
																																					yyyy, mm_d2[mm].capitalize(), \
																																					yyyy, yyyy, mm)
print folder_loc

sshpass = "sshpass -p {0} scp -r modelagem@stark.funceme.br:{1} {2}".format(pw, folder_loc, outpath+'/stark_outros')
subprocess.call(sshpass, shell=True)
print 'files downloaded'

# Move downloaded files

print 'moving files...'

	# Indicadores

folders = ['SDSI', 'SPEI', 'SPI', 'SRI']
for folder in folders:
	files  = glb2(osp.join(outpath, 'stark_outros', folder, '*'))
	for file in files:
		shutil.move(file, osp.join(outpath, 'Indicadores', folder, osp.basename(file)))
		# print("\n".join(file))

	# ESI

['ESI']
'Produtos_apoio/ESI'
pass

	# VHI	

fls  = glb2(osp.join(outpath, 'stark_outros', 'Produtos_apoio', '**'))
fls1 = [f for f in fls if 'VHI' in f or 'VHP' in f]

for file in fls1:
	if osp.isfile(file):
		shutil.move(file, osp.join(outpath, 'Produtos_apoio', 'VHI', osp.basename(file)))

	# Prec Estacoes

fls = glb2(osp.join(outpath, 'stark_outros', 'Produtos_apoio', 'PREC', '**'))

for file in fls:
	if osp.isfile(file):
		shutil.move(file, osp.join(outpath, 'Produtos_apoio', 'Precipitacao', 'Estacoes', osp.basename(file)))

	# Temp

fls = glb2(osp.join(outpath, 'stark_outros', 'Produtos_apoio', 'Temp_INMET', '**'))

for file in fls:
	if 'anom_t' in file:
		if osp.isfile(file):
			shutil.move(file, osp.join(outpath, 'Produtos_apoio', 'Temperatura', 'Anomalia', osp.basename(file)))


for file in fls:
	if 'clim.' in file:
		if osp.isfile(file):
			shutil.move(file, osp.join(outpath, 'Produtos_apoio', 'Temperatura', 'Climatologia', osp.basename(file)))


for file in fls:
	if 'temp_maxima' in file:
		if osp.isfile(file):
			shutil.move(file, osp.join(outpath, 'Produtos_apoio', 'Temperatura', 'Maximas', osp.basename(file)))


for file in fls:
	if 'temp_media' in file:
		if osp.isfile(file):
			shutil.move(file, osp.join(outpath, 'Produtos_apoio', 'Temperatura', 'Medias', osp.basename(file)))

# Remove *kriging and *wgs84 files
fls1 = glb2(osp.join(outpath, 'Indicadores', '*', '*kriging.tif'))
fls2 = glb2(osp.join(outpath, 'Indicadores', '*', '*wgs84.tif'))
fls3 = glb2(osp.join(outpath, 'Produtos_apoio', 'Precipitacao', 'Estacoes', '*kriging.tif'))
fls4 = glb2(osp.join(outpath, 'Produtos_apoio', 'Precipitacao', 'Estacoes', '*wgs84.tif'))

for f in fls1+fls2+fls3+fls4:
	os.remove(f)

# Rename MS folders
fls = sorted(glb2(osp.join(outpath, 'MS_*')))
os.rename(fls[0], osp.join(outpath, ms1))
os.rename(fls[1], osp.join(outpath, ms2))

# Rename VHI
fls = glb2(osp.join(outpath, 'Produtos_apoio', 'VHI', '*.tiff'))
for f in fls:
	os.rename(f, f.split(".", 2)[0] + '.tif')

# Remove empty folders
fls1 = glb2(osp.join(outpath, 'stark_outros', '*'))
fls2 = glb2(osp.join(outpath, 'stark_outros', 'Produtos_apoio', '*'))
for f in fls1+fls2:
	if not os.listdir(f):
		os.rmdir(f)