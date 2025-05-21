import pytest
from logics.functions_str import generate_next_term_from_current_term, get_nth_term, main

def test_first_term():
    assert generate_next_term_from_current_term("1") == "11", "L1='1' -> '11'"

def test_second_term():
    assert generate_next_term_from_current_term("11") == "21", "L2='11' -> '21'"

def test_third_term():
    assert generate_next_term_from_current_term("21") == "1211", "L3='21' -> '1211'"

def test_fourth_term():
    assert generate_next_term_from_current_term("1211") == "111221", "L4='1211' -> '111221'"

def test_fifth_term():
    assert generate_next_term_from_current_term("111221") == "312211", "L5='111221' -> '312211'"

def test_get_nth_term_1():
    assert get_nth_term(1) == "1", "n=1"

def test_get_nth_term_2():
    assert get_nth_term(2) == "11", "n=2" 

def test_get_nth_term_3():
    assert get_nth_term(3) == "21", "n=3"

def test_get_nth_term_4():
    assert get_nth_term(4) == "1211", "n=4"

def test_get_nth_term_5():
    assert get_nth_term(5) == "111221", "n=5"
        
def test_main_solve_4th_term():
    assert main(4) == "21", "n=4, L4='1211'"

def test_main_solve_5th_term():
    assert main(5) == "12", "n=5, L5='111221'"

def test_main_solve_8th_term():
    assert main(8) == "21", "n=8, L8='1113213211' (문제 예시)"

def test_main_solve_n_less_than_3():
    with pytest.raises(ValueError, match=r"입력 n은 3보다 크고 100보다 작아야 합니다."):
        main(3)
    with pytest.raises(ValueError, match=r"입력 n은 3보다 크고 100보다 작아야 합니다."):
        main(2)

def test_main_solve_n_greater_than_100():
    with pytest.raises(ValueError, match=r"입력 n은 3보다 크고 100보다 작아야 합니다."):
        main(100)
    with pytest.raises(ValueError, match=r"입력 n은 3보다 크고 100보다 작아야 합니다."):
        main(101)
