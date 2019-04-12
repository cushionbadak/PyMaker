# PyMaker

## Goal
 - 자연어로 된 문장에 대응하는 python 언어 내 개념 찾기
 - 이를 위해서 자연어로 된 질문을 분석하여 알맞는 python official documentation link 제공

### Example
Q. how to run code 5 times
A. https://docs.python.org/3/reference/compound_stmts.html#the-for-statement

## Plan
 - Stackoverflow에서 official python documentation link를 가진 글 수집 및 전처리
 - 학습의 정답 집합이 될 Python 문서 url 정리
 - 목표를 이루기위한 신경망 모델 찾기
 - Python official documentation 만을 사용해서 학습시킨 대조군 실행결과와 비교
 - 학습 결과를 쉽게 사용할 수 있는 웹 서비스 제작
