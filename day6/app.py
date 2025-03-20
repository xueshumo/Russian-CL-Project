import streamlit as st
import spacy
from spacy import displacy

# 加载俄语模型
nlp = spacy.load("ru_core_news_sm")


# 自定义依存树渲染函数
def render_dep(doc):
    options = {"compact": True, "bg": "#f0f0f0", "font": "Arial"}
    html = displacy.render(doc, style="dep", options=options, page=False)
    return html


# 创建Web界面
st.title("俄语依存语法分析器")
text_input = st.text_input("请输入俄语句子（例如：Я люблю Москву）")

if text_input:
    with st.spinner("分析中..."):
        doc = nlp(text_input)
    st.markdown(render_dep(doc), unsafe_allow_html=True)
    st.subheader("详细分析：")
    for token in doc:
        st.write(f"单词: {token.text} → 词根: {token.lemma_} → 词性: {token.pos_} → 依存关系: {token.dep_}")
    st.success("分析完成！")