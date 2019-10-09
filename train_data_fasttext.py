import csv
import re
import sys
import MeCab

# いらない品詞（stop word）があるならばコメントアウト 
hinshi_list = [
        "名詞",
        "動詞",
        "形容詞",
        "形容動詞",
        "記号",
        "助詞",
        "助動詞",
        "副詞"
        ]


def convert2fasttext(bunrui):
    """ fastText用のラベルに変換 """
    labels = {
        "1": "__label__1",
        "2": "__label__2",
        "3": "__label__3"
        #"4": "__label__4",
        #"5": "__label__5"
    }
    return labels[bunrui]

def convert2wakati(text, tagger):

    r=[]
    mojiretu=' '
    """ わかち書きに変換 """
    node = tagger.parseToNode(text)

    while node:
        #　単語を取得
        if node.feature.split(",")[6] == '*':
            word = node.surface
        else:
            word = node.feature.split(",")[6]
        #word = node.surface

        # 品詞を取得
        hinshi = node.feature.split(",")[0]

        if hinshi in hinshi_list:
            r.append(word)
        node = node.next

    mojiretu = (' '.join(r)).strip()

    return mojiretu

def main():
    tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    with open(sys.argv[1]) as file:
        reader = csv.reader(file)
        for row in reader:
            label = convert2fasttext(row[0])
            comment = convert2wakati("".join(row[1:]), tagger)
            # comment = stopword(comment)
            print("{label}, {comment}\n".format(label=label, comment=comment), end="")

if __name__ == "__main__":
    main()
