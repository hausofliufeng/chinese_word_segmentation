import sys

from utils.dict import load_dict
from tqdm import tqdm



def cut(sentence,max_word_len):
    """
    RMM分词
    
    args:
        sentence(string) : raw sentence
        
    returns:
        list : word list
    """
    sentence=sentence.strip() # 去除首尾空格、换行后的句子
    sentence_len=len(sentence) # 当前句子长度
    result=[] # 切分结果
    
    while sentence_len>0: # 外层循环，针对当前剩余所有序列
        sub_len=min(max_word_len,sentence_len) 
        sub_sentence=sentence[-sub_len:]
        
        while sub_len>0: # 内层循环，针对选取的子序列
            if sub_sentence in word_list:
                result.append(sub_sentence)
                sentence=sentence[:sentence_len-len(sub_sentence)]
                sentence_len=len(sentence)
                break
            else:
                if sub_len>1:
                    sub_sentence=sub_sentence[1:]
                    sub_len=len(sub_sentence)
                    continue
                elif sub_len==1:
                    result.append(sub_sentence)
                    sentence=sentence[:sentence_len-len(sub_sentence)]
                    sentence_len=len(sentence)
                    break
    
    result.reverse()
    
    return result



if __name__ == '__main__':
    try:
        path_to_src=sys.argv[1]
        path_to_des=sys.argv[2]
        path_to_dict=sys.argv[3]
    except:
        print("参数不完整")
        exit()

    word_list = load_dict(path_to_dict)
    # max_word_len=max(len(word) for word in word_list) # 选择字典中最长单词
    max_word_len=17 # 手动指定最长单词

    with open(path_to_src, "r", encoding="utf8") as src:
        data=src.readlines()
        with open(path_to_des,"w",encoding="utf-8") as des:
            for line in tqdm(data):
                des.write(("  ".join(cut(line,max_word_len)))+"\n")