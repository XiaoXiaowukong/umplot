# -*- coding:utf-8 -*-
import shapefile
import os
import numpy as np
import xlrd
import xlwt


class ReadShapeFile():
    def __init__(self):
        pass

    def readShapeFile(self, shpfile):
        sf = shapefile.Reader(shpfile)
        for index, shape_rec in enumerate(sf.shapeRecords()):
            xian_code = shape_rec.record[3]
            areaAllPoints = np.asarray(shape_rec.shape.points)
            areaAllPoints = np.array(areaAllPoints)
            lon0 = str(float(np.min(areaAllPoints[:, 0])))
            lon1 = str(float(np.max(areaAllPoints[:, 0])))
            lat0 = str(float(np.min(areaAllPoints[:, 1])))
            lat1 = str(float(np.max(areaAllPoints[:, 1])))
            lefttop = lon0 + "," + lat1
            rightbottom = lon1 + "," + lat0
            if (xian_code in self.areaDic.keys()):
                if (xian_code[:4] in self.areaDic.keys()):
                    pass
                else:
                    self.areaDic[xian_code[:4]] = ["", self.areaDic[xian_code][1],
                                                   self.areaDic[xian_code][2], self.areaDic[xian_code][3],
                                                   self.areaDic[xian_code][4], self.areaDic[xian_code][5]]
                if (xian_code[:2] in self.areaDic.keys()):
                    pass
                else:
                    self.areaDic[xian_code[:2]] = ["", "", "", self.areaDic[xian_code][3],
                                                   self.areaDic[xian_code][4], self.areaDic[xian_code][5]]
                self.areaDic[xian_code].append(lefttop)
                self.areaDic[xian_code].append(rightbottom)
            else:
                if (xian_code != "0"):
                    print "xian_code is not exist", xian_code
                    break
                else:
                    print "xian_code is", xian_code

    def readstatxls(self, statxls):
        if (os.path.exists(statxls)):
            areaBook = xlrd.open_workbook(statxls)
            areaSheet = areaBook.sheet_by_index(0)  # 或用名称取sheet
            self.areaDic = {}
            for index in range(1, areaSheet.nrows, 1):
                self.areaDic["%s" % areaSheet.row_values(index)[0]] = [areaSheet.row_values(index)[1],
                                                                       areaSheet.row_values(index)[2],
                                                                       areaSheet.row_values(index)[3],
                                                                       areaSheet.row_values(index)[4],
                                                                       areaSheet.row_values(index)[5],
                                                                       areaSheet.row_values(index)[6]]
            del areaBook
        else:
            print "%s is not exist" % statxls

    def wirteAreaInfoXls(self, exportFile):
        f = xlwt.Workbook('utf-8', 'writeBook')  # 创建工作簿
        sheetBase = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
        rowHead = [u'bianma_xian', u'县名称', u'bianma_shi', u'市名称', u'bianma_sheng', u'省名称', u'国家', u'lefttop',
                   u'rightbottom']
        # 生成第一行
        for i, title in enumerate(rowHead):
            sheetBase.write(0, i, title)
        allkeys = self.areaDic.keys()
        allkeys.sort()
        for areaDicinfoIndex, areaKey in enumerate(allkeys):
            if (areaKey.__len__() == 2):
                print "-------", areaKey
                palllons = []
                palllats = []
                for pAreaIdex, pAreaKey in enumerate(allkeys):
                    if (pAreaKey.__len__() == 6 and pAreaKey[:2] == areaKey):
                        print "=====", pAreaKey
                        palllons.append(float(self.areaDic[pAreaKey][6].split(",")[0]))
                        palllons.append(float(self.areaDic[pAreaKey][7].split(",")[0]))
                        palllats.append(float(self.areaDic[pAreaKey][6].split(",")[1]))
                        palllats.append(float(self.areaDic[pAreaKey][7].split(",")[1]))
                # print palllats
                # print palllons
                if (palllats.__len__() != 0 and palllons.__len__() != 0):
                    pLeftTop = str(float(np.min(palllons))) + "," + str(float(np.max(palllats)))
                    pRightBottom = str(float(np.max(palllons))) + "," + str(float(np.min(palllats)))
                    self.areaDic[areaKey].append(pLeftTop)
                    self.areaDic[areaKey].append(pRightBottom)
            elif (areaKey.__len__() == 4):
                print "-------", areaKey
                salllons = []
                salllats = []
                for sAreaIdex, sAreaKey in enumerate(allkeys):
                    if (sAreaKey.__len__() == 6 and sAreaKey[:4] == areaKey):
                        print "=====", sAreaKey
                        salllons.append(float(self.areaDic[sAreaKey][6].split(",")[0]))
                        salllons.append(float(self.areaDic[sAreaKey][7].split(",")[0]))
                        salllats.append(float(self.areaDic[sAreaKey][6].split(",")[1]))
                        salllats.append(float(self.areaDic[sAreaKey][7].split(",")[1]))
                # print "salllats",salllats
                # print "salllons",salllons
                if (salllats.__len__() != 0 and salllons.__len__() != 0):
                    sLeftTop = str(float(np.min(salllons))) + "," + str(float(np.max(salllats)))
                    sRightBottom = str(float(np.max(salllons))) + "," + str(float(np.min(salllats)))
                    self.areaDic[areaKey].append(sLeftTop)
                    self.areaDic[areaKey].append(sRightBottom)
            sheetBase.write(areaDicinfoIndex + 1, 0, areaKey)
            for areaDicinfosIndex, areaDicinfo in enumerate(self.areaDic[areaKey]):
                sheetBase.write(areaDicinfoIndex + 1, areaDicinfosIndex + 1, areaDicinfo)
        f.save(exportFile)  # 保存文件
        del f


if __name__ == '__main__':
    shpfile = "/Volumes/pioneer/pipDemo/umplot/umplots/source/hebing.shp"
    # shpfile = "/Volumes/pioneer/pipDemo/umplot/umplots/source/qixian_WGS84.shp"
    statxls = "/Volumes/pioneer/pipDemo/umplot/umplots/source/hebing.xls"
    myReadShapeFile = ReadShapeFile()
    myReadShapeFile.readstatxls(statxls)
    if (os.path.exists(shpfile)):
        myReadShapeFile.readShapeFile(shpfile)
    else:
        print "%s is not exist" % shpfile
    print myReadShapeFile.areaDic["11"]
    print myReadShapeFile.areaDic["1101"]
    print myReadShapeFile.areaDic["110100"]
    exportFile = "./source/area_all_info.xls"
    myReadShapeFile.wirteAreaInfoXls(exportFile)
