# -*- coding:utf-8 -*-
__version__ = '$Id: plotUtils.py 27349 2018-111-27 18:58:51Z rouault $'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import *
import numpy as np
import matplotlib

import time
from osgeo import gdal
from umOpener.geotiffreader import createXY
from umOpener.openUtils import OpenUtils

from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import xlrd

axis_list = ("on", "off")
is_clip_list = ("True", "False")
plot_list = ("contourf", "pcolormesh", "pcolor")

myTitlefont = matplotlib.font_manager.FontProperties(
    fname="/Users/lhtd_01/Downloads/gn_pyserver_py/um_pyserver_fy/statics/msyh.ttf", style="oblique")

sourcePath = "%s/source" % os.getcwd()


class PlotUtils():
    def __init__(self):
        print "__init__"

    # 初始化
    def initParams(self, **kwgs):
        print kwgs
        self.stopped = False
        self.optparse_init()
        arguments = []
        for kwarg_key in kwgs.keys():
            arguments.append("--%s" % kwarg_key)
            arguments.append(kwgs[kwarg_key])
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        self.initSettings()
        print self.options
        self.process()

    def outsideParams(self, arguments):
        self.stopped = False
        self.optparse_init()
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        self.initSettings()
        print self.options
        self.process()
        # 解析参数

    def optparse_init(self):
        """Prepare the option parser for input (argv)"""
        from optparse import OptionParser, OptionGroup
        usage = 'Usage: %prog [options] input_file(s) [output]'
        p = OptionParser(usage, version='%prog ' + __version__)
        # 绘制的区域（此处是数据进行裁剪的参数）
        p.add_option(
            '-r',
            '--plot_range',
            dest='plotRange',
            help='lat and lon range',
        )
        # 底图的区域
        p.add_option(
            '-m',
            '--map_range',
            dest='mapRange',
            help='map lat and lon range',
        )
        p.add_option(
            '--input_file',
            dest='inputfile',
            help='input file '
        )
        p.add_option(
            '-o',
            '--output_files',
            dest='outputFiles',
            help='export png/jepg etc. file',
        )
        p.add_option(
            '-c',
            '--cmp',
            dest='cmp',
            help='plot data with color',
        )

        # 刻度的开关 off/on
        p.add_option(
            '-a',
            '--axis',
            dest="axis",
            type='choice',
            choices=axis_list,
            help='plot axis'
        )
        # 实际绘制区域所占画布的比例
        p.add_option(
            '--axis_range',
            dest="axisRange",
            help='Axis plot range'
        )
        p.add_option(
            '-d',
            '--dpi',
            dest="dpi",
            help='plot dpi'
        )
        p.add_option(
            '-s',
            '--shape_file',
            dest="shapeFile",
            help='input shapefile'
        )
        p.add_option(
            '-v',
            '--view_shape',
            dest="viewShapeFile",
            help='over basemap shapefile'
        )

        p.add_option(
            '--area_id',
            dest="areaId",
            help='input areaId'
        )
        p.add_option(
            '-w',
            '--pic_weight',
            dest="picWeight",
            help='export pic weight size'
        )
        p.add_option(
            '--is_clip',
            dest="isClipData",
            type="choice",
            choices=is_clip_list,
            help='is clip source data',
        )
        p.add_option(
            '--plot_type',
            dest="plotType",
            type="choice",
            choices=plot_list,
            help='matplotlib plot type',
        )
        # colorbar 的位置[x0,y0,w,h]
        # x0代表在横轴的位置，横轴比例0-1
        # y0代表在纵轴的位置，纵轴比例0-1
        # w 代表colorbar宽度，横轴比例0-1
        # h 代表colorbar高度，纵轴比例0-1
        p.add_option(
            '--colorbar_position',
            dest="colorbarPosition",
            help="set colorbar position"
        )
        p.add_option(
            '--alpha',
            dest="alpha",
            help="set axis alpha"
        )
        p.add_option(
            '--n',
            '--normalize',
            dest="normalize",
            help="value smin,max"
        )

        p.set_defaults(
            plotType="pcolormesh",
            nodata=None,
            plotRange=None,
            mapRange=None,
            axisRange=None,
            shapeFile=None,
            viewShapeFile=None,
            areaId=None,
            colorbarPosition=None,
            cmp="jet",
            axis="off",
            dpi=80,  # 标准分辨率
            picWeight=1080,
            alpha=1.0,
            normalize=None
        )
        self.parser = p

    def initSettings(self):
        if (self.options.plotRange == None):
            pass
            # maxSourcelat = np.max(self.lat)
            # minSourcelat = np.min(self.lat)
            # maxSourcelon = np.max(self.lon)
            # minSourcelon = np.min(self.lon)
            # self.lat0 = minSourcelat
            # self.lat1 = maxSourcelat
            # self.lon0 = minSourcelon
            # self.lon1 = maxSourcelon
        else:
            (lat0, lat1, lon0, lon1) = self.options.plotRange.split(",")
            self.lat0 = float(lat0)
            self.lat1 = float(lat1)
            self.lon0 = float(lon0)
            self.lon1 = float(lon1)
        # ---------------------------------------------
        if (self.options.areaId != None):
            self.options.areaId = self.options.areaId.split(",")
        # ----------------------------------------------
        if (self.options.mapRange == None):
            self.options.mapRange = self.readAreaInfo()
        else:
            (map_lat0, map_lat1, map_lon0, map_lon1) = self.options.mapRange.split(",")
            self.options.mapRange = [float(map_lat0), float(map_lat1), float(map_lon0), float(map_lon1)]
        # ---------------------------------------------
        if (self.options.axisRange == None):
            self.options.axisRange = [0, 0, 1]
        else:
            (left, bottom, weight) = self.options.axisRange.split(",")
            self.options.axisRange = [float(left), float(bottom), float(weight)]
        # ---------------------------------------------
        if (self.options.colorbarPosition == None):
            pass
        else:
            (x0, y0, w, h) = self.options.colorbarPosition.split(",")
            self.options.colorbarPosition = [float(x0), float(y0), float(w), float(h)]
        try:
            if (self.options.dpi == None):
                self.options.dpi = 80
            else:
                self.options.dpi = int(self.options.dpi)
            self.options.picWeight = int(self.options.picWeight)
        except Exception, e:
            self.options.dpi = 80
            self.options.picWeight = 1080
        try:
            self.options.alpha = float(self.options.alpha)
        except Exception, e:
            self.options.alpha = 1.0

        colors = self.options.cmp.split(",")

        if (colors.__len__() == 1):
            pass
        elif (colors.__len__() > 1):
            # cmp = ListedColormap(colors)
            cmp = LinearSegmentedColormap.from_list('custom_colcor', colors, N=256)
            self.options.cmp = cmp
        if (self.options.normalize != None):
            self.options.normalize = self.options.normalize.split(",")
            self.norm = matplotlib.colors.Normalize(vmin=float(self.options.normalize[0]),
                                                    vmax=float(self.options.normalize[1]))
        else:
            self.norm = None

        self.options.outputFiles = self.options.outputFiles.split(",")

    def process(self):
        # self.make_base_data()
        starttime = time.time()
        self.addBaseMap(self.options.mapRange)
        print "addBaseMap time", time.time() - starttime
        starttime = time.time()
        # self.drawBaseData()
        self.drawgdalClipData()
        print "drawgdalClipData time", time.time() - starttime
        # self.simplePlot()

    # 寻找最大值除以一个值得到范围是（10，20）
    def reSize(self, x, y):
        if (x > y):
            bigger = x
        else:
            bigger = y
        levelValue = 1.0
        if (bigger <= 10):
            pass
        elif (10 < bigger < 20):
            pass
        else:
            while bigger > 20:
                levelValue = levelValue * 2
                bigger = bigger / 2.0
        return levelValue

    # 读取固定列表获取区域的信息
    def readAreaInfo(self):
        areaInfoXlsPath = "%s/um_area_info.xlsx" % sourcePath
        areaInfoWorkbook = xlrd.open_workbook(areaInfoXlsPath)
        areaInfosheet = areaInfoWorkbook.sheet_by_index(0)
        areaInfoRows = areaInfosheet.nrows
        allLeftRightTopBottom = []
        if (self.options.areaId != None):
            for areaInfoRowIndex in xrange(areaInfoRows):
                areaInfo = areaInfosheet.row_values(areaInfoRowIndex)
                for areaid in self.options.areaId:
                    if (areaid == areaInfo[2]):
                        print areaInfo[2]
                        print areaInfo[7], areaInfo[8]
                        lefttop = areaInfo[7].split(",")
                        rightbottom = areaInfo[8].split(",")
                        allLeftRightTopBottom.append(
                            [float(rightbottom[1]), float(lefttop[1]), float(lefttop[0]), float(rightbottom[0])])
            allLeftRightTopBottom = np.array(allLeftRightTopBottom)
            return (np.min(allLeftRightTopBottom[:, 0]),
                    np.max(allLeftRightTopBottom[:, 1]),
                    np.min(allLeftRightTopBottom[:, 2]),
                    np.max(allLeftRightTopBottom[:, 3]))
        else:
            # 返回内蒙区域
            return (37.24, 53.23, 97.12, 126.04)

    # ==================================================================================================
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
        parallels = np.arange(-90., 90, 10.)  # 创建纬线数组
        m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10, linewidth=0.1)  # 绘制纬线

        meridians = np.arange(0., 360., 10.)  # 创建经线数组
        m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10, linewidth=0.1)  # 绘制经线
        m.drawcoastlines(linewidth=0.5)
        m.drawstates(linewidth=0.25)
        self.fig = fig
        self.ax = ax
        self.m = m
        self.addShapeFile()

    # ============================================================================================
    def addShapeFile(self):
        if (self.options.viewShapeFile != None):
            self.m.readshapefile(self.options.viewShapeFile, 'states', drawbounds=True)
        else:
            print "no over view shapefile "

    def drawgdalClipData(self):
        if (os.path.exists(self.options.inputfile)):
            if (self.options.shapeFile != None and self.options.areaId != None):
                # cutlineWhere="qxdm LIKE '%s%s%s' " % ("%",self.options.areaId, "%")
                # cutlineWhere = "qxdm LIKE '%s%s' or qxdm LIKE '%s%s' " % ("1502", "%", "1507", "%")
                cutlineWhere = ""
                for areaid_index, areaid in enumerate(self.options.areaId):
                    cutlineWhere = cutlineWhere + "qxdm LIKE '%s%s' " % (areaid, "%")
                    if (areaid_index + 1 == self.options.areaId.__len__()):
                        pass
                    else:
                        cutlineWhere = cutlineWhere + "or "
                ds = gdal.Warp("", self.options.inputfile, format='MEM',
                               cutlineDSName=self.options.shapeFile,
                               cutlineSQL='SELECT * FROM qixian',
                               cutlineWhere=cutlineWhere,
                               dstNodata=np.nan)
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
                        self.drawMaxMinMean(band)
                else:
                    print "gdal clip error"
            else:
                print "will plot all data"
                self.openFile()
                X, Y = np.meshgrid(self.lon, self.lat)
                self.x, self.y = self.m(X, Y)
                bands = self.sourceData.shape[0]
                for band in range(bands):
                    self.data = self.sourceData[band]
                    self.drawMaxMinMean(band)
        else:
            print "%s is not exist" % self.options.inputfile

    def openFile(self):
        myOpenUtils = OpenUtils()
        myOpenUtils.initParams(
            self.options.inputfile,
            file_type="GeoTiff",
            export_type="GeoTiff",
            data_type='float32',
            is_rewirte_data=False,
            proj="mercator")
        self.lat = myOpenUtils.lats
        self.lon = myOpenUtils.lons
        self.sourceData = myOpenUtils.data
        del myOpenUtils

    # 增加或者减少一些小工具
    def addOrDeleteLittleTools(self):
        x, y = self.fig.transFigure.transform((0.9, 0.9))
        # 添加指北针
        zhinbenzhenPath = "%s/zhibeizhen.png" % sourcePath
        self.fig.figimage(plt.imread(zhinbenzhenPath), xo=x, yo=y, zorder=1000)
        # 添加比例尺
        scale = self.m.drawmapscale(115.0, 10.0, 110.5, 10.2, 1100, barstyle='fancy', units='km', zorder=20)
        # 添加文字说明
        text_x, text_y = self.m(120, 10)
        plt.text(text_x, text_y, 'Jul-24-2012')
        # 是否去掉axis的边框
        self.ax.axis(self.options.axis)  # 去掉ax画出的部分s刻度

    def drawMaxMinMean(self, band):

        if (self.options.plotType == "contourf"):
            cs = self.m.contourf(self.x, self.y, self.data, cmap=self.options.cmp, norm=self.norm,
                                 alpha=self.options.alpha)
        elif (self.options.plotType == "pcolormesh"):
            cs = self.m.pcolormesh(self.x, self.y, self.data, cmap=self.options.cmp, norm=self.norm,
                                   alpha=self.options.alpha)
        elif (self.options.plotType == "pcolor"):
            cs = self.m.pcolor(self.x, self.y, self.data, cmap=self.options.cmp, norm=self.norm,
                               alpha=self.options.alpha)
        if (self.options.colorbarPosition != None):
            cax2 = self.fig.add_axes(self.options.colorbarPosition)  # 这块会影响绘制效率
            plt.colorbar(cs, cax=cax2, orientation='vertical')

        self.fig.savefig(self.options.outputFiles[band], format='png', transparent=False, dpi=self.options.dpi,
                         pad_inches=0)
        plt.close()

    def stop(self):
        self.stopped = True


