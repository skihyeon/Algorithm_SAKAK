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
(pytest)
bash run_pytest_str.sh

(change integer n)
python -c "from logics.functions_str import main; print(main(n))"
```

### Solve2 - Conway's Elements Evolution
```bash
(pytest)
bash run_pytest_element.sh

(change integer n)
python -c "from logics.functions_element import main; print(main(n))"
```

## 풀이과정.
- 처음엔 단순히 반복문을 이용해 현재 항으로부터 다음 항을 구하는 식으로 구현
  - 53번째 항까진 1초 이내로 구할 수 있지만, n이 늘어날 수록 시간이 기하급수적으로 늘어남.
  - 70번째 항의 경우, 84초의 시간이 걸림.
  - 문제에서 요구하는 n의 최댓값은 99인데, 이 경우 어느정도의 시간이 소요될지 알 수 없음.

- 개미수열의 규칙상, 첫항을 제외하곤 1~3까지의 숫자만 나올수 있고, 최대 3번까지만 반복될 수 있다는 규칙을 이용
  - 문자열이 아닌, integer를 이용해 계산 시간 단축을 시도.
  - integer를 이용한다고 해서 계산 시간이 크게 줄어들지는 않음.

- 콘웨이 상수(1.303..)를 통해 개미수열 n번째 항의 길이를 알 수 있다는 것을 알게 됨.
  - 가운데 두 자리 수를 구하는 것이 목표임으로, 길이를 알 수 있다면 개미수열을 절반까지만 구할 수 있음.
  - 하지만, 콘웨이 상수는 대수적으로 계산된 값이고, 정확한 수치값이 아님.
  - 정확히 가운데 두자리를 구하는 것이 목표이므로, 적합한 방식이 아님.
  - 해당 과정에서 L99는 1800억~1900억 자리에 달할 것임을 알게됨.

- 천억 자리가 넘는 수를 짧은 시간 내로 계산하기 위해서, 분명 토큰화할 방법이 존재할 거라고 생각함. (최근 읽었던 논문 [OTSL](https://arxiv.org/pdf/2305.03393)에서 영감)
  - 이때, conway의 원소에 관한 [블로그](https://blog.naver.com/9c120n/222065000768)를 접함.
  - 해당 내용에 따르면, 개미수열의 특정 시퀀스가 어떤 원소로 치환되고, 그 치환된 원소들 간에 어떠한 규칙이 있을 것임을 시사
  - 규칙만 찾는다면, 수열의 전체 길이를 극단적으로 줄일 수 있을 것임.
  - ex) '111312212221121123222112' -> 'N' // 24자 -> 1자
  - conway's element evolution 이라는 키워드로 검색했을때, 원소와 규칙을 담은 [테이블](http://www.se16.info/js/lands2.htm)을 발견.
  - ex) L8은 '1113213211'로 'Hf Sn'으로 표현됨. L9는 진화 규칙에 따라 Hf는 Lu로, Sn은 In으로 변환 가능. 따라서 'Lu In'은 '311312 11131221'이 되어 L9와 일치.
  - 해당 규칙을 따라 계산했을 때, L70을 구하는데 일전 84초에서 9초까지 감소함.
  - L70의 길이는 숫자일때 약 3억 자리, 토큰화시 약 2300만 자리, 약 10% 이하의 길이로 압축 가능.
  - L80의 길이는 숫자일때 약 14억 자리, 토큰화시 약 3300만 자리, 약 2% 정도의 길이로 압축 가능.
  - 콘웨이가 주장한, 원소들끼리의 결합까지 고려하면 더 짧은 토큰화가 가능할 것으로 생각되지만, (ex) Pa K == 131112 == Cu, 해당 결합 규칙을 찾지 못해서 구현하지 못했음.
  - 해당 결합 규칙까지 구현할 시 L99도 빠른 시간내에 구할 수 있을 것으로 생각됨.