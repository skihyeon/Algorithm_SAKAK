import re

def parse_elements_from_html(html_content):
    """
    제공된 HTML 내용에서 콘웨이 원소 정보를 파싱하여 elements_db를 생성합니다.
    """
    elements_db = {}
    
    try:
        # HTML 테이블의 각 row를 분리 (<table>...</table> 내부의 <tr>...</tr>)
        # tbody가 명시적으로 없을 수도 있으므로 table 전체에서 tr을 찾습니다.
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
            
            if len(cols) < 4: # 필요한 열(Element Symbol, Evolution, String)이 충분한지 확인
                # print(f"경고: 열 개수 부족으로 행 건너뜀: {row_data}")
                continue

            # 2번째 열: 원소 기호 (Symbol)
            # HTML 예시: <td><b>H</b></td> 또는 <td><b><a name="Al">Al</a></b></td>
            # <b> 태그 내부의 내용을 우선적으로 가져오고, 그 안의 다른 태그는 제거
            b_content_match = re.search(r"<b>(.*?)</b>", cols[1], re.DOTALL | re.IGNORECASE)
            if not b_content_match:
                # print(f"경고: 원소 기호 <b> 태그 파싱 실패: {cols[1][:100]}")
                continue 
            
            element_symbol = re.sub(r"<[^>]+>", "", b_content_match.group(1)).strip()
            # 기호가 알파벳 대문자로 시작하고 (선택적으로 소문자 한 글자) 구성되었는지 확인
            if not re.fullmatch(r"[A-Z][a-z]?", element_symbol): 
                # print(f"경고: 유효하지 않은 원소 기호 형식: '{element_symbol}' from {cols[1][:100]}")
                continue

            # 3번째 열: 변환 규칙 (Evolution)
            # 예: <a href="..."><b>Hf</b></a> <a href="...">Pa</a> ... 또는 <b>H</b> (stable)
            evolution_html = cols[2]
            decays_to_symbols = []
            
            if "(stable)" in evolution_html: # 안정적인 경우
                # <b>H</b> (stable) 에서 H를 추출
                stable_match = re.search(r"<b>([a-zA-Z][a-z]?)</b>\s*\(stable\)", evolution_html, re.IGNORECASE)
                if stable_match:
                    decays_to_symbols = [stable_match.group(1).strip()]
                else: # 안정 표시는 있지만 기호를 못 찾으면 현재 원소 기호 사용 (파싱 오류 대비)
                    decays_to_symbols = [element_symbol] 
            else: # 다른 원소들로 변환되는 경우
                  # <a> 태그 안의 텍스트(원소 기호)를 추출
                decay_links = re.findall(r"<a[^>]*>(.*?)</a>", evolution_html, re.DOTALL | re.IGNORECASE)
                for link_content in decay_links:
                    # <b>He</b> 또는 그냥 He 일 수 있음. 모든 태그 제거 후 순수 텍스트 확인
                    symbol_in_link = re.sub(r"<[^>]+>", "", link_content).strip()
                    if re.fullmatch(r"[A-Z][a-z]?", symbol_in_link): # 유효한 기호 형식인지 확인
                         decays_to_symbols.append(symbol_in_link)
            
            # 변환 정보가 파싱되지 않았고, stable도 아니면 자기 자신으로 (오류일 수 있으나 방어적 처리)
            if not decays_to_symbols and "(stable)" not in evolution_html:
                # print(f"경고: '{element_symbol}'의 변환 정보 없음. 안정으로 간주 (또는 파싱 확인 필요).")
                decays_to_symbols = [element_symbol]

            # 4번째 열: 원소 문자열 (String)
            # 예: <b><font size="1">22</font></b>
            element_string_html = cols[3]
            # <font> 태그 내부 또는 <td> 직접 내용에서 숫자 문자열 추출 시도
            element_string_match = re.search(r"<font[^>]*>(.*?)</font>", element_string_html, re.DOTALL | re.IGNORECASE)
            if element_string_match:
                element_string = re.sub(r"<[^>]+>", "", element_string_match.group(1)).strip() # 태그 제거 및 공백 제거
            else: # font 태그가 없는 경우, <td> 내부의 숫자를 직접 찾음
                element_string = re.sub(r"<[^>]+>", "", element_string_html).strip()

            if not element_string.isdigit(): # 문자열이 숫자로만 구성되어 있는지 확인
                # print(f"경고: '{element_symbol}'의 원소 문자열이 숫자가 아님: '{element_string}'")
                continue # 유효하지 않으면 이 원소는 건너뜀
                
            elements_db[element_symbol] = {
                'string': element_string,
                'length': len(element_string),
                'decays_to': decays_to_symbols
            }
            # print(f"파싱된 원소: {element_symbol} -> {elements_db[element_symbol]}")

    except Exception as e:
        print(f"HTML 파싱 중 오류 발생: {e.__class__.__name__} - {e}")
        raise

    if not elements_db:
        raise ValueError("HTML에서 원소 데이터를 추출하지 못했습니다. HTML 구조를 확인하거나 파싱 로직을 점검해주세요.")
        
    return elements_db

