'''
    爬虫测试网站维基百科
    例如:https://en.wikipedia.org/wiki/Car
'''
import json
import re
import time


# 读取json文件的数据并进行处理
def processing_json():
    json_filename = "data/thekeyword_pipeline.json"
    data_filename = "data/article.txt"
    f_json = open(json_filename, 'r', encoding='utf-8')
    f_date = open(data_filename, 'w', encoding='utf-8')
    # 清空data.txt文件
    f_date.seek(0)
    f_date.truncate()
    for line in f_json.readlines():
        dic = json.loads(line)
        text = dic['p']
        if text:
            # 删除文章里中的[]标记,(),',"
            f_date.writelines(re.sub('\[[^\]]*\]|\(|\)|[\']|[\"]|,', '', text)+'\n')
    f_json.close()
    f_date.close()


# 找出含关键字的句子
def key_sentences(keyword):
    keyword_list = keyword.split(" ")
    data_filename = "data/article.txt"
    ks_filename = "result/"+keyword+"_sentence.txt"
    related_sentence = "data/relatedsentence.txt"
    f_date = open(data_filename, 'r', encoding='utf-8')
    f_ks = open(ks_filename, 'w', encoding='utf-8')
    f_related = open(related_sentence, 'w', encoding='utf-8')
    # 清空文本
    f_ks.seek(0)
    f_related.seek(0)
    f_ks.truncate()
    f_related.truncate()
    with f_date as f:
        # 将文章的句子全部变成小写，方便后面进行比较
        line = f.read().strip().lower()
        # 把文章按逗号切割成句子
        result = line.split(".")
    # 筛选出有关键字的句子
    for sentences in result:
        for word in keyword_list:
            if word in sentences:
                keysentences = "关键字："+word+"\t关键字所在的句子:"+sentences.lstrip('\n')+'\n'
                related_word = word+' '+sentences.lstrip('\n')+'\n'
                f_ks.writelines(keysentences)
                f_related.writelines(related_word)
    f_date.close()
    f_ks.close()
    f_related.close()
    return result


# 找到相关词
def related_word(keyword):
    keyword_list = keyword.split(" ")
    stopword_filename = "data/stopword.txt"
    related_sentence_filename = "data/relatedsentence.txt"
    related_words_filename = "data/relatedword.txt"
    f_stopword = open(stopword_filename,  'r', encoding='utf-8')
    f_related_sentence = open(related_sentence_filename, 'r', encoding='utf-8')
    f_related_words = open(related_words_filename, 'w', encoding='utf-8')
    f_related_words.seek(0)
    f_related_words.truncate()
    stop_word = [line.split() for line in f_stopword.readlines()]
    for sentence in f_related_sentence:
        # 删除句子的所有非字母
        the_word = re.findall('[a-z]+', sentence, re.I)
        # 删除停用词
        for i in stop_word:
            j = "".join(i)
            while j.lower() in the_word:
                the_word.remove(j.lower())
        # 删除关键词
        for k in keyword_list:
            key = "".join(k)
            while key.lower() in the_word:
                the_word.remove(key)
            f_related_words.writelines(' '.join(the_word)+'\n')
    f_stopword.close()
    f_related_sentence.close()
    f_related_words.close()


# 统计相关词
def statistical_correlative(keyword):
    related_word = open('data/relatedword.txt', 'r', encoding='utf-8')
    statistical_results = open("result/"+keyword+"_statistical.txt", 'w', encoding='utf-8')
    parameter = open('data/parameter.txt', 'w', encoding='utf-8')
    list = []
    with related_word as f:
        dictResult = {}
        for line in f.readlines():
            listMatch = re.findall('[a-zA-Z]+', line.lower())

            for eachLetter in listMatch:
                # 对句子单词进行分类并统计出现个数
                eachLetterCount = len(re.findall(eachLetter, line.lower()))
                dictResult[eachLetter] = dictResult.get(eachLetter, 0) + eachLetterCount
                list.append(eachLetter)

        # 对结果排序
        result = sorted(dictResult.items(), key=lambda d: d[1], reverse=True)
        statistical_results.writelines((''.join("%s %s\n" % each for each in result)))
    for item in set(list):
        # 生成下一轮关键字
        parameter.write(item+' ')
    related_word.close()
    statistical_results.close()
    parameter.close()


if __name__ == '__main__':
    processing_json()
    # key_word = input("输入关键字")
    print("在一个回圈中，关键字有1000左右程序需要运行约60s")
    depth = int(input("输入回圈数 (请先将关键字输入到data/parameter.txt,关键字间用空格隔开)"))
    start = time.time()
    # 控制回圈数
    for i in range(0, depth+1):
        key_word = open("data/parameter.txt", 'r', encoding='utf-8')
        keyword_list = key_word.readline().split(" ")
        for item in keyword_list:
            word = "".join(item)
            sentences = key_sentences(word)
            related_word(word)
            statistical_correlative(word)
    end = time.time()
    print("程序运行时间：%f" % (end-start))