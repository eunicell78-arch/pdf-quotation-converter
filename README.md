# PDF Quotation Converter

PDF 견적서를 CSV 파일로 자동 변환하는 Python 프로그램

---

## 🌟 **NEW! Streamlit 웹 앱** (가장 쉽고 정확한 방법!)

### 🌐 웹에서 바로 사용하고 싶으신가요?

**👉 [웹배포 초간단 가이드](웹배포_초간단가이드.md) 보기!** 👈

**5분이면 웹 배포 완료!** Streamlit Cloud에 배포하면:
- ✅ **웹 브라우저에서 바로 접속** (Chrome, Safari, Firefox 등)
- ✅ **URL 공유** → 다른 사람도 사용 가능
- ✅ **설치 불필요** → Python 몰라도 됨
- ✅ **무료!** → 비용 0원
- ✅ **자동 업데이트** → 코드 변경 시 1-2분 내 자동 배포!

### ❓ "배포 후 내가 할 일이 있나요?"

**답변: 아무것도 안 하셔도 됩니다!** 🎉

- ✅ **이미 배포된 경우**: 자동 업데이트 (1-2분 내)
- ✅ **Reboot 불필요**: 자동으로 최신 버전 적용
- 📖 **자세한 설명**: [스트림릿_자동업데이트_설명.md](스트림릿_자동업데이트_설명.md)

### 🚀 로컬에서 실행 (개발자용)

```bash
streamlit run streamlit_app.py
```

브라우저가 자동으로 열립니다: http://localhost:8501

### ✨ Streamlit 버전의 장점

- ✅ **완벽한 정확도**: Python pdfplumber 사용 → 복잡한 PDF도 완벽 처리
- ✅ **드래그 앤 드롭**: 파일을 끌어다 놓기만 하면 변환 완료
- ✅ **실시간 미리보기**: 변환 결과를 즉시 확인
- ✅ **CSV & Excel**: 두 가지 형식으로 다운로드
- ✅ **무료 배포**: Streamlit Cloud에 무료 호스팅 가능

### 📦 웹 배포 가이드

- 🆕 **[웹배포 초간단 가이드](웹배포_초간단가이드.md)** ← 이거 먼저 보세요!
- 📖 [STREAMLIT_배포.md](STREAMLIT_배포.md) ← 상세 가이드

**배포 링크:** https://share.streamlit.io (GitHub 계정으로 로그인 → 저장소 연결 → Deploy!)

---

## 🌐 HTML 웹 버전 (간단한 PDF용)

### ⚠️ GitHub Pages 설정 필요

웹 버전을 사용하려면 **GitHub Pages 활성화**가 필요합니다:

1. **저장소 관리자**가 다음을 수행해야 합니다:
   - GitHub 저장소 → Settings → Pages
   - Source: `copilot/add-gui-for-pdf-to-csv` 브랜치 선택
   - 또는 `gh-pages` 브랜치 생성 및 선택
   - Save 클릭

2. **활성화 후 웹 주소**:
   - 👉 **https://eunicell78-arch.github.io/pdf-quotation-converter/**

3. **자세한 설정 방법**: [GITHUB_PAGES_설정.md](GITHUB_PAGES_설정.md) 참고

### ⚠️ 웹 버전 제한사항 (중요!)

웹 버전은 PDF.js를 사용하여 브라우저에서 직접 변환합니다. 하지만 다음과 같은 경우 정확하지 않을 수 있습니다:

- ❌ 복잡한 테이블 구조 (헤더가 여러 줄에 걸쳐 있는 경우)
- ❌ 많은 병합 셀이 있는 경우
- ❌ 다단 레이아웃 또는 특수한 PDF 구조

**복잡한 PDF의 경우 데스크톱 버전을 사용하시면 훨씬 더 정확한 결과를 얻을 수 있습니다!**

### 🔄 최근 업데이트 (2026-02-10)

**✅ 수정 완료**: CSV 파일이 헤더만 나오고 내용이 비어있던 문제를 해결했습니다!
- 위치 기반 테이블 추출 알고리즘으로 개선
- 병합된 셀 처리 기능 향상
- 데이터 검증 및 명확한 오류 메시지 추가

브라우저 캐시를 지우고 새로고침(Ctrl+Shift+R)하면 최신 버전을 사용할 수 있습니다.

### 🔄 대체 방법 (GitHub Pages 없이 사용)

GitHub Pages가 설정되지 않은 경우, 다음 방법으로 사용하세요:

1. **다운로드 후 로컬 실행**:
   ```bash
   # 저장소 복제
   git clone https://github.com/eunicell78-arch/pdf-quotation-converter.git
   cd pdf-quotation-converter
   
   # 로컬 웹 서버 실행 (Python이 설치된 경우)
   python -m http.server 8000
   
   # 브라우저에서 접속
   # http://localhost:8000
   ```

