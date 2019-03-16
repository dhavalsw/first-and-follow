import argparse

def readInputFile(file):
    f = open(file)
    map1 = {}
    for line in f:
        line = line.replace('\n','')  
        rules = line.split(':') 
        rules[0] = rules[0].strip()

        if "|" in rules[1]:
            sub_array = rules[1].split('|')
            map1[rules[0]] = []
            sub_rules = [x.split(" ") for x in sub_array]
            for x in sub_rules:
                tmp  = []
                for y in x:
                    tmp.append(y.strip())    
                
                map1[rules[0]].append([z for z in tmp if not z == ""] )

        else:
            map1[rules[0]] = [[x.strip() for x in rules[1].split(" ") if not x == ""]]
       
    return map1

def remove_duplicates(values):
    output = []
    seen = []
    for value in values:
        if value not in seen:
            output.append(value)
            seen.append(value)
    return output
        
def first(var,map):
    first1 = []
    for val in map[var]:
        for i,value in enumerate(val) :
            boll = False
            if value == 'epsilon':
                first1.append(value)
            elif value.islower() :
                first1+=value
            else :
                first2 = first(value,map)
                first1 += first2
                if 'epsilon' in first2:
                    if not i == len(val)-1 :
                        first3 = first(val[i+1],map)
                        first1 += first3
                else :
                    boll = True
                    break
        
    first1 = remove_duplicates(first1)
    return first1              

def getFirst(map) :
    first_dict = {}
    for key, value in map.items():
        key_first = first(key,map)
        first_dict[key] = key_first
    return first_dict 

def follow(var,map):
    follow1 = []
    if list(map.keys()).index(var) == 0 :
        follow1 += '$'
    for key,value in map.items():
        for val in value :
            if var == val[-1] :
                        follow1 += follow(key,map)
            for i,v in enumerate(val) :
                if v == var and i+1 <= len(val)-1:
                    if val[i+1].islower() :
                        follow1 += val[i+1]
                    else :
                        firstofNext = first(val[i+1],map)
                        if 'epsilon' in firstofNext:
                            firstofNext.remove('epsilon')
                            follow1 += follow(val[i+1],map)
                        follow1 += firstofNext
                    



            

    return follow1
def getFollow(map):
    follow_dict = {}
    for key, value in map.items():
        key_follow = follow(key,map)
        follow_dict[key] = key_follow
    return follow_dict
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()
    mappy=readInputFile(args.file)
    first_list = getFirst(mappy)
    follow_list = getFollow(mappy)
    f = open("task_5_1_result.txt", "w")
    for key,value in first_list.items() :
        f.write(key+' : ')
        for v in value :
            f.write(v)
            if not v is value[-1]:
                f.write(' ')
            else :
                f.write(' : ')
                follow_of_key = follow(key,mappy)
                for v in follow_of_key :
                    f.write(v+' ')  
        f.write('\n')    
      
    f.close()