 # -*- coding: utf-8 -*-

import os, sys, time
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import csv
import copy

from status_bar import *
from downSampler import *
from logger import *
import inspect

"""
シミュレーション実行関数
"""
def simulate(model, x0, t0=0.0, tf=10.0, dt=0.01, ts=0.0):

  if dt <= 0:
    print("[Error] time step is not positive. dt<=0")
    return None

  if t0 > tf:
    print("[Error] start time is bigger than finish time. t0>tf")
    return None

  try:
    m = model.dynamics
  except AttributeError:
    print("[Error] dynamics method is not exist.")
    return None

  try:
    c = model.controller
    model.set_period(dt)
  except AttributeError:
    print("[Warning] controller method is not exist.")
    c = None

  rkg = RKG(x0=x0, t0=t0)
  log = downSampler(ts/dt)    # ログ周期
  sb = status_bar(N=100)
  for tim in np.arange(t0, tf, dt):
    sb(tim/tf)
    if rkg.step(dth_=dt, motion=m, controller=c, log=log()):
        break

  print("simulation end.")
  return rkg, model

#rkg.to_csv(folder=".\\log", index = "tim", keys  = ["x"])

"""
数値積分
 x0 : 初期状態
 t0 : 初期時間[sec]
 ts : データログ周期[sec]
"""
class RKG(logger):
  def __init__(self, x0, t0):
    self.preset(x0, t0)
  
  """
  preset 初期状態の設定
   x0 : 初期状態（リスト形式）
   t0 : 初期時間[sec]
   Ns : データログ周期[1/Ns回]
  """
  def preset(self, x0, t0):
    self.tim  = t0
    self.x    = x0
    self.dx   = [0]*len(x0)
    self.qx   = [0]*len(x0)
    self.clear()
    self.to_memory()

  """
  to_memory シミュレーション結果の格納
  """
  def to_memory(self):
    self.log(keys=["tim","x"])
  
  """
  step 時間ステップ更新
   dth_ : 時間刻み[sec]
   func : 運動方程式クラス
  """
  def step(self, dth_, motion, controller=None, log=False):
    ra = [0.5, 0.2928932188134525, 1.707106781186548, 0.1666666666666667] 
    rb = [2.0, 1.0, 1.0, 2.0] 
    rc = [0.5, 0.2928932188134525, 1.707106781186548, 0.5] 
    res = False
    
    """ controller """
    if controller is not None:
      controller(self.tim, self.x)
    
    """ motion """ 
    ret = motion(self.tim, self.x, self.dx) 
    res = res or ret 
    for rj in range(4): 
      for rk in range(len(self.x)): 
        r1 = dth_*self.dx[rk] 
        r2 = ra[rj]*(r1 - rb[rj]*self.qx[rk]) 
        self.x[rk]  += r2 
        self.qx[rk] += 3*r2 - rc[rj]*r1 
      if rj == 0 or rj == 2: 
        self.tim += dth_/2.0 
      if rj <= 2: 
        ret = motion(self.tim, self.x, self.dx)
        res = res or ret 
    
    """ data logging """
    if log:
      self.to_memory()

    return res


