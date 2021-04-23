import sys
from fs import fread,fwrite



if __name__ == '__main__':
    path_to_src=sys.argv[1]
    path_to_des=sys.argv[2]
    
    data=fread(path_to_src)
    result=[]

    for d in data:
        result.append(d.replace("  ",""))

    fwrite(path_to_des,result)