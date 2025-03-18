import os
import pandas as pd
from pathlib import Path

# 读取CONLL-U文件
def load_conllu(file_path):
    sentences = []
    current_sent = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('# text = '):
                raw_text = line.strip()[8:]
            elif not line.startswith('#') and '\t' in line:
                fields = line.strip().split('\t')
                current_sent.append(fields)
            elif line == '\n' and current_sent:
                sentences.append({
                    'text': raw_text,
                    'tokens': current_sent
                })
                current_sent = []
    return sentences

# 定义 detect_instrumental 函数
def create_sentence_dict(ud_data):
    sentence_dict = {sent['text']: sent['tokens'] for sent in ud_data}
    return sentence_dict

def detect_instrumental(sentence, sentence_dict):
    tokens = sentence_dict.get(sentence)
    if tokens:
        return any('Case=Ins' in token[5] for token in tokens)
    return False

# 测试规则准确率
def test_rule_accuracy(instrumental_sents, sentence_dict, num_tests=50):
    correct = 0
    for sent in instrumental_sents[:num_tests]:
        if detect_instrumental(sent, sentence_dict):
            correct += 1
    accuracy = correct / num_tests
    return accuracy

# 保存准确率
def save_accuracy(accuracy, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"工具格检测规则准确率：{accuracy:.2%}")

# 保存错误案例
def save_false_cases(instrumental_sents, sentence_dict, output_file, num_tests=50):
    false_data = []
    for sent in instrumental_sents[:num_tests]:
        actual = True
        predicted = detect_instrumental(sent, sentence_dict)
        if predicted != actual:
            false_data.append({
                "句子": sent,
                "预测结果": predicted
            })
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(false_data).to_csv(output_file, index=False)

# 主函数
def main(conllu_file, accuracy_file, false_cases_file):
    ud_data = load_conllu(conllu_file)
    instrumental_sents = [
        sent['text'] for sent in ud_data
        if any('Case=Ins' in token[5] for token in sent['tokens'])
    ]
    sentence_dict = create_sentence_dict(ud_data)
    accuracy = test_rule_accuracy(instrumental_sents, sentence_dict)
    save_accuracy(accuracy, accuracy_file)
    save_false_cases(instrumental_sents, sentence_dict, false_cases_file)

if __name__ == "__main__":
    conllu_file = r'E:\RU_CL\data\UD_Russian-GSD-master\ru_gsd-ud-train.conllu'
    accuracy_file = r'E:\RU_CL\data\result\day4\rule_performance.txt'
    false_cases_file = r'results\day4\false_cases.csv'
    main(conllu_file, accuracy_file, false_cases_file)