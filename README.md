# PDF Quotation Converter

PDF 견적서를 CSV 파일로 자동 변환하는 Python 프로그램

---

## 🎯 코딩을 모르시는 분들은 여기를 보세요!

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