if __name__ == '__main__':
    startTime = time.time()
    argv = sys.argv
    if argv:
        myPlotUtils = PlotUtils()
        myPlotUtils.outsideParams(argv[1:])
        print "end time ", time.time() - startTime

        # 之前用maskout借助shapefile 做裁剪方式
        # def drawBaseData(self):
        #     if (self.options.shapeFile != None):
        #         if (os.path.exists(self.options.shapeFile + ".shp")):
        #             self.m.readshapefile(self.options.shapeFile, 'states')
        #         else:
        #             print "%s is not exist" % self.options.shapeFile
        #             self.stop()
        #     else:
        #         print "no shapefile"
        #     if (not self.stopped):
        #         self.data = self.sourceData[0]
        #         X, Y = np.meshgrid(self.lon, self.lat)
        #         x, y = self.m(X, Y)
        #         if (self.options.plotType == "contourf"):
        #             cs = self.m.contourf(x, y, self.data, cmap=self.options.cmp, alpha=self.options.alpha)
        #         elif (self.options.plotType == "pcolormesh"):
        #             cs = self.m.pcolormesh(x, y, self.data, cmap=self.options.cmp, alpha=self.options.alpha)
        #         elif (self.options.plotType == "pcolor"):
        #             cs = self.m.pcolor(x, y, self.data, cmap=self.options.cmp, alpha=self.options.alpha)
        #         if (self.options.colorbarPosition != "None"):
        #             cax2 = self.fig.add_axes(self.options.colorbarPosition)
        #             cbar = plt.colorbar(cs, cax=cax2, orientation='vertical')
        #         # plt.axis(self.options.axis)  #整个画布去掉刻度去掉刻度
        #         self.ax.axis(self.options.axis)  # 去掉ax画出的部分的刻度
        #         # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)  # 去掉边框
        #         # plt.margins(0, 0)
        #         if (self.options.isClipData == "True" and self.options.shapeFile != None):  # 是否裁剪数据
        #             if (self.options.areaId != None):
        #                 self.options.areaId = self.options.areaId.split(",")
        #                 maskout.shp2clip2(cs, self.ax, self.m, self.options.shapeFile, self.options.areaId)
        #
        #         self.fig.savefig(self.options.outputFiles, format='png', transparent=False, dpi=self.options.dpi,
        #                          pad_inches=0)
        #         plt.close()
        # ==============================================================
        # def make_base_data(self):
        #         self.clipData()
        # def clipData(self):
        #     try:
        #         maxSourcelat = np.max(self.lat)
        #         minSourcelat = np.min(self.lat)
        #         maxSourcelon = np.max(self.lon)
        #         minSourcelon = np.min(self.lon)
        #
        #         print "latlon", self.lat0, self.lat1, self.lon0, self.lon1
        #         if (maxSourcelat >= self.lat0 >= minSourcelat \
        #                     and minSourcelat <= self.lat1 <= maxSourcelat \
        #                     and maxSourcelon >= self.lon0 >= minSourcelon \
        #                     and minSourcelon <= self.lon1 <= maxSourcelon):
        #             (index_Y1, index_Y0) = self.getYIndex(self.lat0, self.lat1, self.lat)
        #             (index_X0, index_X1) = self.getXIndex(self.lon0, self.lon1, self.lon)
        #             self.sourceData = self.sourceData[:, index_Y1:index_Y0, index_X0:index_X1]  # 裁剪之后的数据
        #             self.data = self.sourceData[0]  # 裁剪之后的数据
        #             print "1", self.sourceData.shape
        #             print "lat or lon range is ok"
        #         else:
        #             print "2", self.sourceData.shape
        #             print "lat or lon range is error"
        #     except Exception, e:
        #         print e.message
        #         print "make base data error"
        #         self.stop()
        # ===================================================================================================

        # def getYIndex(self, currentYValue0, currentYValue1, allYValue):
        #     index_Y0 = 0
        #     index_Y1 = 0
        #     for allValueYIndex in allYValue:
        #         if (currentYValue0 >= allValueYIndex):
        #             pass
        #         else:
        #             index_Y0 = index_Y0 + 1
        #         if (currentYValue1 >= allValueYIndex):
        #             pass
        #         else:
        #             index_Y1 = index_Y1 + 1
        #     self.lat = allYValue[index_Y1: index_Y0 + 1]
        #     return (index_Y1, index_Y0 + 1)
        #
        # def getXIndex(self, currentXValue0, currentXValue1, allXValue):
        #     index_X0 = 0
        #     index_X1 = 0
        #     for allValueXIndex in allXValue:
        #         if (currentXValue0 >= allValueXIndex):
        #             pass
        #         else:
        #             index_X0 = index_X0 + 1
        #         if (currentXValue1 >= allValueXIndex):
        #             pass
        #         else:
        #             index_X1 = index_X1 + 1
        #     self.lon = allXValue[len(allXValue) - 1 - index_X0: len(allXValue) - 1 - index_X1 + 1]
        #     return (len(allXValue) - 1 - index_X0, len(allXValue) - 1 - index_X1 + 1)
