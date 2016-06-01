# coding: utf-8

import os.path
import sqlite3
import random

from prepare import PrepareChain


class GenerateText(object):
    u"""
    マルコフ連鎖を用いて適当な文章を生成する
    """
    def __init__(self, n=5):
        u"""
        初期化
        :param n: 何文生成するか（デフォルトは5文）
        """
        self.n = n

    def generate(self):
        u"""
        文章を生成する
        :return: 生成された文章
        """
        if not os.path.exists(PrepareChain.DB_PATH):
            raise IOError(u"DBファイルが存在しません")

        conn = sqlite3.connect(PrepareChain.DB_PATH)
        conn.row_factory = sqlite3.Row

        generated_text = u""
        for i in range(self.n):
            text = self._generate_sentence(conn)
            generated_text += text
        conn.close()

        return generated_text

    def _generate_sentence(self, conn):
        u"""
        ランダムな1文を生成する
        :param conn: DBコネクション
        :return: 生成された1文
        """
        morphemes = []

        first_quartet = self._get_first_quartet(conn)
        morphemes.append(first_quartet[1])
        morphemes.append(first_quartet[2])
        morphemes.append(first_quartet[3])

        while morphemes[-1] != PrepareChain.END:
            prefix1 = morphemes[-3]
            prefix2 = morphemes[-2]
            prefix3 = morphemes[-1]

            quartet = self._get_quartet(conn, (prefix1, prefix2, prefix3))
            morphemes.append(quartet[3])

        result = "".join(morphemes[:-1])

        return result

    def _get_first_quartet(self, conn):
        u"""
        文頭になる四つ組をランダムに取得
        :param conn: DBコネクション
        :return: 文頭になる四つ組のtuple
        """
        prefixes = (PrepareChain.BEGIN,)

        chains = self._get_chain_from_DB(conn, prefixes)
        quartet = self._get_probable_quartet(chains)

        return quartet["prefix1"], quartet["prefix2"], quartet["prefix3"], quartet["suffix"]

    def _get_quartet(self, conn, prefixes):
        u"""
        条件（prefix1, prefix2, prefix3）からsuffixをランダムに取得する
        :param conn: DBコネクション
        :param prefixes: 条件(prefix1, prefix2, prefix3)
        :return: 四つ組のtuple
        """
        chains = self._get_chain_from_DB(conn, prefixes)
        quartet = self._get_probable_quartet(chains)

        return quartet["prefix1"], quartet["prefix2"], quartet["prefix3"], quartet["suffix"]

    def _get_chain_from_DB(self, conn, prefixes):
        u"""
        DBからチェーン情報を取得する
        :param conn: DBコネクション
        :param prefixes: 検索条件（prefix1, prefix2, prefix3）
        :return: チェーン情報の配列
        """

        sql = u"select prefix1, prefix2, prefix3, suffix, freq from chain_freqs where prefix1 = ?"

        if len(prefixes) >= 2:
            sql += u" and prefix2 = ?"
        if len(prefixes) >= 3:
            sql += u" and prefix3 = ?"

        result = []

        cur = conn.execute(sql, prefixes)
        for row in cur:
            result.append(dict(row))

        return result

    def _get_probable_quartet(self, chains):
        u"""
        チェーン配列の中から確率的に1つを返す
        :param chains: チェーンの配列
        :return: 確率的に選んだ四つ組
        """
        total_weight = sum(quartet["freq"] for quartet in chains)

        r = random.uniform(0, total_weight)
        s = 0.0

        for quartet in chains:
            s += quartet["freq"]
            if r < s: return quartet

        return quartet