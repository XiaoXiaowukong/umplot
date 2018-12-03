# coding=utf-8
###################################################################################################################################
#####This module enables you to maskout the unneccessary data outside the interest region on a matplotlib-plotted output instance
####################in an effecient way,You can use this script for free     ########################################################
#####################################################################################################################################
#####USAGE: INPUT  include           'originfig':the matplotlib instance##
#                                    'ax': the Axes instance
#                                    'm': the Basemap instance
#                                    'shapefile': the shape file used for generating a basemap A
#                                    'region':the name of a region of on the basemap A,outside the region the data is to be maskout
#           OUTPUT    is             'clip' :the the masked-out or clipped matplotlib instance.
import shapefile
from matplotlib.path import Path
from matplotlib.patches import PathPatch


def shp2clip(originfig, ax, m, shpfile, region):
    sf = shapefile.Reader(shpfile)
    vertices = []
    codes = []
    for shape_rec in sf.shapeRecords():
        ####这里需要找到和region匹配的唯一标识符，record[]中必有一项是对应的。
        # if shape_rec.record[3] == region:   #####在country1.shp上，对中国以外的其他国家或地区进行maskout
        if shape_rec.record[4] in region:  #####在bou2_4p.shp上，对中国的某几个省份或地区之外的部分进行maskout
            pts = shape_rec.shape.points
            prt = list(shape_rec.shape.parts) + [len(pts)]
            for i in range(len(prt) - 1):
                for j in range(prt[i], prt[i + 1]):
                    vertices.append(m(pts[j][0], pts[j][1]))
                codes += [Path.MOVETO]
                codes += [Path.LINETO] * (prt[i + 1] - prt[i] - 2)
                codes += [Path.CLOSEPOLY]
            clip = Path(vertices, codes)
            clip = PathPatch(clip, transform=ax.transData)
    for contour in originfig.collections:
        contour.set_clip_path(clip)
    return clip


def shp2clip2(originfig, ax, m, shpfile, shpId):
    sf = shapefile.Reader(shpfile)
    vertices = []
    codes = []
    print "shpId", shpId
    for shape_rec in sf.shapeRecords():
        ####这里需要找到和region匹配的唯一标识符，record[]中必有一项是对应的。
        # if shape_rec.record[0] == cityId:  #####在country1.shp上，对中国以外的其他国家或地区进行maskout
        # print "裁剪", str(shape_rec.record[1])

        if str(shape_rec.record[1]) in shpId:  #####在bou2_4p.shp上，对中国的某几个省份或地区之外的部分进行maskout
            print "裁剪===", shape_rec.record[1]
            name = shape_rec.record[2]
            pts = shape_rec.shape.points
            prt = list(shape_rec.shape.parts) + [len(pts)]
            for i in range(len(prt) - 1):
                for j in range(prt[i], prt[i + 1]):
                    vertices.append(m(pts[j][0], pts[j][1]))
                codes += [Path.MOVETO]
                codes += [Path.LINETO] * (prt[i + 1] - prt[i] - 2)
                codes += [Path.CLOSEPOLY]
            clip = Path(vertices, codes)
            clip = PathPatch(clip, transform=ax.transData)
    try:
        for contour in originfig.collections:
            contour.set_clip_path(clip)
    except Exception, e:
        originfig.set_clip_path(clip)
        # for contour in originfig:
        #     contour.set_clip_path(clip)
