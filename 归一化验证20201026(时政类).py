# -*- coding: utf-8 -*-
import numpy as np
from gensim.models import word2vec

# 中文停用词
zh_stopwords = [line.strip() for line in open('./data/stopwords.txt', 'r', encoding='UTF-8').readlines()]
# print(zh_stopwords)


# 敏感词重复的都算
def Attack_Verification(newsegmentfilename, modelfilename, window_size, doc_words, res):
    # 加载模型
    model = word2vec.Word2Vec.load(modelfilename)
    indicator = ["PERSON", "CITY", "COUNTRY", "DATE", "TIME", 'GPE']  # 隐私特征
    # 估计新文档泄露概率
    with open(newsegmentfilename, 'r', encoding='utf-8') as f:
        doc_num = 0
        for line in f.readlines():
            doc_num += 1
            print("--------------------------------第%d篇：------------------------" % doc_num)
            # print(line)
            probability_sum = 0
            text = line.split()
            # print("行读取：",text)
            for i in range(len(text)):
                if text[i] in indicator:
                    if i == 0:
                        word_before = []
                    else:
                        start_posi = i - window_size
                        word_before = text[start_posi:i] if start_posi >= 0 else text[:i]
                    word_after = text[i+1:i+1+window_size]
                    word_before.extend(word_after)

                    context_list = word_before
                    for j in range(len(context_list)-1, -1, -1):
                        if context_list[j] in indicator:
                            del context_list[j]
                    # print(text[i])
                    # print(context_list)
                    # print(model.predict_output_word(context_list, topn=10000))
                    probability = 0.0  # 单词预测概率
                    if context_list:
                        probability = [index[1] for index in model.predict_output_word(context_list, topn=1000000) if index[0] == text[i]][0]
                    # print(probability)
                    probability_sum += probability

            # print("总概率", probability_sum)

            max_doc = max(doc_words)
            min_doc = min(doc_words)
            # print(max_doc)
            # print(min_doc)

            doc_words1 = [(num - min_doc) / (max_doc - min_doc) + 1 for num in doc_words]
            # print(doc_words1)

            tmp = probability_sum/doc_words1[doc_num-1]
            res.append(tmp)
            print("概率均值：", tmp)


# 攻击风险转换成排名
def ASRisk_to_Ranking(res, AS_path):
    print("=======================================")
    print("结果分析：")
    print(res)
    # 验证结果排名
    res0 = np.array(res)
    res_argsort = list(np.argsort(-res0))
    AS_Ranking = [0] * 10

    for j in range(10):
        AS_Ranking[res_argsort[j]] = j + 1

    print("AS_Ranking: ", AS_Ranking)

    # 保存结果
    with open(AS_path, 'w', encoding='UTF-8') as w:
        for line in [AS_Ranking, res]:
            w.write(str(line) + '\n')


if __name__ == '__main__':
    # modelfilename = "./model/时政类/word2vec(5).model"  # model = word2vec.Word2Vec(sentences, window=5, min_count=2)
    # modelfilename = "./model/时政类/word2vec(20).model"  # model = word2vec.Word2Vec(sentences, window=20, negative=2, min_count=2)
    modelfilename = "./model/时政类/word2vec(20.1).model"  # model = word2vec.Word2Vec(sentences, window=20, negative=2, min_count=2)

    tmp_catalog = './data/时政类/'
    segment_list = [tmp_catalog + "new_segment.txt", tmp_catalog + "new1_segment.txt", tmp_catalog + "new2_segment.txt", tmp_catalog + "new3_segment.txt", tmp_catalog + "new4_segment.txt", tmp_catalog + "new5_segment.txt", tmp_catalog + "new6_segment.txt", tmp_catalog + "new7_segment.txt", tmp_catalog + "new8_segment.txt", tmp_catalog + "new9_segment.txt"]
    res_list = [tmp_catalog + "new_res.txt", tmp_catalog + "new1_res.txt", tmp_catalog + "new2_res.txt", tmp_catalog + "new3_res.txt", tmp_catalog + "new4_res.txt", tmp_catalog + "new5_res.txt", tmp_catalog + "new6_res.txt", tmp_catalog + "new7_res.txt", tmp_catalog + "new8_res.txt", tmp_catalog + "new9_res.txt"]
    # 白盒攻击
    AS_list = [tmp_catalog + "new_AS.txt", tmp_catalog + "new1_AS.txt", tmp_catalog + "new2_AS.txt", tmp_catalog + "new3_AS.txt", tmp_catalog + "new4_AS.txt", tmp_catalog + "new5_AS.txt", tmp_catalog + "new6_AS.txt", tmp_catalog + "new7_AS.txt", tmp_catalog + "new8_AS.txt", tmp_catalog + "new9_AS.txt"]
    # # 黑盒攻击
    # AS_Black_list = [tmp_catalog + "new_AS_Black.txt", tmp_catalog + "new1_AS_Black.txt", tmp_catalog + "new2_AS_Black.txt", tmp_catalog + "new3_AS_Black.txt", tmp_catalog + "new4_AS_Black.txt", tmp_catalog + "new5_AS_Black.txt", tmp_catalog + "new6_AS_Black.txt", tmp_catalog + "new7_AS_Black.txt", tmp_catalog + "new8_AS_Black.txt", tmp_catalog + "new9_AS_Black.txt"]

    window_size = 20

    for i in range(len(segment_list)):
        res = []  # 攻击场景文本隐私风险
        # 文本词汇总数
        doc_words = eval(open(res_list[i], 'r', encoding='UTF-8').readline())
        print("doc_words: ", doc_words)
        # 计算攻击场景下的隐私风险
        Attack_Verification(segment_list[i], modelfilename, window_size, doc_words, res)

        # 攻击场景隐私风险转换成排名
        ASRisk_to_Ranking(res, AS_list[i])  # 白盒攻击
        # ASRisk_to_Ranking(res, AS_Black_list[i])  # 黑盒攻击

        print("\n 第%d个文本 结果保存完成！ ================================" % (i+1))
