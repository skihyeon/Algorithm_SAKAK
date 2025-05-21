# Algorithm_SAKAK
problem1

## Setup

### Language
- Python 3.10

### Environment Setup
Create a virtual environment using conda and install dependencies:

```bash
conda create -n problem1 python=3.10
conda activate problem1
pip install -r requirements.txt
```

## Run

This project provides two approaches to solve the problem.

### Solve1 - Simple Iteration
```bash
bash run_pytest_str.sh
```

### Solve2 - Conway's Elements Evolution
```bash
bash run_pytest_element.sh
```

## 방식
- 처음엔 단순히 반복문을 이용해 현재 항으로부터 다음 항을 구하는 식으로 구현
  -> 53번째 항까진 1초 이내로 구할 수 있지만, n이 늘어날 수록 시간이 기하급수적으로 늘어남.
  -> 70번째 항의 경우, 84초의 시간이 걸림.
  -> 문제에서 요구하는 n의 최댓값은 99인데, 이 경우 어느정도의 시간이 소요될지 알 수 없음.

- 이때, conway의 원소에 관한 [블로그](https://blog.naver.com/9c120n/222065000768)를 접함.
  -> 해당 내용에 따르면, 개미수열의 특정 시퀀스가 어떤 원소로 치환되고, 그 치환된 원소들 간에 어떠한 규칙이 있을 것임을 시사
  -> 규칙만 찾는다면, 수열의 전체 길이를 극단적으로 줄일 수 있을 것임.
  -> ex) '111312212221121123222112' -> 'N' // 24자 -> 1자
  -> conway's element evolution 이라는 키워드로 검색했을때, 원소와 규칙을 담은 [테이블](http://www.se16.info/js/lands2.htm)을 발견.
  -> ex) L8은 '1113213211'로 'Hf Sn'으로 표현됨. L9는 진화 규칙에 따라 Hf는 Lu로, Sn은 In으로 변환 가능. 따라서 'Lu In'은 '311312 11131221'이 되어 L9와 일치.
  -> 해당 규칙을 따라 계산했을 때, L70을 구하는데 일전 84초에서 9초까지 감소함.