# OpenClaw 최적화/안정화 점검 리포트

작성일: 2026-02-19 (MST)

## 1) 현재 상태 요약
- OpenClaw 버전 채널: `stable` (최신 `2026.2.19-2`)
- Gateway: 로컬 loopback 바인딩 (`127.0.0.1`)으로 동작
- Telegram: 연결 정상 (`status --deep`에서 OK)
- FileVault: On (좋음)
- macOS Application Firewall: Off (개선 여지)
- Time Machine 백업: 현재 실행중 작업 없음 (`Running=0`)

## 2) 보안 점검 결과 (read-only)
`openclaw security audit --deep` 결과:
- Critical: 0
- Warn: 3
- Info: 1

주요 경고:
1. `gateway.trusted_proxies_missing`
   - 현재는 loopback 로컬 운영이라 큰 문제는 아님
   - 나중에 reverse proxy로 외부 공개 시 `gateway.trustedProxies` 설정 필수
2. `gateway.nodes.deny_commands_ineffective`
   - `gateway.nodes.denyCommands`에 OpenClaw가 인식하지 않는 명령명이 포함됨
   - 실제 차단 효과가 없는 항목이 있어 정리 필요
3. `gateway.probe_failed (deep)`
   - 일부 deep probe에서 `pairing required`로 표시됨
   - 운영 자체는 정상이며, 로컬/권한/연결 컨텍스트 차이로 나타날 수 있음

## 3) 갭 분석 (권장 목표: Home/Workstation Balanced)
목표: 개인 워크스테이션에서 안전+편의 균형

현재 대비 갭:
- [중간] macOS 방화벽 비활성화
- [중간] 비효율 denyCommands 정리 필요
- [낮음] 프록시 신뢰 설정은 지금 당장 불필요(외부 공개 시만 필요)

## 4) 추천 스킬
1. `healthcheck` (최우선)
   - 주기 보안 점검/업데이트 상태 확인 자동화
2. `weather`
   - 일상 자동화용, 가볍고 실용적
3. `skill-creator`
   - 나중에 커스텀 워크플로우 만들 때

## 5) 실행 플랜 (변경은 승인 후)
### A. OpenClaw 설정 정리 (낮은 리스크)
- `gateway.nodes.denyCommands`를 실제 유효 명령으로 교체하거나 제거
- 기대효과: 정책이 의도대로 동작
- 롤백: 변경 전 `openclaw.json` 백업 후 즉시 복원 가능

### B. macOS 방화벽 활성화 검토 (중간 리스크)
- 개인 사용 패턴(로컬 개발/원격접속 여부) 확인 후 적용
- 기대효과: 불필요한 인바운드 노출 감소
- 롤백: 방화벽 비활성화 가능

### C. 주간 점검 자동화 (낮은 리스크)
- 주 1회:
  - `openclaw security audit`
  - `openclaw update status`
- 기대효과: 문제 조기 발견

## 6) 다음 액션 선택 (숫자로 답장)
1. 지금 바로 **변경 없이** 리포트만 유지
2. `denyCommands`부터 안전하게 정리
3. 방화벽까지 포함해 단계별 하드닝 진행
4. 주간 자동 점검(cron) 설정
5. 2+4 같이 진행 (실무 추천)
