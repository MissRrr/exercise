'''
Created on Nov 26, 2020

@author: Celia
'''

from tkinter import *
from tkinter import filedialog 
import tkinter.messagebox


class MY_GUI():
    def __init__(self,init_window):
      self.init_window = init_window
        
    def set_init_window(self):
      self.init_window.title("simple notepad 1.0") 
      self.init_window.geometry('400x400+400+100')      
      self.init_data_text = Text(self.init_window,width=90,height=40,selectforeground="black",undo=True,font=50)  #原始数据录入框
      #顶级菜单窗口
      self.top_menu=Menu(self.init_window)
      self.src_filename = None
      
      #创建文件下拉菜单，添加到顶层菜单窗口
      file_menu=Menu(self.top_menu,tearoff=False)
      #添加下拉内容：
      file_menu.add_command(label="新建",command=self.new_file)
      file_menu.add_command(label="打开",command=self.open_file)
      file_menu.add_command(label="保存",command=self.save_file)
      file_menu.add_command(label="另存为",command=self.other_save_file)
      file_menu.add_separator()
      file_menu.add_command(label="退出",command=quit)
      #添加文件分层菜单项到顶层菜单窗口
      self.top_menu.add_cascade(label="文件", menu=file_menu)
      
      #创建编辑菜单
      edit_menu=Menu(self.top_menu,tearoff=False)
      #创建编辑下拉内容
      edit_menu.add_command(label="撤销",command=self.callback)
      edit_menu.add_command(label="剪切",command=self.cut)
      edit_menu.add_command(label="复制",command=self.copy)
      edit_menu.add_command(label="粘贴",command=self.paste)
      edit_menu.add_separator()
      edit_menu.add_command(label="全选",command=self.select_all)
      #添加编辑分层菜单项到顶层菜单窗口
      self.top_menu.add_cascade(label="编辑",menu=edit_menu)
      
      #右键菜单
      self.pop_up_menu=Menu(self.init_window,tearoff=False)
      #创建右键菜单内容
      self.pop_up_menu.add_command(label="全选",command=self.select_all)
      self.pop_up_menu.add_command(label="撤回",command=self.callback)
      self.pop_up_menu.add_separator()
      self.pop_up_menu.add_command(label="剪切",command=self.cut)
      self.pop_up_menu.add_command(label="复制",command=self.copy)
      self.pop_up_menu.add_command(label="粘贴",command=self.paste)
      #将右键菜单显示函数绑定到Text上
      #<Button-3>鼠标右键,但是mac好像读不出来右键，用<Button-2>鼠标中键（触摸板双指双击可显示）
      self.init_data_text.bind("<Button-2>",self.popup)
      
      self.init_window.config(menu=self.top_menu)
      self.init_data_text.pack()

    def quit(self):
      self.init_window.destroy()
    
    #右键菜单显示函数
    def popup(self,event):
        self.pop_up_menu.post(event.x_root,event.y_root)
    
    #复制功能函数
    def copy(self):
        global content
        content=self.init_data_text.get(SEL_FIRST,SEL_LAST)
        return content
    
    #剪切函数
    def cut(self):
        global content
        content=self.init_data_text.get(SEL_FIRST,SEL_LAST)
        self.init_data_text.delete(SEL_FIRST,SEL_LAST)
        return content
    
    #粘贴功能函数
    def paste(self):
      self.init_data_text.insert(INSERT,content)
       
    def callback(self):
      self.init_data_text.event_generate("<<Undo>>")
      
    def select_all(self):
      self.init_data_text.event_generate("<<SelectAll>>")
  
    def get_text(self):
      return self.init_data_text.get(1.0,END).strip()
  
    def new_file(self):
          file_content = self.get_text()
          if file_content and tkinter.messagebox.askokcancel('提示', '当前内容要进行保存吗？'):
              if self.src_filename:
                  self.save_file(self.src_filename)
              else:
                  self.other_save_file()
          self.init_data_text.delete(1.0, END)
  
    def open_file(self):
      #enc = "utf-8"
      #打开文件前先判断是否要保存，并清除文本内容
      self.new_file()      
      import sys
      # 查看CODESET是否定义
      try:
          import locale
          locale.setlocale(locale.LC_ALL,'')
          #enc = locale.nl_langinfo(locale.CODESET)
      except (ImportError, AttributeError):
          print('error:there is something wrong in CODESET')
  
      self.src_filename=filedialog.askopenfilename(title='open file',filetypes=[("TXT",'.txt'),("all files", "*")],initialdir='../Documents')
      try:
          f=open(self.src_filename,"r")
          file_content = f.read()
          f.close()
          self.init_data_text.insert(INSERT,file_content)

      except:
          print("Could not open File: ")
          print(sys.exc_info()[1])
    
    #保存
    def save_file(self):
      file_name = self.src_filename if self.src_filename else filedialog.askopenfilename(filetypes=[('TXT', '.txt')])
      if file_name:
      #file_name=filedialog.asksaveasfilename(filetypes=[("TXT",".txt")])
        with open(file_name,'w') as f:
            f.write(self.get_text())
        tkinter.messagebox.showinfo('提示', '保存成功')

    #另存为
    def other_save_file(self):
      f = filedialog.asksaveasfile(filetypes=[('TXT', '.txt')])
      if f:
        f.write(self.get_text())
      tkinter.messagebox.showinfo('提示', '保存成功')


if __name__ == '__main__':
  init_window = Tk()              #实例化Tkinter对象
  tkinter_example = MY_GUI(init_window)
  tkinter_example.set_init_window() #设置根窗口默认属性
  init_window.mainloop()     