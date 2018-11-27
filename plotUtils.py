# -*- coding:utf-8 -*-
__version__ = '$Id: plotUtils.py 27349 2018-111-27 18:58:51Z rouault $'
import matplotlib.pyplot as plt
import numpy as np


class PlotUtils():
    def __init__(self):
        print "__init__"

    # 初始化
    def initParams(self, lat, lon, data, **kwgs):
        print kwgs
        self.stopped = False
        self.optparse_init()
        self.lat = lat
        self.lon = lon
        self.sourceData = data
        arguments = []
        for kwarg_key in kwgs.keys():
            arguments.append("--%s" % kwarg_key)
            arguments.append(kwgs[kwarg_key])
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        print self.options
        self.process()

    # 解析参数
    def optparse_init(self):
        """Prepare the option parser for input (argv)"""
        from optparse import OptionParser, OptionGroup
        usage = 'Usage: %prog [options] input_file(s) [output]'
        p = OptionParser(usage, version='%prog ' + __version__)
        p.add_option(
            '-r',
            '--plot_range',
            dest='plotRange',
            help='lat and lon range',
        )
        p.add_option(
            '-o',
            '--output_file',
            dest='outputFile',
            help='export png/jepg etc. file',
        )
        p.add_option(
            '-c',
            '--cmp',
            dest='cmp',
            help='plot data with color',
        )
        p.add_option(
            '--is_open_colorbar',
            dest="isOpenColorBar",
            help='plot have or not have colorbar'
        )
        # 刻度的开关 off/on
        p.add_option(
            '-a',
            '--axis',
            dest="axis",
            help='plot axis'
        )
        p.add_option(
            '-d',
            '--dpi',
            dest="dpi",
            help='plot dpi'
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
        p.set_defaults(
            latOrder="asc",
            dataOrder="asc",
            nodata=None,
            cmp="jet",
            isOpenColorBar=False,
            axis="off",
            dpi=80,  # 标准分辨率
        )
        self.parser = p

    def process(self):
        self.plot()
        self.simplePlot()

    def simplePlot(self):
        if (not self.stopped):
            self.clipData()
            (z, y, x) = self.sourceData.shape
            levelValue = self.reSize(x, y)
            print x / levelValue, y / levelValue
            self.fig = plt.figure(figsize=(x / levelValue, y / levelValue))
            ax = self.fig.add_subplot(1, 1, 1)
            cs = ax.imshow(self.sourceData[0], cmap="jet")
            if (self.options.isOpenColorBar):
                cax2 = self.fig.add_axes(self.options.colorbarPosition)
                cbar = plt.colorbar(cs, cax=cax2, orientation='vertical')
            plt.axis(self.options.axis)  # 去掉刻度
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)  # 去掉边框
            plt.margins(0, 0)
            self.fig.savefig(self.options.outputFile, format='png', transparent=True, dpi=self.options.dpi,
                             pad_inches=0)
            plt.close()

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

    def clipData(self):
        try:
            (lat0, lat1, lon0, lon1) = self.options.plotRange
            print lat0, lat1, lon0, lon1
            maxSourcelat = np.max(self.lat)
            minSourcelat = np.min(self.lat)
            maxSourcelon = np.max(self.lon)
            minSourcelon = np.min(self.lon)
            if (lat0 == "all"):
                lat0 = minSourcelat
            if (lat1 == "all"):
                lat1 = maxSourcelat
            if (lon0 == "all"):
                lon0 = minSourcelon
            if (lon1 == "all"):
                lon1 = maxSourcelon
            print lat0, lat1, lon0, lon1

            if (maxSourcelat >= lat0 >= minSourcelat \
                        and minSourcelat <= lat1 <= maxSourcelat \
                        and maxSourcelon >= lon0 >= minSourcelon \
                        and minSourcelon <= lon1 <= maxSourcelon):
                (index_Y1, index_Y0) = self.getYIndex(lat0, lat1, self.lat)
                (index_X0, index_X1) = self.getXIndex(lon0, lon1, self.lon)
                print (index_Y1, index_Y0)
                print (index_X0, index_X1)
                # print self.lat
                print "0", self.sourceData.shape
                self.sourceData = self.sourceData[:, index_Y1:index_Y0 + 1, index_X0:index_X1 + 1]  # 裁剪之后的数据
                print "1", self.sourceData.shape
                print "lat or lon range is ok"
            else:
                print self.sourceData.shape
                print "lat or lon range is error"
        except Exception, e:
            self.stop()

    # ===================================================================================================

    def getYIndex(self, currentYValue0, currentYValue1, allYValue):
        index_Y0 = 0
        index_Y1 = 0
        print "---", currentYValue0, currentYValue1
        for allValueYIndex in allYValue:
            if (currentYValue0 >= allValueYIndex):
                pass
            else:
                index_Y0 = index_Y0 + 1
            if (currentYValue1 >= allValueYIndex):
                pass
            else:
                index_Y1 = index_Y1 + 1
        self.lat = allYValue[index_Y1: index_Y0]
        return (index_Y1, index_Y0)

    def getXIndex(self, currentXValue0, currentXValue1, allXValue):
        index_X0 = 0
        index_X1 = 0
        print currentXValue0, currentXValue1
        for allValueXIndex in allXValue:
            if (currentXValue0 >= allValueXIndex):
                pass
            else:
                index_X0 = index_X0 + 1
            if (currentXValue1 >= allValueXIndex):
                pass
            else:
                index_X1 = index_X1 + 1
        self.lon = allXValue[len(allXValue) - 1 - index_X0: len(allXValue) - 1 - index_X1]
        return (len(allXValue) - 1 - index_X0, len(allXValue) - 1 - index_X1)

    # ==================================================================================================
    def stop(self):
        self.stopped = True

    def plot(self):
        pass
