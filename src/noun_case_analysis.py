import matplotlib.pyplot as plt
import  pandas as pd


cols=["ID","FORM","LEMMA","UPOS","XPOS","FEATS","HEAD","DEPREL","DEPS","MISC"]
df=pd.read_csv('E:/RU_CL/data/UD_Russian-GSD-master/ru_gsd-ud-train.conllu',sep='\t',comment='#',header=None,names=cols,on_bad_lines='warn')


nouns_df=df[df['UPOS']=='NOUN'].copy()

def extract_case(feats):
    if pd.isna(feats):
        return 'Unknown'
    for pair in feats.split('|'):
        if pair.startswith('Case='):
            return pair.split('=')[1]
    return 'Unknown'
nouns_df['Case']=nouns_df['FEATS'].apply(extract_case)


case_counts=nouns_df['Case'].value_counts().reset_index()
case_counts.columns=['Case','Count']


total=case_counts['Count'].sum()
case_counts['Percentage']=(case_counts['Count']/total*100).round(2)
case_counts.to_csv('result/case_distribution.csv',index=False)

print(case_counts)

import matplotlib.pyplot as pit
plt.rcParams['font.sans-serif']=['SimHei']#设置中文字体为黑体
plt.rcParams['axes.unicode_minus']=False#解决保存图像时负号'-'显示为方块的问题

case_counts.set_index('Case')['Percentage'].plot.pie(autopct='%1.1f%%')
plt.title('俄语名词格分布')
plt.savefig('case_distrabution.png')

merged = pd.merge(nouns_df,df[['ID','DEPREL']],left_on='ID',right_on='ID',how='left')

case_deprel=merged.groupby(['Case','DEPREL']).size().unstack()
print(case_deprel.head())