2. **ZIP 다운로드 후 실행**:
   - [ZIP 다운로드](https://github.com/eunicell78-arch/pdf-quotation-converter/archive/refs/heads/copilot/add-gui-for-pdf-to-csv.zip)
   - 압축 해제
   - `index.html` 파일을 브라우저로 직접 열기

**특징:**
- ✅ **설치 불필요** - 웹브라우저에서 바로 사용
- ✅ **완전 무료** - 제한 없이 사용 가능
- ✅ **안전** - 파일이 서버로 전송되지 않음 (브라우저에서만 처리)
- ✅ **빠름** - 인터넷만 있으면 즉시 사용
- ✅ **모든 기기** - Windows, Mac, Linux, 스마트폰 모두 지원

**사용 방법:**
1. 위 링크 접속 (GitHub Pages 활성화 후)
2. PDF 파일 선택 (또는 드래그)
3. "변환 시작" 버튼 클릭
4. CSV 파일 자동 다운로드!

---

## 🎯 데스크톱 버전 (설치 필요)

코딩을 모르시는 분들을 위한 데스크톱 프로그램:

### 📥 빠른 다운로드 (초보자용)
- **[⚡ 빠른 시작 가이드](빠른시작.md)** - 5분이면 끝! (가장 간단함)
- **[📥 다운로드 및 사용 방법](다운로드_방법.md)** - 자세한 설명 포함

**빠른 시작:**
1. **[여기를 클릭하여 ZIP 파일 다운로드](https://github.com/eunicell78-arch/pdf-quotation-converter/archive/refs/heads/copilot/add-gui-for-pdf-to-csv.zip)**
2. ZIP 파일 압축 해제
3. Python 설치 ([다운로드](https://www.python.org/downloads/) - "Add to PATH" 체크!)
4. `run_converter.bat` 파일을 더블클릭하여 실행!

**더 자세한 내용은:**
- 👉 **[빠른시작.md](빠른시작.md)** - 5분만에 시작하기
- 👉 **[다운로드_방법.md](다운로드_방법.md)** - 상세 다운로드 가이드
- 👉 **[USAGE_GUI.md](USAGE_GUI.md)** - 사용법 및 문제 해결

---

## 📋 주요 기능

- PDF 견적서 자동 파싱
- Product 필드를 Rated Current, Cable Length, Description으로 자동 분리
- 병합된 셀 자동 반복 입력 (Delivery Term, MOQ)
- NRE List 항목 자동 처리
- 표준 CSV 양식으로 출력
- **🆕 사용하기 쉬운 GUI 인터페이스**
- **🆕 바탕화면 더블클릭 실행 지원**

## 🛠️ 요구사항

```bash
pip install pdfplumber pandas openpyxl
```

GUI 버전 추가 요구사항:
```bash
pip install pyinstaller  # EXE 파일 생성 시
```

## 📂 프로젝트 구조

```
pdf-quotation-converter/
├── converter.py          # CLI 변환 프로그램
├── converter_gui.py      # GUI 변환 프로그램 (새로 추가!)
├── run_converter.bat     # Windows GUI 실행 파일
├── build_exe.bat         # EXE 빌드 스크립트
├── requirements.txt      # 필요한 패키지 목록
├── USAGE_GUI.md         # GUI 상세 사용 가이드
├── samples/             # 샘플 파일 폴더
│   ├── input/           # PDF 견적서 샘플
│   └── output/          # 변환된 CSV 샘플
└── README.md
```

## 🚀 사용 방법

### 방법 1: GUI 버전 (추천 - 초보자용)

#### Option A: BAT 파일로 실행 (Python 설치 필요)
1. `run_converter.bat` 파일을 더블클릭
2. GUI 프로그램이 자동으로 실행됩니다
3. PDF 파일을 선택하고 저장 위치를 지정한 후 변환 시작!

#### Option B: EXE 파일로 실행 (Python 설치 불필요 - 추천!)
1. `build_exe.bat` 파일을 더블클릭하여 EXE 생성
2. `dist` 폴더의 `견적서변환기.exe` 파일을 바탕화면에 복사
3. 바탕화면의 EXE 파일을 더블클릭하여 실행
4. PDF 파일을 선택하고 저장 위치를 지정한 후 변환 시작!

**📖 자세한 GUI 사용법은 [USAGE_GUI.md](USAGE_GUI.md)를 참고하세요**

### 방법 2: CLI 버전 (명령줄)

```bash
python converter.py input.pdf output.csv
```

## 📊 변환 규칙

### CSV 컬럼 매핑
- Date = 견적서 Date
- Customer = 견적서 To
- Planner = 견적서 From
- Product = 견적서 Product (Rated Current 기준 윗줄)
- Rated Current = Product에서 추출
- Cable Length = Product에서 추출
- Description = Cable Length 아래 내용
- Delivery Term = 견적서 Delivery Term (병합 시 반복)
- MOQ = 견적서 MOQ (병합 시 반복, "Sample"이면 Qty=1)
- Price = 견적서 Unit Price
- L/T = 견적서 L/T(wks)
- Remark = 견적서 Remark (MOQ가 Sample이면 "Sample" 표시)

### 특수 처리
- Amount 컬럼 제거
- NRE List 항목 별도 처리
- 병합된 셀 자동 반복

## 📝 라이선스

MIT License