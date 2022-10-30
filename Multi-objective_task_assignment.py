# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 20:14:59 2020

@author: user
"""


import numpy as np
import random
import math
#import operator
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import time
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter


gl_NU=4
gl_NT=8

gl_Pc=0.8
gl_Pm=0.2
gl_bomb=2

starttime=time.time()

UCAV_PK=[[0.5,0.8,0.3,0.4,0.5,0.6,0.6,0.7],
        [0.8,0.4,0.4,0.8,0.7,0.6,0.8,0.6],
        [0.6,0.5,0.8,0.3,0.8,0.3,0.7,0.7],
        [0.6,0.4,0.2,0.3,0.3,0.6,0.5,0.6]]  # 无人机对目标的杀伤概率

UCAV_PS=[[0.84,0.35,0.86,0.84,0.56,0.86,0.65,0.75],
         [0.86,0.84,0.56,0.86,0.35,0.84,0.55,0.65],
         [0.56,0.86,0.84,0.84,0.86,0.35,0.65,0.82],
         [0.35,0.86,0.84,0.56,0.92,0.84,0.45,0.52]] #无人机攻击目标后的生存概率 
    
Ob_V=[0.62,0.65,0.68,0.7,0.73,0.78,0.81,0.85] #目标自身的价值 

UAV_V=[0.8,1.1,0.9,1.3]#飞机的价值
 

def Object_1(x):
    """未被无人机摧毁的目标的价值"""
    V_all=0
    for j in range(gl_NT):
        V_all=V_all+Ob_V[j]
        
    V=0
    for i in range(gl_NU):       
        for j in range(gl_NT):
            V=V+(UCAV_PK[i][j])*(Ob_V[j])*(x[i][j])
            #print(V)
    f_1=V_all-V
    #print(V_all)
    return f_1

def Object_2(x):
    """无人机被击毁的总代价"""
    Cost=0
    for i in range(gl_NU):
        
        for j in range(gl_NT):
            Cost=Cost+(1-UCAV_PS[i][j])*UAV_V[i]*(x[i][j])
            
    f_2=Cost
    #print(f_2)
    return f_2
            
    

def Constraint_1(x):
    """
    对生成的个体矩阵的列进行求和，
    便于构造约束条件：每个目标至多攻击一次
    """
    j=0
    i=0
    C1=[]
    
    for j in range(gl_NT):
        a=0
        for i in range(gl_NU):
            a=a+x[i][j]            
        C1.append(a)
    return C1

def Constraint_2(x):
    """
    对生成的个体矩阵的行进行求和，
    便于构造约束条件：每架无人机最多攻击两个目标
    """
    j=0
    i=0
    C2=[]
    
    for i in range(gl_NU):
        a=0
        for j in range(gl_NT):
            a=a+x[i][j]             
        C2.append(a)
    return C2            
            
def Constraint_3(x):
    """在约束1和约束2的条件下，约束3是必然成立的"""
    
    list=[]   
    for j in range(gl_NT):
        v=0
        for i in range(gl_NU):
            v=v+(UCAV_PK[i][j])*(Ob_V[j])*(x[i][j])  
        list.append(v)
    return list

def Pop_creat():
    s=0
    np.list=[]
    np.list_f=[]
    while s<gl_N:  
        c=[0,0,0,0]
        x=np.zeros(shape=(gl_NU,gl_NT))
        a=np.random.randint(-2,-1,size=(gl_NU,gl_NT))
        for i in range(gl_NU):
            if i==0:
                for j in range(gl_NT):
                    if c[i]<2:
                        x[i][j]=random.randint(0,1)
                        if x[i][j]==1:
                            a[i][j]=j
                            c[i]+=1
                        else:
                            a[i][j]=-1
                    else:
                        x[i][j]=0       
            else:
                for j in range(gl_NT):
                    if j==a[0][j] or j==a[1][j] or j==a[2][j] or j==a[3][j]:
                        x[i][j]=0
                    else:
                        if c[i]<2:
                            x[i][j]=random.randint(0,1)
                            if x[i][j]==1:
                                a[i][j]=j
                                c[i]+=1
                            else:
                                a[i][j]=-1
                        else:
                            x[i][j]=0
        nn=0
        for i in range(len(np.list)):
            if x is not np.list[i]:
                nn+=0
            else:
                nn+=1
        if nn==0:
            np.list.append(x)
            s+=1
        else:
            s+=0
    return np.list


def f_value(x):
    np.list_f=[] 
    np.list_f1=[]
    np.list_f2=[]
    for i in range(len(x)):
        f_1=round(Object_1(x[i]),3)#将计算值保留2位小数 
        f_2=round(Object_2(x[i]),3)
        np.list_f.append([f_1,f_2])
        np.list_f1.append(f_1)
        np.list_f2.append(f_2)  
    return (np.list_f1,np.list_f2)


def index_of(a,list):
    """查找列表指定元素的索引"""
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    """函数根据指定的值列表排序"""
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list
      


def fast_non_dominated_sort(Values1,Values2):
    S=[[] for i in range(0,len(Values1))]
    front = [[]]
    n=[0 for i in range(0,len(Values1))]
    rank = [0 for i in range(0, len(Values1))]
    for p in range(0,len(Values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(Values1)):

             if (Values1[p] <= Values1[q] and Values2[p] < Values2[q]) or (Values1[p] < Values1[q] and Values2[p] <= Values2[q]):
                if q not in S[p]:
                    S[p].append(q)
             elif (Values1[p] >= Values1[q] and Values2[p] > Values2[q]) or (Values1[p] > Values1[q] and Values2[p] >= Values2[q]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
 
    i = 0
    while(front[i] != []):
        # 如果分层集合为不为空，
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                # 则将fk中所有给对应的个体np-1
                if( n[q]==0):
                    # 如果nq==0
                    rank[q]=i+1
 
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    del front[len(front)-1]
    return front

def crowding_distance(values1, values2, front):
    """个体的拥挤距离"""
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values1[sorted1[k-1]])/(max(values1)-min(values1))        
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values2[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance

def Change_value(a,b):
    """互换两个变量的值"""   
    c=a
    a=b
    b=c
    return (a,b)


def Crossover(C,D):
    """交叉算子"""

    l1=random.randint(0,gl_NU-1)
    l2=random.randint(0,gl_NU-1)
    a,b=Change_value(C[l1],D[l2])

    A=np.zeros(shape=(gl_NU,gl_NT))
    B=np.zeros(shape=(gl_NU,gl_NT))
    
    for i in range(gl_NU):
        if i!=l1:
            for j in range(gl_NT):
                A[i][j]=C[i][j]
        else:
            for j in range(gl_NT):
                A[i][j]=a[j]
    
    for i in range(gl_NU):
        if i!=l2:
            for j in range(gl_NT):
                B[i][j]=D[i][j]
        else:
            for j in range(gl_NT):
                B[i][j]=b[j] 

    for j in range(gl_NT):
        if A[l1][j]==1:
            for i in range(gl_NU):
                if i!=l1:
                    if A[i][j]==1:
                        A[i][j]=0
    for j in range(gl_NT):
        if B[l2][j]==1:
            for i in range(gl_NU):
                if i!=l2:
                    if B[i][j]==1:
                        B[i][j]=0 
    for i in range(gl_NU):
        C2_A=Constraint_2(A)#行和 
        if C2_A[i]==0:
            mm=0
            for j in range(gl_NT):
                C1_A=Constraint_1(A)#列和
                if mm<=gl_bomb-1 and C1_A[j]==0:
                    A[i][j]=1
                    mm+=1
    for i in range(gl_NU):
        C2_B=Constraint_2(B)
        if C2_B[i]==0:#行和为0，即无人机未执行攻击任务
            nn=0
            for j in range(gl_NT):
                C1_B=Constraint_1(B)
                if nn<=gl_bomb-1 and C1_B[j]==0:#为了保证无人机的攻击量不超过其弹药量
                    B[i][j]=1
                    nn+=1
    return (A,B)
    
 
def Mutation(C):
    """变异算子"""
    n=0
    A=np.zeros(shape=(gl_NU,gl_NT))
    C1=Constraint_1(C)
    for j in range(gl_NT):
        if C1[j]==0:
            for i in range(gl_NU):
                C2=Constraint_2(C)
                if C2[i]<=1 and C[i][j]==0:
                    C[i][j]=1
                    break                                  
            n+=1
        else:
            n+=0
            
    if n==0:
        l3=random.randint(0,gl_NU-1)
        l4=random.randint(0,gl_NU-1)
        a,b=Change_value(C[l3],C[l4])
        
        for i in range(gl_NU):
            if i!=l3 and i!=l4:
                for j in range(gl_NT):
                    A[i][j]=C[i][j]
                    
            elif i==l3:
                for j in range(gl_NT):
                    A[i][j]=a[j]
                
            elif i==l4:
                for j in range(gl_NT):
                    A[i][j]=b[j]
    else:
        A=C   
    return A
                
def Son_creat(Pop1,front):
    #print(len(Pop1))
    n=0
    Pop2=[]
    while n<=gl_N:  #选择->按概率交叉->按概率变异，得到2倍种群大小的种群 
        for i in range(len(front)):
            for l in range(len(front[i])):
                for j in range(l+1,len(front[i])):
                    p1=random.random()
                    if p1<gl_Pc:
                        A1,A2=Crossover(Pop1[front[i][l]],Pop1[front[i][j]])
                        p2=random.random()
                        p22=random.random()
                        if p2<gl_Pm:
                            A1=Mutation(A1)
                        if p22<gl_Pm:
                            A2=Mutation(A2)
                        PP=Pop1+Pop2
                        n1=0 
                        for mm in range(len(PP)):
                            if (A1==PP[mm]).all() == False:
                                n1+=0
                            else:
                                n1+=1
                        if n1==0:
                            Pop2.append(A1)
                            n+=1
                            if n>gl_N:
                                Pop2.pop()
                                break
                        PP=Pop1+Pop2
                        n2=0
                        for mm in range(len(PP)):
                            if (A2==PP[mm]).all() == False:
                                n2+=0
                            else:
                                n2+=1
                        if n2==0:
                            Pop2.append(A2)
                            n+=1
                            if n>gl_N:
                                Pop2.pop()
                                break
                if n>gl_N:
                    break
            if n>gl_N:
                break            
            if i<len(front)-1:
                for j in range(len(front[i])):
                    for ll in range(len(front[i+1])):
                        p3=random.random()
                        if p3<gl_Pc:
                            B1,B2=Crossover(Pop1[front[i][j]],Pop1[front[i+1][ll]])
                            p4=random.random()
                            p44=random.random()
                            if p4<gl_Pm:
                                B1=Mutation(B1)
                            if p44<gl_Pm:
                                B2=Mutation(B2)
                            PP=Pop1+Pop2
                            n3=0
                            for mm in range(len(PP)):
                                if (B1==PP[mm]).all() == False:
                                    n3+=0
                                else:
                                    n3+=1
                            if n3==0:
                                Pop2.append(B1)
                                n+=1
                                if n>gl_N:
                                    Pop2.pop()
                                    break

                            PP=Pop1+Pop2
                            n4=0
                            for mm in range(len(PP)):
                                if (B2==PP[mm]).all() == False:
                                    n4+=0
                                else:
                                    n4+=1
                            if n4==0:
                                Pop2.append(B2)
                                n+=1
                                if n>gl_N:
                                    Pop2.pop()
                                    break
                    if n>gl_N:
                        break
                    
            elif i==len(front)-1:
                for j in range(len(front[i])):
                    for ll in range(len(front[0])):
                        p5=random.random()
                        if p5<gl_Pc:
                            B1,B2=Crossover(Pop1[front[i][j]],Pop1[front[0][ll]])
                            p6=random.random()
                            p66=random.random()
                            if p6<gl_Pm:
                                B1=Mutation(B1)
                            if p66<gl_Pm:
                                B2=Mutation(B2)
                            PP=Pop1+Pop2
                            n3=0
                            for mm in range(len(PP)):
                                if (B1==PP[mm]).all() == False:
                                    n3+=0
                                else:
                                    n3+=1
                            if n3==0:
                                Pop2.append(B1)
                                n+=1
                                if n>gl_N:
                                    Pop2.pop()
                                    break
                            PP=Pop1+Pop2
                            n4=0
                            for mm in range(len(PP)):
                                if (B2==PP[mm]).all() == False:
                                    n4+=0
                                else:
                                    n4+=1
                            if n4==0:
                                Pop2.append(B2)
                                n+=1
                                if n>gl_N:
                                    Pop2.pop()
                                    break
                    if n>gl_N:
                        break
            if n>gl_N:
                break
    return Pop2
                    
def FindSmallest(arr):
    """寻找给定的数组arr中最小的值"""
    Smallest=arr[0] #存储数组中最小的值
    Smallest_index=0 #存储数组中最小的值的索引
    for i in range(1,len(arr)): #遍历数组,通过挨个比较得到最小值
        if arr[i]<Smallest:
            Smallest=arr[i]
            Smallest_index=i
    return Smallest                
                    
        
#主函数    
gl_gen=200
gen_no=0
gl_N=100
Pop_father=Pop_creat()
s1=[]
s2=[]
n1=[]
while(gen_no<gl_gen):

    values1,values2=f_value(Pop_father)     
    front=fast_non_dominated_sort(values1,values2)
    Pop_son=Son_creat(Pop_father,front)    
    Pop_new=Pop_father+Pop_son   
    f1,f2=f_value(Pop_new)
    front=fast_non_dominated_sort(f1,f2)
    size=0
    n=0
    for i in range(len(front)):
        
        if size<gl_N:
            size=size+len(front[i])
            n+=1
        elif size>=gl_N:
            i=i-1
            break
    C=crowding_distance(f1, f2, front[i])
    Pop_father1=[]
    for l in range(i+1):
        if l!=i:
            for ll in range(len(front[l])):
                Pop_father1.append(Pop_new[front[l][ll]])
        elif l==i:
            S=[]
            while(len(S)!=len(C)):
                index=index_of(min(C),C)
                S.append(index)
                C[index]=math.inf
            sorted1=sort_by_values(front[l],f1)
            for ll in range(len(S)-1,-1,-1):
                if len(Pop_father1)<gl_N:
                    Pop_father1.append(Pop_new[sorted1[S[ll]]])
                if len(Pop_father1)>=gl_N:
                    break
    
    f1,f2=f_value(Pop_father1)  
    for lll in range(len(f1)):
        for jj in range(len(f1)):
            if jj!=lll and f1[lll]==f1[jj] and f2[lll]==f2[jj]:
                break
    front=fast_non_dominated_sort(f1,f2)
    gen_no+=1
    Pop_father=Pop_father1
    Pop_father1=[]
    value1,value2=f_value(Pop_father)
    #print(value1)
    front=fast_non_dominated_sort(value1,value2)
    #print(front[0])
    Pop_best=[]
    for jj in range(len(front[0])):
        Pop_best.append(Pop_father[front[0][jj]])
    
    ff1,ff2=f_value(Pop_father)
    f11=[]
    f22=[]
    nn=0
    sorted3=sort_by_values(front[0],ff1)
    sorted4=sort_by_values(front[0],ff2)
    f11.append(value1[sorted3[0]])
    f22.append(value2[sorted4[len(front[0])-1]])
    for k in range(1,len(front[0])-1):
        if value1[sorted3[k+1]]-value1[sorted3[k]]<=0.03 and value2[sorted4[len(front[0])-k-1]]-value2[sorted4[len(front[0])-k-2]]>=0.05:
            nn+=1
        elif value1[sorted3[k+1]]-value1[sorted3[k]]>=0.04 and value2[sorted4[len(front[0])-k-1]]-value2[sorted4[len(front[0])-k-2]]<=0.01:
            nn+=1
        else:
            f11.append(f1[sorted3[k]])
            f22.append(f2[sorted4[len(front[0])-k-1]])
    
    f11.append(value1[sorted3[len(front[0])-1]])
    f22.append(value2[sorted4[0]])

    S1=FindSmallest(f11)
    S2=FindSmallest(f22)
    
    s1.append(S1)
    s2.append(S2)
    n1.append(gen_no)


print("gen_no=%s"%gen_no)
print(f11)
print("nn=%s"%nn)
print("s1=%s"%s1)
print("s2=%s"%s2)
print("n1=%s"%n1)
file_handle=open('result.txt',mode='w')
for ii in range(len(Pop_father)):
    file_handle.write(str(Pop_father[ii])+'\n'+'\n')#str将数据强制转换为字符串+'\n'+'\n'
    #file_handle.write(',')
    
for ii in range(len(f11)):
    file_handle.write(str(f11[ii]))
    file_handle.write(',')
    file_handle.write(' ')
    
file_handle.write('\n')

for ii in range(len(f22)):
    file_handle.write(str(f22[ii]))
    file_handle.write(',')
    file_handle.write(' ')
file_handle.close()


plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)

plt.scatter(f11, f22)
plt.show()

endtime=time.time()
dtime=endtime-starttime
print("运行时间：%.8s s" % dtime)
