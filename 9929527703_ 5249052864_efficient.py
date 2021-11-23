import math

def generateString(base_string, indices):
    result_string = base_string
    for i in indices:
        i = int(i)
        if i+1 < len(result_string):
            result_string = result_string[:i+1] + result_string + result_string[i+1:]
        else:
            result_string = result_string[:i+1] + result_string 
        #print(result_string)
    return result_string
      
# input generator : read from input.txt

def generateInputStrings(filename):
    with open(filename,"r") as f:
        lines = f.readlines()
        lines = [x.replace("\n","") for x in lines]

        n = len(lines)
        X_base_string = lines[0]
        X_gen_indices = []
        i=1
        while i<n :
            index =  lines[i]
            if index.isdigit():
                X_gen_indices.append(index)
            else:
                break
            i+=1
        # print(X_base_string,X_gen_indices)
        X = generateString(X_base_string,X_gen_indices)

        Y_base_string = lines[i]
        Y_gen_indices = []
        i+=1
        while i<n:
            Y_gen_indices.append(lines[i])
            i+=1
        # print(Y_base_string,Y_gen_indices)
        Y = generateString(Y_base_string,Y_gen_indices)
        return X,Y

# sequence alignment
# output 
    # The first 50 elements and the last 50 elements of the actual alignment.
    # 2. The time it took to complete the entire solution.
    # 3. Memory required.
    
   
#function to get alignment
def basicAlignment(x, y, mismatch, delta):
    m = len(x)
    n = len(y)
    dp=[[0] * (n+1) for i in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i * delta 
    for i in range(n+1):
        dp[0][i] = i * delta
    
    for i in range(1,m+1):
        for j in range(1,n+1):
            if (x[i - 1] == y[j - 1]):
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + mismatch[x[i-1]][y[j-1]] ,
                                dp[i - 1][j] + delta,
                                dp[i][j - 1] + delta)
    return dp
 

def spaceEfficientAlignment(x, y, mismatch, delta):
    m = len(x)
    n = len(y)
    # 2 cols, m+1 rows
    dp2 = [[0] * (2) for i in range(m+1)]
    for i in range(m+1):
        dp2[i][0] = i * delta 

    for j in range(1,n+1):
        dp2[0][1] = j*delta
        for i in range(1,m+1):
            if (x[i - 1] == y[j - 1]):
                dp2[i][1] = dp2[i-1][0]
            else:
                dp2[i][1] = min(dp2[i - 1][0] + mismatch[x[i-1]][y[j-1]] ,
                                dp2[i - 1][1] + delta,
                                dp2[i][0] + delta)
        for i in range(m+1):
            dp2[i][0] = dp2[i][1]
    #print(dp2[m][1], "rows = ",m,"cols = 2")
    lastCol = []
    for i in range(1,m+1):
        lastCol.append(dp2[i][1])
    return lastCol

def getMinimisingIndex(f,g):
    minVal = math.inf
    ind = -1
    for i in range(len(f)):
        if f[i]+g[i]<minVal:
            minVal = f[i]+g[i]
            ind = i 
    return ind

def getAlignment(dp,x,y,m,n):
    l = n + m
    i = m; j = n
    xpos = l
    ypos = l
    xans=[""]*(l+1)
    yans=[""]*(l+1)
    while ( not (i == 0 or j == 0)):
        if (x[i - 1] == y[j - 1]):
            xans[xpos] = x[i - 1]
            xpos-=1
            yans[ypos] = y[j - 1]
            ypos-=1
            i-=1
            j-=1
        elif (dp[i - 1][j - 1] + mismatch[x[i-1]][y[j-1]] == dp[i][j]):
            xans[xpos] = x[i - 1]
            xpos-=1
            yans[ypos] = y[j - 1]
            ypos-=1
            i-=1
            j-=1
        elif (dp[i - 1][j] + delta == dp[i][j]):
            xans[xpos] = x[i - 1]
            xpos-=1
            yans[ypos] = '_'
            ypos-=1
            i-=1
        elif (dp[i][j - 1] + delta == dp[i][j]):
            xans[xpos] = '_'
            xpos-=1
            yans[ypos] = y[j - 1]
            ypos-=1
            j-=1
    
    while (xpos > 0):
        if (i > 0):
            i-=1
            xans[xpos] = x[i]
            xpos-=1
        else:
            xans[xpos] = '_'
            xpos-=1
    
    while (ypos > 0):
        if (j > 0):
            j-=1
            yans[ypos] = y[j]
            ypos-=1
        else:
            yans[ypos] = '_'
            ypos-=1
 
    
    id = 1
    for i in range(l,0,-1):
        if (yans[i] == '_' and xans[i] == '_'):
            id = i + 1
            break
 
    
    # print(dp[m][n])
    # print("".join(xans[id:id+51]),"".join(xans[-50:]))
    # print("".join(yans[id:id+51]),"".join(yans[-50:]))
    return "".join(xans[id:]),"".join(yans[id:])


def divideAndConquerAlignment(X,Y):
    print(X,Y)
    m = len(X)
    n = len(Y)
    Z=""
    W=""
    if m==0:
        for i in range(n):
            Z=Z+"_"
            W=W+Y[i]
    elif n==0:
        for i in range(m):
            Z=Z+X[i]
            W=W+"_"
    elif m==1 or n==1:
        dp = basicAlignment(X,Y,mismatch,delta)
        Z,W = getAlignment(dp,X,Y,m,n)
        #print("basic : ",Z,W)
    else:
        X_L = X[:m//2]
        X_R = X[m//2:]
        X_R_rev = X_R[::-1]

        f=spaceEfficientAlignment(X_L,Y,mismatch,delta) 
        print(X_L, Y, f)
        g=spaceEfficientAlignment(X_R_rev,Y[::-1],mismatch,delta) 
        print(X_R_rev, Y[::-1], g)
        g.reverse()
        q = getMinimisingIndex(f,g)
        print(f,g,q)
        
        Z1,W1 = divideAndConquerAlignment(X_L,Y[:q+1])
        print(X_L,Y[:q+1],Z1,W1)
        Z2,W2 = divideAndConquerAlignment(X_R,Y[q+1:])
        print(X_R,Y[q+1:],Z2,W2)
        Z,W =  Z1+Z2, W1+W2
        # P.append([q,n//2])
        # print(q)
        # divideAndConquerAlignment(X[:m//2],Y_L)
        # divideAndConquerAlignment(X[m//2:],Y_R)
    return Z,W 


# gap penalty
delta = 30
# mismatch penalty
mismatch = { 
    "A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
    "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
    "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
    "T" : {"A" : 94,  "C" : 48,  "G" : 110,  "T": 0}
}


# input_file = "BaseTestcases_CS570FinalProject/input1.txt"
# X,Y=generateInputStrings(input_file)
# print(X,Y)
X="CATA"
Y = "AATA"
Z,W=divideAndConquerAlignment(X,Y)
print(Z,W)
# print(P)

dp = basicAlignment(X,Y,mismatch,delta)
Z,W = getAlignment(dp,X,Y,len(X),len(Y)) 
print(Z,W,dp[len(X)][len(Y)])
