import sys



punc="""
--——，。？！：；“”"'‘’,.，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥
"""



def divide(data):
    """
    将属于一句话的字组合成list
    """
    result=[[]]
    count=0
    
    for d in data:
        if d!="\n":
            result[count].append(d)
        else:
            count+=1
            result.append([])
            
    return result



def handleLine(content):
    """
    每一行转换为对应的字符串
    """
    
    content=content.replace("\n","").split("\t")
    
    word=content[0]
    try:
        flag=content[1]
    except:
        print(content)
        return
    if flag=='B':
        if word in punc:
            return content[0]+"  "
        else:
            return content[0]
    elif flag=='M':
        return content[0]
    elif flag=='E':
        return content[0]+'  '
    else:
        return content[0]+'  '



def sentenceParse(sentence):
    """
    对divive函数分出来的每句话进行组合
    """
    result=""
    for s in sentence:
        result+=handleLine(s)
        
    return result



if __name__ == '__main__':
    path_to_src=sys.argv[1]
    path_to_des=sys.argv[2]

    with open(path_to_src,"r",encoding="utf-8") as f:
        data=f.readlines()

    data=divide(data)

    with open(path_to_des,"w+",encoding="utf-8") as f:
        for d in data:
            f.writelines(sentenceParse(d)+"\n")