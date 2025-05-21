import pytest
from logics.functions_element import main

def test_main_valid_input():
    assert isinstance(main(5), str), "반환값이 문자열이어야 합니다"
    assert len(main(5)) == 2, "가운데 두 자리 수이므로 길이는 2여야 합니다"

def test_main_answer_for_L18():
    assert main(18) == "12", "L18의 가운데 두 자리 수는 12이어야 합니다"

def test_main_answer_for_L19():
    assert main(19) == "12", "L19의 가운데 두 자리 수는 12이어야 합니다"

def test_main_answer_for_L20():
    assert main(20) == "31", "L20의 가운데 두 자리 수는 31이어야 합니다"

def test_main_answer_for_L21():
    assert main(21) == "33", "L21의 가운데 두 자리 수는 33이어야 합니다"

def test_main_answer_for_L22():
    assert main(22) == "11", "L22의 가운데 두 자리 수는 11이어야 합니다"

def test_main_answer_for_L23():
    assert main(23) == "11", "L23의 가운데 두 자리 수는 11이어야 합니다"

def test_main_answer_for_L24():
    assert main(24) == "11", "L24의 가운데 두 자리 수는 11이어야 합니다"

def test_main_answer_for_L25():
    assert main(25) == "32", "L25의 가운데 두 자리 수는 32이어야 합니다"

def test_main_answer_for_L26():
    assert main(26) == "11", "L26의 가운데 두 자리 수는 11이어야 합니다"

def test_main_answer_for_L27():
    assert main(27) == "32", "L27의 가운데 두 자리 수는 32이어야 합니다"

def test_main_answer_for_L28():
    assert main(28) == "22", "L28의 가운데 두 자리 수는 22이어야 합니다"

def test_main_answer_for_L29():
    assert main(29) == "22", "L29의 가운데 두 자리 수는 22이어야 합니다"

def test_main_answer_for_L30():
    assert main(30) == "21", "L30의 가운데 두 자리 수는 21이어야 합니다"

def test_main_answer_for_L31():
    assert main(31) == "11", "L31의 가운데 두 자리 수는 11이어야 합니다"

def test_main_answer_for_L32():
    assert main(32) == "31", "L32의 가운데 두 자리 수는 31이어야 합니다"

def test_main_answer_for_L33():
    assert main(33) == "12", "L33의 가운데 두 자리 수는 12이어야 합니다"

def test_main_answer_for_L34():
    assert main(34) == "22", "L34의 가운데 두 자리 수는 22이어야 합니다"

def test_main_answer_for_L35():
    assert main(35) == "12", "L35의 가운데 두 자리 수는 12이어야 합니다"

def test_main_answer_for_L36():
    assert main(36) == "13", "L36의 가운데 두 자리 수는 13이어야 합니다"

def test_main_answer_for_L37():
    assert main(37) == "21", "L37의 가운데 두 자리 수는 21이어야 합니다"

def test_main_answer_for_L38():
    assert main(38) == "13", "L38의 가운데 두 자리 수는 13이어야 합니다"

def test_main_answer_for_L39():
    assert main(39) == "21", "L39의 가운데 두 자리 수는 21이어야 합니다"

def test_main_answer_for_L40():
    assert main(40) == "23", "L40의 가운데 두 자리 수는 23이어야 합니다"

def test_main_answer_for_L41():
    assert main(41) == "13", "L41의 가운데 두 자리 수는 13이어야 합니다"

def test_main_answer_for_L60():
    assert main(60) == "11", "L60의 가운데 두 자리 수는 11이어야 합니다"

def test_main_answer_for_L70():
    assert main(70) == "12", "L70의 가운데 두 자리 수는 11이어야 합니다"


