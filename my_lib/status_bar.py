# -*- coding: utf-8 -*-

import os, sys, time

"""
ステータスバー
"""
class status_bar:
  """
  コンストラクタ
  N : バー表示数
  """
  def __init__(self,N):
    self.ratio = 0
    self.N     = N
    print("0"+"_"*N+"100%\n"+" ",end="")
    #sys.stdout.write("0"+"_"*N+"100%\n"+" ")  # python2
    
  """
  Function call　バー更新
  r : 進捗率(0~1)
  """
  def __call__(self,r):
    if r*100.0 >= self.ratio:
      self.ratio += 100.0/self.N
      print("|", end="")
      #sys.stdout.write("|")  # python2
    if r>=1.0:
      print("end")