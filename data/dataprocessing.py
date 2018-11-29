import json
import re
import pickle
# 读取json文件的数据并进行处理
def processing_json():
    json_filename = "thekeyword_pipeline.json"
    data_filename = "data.txt"
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
def key_sentences(keyword, url):
    keyword_list = keyword.split(" ")
    data_filename = "data.txt"
    ks_filename = "keysentence.txt"
    related_sentence = "relatedsentence.txt"
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
                keysentences = "关键字："+word+"\t关键字所在的句子:"+sentences.lstrip('\n')+"\t句子所在链接："+url+'\n'
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
    stopword_filename = "stopword.txt"
    related_sentence_filename = "relatedsentence.txt"
    related_words = "relatedword.txt"
    f_stopword = open(stopword_filename,  'r', encoding='utf-8')
    f_related_sentence = open(related_sentence_filename, 'r', encoding='utf-8')
    f_related_words = open(related_words, 'w', encoding='utf-8')
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
    related_word = open('relatedword.txt', 'r', encoding='utf-8')
    statistical_results = open('statisticalresults.txt', 'w', encoding='utf-8')
    with related_word as f:
        dictResult = {}
        for line in f.readlines():
            listMatch = re.findall('[a-zA-Z]+', line.lower())

            for eachLetter in listMatch:
                eachLetterCount = len(re.findall(eachLetter, line.lower()))
                dictResult[eachLetter] = dictResult.get(eachLetter, 0) + eachLetterCount
        # 对结果排序
        result = sorted(dictResult.items(), key=lambda d: d[1], reverse=True)
        statistical_results.writelines((''.join("%s %s\n" % each for each in result)))

if __name__ == '__main__':
    processing_json()
    key_word = input("输入关键字")
    url = input("爬取的网站")
    sentences = key_sentences(key_word, url)
    related_word(key_word)
    statistical_correlative(key_word)