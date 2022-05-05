"""Simple Tester for Kazakh grapheme-to-phoneme conversion based on the standard dialect (non-city dialect).
"""

from absl.testing import absltest
import KazakhG2P


class KazakhG2PTest(absltest.TestCase):
    def assertPron(self, grapheme: str, phoneme: str):
        self.assertEqual(KazakhG2P.to_phoneme(grapheme), phoneme)

    def testG2P(self):
        self.assertPron("seniń", "senɪŋ")
        self.assertPron("kitap", "kɪtap")
        self.assertPron("bireý", "bɪɾeyw")
        self.assertPron("alý", "aluw")
        self.assertPron("qaldym", "qχaldɯm")
        self.assertPron("qazaqstan", "qχazaqstan")
        self.assertPron("ýaqyt", "waqɯt")
        self.assertPron("óte", "ɜʷte")
        self.assertPron("osylaı", "ɣʷsɯlaj")
        self.assertPron("balalarymyzǵa", "balalaɾɯmɯzɣa")


if __name__ == '__main__':
    absltest.main()
