from umOpener.openUtils import OpenUtils

from plotUtils import PlotUtils
import time
import numpy as np


def tif2tif():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.tif",
        # "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701100048_P_CLDAS_RT_ASI_0P0625_HOR-PRE-2018070109.tif",
        # "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701102332_P_CLDAS_RT_ASI_0P0625_HOR-SM000005-2018070109.tif",
        file_type="GeoTiff",
        out_file="./tif2tif.tif",
        export_type="GeoTiff",
        data_type='float32',
        lat_order="asc",
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "PAIR"],
        is_rewirte_data=False,
        proj="mercator")

    return (myOpenUtils.lats, myOpenUtils.lons, myOpenUtils.data)


def plot(lat, lon, data):
    myPlotUtils = PlotUtils()
    lat = np.asarray(lat)
    # myPlotUtils.initParams(lat, lon, data, plot_range="all,all,all,all",
    #                        map_range="all,all,all,all", axis_range="0.05,0.05,0.9",
    #                        output_file="./export_contourf.png",
    #                        shape_file="/Users/lhtd_01/Downloads/gn_pyserver_py/um_pyserver_fy/statics/map/wgs_84_gbk/qixian_gbk",
    #                        area_id="152921000000", axis="off", is_clip="False",
    #                        cmp='red', dpi=80, is_open_colorbar="False", colorbar_position="0.9,0.1,0.03,0.5")
    myPlotUtils.initParams(lat, lon, data,
                           output_file="./export.png",
                           # shape_file="/Users/lhtd_01/Downloads/gn_pyserver_py/um_pyserver_fy/statics/map/wgs_84_gbk/qixian_gbk",
                           area_id="152921000000",
                           axis="off",
                           is_clip="False",
                           pic_weight="1000",
                           plot_type="pcolormesh",
                           cmp='binary',
                           dpi="80",
                           colorbar_position="0.95,0.0,0.01,0.25",
                           plot_range="37.24,54,97.12,127",
                           map_range="37.24,54,97.12,127",
                           axis_range="0.0,0.0,1")


if __name__ == '__main__':
    startTime = time.time()
    (lat, lon, data) = tif2tif()
    print "read: %s" % str(time.time() - startTime)
    plot(lat, lon, data)
    print "time: %s" % str(time.time() - startTime)
