# gap penalty
delta = 30
# mismatch penalty
mismatch = { 
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

input_file = "BaseTestcases_CS570FinalProject/input1.txt"
X,Y=generateInputStrings(input_file)
print(X,Y)

# sequence alignment
# output 
    # The first 50 elements and the last 50 elements of the actual alignment.
    # 2. The time it took to complete the entire solution.
    # 3. Memory required.