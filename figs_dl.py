# -*- coding: UTF-8 -*-
'''
Created on Dec 21 2018

Download figuras CPTEC/INMET/NOAA

@author: Diego Xavier - Modelagem Numerica/FUNCEME


'''
# Import modules
import subprocess, os
from os import path as osp
from glob import glob as glb
import argparse

def arguments():
    """
    Function to insert parameters from external environment (example: shell)

    In this function is possible to insert the following parameters:
    Ano desejado (-ano), Mes desejado(-mes),
    Mes final (-mes_final), Diretorio do monitor atual estruturado (-src)
    
    Ex1: Download das figuras para Jan 2019:
         python figs_dl.py -ano=2019 -mes=01 -src='/home/funceme/alo'
    Ex2: Download das figuras para todo o ano de 2018:
    	 python figs_dl.py -ano=2018 -mes=01 -mes_final=12 -src=-src=/home/funceme/monitor/55_MAPAS_JAN2019/QGIS_INICIAL_FINAL
    """
    
    __description__ = "Script de download das figuras do CPTEC, INMET e NOAA"
 
    global args
    
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-ano',       help='Ano requerido das figuras')
    parser.add_argument('-mes',       nargs='+', help='Mes requerido das figuras')
    parser.add_argument('-mes_final', nargs='+', help='Caso deseje mais de um mes acrescente o mes final')
    parser.add_argument('-src',       help='Diretorio do monitor atual estruturado')
    
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


# Set year, months and outpath
yyyy    = args.ano

if type(args.mes_final) == type(None):
	mms = args.mes
else:
	mms = range(int(args.mes[0]), int(args.mes_final[0])+1)

source  = args.src

outpath = osp.join(source, 'FIGS')
ckdir(outpath)

# yyyy    = '2018'
# mms     = ['12', '11']
# outpath = '/home/funceme/monitor/54_sMAPAS_DEZ2018/FIGS'

# Dictionaries
mm_d1 = {'01':'jan', '02':'fev', '03':'mar', '04':'abr', '05':'mai', '06': 'jun',
'07': 'jul', '08':'ago', '09':'set', '10':'out', '11':'nov', '12': 'dez'}

mm_d2 = {'01':'janeiro', '02':'fevereiro', '03':'marco', '04':'abril', '05':'maio', '06': 'junho',
'07': 'julho', '08':'agosto', '09':'setembro', '10':'outubro', '11':'novembro', '12': 'dezembro'}

# print(mms)
# print(type(mms))
# print(mms[0])
# print(type(mms[0]))
# print(''.join(mms[0]))
# print(type(''.join(mms[0])))
# exit()

