# -*- coding: UTF-8 -*-
'''
Created on Dec 21 2018

Geracao figuras do Monitor de Secas

@author: Diego Xavier - Modelagem Numerica/FUNCEME

Based on QGIS Python Programming Cookbook (Joel Lawhead - 2015)
QGIS API Documentation: https://qgis.org/api/
Run on terminal: $ /usr/bin/python /home/funceme/monitor/flux/figs_gen.py

'''

# Import modules
import os, sys, fnmatch, argparse
from qgis.core import *
import qgis.utils
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication
from qgis.utils import iface
from qgis.utils import *
from os import path as osp
from glob import glob as glb
from os.path import basename as bn
from time import sleep

x = QApplication([], True)
sys.path.append("/usr/share/qgis/python/plugins/")

def arguments():
    """
    Function to insert parameters from external environment (example: shell)

    In this function is possible to insert the following parameters:
    Diretorio do monitor atual estruturado (-src)

    Ex1: Gerar figuras de apoio:
        /usr/bin/python figs_gen.py -src=/home/funceme/monitor/55_MAPAS_JAN2019/QGIS_INICIAL_FINAL
    """

    __description__ = "Script de geracao das figuras de apoio do Monitor"

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
    if os.path.exists(path): 
        return True
    elif not os.path.exists(path):
        os.mkdir(path)

