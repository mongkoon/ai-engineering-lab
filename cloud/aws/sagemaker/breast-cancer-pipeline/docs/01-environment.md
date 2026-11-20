# 01. AWS SageMaker Environment Setup

## 1. Overview

Amazon SageMaker AI를 활용하여 Breast Cancer Wisconsin (Diagnostic) 데이터셋 기반 머신러닝 파이프라인을 구축한다.

데이터 전처리, 모델 학습, 성능 평가를 독립적인 파이프라인 단계로 구성하고, 실험 재현성과 클라우드 리소스 관리 방식을 검증한다.

**주요 기술 영역**

- AWS 기반 머신러닝 개발 환경 구축
- SageMaker Pipelines를 활용한 ML 워크플로 자동화
- S3 기반 데이터 및 모델 아티팩트 관리
- 모델 평가와 하이퍼파라미터 실험 비교
- 클라우드 비용 및 리소스 수명주기 관리

## 2. Architecture

개발 환경과 머신러닝 실행 환경을 분리하여 구성한다.

```text
Amazon SageMaker Studio
    |
    +-- JupyterLab
    |     +-- Python / SageMaker SDK
    |
    +-- SageMaker Pipelines
          +-- Preprocessing
          +-- Training
          +-- Evaluation
                 |
                 v
              Amazon S3
          (ML Artifacts)
```

## 3. Environment Configuration

**환경 구성일:** 2026-11-21

| Component | Configuration | Status |
|---|---|---|
| Cloud Provider | AWS | Configured |
| Region | ap-northeast-2 (Seoul) | Configured |
| ML Platform | Amazon SageMaker AI | Configured |
| Domain | Dedicated SageMaker Domain | Created |
| IDE | SageMaker Studio JupyterLab | Space created |
| Space | BreastCancer / Private | Stopped |
| Instance Type | ml.t3.medium | Configured |
| Storage | 5GB EBS | Configured |
| Container Image | SageMaker Distribution 5.0.0 | Selected |
| Object Storage | Dedicated Amazon S3 bucket | Created |
| Execution Role | IAM role configured through Quick setup | Permission validation pending |

실제 AWS 계정 정보와 리소스 식별자는 공개 문서에 포함하지 않는다.

## 4. Infrastructure Design Decisions

### 4.1 Environment Isolation

기존 머신러닝 실험 환경과 독립적인 SageMaker Domain 및 JupyterLab Space를 생성했다.

이를 통해 다음 목표를 달성한다.

- 프로젝트별 실행 환경 분리
- 데이터 및 모델 아티팩트의 저장 경로 구분
- 리소스 사용량과 비용의 추적 가능성 향상
- 특정 환경의 리소스를 독립적으로 정리할 수 있는 구조 확보

### 4.2 Compute Configuration

JupyterLab 개발 환경에는 `ml.t3.medium` 인스턴스를 선택했다.

소규모 데이터셋을 이용한 파이프라인 개발과 SDK 실행을 목적으로 하며, 실제 전처리 및 학습 작업은 SageMaker 관리형 작업 인스턴스에서 수행하도록 설계한다.

### 4.3 Storage Strategy

S3 저장소는 기존 실험 데이터와 분리된 전용 버킷을 사용한다.

파이프라인 개발 과정에서 다음 아티팩트를 관리할 예정이다.

- 입력 및 전처리 데이터
- 학습 코드와 모델 아티팩트
- 평가 결과 JSON
- 실험별 성능 지표

실제 저장 경로와 결과는 파이프라인 구현 및 검증 후 기록한다.

### 4.4 Security

- JupyterLab Space를 Private으로 구성
- S3 Public Access Block 활성화
- S3 ACL 비활성화
- SSE-S3 기본 암호화 사용
- IAM 실행 권한은 실제 작업 실행 전 검증
- 인증 정보와 계정 식별자는 저장소에 커밋하지 않음

## 5. Cost Management

SageMaker 개발 환경과 머신러닝 실행 작업의 비용을 구분하여 관리한다.

- JupyterLab 컴퓨팅은 필요한 시간에만 실행한다.
- JupyterLab 중지 이후에도 EBS 스토리지 비용이 발생할 수 있음을 고려한다.
- Processing 및 Training 작업의 인스턴스 유형과 실행 시간을 기록한다.
- S3 저장 객체와 CloudWatch 로그의 잔여 비용을 점검한다.
- 개발 환경 종료 시 연결된 스토리지와 기타 잔여 리소스를 별도로 확인한다.

## 6. Current Validation Status

- [x] AWS 리전 확인
- [x] 독립 SageMaker Domain 생성
- [x] JupyterLab Space 생성
- [x] JupyterLab 인스턴스 및 스토리지 설정 확인
- [x] 전용 S3 버킷 생성
- [ ] JupyterLab 실행 및 환경 검증
- [ ] SageMaker SDK 버전 확인
- [ ] IAM 실행 권한과 S3 접근 검증
- [ ] ML Pipeline 구현
- [ ] 실험 실행 및 결과 비교
- [ ] 리소스 정리 및 비용 검증

## 7. Next Steps

1. JupyterLab 실행 및 Python 개발 환경 확인
2. SageMaker SDK와 필수 라이브러리 검증
3. 데이터 전처리·학습·평가 코드 구현
4. SageMaker Pipeline 구성 및 실험 실행
5. 성능 평가, 결과 분석 및 재현성 검증
6. 클라우드 리소스 정리 및 운영 회고

---

> 이 문서는 실제 구축 및 검증한 내용을 기준으로 갱신한다. 예정된 작업과 검증 완료된 작업을 명확하게 구분한다.
