
from plotUtils import PlotUtils
import time


def plot():
    myPlotUtils = PlotUtils()
    myPlotUtils.initParams(
        # "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.tif",
        "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.tif",
        output_file="./export.png",
        shape_file="/Users/lhtd_01/Downloads/oschina/um_fy3_znoal/fy3/shp/qixian.shp",
        area_id="1507",
        # area_id="None",
        axis="off",
        is_clip="False",
        pic_weight="1000",
        # plot_type="contourf",
        plot_type="pcolormesh",
        # plot_type="pcolor",
        alpha="1.0",
        # cmp='jet',
        cmp='#ffffe5,#90ee90,#008ae5',
        dpi="80",
        colorbar_position="0.9,0.01,0.01,0.25",
        plot_range="0,60,70,140",
        map_range="0,60,70,140",
        axis_range="0.0,0.0,1")


if __name__ == '__main__':
    startTime = time.time()
    plot()
    print "time: %s" % str(time.time() - startTime)
