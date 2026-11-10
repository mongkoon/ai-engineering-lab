# 03. 네트워크 설계 및 구성

- **상태:** 미진행

## 설계 초안

```text
Internet (필요 시)
    |
[보안 규칙 / NSG]
    |
VCN → Subnet → Compute (Ubuntu)
```

## 점검 항목

- [ ] VCN CIDR 및 Subnet 역할 검토
- [ ] Public / Private Subnet 선택 근거 문서화
- [ ] 라우팅 및 Gateway 종류 확인
- [ ] 보안 목록 / NSG에서 필요한 포트만 허용
- [ ] SSH 직접 노출이 필요한지 평가 (Bastion 등 대안 검토)
- [ ] SSH 허용 시 출발지 범위를 최소화 (가능하면 본인 IP /32)
- [ ] 미사용 Ingress 규칙 차단 및 접속 테스트
- [ ] 생성한 Network 리소스 중 비용 항목 식별

## 최종 기록 (민감정보 제거)

- 네트워크 형태:
- 공개 포트:
- 접속 방법:
- 검증 결과:
