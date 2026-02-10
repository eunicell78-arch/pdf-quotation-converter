# Issue #3 해결: 다중 페이지 PDF 변환 문제

## 문제 상황
"2페이지 이상인 견적서 파일로 테스트하면 변환이 누락돼"

## 원인 분석

### test1.pdf 구조 (3페이지)
- **Page 1**: 헤더가 있는 테이블 → 15개 항목 추출 ✅
- **Page 2**: **헤더 없는 연속 테이블** + NRE List → 0개 항목 추출 ❌
- **Page 3**: 헤더만 있음 (데이터 없음) → 0개 항목 ❌

### 근본 원인
Page 2의 메인 견적 테이블은 헤더 없이 바로 데이터로 시작하는 **연속 테이블**입니다:
```
Row 0: ['2-1', 'NACS Charging Cable...', 'FOB Shanghai', '50', '$635.70', '8-10', '']
```

이전 코드는 헤더에 "Product"와 "MOQ"가 **모두** 있는 테이블만 인식했기 때문에, 헤더 없는 연속 테이블을 무시했습니다.

## 해결 방법

### 1. 연속 테이블 자동 감지
헤더 없는 테이블도 다음 조건으로 자동 인식:
- 컬럼 수가 6-8개 (유연하게 설정)
- 가격 데이터에 $ 기호 포함
- 숫자 데이터 (MOQ) 포함

### 2. 헤더 유무에 따른 처리
```python
헤더 있음:
  → 헤더를 파싱하여 컬럼 위치 파악
  → 2번째 행부터 데이터 추출

헤더 없음:
  → 표준 컬럼 순서 가정 (Item, Product, Delivery Term, MOQ, Price, L/T, Remark)
  → 1번째 행부터 데이터 추출
```

### 3. 줄바꿈 처리
Delivery Term의 줄바꿈을 공백으로 변환:
- "FOB\nShanghai" → "FOB Shanghai"
- "DAP Korea\nby Sea\nFreight" → "DAP Korea by Sea Freight"

## 테스트 결과

### 수정 전
```bash
python converter.py test1.pdf output.csv
✅ Total rows: 16  # Page 1만 추출됨!
```

### 수정 후
```bash
python converter.py test1.pdf output.csv
✅ Total rows: 31  # 모든 페이지 추출됨!
```

### 페이지별 추출 결과
- **Page 1**: 15개 항목 (350A, 6M 케이블, 다양한 MOQ) ✅
- **Page 2**: 15개 항목 (350A, 7.62M 케이블, 다양한 MOQ) ✅
- **Page 2**: 1개 NRE 항목 (Crimping Fixture) ✅
- **총합**: 31개 행 완벽 추출 ✅

## 사용 방법

### 데스크톱 버전
```bash
python converter.py your_multipage.pdf output.csv
```

### Streamlit 웹 버전
1. Streamlit 앱 접속
2. PDF 파일 업로드
3. 자동 변환 및 다운로드

**Streamlit 앱이 배포되어 있다면 자동으로 업데이트됩니다!** (1-2분 소요)

## 검증 완료
- ✅ 3페이지 PDF 완벽 추출
- ✅ 헤더 있는 테이블 지원
- ✅ 헤더 없는 연속 테이블 지원
- ✅ Delivery Term 포맷 정리
- ✅ 코드 리뷰 통과
- ✅ 보안 검사 통과

## 추가 개선사항
- 컬럼 수 검증을 유연하게 변경 (정확히 7개 → 6-8개)
- 숫자 감지 로직 개선 (빈 문자열 처리)
- 더 강건한 테이블 인식

문제 완전 해결! 🎉
