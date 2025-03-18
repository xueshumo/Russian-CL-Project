
import spacy
from spacy.language import Language


# 集成解析器
@Language.factory("ensemble_parser")
class EnsembleParser:
    def __init__(self, nlp, name):
        sm_nlp = spacy.load("ru_core_news_sm")
        self.sm_parser = sm_nlp.get_pipe("parser")
        lg_nlp = spacy.load("ru_core_news_lg")
        self.lg_parser = lg_nlp.get_pipe("parser")

    def __call__(self, doc):
        # 双重解析投票
        sm_doc = self.sm_parser(doc)
        lg_doc = self.lg_parser(doc)
        # 自定义融合逻辑（示例：优先选用lg结果）
        for token in doc:
            token.dep_ = lg_doc[token.i].dep_
        return doc


# 增强检测工具格的函数
def enhanced_detect_instrumental(doc):
    instrumental_tokens = []
    for token in doc:
        # 组合特征：形态+依存+上下文
        conditions = [
            'Case=Ins' in token.morph,  # 形态特征
            token.dep_ in ['obl', 'nmod'],  # 放宽依存类型
            any(child.dep_ == 'case' for child in token.children),  # 检查介词
            doc[token.head.i].pos_ in ['VERB', 'NOUN']  # 父节点词性限制
        ]
        if sum(conditions) >= 3:
            instrumental_tokens.append(token)
    return len(instrumental_tokens) > 0


# 依存关系修正规则
dep_correction_rules = {
    ('nmod', 'NOUN'): 'obl',  # 将名词的nmod修正为obl
    ('amod', 'ADJ'): 'nmod',  # 形容词修饰修正
}


# 依存关系后处理组件
@Language.component("postprocess_deps")
def postprocess_deps(doc):
    # 这里是你的依赖关系后处理逻辑
    for token in doc:
        key = (token.dep_, token.pos_)
        if key in dep_correction_rules:
            token.dep_ = dep_correction_rules[key]
    return doc


# 创建nlp对象
nlp = spacy.load("ru_core_news_lg")
nlp.add_pipe("ensemble_parser", first=True)
nlp.add_pipe("postprocess_deps", after='parser')

# 测试用例
test_cases = [
    {
        "text": "Он режет хлеб ножом",
        "expected": [("ножом", "Ins", "obl")]
    },
    {
        "text": "Письмо написано пером",
        "expected": [("пером", "Ins", "obl")]
    }
]


# 验证分析结果的函数
def validate_analysis(nlp):
    for case in test_cases:
        doc = nlp(case["text"])
        results = [
            (token.text, token.morph.get("Case")[0] if token.morph.get("Case") else None, token.dep_)
            for token in doc
        ]
        print(f"Text: {case['text']}")
        print(f"Expected: {case['expected']}")
        print(f"Results: {results}")
        assert any(r in results for r in case["expected"]), f"Failed: {case['text']}"
    print("所有测试用例通过!")


# 调用验证函数
validate_analysis(nlp)

from spacy import displacy

def interactive_debug(sentence):
    doc = nlp(sentence)
    displacy.serve(doc, style="dep", port=5000)

# 调用 interactive_debug 函数
# 注意：由于 displacy.serve 是阻塞函数，调用该函数后后续代码将无法执行
# 你可以选择注释掉 validate_analysis 函数调用，然后取消下面这行代码的注释
# interactive_debug("Он режет хлеб ножом")