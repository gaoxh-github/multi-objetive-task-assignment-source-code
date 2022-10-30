# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 17:44:10 2021

@author: Dell
"""

import numpy as np
import math
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

gl_NU=4
gl_NT=20
gl_N=100#种群规模,即染色体个数

gl_bomb=5

UCAV_PK=[[0.5,0.8,0.3,0.4,0.5,0.6,0.6,0.7,0.7,0.6,0.5,0.6,0.4,0.6,0.4,0.3,0.3,0.8,0.3,0.7],
        [0.8,0.4,0.4,0.8,0.7,0.6,0.8,0.6,0.6,0.7,0.7,0.3,0.3,0.5,0.3,0.5,0.3,0.7,0.3,0.6],
        [0.6,0.5,0.8,0.3,0.8,0.3,0.7,0.7,0.7,0.4,0.6,0.5,0.3,0.5,0.4,0.6,0.3,0.8,0.4,0.8],
        [0.6,0.4,0.2,0.3,0.3,0.6,0.5,0.6,0.7,0.6,0.6,0.7,0.4,0.7,0.6,0.5,0.4,0.8,0.4,0.8]] #无人机对目标的杀伤概率

UCAV_PS=[[0.84,0.35,0.86,0.84,0.56,0.86,0.65,0.75,0.79,0.85,0.68,0.82,0.54,0.77,0.45,0.86,0.65,0.84,0.74,0.75],
          [0.86,0.84,0.56,0.86,0.35,0.84,0.55,0.65,0.70,0.76,0.49,0.56,0.56,0.70,0.58,0.85,0.84,0.82,0.92,0.52],
          [0.56,0.86,0.84,0.84,0.86,0.35,0.65,0.82,0.47,0.84,0.56,0.32,0.86,0.75,0.50,0.52,0.86,0.91,0.87,0.40],
          [0.35,0.86,0.84,0.56,0.92,0.84,0.45,0.52,0.35,0.70,0.58,0.92,0.50,0.82,0.52,0.85,0.84,0.80,0.85,0.40]] #无人机攻击目标后的生存概率 
    
Ob_V=[0.62,0.65,0.68,0.7,0.73,0.78,0.81,0.85,0.72,0.78,0.62,0.65,0.76,0.88,0.63,0.7,0.68,0.82,0.75,0.81] #目标自身的价值 

UAV_V=[0.8,1.1,0.9,1.3]#飞机的价值
xx=[[0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
     [1., 0., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
     [0., 1., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0.]]
def Object_1(x):
    """未被无人机摧毁的目标的价值"""
    V_all=0
    for j in range(gl_NT):
        V_all=V_all+Ob_V[j]
        
    V=0
    for i in range(gl_NU):       
        for j in range(gl_NT):
            V=V+(UCAV_PK[i][j])*(Ob_V[j])*(x[i][j])
    f_1=V_all-V
    return f_1

def Object_2(x):
    """无人机被击毁的总代价"""
    Cost=0
    for i in range(gl_NU):
        
        for j in range(gl_NT):
            Cost=Cost+(1-UCAV_PS[i][j])*UAV_V[i]*(x[i][j])            
    f_2=Cost
    return f_2

cc=0
while cc<2:
    nnn=0
    Triggering_conditions=(input('是否有新的任务（有新任务输入1，否则，输入0）:'))    
    while Triggering_conditions != 1 and Triggering_conditions != 0:
        # print("输入错误!")
        # print("请输入0或1")
        Triggering_conditions=int(input('是否有新的任务（有新任务输入1，否则，输入0）:'))
    if Triggering_conditions==0:
       print('无触发条件')
       break
    if Triggering_conditions==1:
        Tasks=int(input('输入任务编码:'))
        Ob_V1=float(input('Ob_V='))
        Ob_V.append(Ob_V1)
        UCAV_PK1=[]
        UCAV_PS1=[]
        probability_target= [[0.38, 0.86, 0.35],
                             [0.51, 0.95, 0.55], 
                             [0.39, 0.86, 0.34], 
                             [0.64, 0.94, 0.62]]
        probability_UAV= [[0.4, 0.78, 0.36], 
                          [0.59, 0.91, 0.59],
                          [0.36, 0.8, 0.39], 
                          [0.59, 0.97, 0.54]]
        
        for ii in range(len(UAV_V)):
            UCAV_PK11=float(input('UCAV_PK='))
            UCAV_PK[ii].append(UCAV_PK11)
            UCAV_PK1.append(UCAV_PK11)
        for ii in range(len(UAV_V)):
            UCAV_PS11=float(input('UCAV_PS='))
            UCAV_PS[ii].append(UCAV_PS11)
            UCAV_PS1.append(UCAV_PS11)
        alpha1=float(input('请输入权重alpha1=:'))
        
        print('UCAV_PK1=',UCAV_PK1)
        while (alpha1>1 or alpha1<0):
            print("输入错误!")
            print("请输入0-1之间的数")
            alpha1=float(input('请输入权重alpha1=:'))
        task=[]
       
        for j in range(len(xx)):
            task1=[]
            for jj in range(len(xx[j])):
                if xx[j][jj]==1:
                    task1.append(jj+1)
            task.append(task1)
        
        
        ammunition=[]
        for i in range(len(UAV_V)):
            sum1=0
            sum1=sum1+len(task[i])
            ammunition.append(gl_bomb-sum1)
        constract=[]   
        for ii in range(len(ammunition)):
            if ammunition[ii]==0:#第ii架无人机
                f_U1=[]
                V_all=0
                for j in range(gl_NT):
                    V_all=V_all+Ob_V[j]
                V=0    
                D=0
                
                for l in range(len(task[ii])):
                   
                    V=(UCAV_PK[ii][task[ii][l]-1])*(Ob_V[task[ii][l]-1])
                    D=(UCAV_PS[ii][task[ii][l]-1])*UAV_V[ii]
                    fnew=alpha1*(V)+(1-alpha1)*D
                    f_U1.append(fnew)
                
                f_newtask=alpha1*((UCAV_PK1[ii])*(Ob_V1))+(1-alpha1)*((UCAV_PS1[ii])*(UAV_V[ii]))
                smallest=f_U1[0]
                for f in range(len(f_U1)):
                    if f_U1[f]<smallest:
                        smallesst=f_U1[f]
                        jj=f
                    elif f_U1[f]==smallest:
                        jj=0
                if f_newtask<smallest:
                    constract1=[ii,0,0,-500]
                else:
                    constract1=[ii,Tasks,task[ii][jj],f_newtask-smallest]
                
            elif ammunition[ii]!=0:#第ii架无人机
            
                f_newtask=alpha1*(UCAV_PK1[ii])*(Ob_V1)+(1-alpha1)*((UCAV_PS1[ii])*(UAV_V[ii]))
                constract1=[ii,Tasks,-1,f_newtask]
            constract.append(constract1)
        print('lenconstract=',len(constract))    
        bigger=constract[0][3]   
        for k in range(len(constract)):
            if constract[k][3]>bigger:
                bigger=constract[k][3]
                uav=k
            else:
                bigger=constract[0][3]
                uav=0
        print('uav=',uav)
        
        Constract_end=constract[uav]
        for h in range(len(xx)):
            xx[h].append(0)
        if Constract_end[3]!=-500:
            if Constract_end[2]==-1:
                task[Constract_end[0]].append(Tasks)
            elif Constract_end[2]!=-1:
                task[Constract_end[0]].append(Tasks)
                task[Constract_end[0]].remove(Constract_end[2])
            if Constract_end[2]==-1:
                for h in range(len(xx)):
                    if h==uav:
                        # xx[h].append(1)
                        xx[h][Constract_end[1]-1]=1
                    # elif h!=uav:
                    #     xx[h].append(0)
            elif Constract_end[2]!=-1:
                
                    
                xx[Constract_end[0]][Constract_end[2]-1]=0
                xx[Constract_end[0]][Constract_end[1]-1]=1
        print('lenxx0=',len(xx[0]))   
        print('xx=',xx)

        print('task=',task)   
        nnn+=1
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        