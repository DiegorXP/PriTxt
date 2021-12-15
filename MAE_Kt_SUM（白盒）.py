# -*- coding: utf-8 -*-
# 白盒
MAE_1 = [18, 18, 24]
MAE_2 = [28, 30, 26]
MAE_3 = [30, 32, 34]
MAE_4 = [22, 24, 28]
MAE_5 = [14, 16, 22]
# --------------------------------
Kt_1 = [11, 12, 13]
Kt_2 = [18, 20, 19]
Kt_3 = [21, 21, 22]
Kt_4 = [13, 15, 16]
Kt_5 = [7, 8, 12]


MAE_SUM = [0, 0, 0]
Kt_SUM = [0, 0, 0]

MAE_list = [MAE_1, MAE_2, MAE_3, MAE_4, MAE_5]
Kt_list = [Kt_1, Kt_2, Kt_3, Kt_4, Kt_5]

for i in range(len(MAE_list)):
    MAE_SUM = [MAE_SUM[j] + MAE_list[i][j] for j in range(len(MAE_SUM))]
    Kt_SUM = [Kt_SUM[j] + Kt_list[i][j] for j in range(len(Kt_SUM))]

print("MAE_SUM: ", MAE_SUM)
print("Kt_SUM: ", Kt_SUM)