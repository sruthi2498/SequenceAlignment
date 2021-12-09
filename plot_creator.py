import os
#import basic
#import efficient

X=[]
time1=[]
time2=[]
mem1=[]
mem2=[]

for i in range(18):
    '''x,t1,m1=basic.find_answer("input"+str(i+1)+".txt")
    x,t2,m2=efficient.find_answer("input"+str(i+1)+".txt")
    X.append(x)
    time1.append(t1)
    time2.append(t2)
    mem1.append(m1)
    mem2.append(m2)'''
    os.system("python3 nw.py inputs/input"+str(i+1)+".txt")
    os.system("python3 e1.py inputs/input"+str(i+1)+".txt")
    os.system("python3 e2.py inputs/input"+str(i+1)+".txt")
    
'''print(X)
print(time1)
print(time2)
print(mem1)
print(mem2)'''

