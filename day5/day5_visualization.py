# day5_visualization.py
import spacy
from spacy import displacy
from pathlib import Path
# 正确的导入语句，顶格写
from webdriver_manager.chrome import ChromeDriverManager

# 加载俄语模型
nlp = spacy.load("ru_core_news_sm")

# 需要分析的句子（按需修改）
sentences = [
    "Я читаю книгу о искусственном интеллекте",  # 我在读一本关于人工智能的书
    "Собака гонится за кошкой по улице",        # 狗在街上追猫
    "Преподаватель объясняет студентам теорию грамматики"  # 老师向学生讲解语法理论
]

# 创建保存目录
output_dir = Path("dependency_trees")
output_dir.mkdir(exist_ok=True)

# 批量生成并保存依存树
for i, sent in enumerate(sentences, 1):
    doc = nlp(sent)
    html = displacy.render(doc, style="dep", page=True, options={'compact': True})
    # 在displacy渲染后插入meta标签
    html = html.replace('<head>', '<head>\n<meta charset="UTF-8">')

    # 保存为HTML
    output_path = output_dir / f"sentence_{i}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已生成：{output_path}")

