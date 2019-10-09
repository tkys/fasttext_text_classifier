# fasttext_text_classifier

 Ubuntu 18.04 LTS
* Python 3
* MeCab
* mecab-python3
* mecab-ipadic-NEologd (MeCabの新語辞書)
* fasttext



### MeCab関連の環境構築

mecabインストール、neologd辞書の用意、ipadicとか

```
$ sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file

$ pip3 install mecab-python3
```


## mecab-ipadic-NEologd：MeCabの新語辞書　mecab-ipadic-NEologdのインストール/更新方法

辞書のシードデータは、GitHubリポジトリを介して配布されます。

「git clone」し複製されたリポジトリのディレクトリに移動、
次のコマンドで、最近のmecab-ipadic-NEologdをインストールまたは更新（上書き）できます。

```
$ git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
$ cd mecab-ipadic-neologd
$ ./bin/install-mecab-ipadic-neologd -n
```
途中のメッセージからmecab-configをインストールした場合は、使用するmecab-configのパスを設定する必要があります。


次のヘルプコマンドにてコマンドラインオプションを確認できます。

```
$ ./bin/install-mecab-ipadic-neologd -h
```

### neologd辞書の場所を確認
```
$ echo `mecab-config --dicdir`"/mecab-ipadic-neologd"

/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd
```

--------
### fasttextの環境構築

fastTextのインストールは通常`pip install fasttext `。すごく楽。
ただし今回はオートチューニングを使いたいので、最新リポジトリからもってきてインストール。

```
autotune is a new feature that is not included in the last release (0.9.1). You should install the "dev" version, that is, clone the repo

$ git clone https://github.com/facebookresearch/fastText.git
$ cd fastText
$ pip install .

```



--------
## fasttext用の学習用データの作成

### インプットデータ用意

1行に　`{label},{text}　`の形式で用意します

* input.txt
```
1,変換時に、Stop Wordの処理をしたりしますが、まずはStop Word無しで学習させてみます。
3,fastTextでクラス分けをする際の教師データは、下記のようなフォーマットなのでcsvから変換します。
2,教師データとしてはあまり宜しくない感じはしますが、とりあえずfastTextに入力してみます。
1,精度は、fastTextによって予測されたラベルの中の正しいラベルの数です。リコールは、すべての実際のラベルのうち、正常に予測されたラベルの数です。これをより明確にする例を見てみましょう。
3,モデルによって予測されるラベルはですfood-safety。これは関係ありません。どういうわけか、モデルは単純な例では失敗するようです。
```

### fasttext形式ラベルと分かち書き
以下コマンドにて、 `__label__N,(分かち書き済みテキスト)`　の形式で　log.txtに出力します。
```
$python3 train_data_fasttext.py input.csv > log.txt
```


### log.txt　の確認

```
$cat log.txt
__label__1, 変換 時 に 、 Stop Word の 処理 を する たり する ます が 、 Stop Word 無し で 学習 する せる て みる ます 。
__label__3, fastText で クラス 分け を する 際 の 教師 データ は 、 下記 の よう だ フォーマット だ ので CSV から 変換 する ます 。
__label__2, 教師 データ として は あまり 宜しい ない 感じ は する ます が 、 とりあえず fastText に 入力 する て みる ます 。
__label__1, 精度 は 、 fastText によって 予測 する れる た ラベル の 中 の 正しい ラベル の 数 です 。 リコール は 、 すべて の 実際 の ラベル の うち 、 正常 に 予測 する れる た ラベル の 数 です 。 これ を より 明確 に する 例 を 見る て みる ます う 。
__label__3, モデル によって 予測 する れる ラベル は です Food - safety 。 これ は 関係 ある ます ん 。 わけ か 、 モデル は 単純 だ 例 で は 失敗 する よう です 。

```

### train_data_fasttext.py でのMeCabの分かち書き挙動とfasttext形式ラベル付けの対応

* 抽出する品詞の指定
```
# いらない品詞があるならばコメントアウト
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
```

* MeCabの辞書（mecab-ipadic-neologd）のpath指定
```
    tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
```



* fasttext形式でのラベル付け対応

```
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
```
ここではinput.csvの要素1列目の{label}が　1,2,3　でラベルしてあるケースとしています


--------