def StringToRaster():
    mm_d1 = {'01':'Jan', '02':'Fev', '03':'Mar', '04':'Abr', '05':'Mai', '06': 'Jun',
             '07': 'Jul', '08':'Ago', '09':'Set', '10':'Out', '11':'Nov', '12': 'Dez'}

    # Project folder
    project_folder = args.src
    outpath        = osp.join(project_folder, 'FIGS', 'FIGS_APOIO')
    ckdir(outpath)
    # Current month and year
    fls = glb(project_folder + "/*.qgs")
    for f in fls:
        if len(osp.basename(f)) == 13:
            yyyy, mm = osp.basename(f)[3:7], osp.basename(f)[7:9]
            print yyyy,mm
       
    # Load map
    # print('step1')
    # print(' ')
    # sleep(0)

    reg = QgsMapLayerRegistry.instance()

    # Load project
    f = QFileInfo(f)
    p = QgsProject.instance()
    p.read(f)

    # Load mask
    msk_fl  = osp.join(project_folder, 'Base_cartografica', 'MS_Mascara.shp')
    msk_qml = osp.join(project_folder, 'Base_cartografica', 'MS_Mascara.qml')
    lyr = QgsVectorLayer(msk_fl, "MS_Mascara", "ogr")
    lyr.loadNamedStyle(msk_qml)
    lyr.triggerRepaint()
    reg.addMapLayer(lyr, False)

    for idx, tif in enumerate(QgsMapLayerRegistry.instance().mapLayers().values()):
        bname = tif.name()
        lfls = len(QgsMapLayerRegistry.instance().mapLayers().values())
        if tif.type() == 1:

            # Create blank image
            #print('step2')
            #print(' ')
            sleep(0)

            if idx == 0:
                i = QImage(QSize(600, 600), QImage.Format_ARGB32_Premultiplied)
                c = QColor("White")
                i.fill(c.rgb())
                p = QPainter()
                p.begin(i)

            # Get map layers ID
            lyrs = [lyr.id(), tif.id()]

            mr = QgsMapRenderer()

            # Choose layers
            mr.setLayerSet(lyrs)

            rect = QgsRectangle(lyr.extent())

            # Set scale and extent
            rect.scale(1.2)
            mr.setExtent(rect)

            # Create composition
            #print('step3')
            #print(' ')
            sleep(0)

            c = QgsComposition(mr)
            c.setPlotStyle(QgsComposition.Print)
            c.setPaperSize(150, 210)

            w, h = c.paperWidth(), c.paperHeight()
            x = (c.paperWidth() - w)
            y = ((c.paperHeight() - h)) + 10

            # Set extent
            composerMap = QgsComposerMap(c,x,y,w,h)
            composerMap.setNewExtent(rect)

            # Set border frame
            c.addItem(composerMap)

            # Get titles
            splt = bname.split("_", 2)
            if splt[0] in ['SDSI', 'SPI', 'SPEI', 'SRI'] and 'Blend' not in bname:
                ttl  = splt[0] + ' ' + splt[1][-2:] + ' ' + 'meses'
                if splt[1][-2:] == '01':
                    ttl = splt[0]+ ' ' + splt[1][-2:] + ' ' + 'mes'
                print(bname, 0, ttl)
            
            if 'Blend' in bname:
                splt = bname.split("_", 4)
                ttl  = 'Combinado - Minimo -' + ' ' + splt[3] + ' e ' + splt[4]
                print(bname, 1, ttl)
            
            if 'ACCUM' in bname:
                splt = bname.split("_", 2)
                ttl  = 'Precipitacao Acumulada - ' + splt[1][-2:] + ' meses'
                if splt[1][-2:] == '01':
                    ttl = 'Precipitacao Acumulada - ' + splt[1][-2:] + ' mes'
                print(bname, 2, ttl)
            
            if 'ANOMPERC' in bname:
                splt = bname.split("_", 2)
                ttl  = 'Anomalia Percentual de Precipitacao - ' + splt[1][-2:] + ' meses'
                if splt[1][-2:] == '01':
                    ttl = 'Anomalia Percentual de Precipitacao - ' + splt[1][-2:] + ' mes'
                print(bname, 3, ttl)

            if 'VHP' in bname:
                splt = bname.split(".", 7)
                ttl  = 'VHI Semanal - {0}/{1}/{2}'.format(splt[4][-2:], mm_d1[splt[4][-4:-2]], splt[4][1:5])
            if 'VHI' in bname and 'VHP' not in bname:
                splt = bname.split("_", 3)
                print splt
                ttl  = 'VHI Mensal - Minimo - {0}/{1}'.format(mm_d1[splt[2][-2:]], splt[2][:4])
                if 'mean' in bname:
                    ttl  = 'VHI Mensal - Media - {0}/{1}'.format(mm_d1[splt[2][-2:]], splt[2][:4])
                print(bname, 4, ttl)

            if 'temp_maxima' in bname:
                splt = bname.split("_", 5)
                ttl  = 'Temperatura Maxima - {0}/{1} - Estacoes Automaticas'.format(splt[3].capitalize(), splt[2])
                if len(splt) == 6:
                    ttl  = 'Temperatura Maxima - {0}/{1} - Estacoes Automaticas'.format(splt[4], splt[3][:4])
            if 'temp_media' in bname:
                splt = bname.split("_", 5)
                ttl  = 'Temperatura Media - {0}/{1} - Estacoes Automaticas'.format(splt[3].capitalize(), splt[2])
                if len(splt) == 6:
                    ttl  = 'Temperatura Media- {0}/{1} - Estacoes Automaticas'.format(splt[4], splt[3][:4])
                print(bname, 5, ttl)

            if 'anom_tmax' in bname:
                splt = bname.split("_", 7)
                ttl  = 'Anomalia de Temperatura Maxima - {0} - 1981 a 2010'.format(splt[2].upper())
            if 'anom_tmed' in bname:
                splt = bname.split("_", 7)
                ttl  = 'Anomalia de Temperatura Media - {0} - 1981 a 2010'.format(splt[2].upper())
                print(bname, 6, ttl)


            if 'clim.tmax' in bname:
                splt = bname.split(".", 7)
                ttl  = 'Climatologia de Temperatura Maxima - {0} - 1981 a 2010'.format(splt[2].upper())
            if 'clim.tmed' in bname:
                splt = bname.split(".", 7)
                ttl  = 'Climatologia de Temperatura Media - {0} - 1981 a 2010'.format(splt[2].upper())
                print(bname, 7, ttl)

            # Add Label
            c.label = QgsComposerLabel(c)
            try:
                c.label.setText("{0}".format(ttl))
            except:
                c.label.setText("{0}".format(bname))
            c.label.setFont(QFont("Cantarell", 14, QFont.Bold))
            c.label.adjustSizeToText()
            c.label.setItemPosition(5, 5)
            c.addItem(c.label)

            c.date = QgsComposerLabel(c)

            print(mm, yyyy)
            c.date.setText(mm_d1[mm] + '/' + yyyy)
            
            # Titulo para raster de meses anteriores
            try:
                if bname.split("_", 2)[1][:4].isdigit() and bname.split("_", 2)[1][4:6].isdigit():
                    yyyy1 = bname.split("_", 2)[1][:4]
                    mm1   = bname.split("_", 2)[1][4:6]
                    c.date.setText(mm_d1[mm1] + '/' + yyyy1)
            except:
                pass

            c.date.setFont(QFont("Cantarell", 14, QFont.Bold))
            c.date.adjustSizeToText()
            c.date.setItemPosition(5, 12)
            c.addItem(c.date)

            # Add Scale bar
            c.scalebar = QgsComposerScaleBar(c)
            c.scalebar.setStyle('Line Ticks Up')
            c.scalebar.setFont(QFont("Cantarell", 9))
            c.scalebar.setComposerMap(composerMap)
            c.scalebar.applyDefaultSize()
            c.scalebar.setNumSegmentsLeft(0)
            c.scalebar.setItemPosition(10, 195)
            c.addItem(c.scalebar)

            # Add north arrow
            # ar_x, ar_y = 15, 50

            # c.arrow = QgsComposerArrow(QPointF(ar_x, ar_y), QPointF(ar_x, ar_y-8), c)
            # c.addItem(c.arrow)

            # f = QFont()
            # f.setBold(True)
            # f.setFamily("Cantarell")
            # f.setPointSize(13)
            # c.labelNorth = QgsComposerLabel(c)
            # c.labelNorth.setText("N")
            # c.labelNorth.setFont(f)
            # c.labelNorth.adjustSizeToText()
            # c.labelNorth.setFrameEnabled(False)
            # c.labelNorth.setItemPosition(ar_x-2.5, ar_y-18)
            # c.addItem(c.labelNorth)

            # Add MS Legend

            if any(name in bname.lower() for name in ['sdsi', 'spei', 'spi', 'sri', 'esi']) and 'ultim' not in bname.lower():
                c.logo = QgsComposerPicture(c)
                c.logo.setPictureFile(osp.join(project_folder, 'MS-leg_new.png'))
                c.logo.setSceneRect(QRectF(0,0,57,42))
                c.logo.setItemPosition(93,162)
                c.addItem(c.logo)
            elif any(name in bname.lower() for name in ['accum', 'anom', 'anomperc', 'clim', 'temp', 'vhp', 'vhi']):
                c.legend = QgsComposerLegend(c)
                
                lyrGroup = QgsLayerTreeGroup()
                for l in QgsMapLayerRegistry.instance().mapLayers().values():
                    if l.name() == tif.name():
                        lyrGroup.addLayer(l)
                c.legend.modelV2().setRootGroup(lyrGroup)
                
                c.legend.setTitle('LEGENDA')
                
                
                if any(name in bname.lower() for name in ['anom_t', 'clim.t', 'temp']):
                    un = u'   ° C'
                elif any(name in bname.lower() for name in ['accum_']):
                    un = '  mm'
                elif any(name in bname.lower() for name in ['anomperc_']):
                    un = '  %'
                else:
                    un = ' '

                tif.setLayerName(un)
                c.legend.setStyleFont(QgsComposerLegendStyle.Title, QFont('Cantarell', 11))
                c.legend.setStyleFont(QgsComposerLegendStyle.Subgroup, QFont('Cantarell', 8,2))
                c.legend.setStyleFont(QgsComposerLegendStyle.SymbolLabel, QFont('Cantarell', 8))
                c.legend.setSymbolHeight(2)
                c.legend.adjustBoxSize()
                c.legend.setItemPosition(106, 120)
                c.addComposerLegend(c.legend)

            # Set DPI
            dpi = c.printResolution()
            c.setPrintResolution(dpi)

            mm_in_inch = 25.4
            dpmm   = dpi / mm_in_inch
            width  = int(dpmm * c.paperWidth())
            height = int(dpmm * c.paperHeight())

            # Initialize image
            #print('step4')
            #print(' ')
            sleep(0)

            image = QImage(QSize(width, height), QImage.Format_ARGB32)
            image.setDotsPerMeterX(dpmm * 1000)
            image.setDotsPerMeterY(dpmm * 1000)
            image.fill(0)

            # Render composition
            imagePainter = QPainter(image)
            sourceArea = QRectF(0, 0, c.paperWidth(), c.paperHeight())
            targetArea = QRectF(0, 0, width, height)
            c.render(imagePainter, targetArea, sourceArea)  
            imagePainter.end()
            # del(imagePainter)

            # Save file
            #print('step5')
            #print(' ')
            sleep(0)

            fname   = "/{0}.png".format(bname)

            image.save(outpath+fname, "png")

            #print(idx)


if __name__ == "__main__":
    QgsApplication.setPrefixPath("/usr/share/qgis", True)
    qgs = QgsApplication([], True)
    qgs.initQgis()
    StringToRaster()
    qgs.exitQgis()
