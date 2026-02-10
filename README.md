# PDF Quotation Converter & 만세력 계산기

이 저장소에는 두 가지 도구가 있습니다:
1. **PDF 견적서 변환기** - PDF 견적서를 CSV 파일로 자동 변환
2. **사주팔자 만세력 계산기** - 웹 기반 사주팔자 계산 도구

---

## 🔮 사주팔자 만세력 계산기

웹 브라우저에서 바로 사용할 수 있는 사주팔자 만세력 계산기입니다.

### 주요 기능

- ✅ 정확한 사주팔자 계산 (1900-2100년)
- ✅ 음력/양력 자동 변환
- ✅ 태양시 보정 지원
- ✅ 절기 시간 정확히 반영
- ✅ 조자시/야자시 처리
- ✅ 오행 분석 및 시각화
- ✅ 웹 UI로 쉬운 사용

### 사용 방법

```bash
# 웹 앱 실행
streamlit run app.py
```

웹 브라우저에서 http://localhost:8501 에 접속하여 사용할 수 있습니다.

### 스크린샷

**입력 화면:**

![만세력 입력 화면](https://github.com/user-attachments/assets/829518d5-354f-474b-a1de-79c91f689d06)

**계산 결과:**

![만세력 결과 화면](https://github.com/user-attachments/assets/19e6a97e-38bb-4b67-93c8-7fcbc8d26d45)

### Streamlit Cloud 배포

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
2. GitHub 저장소 연결 (Sign in with GitHub)
3. "New app" 클릭
4. Repository: `eunicell78-arch/pdf-quotation-converter` 선택
5. Main file path: `app.py` 입력
6. Deploy 클릭

---

## 📄 PDF Quotation Converter

PDF 견적서를 CSV 파일로 자동 변환하는 Python 프로그램

## 📋 주요 기능

- PDF 견적서 자동 파싱
- Product 필드를 Rated Current, Cable Length, Description으로 자동 분리
- 병합된 셀 자동 반복 입력 (Delivery Term, MOQ)
- NRE List 항목 자동 처리
- 표준 CSV 양식으로 출력

## 🛠️ 요구사항

```bash
# 모든 의존성 설치
pip install -r requirements.txt
```

또는 개별 설치:
```bash
# PDF 변환기용
pip install pdfplumber pandas openpyxl

# 만세력 계산기용 (추가)
pip install sajupy streamlit
```

## 📂 프로젝트 구조

```
pdf-quotation-converter/
├── app.py                # 사주팔자 만세력 계산기 (Streamlit 웹앱)
├── converter.py          # PDF 견적서 변환 프로그램
├── requirements.txt      # 필요한 패키지 목록
├── .streamlit/
│   └── config.toml       # Streamlit 설정
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

## 🔗 관련 프로젝트

- [eunicell78-arch/saju84](https://github.com/eunicell78-arch/saju84) - 사주팔자 만세력 계산기 (별도 저장소)

## 📚 참고 자료

### 만세력 계산기
- [sajupy GitHub](https://github.com/0ssw1/sajupy) - 사주팔자 계산 Python 라이브러리
- [manseryeok](https://github.com/yhj1024/manseryeok) - 만세력 계산 참고

## 📝 라이선스

MIT License