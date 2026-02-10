# 문제 분석 - Issue #2

## 업로드된 파일 분석

**PDF 파일**: `3QUO_NACS 250A KC_6.5m_Sample_20251222.pdf`
**현재 웹 변환 결과**: 모든 데이터가 Customer 열에 몰려있음 (완전히 잘못됨)

## 문제 원인

PDF의 테이블 구조:
```
Item | Product | Delivery Term | MOQ | Unit Price | L/T | Remark
-----|---------|---------------|-----|------------|-----|-------
  1  | NACS... |    FOB SH     |  1  |  $535.62   | 4-6 | Sample
     |         | DAP KR BY SEA |     |  $610.01   | 6-8 |
     |         | DAP KR BY AIR |     |  $709.19   | 4-6 |
```

**웹 변환기의 문제점:**
1. PDF.js는 pdfplumber와 달리 테이블을 자동 인식하지 못함
2. 현재 위치 기반 파싱이 이 PDF 구조에서 실패
3. 헤더 감지가 작동하지 않음
4. 모든 텍스트가 잘못된 열에 배치됨

## 해결 방법

**데스크톱 버전은 정상 작동** ✅
- pdfplumber가 테이블을 올바르게 추출
- 출력: 올바른 CSV with 1 row

**웹 버전 수정 필요** ❌
- 더 robust한 테이블 감지 알고리즘 필요
- 헤더 인식 개선
- 또는: 사용자에게 데스크톱 버전 사용 권장

## 권장 사항

이 PDF 구조는 웹 버전의 현재 구현으로는 처리하기 매우 어렵습니다.
**당장의 해결책: 데스크톱 버전 사용**

```bash
python converter.py sample_input.pdf output.csv
```

이렇게 하면 올바른 결과를 얻을 수 있습니다.
