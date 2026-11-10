# 07. Kubernetes / Kubeflow 확장 계획

- **상태:** 미진행

## 목적

Docker에서 Kubernetes로 확장하고 추후 Kubeflow Pipelines를 활용해 MLOps/RAG 실습을 수행합니다.

## 순서

- [ ] 선택한 OCI VM 사양으로 클러스터 구현 가능성·제약 확인
- [ ] 학습용 배포 방식 결정 (예: kind, k3s 등 비교)
- [ ] `kubectl` 컨텍스트 및 노드 상태 확인
- [ ] Namespace / Pod / Deployment / Service 실습
- [ ] StorageClass / PVC 확인
- [ ] Kubeflow/KFP 설치 호환성 및 자원 요구 재검토
- [ ] KFP 파이프라인 실행 결과 기록

> Kubeflow는 기본 시스템 서비스만으로도 자원을 소비합니다. VM 크기와 아키텍처 호환성을 확인하기 전에는 설치 성공을 전제로 하지 않습니다.
