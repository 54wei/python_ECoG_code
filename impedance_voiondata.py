import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
import pandas as pd


# #list data
# Cancan_impedance = [294, 250, 314, 274, 295, 279, 289, 274, 298, 285, 285, 275, 403, 271, 259, 295, 233, 
#                     296, 284, 283, 247, 277, 318, 307, 370, 296, 281, 291, 300, 286, 297, 289]

# Dandan_impedance = [301,276,292,287,289,282,290,278,302,288,287,279,356,277,265,265,239,303,291,
#                     290,253,283,524,313,377,287,288,289,307,293,504,296]


Qing1017_FL = [51,1597,47,49,46,30,45,67,50,34,46,45,39,42,32,36,49,55,36,24,552,42,33,45,172,374,56,41,45,43,278,51]
Qing1017_TPL = [109,55,34,58,58,793,60,273,42,38,36,38,59,38,46,55,48,44,46,38,29,50,40,31,54,44,47,35,47,50,45,39]
Qing1017_OL = [36 ,757 ,30 ,28 ,32 ,38 ,41 ,62 ,43 ,50 ,37 ,39 ,43 ,42 ,34 ,41 ,36 ,40 ,49 ,63 ,50 ,42 ,31 ,44 ,47 
               ,42 ,48 ,50 ,54 ,51 ,46 ,1695]

# 庆庆两次不同的阻抗。

Qing1230_FL = [63,47,64,51,54,60,49,50,64,64,64,65,57,56,52,57,50,45,156,56,54,46,47,60,224,57,556,55,529,67,503,116]
Qing1230_TPL = [69 ,1568 ,71 ,55 ,59 ,57 ,60 ,75 ,55 ,62 ,57 ,52 ,47 ,57 ,44 ,55 ,44 ,35 ,46 ,65 ,57 ,34 ,
                42 ,50 ,50 ,953 ,46 ,40 ,49 ,1740 ,51 ,44]
Qing1230_OL = [65 ,49 ,55 ,52 ,50 ,41 ,47 ,35 ,35 ,37 ,35 ,48 ,43 ,38 ,40 ,45 ,41 ,43 ,54 ,58 ,645 ,
               59 ,58 ,47 ,44 ,43 ,37 ,53 ,55 ,19 ,768,30]
#合并在一起
list1 = Qing1017_FL + Qing1017_TPL + Qing1017_OL
list2 = Qing1230_FL + Qing1230_TPL + Qing1230_OL

# 转换成一个DataFrame对象，并指定列名为A,B,C,D,E
df = pd.DataFrame({'First month': list1,'Sixth Month': list2})

# 使用violinplot函数绘制小提琴图，并使用DataFrame对象作为数据参数，指定x参数为列名，指定palette参数为"Set3"来设置颜色方案
ax = sns.violinplot(data=df,trim = False)

# 设置字体为SimHei
# # plt.rcParams['font.sans-serif'] = ['SimHei']
# ax = sns.violinplot(data=[Cancan_impedance,Dandan_impedance] )

# 使用stripplot函数绘制散点图，并设置jitter,size,color等参数
sns.stripplot(data=[list1,list2], jitter=0.1, size=5, color='red', ax=ax)
# 修改横坐标的标签
ax.set_xticklabels(['First month','Third Month'])
plt.xticks(fontsize=14)
# 显示图形
plt.show()
# median = np.median(Cancan_impedance)
# print("Median:", median)