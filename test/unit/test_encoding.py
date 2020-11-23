from napi.encoding import _is_correct_encoding

CORRECT_SUBS = """1
00:00:09,320 --> 00:00:15,000
<i>Na rządzie ciąży presja,</i>
<i>by pilnie zredukować wzrost cen jedzenia.</i>

2
00:00:15,320 --> 00:00:20,000
<i>Najnowszy indeks cen żywności wskazuje,</i>
<i>że w ciągu ostatniego półrocza</i>

3
00:00:20,320 --> 00:00:25,400
<i>wartość wielu artykułów podwoiła się,</i>
<i>co odbiło się na wzroście cen.</i>"""

INCORRECT_SUB = """ď»ż1
00:00:09,320 --> 00:00:15,000
<i>Na rzÄ…dzie ciÄ…ĹĽy presja,</i>
<i>by pilnie zredukowaÄ‡ wzrost cen jedzenia.</i>

2
00:00:15,320 --> 00:00:20,000
<i>Najnowszy indeks cen ĹĽywnoĹ›ci wskazuje,</i>
<i>ĹĽe w ciÄ…gu ostatniego pĂłĹ‚rocza</i>

3
00:00:20,320 --> 00:00:25,400
<i>wartoĹ›Ä‡ wielu artykuĹ‚Ăłw podwoiĹ‚a siÄ™,</i>
<i>co odbiĹ‚o siÄ™ na wzroĹ›cie cen.</i>"""


def test_should_detect_correct_encoding():
    assert _is_correct_encoding(CORRECT_SUBS) is True, f"Failed to detect correct encoding"


def test_should_detect_incorrect_encoding():
    assert _is_correct_encoding(INCORRECT_SUB) is False, f"Failed to detect incorrect encoding"
