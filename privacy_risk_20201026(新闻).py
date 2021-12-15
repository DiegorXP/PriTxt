# -*- coding: utf-8 -*-
import numpy as np
from stanfordnlp.server import CoreNLPClient
from gensim.test.utils import get_tmpfile
from gensim.models import word2vec

"""
最终：（已去停用词）
modelfilename = "./model/word2vec20200711(20).model"  # model = word2vec.Word2Vec(sentences, window=20)；
验证：
白盒：modelfilename = "./model/word2vec20200711(20).model"  # model = word2vec.Word2Vec(sentences, window=20)；
黑盒：modelfilename = "./model/word2vec20200711(3).model"  # model = word2vec.Word2Vec(sentences, window=5)；  
"""

properties = {
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


def wtype(ner):
    if ner in ('PERSON', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY', 'DATE', 'TIME', 'GPE', 'NUMBER', 'PERCENT'):
        if ner in ('CITY', 'STATE_OR_PROVINCE'):
            return 'CITY'
        return ner
    return ""


# 中文停用词
zh_stopwords = [line.strip() for line in open('./data/stopwords.txt', 'r', encoding='UTF-8').readlines()]
# print(zh_stopwords)


# 训练词向量: segmentfilename: 分词文档保存路径; modelfilename: 模型保存路径
def train(segmentfilename, modelfilename):
    print(modelfilename + " 训练开始........")
    # 加载语料
    sentences = word2vec.LineSentence(segmentfilename)
    # 创建临时文件
    path = get_tmpfile(modelfilename)
    # 训练语料，COBW
    # model = word2vec.Word2Vec(sentences, window=5)  # modelfilename = "./model/word2vec(5).model"
    model = word2vec.Word2Vec(sentences, window=20)  # modelfilename = "./model/word2vec(20).model"
    model.save(modelfilename)
    print(modelfilename + " 训练结束........")


# 预测隐私风险
def Evaluate_Risk(text, modelfilename, res):
    # 加载模型
    model = word2vec.Word2Vec.load(modelfilename)

    indicator = ["PERSON", "CITY", "COUNTRY", "DATE", "TIME", 'GPE']  # 隐私特征

    # zh-Client
    word_simi_dict = {}  # 敏感值字典，键为词，值为[词出现的次数，风险指数]
    privacy_words = []   # 敏感词
    outstr = ''  # 返回值是字符串， 分词后的文本
    with CoreNLPClient(annotators=['ner'], timeout=90000, memory='16G', properties=properties) as client:
        annotated = client.annotate(text)
        for value in annotated.sentence:
            for word in value.token:
                if word.word not in zh_stopwords:
                    if word.ner != "O":  # 找到敏感词或数字/百分数
                        tp = wtype(word.ner)
                        if tp:
                            if tp in indicator:  # 敏感词
                                privacy_words.append(word.word)
                            else:  # 数字/百分数
                                if tp not in word_simi_dict:
                                    word_simi_dict[tp] = [1, None]
                                else:
                                    word_simi_dict[tp][0] += 1

                            outstr = " ".join((outstr, tp))
                            continue

                    outstr = " ".join((outstr, word.word))
                    if word.word not in word_simi_dict:
                        word_simi_dict[word.word] = [1, None]
                    else:
                        word_simi_dict[word.word][0] += 1

    # print("[词,敏感值]字典--------------------------------\n", word_simi_dict)

    hightprivacy_words = []  # 与指示词相似度 大于0.95的词
    hightprivacy_sum1 = 0  # 与指示词相似度 大于0.95的词的个数；词重复多次都算
    sum_sim = 0  # 准敏感词总相似度
    for k, v in word_simi_dict.items():
        if not v[1]:  # 如果v[1]==None
            if k in model.wv.vocab:  # 判断一个词语是否被词典收录
                word_simi = 0
                for i in indicator:  # 计算除敏感词之外的词与隐私特征之间相似度
                    simi = model.wv.similarity(k, i)
                    if word_simi < simi:
                        word_simi = simi

                word_simi_dict[k][1] = word_simi  # word_simi_dict中的value中的第2位，表示相似度
                if word_simi >= 0.50:  # 准敏感词
                    hightprivacy_sum1 += v[0]  # 统计相似度>=0.95的个数
                    hightprivacy_words.append(k)  # 与隐私特征相似度高达0.95的词
                    sum_sim += v[0] * word_simi

    # print("（最终）[词，敏感值]字典--------------------------------\n", word_simi_dict)

    # ==============================================================================================================
    # 文本隐私风险--词重复多次都算
    print("--------------------词重复多次都算;一个敏感词由多个词构成，敏感值只算一个-----------------------")
    novacanum2 = sum([v[0] for v in word_simi_dict.values() if v[1] == None])
    print("生词个数(不去重)：", novacanum2)

    # 文档中词的个数（除敏感词和生词）
    words_sum2 = sum([v[0] for v in word_simi_dict.values() if v[1] != None and v[1] != 1.0])
    print("文档词个数（除敏感词和生词）:", words_sum2)

    # 文档的比特数（除敏感词和生词）
    words_bits2 = sum([len(k)*v[0] for k, v in word_simi_dict.items() if v[1] != None and v[1] != 1.0])
    print("文档比特数（除敏感词和生词）：", words_bits2)

    print("准敏感词个数（可重复）（相似度0.95以上）：", hightprivacy_sum1)
    print("准敏感词: ", hightprivacy_words)

    # 敏感词
    privacywords_num = len(privacy_words)  # 敏感词个数
    privacywords_bit = sum([len(num) for num in privacy_words])  # 敏感词比特数
    print("敏感词个数(重复也算)： ", privacywords_num)
    print("敏感词比特数(重复也算)： ", privacywords_bit)
    print("敏感词：", privacy_words)

    sums2 = words_sum2 + privacywords_num  # 文档词个数（除生词）
    new_risk = (sum_sim+privacywords_num)/sums2  # 文本隐私风险
    number_risk = privacywords_num/sums2  # 敏感词个数占比
    bits_risk = privacywords_bit/(words_bits2+privacywords_bit)  # 敏感词比特数占比

    print("最终结果==============")
    print("文档词个数:", sums2, "; 文档隐私风险:", new_risk)
    print("文档敏感词个数:", privacywords_num, "; 敏感词个数占比:", number_risk, "; 敏感词比特占比:", bits_risk)
    print("相似度0.95以上词个数（敏感词+准敏感词）:", hightprivacy_sum1+privacywords_num, "; 占比:", (hightprivacy_sum1+privacywords_num)/sums2)
    tmp = [new_risk, number_risk, bits_risk, sums2, privacywords_num, hightprivacy_sum1]  # [文本隐私风险, 敏感词个数占比, 敏感词比特数占比, 文档词个数, 敏感词个数, 准敏感词个数]
    res.append(tmp)

    return outstr


# 隐私风险转换成排名
def Risk_to_Ranking(res, res_path):
    print("\n结果分析：")
    print("res: ", res)

    doc_words = [line[3] for line in res]  # 文档词个数
    print("doc_words: ", doc_words)

    # 计算新方法文本隐私风险，敏感词个数占比隐私风险，敏感词比特数占比隐私风险
    PriTxt_Risk = [line[0] for line in res]
    Number_Risk = [line[1] for line in res]
    Bits_Risk = [line[2] for line in res]
    print("PriTxt_Risk: ", [round(i, 4) for i in PriTxt_Risk])
    print("Number_Risk: ", [round(i, 4) for i in Number_Risk])
    print("Bits_Risk: ", [round(i, 4) for i in Bits_Risk])

    privacy_words = [line[4] for line in res]  # 准敏感词个数
    print("privacy_words: ", privacy_words)
    hightprivacy_words = [line[5] for line in res]  # 准敏感词个数
    print("hightprivacy_words: ", hightprivacy_words)

    Risk0 = np.array(PriTxt_Risk)
    Risk1 = np.array(Number_Risk)
    Risk2 = np.array(Bits_Risk)

    PriTxt_argsort = list(np.argsort(-Risk0))
    Number_argsort = list(np.argsort(-Risk1))
    Bits_argsort = list(np.argsort(-Risk2))

    # 计算新方法文本隐私风险排名，敏感词个数占比隐私风险排名，敏感词比特数占比隐私风险排名
    PriTxt_Ranking = [0] * 10
    Number_Ranking = [0] * 10
    Bits_Ranking = [0] * 10

    for i in range(10):
        PriTxt_Ranking[PriTxt_argsort[i]] = i + 1
        Number_Ranking[Number_argsort[i]] = i + 1
        Bits_Ranking[Bits_argsort[i]] = i + 1

    print("PriTxt_Ranking: ", PriTxt_Ranking)
    print("Number_Ranking: ", Number_Ranking)
    print("Bits_Ranking: ", Bits_Ranking)

    # 保存结果
    with open(res_path, 'w', encoding='UTF-8') as w:
        for line in [doc_words, PriTxt_Risk, Number_Risk, Bits_Risk, PriTxt_Ranking, Number_Ranking, Bits_Ranking, privacy_words, hightprivacy_words]:
            w.write(str(line) + '\n')
    print("\n 结果保存完成！ ================================")


if __name__ == '__main__':
    # 分词训练文档，模型保存路径
    segmentfilename = "./data/trainset_segment.txt"

    # modelfilename = "./model/word2vec(5).model"  # model = word2vec.Word2Vec(sentences, window=5)
    modelfilename = "./model/word2vec(20).model"  # model = word2vec.Word2Vec(sentences, window=20)
    # modelfilename = "./model/word2vec(20.1).model"  # model = word2vec.Word2Vec(sentences, window=20)

    # # 训练词向量模型（只用训练一次）
    # train(segmentfilename, modelfilename)

    """
    # 要预测的新文档
    tmp_catalog = './data/'
    newfile_list = [tmp_catalog+"new.txt", tmp_catalog+"new1.txt", tmp_catalog+"new2.txt", tmp_catalog+"new3.txt", tmp_catalog+"new4.txt", tmp_catalog+"new5.txt", tmp_catalog+"new6.txt", tmp_catalog+"new7.txt", tmp_catalog+"new8.txt", tmp_catalog+"new9.txt"]
    write_list = [tmp_catalog+"new_segment.txt", tmp_catalog+"new1_segment.txt", tmp_catalog+"new2_segment.txt", tmp_catalog+"new3_segment.txt", tmp_catalog+"new4_segment.txt", tmp_catalog+"new5_segment.txt", tmp_catalog+"new6_segment.txt", tmp_catalog+"new7_segment.txt", tmp_catalog+"new8_segment.txt", tmp_catalog+"new9_segment.txt"]
    res_list = [tmp_catalog+"new_res.txt", tmp_catalog+"new1_res.txt", tmp_catalog+"new2_res.txt", tmp_catalog+"new3_res.txt", tmp_catalog+"new4_res.txt", tmp_catalog+"new5_res.txt", tmp_catalog+"new6_res.txt", tmp_catalog+"new7_res.txt", tmp_catalog+"new8_res.txt", tmp_catalog+"new9_res.txt"]

    # 估计新文档隐私程度
    for i in range(len(newfile_list)):
        res = []
        with open(write_list[i], 'w', encoding='UTF-8') as w:
            with open(newfile_list[i], 'r', encoding='utf-8') as f:
                doc_num = 0
                for line in f.readlines():
                    doc_num += 1
                    print("--------------------------------第%d篇：------------------------" % doc_num)
                    line = line.strip()
                    # print(line.split('\t')[1])
                    token_sen = Evaluate_Risk(line.split('\t')[1], modelfilename, res)
                    w.write(token_sen + '\n')
        print("\n ==========================================第%d个文本----文本隐私风险估计---验证文本分词----完成===============================================" % (i+1))

        # print(res)
        Risk_to_Ranking(res, res_list[i])

    """
    # 加载模型
    model = word2vec.Word2Vec.load(modelfilename)
    indicator = ["PERSON", "CITY", "COUNTRY", "DATE", "TIME", 'GPE']  # 隐私特征
    max_similar = []
    for s in indicator:
        print("----------------%s------------------" % s)
        tmp = model.most_similar(s, topn=100)
        max_similar.append(tmp[0][1])
        print(tmp)
    print("======================== max_similar =============================")
    print(max_similar)












