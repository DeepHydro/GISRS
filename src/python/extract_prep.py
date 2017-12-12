# The contents of this file are subject to the MIT License (MIT)
# You may not use this file except in compliance with the License. 
# The Initial Developer of this Original Code is Dr. Yong Tian at SUSTech
# Created 10/10/2017 10:30 AM
# Contact tiany@sustc.edu.cn
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Local variables
# 1364.tif所在目录
in_dir = "E:\\class\\GISRS\\Lecture_7\\Data\\Precipitation\\"
# 提取之后的RASTER存放路径
out_dir = "E:\\class\\GISRS\\Lecture_7\\Data\\Precipitation\\china\\"
# Mask 文件
china_bound = "E:\\class\GISRS\\Lecture_7\\Data\\Precipitation\\china_bound.shp"
# 文件名起始编号
start_index = 1359
end_index = 1382

# 输出统计文件目录
stat_file = out_dir + "stat_prep.csv"
fs_stat = open(stat_file,'w')
print>>fs_stat,"Index",",","Mean"

for index in range(start_index, end_index+1):
    fn_in = in_dir + str(index) + ".tif"
    fn_out = out_dir + str(index)+ "_china.tif"
    # Process: Extract by Mask
    arcpy.gp.ExtractByMask_sa(fn_in, china_bound, fn_out)
    # Process: Get statastics of output raster
    st = arcpy.GetRasterProperties_management(fn_out, "MEAN")
    mean= st.getOutput(0)
    print index
    print>>fs_stat,index,",",mean

fs_stat.close()
