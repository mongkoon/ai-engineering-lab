# OCI Lab

**목적:** OCI에 AI 플랫폼 실습용 Linux 인프라를 구성하고, Docker → Kubernetes → Kubeflow/KFP 실습으로 점진적으로 확장합니다.

## 권장 진행 순서

| 단계 | 문서 | 검증 목표 |
|---|---|---|
| 0 | [목표·사양](00-scope-and-spec.md) | OCPU·RAM·디스크·리전 확정 |
| 1 | [비용 안전장치](01-cost-guardrails.md) | 무료 크레딧·알림·과금 위험 점검 |
| 2 | [계정/IAM](02-account-iam.md) | 최소 권한 및 MFA 점검 |
| 3 | [네트워크](03-network.md) | VCN/Subnet/접근 규칙 점검 |
| 4 | [Compute](04-compute.md) | VM 생성·스토리지 확인 |
| 5 | [서버 초기화](05-server-bootstrap.md) | SSH/패키지/보안 확인 |
| 6 | [Docker](06-docker.md) | 컨테이너 실행 성공 |
| 7 | [Kubernetes](07-kubernetes.md) | 학습용 클러스터 실행 |
| 8 | [운영·비용](08-operations-and-cost.md) | 자원 사용량 및 청구 확인 |
| 9 | [정리](09-teardown.md) | 잔여 과금 리소스 점검 |

## 시작 전 원칙

- **정확한 인스턴스 사양은 아직 미확정입니다.** 이전 논의의 수치를 확인한 뒤 표에 기록합니다.
- 리전·요금·Always Free / Trial 적용 여부는 생성 직전 OCI 콘솔과 공식 문서로 확인합니다.
- 예산 알림을 **하드 스펜딩 캡**으로 간주하지 않습니다.
- 생성·수정·종료 시마다 실제 결과를 문서에 반영합니다.
- 원본 콘솔 캡처는 공개하기 전에 가립니다.
