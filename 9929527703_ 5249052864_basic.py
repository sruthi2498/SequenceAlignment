# gap penalty
# mismatch penalty
# input generator : read from input.txt
# sequence alignment
# output 
    # The first 50 elements and the last 50 elements of the actual alignment.
    # 2. The time it took to complete the entire solution.
    # 3. Memory required.
    
#function to get alignment
def getAlignment(x, y, pxy, pgap):
    m = len(x)
    n = len(y)
    
    dp=[[0] * (n+1) for i in range(m+1)]
    
    for i in range(m+1):
        dp[i][0] = i * pgap
        
    for i in range(n+1):
        dp[0][i] = i * pgap
    
    for i in range(1,m+1):
        for j in range(1,n+1):
            if (x[i - 1] == y[j - 1]):
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + pxy ,
                                dp[i - 1][j] + pgap,
                                dp[i][j - 1] + pgap)
 

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
        elif (dp[i - 1][j - 1] + pxy == dp[i][j]):
            xans[xpos] = x[i - 1]
            xpos-=1
            yans[ypos] = y[j - 1]
            ypos-=1
            i-=1
            j-=1
        elif (dp[i - 1][j] + pgap == dp[i][j]):
            xans[xpos] = x[i - 1]
            xpos-=1
            yans[ypos] = '_'
            ypos-=1
            i-=1
        elif (dp[i][j - 1] + pgap == dp[i][j]):
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
 
    
    print(dp[m][n])
    print(xans[id:])
    print(yans[id:])
    return

getAlignment("AGGGCT","AGGCA",3,2)