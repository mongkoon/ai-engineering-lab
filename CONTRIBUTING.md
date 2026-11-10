# 기록 및 변경 규칙

이 저장소는 학습 기록용으로, 실습을 한 단계씩 검증하며 변경합니다.

1. 기존 문서의 **목표 → 사전 조건 → 실행 → 검증 → 비용·보안 → 정리** 흐름을 유지합니다.
2. 새로운 작업은 `docs/templates/lab-note.md`를 복사해 작성합니다.
3. 오류 해결은 `docs/templates/troubleshooting.md`를 사용합니다.
4. 사양 선택 등 중요한 판단은 `docs/templates/adr.md` 양식으로 남깁니다.
5. 실제로 실행하지 않은 명령에 대해서는 `예정` 또는 `예시`라고 명확히 표기합니다.
6. 커밋 전 비밀정보와 클라우드 리소스 식별자 노출 여부를 확인합니다.

커밋 예시: `docs(oci): document network design`, `lab(docker): verify hello-world`.
