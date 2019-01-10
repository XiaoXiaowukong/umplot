# -*- coding:utf-8 -*-
from plotUtils import PlotUtils
import time


def plot():
    myPlotUtils = PlotUtils()
    myPlotUtils.initParams(
        # input_file="/Volumes/pioneer/gdal_Demo_内蒙三维数据/cmcast/cldas_nrt_tif/2018/12/20181201/Z_NAFP_C_BABJ_20181203000812_P_CLDAS_NRT_CHN_0P0625_HOR-RSM000010-2018120100.tif",
        input_file="/Volumes/pioneer/gdal_Demo_内蒙三维数据/cmcast/cldas_nrt_tif/2018/12/20181201/mean.tif,/Volumes/pioneer/gdal_Demo_内蒙三维数据/cmcast/cldas_nrt_tif/2018/12/20181201/max.tif,/Volumes/pioneer/gdal_Demo_内蒙三维数据/cmcast/cldas_nrt_tif/2018/12/20181201/min.tif",
        output_files="./MEAN.png,./MAX.png,./MIN.png",
        # area_id="62",
        # area_id="231123",
        area_id="61,62,63,64,13,14,15",
        view_shape="/Volumes/pioneer/pipDemo/umplot/umplots/source/qixian_WGS84",
        # axis="on",
        # is_clip="False",
        # pic_weight="1000",
        # plot_type="contourf",
        plot_type="pcolormesh",
        # plot_type="pcolor",
        # alpha="1.0",
        # cmp='jet',
        cmap='#ffffe5,#90ee90,#008ae5,#ffff00',
        # dpi="80",
        colorbar_position="0.9,0.01,0.01,0.25",
        # plot_range="30,40,80,90",
        # map_range="0,60,70,140",
        axis_range="0.05,0.05,0.9",
        # normalize="0,400",
        levels="60,85,90"
    )
    myPlotUtils.process()


if __name__ == '__main__':
    startTime = time.time()
    plot()
    print "time: %s" % str(time.time() - startTime)
