import sys
import getopt

from tqdm import tqdm


def tagGenerate(word):
    """
    接收单词，为单词打上BMES标签，标点符号按B处理。
    输出是标签字符串：'BE'
    
    args:
        word(str)
        
    returns:
        string
    """
    
    punc="""
    --——，。？！：；“”"'‘’,.，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥
    """
    if word in punc:
        return 'B'*len(word)
    else:
        count=len(word)
        if count==1:
            return 'S'
        elif count==2:
            return 'BE'
        else:
            return 'B'+(count-2)*'M'+'E'



def sentenceTag(sentence):
    """
    为每条分词后的语句打标签
    原句中间无意义空格会删除
    
    args:
        sentence(str) # "我  爱  中国  ！  "
        
    returns:
        list[sentence,tags] # ['我爱中国！','SSBEB']
    """
    
    word_list=sentence.replace("\n",'').split("  ")
    if word_list[-1]=="":
        word_list.pop()
    
    result=['','']
    for w in word_list:
        result[0]+=w
        result[1]+=tagGenerate(w)
        
    return result



def dataGenerate(x):
    """
    """
    
    result=[]
    sentence=x[0]
    tag=x[1]
    
    for index,word in enumerate(sentence):
        result.append(word+' '+tag[index]+'\n')
        
    result.append("\n")
        
    return result



if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:],"hi:o:m:")

    for opt, arg in opts:
        if opt == '-i':
            path_to_src=arg
        elif opt in ('-o'):
            path_to_des= arg
        elif opt in ('-m'):
            mode=arg
        elif opt in ('-h'):
            print('sentence2crf.py -i <inputfile> -o <outputfile> -m <mode> #模式1带tag，模式2不带tag')
            exit()


    if mode=='2':
        with open(path_to_src,"r",encoding="utf-8") as f:
            data=f.readlines()

        with open(path_to_des,"w+",encoding="utf-8") as f:
            for sentence in tqdm(data):
                for char in sentence:
                    if char==" ":
                        pass # 原句有空格，形成BMES文件时要删除，否则会造成句子边界 识别错误
                    elif char!="\n":
                        f.writelines(char+'\n')
                    else:
                        f.writelines("\n")
    elif mode=='1':
        with open(path_to_src,"r",encoding="utf-8") as f:
            data=f.readlines()

        with open(path_to_des,"w+",encoding="utf-8") as f:
            for sentence in tqdm(data):
                f.writelines(dataGenerate(sentenceTag(sentence)))