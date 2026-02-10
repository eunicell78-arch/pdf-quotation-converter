# 🌐 GitHub Pages 활성화 방법

이 파일은 웹 버전을 활성화하기 위한 관리자용 안내입니다.

## ⚠️ 현재 상태: 404 오류 해결 방법

웹 링크가 404 오류를 반환하는 경우, GitHub Pages가 아직 활성화되지 않았기 때문입니다.

## 📋 GitHub Pages 설정하기

### 방법 1: 기존 브랜치 사용 (추천)

1. **GitHub 저장소 설정으로 이동**
   - https://github.com/eunicell78-arch/pdf-quotation-converter
   - 상단의 **Settings** (설정) 탭 클릭
   - 왼쪽 메뉴에서 **Pages** 클릭

2. **Source 설정**
   - Branch: `copilot/add-gui-for-pdf-to-csv` 선택
   - Folder: `/ (root)` 선택
   - **Save** 버튼 클릭

3. **배포 확인**
   - 몇 분 기다립니다 (보통 1-3분)
   - 페이지를 새로고침합니다
   - 상단에 다음과 같은 메시지가 나타납니다:
     ```
     ✅ Your site is published at https://eunicell78-arch.github.io/pdf-quotation-converter/
     ```

### 방법 2: gh-pages 브랜치 생성 (대안)

GitHub Pages는 `gh-pages` 브랜치를 자동으로 감지합니다:

```bash
# 현재 브랜치에서 gh-pages 브랜치 생성
git checkout copilot/add-gui-for-pdf-to-csv
git checkout -b gh-pages
git push origin gh-pages

# GitHub이 자동으로 감지하고 배포합니다
```

## 🔍 404 오류 해결

### 원인 1: GitHub Pages가 활성화되지 않음
**해결**: 위의 방법 1 또는 2를 따라 GitHub Pages를 활성화하세요.

### 원인 2: 잘못된 브랜치 선택
**해결**: Settings → Pages에서 올바른 브랜치(`copilot/add-gui-for-pdf-to-csv` 또는 `gh-pages`)를 선택했는지 확인하세요.

### 원인 3: 배포 진행 중
**해결**: 첫 배포는 3-5분 정도 걸릴 수 있습니다. 잠시 기다린 후 다시 시도하세요.

### 원인 4: 저장소가 Private
**해결**: GitHub Pages는 Public 저장소에서만 무료로 사용 가능합니다. Settings → General에서 저장소를 Public으로 변경하세요.

## 🔄 GitHub Pages 없이 사용하는 방법

GitHub Pages 설정이 어려운 경우, 다음 대안을 사용하세요:

### 대안 1: 로컬 웹 서버 실행

```bash
# 저장소 클론
git clone https://github.com/eunicell78-arch/pdf-quotation-converter.git
cd pdf-quotation-converter

# Python 웹 서버 실행 (Python 3 설치 필요)
python -m http.server 8000

# 브라우저에서 열기
# http://localhost:8000
```

### 대안 2: ZIP 다운로드 후 브라우저에서 열기

1. [ZIP 파일 다운로드](https://github.com/eunicell78-arch/pdf-quotation-converter/archive/refs/heads/copilot/add-gui-for-pdf-to-csv.zip)
2. 압축 해제
3. `index.html` 파일을 더블클릭하거나 브라우저로 드래그

⚠️ **주의**: 일부 브라우저는 보안상의 이유로 로컬 파일에서 PDF.js CDN을 차단할 수 있습니다. 이 경우 위의 로컬 웹 서버 방법을 사용하세요.

### 대안 3: Node.js 서버 사용

```bash
# npx를 사용한 간단한 서버 (Node.js 필요)
npx http-server -p 8000

# 또는 
npx serve
```

## 📁 웹 버전 파일 구조

```
pdf-quotation-converter/
├── index.html          # 메인 웹 페이지 ✅
├── styles.css          # 스타일시트 ✅
├── web-converter.js    # JavaScript 변환 로직 ✅
├── WEB_사용법.md       # 웹 버전 사용 가이드
├── README.md           # 프로젝트 메인 README
└── ... (기타 파일들)
```

✅ 표시된 3개 파일이 웹 버전 실행에 필요합니다.

---

## 🔧 선택사항: Custom Domain (선택)

사용자 정의 도메인을 사용하고 싶다면:

1. Settings → Pages로 이동
2. **Custom domain** 섹션에 도메인 입력
3. DNS 설정에 CNAME 레코드 추가:
   ```
   CNAME: eunicell78-arch.github.io
   ```
4. **Enforce HTTPS** 체크

---

## 📁 웹 버전 파일 구조

```
pdf-quotation-converter/
├── index.html          # 메인 웹 페이지
├── styles.css          # 스타일시트
├── web-converter.js    # JavaScript 변환 로직
├── WEB_사용법.md       # 웹 버전 사용 가이드
├── README.md           # 프로젝트 메인 README (웹 링크 포함)
└── ... (기타 파일들)
```

---

## ✅ 완료 체크리스트

- [ ] GitHub Pages 활성화 완료
- [ ] 웹사이트 접속 확인
- [ ] PDF 업로드 테스트
- [ ] 변환 기능 테스트
- [ ] 모바일에서 테스트
- [ ] README의 링크 확인

---

## 🎯 웹 버전 주소

활성화 후 웹 버전은 다음 주소에서 사용할 수 있습니다:

**https://eunicell78-arch.github.io/pdf-quotation-converter/**

이 주소를:
- README.md에 추가했습니다 ✅
- 다운로드_방법.md에 추가했습니다 ✅
- 빠른시작.md에 추가했습니다 ✅
- WEB_사용법.md에 추가했습니다 ✅

---

## 🔄 업데이트 방법

웹 버전을 업데이트하려면:

1. `index.html`, `styles.css`, 또는 `web-converter.js` 파일 수정
2. 변경사항을 commit & push
3. GitHub Actions가 자동으로 배포 (1-3분 소요)
4. 사용자는 브라우저 새로고침으로 최신 버전 사용

---

## 📊 웹 버전 vs 데스크톱 버전

| 특징 | 웹 버전 | 데스크톱 버전 |
|------|---------|--------------|
| 파일 | index.html, styles.css, web-converter.js | converter.py, converter_gui.py |
| 실행 환경 | 웹 브라우저 | Python + tkinter |
| PDF 파싱 | PDF.js (JavaScript) | pdfplumber (Python) |
| 설치 | 불필요 | Python + 패키지 필요 |
| 업데이트 | 자동 (새로고침) | 수동 (재다운로드) |
| 플랫폼 | 모든 플랫폼 | Windows, Mac, Linux |

---

## 🛠️ 문제 해결

### 404 에러가 발생하면?
- Branch 이름이 정확한지 확인
- index.html이 루트 디렉토리에 있는지 확인
- 몇 분 기다린 후 다시 시도

### 변경사항이 반영되지 않으면?
- Git push가 완료되었는지 확인
- GitHub Actions 탭에서 배포 상태 확인
- 브라우저 캐시 강제 새로고침 (Ctrl+Shift+R 또는 Cmd+Shift+R)

### 웹 버전이 작동하지 않으면?
- 브라우저 콘솔(F12)에서 에러 확인
- PDF.js CDN이 로드되는지 확인
- JavaScript가 활성화되어 있는지 확인

---

## 📞 지원

문제가 있으면 GitHub Issues에 문의해주세요!
