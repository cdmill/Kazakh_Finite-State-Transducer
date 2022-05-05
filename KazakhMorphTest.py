"""Simple Tester for Kazakh morphology generation that handles vowel & consonant harmonies.
"""

from absl.testing import absltest
import KazakhMorphology


class KazakhMorphTest(absltest.TestCase):
    def assertMorph(self, input_word: str, expected: str):
        self.assertEqual(KazakhMorphology.inflect(input_word), expected)

    def testG2P(self):
        # Verbal Tests
        #
        # Negative Tests
        self.assertMorph("sený+NEG", "senbeý")
        self.assertMorph("jazý+NEG", "jazbaý")
        self.assertMorph("qulý+NEG", "qulmaý")
        self.assertMorph("jeý+NEG", "jemeý")
        self.assertMorph("satý+NEG", "satpaý")
        self.assertMorph("kótý+NEG", "kótpeý")
        # Causative Tests
        self.assertMorph("sený+CAUSE", "sendirý")
        self.assertMorph("jazý+CAUSE", "jazdyrý")
        self.assertMorph("qulý+CAUSE", "quldyrý")
        self.assertMorph("jeý+CAUSE", "jetý")
        self.assertMorph("satý+CAUSE", "sattyrý")
        self.assertMorph("kótý+CAUSE", "kóttirý")
        # Passive Tests
        self.assertMorph("sený+PASS", "senilý")
        self.assertMorph("alý+PASS", "alyný")
        self.assertMorph("jazý+PASS", "jazylý")
        self.assertMorph("qulý+PASS", "qulyný")
        # Present Participle Tests
        self.assertMorph("sený+PRES-PTCP", "senetin")
        self.assertMorph("alý+PRES-PTCP", "alatyn")
        self.assertMorph("jeý+PRES-PTCP", "jeıetin")
        # Past Participle Tests
        self.assertMorph("sený+PAST-PTCP", "sengen")
        self.assertMorph("jazý+PAST-PTCP", "jazǵan")
        self.assertMorph("jeý+PAST-PTCP", "jegen")
        self.assertMorph("satý+PAST-PTCP", "satqan")
        self.assertMorph("kótý+PAST-PTCP", "kótken")

        # Non-Verb Morphological Tests
        #
        # Plural Tests
        self.assertMorph("bala+PLR", "balalar")
        self.assertMorph("kirpi+PLR", "kirpiler")
        self.assertMorph("sóz+PLR", "sózder")
        self.assertMorph("adam+PLR", "adamdar")
        self.assertMorph("mektep+PLR", "mektepter")
        self.assertMorph("qazaq+PLR", "qazaqtar")
        # Possessive Tests
        self.assertMorph("bala+1SING-POSS", "balam")
        self.assertMorph("bala+PLR+1SING-POSS", "balalarym")
        self.assertMorph("adam+2SING-POSS", "adamyń")
        self.assertMorph("adam+PLR+2SING-POSS", "adamdaryń")
        self.assertMorph("mektep+1PLR-POSS", "mektepimiz")
        self.assertMorph("qala+1PLR-POSS", "qalamyz")
        self.assertMorph("bala+2PLR-POSS", "balańyz")
        self.assertMorph("bala+PLR+2PLR-POSS", "balalaryńyz")
        self.assertMorph("kirpi+3-POSS", "kirpisi")
        self.assertMorph("kirpi+PLR+3-POSS", "kirpileri")
        # Accusative Case Tests
        self.assertMorph("qala+ACC", "qalany")
        self.assertMorph("qazaq+ACC", "qazaqty")
        self.assertMorph("sóz+ACC", "sózdi")
        self.assertMorph("adam+ACC", "adamdy")
        self.assertMorph("shymkent+ACC", "shymkentti")
        # Genitive Case Tests
        self.assertMorph("qala+GEN", "qalanyń")
        self.assertMorph("shymkent+GEN", "shymkenttiń")
        self.assertMorph("sóz+GEN", "sózdiń")
        self.assertMorph("qazaq+GEN", "qazaqtyń")
        # Dative Case Tests
        self.assertMorph("bala+DAT", "balaǵa")
        self.assertMorph("qazaq+DAT", "qazaqqa")
        self.assertMorph("sóz+DAT", "sózge")
        self.assertMorph("mektep+DAT", "mektepke")
        # Locative Case Tests
        self.assertMorph("qala+LOC", "qalada")
        self.assertMorph("kól+LOC", "kólde")
        self.assertMorph("saıt+LOC", "saıtta")
        self.assertMorph("mektep+LOC", "mektepte")
        # Ablative Case Tests
        self.assertMorph("qala+ABL", "qaladan")
        self.assertMorph("qazaqstan+ABL", "qazaqstannan")
        self.assertMorph("shymkent+ABL", "shymkentten")
        self.assertMorph("kól+ABL", "kólden")
        # Instrumental Case Tests - NOTE: only conforms to consonant harmony
        self.assertMorph("qala+INS", "qalamen")
        self.assertMorph("qazaqstan+ABL+INS", "qazaqstannanmen")
        self.assertMorph("sóz+INS", "sózben")
        self.assertMorph("mektep+INS", "mekteppen")

        # Test Concatenations
        self.assertMorph("bala+1SING-POSS+DAT", "balama")
        self.assertMorph("kirpi+1PLR-POSS+DAT", "kirpimize")
        self.assertMorph("sóz+2SING-POSS+DAT", "sózińe")
        self.assertMorph("bala+3-POSS+DAT", "balasyna")
        self.assertMorph("bala+3-POSS+LOC", "balasynda")
        self.assertMorph("kirpi+3-POSS+LOC", "kirpisinde")
        self.assertMorph("bala+3-POSS+ABL", "balasynan")
        self.assertMorph("kirpi+3-POSS+ABL", "kirpisinen")


if __name__ == '__main__':
    absltest.main()
