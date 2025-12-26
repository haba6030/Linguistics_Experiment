# 🎯 최종 배포 체크리스트

GitHub에 업로드하기 전 반드시 확인하세요!

## ✅ 파일 구조 확인

```
TermProject/
├── index.html                      # 본 실험
├── index_pilot.html                # 파일럿 (테스트용)
├── css/
│   └── style.css                   # 스타일 (라디오 버튼 30px)
├── js/
│   ├── experiment.js               # 본 실험 로직
│   ├── experiment_pilot.js         # 파일럿 로직
│   └── plugins/
│       └── jspsych-spr.js          # SPR 플러그인
├── stimuli/
│   ├── list1.json                  # 리스트 1
│   ├── list2.json                  # 리스트 2
│   ├── list3.json                  # 리스트 3
│   └── list4.json                  # 리스트 4
├── google-apps-script.js           # Apps Script 코드 (참고용)
├── DEPLOY_GITHUB.md                # GitHub 배포 가이드
└── README_EXPERIMENT.md            # 실험 설명서
```

## ✅ 수정사항 반영 확인

### 1. 라디오 버튼 크기 ✓
- **css/style.css**:
  - 데스크톱: 30px × 30px
  - 모바일: 26px × 26px

### 2. 리커트 척도 통일 ✓
- **모든 리커트 척도**: 5점 척도로 통일
  - 그럴듯한 정도: 1-5점
  - 부정적 정도: 1-5점

### 3. 데이터 필터링 개선 ✓
- **experiment.js & experiment_pilot.js**:
  - SPR: `'spr'` 또는 `'spr_main'` 모두 허용
  - Rating: `'survey-likert'`에서 `item_id`로 구분
  - MC: `'survey-likert'`에서 `modifier_text`로 구분

### 4. 디버깅 로그 추가 ✓
- **콘솔 출력**:
  ```javascript
  Total trials: [숫자]
  All trial types: [배열]
  Data counts: {spr: X, rating: Y, mc: Z}
  ```

### 5. 파일럿 버전 축소 ✓
- **SPR**: 4개 문장
- **Rating**: 4개 문장
- **MC**: 3개 항목
- **예상 시간**: 약 2분

## ✅ Google Apps Script 설정

### 배포 전 확인사항:

1. **Apps Script 배포**
   - [ ] Google Sheets에서 Apps Script 열기
   - [ ] `google-apps-script.js` 코드 복사 & 붙여넣기
   - [ ] **배포** → **새 배포**
   - [ ] 유형: **웹 앱**
   - [ ] 액세스: **모든 사용자 (Anyone)**
   - [ ] 배포 URL 복사

2. **URL 업데이트**
   - [ ] `js/experiment.js` 23번째 줄
   - [ ] `js/experiment_pilot.js` 23번째 줄

   ```javascript
   const GOOGLE_SCRIPT_URL = 'YOUR_ACTUAL_SCRIPT_URL_HERE';
   ```

3. **Google Sheets 준비**
   - [ ] 5개 시트 생성: Metadata, SPR_Data, Rating_Data, Recall_Data, Manipulation_Check
   - [ ] 컬럼 헤더 설정 (GOOGLE_SHEETS_SETUP.md 참고)

## ✅ 로컬 테스트 (배포 전 필수!)

### 파일럿 테스트:
```bash
# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 열기
http://localhost:8000/index_pilot.html
```

### 확인사항:
- [ ] 실험이 끝까지 진행됨
- [ ] 브라우저 콘솔(F12)에서 데이터 카운트 확인:
  ```
  Data counts:
  - SPR trials: 4
  - Rating trials: 4
  - MC trials: 3
  ```
- [ ] Google Sheets에 모든 데이터 저장됨
- [ ] 라디오 버튼이 충분히 큼
- [ ] 리커트 척도가 모두 5점

### 본 실험 테스트 (선택):
```
http://localhost:8000/index.html?list=1
```

- [ ] 44개 SPR, 32개 Rating, 23개 MC 확인

## ✅ GitHub 업로드 준비

### 제외할 파일 확인:
- `.DS_Store` (macOS)
- `__pycache__/` (Python)
- `*.pyc` (Python 캐시)
- 테스트 데이터 파일

### Git 명령어:
```bash
cd /Users/jinilkim/Library/CloudStorage/OneDrive-Personal/Desktop/2025-2/Expling/TermProject

# Git 초기화
git init

# .gitignore 생성
echo ".DS_Store" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Talren SPR experiment"

# GitHub와 연결 (YOUR_USERNAME 변경 필요!)
git remote add origin https://github.com/YOUR_USERNAME/talren-spr-experiment.git

# 업로드
git branch -M main
git push -u origin main
```

## ✅ GitHub Pages 활성화

1. [ ] GitHub repository 페이지 → **Settings**
2. [ ] 왼쪽 메뉴 → **Pages**
3. [ ] Source: **main** 브랜치, **/ (root)** 폴더
4. [ ] **Save** 클릭
5. [ ] 2-3분 대기
6. [ ] URL 확인: `https://YOUR_USERNAME.github.io/talren-spr-experiment/`

## ✅ 배포 후 최종 테스트

### 온라인 테스트:
```
https://YOUR_USERNAME.github.io/talren-spr-experiment/index_pilot.html
```

### 확인사항:
- [ ] 페이지가 정상적으로 로드됨
- [ ] CDN 리소스 로드 확인 (jsPsych, Noto Sans KR 폰트)
- [ ] 실험 진행 가능
- [ ] Google Sheets에 데이터 저장
- [ ] 다양한 브라우저에서 테스트:
  - [ ] Chrome
  - [ ] Safari
  - [ ] Firefox
  - [ ] 모바일 Safari (iOS)
  - [ ] 모바일 Chrome (Android)

### 리스트 지정 테스트:
- [ ] `?list=1`
- [ ] `?list=2`
- [ ] `?list=3`
- [ ] `?list=4`

## 📊 데이터 수집 체크

실험 1회 실행 후 Google Sheets 확인:

### Metadata 시트:
- [ ] 1개 행 (참가자 정보)
- [ ] participant_id, list_id, timestamp 등

### SPR_Data 시트:
- [ ] 44개 행 (본 실험) 또는 4개 행 (파일럿)
- [ ] region_rts 컬럼에 RT 배열

### Rating_Data 시트:
- [ ] 32개 행 (본 실험) 또는 4개 행 (파일럿)
- [ ] rating 컬럼에 1-5 값

### Recall_Data 시트:
- [ ] 1개 행
- [ ] recall_text 컬럼에 텍스트

### Manipulation_Check 시트:
- [ ] 23개 행 (본 실험) 또는 3개 행 (파일럿)
- [ ] modifier_text, rating (1-5)

## 🎉 배포 완료!

모든 체크리스트를 완료했다면 **실험 준비 완료**입니다!

### 참가자에게 제공할 URL:
```
본 실험:
https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html

파일럿 (테스트용):
https://YOUR_USERNAME.github.io/talren-spr-experiment/index_pilot.html
```

### 참가자 안내사항:
- 예상 소요 시간: 약 20-25분 (파일럿: 2분)
- PC 또는 모바일 접속 가능
- Chrome 또는 Safari 브라우저 권장
- 조용한 환경에서 집중하여 참여

---

**문제 발생 시**: DEBUG_GUIDE.md 참고
