import pytest
from logics.functions_element import main

def test_main_valid_input():
    assert isinstance(main(5), str), "반환값이 문자열이어야 합니다"
    assert len(main(5)) == 2, "가운데 두 자리 수이므로 길이는 2여야 합니다"
    
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


@pytest.mark.parametrize("n, expected", [
    (4, "21"), (5, "12"), (8, "21"), (18, "12"), 
    (19, "12"), (20, "31"), (21, "33"), (22, "11"), (23, "11"), 
    (24, "11"), (25, "32"), (26, "11"), (27, "32"), (28, "22"), 
    (29, "22"), (30, "21"), (31, "11"), (32, "31"), (33, "12"), 
    (34, "22"), (35, "12"), (36, "13"), (37, "21"), (38, "13"), 
    (39, "21"), (40, "23"), (41, "13"), (60, "11"), (70, "12")
])
def test_main_answer_for_various_generations(n, expected):
    assert main(n) == expected, f"L{n}의 가운데 두 자리 수는 {expected}이어야 합니다"
