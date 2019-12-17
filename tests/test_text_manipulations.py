from mocking_spongebob import text_manipulations

def test_mocking_case_single_word():
    assert text_manipulations.mocking_case('helloworld') == 'hElLoWoRlD'
    assert text_manipulations.mocking_case('thisisnotstatic') == 'tHiSiSnOtStAtIc'
    assert text_manipulations.mocking_case('CASEisNOTimportant') == 'cAsEiSnOtImPoRtAnT'

def test_mocking_case_multi_word():
    assert text_manipulations.mocking_case('hello world') == 'hElLo WoRlD'
    assert text_manipulations.mocking_case('the rain in spain falls mainly on the plain') == 'tHe RaIn In SpAiN fAlLs MaInLy On ThE pLaIn'

def test_mocking_case_non_alpha():
    assert text_manipulations.mocking_case('hello!world') == 'hElLo!WoRlD'
    assert text_manipulations.mocking_case('hello,world') == 'hElLo,WoRlD'
    assert text_manipulations.mocking_case('hello. world') == 'hElLo. WoRlD'
    assert text_manipulations.mocking_case('hello, world') == 'hElLo, WoRlD'
    assert text_manipulations.mocking_case('hello, world!') == 'hElLo, WoRlD!'
    assert text_manipulations.mocking_case('!hello, world!') == '!hElLo, WoRlD!'

