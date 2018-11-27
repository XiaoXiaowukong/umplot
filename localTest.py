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
    lat0 = "all"
    lat1 = "all"
    lon0 = "all"
    lon1 = "all"
    myPlotUtils.initParams(lat, lon, data, plot_range=[lat0, lat1, lon0, lon1],
                           output_file="./export.png",
                           cmp='red', is_open_colorbar=True, dpi=80, colorbar_position=[0.9, 0.0, 0.05 / 3, 1])


if __name__ == '__main__':
    startTime = time.time()
    (lat, lon, data) = tif2tif()
    print "read: %s" % str(time.time() - startTime)
    plot(lat, lon, data)
    print "time: %s" % str(time.time() - startTime)
