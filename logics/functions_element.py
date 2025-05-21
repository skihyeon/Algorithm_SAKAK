import re
import os
import time
from typing import List, Dict, Optional, Any, Union

def parse_elements_from_html(html_content: str) -> Dict[str, Dict[str, Any]]:
    """
    제공된 HTML 내용에서 콘웨이 원소 정보를 파싱하여 elements_db를 생성합니다.
    """
    elements_db = {}
    
    try:
        # HTML 테이블의 각 row를 분리 (<table>...</table> 내부의 <tr>...</tr>)
        table_match = re.search(r"<table.*?>(.*?)</table>", html_content, re.DOTALL | re.IGNORECASE)
        if not table_match:
            raise ValueError("HTML에서 테이블(table)을 찾을 수 없습니다.")
        
        table_content = table_match.group(1)
        rows_html = re.findall(r"<tr.*?>(.*?)</tr>", table_content, re.DOTALL | re.IGNORECASE)
        
        if not rows_html:
            raise ValueError("HTML에서 테이블 행(tr)을 찾을 수 없습니다.")

        # 첫 번째 행은 헤더이므로 건너뜁니다.
        for row_data in rows_html[1:]: 
            cols = re.findall(r"<td.*?>(.*?)</td>", row_data, re.DOTALL | re.IGNORECASE)
            
            if len(cols) < 4:  # 필요한 열(Element Symbol, Evolution, String)이 충분한지 확인
                continue

            # 2번째 열: 원소 기호 (Symbol)
            b_content_match = re.search(r"<b>(.*?)</b>", cols[1], re.DOTALL | re.IGNORECASE)
            if not b_content_match:
                continue 
            
            element_symbol = re.sub(r"<[^>]+>", "", b_content_match.group(1)).strip()
            # 기호가 알파벳 대문자로 시작하고 (선택적으로 소문자 한 글자) 구성되었는지 확인
            if not re.fullmatch(r"[A-Z][a-z]?", element_symbol): 
                continue

            # 3번째 열: 변환 규칙 (Evolution)
            evolution_html = cols[2]
            decays_to_symbols = []
            
            if "(stable)" in evolution_html:  # 안정적인 경우
                # <b>H</b> (stable) 에서 H를 추출
                stable_match = re.search(r"<b>([a-zA-Z][a-z]?)</b>\s*\(stable\)", evolution_html, re.IGNORECASE)
                if stable_match:
                    decays_to_symbols = [stable_match.group(1).strip()]
                else:  # 안정 표시는 있지만 기호를 못 찾으면 현재 원소 기호 사용
                    decays_to_symbols = [element_symbol] 
            else:  # 다른 원소들로 변환되는 경우
                decay_links = re.findall(r"<a[^>]*>(.*?)</a>", evolution_html, re.DOTALL | re.IGNORECASE)
                for link_content in decay_links:
                    symbol_in_link = re.sub(r"<[^>]+>", "", link_content).strip()
                    if re.fullmatch(r"[A-Z][a-z]?", symbol_in_link):  # 유효한 기호 형식인지 확인
                         decays_to_symbols.append(symbol_in_link)
            
            # 변환 정보가 없으면 자기 자신으로 (방어적 처리)
            if not decays_to_symbols and "(stable)" not in evolution_html:
                decays_to_symbols = [element_symbol]

            # 4번째 열: 원소 문자열 (String)
            element_string_html = cols[3]
            element_string_match = re.search(r"<font[^>]*>(.*?)</font>", element_string_html, re.DOTALL | re.IGNORECASE)
            if element_string_match:
                element_string = re.sub(r"<[^>]+>", "", element_string_match.group(1)).strip()
            else:  # font 태그가 없는 경우, <td> 내부의 숫자를 직접 찾음
                element_string = re.sub(r"<[^>]+>", "", element_string_html).strip()

            if not element_string.isdigit():  # 문자열이 숫자로만 구성되어 있는지 확인
                continue  # 유효하지 않으면 이 원소는 건너뜀
                
            elements_db[element_symbol] = {
                'string': element_string,
                'length': len(element_string),
                'decays_to': decays_to_symbols
            }

    except Exception as e:
        raise

    if not elements_db:
        raise ValueError("HTML에서 원소 데이터를 추출하지 못했습니다. HTML 구조를 확인하거나 파싱 로직을 점검해주세요.")
        
    return elements_db


def evolve_sequence(current_element_sequence: List[str], db: Dict[str, Dict[str, Any]]) -> List[str]:
    """한 세대 진화시키는 함수"""
    next_sequence = []
    for element_name in current_element_sequence:
        if element_name not in db:
            continue  # 정의되지 않은 원소는 건너뜀

        element_data = db[element_name]
        if not element_data.get('decays_to'):  # decays_to가 비어있거나 없는 경우 (안정적)
             next_sequence.append(element_name)
        else:
            next_sequence.extend(element_data['decays_to'])
    
    return next_sequence


