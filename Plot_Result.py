import matplotlib.pyplot as plt

# # 英文数据集--Kt (3篇)
# x1=[16/135, 18/135, 26/135]  # 白盒
# x2=[18/135, 20/135, 30/135]  # 黑盒

# # 英文数据集--MAE(3篇)
# x1 = [28/30, 34/30, 42/30]   # 白盒
# x2 = [28/30, 34/30, 44/30]  # 黑盒

# ---------------------------------------------------
# # 新闻类数据集 --Kt(5篇）
# x1 = [57/225, 61/225, 69/225]  # 白盒
# x2 = [64/225, 68/225, 72/225]  # 黑盒

# # 新闻类数据集 --MAE(5篇）
# x1 = [84/50, 100/50, 108/50]  # 白盒
# x2 = [102/50, 106/50, 116/50]  # 黑盒

# ---------------------------------------------------
# # 体育类数据集 --Kt(5篇）
# x1 = [65/225, 69/225, 72/225]  # 白盒
# x2 = [89/225, 91/225, 94/225]  # 黑盒

# # 体育类数据集 --MAE(5篇）
# x1 = [106/50, 108/50, 116/50]  # 白盒
# x2 = [130/50, 130/50, 136/50]  # 黑盒

# ---------------------------------------------------
# # 时政类数据集 --Kt(5篇）
# x1 = [26/225, 32/225, 32/225]  # 白盒
# x2 = [40/225, 46/225, 48/225]  # 黑盒

# # 时政类数据集 --MAE(5篇）
# x1 = [44/50, 50/50, 52/50]  # 白盒
# x2 = [64/50, 70/50, 72/50]  # 黑盒

# ---------------------------------------------------
# # 财经类数据集 --Kt(5篇）
# x1 = [36/225, 37/225, 47/225]  # 白盒
# x2 = [47/225, 50/225, 64/225]  # 黑盒

# # 财经类数据集 --MAE(5篇）
# x1 = [56/50, 60/50, 74/50]  # 白盒
# x2 = [80/50, 82/50, 100/50]  # 黑盒


# asr_list = [1, 2, 3]
asr_list = [1, 1.2, 1.4]

plt.plot(asr_list, x1, color='y', label='White_box', marker='v',lw='2', markersize='10', mfc='None', mec='y', mew=2)
plt.plot(asr_list, x2, color='b', label='Black_box', marker='^',lw='2', markersize='10', mfc='None', mec='b', mew=2)

# plt.plot(asr_list, x1,color='r',label='|W|/|T|=1',marker='v',lw='2',markersize='10',mfc='None',mec='r',mew=2)
# plt.plot(asr_list, x2,color='g',label='|W|/|T|=2',marker='^',lw='2',markersize='10',mfc='None',mec='g',mew=2)
# plt.plot(asr_list, x3,color='y',label='|W|/|T|=3',marker='s',lw='2',markersize='10',mfc='None',mec='y',mew=2)
# plt.plot(asr_list, x4,color='m',label='|W|/|T|=4',marker='d',lw='2',markersize='10',mfc='None',mec='m',mew=2)
# plt.plot(asr_list, x5,color='b',label='|W|/|T|=10000',marker='o',lw='2',markersize='10',mfc='None',mec='b',mew=2)

leg=plt.legend(loc=0, numpoints=1)  # ((plot1[0],plot2[0]),('Privacy Preserved','Without Privacy'),ncol=2)

##plt.xticks(asr_list)
plt.xticks(asr_list, ('PriTxt', 'Pri_Words', 'Pri_Characters') )

# ax=plt.xlabel('Privacy_risk_Methods')
# ay=plt.ylabel('Kendall_tall_distance')
# ay=plt.ylabel('MAE_value')

# plt.grid(lw=1)

# 英文数据集
# tt=plt.title('Author information dataset verification results (Kt)')
# tt=plt.title('Author information dataset verification results (MAE)')

# 新闻类数据集
# tt=plt.title('News_Dataset verification results (Kt)')
# tt=plt.title('News_Dataset verification results (MAE)')

# 体育类
# tt=plt.title('Sports_Dataset verification results (Kt)')
# tt=plt.title('Sports_Dataset verification results (MAE)')

# 时政类
# tt=plt.title('Current_Political_Dataset verification results (Kt)')
# tt=plt.title('Current_Political_Dataset verification results (MAE)')

# 财经类
# tt=plt.title('Financial_Dataset verification results (Kt)')
# tt=plt.title('Financial_Dataset verification results (MAE)')

# tt.set_fontsize(25)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
for t in leg.get_texts():
    t.set_fontsize(18)
# ax.set_fontsize(20)
# ay.set_fontsize(20)

plt.show()