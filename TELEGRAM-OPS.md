# Telegram 운영 정리 (OpenClaw)

## 현재 결론
- 이슈 원인: `409 Conflict (getUpdates)`
- 의미: 같은 봇 토큰을 다른 인스턴스(서버/스크립트/앱)에서도 동시에 사용
- 조치: 새 토큰으로 교체 + Gateway 재시작 + DM pairing 승인
- 상태: 실시간 응답 정상

## 표준 점검 순서
1. 상태 확인
```bash
openclaw status
openclaw channels status --probe
```

2. Telegram 로그 확인
```bash
openclaw channels logs --channel telegram --lines 120
```

3. 페어링 확인 (DM 정책이 pairing일 때)
```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE> --notify
```

## 토큰 교체 절차
1. BotFather에서 `/token`으로 새 토큰 발급
2. `~/.openclaw/openclaw.json` 수정
   - `channels.telegram.botToken` 값 교체
3. 재시작
```bash
openclaw gateway restart
```
4. 재검증
```bash
openclaw channels status --probe
```

## 재발 방지
- 동일 토큰을 두 곳 이상에서 동시에 실행하지 않기
- 이전 테스트 인스턴스(로컬/서버/컨테이너) 종료 확인
- 토큰 재발급 후 기존 토큰은 즉시 폐기

## 트러블슈팅 키워드
- `pairing required`: DM pairing 미승인 상태
- `409 Conflict: terminated by other getUpdates request`: 중복 실행 충돌
- `token:config, works`: 토큰 자체는 유효

## 원라이너 점검 세트
```bash
openclaw status && openclaw channels status --probe && openclaw channels logs --channel telegram --lines 80
```
