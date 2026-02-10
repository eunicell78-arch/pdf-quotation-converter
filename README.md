# PDF Quotation Converter

PDF 견적서를 CSV 파일로 자동 변환하는 Python 프로그램

## 📋 주요 기능

- PDF 견적서 자동 파싱
- Product 필드를 Rated Current, Cable Length, Description으로 자동 분리
- 병합된 셀 자동 반복 입력 (Delivery Term, MOQ)
- NRE List 항목 자동 처리
- 표준 CSV 양식으로 출력

## 🛠️ 요구사항

```bash
pip install pdfplumber pandas openpyxl
```

## 📂 프로젝트 구조

```
pdf-quotation-converter/
├── converter.py          # 메인 변환 프로그램
├── requirements.txt      # 필요한 패키지 목록
├── samples/             # 샘플 파일 폴더
│   ├── input/           # PDF 견적서 샘플
│   └── output/          # 변환된 CSV 샘플
└── README.md
```

## 🚀 사용 방법

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