for i in range(len(mms)):
	
	mm = ''.join(str(mms[i])).zfill(2)
	print(yyyy, mm)

	# Urls
		# Prec Acum 30d/90d INMET
	urls = ['http://www.inmet.gov.br/mapas_chuva/{0}/{1}/Prec-Acum-30d_{2}{3}23.png'.format(yyyy, mm, yyyy, mm),
	'http://www.inmet.gov.br/mapas_chuva/{0}/{1}/Prec-Acum-90d_{2}{3}23.png'.format(yyyy, mm, yyyy, mm),
		# Prec Acum mensal CPTEC
	'http://img0.cptec.inpe.br/~rclima/historicos/mensal/brasil/{0}/brchuvat{1}{2}.gif'.format(mm_d1[mm], mm, yyyy[2:]),



		# Prec Clim 61-90 trimestral CPTEC
	'http://img0.cptec.inpe.br/~rclima/climatologias/sazonal/brasil/prectri{0}.gif'.format(int(mm)),
		# Prec Clim 61-90 mensal CPTEC
	'http://img0.cptec.inpe.br/~rclima/climatologias/mensal/brasil/precip{0}.gif'.format(mm),

		# Prec Clim 81-10 mensal INMET
	'http://www.inmet.gov.br/webcdp/climatologia/normais2/imagens/normais/mapas/1981-2010/precipitacao/precipitacao_acumulada_mensal/precipitacao_acumulada_mensal_{0}.png'.format(mm_d2[mm]),
		# Prec Clim 61-90 mensal INMET
	'http://www.inmet.gov.br/webcdp/climatologia/normais2/imagens/normais/mapas/1961-1990/precipitacao/precipitacao_acumulada_mensal_anual/precit_mensal_{0}.jpg'.format(mm_d2[mm]),



		# Prec Anom mensal CPTEC
	"http://img0.cptec.inpe.br/~rclima/historicos/mensal/brasil/{0}/abrchuvat{1}{2}.gif".format(mm_d1[mm], mm, yyyy[2:]),



		# Prec Quantis mensal INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_quantis/mapas/{0}{1}_quantis1Oacres.png'.format(yyyy, mm),
		# Prec Quantis trimestral INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_quantis/mapas/{0}{1}_quantis3Oacres.png'.format(yyyy, mm),
		# Prec Quantis semestral INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_quantis/mapas/{0}{1}_quantis6Oacres.png'.format(yyyy, mm),



		# SPI 1 INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_spi/mapas/{0}{1}_spi1Oacres.png'.format(yyyy, mm),
		# SPI 3 INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_spi/mapas/{0}{1}_spi3Oacres.png'.format(yyyy, mm),
		# SPI 6 INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_spi/mapas/{0}{1}_spi6Oacres.png'.format(yyyy, mm),
		# SPI 12 INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_spi/mapas/{0}{1}_spi12Oacres.png'.format(yyyy, mm),
		# SPI 24 INMET
	'http://www.inmet.gov.br/webcdp/climatologia/chuva_spi/mapas/{0}{1}_spi24Oacres.png'.format(yyyy, mm),



		# Soil Moisture mensal NOAA
	'http://www.cpc.noaa.gov/soilmst/glb_lb/rank_w.fusa.{0}{1}.gif'.format(yyyy, mm)]

	# Filenames
		# File structure
	prdcts = ['Prec_Acum', 'Prec_Clim', 'Prec_Anom', 'Prec_Quantis', 'SPI', 'Soil_Moist']
	src    = ['Cptec', 'Inmet', 'NOAA']
	prd    = ['mensal', 'trimestre', 'semestre']
	clim   = ['61-90', '81-10']
	spi    = ['SPI_01', 'SPI_03', 'SPI_06', 'SPI_12', 'SPI_24']

			# Prec Acum
	fnames = ['{0}_30d_{1}_{2}'.format(prdcts[0], src[1], (yyyy+mm)),
	'{0}_90d_{1}_{2}'.format(prdcts[0], src[1], (yyyy+mm)),
	'{0}_{1}_{2}'.format(prdcts[0], src[0], (yyyy+mm)),

			# Prec Clim
	'{0}_{1}_{2}_{3}_{4}'.format(prdcts[1], src[0], (mm+'-'+mm_d1[mm]), clim[0], prd[1]),
	'{0}_{1}_{2}_{3}'.format(prdcts[1], src[0], (mm+'-'+mm_d1[mm]), clim[0]),
	'{0}_{1}_{2}_{3}'.format(prdcts[1], src[1], (mm+'-'+mm_d1[mm]), clim[1]),
	'{0}_{1}_{2}_{3}'.format(prdcts[1], src[1], (mm+'-'+mm_d1[mm]), clim[0]),

			# Prec Anom
	'{0}_{1}_{2}'.format(prdcts[2], src[0], (yyyy+mm)),

			# Prec Quantis
	'{0}_{1}_{2}_{3}'.format(prdcts[3], src[1], (yyyy+mm), prd[0]),
	'{0}_{1}_{2}_{3}'.format(prdcts[3], src[1], (yyyy+mm), prd[1]),
	'{0}_{1}_{2}_{3}'.format(prdcts[3], src[1], (yyyy+mm), prd[2]),

			# SPI Inmet
	'{0}_{1}_{2}'.format(spi[0], src[1], (yyyy+mm)),
	'{0}_{1}_{2}'.format(spi[1], src[1], (yyyy+mm)),
	'{0}_{1}_{2}'.format(spi[2], src[1], (yyyy+mm)),
	'{0}_{1}_{2}'.format(spi[3], src[1], (yyyy+mm)),
	'{0}_{1}_{2}'.format(spi[4], src[1], (yyyy+mm)),

			# Soil Moisture NOAA
	'{0}_{1}_{2}'.format(prdcts[5], src[2], (yyyy+mm))]


		# Download
	for i, url in enumerate(urls):
		print(url)

		ext  = osp.splitext(url)[1]
		out  = osp.join(outpath, fnames[i]+ext)

		#proc = subprocess.call('wget -q -O {0} {1} || rm -f {2}'.format(out, url, out), shell=True) # add -q for quiet
		proc = subprocess.call('wget -q -O {0} {1}'.format(out, url), shell=True) # add -q for quiet

		print(fnames[i])
		
		if proc != 0:
			print('ERROR: PROBLEM WITH URL')
		else:
			print('URL OK')
		print(' ')

		# Rmv empty files
	print 'removing files with error...'
	for f in glb(outpath + '/*'):
		if osp.getsize(f) == 0:
			os.remove(f)