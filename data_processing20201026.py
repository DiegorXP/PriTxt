# -*- coding: utf-8 -*-
from stanfordnlp.server import CoreNLPClient
from collections import defaultdict
import re

Ner_list= []  # 查看ner属性有哪些
GPE_list = []  # 查看ner="GPE"属性有哪些词

properties={
            # segment
            "tokenize.language": "zh",
            "segment.model": "edu/stanford/nlp/models/segmenter/chinese/ctb.gz",
            "segment.sighanCorporaDict": "edu/stanford/nlp/models/segmenter/chinese",
            "segment.serDictionary": "edu/stanford/nlp/models/segmenter/chinese/dict-chris6.ser.gz",
            "segment.sighanPostProcessing": "true",
            # sentence split
            "ssplit.boundaryTokenRegex": "[.。]|[!?！？]+",
            # pos
            "pos.model": "edu/stanford/nlp/models/pos-tagger/chinese-distsim/chinese-distsim.tagger",
            # ner
            "ner.language": "chinese",
            "ner.model": "edu/stanford/nlp/models/ner/chinese.misc.distsim.crf.ser.gz",
            "ner.applyNumericClassifiers": "true",
            "ner.useSUTime": "false",
            # regexner
            "ner.fine.regexner.mapping": "edu/stanford/nlp/models/kbp/chinese/gazetteers/cn_regexner_mapping.tab",
            "ner.fine.regexner.noDefaultOverwriteLabels": "CITY,COUNTRY,STATE_OR_PROVINCE"
        }


# pattern_dict = {
#         'DATE': re.compile(r'\d{1,4}[年月日]$|\d{4}\/\d{1,2}\/\d{1,2}$|\d{4}[\/\-]\d{1,2}$'),
#         'TIME': re.compile(r'\d{1,2}:\d{1,2}$|\d{1,2}[点|时]$')
# }


def wtype(ner):
    if ner in ('PERSON', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY', 'DATE', 'TIME', 'GPE', 'NUMBER', 'PERCENT'):
        if ner in ('CITY', 'STATE_OR_PROVINCE'):
            return 'CITY'
        return ner
    return ""


# 停用词
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='UTF-8').readlines()]
    return stopwords


# 对句子进行分词
def seg_sentence(text, zh_stopwords):
    zh_words = []  # 查看分此结果(word.word, word.ner)
    word_dict = defaultdict(list)
    outstr = ''  # 返回值是字符串
    #  zh-Client
    with CoreNLPClient(annotators=['ner'], timeout=90000, memory='16G', properties=properties) as client:
        # Below is nlp process
        print('Analyzing...')
        annotated = client.annotate(text)
        print('process finished...')
        for value in annotated.sentence:
            for word in value.token:
                if word.word not in zh_stopwords:
                    if word != '\t':
                        zh_words.append((word.word, word.ner))
                        if word.ner not in Ner_list:
                            Ner_list.append(word.ner)
                        if word.ner == 'GPE':
                            GPE_list.append(word.word)

                        if word.ner != "O":
                            tp = wtype(word.ner)
                            if tp:
                                outstr = " ".join((outstr, tp))
                            else:
                                outstr = " ".join((outstr, word.word))
                        else:
                            outstr = " ".join((outstr, word.word))
        # print("-----zh_client----")
        # print(zh_words)
        return outstr


def tokenFile(file_path, write_path, stopwords):
    count = 0
    with open(write_path, 'w', encoding='UTF-8') as w:
        with open(file_path, 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                count += 1
                print("--------------------------------第%d篇：------------------------" % count)
                line = line.strip()
                token_sen = seg_sentence(line.split('\t')[1], stopwords)
                w.write(token_sen + '\n')
                print("第%d篇保存成功！========" % count)
    print(file_path + ' has been token and token_file_name is ' + write_path)


if __name__ == "__main__":
    stopwords_path = './data/stopwords.txt'
    tmp_catalog = './data/cnews/'
    write_catalog = './data/token/'

    Category_list = ["体育", "娱乐", "家居", "房产", "教育", "时尚", "时政", "游戏", "科技", "财经"]
    file_post_list = ['cnews.train.txt', 'cnews.test.txt', 'cnews.val.txt']
    write_post_list = ['_train_token.txt', '_test_token.txt', '_val_token.txt']

    file_list = [tmp_catalog+category+filepostname for category in Category_list for filepostname in file_post_list]
    write_list = [write_catalog+category+writepostname for category in Category_list for writepostname in write_post_list]
    # print(file_list)
    # print(write_list)

    stopwords = stopwordslist(stopwords_path)

    for i in range(len(file_list)):
        print("=========================================开始处理文本%s==================================================" % file_list[i])
        tokenFile(file_list[i], write_list[i], stopwords)

    print("\n token finished....")

    print("Ner_list: ", Ner_list)
    print("GPE_list: ", GPE_list)