def evolve_sequence(current_element_sequence, db):
    """한 세대 진화시키는 함수"""
    next_sequence = []
    for element_name in current_element_sequence:
        if element_name not in db:
            print(f"경고: '{element_name}' 원소가 DB에 정의되지 않았습니다. 해당 원소의 정의를 확인해주세요. 이 원소는 진화에서 제외됩니다.")
            continue # 정의되지 않은 원소는 건너뜀

        element_data = db[element_name]
        if not element_data.get('decays_to'): # decays_to가 비어있거나 없는 경우 (안정적)
             # print(f"정보: '{element_name}' 원소의 decays_to가 비어있거나 없어 안정된 것으로 간주하고 자신을 추가합니다.")
             next_sequence.append(element_name)
        else:
            next_sequence.extend(element_data['decays_to'])
    return next_sequence

def get_middle_two_digits_of_Ln(initial_sequence_elements, start_generation_num, target_generation_num, db):
    """
    주어진 초기 원소 시퀀스에서 시작하여 목표 세대의 가운데 두 자리 숫자를 찾습니다.
    """
    current_sequence = list(initial_sequence_elements) # 원본 수정을 피하기 위해 복사

    print(f"L{start_generation_num}의 초기 원소 시퀀스 (개수: {len(current_sequence)}): {current_sequence[:10] if len(current_sequence) > 10 else current_sequence}")
    
    for gen in range(start_generation_num, target_generation_num):
        current_sequence = evolve_sequence(current_sequence, db)
        if not current_sequence:
            print(f"L{gen+1}세대에서 시퀀스가 비었습니다. DB 또는 로직 오류 가능성이 있습니다.")
            return None
        
        # 세대별 로그 (필요시 주석 해제, 매우 길 수 있음)
        # if (gen + 1) % 10 == 0 or gen + 1 == target_generation_num :
        #      print(f"L{gen+1}세대 진화 완료. 현재 원소 시퀀스 항목 수: {len(current_sequence)}")


    # 목표 세대(Ln)의 총 길이 계산
    total_length_Ln = 0
    # 진화 후 최종 시퀀스에서 DB에 없는 원소가 포함될 가능성을 배제하기 위해 한 번 더 필터링
    valid_final_sequence = []
    for element_name in current_sequence:
        if element_name in db:
            total_length_Ln += db[element_name]['length']
            valid_final_sequence.append(element_name)
        else:
            print(f"경고: 최종 시퀀스의 '{element_name}' 원소가 DB에 없어 길이 계산 및 최종 문자열 구성에서 제외됩니다.")
    
    current_sequence = valid_final_sequence # 유효한 원소들로만 구성된 시퀀스로 업데이트

    if total_length_Ln == 0:
        print(f"L{target_generation_num}의 유효한 총 길이가 0입니다. 모든 원소가 DB에 없거나 로직 오류일 수 있습니다.")
        return None

    print(f"L{target_generation_num}의 총 길이 (원소 기반): {total_length_Ln}")

    # 가운데 두 자리의 인덱스 계산 (0-based)
    # 길이가 L일 때, 가운데 두 자리는 (L-1)//2 와 L//2
    mid1_idx = (total_length_Ln - 1) // 2
    mid2_idx = total_length_Ln // 2 

    print(f"가운데 인덱스 (0-based): {mid1_idx}, {mid2_idx}")

    # 가운데 두 자리 숫자 찾기
    char1, char2 = None, None
    current_pos = 0
    for element_name in current_sequence: # 유효한 원소 시퀀스 사용
        # 이 시점에서 element_name은 반드시 db에 있어야 함 (위에서 필터링)
        element_info = db[element_name]
        el_len = element_info['length']
        el_str = element_info['string']

        # mid1_idx가 현재 원소 내에 있는지 확인
        if char1 is None and mid1_idx >= current_pos and mid1_idx < current_pos + el_len:
            char1 = el_str[mid1_idx - current_pos]

        # mid2_idx가 현재 원소 내에 있는지 확인
        if char2 is None and mid2_idx >= current_pos and mid2_idx < current_pos + el_len:
            char2 = el_str[mid2_idx - current_pos]

        if char1 is not None and char2 is not None: # 두 자리 모두 찾았으면 종료
            # 만약 mid1_idx와 mid2_idx가 같은 위치를 가리키고 (길이가 홀수),
            # char2가 그 다음 문자를 가져와야 한다면 추가 로직이 필요할 수 있지만,
            # 현재는 각 인덱스에 해당하는 문자를 독립적으로 찾음.
            # mid1_idx와 mid2_idx가 같으면 char1과 char2도 같게됨.
            # "가운데 두자리"가 인접한 두자리를 의미하면, mid2_idx는 mid1_idx+1 이어야 함 (짝수 길이일때)
            # (L-1)//2 와 (L-1)//2 + 1 (단, L > 0)
            # 현재 정의된 mid1, mid2는 L이 홀수이면 같은 인덱스, L이 짝수이면 인접한 인덱스.
            # 예를 들어 길이가 5이면 mid1=2, mid2=2. 가운데 "두"자리가 아니라 가운데 "한"자리의 인덱스들.
            # "가운데 두 자리"는 보통 (L/2 - 1)과 (L/2) (1-based) 또는 (L//2 - 1)과 (L//2) (0-based) (길이가 짝수일때)
            # 길이가 홀수 L일때는 (L-1)/2 번째와 그 다음것.
            # L=5, (0,1,2,3,4) -> mid1=2, mid2=2. 가운데는 2번째. "가운데 두자리"는 1,2 또는 2,3.
            # 여기서는 (L-1)//2 와 L//2 로 했으니,
            # L=5 (0,1,2,3,4): mid1=2, mid2=2. (2번째, 2번째)
            # L=4 (0,1,2,3): mid1=1, mid2=2. (1번째, 2번째)
            # 이 정의가 "가운데 두자리"에 맞는지 확인 필요. 
            # 만약 항상 인접한 두자리를 원한다면, mid2_idx는 mid1_idx + 1 (단, mid1_idx+1 < total_length_Ln) 로 설정.
            # 여기서는 현재 mid1_idx, mid2_idx 정의를 따름.
            break 

        current_pos += el_len
    
    # 결과 문자 구성
    if total_length_Ln == 0:
        return "??" # 또는 None
    if total_length_Ln == 1:
        # 길이가 1이면 가운데 "두"자리는 없음. 첫번째(유일한) 문자 반환 시도.
        if char1 is not None:
            return char1 + "?" # 또는 char1 만 반환하거나, 적절한 처리
        else: # 이 경우는 로직 오류일 가능성이 높음
            print("오류: 길이가 1이지만 문자를 찾지 못했습니다.")
            return "??"

    # char1이나 char2를 못찾은 경우(극단적인 경우, 예: DB에 없는 원소만 남음) 대비
    res_char1 = char1 if char1 is not None else "?"
    res_char2 = char2 if char2 is not None else "?"
        
    return res_char1 + res_char2

