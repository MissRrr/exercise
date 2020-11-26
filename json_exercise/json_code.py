'''
Created on Nov 19, 2020

@author: Celia
'''
#coding=utf-8
import os
import json

"""ROOT = os.getcwd()
PATH = os.path.join(ROOT,'iSCSI_Data.json')"""

class JsonHandle():
  
  def __init__(self,root,path):
    self.root = root
    self.path = path
    self.load_dict = self.read_json_file(self.path)
  
  
  def read_json_file(self,path):
    if os.access(path,os.F_OK):
      load_f = open(path,'r',encoding='utf-8')
      load_dict = json.load(load_f)
      load_f.close()
      return load_dict
    
    
  def write_json_file(self):
    with open(self.path,'w',encoding='utf-8') as dump_f:
        json.dump(self.load_dict,dump_f,ensure_ascii=False,indent=4,separators=(',', ': ')) 
    
    
  def searsh_by_json_key(self,json_key,*args):
    #根据传入的json层级和keyword来查询
    if not (self.variable_is_Empty(args[0]) or self.variable_is_Empty(json_key)):
      if args[0]  not in self.load_dict[json_key].keys():
        print('there is no'+args[0])
      print(self.load_dict[json_key][args[0]])
    else:
      print('your input is invalid')
      return
            
            
  def del_by_json_key(self,json_key,*args):
    '''
    Host/Disk:
    args[0]--keyword args[1]--del data
    HostGroup/DiskGroup:
    args[0]--keyword args[1]--del data list
    Map:
    (keyword不能为空）
    args[0]--keyword args[1]--del HostGroup list args[2]--del DiskGroup list
    '''
    
    if json_key == 'Host' or json_key == 'Disk':
      if args[0] not in self.load_dict[json_key]:
        print('this key word is not existed，this operate is invalid')
        return
      self.load_dict[json_key].pop(args[0])
      print(self.load_dict[json_key])
    elif json_key == 'HostGroup' or json_key == 'DiskGroup':
      if args[0] not in self.load_dict[json_key]:
        print('this key word is not existed，this operate is invalid')
        return
      self.load_dict[json_key].pop(args[0])
      print(self.load_dict[json_key])
    elif json_key == 'Map':
      if self.variable_is_Empty(args[0]) or args[0] not in self.load_dict[json_key].keys():
        print('this operate is invalid')
        return
      #同时删除DiskGroup和HostGroup,
      if (not self.variable_is_Empty(args[1])) and (not self.variable_is_Empty(args[2])):
        del_host_list = args[1].split(',')
        #确定传入参数存在于DiskGroup，不存在删除
        for host in del_host_list:
          if host not in self.load_dict[json_key][args[0]].get('HostGroup'):
            del_host_list.remove(host)
        for host in del_host_list:                
          self.load_dict[json_key][args[0]].get('HostGroup').remove(host)
        del_disk_list = args[2].split(',')
        #确定传入参数存在于HostGroup，不存在删除
        for disk in del_disk_list:
          if disk not in self.load_dict[json_key][args[0]].get('DiskGroup'):
            del_disk_list.remove(disk)
        for disk in del_disk_list:                
          self.load_dict[json_key][args[0]].get('DiskGroup').remove(disk)
      #只删除HostGroup
      elif not self.variable_is_Empty(args[1]):
        del_host_list = args[1].split(',')
        #确定传入参数存在于HostGroup，不存在删除
        for host in del_host_list:
          if host not in self.load_dict[json_key][args[0]].get('HostGroup'):
            del_host_list.remove(host)
        for host in del_host_list:                
          self.load_dict[json_key][args[0]].get('HostGroup').remove(host)
      #只删除DiskGroup
      elif not self.variable_is_Empty(args[2]):
        del_disk_list = args[2].split(',')
        #确定传入参数存在于DiskGroup，不存在删除
        for disk in del_disk_list:
          if disk not in self.load_dict[json_key][args[0]].get('DiskGroup'):
            del_disk_list.remove(disk)
        for disk in del_disk_list:                
          self.load_dict[json_key][args[0]].get('DiskGroup').remove(disk)
      #直接删除一个map
      else:
        self.load_dict[json_key].pop(args[0])
      print(self.load_dict[json_key])
    else:
      print('your input is invalid')
      return
    self.write_json_file()
    
                   
  def add_by_json_key(self,json_key,*args):
    '''
    字典keyword增加时，注意是否会重复
    Host/Disk:
    args[0]--keyword args[1]--new data
    HostGroup/DiskGroup:
    args[0]--keyword args[1]--new data list
    Map：
    args[0]--keyword args[1]--new host data list args[2]--new disk data list
    '''
    if json_key == 'Host' or json_key == 'Disk':
      if self.variable_is_Empty(args[0]) or self.variable_is_Empty(args[1]):
        print('your input is invalid')
        return
      if args[0] in self.load_dict[json_key]:
        print('this key word is existed，this operate is invalid')
        return
      new_dict={args[0]:args[1]}
      self.load_dict[json_key].update(new_dict)
      print(self.load_dict[json_key])
    elif json_key == 'HostGroup' or json_key == 'DiskGroup':
      if self.variable_is_Empty(args[0]) or self.variable_is_Empty(args[1]):
        print('your input is invalid')
        return
      if args[0] in self.load_dict[json_key]:
        print('this key word is existed，this operate is invalid')
        return
      new_dict={args[0]:args[1].split(',')}
      self.load_dict[json_key].update(new_dict)
      print(self.load_dict[json_key])
    elif json_key == 'Map':
      if self.variable_is_Empty(args[0]) or self.variable_is_Empty(args[1]) or self.variable_is_Empty(args[2]):
        print('your input is invalid')
        return
      if args[0] in self.load_dict[json_key]:
        print('this key word is existed，this operate is invalid')
        return
      new_Host_Group_dict = {'HostGroup':args[1].split(',')}
      new_Disk_Group_dict = {'DiskGroup':args[2].split(',')}
      new_dict={args[0]:{**new_Host_Group_dict,**new_Disk_Group_dict}}
      self.load_dict[json_key].update(new_dict)
      print(self.load_dict[json_key])
    else:
      print('your input is invalid')
      return
    self.write_json_file()
    
          
  def update_by_json_key(self,json_key,*args):
    """
    Host/Disk:
    args[0]--keyword args[1]--new data
    HostGroup/DiskGroup:
    args[0]--keyword args[1]--new data list
    Map：
    args[0]--keyword args[1]--hg old data args[2]--hg new data 
                     args[3]--dg old data args[4]--dg new data
    """
    if json_key == 'Host' or json_key == 'Disk':
      if self.variable_is_Empty(args[0]) or self.variable_is_Empty(args[1]):
          print('your input is invalid')
          return
      new_dict={args[0]:args[1]}
      if args[0] in self.load_dict[json_key].keys():
        self.load_dict[json_key].update(new_dict)
        print(self.load_dict[json_key])
      else:
        print('this keyword didn\'t in the dict')
        return
    elif json_key == 'HostGroup' or json_key == 'DiskGroup':
      if self.variable_is_Empty(args[0]) or self.variable_is_Empty(args[1]):
        print('your input is invalid')
        return
      if args[0] in self.load_dict[json_key].keys():
        new_dict={args[0]:args[1].split(',')}
        self.load_dict[json_key].update(new_dict)
        print(self.load_dict[json_key])
      else:
        print('this keyword didn\'t in the dict')
        return
    elif json_key == 'Map':
      if (self.variable_is_Empty(args[0])) and (self.variable_is_Empty(args[1]) or self.variable_is_Empty(args[2])) and (self.variable_is_Empty(args[3]) or self.variable_is_Empty(args[4])):
        print('your input is invalid')
        return
      #可以一个值的更新替换
      for value in args[1::2]:
        if self.variable_is_Empty(value):
          continue
        else:
          v_type = value[:2]
          if v_type == 'hg':
            if value in self.load_dict[json_key][args[0]]['HostGroup']:
              self.load_dict[json_key][args[0]]['HostGroup'].remove(args[1])
              self.load_dict[json_key][args[0]]['HostGroup'].append(args[2])
            else:
              print(f'there is not {value} in the {args[0]},this update is invalid')
              return
          elif v_type == 'dg':
            if value in self.load_dict[json_key][args[0]]['DiskGroup']:
              self.load_dict[json_key][args[0]]['DiskGroup'].remove(args[3])
              self.load_dict[json_key][args[0]]['DiskGroup'].append(args[4])
            else:
              print(f'there is not {value} in the {args[0]},this update is invalid')
              return
          else:
            print('this operate is invalid')
      print(self.load_dict[json_key])
    else:
      print('your input is invalid')
      return
    self.write_json_file()

  
  def accoding_to_host_to_find_disk(self,host):
    #根据输入的host去查询它所利用到res
    with open(self.path,'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
    disk_list=[]
    for gg_info in load_dict['Map'].values():
      for hg in gg_info['HostGroup']:
        if host in load_dict['HostGroup'][hg]:
          for dg in gg_info['DiskGroup']:
            for disk in load_dict['DiskGroup'][dg]:
              disk_list.append(disk)
    disk_list = set(disk_list)
    print(disk_list)
              
                        
  def variable_is_Empty(self,variable):
    #判断变量是否为空
    return (variable == '' or variable.strip() == '' or len(variable) == 0 or variable.isspace())        
  


if __name__ == '__main__':
  root = os.getcwd()
  path = os.path.join(root,'iSCSI_Data.json')
  
  json_handler = JsonHandle(root,path)
  json_handler.add_by_json_key('Host','h8','iqn.2020-11.com.example:pytest08')
  json_handler.del_by_json_key('Host','h8')
  #json_handler.add_by_json_key('Map','map4','hg1,hg2','dg3,dg1')
  #json_handler.del_by_json_key('Map','map4','hg1','')
  #json_handler.update_by_json_key('Map','map1','hg1','hg3','dg2','dg1')
  #json_handler.searsh_by_json_key('Map','map1')
  json_handler.accoding_to_host_to_find_disk('h1')
  

  

        
    
    
