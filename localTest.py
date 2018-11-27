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
    lat0 = 49.7
    lat1 = 50
    lon0 = 70
    lon1 = "all"
    # print np.max(lat)
    # print np.min(lat)
    # print np.max(lon)
    # print np.min(lon)
    myPlotUtils.initParams(lat, lon, data, plot_range=[lat0, lat1, lon0, lon1],
                           output_file="./export.jpeg",
                           cmp='red', is_open_colorbar=False, dpi=40)


if __name__ == '__main__':
    startTime = time.time()
    (lat, lon, data) = tif2tif()
    print lat
    print lon
    print data
    plot(lat, lon, data)
    print "time: %s" % str(time.time() - startTime)