# --- 실행 ---
def main(n: int) -> str:
    # 여기에 개발자님이 파일에서 읽거나 직접 복사한 HTML 전체 내용을 할당합니다.
    # HTML 파일 로드
    import os
    
    html_file_path = os.path.join(os.path.dirname(__file__), 
                                 "Evolution of Conway's 92 Look and Say audioactive elements.html")
    
    with open(html_file_path, 'r', encoding='windows-1252') as file:
        html_file_content = file.read()
    # print(html_file_content)
    if "PASTE_HTML_CONTENT_HERE" in html_file_content:
        print("오류: html_file_content 변수에 실제 HTML 전체 내용을 붙여넣어 주세요.")
        exit()

    try:
        print("HTML 내용으로부터 원소 데이터베이스 파싱 시작...")
        ELEMENTS_DATABASE = parse_elements_from_html(html_file_content)
        print(f"원소 데이터베이스 파싱 완료. 총 {len(ELEMENTS_DATABASE)}개 원소 발견.")
        
        # 파싱된 DB의 일부를 출력하여 검증 (필요시 주석 해제)
        # print("\n파싱된 원소 데이터베이스 (상위 5개, 하위 5개):")
        # items = list(ELEMENTS_DATABASE.items())
        # if len(items) > 10:
        #     for i in range(5): print(f"'{items[i][0]}': {items[i][1]}")
        #     print("...")
        #     for i in range(len(items)-5, len(items)): print(f"'{items[i][0]}': {items[i][1]}")
        # else:
        #     for k, v in items: print(f"'{k}': {v}")
        
        # Hf와 Sn이 DB에 올바르게 파싱되었는지 확인 (초기 시퀀스 구성 요소)
        if 'Hf' not in ELEMENTS_DATABASE or 'Sn' not in ELEMENTS_DATABASE:
            missing = []
            if 'Hf' not in ELEMENTS_DATABASE: missing.append('Hf')
            if 'Sn' not in ELEMENTS_DATABASE: missing.append('Sn')
            raise ValueError(f"초기 원소로 사용할 {missing}이(가) 파싱된 데이터베이스에 없습니다. HTML 파싱 로직 또는 HTML 내용을 확인해주세요.")
        
        print(f"\nHf 원소 정보 (검증용): {ELEMENTS_DATABASE.get('Hf')}")
        print(f"Sn 원소 정보 (검증용): {ELEMENTS_DATABASE.get('Sn')}")

        # L1="1"로 시작하는 수열의 L8 = "1113213211" 은 ['Hf', 'Sn'] 으로 분해됨
        initial_elements_L8 = ['Hf', 'Sn']
        start_gen = 8 # L8부터 시작
        TARGET_GENERATION = n

        import time
        start_time = time.time()
        print(f"\nL{TARGET_GENERATION}의 가운데 두 자리 숫자 계산 시작 (L{start_gen}={initial_elements_L8} 에서 출발)...")
        middle_digits = get_middle_two_digits_of_Ln(
            initial_elements_L8,
            start_gen,
            TARGET_GENERATION,
            ELEMENTS_DATABASE
        )
        print(f"L{TARGET_GENERATION}의 가운데 두 자리 숫자 계산 완료. 실행 시간: {time.time() - start_time}초")
        if middle_digits is not None:
            print(f"\n최종 결과: L{TARGET_GENERATION}의 가운데 두 자리 숫자는 \"{middle_digits}\" 입니다.")
        else:
            print(f"\n최종 결과: L{TARGET_GENERATION}의 가운데 두 자리 숫자를 계산하지 못했습니다.")
        return middle_digits
    except ValueError as e:
        print(f"처리 중 오류 발생 (ValueError): {e}")
    except KeyError as e: # 이 오류는 보통 db[element_name] 접근 시 발생
        print(f"처리 중 키 오류 발생 (KeyError): '{e}' - 해당 원소가 elements_db에 없거나, decays_to 리스트에 잘못된 이름이 있을 수 있습니다. 파싱 결과를 확인해주세요.")
    except Exception as e:
        print(f"처리 중 예상치 못한 오류 발생: {e.__class__.__name__} - {e}")