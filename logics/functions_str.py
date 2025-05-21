

def generate_next_term_from_current_term(current_term: str) -> str:
    """
    args:
        current_term: str
    returns:
        next_term: str
    
    현재 term의 다음 term을 생성.
    """
    if not current_term:
        return ""
    
    next_term_parts = []
    i = 0
    n_len = len(current_term)
    while i < n_len:
        current_char = current_term[i]
        count = 1
        j = i + 1
        while j < n_len and current_term[j] == current_char:
            count += 1
            j += 1
        next_term_parts.append(str(count))
        next_term_parts.append(current_char)
        i = j
    return "".join(next_term_parts)

def get_nth_term(n: int) -> str:
    """
    args:
        n: int
    returns:
        nth_term: str
    
    n번째 개미수열 항을 생성.
    """
    if n <= 0:
        raise ValueError("n은 양의 정수여야 합니다.")
    if n == 1:
        return "1"
    
    current_term = "1"
    for _ in range(1, n): # n번째 항을 얻기 위해 n-1번 반복
        current_term = generate_next_term_from_current_term(current_term)
    return current_term

def main(n: int) -> str:
    """
    args:
        n: int
    returns:
        nth_term: str
    
    양의 정수 n이 주어질때  n번째 항(Ln)의 자릿수 중 가운데 두 자리 수(m)를 출력.
    """
    if not (3 < n < 100):
        raise ValueError("입력 n은 3보다 크고 100보다 작아야 합니다.")
    
    import time
    start_time = time.time()
    ln_term = get_nth_term(n)
    length = len(ln_term)
    print(f"get_nth_term 함수 실행 시간: {time.time() - start_time}초")
    # print(ln_term)
    if length < 2:
        raise ValueError(f"첫 항입니다.")
    
    ## 가운데 2자리 수? -> 항상 짝수 길이를 가진 항이어야 함.
    ## 개미 수열이 홀수 길이 항을 가질 수 있나?
    ## (# of digits, digit) 형태의 반복이므로, 항상 짝수 길이항을 가짐. (첫 항 제외)
    ## 홀수 길이 항은 dont care
    
    mid_start_index = (length // 2) - 1
    middle_two_digits = ln_term[mid_start_index : mid_start_index + 2]
    return middle_two_digits


