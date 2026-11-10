# AI Engineering Lab

> AI 플랫폼 인프라 설계부터 MLOps·LLMOps 실습과 운영까지 **설계 → 구축 → 검증 → 운영 → 회고**를 기록하는 기술 포트폴리오.

현재 시작점은 **Oracle Cloud Infrastructure(OCI)** 실습입니다. 여기서 구축한 서버를 활용해 Docker, Kubernetes, Kubeflow, MLOps, RAG 프로젝트로 확장합니다.

## 학습 영역

| 영역 | 목표 | 경로 |
|---|---|---|
| Fundamentals | AI 엔지니어링·네트워크·시스템 설계 | [fundamentals/](fundamentals/) |
| Infrastructure | Linux, Docker, Kubernetes, Terraform, Ansible | [infrastructure/](infrastructure/) |
| Cloud | OCI, AWS, GCP, Azure | [cloud/](cloud/) |
| AI Platform | 플랫폼 아키텍처, Kubeflow, 서빙, 관측성 | [ai-platform/](ai-platform/) |
| MLOps | 학습 파이프라인, 실험 추적, 모델 등록, CI/CD | [mlops/](mlops/) |
| LLMOps | RAG, 벡터DB, 서빙, 평가, 추적 | [llmops/](llmops/) |
| Projects | End-to-End 구현·검증 | [projects/](projects/) |

## 첫 번째 실습: OCI 기반 AI 플랫폼 인프라

1. [목표 및 VM 사양 확정](cloud/oci/00-scope-and-spec.md)
2. [비용·무료 크레딧·알림](cloud/oci/01-cost-guardrails.md)
3. [계정/IAM](cloud/oci/02-account-iam.md)
4. [VCN/네트워크](cloud/oci/03-network.md)
5. [컴퓨트 인스턴스](cloud/oci/04-compute.md)
6. [서버 초기화](cloud/oci/05-server-bootstrap.md)
7. [Docker](cloud/oci/06-docker.md)
8. [Kubernetes](cloud/oci/07-kubernetes.md)
9. [운영 및 비용](cloud/oci/08-operations-and-cost.md)
10. [실습 종료 및 과금 확인](cloud/oci/09-teardown.md)

> **현재 상태:** 저장소 구조와 문서 초안만 준비된 상태입니다. 실습 완료 여부는 실제 검증 후 갱신합니다.

## 기록 원칙

- 실행 명령과 관찰 결과, 오류, 해결 과정, 기술 선택 이유를 구분해서 기록합니다.
- 실제 프로젝트 구성은 [`projects/`](projects/)에, 반복 가능한 스크립트는 [`scripts/`](scripts/)에 저장합니다.
- 공통 문서 양식은 [`docs/templates/`](docs/templates/)를 사용합니다.
- 토큰, API 키, 개인키, 비밀번호, 실제 계정 식별자, 민감한 환경값은 커밋하지 않습니다.
- 클라우드 요금·무료 티어 조건은 실습 시점의 공식 문서와 콘솔을 기준으로 확인합니다.
- 외부 강의자료를 그대로 재배포하지 않고 직접 작성한 실습 코드와 결과를 중심으로 관리합니다.
