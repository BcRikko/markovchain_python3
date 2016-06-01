マルコフ連鎖で文章を生成する
====


マルコフ連鎖を用いて適当な文章をランダムで生成するプログラム

[o-tomox/TextGenerator](https://github.com/o-tomox/TextGenerator) と [naoyashiga/GenerateText.py](https://gist.github.com/naoyashiga) を参考に書いてみた


Dependencies
----

* Python 3.5.1
* mecab-python3 v0.7


### mecab-python3を使う前に

```
$ brew install mecab
$ brew install mecab-ipadic
```


Usage
----
1. `./input.txt`に辞書となる文章を保存する
2. 辞書を作成する
3. 文章を生成する

```
# 辞書作成
$ python main.py 1

# 文章生成
$ python main.py 2
```


Files
----

### main.py
実行用プログラム  
引数（1:辞書作成、2:文章生成）を渡して実行する

### prepare.py
与えられた文章を解析し、辞書（`chain.db`）を作成する

### generate.py
辞書（`chain.db`）を用いて、文章を生成する

### input.txt
辞書をつくるための文章  
とにかく大量にあったほうがいいので、青空文庫とか使うのがオススメ

### chain.db
prepare.pyを実行したときに作成される辞書DB

### schema.sql
DB作成のためのDDL

### test/test.py
`prepare.py`のテストコード