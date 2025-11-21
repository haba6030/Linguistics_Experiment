# Talren SPR Experiment

Self-Paced Reading (SPR) 실험: 탈렌족에 대한 혐오 표현과 그럴듯함 조작 연구

## 📋 실험 개요

- **과제**: 자기조절 읽기 (Self-Paced Reading)
- **독립변인**:
  - 감정 (Emotion): Hate vs. Neutral
  - 그럴듯함 (Plausibility): Plausible vs. Implausible
- **종속변인**:
  - 영역별 읽기 시간 (Region RT)
  - 그럴듯함 평가 (1-5점)
- **설계**: 2×2 Latin Square (4개 리스트)

## 🚀 빠른 시작

### 로컬 테스트

```bash
# 프로젝트 폴더로 이동
cd TermProject

# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 열기
# 파일럿: http://localhost:8000/index_pilot.html
# 본 실험: http://localhost:8000/index.html
```

### GitHub Pages 배포

1. **GitHub Repository 만들기**
   - GitHub 로그인 → New repository
   - Public으로 설정

2. **코드 업로드**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **GitHub Pages 활성화**
   - Repository → Settings → Pages
   - Source: main 브랜치, / (root)
   - Save

4. **URL 확인** (2-3분 후)
   ```
   https://YOUR_USERNAME.github.io/REPO_NAME/index.html
   ```

## ⚙️ Google Apps Script 설정

### 1. Google Sheets 생성

5개 시트를 만들고 아래 컬럼 추가:

**Metadata**: `Timestamp`, `Participant_ID`, `List_ID`, `Total_Duration`, `Browser`, `Screen_Width`, `Screen_Height`

**SPR_Data**: `Timestamp`, `Participant_ID`, `List_ID`, `Trial_Index`, `Item_ID`, `Base`, `Emotion`, `Plausibility`, `Version`, `Is_Filler`, `Sentence_Text`, `Regions`, `Region_RTs`, `Total_Reading_Time`

**Rating_Data**: `Timestamp`, `Participant_ID`, `List_ID`, `Item_ID`, `Base`, `Emotion`, `Plausibility`, `Stimulus_Text`, `Rating`, `RT`

**Recall_Data**: `Timestamp`, `Participant_ID`, `List_ID`, `Recall_Text`

**Manipulation_Check**: `Timestamp`, `Participant_ID`, `List_ID`, `Modifier_Text`, `Modifier_Category`, `Rating`, `RT`

### 2. Apps Script 배포

1. Google Sheets → 확장 프로그램 → Apps Script
2. `google-apps-script.js` 내용 복사 & 붙여넣기
3. **배포** → **새 배포**
4. 유형: **웹 앱**
5. 다음 권한으로 실행: **나**
6. 액세스 권한: **모든 사용자**
7. 배포 → URL 복사

### 3. URL 업데이트

`js/experiment.js`와 `js/experiment_pilot.js`의 23번째 줄:

```javascript
const GOOGLE_SCRIPT_URL = 'YOUR_SCRIPT_URL_HERE';
```

## 📁 프로젝트 구조

```
TermProject/
├── index.html                 # 본 실험 (20-25분)
├── index_pilot.html           # 파일럿 (2분)
├── css/
│   └── style.css
├── js/
│   ├── experiment.js          # 본 실험: 44 SPR, 32 Rating, 23 MC
│   ├── experiment_pilot.js    # 파일럿: 4 SPR, 4 Rating, 3 MC
│   └── plugins/
│       └── jspsych-spr.js
├── stimuli/
│   ├── list1.json            # Latin Square List 1
│   ├── list2.json            # Latin Square List 2
│   ├── list3.json            # Latin Square List 3
│   └── list4.json            # Latin Square List 4
└── google-apps-script.js      # Apps Script 코드 (참고용)
```

## 🔗 실험 URL

### 기본 URL
```
본 실험: https://YOUR_USERNAME.github.io/REPO_NAME/index.html
파일럿: https://YOUR_USERNAME.github.io/REPO_NAME/index_pilot.html
```

### 리스트 지정
```
?list=1  # List 1
?list=2  # List 2
?list=3  # List 3
?list=4  # List 4
```

예시:
```
https://YOUR_USERNAME.github.io/REPO_NAME/index.html?list=1
```

리스트를 지정하지 않으면 자동으로 무작위 할당됩니다.

## 🧪 테스트

### 로컬 테스트
1. 파일럿 실행 (`index_pilot.html`)
2. 브라우저 콘솔(F12) 확인:
   ```
   Data counts:
   - SPR trials: 4
   - Rating trials: 4
   - MC trials: 3
   ```
3. Google Sheets에서 데이터 확인

### 온라인 테스트
1. GitHub Pages URL에서 파일럿 실행
2. 다양한 브라우저/기기에서 테스트
   - Chrome, Safari, Firefox
   - 모바일 (iOS, Android)

## 📊 데이터 구조

### 본 실험
- **SPR**: 44개 문항 (실험 32 + 필러 12)
- **Rating**: 32개 (실험 문항만)
- **Recall**: 1개
- **MC**: 23개 (혐오 11 + 중립 12)

### 파일럿
- **SPR**: 4개 문항
- **Rating**: 4개
- **Recall**: 1개
- **MC**: 3개

## ❗ 문제 해결

### 데이터가 저장되지 않음
1. 브라우저 콘솔(F12)에서 에러 확인
2. Google Apps Script URL 확인
3. Apps Script 배포 권한: "모든 사용자"로 설정
4. Google Sheets 시트 이름 확인 (정확히 일치해야 함)

### 페이지가 로딩되지 않음
1. GitHub Pages 활성화 확인
2. 2-3분 대기 후 재시도
3. 브라우저 캐시 삭제 (Ctrl+Shift+R)

### 스타일이 깨짐
1. CSS 파일 경로 확인
2. CDN 리소스 로드 확인 (jsPsych, Noto Sans KR)

## 📱 권장 환경

- **브라우저**: Chrome, Safari, Firefox (최신 버전)
- **화면**: 최소 1024px 너비 권장
- **모바일**: 지원 (반응형 디자인)
- **시간**: 조용한 환경에서 20-25분 집중

## 📞 문의

문제 발생 시 브라우저 콘솔 스크린샷과 함께 문의해주세요.

---

Built with [jsPsych 7.3.4](https://www.jspsych.org/)
