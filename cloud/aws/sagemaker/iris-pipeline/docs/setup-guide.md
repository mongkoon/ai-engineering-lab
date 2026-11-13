
# 11주차 실습: AWS SageMaker Iris Pipeline

## 1. 실습 목표

- SageMaker Pipelines 구축
- Iris 데이터 전처리·학습·평가
- 조건부 모델 레지스트리 등록
- 모델 수동 승인
- Serverless Endpoint 배포 및 삭제

## 2. 실습 환경

| 항목 | 설정 |
|---|---|
| AWS Region | ap-northeast-2 |
| SageMaker Studio | JupyterLab |
| Studio Instance | ml.t3.medium |
| Processing | ml.m5.large |
| Training | ml.m5.large |
| SageMaker SDK | 3.26.0 |

## 3. 사전 준비

### Step 1. AWS 계정 설정
- [ ] AWS 계정 로그인
- [ ] MFA 설정
- [ ] 서울 리전 선택

### Step 2. 비용 관리
- [ ] AWS Budgets 설정
- [ ] 비용 경보 설정

### Step 3. SageMaker 환경
- [ ] Service Quotas 확인
- [ ] Studio Domain 생성
- [ ] IAM 실행 역할 확인
- [ ] S3 버킷 생성

### Step 4. SDK 설치

```bash
python -m pip install "sagemaker[mlops,train,serve]==3.26.0"
```

## 4. 실습 진행

1. 데이터 전처리
2. 모델 학습
3. 모델 평가
4. 정확도 기준 확인
5. 모델 등록
6. 모델 수동 승인
7. 서버리스 배포 및 추론

## 5. 실습 종료

- [ ] Endpoint 삭제
- [ ] Endpoint Configuration 삭제
- [ ] 불필요한 모델 및 아티팩트 정리
- [ ] Studio JupyterLab 중지
- [ ] AWS 비용 확인
