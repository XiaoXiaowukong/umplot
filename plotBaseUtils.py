# -*- coding:utf-8 -*-
__version__ = '$Id: plotBaseUtils.py 27349 2018-111-27 18:58:51Z rouault $'

import os
import matplotlib

sourceDIRPath = "%s/source" % os.path.dirname(os.path.abspath(__file__))
defaultShapeFile = "%s/hebing.shp" % sourceDIRPath
axis_list = ("on", "off")
is_clip_list = ("True", "False")
plot_list = ("contourf", "pcolormesh", "pcolor")


class PlotBaseUtils():
    def __init__(self):
        pass

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

    def outsideParams(self, arguments):
        self.stopped = False
        self.optparse_init()
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        self.initSettings()
        print self.options

    def optparse_init(self):
        """Prepare the option parser for input (argv)"""
        from optparse import OptionParser, OptionGroup
        usage = 'Usage: %prog [options] input_file(s) [output]'
        p = OptionParser(usage, version='%prog ' + __version__)
        # 底图的区域
        p.add_option(
            '-m',
            '--map_range',
            dest='mapRange',
            help='map lat and lon range',
        )
        p.add_option(
            '--input_files',
            dest='inputfiles',
            help='input files '
        )
        p.add_option(
            '-o',
            '--output_files',
            dest='outputFiles',
            help='export png/jepg etc. file',
        )
        p.add_option(
            '-c',
            '--cmap',
            dest='cmap',
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
            dest="isClip",
            type="choice",
            choices=is_clip_list,
            help='is clip source tif',
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
        p.add_option(
            '-l',
            '--levels',
            dest="levels",
            help="set data plot level"
        )
        p.add_option(
            '--company_name',
            dest='companyName',
            help='company name str'

        )
        p.set_defaults(
            plotType="pcolormesh",
            nodata=None,
            plotRange=None,
            mapRange=None,
            axisRange=None,
            shapeFile=defaultShapeFile,
            viewShapeFile=None,
            areaId=None,  # 默认全内蒙
            colorbarPosition=None,
            cmap="jet",
            axis="on",
            dpi=80,  # 标准分辨率
            picWeight=1080,
            alpha=1.0,
            normalize=None,
            levels=None,
            isClip="True",
            companyName="制作单位：内蒙古生态与农业气象中心"
        )
        self.parser = p

    def initSettings(self):
        # 指标等级
        if (self.options.levels != None):
            self.options.levels = self.options.levels.split(",")
        # 输入文件分割
        if (self.options.inputfiles != None):
            self.options.inputfiles = self.options.inputfiles.split(",")
        # 选择区域
        if (self.options.areaId != None):
            self.options.areaId = self.options.areaId.split(",")
        # basemap展示区域
        if (self.options.mapRange == None):
            self.options.mapRange = self.readAreaInfo()
        else:
            (map_lat0, map_lat1, map_lon0, map_lon1) = self.options.mapRange.split(",")
            self.options.mapRange = [float(map_lat0), float(map_lat1), float(map_lon0), float(map_lon1)]
        # 绘制区域所占画布区域比例
        if (self.options.axisRange == None):
            self.options.axisRange = [0, 0, 1]
        else:
            (left, bottom, weight) = self.options.axisRange.split(",")
            self.options.axisRange = [float(left), float(bottom), float(weight)]
        # colorbar在画布的区域比例
        if (self.options.colorbarPosition == None):
            pass
        else:
            (x0, y0, w, h) = self.options.colorbarPosition.split(",")
            self.options.colorbarPosition = [float(x0), float(y0), float(w), float(h)]
        # 绘图分辨率
        try:
            if (self.options.dpi == None):
                self.options.dpi = 80
            else:
                self.options.dpi = int(self.options.dpi)
            # 绘图的宽度
            self.options.picWeight = int(self.options.picWeight)
        except Exception, e:
            self.options.dpi = 80
            self.options.picWeight = 1080
        # 绘图的透明度
        try:
            self.options.alpha = float(self.options.alpha)
        except Exception, e:
            self.options.alpha = 1.0
        self.options.cmap = self.options.cmap.split(",")
        print self.options.cmap

        # 设置绘制数据的数值范围
        if (self.options.normalize != None):
            self.options.normalize = self.options.normalize.split(",")
            self.options.normalize = matplotlib.colors.Normalize(vmin=float(self.options.normalize[0]),
                                                                 vmax=float(self.options.normalize[1]))
        else:
            self.options.normalize = None
        # 输出文件分割
        if (self.options.outputFiles != None):
            self.options.outputFiles = self.options.outputFiles.split(",")
