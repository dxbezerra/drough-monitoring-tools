# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:27:39 2018

@author: Diego Xavier - Modelagem Numérica/FUNCEME

execfile(u'/home/funceme/monitor/MS_project_gen.py'.encode('UTF-8'))

Como carregar e rodar script dentro do QGIS:
https://gis.stackexchange.com/questions/29580/how-to-run-a-simple-python-script-for-qgis-from-outside-e-g-sublime-text

Layer Trees:
https://www.lutraconsulting.co.uk/blog/2014/07/25/qgis-layer-tree-api-part-2/
https://www.hatarilabs.com/ih-en/how-to-add-multiple-vector-layers-and-group-them-in-qgis-with-pyqgis-tutorial

Getting layer name:
https://gis.stackexchange.com/questions/136861/getting-layer-by-name-in-pyqgis

Groups visibility:
https://gis.stackexchange.com/questions/189294/pyqgis-toggle-group-visibility-and-recursively-subsub-group-visibility

Unfold all groups by editing project .xml:
https://gis.stackexchange.com/questions/137045/workaround-for-grouped-layers-to-stay-collapsed-when-opening-project
"""
from qgis.utils import iface
import os, sys, fileinput, argparse
from os.path import basename as bn
from os.path import join as jn
from os.path import splitext as st
from glob import glob as glb
import qgis.utils
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.PyQt import QtXml

x = QApplication([], True)
sys.path.append("/usr/share/qgis/python/plugins/")

def arguments():
	"""
	Function to insert parameters from external environment (example: shell)

	In this function is possible to insert the following parameters:
	Ano atual do monitor(-ano), Mes atual do monitor(-mes),
	Diretorio do monitor atual estruturado (-src)

	Ex1: Gerar projeto QGIS para Janeiro 2019:
		/usr/bin/python project_gen.py -ano=2019 -mes=01 -src=/home/funceme/monitor/55_MAPAS_JAN2019/QGIS_INICIAL_FINAL
	"""

	__description__ = "Script de geracao do projeto QGIS"

	global args
	parser = argparse.ArgumentParser(description=__description__)
	parser.add_argument('-ano', help='Ano atual do Monitor')
	parser.add_argument('-mes', help='Mes atual do Monitor')
	parser.add_argument('-src', help='Diretorio estruturado do monitor atual')

	args = parser.parse_args()

	return args

arguments()

def StringToRaster():

	# Functions
	def add_vlayer(shape, group, order=0, addToLegend=False):
		"""
		Function to add a vector layer on a specific group.
		"""
		vlayer = QgsVectorLayer(shape, st(bn(shape))[0], "ogr")
		crs = vlayer.crs()
		crs.createFromId(4326)
		vlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(vlayer, addToLegend)
		group.insertChildNode(order, QgsLayerTreeLayer(vlayer))

	def add_rlayer(tif, group, order=0, addToLegend=False):
		"""
		Function to add a raster layer on a specific group.
		"""
		rlayer = QgsRasterLayer(tif, st(bn(tif))[0])
		crs = rlayer.crs()
		crs.createFromId(4326)
		rlayer.setCrs(crs)
		QgsMapLayerRegistry.instance().addMapLayer(rlayer, addToLegend)
		group.insertChildNode(order, QgsLayerTreeLayer(rlayer))

	def find_n_replace(fileToSearch, textToSearch="expanded=\"1\"", textToReplace="expanded=\"0\""):
		""""
		Function to find and replace a text on the project XML.
		"""
		tempFile = open(fileToSearch, 'r+')
		for line in fileinput.input(fileToSearch):
			tempFile.write(line.replace(textToSearch, textToReplace))
		tempFile.close()

	# Mes e Ano do Monitor atual
	mm, yyyy = args.mes, args.ano
	# mm, yyyy = '01', '2019'
	# Diretorio do projeto
	project_folder = args.src
	# project_folder = '/home/funceme/alo'

	# Nome do arquivo .qgs
	project_fname  = "MS_{0}{1}.qgs".format(yyyy, mm)
	project = QgsProject.instance()
	project.setFileName(jn(project_folder, project_fname))

	# Avoid CRS layer window
	settings = QSettings()
	oldProjValue = settings.value("/Projections/defaultBehaviour", "prompt", type=str)
	settings.setValue("/Projections/defaultBehaviour", "useProject")

	# Groups
	ms1, ms2 = "MS_{0}{1}".format(yyyy, mm), "MS_{0}{1}".format(yyyy, str(int(mm)-1).zfill(2))
	if ms2[-2:] == '00':
		ms2 = 'MS_' + str(int(yyyy)-1) + '12'

	groups = ['Base_cartografica', ms1, ms2, 'Indicadores', 'Produtos_apoio']
	
	for i, group in enumerate(groups):
		root = QgsProject.instance().layerTreeRoot()
		
		# Set WGS-84 CRS and Enable 'On-the-fly' transformation
		CRS = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
		canvas = QgsMapCanvas()
		canvas.setDestinationCrs(CRS)
		canvas.mapRenderer().setProjectionsEnabled(True)
		
		if not os.path.isdir(jn(project_folder, group)):
			os.mkdir(jn(project_folder, group))
		
		if i == 0:
			# Base_cartografica
			path   = jn(project_folder, group)
			shapes = sorted(glb(path + "/**/*.shp"))
			# Create Group
			add_group = root.addGroup(group)
			# Insert Data
			for shape in shapes:
				add_vlayer(shape, add_group, order=-1)
			# Set Styles
			for layer in QgsMapLayerRegistry.instance().mapLayers().values():
				layer.loadNamedStyle(path + "/base_cartografica.qml")
				if 'Estados' in layer.name() or 'UF' in layer.name():
					layer.loadNamedStyle(path + "/limites.qml")
				if 'Mascara' in layer.name():
					layer.loadNamedStyle(path + "/mascara.qml")					
			# Set Visibility
			add_group.setVisible(Qt.Unchecked)
		if i == 1:
			# MS_Atual
			path   = jn(project_folder, group)
			shapes = sorted(glb(path + "/*.shp"))
			# Create Group
			add_group = root.addGroup(group)
			# Insert data
			for shape in shapes[2:]:
				add_vlayer(shape, add_group, order=0)
			for shape in shapes[:2]:
				add_vlayer(shape, add_group, order=0)
			# Set Styles
			#for layer in QgsMapLayerRegistry.instance().mapLayers().values():
			#		if layer.name() == 'MS_Impactos':
			#		layer.loadNamedStyle(path + "/MS_Impactos.qml")
			# Set Visibility
			add_group.setVisible(Qt.Unchecked)
		if i == 2:
			# MS_Anterior
			path   = jn(project_folder, group)
			shapes = sorted(glb(path + "/*.shp"))
			# Create Group
			add_group = root.addGroup(group)
			# Insert data
			for shape in shapes[2:]:
				add_vlayer(shape, add_group, order=0)
			for shape in shapes[:2]:
				add_vlayer(shape, add_group, order=0)
			# Set Styles
			for layer in QgsMapLayerRegistry.instance().mapLayers().values():
				if 'MS_Impactos' in layer.name():
					layer.loadNamedStyle(path + "/MS_Impactos.qml")
				if 'Tipo' in layer.name():
					layer.loadNamedStyle(path + "/MS_Impactos_Tipo.qml")
			# Set Visibility
			add_group.setVisible(Qt.Unchecked)
			# Unexpand group
			add_group.setExpanded(False)
		if i == 3:
			# Indicadores
			# Create Group
			add_group = root.addGroup(group)
			subgroups = ['SDSI', 'SPEI', 'SPI', 'SRI', 'Indicador_combinado']
			for subg in subgroups:
				## Como adicionar arquivo nas pastas?
				if not os.path.isdir(jn(jn(project_folder, group), subg)):
					os.mkdir(jn(jn(project_folder, group), subg))
				# Create Subgroup
				add_subg = add_group.addGroup(subg)
				# Load Tifs and Shapes
				path   = (jn(jn(project_folder, group), subg))
				tifs   = sorted(glb(path + "/*.tif"))[::-1]
				shapes = sorted(glb(path + "/*.shp"))[::-1]
				# Insert data
				for tif in tifs:
					add_rlayer(tif, add_subg, order=0)
				if shapes:
					for shape in shapes:
						add_vlayer(shape, add_subg, order=0)
				# Set Styles
				for layer in QgsMapLayerRegistry.instance().mapLayers().values():
					if 'SDSI' in layer.name() and subg == 'SDSI':
						layer.loadNamedStyle(path + "/SDSI.qml")
					if 'SPEI' in layer.name() and subg == 'SPEI':
						layer.loadNamedStyle(path + "/SPEI.qml")
					if 'SPI' in layer.name() and subg  == 'SPI':
						layer.loadNamedStyle(path + "/SPI.qml")
					if 'SRI' in layer.name() and subg  == 'SRI':
						layer.loadNamedStyle(path + "/SRI.qml")

					# Se for shape e indicador
					if layer.type() == 0 and any(name in layer.name() for name in ['SDSI', 'SPEI', 'SPI', 'SRI']):
						ind = layer.name().split("_", 2)[0]
						mon = layer.name()[-3:]
						layer.loadNamedStyle(path + "/{0}_{1}_ponto.qml".format(ind, mon))
						# print(layer.name(), layer.type())

					if 'Blend' in layer.name() and subg  == 'Indicador_combinado':
						layer.loadNamedStyle(path + "/blend.qml")
				
				# Set Visibility
				add_subg.setVisible(Qt.Unchecked)
				# Unexpand group
				add_subg.setExpanded(False)
			# Set Visibility
			add_group.setVisible(Qt.Unchecked)
			# Unexpand group
			add_group.setExpanded(False)
			project.write()
		if i == 4:
			# Produtos_apoio
			# Create Group
			add_group = root.addGroup(group)
			subgroups = ['Precipitacao', 'Temperatura', 'VHI', 'ESI', 'Relevo']
			for subg in subgroups:
				## Como adicionar arquivo nas pastas?
				if not os.path.isdir(jn(jn(project_folder, group), subg)):
					os.mkdir(jn(jn(project_folder, group), subg))
				# Create Subgroup
				add_subg = add_group.addGroup(subg)
				# Create Sub-subgroups
				if subg == 'Precipitacao':
					subsubg = ['Acumulado', 'Anomalia', 'Climatologia', 'Estacoes', 'Quantis', 'SPI_outros']
					for ssub in subsubg:
						# Add sub-subgroup
						add_subsubg = add_subg.addGroup(ssub)
						# Load Tifs
						path = (jn(jn(project_folder, group), subg, ssub))
						tifs = sorted(glb(path + "/*.tif"))
						if ssub == 'Estacoes':
							tifs = tifs[::-1]
						if ssub == 'SPI_outros':
							tifs = tifs[::-1]
						# Insert Data
						for tif in tifs:
							add_rlayer(tif, add_subsubg, order=0)
						# Set Styles
						for layer in QgsMapLayerRegistry.instance().mapLayers().values():
							if 'ACCUM' in layer.name() and 'm01'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m01.qml")
							if 'ACCUM' in layer.name() and 'm03'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m03.qml")
							if 'ACCUM' in layer.name() and 'm04'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m04.qml")
							if 'ACCUM' in layer.name() and 'm06'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m06.qml")
							if 'ACCUM' in layer.name() and 'm12'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m12.qml")
							if 'ACCUM' in layer.name() and 'm18'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m18.qml")
							if 'ACCUM' in layer.name() and 'm24'in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ACCUM_m24.qml")
							if 'ANOMPERC' in layer.name() and ssub == 'Estacoes':
								layer.loadNamedStyle(path + "/ANOMPERC.qml")
						# Set Visibility and Unexpand
						add_subsubg.setVisible(Qt.Unchecked)
						# Set Unexpand
						add_subsubg.setExpanded(False)
				elif subg == 'Temperatura':
					subsubg = ['Anomalia', 'Climatologia', 'Maximas', 'Medias']
					for ssub in subsubg:
						# Add sub-subgroup
						add_subsubg = add_subg.addGroup(ssub)
						path = (jn(jn(project_folder, group), subg, ssub))
						tifs = sorted(glb(path + "/*.tif"))
						# Insert Data
						for tif in tifs:
							add_rlayer(tif, add_subsubg, order=0)
						# Set Styles
						for layer in QgsMapLayerRegistry.instance().mapLayers().values():
							if 'anom_t' in layer.name():
								layer.loadNamedStyle(path + "/anom.qml")
							if 'clim.tmed' in layer.name():
								layer.loadNamedStyle(path + "/clim.qml")
							if 'clim.tmax' in layer.name():
								layer.loadNamedStyle(path + "/clim.tmax.qml")	
							if 'temp_maxima' in layer.name():
								layer.loadNamedStyle(path + "/max.qml")
							if 'temp_media' in layer.name():
								layer.loadNamedStyle(path + "/med.qml")
						# Set Visibility and Unexpand
						add_subsubg.setVisible(Qt.Unchecked)
						# Set Unexpand
						add_subsubg.setExpanded(False)
				else:
					path   = (jn(jn(project_folder, group), subg))
					tifs   = sorted(glb(path + "/*.tif"))[::-1]
					# Insert data
					for tif in tifs:
						add_rlayer(tif, add_subg, order=0)
					# Set Styles
					for layer in QgsMapLayerRegistry.instance().mapLayers().values():
						if 'ESI' in layer.name():
							layer.loadNamedStyle(path + "/ESI.qml")
						if 'VHP' in layer.name():
							layer.loadNamedStyle(path + "/VHI.qml")
						if 'VHI_sam' in layer.name():
							layer.loadNamedStyle(path + "/VHI.qml")
				# Set Visibility
				add_subg.setVisible(Qt.Unchecked)
				# Set Unexpand
				add_subg.setExpanded(False)
			# Set Visibility
			add_group.setVisible(Qt.Unchecked)
			# Unexpand group
			add_group.setExpanded(False)

	# Load composer

	# myMapRenderer = QgsMapRenderer()
	# myComposition = QgsComposition(myMapRenderer)
	# template = QtCore.QFile(jn(project_folder, "template_legenda_monitor.qpt"))
	# doc = QtXml.QDomDocument()
	# doc.setContent(template, False)
	# myComposition.loadFromTemplate(doc)

	# myMapRenderer = QgsMapRenderer()
	# myComposition = QgsComposition(myMapRenderer)
	# myFile = jn(project_folder, "template_legenda_monitor.qpt")
	# myTemplateFile = file(myFile, 'rt')
	# myTemplateContent = myTemplateFile.read()
	# myTemplateFile.close()
	# myDocument = QtXml.QDomDocument()
	# myDocument.setContent(myTemplateContent)
	# myComposition.loadFromTemplate(myDocument)

	# # Add all layers in map canvas to render
	# myMapRenderer = QgsMapRenderer()

	# # Load template from file
	# myComposition = QgsComposition(myMapRenderer)
	# myFile = jn(project_folder, "template_legenda_monitor.qpt")
	# # print(myFile)
	# # print(os.path.isfile(myFile))
	# myTemplateFile = file(myFile, 'rt')
	# myTemplateContent = myTemplateFile.read()
	# # myTemplateFile.close()
	# myDocument = QtXml.QDomDocument()
	# myDocument.setContent(myTemplateContent)
	
	# compo = iface.createNewComposer(title="monitor")
	# compo.composition().loadFromTemplate(myDocument)
	# iface.activeComposers()
	# # myComposition.loadFromTemplate(myDocument)

	project.write()

	# Unexpand all by editing project file
	fileToSearch = jn(project_folder, project_fname)
	find_n_replace(fileToSearch)

	# Set Title
	find_n_replace(fileToSearch, textToSearch="<title></title>", \
		textToReplace="<title>MONITOR DE SECAS {0}/{1}</title>".format(mm, yyyy))

	# Close project
	project.clear()
	del(project)

# Exit QGIS
if __name__ == "__main__":
    QgsApplication.setPrefixPath("/usr/share/qgis", True)
    qgs = QgsApplication([], True)
    qgs.initQgis()
    StringToRaster()
    qgs.exitQgis()

# Set initial message
# Project = QgsProject.instance().read(QFileInfo(fileToSearch))
# msgbar = iface.messageBar()
# msgbar.pushMessage('AVISO', 'Projeto teste do Monitor de Secas', QgsMessageBar.WARNING, 30)