def get_middle_two_digits_of_Ln(
    initial_sequence_elements: List[str], 
    start_generation_num: int, 
    target_generation_num: int, 
    db: Dict[str, Dict[str, Any]]
) -> Optional[str]:
    """
    주어진 초기 원소 시퀀스에서 시작하여 목표 세대의 가운데 두 자리 숫자를 찾습니다.
    """
    current_sequence = list(initial_sequence_elements)  # 원본 수정을 피하기 위해 복사
    
    for gen in range(start_generation_num, target_generation_num):
        current_sequence = evolve_sequence(current_sequence, db)
        if not current_sequence:
            return None

    # 목표 세대(Ln)의 총 길이 계산
    total_length_Ln = 0
    # 진화 후 최종 시퀀스에서 DB에 없는 원소가 포함될 가능성을 배제하기 위해 필터링
    valid_final_sequence = []
    
    for element_name in current_sequence:
        if element_name in db:
            total_length_Ln += db[element_name]['length']
            valid_final_sequence.append(element_name)
    
    current_sequence = valid_final_sequence  # 유효한 원소들로만 구성된 시퀀스로 업데이트

    if total_length_Ln == 0:
        return None

    # 가운데 두 자리의 인덱스 계산 (0-based)
    # 길이가 L일 때, 가운데 두 자리는 (L-1)//2 와 L//2
    mid1_idx = (total_length_Ln - 1) // 2
    mid2_idx = total_length_Ln // 2 

    # 가운데 두 자리 숫자 찾기
    char1, char2 = None, None
    current_pos = 0
    
    for element_name in current_sequence:  # 유효한 원소 시퀀스 사용
        element_info = db[element_name]
        el_len = element_info['length']
        el_str = element_info['string']

        # mid1_idx가 현재 원소 내에 있는지 확인
        if char1 is None and mid1_idx >= current_pos and mid1_idx < current_pos + el_len:
            char1 = el_str[mid1_idx - current_pos]

        # mid2_idx가 현재 원소 내에 있는지 확인
        if char2 is None and mid2_idx >= current_pos and mid2_idx < current_pos + el_len:
            char2 = el_str[mid2_idx - current_pos]

        if char1 is not None and char2 is not None:  # 두 자리 모두 찾았으면 종료
            break 

        current_pos += el_len
    
    # 결과 문자 구성
    if total_length_Ln == 0:
        return "??"

    res_char1 = char1 if char1 is not None else "?"
    res_char2 = char2 if char2 is not None else "?"
        
    return res_char1 + res_char2


def get_nth_middle_two_digits_for_less_than_8(n: int) -> str:
    """
    8 미만의 수에 대해선 주어진 값으로 반환.
    """
    if n < 4 or n > 7:
        raise ValueError("입력 n은 3보다 크고 100보다 작아야 합니다.")
    
    result_map = {
        4: "21",
        5: "12",
        6: "22",
        7: "12"
    }
    return result_map[n]


def main(n: int) -> str:
    """
    주어진 n에 대해 콘웨이 원소 시퀀스의 n번째 세대 가운데 두 자리 숫자를 계산합니다.
    """
    if n < 8:
        return get_nth_middle_two_digits_for_less_than_8(n)
    elif n > 99:
        raise ValueError("입력 n은 3보다 크고 100보다 작아야 합니다.")
    
    html_file_path = os.path.join(os.path.dirname(__file__), 
                                 "Evolution of Conway's 92 Look and Say audioactive elements.html")
    
    try:
        with open(html_file_path, 'r', encoding='windows-1252') as file:
            html_file_content = file.read()

        ELEMENTS_DATABASE = parse_elements_from_html(html_file_content)
        
        if 'Hf' not in ELEMENTS_DATABASE or 'Sn' not in ELEMENTS_DATABASE:
            missing = []
            if 'Hf' not in ELEMENTS_DATABASE: missing.append('Hf')
            if 'Sn' not in ELEMENTS_DATABASE: missing.append('Sn')
            raise ValueError(f"초기 원소로 사용할 {missing}이(가) 파싱된 데이터베이스에 없습니다.")
        
        # L1="1"로 시작하는 수열의 L8 = "1113213211" 은 ['Hf', 'Sn'] 으로 분해됨.
        initial_elements_L8 = ['Hf', 'Sn']
        start_gen = 8  # L8 과 일치하는 원소 조합 있음. 이후 원소 진화 가능.
        TARGET_GENERATION = n

        start_time = time.time()
        middle_digits = get_middle_two_digits_of_Ln(
            initial_elements_L8,
            start_gen,
            TARGET_GENERATION,
            ELEMENTS_DATABASE
        )
        
        if middle_digits == "??":
            raise ValueError(f"L{TARGET_GENERATION}의 가운데 두 자리 숫자를 계산하지 못했습니다.")
        elif middle_digits is not None:
            return middle_digits
        else:
            raise ValueError(f"L{TARGET_GENERATION}의 가운데 두 자리 숫자를 계산하지 못했습니다.")
        
    except ValueError as e:
        print(f"처리 중 오류 발생 (ValueError): {e}")
        raise
    except KeyError as e:
        print(f"처리 중 키 오류 발생 (KeyError): '{e}' - 해당 원소가 elements_db에 없거나, decays_to 리스트에 잘못된 이름이 있을 수 있습니다.")
        raise
    except Exception as e:
        print(f"처리 중 예상치 못한 오류 발생: {e.__class__.__name__} - {e}")
        raise