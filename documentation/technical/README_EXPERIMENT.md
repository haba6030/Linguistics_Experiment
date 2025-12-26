# Talren SPR Experiment

Self-Paced Reading (SPR) 실험을 위한 jsPsych 기반 온라인 실험 프로그램입니다.

## 📁 프로젝트 구조

```
.
├── index.html                  # 메인 HTML 파일
├── js/
│   ├── experiment.js          # 실험 로직 메인 스크립트
│   └── plugins/
│       └── jspsych-spr.js     # 커스텀 SPR 플러그인
├── css/
│   └── style.css              # 스타일시트
├── stimuli/
│   ├── list1.json             # 리스트 1 자극
│   ├── list2.json             # 리스트 2 자극
│   ├── list3.json             # 리스트 3 자극
│   └── list4.json             # 리스트 4 자극
├── data/                       # 서버 저장 데이터 (자동 생성)
├── server.js                   # Node.js 데이터 저장 서버
├── convert_csv_to_json.py     # CSV → JSON 변환 스크립트
├── package.json
└── README_EXPERIMENT.md        # 본 문서
```

## 🚀 빠른 시작

### 방법 1: 클라이언트 전용 (서버 없이 로컬 저장)

1. 웹 브라우저에서 `index.html` 파일을 직접 엽니다
2. 실험이 완료되면 자동으로 CSV 파일이 다운로드됩니다

**주의**: 파일 프로토콜(`file://`)에서는 JSON 로딩이 안 될 수 있습니다.
간단한 웹 서버를 사용하세요:

```bash
# Python 3 사용
python -m http.server 8000

# 또는 Python 2
python -m SimpleHTTPServer 8000

# 브라우저에서 http://localhost:8000 접속
```

### 방법 2: 서버 기반 데이터 저장

1. **Node.js 설치** (아직 설치 안 했다면)
   - https://nodejs.org/ 에서 다운로드

2. **의존성 패키지 설치**
   ```bash
   npm install
   ```

3. **서버 시작**
   ```bash
   npm start
   # 또는
   node server.js
   ```

4. **브라우저에서 접속**
   ```
   http://localhost:3000
   ```

5. **데이터 저장 활성화** (선택사항)
   - `js/experiment.js` 파일 열기
   - `on_finish` 함수에서 `saveDataToServer()` 주석 해제

## 🔧 실험 설정

### 리스트 할당

URL 파라미터로 리스트를 지정할 수 있습니다:

```
http://localhost:3000/?list=1    # List 1
http://localhost:3000/?list=2    # List 2
http://localhost:3000/?list=3    # List 3
http://localhost:3000/?list=4    # List 4
```

파라미터가 없으면 랜덤으로 리스트가 할당됩니다.

### 배경 문단 수정

`js/experiment.js` 파일에서 `BACKGROUND_PASSAGE` 변수를 찾아 실제 배경 텍스트로 교체하세요:

```javascript
const BACKGROUND_PASSAGE = `
  <div style="max-width: 700px; margin: 0 auto; text-align: left; line-height: 1.8;">
    <h2 style="text-align: center; margin-bottom: 30px;">탈렌족에 관한 배경 정보</h2>
    <p>
      여기에 실제 배경 문단을 입력하세요...
    </p>
  </div>
`;
```

### 연구자 정보 수정

`js/experiment.js` 파일의 디브리핑 섹션에서 연구자 연락처를 업데이트하세요.

## 📊 데이터 구조

### SPR 시행 데이터

각 문장 읽기 시행마다 다음 정보가 기록됩니다:

- `participant_id`: 참가자 ID (6자리 랜덤 숫자)
- `list_id`: 할당된 리스트 (1-4)
- `item_id`: 자극 항목 ID (예: E1, E2, F1...)
- `base`: 기본 항목 번호 (B1-B20)
- `emotion`: 감정 조건 (H=hate, N=neutral)
- `plausibility`: 그럴듯함 조건 (P=plausible, I=implausible)
- `version`: 버전 (1 또는 2)
- `is_filler`: 필러 여부 (0=실험 항목, 1=필러)
- `sentence_text`: 전체 문장
- `regions`: 지역별 텍스트 배열 (JSON 문자열)
- `region_rts`: 지역별 반응 시간 배열 (JSON 문자열)
- `total_reading_time`: 전체 읽기 시간 (ms)

### 그럴듯함 평가 데이터

- `item_id`, `emotion`, `plausibility`, `is_filler`
- `rating`: 1-5 척도 평가값

### 자유 회상 데이터

- `free_recall_text`: 자유 회상 응답

### 조작 점검 데이터

- `mc_type`: "modifier_negativity"
- `modifier_text`: 평가한 수식어
- `modifier_category`: "hate" 또는 "neutral"
- `rating`: 1-7 척도 부정성 평가

## 🔄 자극 파일 업데이트

CSV 파일을 수정한 후 JSON으로 다시 변환하려면:

```bash
python convert_csv_to_json.py
```

또는

```bash
npm run convert
```

## 🎨 스타일 커스터마이징

`css/style.css` 파일을 수정하여:
- 폰트 크기 조정
- 색상 테마 변경
- 레이아웃 수정

주요 CSS 클래스:
- `.spr-region`: SPR 텍스트 영역
- `.spr-instruction`: 하단 안내 문구
- `.jspsych-btn`: 버튼 스타일

## 🧪 실험 흐름

1. **환영/동의 화면**: 실험 설명 및 시작
2. **배경 문단**: 탈렌족에 대한 배경 정보
3. **SPR 안내**: 읽기 과제 방법 설명
4. **연습 시행**: 1회 연습
5. **본 실험**: 자극 문장 순차 제시 (SPR)
6. **휴식**
7. **그럴듯함 평가**: 각 문장의 진실성 평가
8. **자유 회상**: 기억나는 내용 작성
9. **조작 점검**: 수식어 부정성 평가
10. **디브리핑**: 실험 종료 및 설명

## 📝 데이터 분석

저장된 CSV 파일을 R 또는 Python으로 불러올 수 있습니다:

### R 예시

```r
library(tidyverse)
library(jsonlite)

# 데이터 불러오기
data <- read_csv("talren_spr_data_p123456_list1.csv")

# SPR 데이터만 필터
spr_data <- data %>%
  filter(trial_type == "spr_main")

# 지역별 RT 파싱
spr_data <- spr_data %>%
  mutate(
    region_rts_parsed = map(region_rts, fromJSON)
  )
```

### Python 예시

```python
import pandas as pd
import json

# 데이터 불러오기
data = pd.read_csv('talren_spr_data_p123456_list1.csv')

# SPR 데이터 필터
spr_data = data[data['trial_type'] == 'spr_main']

# RT 파싱
spr_data['region_rts_parsed'] = spr_data['region_rts'].apply(json.loads)
```

## ⚠️ 문제 해결

### JSON 파일을 불러올 수 없음
- 웹 서버를 통해 실행하고 있는지 확인 (`file://` 프로토콜 사용 불가)
- CORS 오류 발생 시 서버 사용 권장

### 데이터가 저장되지 않음
- 클라이언트 저장: 브라우저 다운로드 권한 확인
- 서버 저장: `server.js`가 실행 중인지, `data/` 폴더 쓰기 권한이 있는지 확인

### 한글이 깨짐
- 파일 인코딩이 UTF-8인지 확인
- CSV 변환 시 `encoding='utf-8-sig'` 사용

## 📧 문의

실험 관련 문의사항은 연구자에게 연락해주세요.

---

**개발 정보**
- jsPsych 버전: 7.3.4
- Node.js 서버: Express 4.x
- 폰트: Noto Sans KR (Google Fonts)
