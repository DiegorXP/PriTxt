# -*- coding: utf-8 -*-

MAE_1 =[18, 18, 24]
MAE_2 = [36, 38, 32]
MAE_3 = [30, 26, 28]
MAE_4 = [30, 34, 34]
MAE_5 = [18, 20, 26]
# --------------------------------
Kt_1 = [13, 12, 15]
Kt_2 = [28, 28, 23]
Kt_3 = [15, 15, 16]
Kt_4 = [18, 20, 21]
Kt_5 =  [10, 11, 15]


MAE_SUM = [0, 0, 0]
Kt_SUM = [0, 0, 0]

MAE_list = [MAE_1, MAE_2, MAE_3, MAE_4, MAE_5]
Kt_list = [Kt_1, Kt_2, Kt_3, Kt_4, Kt_5]

for i in range(len(MAE_list)):
    MAE_SUM = [MAE_SUM[j] + MAE_list[i][j] for j in range(len(MAE_SUM))]
    Kt_SUM = [Kt_SUM[j] + Kt_list[i][j] for j in range(len(Kt_SUM))]

print("MAE_SUM: ", MAE_SUM)
print("Kt_SUM: ", Kt_SUM)