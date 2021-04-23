import re
import sys
import numpy as np

from sentence2crf import tagGenerate,sentenceTag
from crf2sentence import sentenceParse
from fs import fread,fwrite



regRules=[
    re.compile(r'年度'),
    re.compile(r'[一二三四五六七八九零〇○0０123456789]{4}年?'),
    re.compile(r'[一二三四五六七八九十0123456789]{1,2}月'),
    re.compile(r'[一二三四五六七八九十0123456789]{1,3}日'),
    re.compile(r'[0123456789]{1,}[只个把条]{1}'),
]



def patch_gen(phrase,regRules):
    """
    让句子匹配regRules中的正则，返回匹配结果，
    
    args:
        phrase(str) : 分词后的句子，单词以两个空格分开
        regRules(list) : 正则列表
        
    returns:
        list : 包含patch的列表，列表越靠前优先级越高
    """
    phrase=phrase.replace("  ","")
    result=[]
    
    for rule in regRules:
        it=re.finditer(rule,phrase)
        for match in it:
            position=match.span()
            target=match.group()
            result.append([position,target])
            
    result=get_valid_patch(phrase,result) # 过滤出冲突的patch
            
    return result



def get_valid_patch(phrase,patches):
    """
    为句子过滤掉重叠的patch
    
    args:
        phrase(str) : 分词后的句子
        patches(list) : patch_gen产生的所有patch
        
    returns:
        list : 合规的patches
    """
    result=[]
    phrase=phrase.replace("  ","")
    flag=np.zeros(len(phrase)).astype(np.int8) # 每个word都标记为0，代表没有被修改过
    for p in patches:
        position=p[0]
        flag_new=flag
        flag_new[position[0]:position[1]]+=1 # 先将需要修改的位置+1
#         print(flag_new)
        
        if max(flag_new)>1:
            # 代表有重叠，此例规则作废
            continue
        else:
            # 没有重叠，规则可以生效
            result.append(p)
            flag=flag_new
            
    return result



def patch(phrase,regRules):
    """
    按照regRules规定的正则，去修复分词后的phrase
    
    args:
        phrase(str) : 分词后的句子，单词以两个空格分开
        regRules(list) : 正则列表
        
    returns:
        string : 修正后的分词过的句子
    """
    
    patches=patch_gen(phrase,regRules) # 获取有效patch
    
    for index,p in enumerate(patches):
        patches[index].append(tagGenerate(p[1])) # 为patch生成BMES标签
        
    [word_list,tag_list]=sentenceTag(phrase) # 获取原句每个word以及标签
    
    word_list=list(word_list)
    tag_list=list(tag_list)
    for p in patches:
        position=p[0]
        tags=list(p[2])
        tag_list[position[0]:position[1]]=tags # 用每个patch覆盖原有tag
        try:
            if tag_list[position[0]-1]=="M":
                tag_list[position[0]-1]="E" # 修正“太原2000年”这种错误，避免BM标签没有E结尾
        except:
            pass
    
    count=len(tag_list)
    sentence=[]
    for i in range(count):
        sentence.append(word_list[i]+"\t"+tag_list[i]) # word和tag组合成BMES格式数据
     
    return sentenceParse(sentence)



if __name__ == '__main__':
    path_to_src=sys.argv[1]
    path_to_des=sys.argv[2]

    data=fread(path_to_src)
    result=[]
    for d in data:
        result.append(patch(d,regRules)+"\n")

    fwrite(path_to_des,result)