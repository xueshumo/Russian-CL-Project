2025-03-17 俄语名词格统计实验
异常记录
1.行号31：使用matplotlib保存图片（plt.savefig('case_distrabution.png'))时，当前使用的字体中缺少某些字符（如
CJK UNIFIED IDEOGRAPH相关的字符）
    处理：plt.rcParams['font.sans-serif']=['SimHei']#设置中文字体为黑体
plt.rcParams['axes.unicode_minus']=False#解决保存图像时负号'-'显示为方块的问题
2.行号17：extract_case函数中的return位置错误，导致Unknown占比100
  处理：将return移到循环外部
3.行号6：相对路径出现问题，原：'data/UD_Russian-GSD-master\ru_gsd-ud-train.conllu
  处理：改为绝对路径：'E:/RU_CL/data/UD_Russian-GSD-master/ru_gsd-ud-train.conllu'gi