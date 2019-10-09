import unittest
from mocking_spongebob import text_manipulations

class TextManipulationsTestCase(unittest.TestCase):
    def test_mocking_case_single_word(self):
        assert text_manipulations.mocking_case('helloworld') == 'hElLoWoRlD'
        assert text_manipulations.mocking_case('thisisnotstatic') == 'tHiSiSnOtStAtIc'
        assert text_manipulations.mocking_case('CASEisNOTimportant') == 'cAsEiSnOtImPoRtAnT'

    def test_mocking_case_multi_word(self):
        assert text_manipulations.mocking_case('hello world') == 'hElLo WoRlD'
        assert text_manipulations.mocking_case('the rain in spain falls mainly on the plain') == 'tHe RaIn In SpAiN fAlLs MaInLy On ThE pLaIn'

    def test_mocking_case_non_alpha(self):
        assert text_manipulations.mocking_case('hello!world') == 'hElLo!WoRlD'
        assert text_manipulations.mocking_case('hello,world') == 'hElLo,WoRlD'
        assert text_manipulations.mocking_case('hello. world') == 'hElLo. WoRlD'
        assert text_manipulations.mocking_case('hello, world') == 'hElLo, WoRlD'
        assert text_manipulations.mocking_case('hello, world!') == 'hElLo, WoRlD!'
        assert text_manipulations.mocking_case('!hello, world!') == '!hElLo, WoRlD!'

if __name__ == '__main__':
    unittest.main()
