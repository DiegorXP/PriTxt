# -*- coding: utf-8 -*-

def MAE(AS_Ranking, PriTxt_Ranking, Number_Ranking, Bits_Ranking):

    tmp0 = [abs(PriTxt_Ranking[i] - AS_Ranking[i]) for i in range(10)]
    tmp1 = [abs(Number_Ranking[i] - AS_Ranking[i]) for i in range(10)]
    tmp2 = [abs(Bits_Ranking[i] - AS_Ranking[i]) for i in range(10)]

    res = [sum(tmp0), sum(tmp1), sum(tmp2)]
    return res


# 计算逆序对
def Kendall_tall_distance(AS_Ranking, PriTxt_Ranking, Number_Ranking, Bits_Ranking):
    PriTxt_list = []
    Number_list = []
    Bits_list = []
    for i in range(1, 11):
        ind = AS_Ranking.index(i)
        PriTxt_list.append(PriTxt_Ranking[ind])
        Number_list.append(Number_Ranking[ind])
        Bits_list.append(Bits_Ranking[ind])

    PriTxt_count = 0
    Number_count = 0
    Bits_count = 0
    for i in range(9):
        for j in range(i+1, 10):
            if PriTxt_list[i] > PriTxt_list[j]:
                PriTxt_count += 1
            if Number_list[i] > Number_list[j]:
                Number_count += 1
            if Bits_list[i] > Bits_list[j]:
                Bits_count += 1
    return [PriTxt_count, Number_count, Bits_count]


if __name__=="__main__":
    tmp_catalog = './data/体育类/'

    res_list = [tmp_catalog + "new_res.txt", tmp_catalog + "new1_res.txt", tmp_catalog + "new2_res.txt", tmp_catalog + "new3_res.txt", tmp_catalog + "new4_res.txt", tmp_catalog + "new5_res.txt", tmp_catalog + "new6_res.txt", tmp_catalog + "new7_res.txt", tmp_catalog + "new8_res.txt", tmp_catalog + "new9_res.txt"]
    # # 白盒攻击
    # AS_list = [tmp_catalog + "new_AS.txt", tmp_catalog + "new1_AS.txt", tmp_catalog + "new2_AS.txt", tmp_catalog + "new3_AS.txt", tmp_catalog + "new4_AS.txt", tmp_catalog + "new5_AS.txt", tmp_catalog + "new6_AS.txt", tmp_catalog + "new7_AS.txt", tmp_catalog + "new8_AS.txt", tmp_catalog + "new9_AS.txt"]
    # 黑盒攻击
    AS_Black_list = [tmp_catalog + "new_AS_Black.txt", tmp_catalog + "new1_AS_Black.txt", tmp_catalog + "new2_AS_Black.txt", tmp_catalog + "new3_AS_Black.txt", tmp_catalog + "new4_AS_Black.txt", tmp_catalog + "new5_AS_Black.txt", tmp_catalog + "new6_AS_Black.txt", tmp_catalog + "new7_AS_Black.txt", tmp_catalog + "new8_AS_Black.txt", tmp_catalog + "new9_AS_Black.txt"]

    MAE_Sum = [0, 0, 0]
    Kt_Sum = [0, 0, 0]
    for i in range(len(res_list)):
        Res_Ranking = []  # 预测结果
        with open(res_list[i], 'r', encoding='utf-8') as f:
            for line in f.readlines():
                Res_Ranking.append(eval(line))

        # print("Res_Ranking:")
        # print(Res_Ranking)

        # AS_Ranking = eval(open(AS_list[i], 'r', encoding='UTF-8').readline())  # 攻击场景结果--白盒
        AS_Ranking = eval(open(AS_Black_list[i], 'r', encoding='UTF-8').readline())  # 攻击场景结果--黑盒

        PriTxt_Ranking = Res_Ranking[4]   # 新方法隐私风险
        Number_Ranking = Res_Ranking[5]  # 敏感词个数占比
        Bits_Ranking = Res_Ranking[6]  # 敏感词字符数占比

        print("AS_Ranking: ", AS_Ranking)
        print("PriTxt_Ranking: ", PriTxt_Ranking)
        print("Number_Ranking: ", Number_Ranking)
        print("Bits_Ranking: ", Bits_Ranking)

        MAE_Res = MAE(AS_Ranking, PriTxt_Ranking, Number_Ranking, Bits_Ranking)  # 计算MAE值
        Kt_distance = Kendall_tall_distance(AS_Ranking, PriTxt_Ranking, Number_Ranking, Bits_Ranking)  # 计算Kendall_tall_distance值

        print("第%d个文本--结果分析：" % (i+1))
        print("MAE: ", MAE_Res)
        print("Kendall_tall_distance: ", Kt_distance)
        print("----------------------------------------------\n")

        MAE_Sum = [MAE_Sum[j]+MAE_Res[j] for j in range(3)]
        Kt_Sum = [Kt_Sum[j]+Kt_distance[j] for j in range(3)]

    print("=========================================================\n最终结果：")
    print("MAE_Sum: ", MAE_Sum)
    print("Kt_Sum: ", Kt_Sum)
