# Breast Cancer Classification Pipeline

## Overview

Breast Cancer Wisconsin (Diagnostic) 데이터셋을 활용하여 Amazon SageMaker Pipelines 기반 머신러닝 파이프라인을 구현하고 평가합니다.

## Objectives

- 데이터 전처리 → 모델 학습 → 모델 평가
- SageMaker SDK 3.x 활용
- 하이퍼파라미터 변경에 따른 3회 이상 실행
- Accuracy, Recall, Precision, F1 비교
- 악성 종양(target=0) 탐지 성능 분석
- 실험 재현성 및 AWS 비용 관리

## Tech Stack

- AWS SageMaker AI
- Amazon S3
- Python
- scikit-learn
- SageMaker SDK 3.x

## Progress

- [ ] AWS 환경 및 기존 비용 확인
- [ ] SageMaker SDK 실행 환경 준비
- [ ] 데이터 전처리 구현
- [ ] 모델 학습 구현
- [ ] 모델 평가 구현
- [ ] SageMaker Pipeline 실행
- [ ] 3회 이상 실험 및 결과 비교
- [ ] 결과 분석 및 실습 정리
- [ ] AWS 리소스 정리

## Notes

실행 결과와 기술적 판단은 실제 검증 이후 기록합니다.

본 실습에서는 실시간 추론 엔드포인트를 배포하지 않습니다.
