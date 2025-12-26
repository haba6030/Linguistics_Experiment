# GitHub Pages 배포 가이드

이 실험을 GitHub Pages를 통해 온라인으로 호스팅하는 방법입니다.

## 📋 준비사항

1. GitHub 계정 (없으면 https://github.com 에서 가입)
2. 프로젝트 파일들이 준비된 상태

## 🚀 배포 단계

### 1단계: GitHub에 새 Repository 만들기

1. GitHub에 로그인
2. 우측 상단 **+** 버튼 → **New repository** 클릭
3. Repository 설정:
   - **Repository name**: `talren-spr-experiment` (또는 원하는 이름)
   - **Public** 선택 (GitHub Pages는 Public repository 필요)
   - **Add a README file** 체크 해제 (이미 파일이 있음)
   - **Create repository** 클릭

### 2단계: 로컬 프로젝트를 GitHub에 업로드

터미널/명령 프롬프트를 열고 프로젝트 폴더로 이동:

```bash
cd /Users/jinilkim/Library/CloudStorage/OneDrive-Personal/Desktop/2025-2/Expling/TermProject
```

Git 초기화 및 파일 추가:

```bash
# Git 저장소 초기화
git init

# .gitignore 파일 생성 (불필요한 파일 제외)
echo ".DS_Store" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore

# 모든 파일을 staging
git add .

# 첫 커밋 생성
git commit -m "Initial commit: Talren SPR experiment"

# GitHub repository와 연결 (YOUR_USERNAME을 본인 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/talren-spr-experiment.git

# main 브랜치로 이름 변경 (필요시)
git branch -M main

# GitHub에 업로드
git push -u origin main
```

### 3단계: GitHub Pages 활성화

1. GitHub repository 페이지로 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Pages** 클릭
4. **Source** 섹션:
   - **Branch**: `main` 선택
   - **Folder**: `/ (root)` 선택
   - **Save** 클릭
5. 몇 분 후 페이지 상단에 URL이 표시됩니다:
   ```
   Your site is published at https://YOUR_USERNAME.github.io/talren-spr-experiment/
   ```

## 🔗 실험 URL

배포가 완료되면 다음 URL로 접속 가능:

- **본 실험**: `https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html`
- **파일럿**: `https://YOUR_USERNAME.github.io/talren-spr-experiment/index_pilot.html`

리스트 지정:
- `https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html?list=1`
- `https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html?list=2`
- `https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html?list=3`
- `https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html?list=4`

## 🔄 실험 파일 업데이트하기

파일을 수정한 후 GitHub에 다시 업로드:

```bash
# 변경된 파일 확인
git status

# 변경 사항 staging
git add .

# 커밋 메시지와 함께 저장
git commit -m "Update experiment: [변경 내용 설명]"

# GitHub에 업로드
git push
```

GitHub Pages는 자동으로 업데이트됩니다 (1-2분 소요).

## ⚙️ Google Apps Script 설정 확인

GitHub Pages에서 실행하려면 **Google Apps Script URL이 올바르게 설정**되어 있어야 합니다.

### 확인할 파일:
- `js/experiment.js` → 23번째 줄
- `js/experiment_pilot.js` → 23번째 줄

```javascript
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
```

### Apps Script 배포 설정:
1. Google Sheets → 확장 프로그램 → Apps Script
2. **배포** → **배포 관리**
3. **액세스 권한**: "모든 사용자" (Anyone)
4. URL 복사하여 위 파일에 붙여넣기

## 🧪 테스트

배포 후 반드시 테스트:

1. **파일럿 테스트**: 짧은 버전으로 전체 플로우 확인
2. **브라우저 콘솔** (F12) 확인:
   ```
   Data counts:
   - SPR trials: 44 (pilot: 4)
   - Rating trials: 32 (pilot: 4)
   - MC trials: 23 (pilot: 3)
   ```
3. **Google Sheets** 확인: 모든 시트에 데이터 저장되는지 확인

## 📱 다양한 기기에서 테스트

- 데스크톱 (Chrome, Firefox, Safari)
- 모바일 (iOS Safari, Android Chrome)
- 다양한 화면 크기

## 🔒 보안 고려사항

- Google Apps Script URL은 공개되어도 안전합니다 (POST만 허용)
- 민감한 정보는 코드에 포함하지 마세요
- Google Sheets는 본인만 접근 가능하도록 설정

## 📊 참가자 모집

GitHub Pages URL을 참가자에게 배포:

**예시 안내문**:
```
실험 참여 링크:
https://YOUR_USERNAME.github.io/talren-spr-experiment/index.html

- 예상 소요 시간: 약 20-25분
- PC 또는 모바일 접속 가능
- Chrome 또는 Safari 브라우저 권장
```

## ❗ 문제 해결

### 페이지가 로딩되지 않음
- GitHub Pages 활성화 확인
- 2-3분 대기 후 다시 시도
- URL이 정확한지 확인

### 데이터가 저장되지 않음
1. 브라우저 콘솔(F12) 확인
2. Google Apps Script URL 확인
3. Apps Script 배포 권한 확인 ("모든 사용자")

### 스타일이 깨짐
- CSS 파일 경로 확인
- 브라우저 캐시 삭제 (Ctrl+Shift+R)

## 📞 지원

문제가 발생하면:
1. 브라우저 콘솔 스크린샷
2. Google Apps Script 실행 로그
3. GitHub repository 설정 확인

---

**참고**: GitHub Pages는 정적 파일만 호스팅합니다. 서버 사이드 코드는 Google Apps Script를 통해 실행됩니다.
