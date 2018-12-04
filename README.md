# umplot
## 基础配置
* matplotlib
* numpy
* mpl_toolkits(basemap)

## 使用说明(除lat,lon,data,其他参数值都为string类型。除lat,lon,data必须按顺序写到参数集最前，其他可以不按顺序。传入标*为必须传入)
* *1.lat 一维维度（从高到低）
* *2.lon 一维经度（从低到高）
* *3.data 三维数据（1,xx,xx）
* *4.output_file 输出文件（xx.png/xx.jpeg）
* 5.plot_type 绘制方式("contourf", "pcolormesh", "pcolor") 默认contourf
* 5.shape_file 需要绘制的shape文件
* 6.area_id 需要裁剪的区域（和shape文件绑定，利用shape文件里面的区域值来确定）
* 注意! shape_file 输入 area_id可以不输入，area_id 输入shape_file必须输入
* 7.is_clip 是否裁剪区域（True/False）
* 8.axis （on/off）是否关闭刻度
* 9.pic_weight 输出图片宽度（默认1080）
* 10.cmp 渲染色卡（matplotlib 提供参数，自行查找其他值）
* 11.dpi 输出图片dpi (默认80)
* 12.colorbar_position 色卡图例位置"a,b,c,d"(a:左起点，在画布X轴方向比例值（0-1）b:下起点，在画布Y轴方向比例值（0-1) c:色卡宽度，在画布X轴方向比例值（0-1）d:色卡的高度，在画布Y轴方向比例值（0-1))
* 13.plot_range 输入数据区域"lat0,lat1,lon0,lon1"，根据区域进行绘制前裁剪，默认输入数据（lat,lon）最大区域
* 14.map_range 底图绘制区域"lat0,lat1,lon0,lon1" 默认和输入数据区域相同
* 15.画笔axis 位置 "a,b,c"（a:左起点，在画布X轴方向比例值（0-1),b:下起点，在画布Y轴方向比例值（0-1),c:宽度，在画布X轴方向比例值（0-1））默认"0.0,0.0,1.0"

## 示例
```
myPlotUtils.initParams(lat, lon, data,
                           output_file="./export.png",
                           # shape_file="/Users/lhtd_01/Downloads/gn_pyserver_py/um_pyserver_fy/statics/map/wgs_84_gbk/qixian_gbk",
                           # area_id="152921000000",
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
```
