# coding: utf-8

# 上の階層のモジュールを読み込むため
import sys
import os
print(os.getcwd())
sys.path.append(os.getcwd())

import unittest
from prepare import PrepareChain


class TestImportText(unittest.TestCase):
    u"""
    テスト用クラス
    """
    def setUp(self):
        u"""
        テスト実行準備
        """
        self.text = u"おはよう。今日は、良い天気です。Hello markov.\n吾輩は猫である\r\n名前はまだない。"
        self.chain = PrepareChain(self.text)

    def test_make_chain_freqs(self):
        u"""
        全体テスト
        """
        quartet_freqs = self.chain.make_chain_freqs()
        answer = {
            (self.chain.BEGIN, u"今日", u"は", u"、"): 1,
            (u"今日", u"は", u"、", u"良い"): 1,
            (u"は", u"、", u"良い", u"天気"): 1,
            (u"、", u"良い", u"天気", u"です"): 1,
            (u"良い", u"天気", u"です", u"。"): 1,
            (u"天気", u"です", u"。", self.chain.END): 1,
            (self.chain.BEGIN, u"吾輩", u"は", u"猫"): 1,
            (u"吾輩", u"は", u"猫", u"で"): 1,
            (u"は", u"猫", u"で", u"ある"): 1,
            (u"猫", u"で", u"ある", self.chain.END): 1,
            (self.chain.BEGIN, u"名前", u"は", u"まだ"): 1,
            (u"名前", u"は", u"まだ", u"ない"): 1,
            (u"は", u"まだ", u"ない", u"。"): 1,
            (u"まだ", u"ない", u"。", self.chain.END): 1
        }
        self.assertEqual(quartet_freqs, answer)

    def test_divide(self):
        u"""
        複数の文章を1文ずつに分ける
        """
        sentence = self.chain._divide(self.text)

        answer = [u"おはよう。", u"今日は、良い天気です。", u"Hello markov.", u"吾輩は猫である", u"名前はまだない。"]
        self.assertEqual(sentence.sort(), answer.sort())

    def test_morphological_analysis(self):
        u"""
        1文の形態素解析を行う
        """
        sentence = u"今日は、良い天気です。"
        morphemes = self.chain._morphological_analysis(sentence)

        answer = [u"今日", u"は", u"、", u"良い", u"天気", u"です", u"。"]
        self.assertEqual(morphemes.sort(), answer.sort())

    def test_make_quartet(self):
        u"""
        形態素解析で分割された配列を、四つ組にして出現回数を数える
        """
        sentence = u"今日は、良い天気です。"
        morphemes = self.chain._morphological_analysis(sentence)
        quartet_freqs = self.chain._make_quartet(morphemes)

        answer = {
            (self.chain.BEGIN, u"今日", u"は", u"、"): 1,
            (u"今日", u"は", u"、", u"良い"): 1,
            (u"は", u"、", u"良い", u"天気"): 1,
            (u"、", u"良い", u"天気", u"です"): 1,
            (u"良い", u"天気", u"です", u"。"): 1,
            (u"天気", u"です", u"。", self.chain.END): 1
        }
        self.assertEqual(quartet_freqs, answer)

    def test_make_quartet_too_short(self):
        u"""
        形態素解析で分割された配列を、四つ組にして出現回数を数える
        ※ エラーパターン: 形態素が少なすぎる場合
        """
        sentence = u"良い天気。"
        morphemes = self.chain._morphological_analysis(sentence)
        quartet_freqs = self.chain._make_quartet(morphemes)

        answer = {}
        self.assertEqual(quartet_freqs, answer)

    def test_make_quartet_just_4(self):
        u"""
        形態素解析で分割された配列を、四つ組にして出現回数を数える
        ※ 形態素がちょうど四つ組
        """
        sentence = u"おはようございます。"
        morphemes = self.chain._morphological_analysis(sentence)
        quartet_freqs = self.chain._make_quartet(morphemes)

        answer = {
            (self.chain.BEGIN, u"おはよう", u"ござい", u"ます"): 1,
            (u"おはよう", u"ござい", u"ます", u"。"): 1,
            (u"ござい", u"ます", u"。", self.chain.END): 1
        }
        self.assertEqual(quartet_freqs, answer)

    def tearDown(self):
        u"""
        テスト終了
        """
        pass

if __name__ == "__main__":
    unittest.main()

