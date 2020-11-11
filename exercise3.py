#!/usr/bin/python3.6
#coding=utf-8

"""题目：计算一个文件大致包含多少个单词 """
def count_words(filename):
  try:
    with open(filename) as file_obj:
      contents = file_obj.read()
  #如果try代码块中的代码导致了错误, Python将查找except代码块,如果指定的错误与引发的错误相同，Python会运行其中的代码
  except FileNotFoundError:
    msg = "Sorry, the file " + filename + " does not exist."
    print(msg)
  #依赖于 try 代码块成功执行的代码都应放到 else 代码块中
  else:
    #计算文件大致包含多少个单词
    words = contents.split()
    num_words = len(words)
    print("The file " + filename + " has about " + str(num_words) +" words.")

if __name__=='__main__':
  filename = 'passage.txt'
  count_words(filename)
