# umplot 绘图库
## 运行环境
* python 版本 2.7

## 依赖库
* matplotlib 版本：2.2.2
* numpy 版本：1.15.3
* mpl_toolkits(basemap) 版本：1.1.0
* umOpener 版本：0.0.9 

## 参数说明(标*为必须传入)
* ***input_file** 输入文件（支持tif和img）
* ***output_files** 输出文件 多个可以用","隔开
* ***shape_file** gdal矢量裁剪依据的模板shape文件
* area_id 需要裁剪的区域id多个可以用","隔开 例"1507,1502,1509,1506,1529,150424" 默认全部数据
  (注意! shape_file 输入 area_id可以不输入，area_id 输入shape_file必须输入）
* view_shape 覆盖一层shape文件
* axis 刻度开关（off,on）默认off
* pic_weight 生成图片宽度 默认1080
* plot_type 绘制方式("contourf", "pcolormesh", "pcolor") 默认pcolormesh
* alpha 透明度 默认1.0
* cmp 渲染色卡（matplotlib 提供参数，自行查找其他值）默认"jet",可以使用'#ffffe5,#90ee90,#008ae5'
* dpi 输出图片dpi (默认80)
* colorbar_position 色卡图例位置"a,b,c,d"(a:左起点，在画布X轴方向比例值（0-1）b:下起点，在画布Y轴方向比例值（0-1) 
    c:色卡宽度，在画布X轴方向比例值（0-1）d:色卡的高度，在画布Y轴方向比例值（0-1))
* plot_range 输入数据区域"lat0,lat1,lon0,lon1"，根据区域进行绘制前裁剪，默认输入数据（lat,lon）最大区域
* map_range 底图绘制区域"lat0,lat1,lon0,lon1" 默认和输入数据区域相同
* axis_range 画笔axis 位置 "a,b,c"（a:左起点，在画布X轴方向比例值（0-1),b:下起点，在画布Y轴方向比例值（0-1),c:宽度，在画布X轴方向比例值（0-1））默认"0.0,0.0,1.0"
* normalize 绘制数据阈值 默认None

## 示例
```
    myPlotUtils = PlotUtils()
    myPlotUtils.initParams(
        input_file="/Volumes/pioneer/gdal_Demo/cldas_nrt_day/2018/12_tif/Z_NAFP_C_BABJ_20181203230448_P_CLDAS_NRT_ASI_0P0625_DAY-TMP-2018120100.tif",
        output_files="./export_min.png,./export_max.png,./export_mean.png",
        shape_file="/Users/lhtd_01/Downloads/oschina/um_fy3_znoal/fy3/shp/qixian.shp",
        area_id="1507,1502,1509,1506,1529,150424",
        # view_shape="/Volumes/pioneer/pipDemo/umplot/umplots/source/qixian_WGS84",
        # axis="on",
        # pic_weight="1000",
        # plot_type="contourf",
        # plot_type="pcolormesh",
        # plot_type="pcolor",
        # alpha="1.0",
        # cmp='jet',
        # cmp='#ffffe5,#90ee90,#008ae5',
        # dpi="80",
        # colorbar_position="0.9,0.01,0.01,0.25",
        # plot_range="30,40,80,90",
        # map_range="0,60,70,140",
        # axis_range="0.05,0.05,0.9",
        # normalize="0,400",
    )
```

## 外部调用参数说明(标*为必须传入)
* ***--input_file** 输入文件（支持tif和img）
* ***--output_files** 输出文件 多个可以用","隔开
* ***--shape_file** gdal矢量裁剪依据的模板shape文件
* --area_id 需要裁剪的区域id多个可以用","隔开 例"1507,1502,1509,1506,1529,150424" 默认全部数据
  (注意! shape_file 输入 area_id可以不输入，area_id 输入shape_file必须输入）
* --view_shape 覆盖一层shape文件
* --axis 刻度开关（off,on）默认off
* --pic_weight 生成图片宽度 默认1080
* --plot_type 绘制方式("contourf", "pcolormesh", "pcolor") 默认pcolormesh
* --alpha 透明度 默认1.0
* --cmp 渲染色卡（matplotlib 提供参数，自行查找其他值）默认"jet",可以使用'#ffffe5,#90ee90,#008ae5'
* --dpi 输出图片dpi (默认80)
* --colorbar_position 色卡图例位置"a,b,c,d"(a:左起点，在画布X轴方向比例值（0-1）b:下起点，在画布Y轴方向比例值（0-1) 
    c:色卡宽度，在画布X轴方向比例值（0-1）d:色卡的高度，在画布Y轴方向比例值（0-1))
* --plot_range 输入数据区域"lat0,lat1,lon0,lon1"，根据区域进行绘制前裁剪，默认输入数据（lat,lon）最大区域
* --map_range 底图绘制区域"lat0,lat1,lon0,lon1" 默认和输入数据区域相同
* --axis_range 画笔axis 位置 "a,b,c"（a:左起点，在画布X轴方向比例值（0-1),b:下起点，在画布Y轴方向比例值（0-1),c:宽度，在画布X轴方向比例值（0-1））默认"0.0,0.0,1.0"
* --normalize 绘制数据阈值 默认None

## 示例
```
python plotUtils.py --input_file /Volumes/pioneer/gdal_Demo/cldas_nrt_day/2018/12_tif/Z_NAFP_C_BABJ_20181203230448_P_CLDAS_NRT_ASI_0P0625_DAY-TMP-2018120100.tif \
                    --output_files ./export_min.png,./export_max.png,./export_mean.png
```