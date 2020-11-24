'''
Created on Nov 20, 2020

@author: Celia
'''

import os
import json
import jsonpath

ROOT = os.getcwd()
PATH = os.path.join(ROOT,'iSCSI_Data.json')
LOAD_DICT={}

if os.access(PATH,os.F_OK):
  with open(PATH,'r',encoding='utf-8') as load_f:
      LOAD_DICT = json.load(load_f)

def print_dict(array):
  res_num_dict = {}
  res_num = []
  for i in array:
    #如果不存在的话，将元素作为key，值为列表中元素的count
    if i not in res_num_dict.keys():
      res_num_dict[i] = array.count(i)
  #将元素出现次数放入列表
  for value in res_num_dict.values():
    res_num.append(value)
  print(res_num_dict)

#以map为组的一个Xgroup的多层列表，结构[[[……], [……]], [[……], [……]]，…… [[……], [……]]]
def divide_by_map(map_list,group_dict):
  res_list=[]
  for i in range(len(map_list)):
    tmp_list=[]
    for j in range(len(map_list[i])):
      #以map进行分组，同一个map的HostGroup放在同一个列表里
      tmp_list.append((group_dict.get(map_list[i][j])))
    res_list.append(tmp_list)
  return res_list

#将同一个map的Xgroup的X拆分出来放在列表里，每一个列表值是该map的X列表
def divide_group_by_each_map(x_list):
  host_group_list_each_map=[]
  for i in x_list:
    tmp=[]
    if len(i)==1:
      tmp = i[0]
    for j in range(1,len(i)):
      tmp = i[j-1]+i[j]
    host_group_list_each_map.append(tmp)
  return host_group_list_each_map


def main():
  #jsonpath.jsonpath()返回的是一个list,取[0]是该列表只有一个值，为了方便获取列表里的字典。
  map_host_list = jsonpath.jsonpath(LOAD_DICT,"$.Map.*.HostGroup") #[['hg1', 'hg2'], ['hg1', 'hg3'], ['hg1', 'hg3']]
  map_disk_list = jsonpath.jsonpath(LOAD_DICT,"$.Map.*.DiskGroup") #[['dg1', 'dg2'], ['dg1', 'dg3'], ['dg1']]
  host_group_dict = jsonpath.jsonpath(LOAD_DICT,"$.HostGroup")[0]  #{'hg1': ['h1', 'h2'], 'hg2': ['h3', 'h4'], 'hg3': ['h5', 'h3'], 'hg4': ['h6'], 'hg5': ['h7']}
  disk_group_dict = jsonpath.jsonpath(LOAD_DICT,"$.DiskGroup")[0]  #{'dg1': ['res_a', 'res_b'], 'dg2': ['res_c', 'res_b'], 'dg3': ['res_d', 'res_c']}

  host_list = divide_by_map(map_host_list, host_group_dict)
  host_group_list_each_map= divide_group_by_each_map(host_list)
  
  disk_list=divide_by_map(map_disk_list, disk_group_dict)
  disk_group_list_each_map = divide_group_by_each_map(disk_list)
  
  #存放res和对应host进行拼接之后的字符串
  res_host_list=[]
  for d,h in zip(disk_group_list_each_map,host_group_list_each_map):
    for i in range(len(d)): 
      for j in range(len(h)):
        res_host_list.append(d[i]+'_'+h[j])

  #res的二维数组
  res_list=[]
  for i in range (len(map_disk_list)):
    for j in range(len(map_disk_list[i])):
      #获得一个res的二维数组
      res_list.append(disk_group_dict.get(map_disk_list[i][j]))
  #res的一维数组
  disk_array=[]
  for i in range(len(res_list)):
    for j in range(len(res_list[i])):
      #获得一个res的一维数组
      disk_array.append(res_list[i][j])
  
  #result1
  print_dict(res_host_list)
  #result2
  print_dict(disk_array)


if __name__ == '__main__':
    main()
