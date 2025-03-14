import spacy
nlp = spacy.load("ru_core_news_sm")
text="Я люблю читать книги.Собака бежит по парку.Зимой идет снег.Президент выступил с речью.Математика — это наука о числах.Мы поедем на поезде в Санкт-Петербург.Кофе готовится из обжаренных зерен.Интернет изменил способ общения людей.Университет предлагает новые курсы.Спорт помогает поддерживать здоровье.  "
doc=nlp(text)
for token in doc:
    print(f"单词：{token.text:<15} 原型：{token.lemma_:<15} 词性：{token.pos_:<10} 详细标签：{token.tag_}")


from collections import defaultdict
pos_counter=defaultdict(int)
total_words=0
for token in doc:
    if token.pos_=="PUNCT":
        continue
    pos_counter[token.pos_]+=1
    total_words+=1
print("\n===词性分布统计===")
for pos,count in pos_counter.items():
    print(f"{pos}:{count}({count/total_words:.1%})")