# 06. Docker 설치 및 검증

- **상태:** 미진행

## 목표

Ubuntu에서 Docker Engine을 구성하고 단순 컨테이너가 정상 동작하는지 확인합니다.

## 점검

- [ ] OS 및 CPU 아키텍처에 맞는 공식 설치 절차 확인
- [ ] Docker Engine 및 Compose 버전 확인
- [ ] Docker 데몬 실행 상태 확인
- [ ] `hello-world` 실행
- [ ] Nginx 등 테스트 서비스의 필요한 포트만 제한적으로 개방
- [ ] 불필요한 이미지·컨테이너·볼륨 정리

## 확인 명령 (설치 완료 후)

```bash
docker version
docker info
docker run --rm hello-world
```

## 주의

`docker` 그룹 권한은 사실상 호스트의 높은 권한으로 이어질 수 있어 사용자 추가 여부를 신중히 결정합니다.
