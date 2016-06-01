# coding: utf-8

import MeCab
import re
from collections import defaultdict
import sqlite3


class PrepareChain(object):
    u"""
    受け取った文章からチェーンを生成してDBに保存する
    """

    BEGIN = "__BEGIN_SENTENCE__"
    END = "__END_SENTENCE__"
    DB_PATH = "chain.db"
    DB_SCHEMA_PATH = "schema.sql"

    def __init__(self, sentences):
        u"""
        初期化
        :param sentences: 文章（インポートしたテキストファイル全体）
        """
        self.text = sentences
        self.tagger = MeCab.Tagger("-Owakati")
        # tagger.parse("")をしないと['utf-8' codec can't decode byte.]というエラーになる
        self.tagger.parse("")

    def make_chain_freqs(self):
        u"""
        形態素解析してチェーンを生成する
        :return: 形態素で分割された配列
        """
        sentences = self._divide(self.text)

        # 4つ組の出現回数を保持するdictionary
        # 3つ組で試したら制度がわるかったので…
        quartet_freqs = defaultdict(int)

        for sentence in sentences:
            # 形態素解析
            morphemes = self._morphological_analysis(sentence)
            # 4つ組をつくる
            quartets = self._make_quartet(morphemes)
            # 出現回数をカウント
            for (quartet, n) in quartets.items():
                quartet_freqs[quartet] += n

        return quartet_freqs

    def _divide(self, text):
        u"""
        句点、改行などでテキストを分割し、配列を返す
        :param text: テキスト
        :return: 分割されたテキスト（配列）
        """
        delimiter = u"。|．|\."

        sentences = re.sub(r"({0})".format(delimiter), r"\1\n", text)
        sentences = sentences.splitlines()
        sentences = [sentence.strip() for sentence in sentences]

        return sentences

    def _morphological_analysis(self, sentence):
        u"""
        1文の形態素解析を行う
        :param sentence: 1文
        :return: 形態素で分割された配列
        """
        morphemes = []

        node = self.tagger.parseToNode(sentence)
        while node:
            if node.posid != 0:
                morphemes .append(node.surface)
            node = node.next

        return morphemes

    def _make_quartet(self, morphemes):
        u"""
        形態素解析で分割された配列を、四つ組にして出現回数を数える
        :param morphemes: 形態素解析された配列
        :return: 四つ組とその出現回数の辞書 {key:四つ組(tuple) , val:出現回数}
        """
        if len(morphemes) < 4:
            return {}

        quartet_freqs = defaultdict(int)

        for i in range(len(morphemes) - 3):
            quartet = tuple(morphemes[i:i+4])
            quartet_freqs[quartet] += 1

        # BEGINを追加
        quartet = (self.BEGIN, morphemes[0], morphemes[1], morphemes[2])
        quartet_freqs[quartet] = 1

        # ENDを追加
        quartet = (morphemes[-3], morphemes[-2], morphemes[-1], self.END)
        quartet_freqs[quartet] = 1

        return quartet_freqs

    def save(self, quartet_freqs, init=False):
        u"""
        四つ組ごとにDBに保存すうｒ
        :param quartet_freqs: 四つ組とその出現回数の辞書 {key: 四つ組(tuple), val:出現回数}
        :param init: DBを初期化するかどうか
        """
        print('save', init)
        conn = sqlite3.connect(self.DB_PATH)

        if init:
           with open(self.DB_SCHEMA_PATH, 'r') as f:
               schema = f.read()
               conn.executescript(schema)

        data = [(quartet[0], quartet[1], quartet[2], quartet[3], freq) for (quartet, freq) in quartet_freqs.items()]

        statement = u"insert into chain_freqs (prefix1, prefix2, prefix3, suffix, freq) values (?, ?, ?, ?, ?)"
        conn.executemany(statement, data)

        conn.commit()
        conn.close()