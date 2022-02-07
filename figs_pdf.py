
# -*- coding: UTF-8 -*-
'''
Created on Jan 15 2018

Geracao dos PDFs do Monitor de Secas

@author: Diego Xavier - Modelagem Numerica/FUNCEME
'''
from glob import glob as glb
from os import path as osp

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm

def generate_pdf(x, y, figs, outpath, filename='gen.pdf', layout='3x4', i=0, j=0, width=70, height=70, ls=False):
	"""
	A4 - (210.0, 297.0) mm

	x: posicao horizontal inicial (mm) - int
	y: posicao vertical inicial (mm) - int
	layout: escolha do layout - str
	figs: caminho das figuras - list
	filename: caminho do arquivo final - str
	i: incremento horizontal (mm) - int
	j: incremento vertical (mm) - int
	width: largura da figura (mm) - int
	height: altura da figura (mm) - int
	ls: modo paisagem - bool
	"""

	c = canvas.Canvas(osp.join(outpath, filename), pagesize=A4)
	
	if ls:
		c = canvas.Canvas(osp.join(outpath, filename), pagesize=landscape(A4))
	
	print osp.join(outpath, filename)

	jj = j
	ii = i
	i, j = 0, 0
	for idx, fig in enumerate(figs):
		im = Image.open(fig)

		if layout == '3x4':
			if idx == 4 or idx == 8:
				i += ii
				j  = 0

		if layout == '2x4':
			if idx == 4:
				i  = 0
				j += jj

		if layout == '3x3':
			if idx == 3 or idx == 6:
				i += ii
				j  = 0

		if layout == '1x3':
			pass

		c.drawInlineImage(im, x+(i*mm), y+(j*mm), width=width*mm, height=height*mm)
		print osp.basename(fig), "-", i, j
		
		if ls:
			i += ii
		if not ls:
			j += jj

	c.save()

outpath = '/home/funceme/monitor/55_MAPAS_JAN2019/QGIS_INICIAL_FINAL/FIGS/pdf'

# Prec CPTEC
accum = sorted(glb("/home/funceme/monitor/figs/2018/FIGS/lt/*Acum_Cptec*"))

clim  = sorted(glb("/home/funceme/monitor/figs/2018/FIGS/lt/*Clim_Cptec*61-90.gif"))
myorder = [0, 3, 2, 1]
clim  = [clim[i] for i in myorder[::-1]]

anom  = sorted(glb("/home/funceme/monitor/figs/2018/FIGS/lt/*Anom_Cptec*"))
figs  = accum+clim+anom

generate_pdf(0, 20, figs, outpath, filename='pr_cptec_3x4.pdf', layout='3x4', i=70, j=70, width=70, height=70)
exit()

# VHI (ou EVI)
vhi_wk  = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/VHP*"))[:4]
vhi_mon = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/VHI*"))[:4]
figs    = vhi_wk+vhi_monx

generate_pdf(0, 3, figs, outpath, filename='vhi_2x4.pdf', layout='2x4', i=73, j=103, width=75, height=104, ls=True)

# Prec Accum 3x3
accum = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/ACCUM*"))
anom  = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/ANOMPERC*"))
figs_pr  = accum+anom

generate_pdf(3, 8, figs_pr, outpath, filename='pr_funceme_3x3.pdf', layout='3x3', i=70, j=95, width=68, height=95)

# Prec Accum 1x3 (ou MS 1x3)
accum = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/ACCUM*"))[:3]
figs  = accum

generate_pdf(5, 110, figs, outpath, filename='pr_funceme_1x3.pdf', layout='1x3', i=95, j=0, width=100, height=139, ls=True)









# Prec Accum 1x3 + 1x9 Prec
accum = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/ACCUM*"))[:3]
figs  = accum

filename = "MS_prec_1x3_1x9.pdf"
print osp.join(outpath, filename)

c = canvas.Canvas(osp.join(outpath, filename), pagesize=landscape(A4))

i, j = 0, 0
for idx, fig in enumerate(figs):
	im = Image.open(fig)
	c.drawInlineImage(im, (i*mm)+5, (j*mm)+10, width=100*mm, height=139*mm)
	print osp.basename(fig), "-", i, j
	i += 95
	

i, j = 0, 0
for idx, fig in enumerate(figs_pr):
	im = Image.open(fig)
	c.drawInlineImage(im, (i*mm)+8, 155*mm, width=32*mm, height=45*mm)
	print osp.basename(fig), "-", i, j
	i += 31
	

c.save()







# Indices
vhi_wk  = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/VHP*"))[:4]
vhi_mon = sorted(glb("/home/funceme/monitor/54_MAPAS_DEZ2018/FIGS/pdf/VHI*"))[:4]
figs    = vhi_wk+vhi_mon

filename = "indices_2x4.pdf"
print osp.join(outpath, filename)

c = canvas.Canvas(osp.join(outpath, filename), pagesize=landscape(A4))

i, j, cnt = 0, 0, 0
while cnt < 8*3:
	for idx, fig in enumerate(figs):
		if idx == 4:
			i  = 0
			j += 103
		im = Image.open(fig)
		c.drawInlineImage(im, (i*mm)+0, (j*mm)+3, width=75*mm, height=104*mm)
		print osp.basename(fig), "-", i, j

		i += 73

		if idx == 7:
			# new page
			c.showPage()
			i, j = 0, 0

		cnt += 1

c.save()
