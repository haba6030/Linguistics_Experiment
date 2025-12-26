# Google Sheets 데이터 저장 디버깅 가이드

Metadata와 Recall만 저장되고 SPR, Rating, MC 데이터가 저장되지 않는 문제 해결 방법입니다.

## 🔍 문제 진단

### 1단계: 브라우저 콘솔 확인

1. 실험을 끝까지 진행
2. **F12** 또는 **우클릭 > 검사** 눌러 개발자 도구 열기
3. **Console** 탭 선택
4. 다음 메시지 확인:

```
Data counts:
- SPR trials: 44          ← 이 숫자가 0이면 문제!
- Rating trials: 32       ← 이 숫자가 0이면 문제!
- Recall trials: 1
- MC trials: 23           ← 이 숫자가 0이면 문제!

Payload prepared:
- SPR data items: 44
- Rating data items: 32
- MC data items: 23
```

**만약 숫자가 0이라면**: 데이터가 제대로 수집되지 않음
**숫자가 정상이라면**: Apps Script 문제

---

### 2단계: Apps Script 로그 확인

1. Google Sheets 열기
2. **확장 프로그램** > **Apps Script**
3. 상단 메뉴에서 **실행** > **실행 로그** 클릭
4. 로그 메시지 확인:

```
saveCompleteData called
Participant ID: 123456
List ID: 1
SPR data length: 44       ← 0이면 문제!
Rating data length: 32    ← 0이면 문제!
MC data length: 23        ← 0이면 문제!
Metadata saved
SPR data saved: 44 items
Rating data saved: 32 items
Recall data saved
MC data saved: 23 items
```

---

## 🛠️ 해결 방법

### 방법 1: Apps Script 재배포

가장 흔한 원인은 Apps Script가 제대로 배포되지 않은 경우입니다.

1. Apps Script 에디터에서 **배포** > **배포 관리** 클릭
2. 기존 배포 옆 **편집** 버튼 클릭
3. **버전** > **새 버전** 선택
4. **배포** 클릭
5. 실험 다시 실행

---

### 방법 2: trial_type 확인

브라우저 콘솔에서 모든 데이터 확인:

```javascript
// 콘솔에 입력
jsPsych.data.get().values()
```

각 trial의 `trial_type` 필드 확인:
- SPR: `trial_type: 'spr_main'`
- Rating: `trial_type: 'plausibility_rating'`
- MC: `trial_type: 'manipulation_check'`

**만약 trial_type이 다르다면**: experiment.js 수정 필요

---

### 방법 3: 데이터 매핑 문제

Rating과 MC 데이터에서 `response.Q0`가 없을 수 있습니다.

#### Rating 데이터 확인

브라우저 콘솔:
```javascript
jsPsych.data.get().values().filter(t => t.trial_type === 'plausibility_rating')[0]
```

`response` 객체 구조 확인:
- 정상: `{Q0: 3}`
- 비정상: `{}`

#### 수정 방법

`experiment.js`의 rating_data 매핑 부분 (약 622줄):

**현재**:
```javascript
rating: trial.response ? trial.response.Q0 : null,
```

**수정** (jsPsych 7.x의 경우):
```javascript
rating: trial.response ? Object.values(trial.response)[0] : null,
```

---

### 방법 4: 전체 payload 확인

콘솔에서 전체 payload 복사:

```javascript
// 실험 완료 직후 콘솔에 입력
copy(JSON.stringify(payload))
```

1. payload를 복사
2. [JSONLint](https://jsonlint.com/)에 붙여넣기
3. 구조 확인

예상되는 구조:
```json
{
  "dataType": "complete",
  "participant_id": 123456,
  "list_id": 1,
  "spr_data": [...],     // 44개 항목
  "rating_data": [...],  // 32개 항목
  "mc_data": [...]       // 23개 항목
}
```

---

## 📝 체크리스트

실험을 다시 실행하기 전에 확인:

- [ ] Apps Script URL이 `experiment.js`에 올바르게 입력됨
- [ ] Apps Script가 최신 버전으로 배포됨
- [ ] 배포 권한이 "모든 사용자"로 설정됨
- [ ] 실험을 **끝까지** 진행 (중간에 새로고침 안 함)
- [ ] 브라우저 콘솔에 오류 없음

---

## 🔧 임시 해결책: 로컬 CSV 다시 활성화

Google Sheets가 작동하지 않는 경우, 임시로 로컬 저장 사용:

`experiment.js` 수정 (43-45줄):

```javascript
on_finish: function() {
  // Save data to Google Sheets
  saveDataToGoogleSheets();

  // Temporary: Also save locally
  jsPsych.data.get().localSave('csv', `talren_spr_data_p${participant_id}_list${list_id}.csv`);
}
```

---

## 🆘 여전히 문제가 있다면

1. **브라우저 콘솔 스크린샷** 찍기
2. **Apps Script 로그** 복사
3. **Google Sheets의 시트 목록** 확인
4. 위 정보와 함께 연구자에게 문의

---

## 📊 정상 작동 확인

실험 후 Google Sheets에서 다음 확인:

### Metadata 시트
- 1개 행 (참가자 정보)

### SPR_Data 시트
- 44개 행 (실험 + 필러)
- 컬럼: Timestamp, Participant_ID, Item_ID, Regions, Region_RTs 등

### Rating_Data 시트
- 32개 행 (실험 문항만)
- 컬럼: Timestamp, Participant_ID, Item_ID, Rating 등

### Recall_Data 시트
- 1개 행 (자유 회상)
- 컬럼: Timestamp, Participant_ID, Recall_Text

### Manipulation_Check 시트
- 23개 행 (수식어 평가)
- 컬럼: Timestamp, Participant_ID, Modifier_Text, Rating 등

**모든 시트가 제대로 채워져 있다면 성공!** ✅
