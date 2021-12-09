import sys
import psutil 
import os 
import time
def nw(A, B, simMatrix, gapPenalty):
    # The Needleman-Wunsch algorithm
    
    # Stage 1: Create a zero matrix and fills it via algorithm
    n, m = len(A), len(B)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = gapPenalty*j
    for i in range(n+1):
        mat[i][0] = gapPenalty*i
    for i in range(1, n+1):
        for j in range(1, m+1):
            mat[i][j] = min(mat[i-1][j-1] + simMatrix[A[i-1]][B[j-1]], mat[i][j-1] + gapPenalty, mat[i-1][j] + gapPenalty)

    # Stage 2: Computes the final alignment, by backtracking through matrix
    alignmentA = ""
    alignmentB = ""
    i, j = n, m
    while i and j:
        score, scoreDiag, scoreUp, scoreLeft = mat[i][j], mat[i-1][j-1], mat[i-1][j], mat[i][j-1]
        if score == scoreDiag + simMatrix[A[i-1]][B[j-1]]:
            alignmentA = A[i-1] + alignmentA
            alignmentB = B[j-1] + alignmentB
            i -= 1
            j -= 1
        elif score == scoreUp + gapPenalty:
            alignmentA = A[i-1] + alignmentA
            alignmentB = '-' + alignmentB
            i -= 1
        elif score == scoreLeft + gapPenalty:
            alignmentA = '-' + alignmentA
            alignmentB = B[j-1] + alignmentB
            j -= 1
    while i:
        alignmentA = A[i-1] + alignmentA
        alignmentB = '-' + alignmentB
        i -= 1
    while j:
        alignmentA = '-' + alignmentA
        alignmentB = B[j-1] + alignmentB
        j -= 1
    # Now return result in format: [1st alignment, 2nd alignment, similarity]
    return [alignmentA, alignmentB, mat[n][m]]

def forwards(x, y, simMatrix, gapPenalty):
    # This is the forwards subroutine.
    n, m = len(x), len(y)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = gapPenalty*j
    for i in range(1, n+1):
        mat[i][0] = mat[i-1][0] + gapPenalty
        for j in range(1, m+1):
            mat[i][j] = min(mat[i-1][j-1] + simMatrix[x[i-1]][y[j-1]],
                            mat[i-1][j] + gapPenalty,
                            mat[i][j-1] + gapPenalty)
        # Now clear row from memory.
        mat[i-1] = []
    return mat[n]    

def backwards(x, y, simMatrix, gapPenalty):
    # This is the backwards subroutine.
    n, m = len(x), len(y)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = gapPenalty*j
    for i in range(1, n+1):
        mat[i][0] = mat[i-1][0] + gapPenalty
        for j in range(1, m+1):
            mat[i][j] = min(mat[i-1][j-1] + simMatrix[x[n-i]][y[m-j]],
                            mat[i-1][j] + gapPenalty,
                            mat[i][j-1] + gapPenalty)
        # Now clear row from memory.
        mat[i-1] = []
    return mat[n]

def hirschberg(x, y, simMatrix, gapPenalty):
    # This is the main Hirschberg routine.
    n, m = len(x), len(y)
    if n<2 or m<2:
        # In this case we just use the N-W algorithm.
        return nw(x, y, simMatrix, gapPenalty)
    else:
        # Make partitions, call subroutines.
        F, B = forwards(x[:n//2], y, simMatrix, gapPenalty), backwards(x[n//2:], y, simMatrix, gapPenalty)
        partition = [F[j] + B[m-j] for j in range(m+1)]
        cut = partition.index(min(partition))
        # Clear all memory now, so that we don't store data during recursive calls.
        F, B, partition = [], [], []
        # Now make recursive calls.
        callLeft = hirschberg(x[:n//2], y[:cut], simMatrix, gapPenalty)
        callRight = hirschberg(x[n//2:], y[cut:], simMatrix, gapPenalty)
        # Now return result in format: [1st alignment, 2nd alignment, similarity]
        return [callLeft[r] + callRight[r] for r in range(3)]

gapPenalty = 30
# mismatch penalty
simMatrix = { 
    "A" : {"A" : 0,   "C" : 110, "G" : 48,  "T" : 94},
    "C" : {"A" : 110, "C" : 0,   "G" : 118, "T" : 48},
    "G" : {"A" : 48,  "C" : 118, "G" : 0,   "T" : 110},
    "T" : {"A" : 94,  "C" : 48,  "G" : 110,  "T": 0}
}
 


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
    
begin=time.time()
input_file = sys.argv[1]
X,Y=generateInputStrings(input_file)    
xAns,yAns,cost = hirschberg(X, Y,simMatrix,gapPenalty)
end=time.time()
process = psutil.Process(os.getpid())
memory=process.memory_info().rss/1024
# print(memory,cost)
f = open("time2.txt", "a")
f.write(str(end-begin)+"\n")
f.close()
f = open("mem2.txt", "a")
f.write(str(memory)+"\n")
f.close()