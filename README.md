# AI Engineering Lab

> AI 엔지니어링 학습과 실습을 **설계 → 구축 → 검증 → 운영 → 회고** 순서로 기록하는 개인 기술 저장소입니다.

클라우드 인프라부터 Linux, Docker, Kubernetes, MLOps, LLMOps, RAG까지 다룹니다. 현재는 **Oracle Cloud Infrastructure(OCI) 실습**부터 시작합니다.

## 학습 영역

| 영역 | 주요 주제 | 경로 |
|---|---|---|
| 기초 | AI 플랫폼 아키텍처·컴퓨팅 개념 | [`fundamentals/`](fundamentals/) |
| Linux | 서버 관리, 네트워크, 권한 | [`linux/`](linux/) |
| Containers | 이미지, Dockerfile, Compose | [`docker/`](docker/) |
| Kubernetes | Pod, Deployment, Service, Storage | [`kubernetes/`](kubernetes/) |
| Cloud | OCI · AWS · GCP · Azure | [`cloud/`](cloud/) |
| IaC | Terraform, Ansible | [`infrastructure-as-code/`](infrastructure-as-code/) |
| MLOps | Kubeflow, KFP, 실험·아티팩트 관리 | [`mlops/`](mlops/) |
| LLMOps | 관측성, 품질 평가, 비용, 가드레일 | [`llmops/`](llmops/) |
| RAG | 청킹, 임베딩, 벡터 검색, 평가 | [`rag/`](rag/) |
| 통합 | 엔드투엔드 프로젝트 | [`projects/`](projects/) |

## 현재 진행: OCI 기반 AI 플랫폼 실습 환경

1. [`cloud/oci/00-scope-and-spec.md`](cloud/oci/00-scope-and-spec.md) — 목표 및 VM 사양 확정
2. [`cloud/oci/01-cost-guardrails.md`](cloud/oci/01-cost-guardrails.md) — 비용·무료 크레딧·알림 확인
3. [`cloud/oci/02-account-iam.md`](cloud/oci/02-account-iam.md) — IAM과 접근 보호
4. [`cloud/oci/03-network.md`](cloud/oci/03-network.md) — 네트워크 구성
5. [`cloud/oci/04-compute.md`](cloud/oci/04-compute.md) — 인스턴스 및 스토리지
6. [`cloud/oci/05-server-bootstrap.md`](cloud/oci/05-server-bootstrap.md) — 초기 서버 점검
7. [`cloud/oci/06-docker.md`](cloud/oci/06-docker.md) — 컨테이너 환경
8. [`cloud/oci/07-kubernetes.md`](cloud/oci/07-kubernetes.md) — Kubernetes 실습
9. [`cloud/oci/08-operations-and-cost.md`](cloud/oci/08-operations-and-cost.md) — 사용량과 비용 관찰
10. [`cloud/oci/09-teardown.md`](cloud/oci/09-teardown.md) — 사용 종료 및 잔여 과금 점검

> **상태 안내:** 이 저장소는 초기 템플릿입니다. 체크박스는 실습 완료 후 직접 갱신하고, 성공하지 않은 명령이나 테스트를 완료로 표시하지 않습니다.

## 기록 원칙

- 왜 이 구성을 선택했는지 **의사결정 근거**와 대안을 함께 적습니다.
- 실제로 실행한 **명령 / 결과 / 오류 / 해결 방법**을 구분해 기록합니다.
- OCI 요금과 서비스 제공 여부는 **실습 당일 콘솔·공식 문서에서 재확인**합니다.
- 계정 식별자, API 키, SSH 개인키, 토큰, 외부 공개 IP 및 개인정보 등은 공개 저장소에 올리기 전에 비식별화합니다.
- 문서 양식은 [`docs/templates/`](docs/templates/)를 참고합니다.

## 빠른 시작

```bash
git clone <YOUR_REPOSITORY_URL>
cd ai-engineering-lab
# cloud/oci/00-scope-and-spec.md에서 목표와 사양부터 기록
```

## 참고

이 저장소는 자체 작성한 실습 기록을 중심으로 합니다. 수업 강의자료·타인의 저작물은 이용 권한을 확인한 경우에만 포함합니다.
