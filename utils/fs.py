# 封装常用的按行读数据和写数据的函数



def fread(fileName):
    """
    read file data by line

    args:
        fileName(str)

    returns:
        list
    """

    with open(fileName,'r',encoding="utf-8") as f:
        data=f.readlines()

    return data



def fwrite(fileName,data):
    """
    write file data by line

    args:
        fileName(str)
        data(list)

    returns:
        None
    """

    with open(fileName,'w+',encoding="utf-8") as f:
        for d in data:
            f.writelines(d)