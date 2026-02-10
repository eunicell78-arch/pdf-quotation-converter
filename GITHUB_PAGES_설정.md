# 🌐 GitHub Pages 활성화 방법

이 파일은 웹 버전을 활성화하기 위한 관리자용 안내입니다.

## 📋 GitHub Pages 설정하기

### 1단계: GitHub 저장소 설정으로 이동

1. GitHub에서 이 저장소로 이동: https://github.com/eunicell78-arch/pdf-quotation-converter
2. 상단의 **Settings** (설정) 탭 클릭
3. 왼쪽 메뉴에서 **Pages** 클릭

### 2단계: Branch 설정

1. **Source** 섹션에서:
   - Branch: `copilot/add-gui-for-pdf-to-csv` 선택
   - Folder: `/ (root)` 선택
2. **Save** 버튼 클릭

### 3단계: 배포 확인

1. 몇 분 기다립니다 (보통 1-3분)
2. 페이지를 새로고침합니다
3. 상단에 다음과 같은 메시지가 나타납니다:
   ```
   ✅ Your site is published at https://eunicell78-arch.github.io/pdf-quotation-converter/
   ```

### 4단계: 테스트

1. 표시된 링크를 클릭합니다
2. 웹 변환기 페이지가 열리는지 확인합니다
3. PDF 파일을 업로드하고 변환을 테스트합니다

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
