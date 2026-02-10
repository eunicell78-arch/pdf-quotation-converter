# 🔧 문제 해결: CSV 파일이 비어있는 경우

## 증상
"링크 접속했고, 파일변환 했는데 헤더만 나오고 내용은 전부 공란이야"

CSV 파일을 열었을 때 헤더 행(Date, Customer, Product 등)만 있고 데이터 행이 비어있습니다.

---

## ✅ 해결됨! (2026-02-10)

이 문제는 **수정되었습니다**. 최신 버전을 사용하세요:

### 1. 브라우저 캐시 지우기

웹 버전을 사용하는 경우, 브라우저 캐시를 지워야 최신 코드가 적용됩니다:

**Chrome/Edge:**
- `Ctrl + Shift + R` (Windows/Linux)
- `Cmd + Shift + R` (Mac)

**Firefox:**
- `Ctrl + F5` (Windows/Linux)
- `Cmd + Shift + R` (Mac)

**Safari:**
- `Cmd + Option + R`

또는:
1. 브라우저 설정 → 개인정보 → 인터넷 사용 기록 삭제
2. "캐시된 이미지 및 파일" 선택
3. 삭제 후 페이지 새로고침

### 2. 변환 다시 시도

캐시를 지운 후:
1. 웹 페이지 새로고침
2. PDF 파일 다시 선택
3. 변환 시작

---

## 🔍 여전히 문제가 있나요?

### 개발자 콘솔 확인

브라우저 개발자 도구를 열어 로그를 확인하세요:

1. **F12** 키를 누르거나 우클릭 → "검사"
2. **Console** 탭 선택
3. PDF 변환 시도
4. 콘솔에 표시되는 메시지 확인:

**정상 동작 시 표시되는 로그:**
```
Detected columns: {item: {...}, product: {...}, moq: {...}, ...}
Extracted items: [...]
Total items extracted: 5
```

**문제가 있을 때 표시되는 메시지:**
```
No table header found with Product and MOQ columns
Extracted items: []
Error: PDF에서 데이터를 추출할 수 없습니다
```

### 원인별 해결 방법

#### 원인 1: 테이블 헤더를 찾을 수 없음
**증상**: "No table header found with Product and MOQ columns"

**해결**:
- PDF에 "Product"와 "MOQ" 컬럼이 있는 테이블이 있는지 확인
- 테이블 형식이 아닌 스캔 이미지 PDF인 경우 데스크톱 버전도 변환 불가
- 올바른 견적서 형식인지 확인

#### 원인 2: 추출된 항목이 없음
**증상**: "Extracted items: []"

**해결**:
1. PDF가 텍스트 기반인지 확인 (스캔 이미지 아님)
2. 테이블 구조가 표준 형식인지 확인
3. 데스크톱 버전 사용 (더 강력한 파싱)

#### 원인 3: 브라우저 호환성
**해결**:
- Chrome 또는 Edge 브라우저 사용 (권장)
- 브라우저를 최신 버전으로 업데이트

---

## 🐛 기술적 배경 (개발자용)

### 수정 내용

이전 코드:
```javascript
// 단순히 숫자로 시작하는 라인만 찾음
if (line.match(/^\d+\s+/)) {
    currentItem = { item: ..., product: '', moq: '', ... };
}
// 모든 필드가 빈 값으로 남음!
```

수정된 코드:
```javascript
// 위치 기반 테이블 파싱
1. textContent.items의 X/Y 좌표 사용
2. Y 좌표로 행 그룹화
3. X 좌표로 열 정렬
4. 헤더에서 열 위치 파악
5. 데이터를 올바른 열에 배치
```

### 테이블 추출 알고리즘

1. **행 감지**: Y 좌표(수직 위치)로 텍스트 항목을 그룹화
2. **열 정렬**: 각 행 내에서 X 좌표(수평 위치)로 정렬
3. **헤더 찾기**: "Product"와 "MOQ"를 포함하는 행 찾기
4. **열 매핑**: 헤더의 X 위치를 사용하여 열 경계 결정
5. **데이터 추출**: 각 텍스트를 가장 가까운 열에 할당
6. **병합 셀 처리**: Item, Product, Delivery Term의 값 유지

---

## 💡 대안: 데스크톱 버전 사용

웹 버전이 제대로 작동하지 않으면 데스크톱 버전을 사용하세요:

### 장점:
- ✅ 더 강력한 PDF 파싱 (pdfplumber 라이브러리)
- ✅ 복잡한 테이블 구조 처리 가능
- ✅ 더 정확한 결과

### 사용 방법:
```bash
# Python 설치 후
pip install -r requirements.txt

# GUI 버전 실행
python converter_gui.py

# 또는 CLI 버전
python converter.py input.pdf output.csv
```

자세한 내용: [다운로드_방법.md](다운로드_방법.md)

---

## 📊 비교: 웹 vs 데스크톱

| 항목 | 웹 버전 | 데스크톱 버전 |
|------|---------|--------------|
| 설치 | 불필요 | Python + 패키지 필요 |
| PDF 파싱 | PDF.js (JavaScript) | pdfplumber (Python) |
| 테이블 추출 | 위치 기반 | 내장 테이블 추출 |
| 정확도 | 일반적인 PDF에 적합 | 복잡한 PDF도 처리 |
| 속도 | 빠름 | 더 빠름 |
| 오프라인 | 제한적 | 완전 지원 |

---

## 📞 여전히 도움이 필요하신가요?

1. **GitHub Issues 제출**:
   - https://github.com/eunicell78-arch/pdf-quotation-converter/issues
   - 문제가 발생한 PDF 파일 예제 첨부 (가능한 경우)
   - 브라우저 콘솔 로그 복사

2. **문서 참고**:
   - [WEB_사용법.md](WEB_사용법.md) - 웹 버전 상세 가이드
   - [404_해결가이드.md](404_해결가이드.md) - 접속 문제 해결
   - [USAGE_GUI.md](USAGE_GUI.md) - 데스크톱 버전 가이드

---

**요약**: 브라우저 캐시를 지우고 페이지를 새로고침하면 수정된 버전이 적용됩니다!
