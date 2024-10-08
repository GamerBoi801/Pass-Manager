from main import encrypt_mine

def test_1():
    assert encrypt_mine('111111') == '111111'
    assert encrypt_mine('Elmo') == 'Hopr'

def test_2():
    assert encrypt_mine('Geese Howrd') == 'Jhhvh Krzug'
    assert encrypt_mine('Julius Ceasar') == 'Mxolxv Fhdvdu'

def test3():
    assert encrypt_mine('The quick brown fox jumped over the lazy dog. ') == 'Wkh txlfn eurzq ira mxpshg ryhu wkh odcb grj. '
    assert encrypt_mine('testing one two three.') == 'whvwlqj rqh wzr wkuhh.'
    assert encrypt_mine('THIS IS A TEST.') == 'WKLV LV D WHVW.'

def quote_test():
    assert encrypt_mine('In the middle of difficulty lies opportunity.') == 'Lq wkh plggoh ri glfficxowlhv olhv rSruqlw\ty.'