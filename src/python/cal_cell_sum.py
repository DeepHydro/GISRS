#
# The contents of this file are subject to the MIT License (MIT)
# You may not use this file except in compliance with the License. 
# The Initial Developer of this Original Code is Wang Xinchi at SUSTech
#  Created 11/10/2017 10:30 AM
# Contact 11510857@mail.sustc.edu.cn
#
 #调用模块
print 'import modules......\n\n'
import arcpy
import os
print 'import modules over.\n\n'

#设置输入tif文件所在文件夹的目录
input_dir = 'C:\\Gis\\Lecture7\\Budyko\\PPT'
os.chdir(input_dir)

#将tif文件转换至输入格式
list_input = []
list_file_name = os.listdir(input_dir)
for each in range(0,len(list_file_name)):
    every_file_dir = os.path.join(input_dir,list_file_name[each])
    if os.path.splitext(every_file_dir)[-1] == '.tif':
        print 'add ' + list_file_name[each] + '......\n'
        list_input.append(list_file_name[each])

str_input = ''
for each in range(0,len(list_input)):
    str_input += list_input[each] + ';'
str_input = str_input[:-1]


#设置输出目录
output_name = 'sum_PPT'
os.mkdir(output_name)
output_path = os.path.join(input_dir,output_name,output_name + '.tif')


# Process: Cell Statistics
print 'processing cell statistics......\n\n'
arcpy.gp.CellStatistics_sa(str_input, output_path, "SUM", "DATA")
print 'cell statistics over.'
