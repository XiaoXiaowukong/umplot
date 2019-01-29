# -*- coding:utf-8 -*-
# 墒情
__version__ = '$Id: plotUtils.py 27349 2018-111-27 18:58:51Z rouault $'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import *
import numpy as np
import matplotlib
import time
from osgeo import gdal, osr
from umOpener.geotiffreader import createXY
from umOpener.openUtils import OpenUtils

import xlrd
import os
from plotBaseUtils import PlotBaseUtils
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import math

sourceDIRPath = "%s/source" % os.path.dirname(os.path.abspath(__file__))
defaultShapeFile = "%s/hebing.shp" % sourceDIRPath
defaultAreaInfoXls = "%s/area_all_info.xls" % sourceDIRPath
zhinbenzhenPath = "%s/zhibeizhen.png" % sourceDIRPath
companyLogo = "%s/logo_50.png" % sourceDIRPath
msyhPath = "%s/msyh.ttf" % sourceDIRPath
myTitlefont = matplotlib.font_manager.FontProperties(fname=msyhPath, style="oblique")


# myTitlefont.set_size(15)


class PlotUtils(PlotBaseUtils):
    def __init__(self):
        PlotBaseUtils.__init__(self)

    # 开始
    def process(self):
        starttime = time.time()
        self.addBaseMap(self.options.mapRange)
        print "addBaseMap time", time.time() - starttime
        starttime = time.time()
        self.drawgdalClipData()
        print "drawgdalClipData time", time.time() - starttime

    # 读取固定列表获取区域的信息
    def readAreaInfo(self):
        areaInfoWorkbook = xlrd.open_workbook(defaultAreaInfoXls)
        areaInfosheet = areaInfoWorkbook.sheet_by_index(0)
        areaInfoRows = areaInfosheet.nrows
        self.defaultAreaInfoList = {}
        for areaInfoRowIndex in xrange(areaInfoRows):
            if (areaInfoRowIndex > 0):
                self.defaultAreaInfoList[areaInfosheet.row_values(areaInfoRowIndex)[0]] = areaInfosheet.row_values(
                    areaInfoRowIndex)
        allLeftRightTopBottom = []
        if (self.options.areaId != None):
            for areaid in self.options.areaId:
                if (areaid in self.defaultAreaInfoList.keys()):
                    areaInfo = self.defaultAreaInfoList[areaid]
                    lefttop = areaInfo[7].split(",")
                    rightbottom = areaInfo[8].split(",")
                    allLeftRightTopBottom.append(
                        [float(rightbottom[1]), float(lefttop[1]), float(lefttop[0]), float(rightbottom[0])])
                else:
                    print "%s areid not found" % areaid
            allLeftRightTopBottom = np.array(allLeftRightTopBottom)
            return (np.min(allLeftRightTopBottom[:, 0]),
                    np.max(allLeftRightTopBottom[:, 1]),
                    np.min(allLeftRightTopBottom[:, 2]),
                    np.max(allLeftRightTopBottom[:, 3]))
        else:
            # 返回内蒙区域
            # return (37.24, 53.23, 97.12, 126.04)
            # 返回全国
            return (15.0, 55.0, 70.0, 140.0)

    # ===================加载底图===============================================================================
    def addBaseMap(self, mapInfo):
        dpi = self.options.dpi
        fig = plt.figure(dpi=dpi)
        m = Basemap(projection='merc', resolution='i', llcrnrlon=mapInfo[2], llcrnrlat=mapInfo[0],
                    urcrnrlon=mapInfo[3], urcrnrlat=mapInfo[1], lat_1=mapInfo[0], lat_2=mapInfo[1],
                    lon_0=(mapInfo[2] + mapInfo[3]) / 2.0, area_thresh=1000)
        fig_width = self.options.picWeight
        fig_width = fig_width / float(self.options.dpi)
        fig_height = fig_width * m.aspect
        figsize = (fig_width, fig_height)
        fig.set_size_inches(figsize)
        self.rec = [self.options.axisRange[0], self.options.axisRange[1], self.options.axisRange[2],
                    self.options.axisRange[2] * fig_width * m.aspect / float(fig_height)]
        ax = fig.add_axes(self.rec)
        # m.drawcoastlines()  # 画海岸线
        # m.drawcountries()  # 画国界线
        # m.drawmapboundary()  # 画中国内部区域，即省界线
        # parallels = np.arange(-90., 90, 1.)  # 创建纬线数组
        # m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10, linewidth=0.1)  # 绘制纬线
        # meridians = np.arange(0., 360., 1.)  # 创建经线数组
        # m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10, linewidth=0.1)  # 绘制经线
        if (self.options.isTransparent == "False"):
            m.drawcoastlines(linewidth=0.5)
            m.drawstates(linewidth=0.25)
        self.fig = fig
        self.ax = ax
        self.m = m
        self.addShapeFile()

    # ===============================加载图层=============================================================
    def addShapeFile(self):
        if (self.options.viewShapeFile != None):
            self.m.readshapefile(self.options.viewShapeFile, 'states', drawbounds=True)
        else:
            print "no over view shapefile "

    def drawgdalClipData(self):
        print self.options.inputfiles
        if (self.options.inputfiles == None):
            return;
        else:
            bandIndex = 0;
            for inputFileIndex, inputfile in enumerate(self.options.inputfiles):
                self.options.inputfile = inputfile
                if (os.path.exists(self.options.inputfile)):
                    if (self.options.isClip == "True"):
                        if (self.options.shapeFile != None and self.options.areaId != None):
                            cutlineWhere = ""
                            for areaid_index, areaid in enumerate(self.options.areaId):
                                cutlineWhere = cutlineWhere + "ADCODE99 LIKE '%s%s' " % (areaid, "%")
                                if (areaid_index + 1 == self.options.areaId.__len__()):
                                    pass
                                else:
                                    cutlineWhere = cutlineWhere + "or "
                            print cutlineWhere
                            dstSRS = osr.SpatialReference()
                            dstSRS.ImportFromEPSG(4326)
                            ds = gdal.Warp("", self.options.inputfile, format='MEM',
                                           cutlineDSName=self.options.shapeFile,
                                           cutlineSQL='SELECT * FROM hebing',
                                           cutlineWhere=cutlineWhere,
                                           dstNodata=np.nan,
                                           dstSRS=dstSRS,
                                           resampleAlg=gdal.GRIORA_NearestNeighbour)
                            if (ds != None):
                                cols = ds.RasterXSize  # 获取文件的列数
                                rows = ds.RasterYSize  # 获取文件的行数
                                bands = ds.RasterCount
                                current_geotransf = ds.GetGeoTransform()  # 获取放射矩阵
                                (current_lat, current_lon) = createXY(current_geotransf, cols, rows)
                                self.lon = current_lon
                                self.lat = current_lat
                                X, Y = np.meshgrid(self.lon, self.lat)
                                self.x, self.y = self.m(X, Y)
                                for band in range(0, bands, 1):
                                    currentBand = ds.GetRasterBand(band + 1)
                                    current_data = currentBand.ReadAsArray(0, 0, cols, rows)
                                    self.data = current_data
                                    self.drawMaxMinMean(bandIndex)
                                    bandIndex = bandIndex + 1
                            else:
                                print "----->gdal clip error"
                    else:
                        print "will plot all data"
                        # 绘制原始数据
                        self.openFile()
                        X, Y = np.meshgrid(self.lon, self.lat)
                        self.x, self.y = self.m(X, Y)
                        bands = self.sourceData.shape[0]
                        for band in range(bands):
                            self.data = self.sourceData[band]
                            self.data[self.data == self.noData[band]] = np.nan
                            self.drawMaxMinMean(bandIndex)
                            bandIndex = bandIndex + 1
                else:
                    print "%s is not exist" % self.options.inputfile

    # 读取原始文件数据
    def openFile(self):
        myOpenUtils = OpenUtils()
        myOpenUtils.initParams(
            self.options.inputfile,
            file_type="GeoTiff")
        self.lat = myOpenUtils.lats
        self.lon = myOpenUtils.lons
        self.sourceData = myOpenUtils.data
        self.noData = myOpenUtils.no_data
        del myOpenUtils

    # 增加或者减少一些小工具
    def addOrDeleteLittleTools(self):
        x, y = self.fig.transFigure.transform((0.9, 0.9))
        # 添加指北针
        self.fig.figimage(plt.imread(zhinbenzhenPath), xo=x, yo=y, zorder=1000)
        # 添加文字说明
        im = plt.imread(companyLogo)
        (picx, picy, picz) = im.shape
        x1, y0 = self.ax.transAxes.transform((1.0, 0.0))
        x0, y1 = self.ax.transAxes.transform((0.0, 1.0))
        vCenter = picx / 2 / y1
        companyName = self.ax.text(1.0, vCenter, unicode(self.options.companyName, "utf-8"),
                                   horizontalalignment="right", verticalalignment="center", transform=self.ax.transAxes,
                                   fontproperties=myTitlefont)
        wordWeight = len(unicode(self.options.companyName, "utf-8")) * companyName.get_fontsize()
        # 添加制作单位logo
        imf = self.fig.figimage(im, xo=x1 - wordWeight - 50 * 2, yo=y0, zorder=1000)
        # 添加比例尺
        # 先算出图片左边的经纬度
        leftpicW = x1 - wordWeight - 50 * 2
        # log左边的经度
        pic_left = ((self.options.mapRange[3] - self.options.mapRange[2]) / (x1 - x0)) * (leftpicW - x0) + \
                   self.options.mapRange[2]
        lessWeigth = 111 * abs(math.cos(int(self.options.mapRange[0])))
        # 剩余经度
        leftEmpty = pic_left - self.options.mapRange[2]
        if (leftEmpty >= 20):
            scale_weight = 3 * lessWeigth
            scale_center = pic_left - 3
            my_units = "km"
        elif (leftEmpty >= 10 and leftEmpty < 20):
            scale_weight = 2 * lessWeigth
            scale_center = pic_left - 2
            my_units = "km"
        elif (leftEmpty > 5 and leftEmpty < 10):
            scale_weight = 1 * lessWeigth
            scale_center = pic_left - 1
            my_units = "km"
        elif (leftEmpty < 5 and leftEmpty > 1):
            scale_weight = 0.5 * lessWeigth
            print "scale_weight", scale_weight
            scale_center = pic_left - 0.5
            my_units = "km"
        else:
            # 剩余多少米
            left_empty_mile = leftEmpty * lessWeigth * 1000
            scale_weight = left_empty_mile / 2
            scale_center = pic_left - scale_weight / 1000 / lessWeigth / 2
            my_units = "m"
        scale_weight = int(scale_weight / 5) * 5
        # scale_weight = 500
        scale_add = 35 / (y1 - y0) * (self.options.mapRange[1] - self.options.mapRange[0])
        self.m.drawmapscale(scale_center, self.options.mapRange[0] + scale_add, pic_left,
                            self.options.mapRange[0] + scale_add, scale_weight, units=my_units,
                            barstyle='fancy', ax=self.ax,
                            zorder=20, fontsize=9, linewidth=0.1)


    def drawMaxMinMean(self, band):
        print "band name ", band
        print self.options.mapRange
        if (self.options.levels != None):
            self.remakeLevels()
            extend = 'both'
            mycolor = []
            for levelsIndex in range(self.levels.__len__() + 1):
                mycolor.append(self.options.cmap[levelsIndex])
            if (self.levels.__len__() == 1):
                mycolor.insert(0, "#ffffff")
                self.levels.insert(0, np.nanmin(self.data))
            cs = self.m.contourf(self.x, self.y, self.data, norm=self.options.normalize, levels=self.levels,
                                 alpha=self.options.alpha, extend=extend, colors=mycolor)
        else:

            # if (self.options.levels != None):
            #     self.options.cmap = ListedColormap(self.colors)
            # else:
            # 渐变色
            self.colors = LinearSegmentedColormap.from_list('custom_colcor', self.options.cmap, N=256)
            if (self.options.plotType == "contourf"):
                cs = self.m.contourf(self.x, self.y, self.data, cmap=self.colors, norm=self.options.normalize,
                                     alpha=self.options.alpha)
            elif (self.options.plotType == "pcolormesh"):
                cs = self.m.pcolormesh(self.x, self.y, self.data, cmap=self.colors, norm=self.options.normalize,
                                       alpha=self.options.alpha)
            elif (self.options.plotType == "pcolor"):
                cs = self.m.pcolor(self.x, self.y, self.data, cmap=self.colors, norm=self.options.normalize,
                                   alpha=self.options.alpha)
        if (self.options.isAddViews == "True"):
            self.addOrDeleteLittleTools()
        # if (self.options.colorbarPosition != None):
        #     cax2 = self.fig.add_axes(self.options.colorbarPosition)  # 这块会影响绘制效率
        #     plt.colorbar(cs, cax=cax2, orientation='vertical')
        print self.options.outputFiles[band]
        if (self.options.isTransparent == "False"):
            transparent = False
        else:
            transparent = True
        # 是否去掉axis的边框
        self.ax.axis(self.options.axis)  # 去掉ax画出的部分刻度
        self.fig.savefig(self.options.outputFiles[band], format='png', transparent=transparent, dpi=self.options.dpi,
                         pad_inches=0)
        plt.close()

    def remakeLevels(self):
        self.levels = []
        for level in self.options.levels:
            self.levels.append(float(level))
        print self.levels


def stop(self):
    self.stopped = True


if __name__ == '__main__':
    startTime = time.time()
    argv = sys.argv
    if argv:
        myPlotUtils = PlotUtils()
        myPlotUtils.outsideParams(argv[1:])
        myPlotUtils.process()
        print "end time ", time.time() - startTime
