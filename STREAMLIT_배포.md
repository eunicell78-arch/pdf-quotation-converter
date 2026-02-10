# 🚀 Streamlit 배포 가이드

## Streamlit Cloud에 배포하기 (추천!)

### 1️⃣ 준비사항
- GitHub 계정
- 이 저장소가 GitHub에 있어야 함

### 2️⃣ Streamlit Cloud 배포

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 방문
   - GitHub 계정으로 로그인

2. **New app 클릭**

3. **저장소 정보 입력**
   ```
   Repository: eunicell78-arch/pdf-quotation-converter
   Branch: copilot/add-gui-for-pdf-to-csv
   Main file path: streamlit_app.py
   ```

4. **Deploy! 클릭**
   - 자동으로 앱이 빌드되고 배포됩니다
   - 몇 분 후 URL이 생성됩니다

5. **완료!**
   - 생성된 URL을 공유하세요
   - 예: `https://your-app-name.streamlit.app`

---

## 로컬에서 실행하기

### 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
streamlit run streamlit_app.py
```

브라우저가 자동으로 열립니다: http://localhost:8501

---

## 📊 Streamlit vs 기존 웹 버전 비교

| 항목 | 기존 HTML/JS | Streamlit |
|------|-------------|-----------|
| **설치** | 불필요 | Python 필요 |
| **PDF 파싱** | PDF.js (제한적) | pdfplumber (강력) |
| **복잡한 PDF** | ❌ 실패 | ✅ 성공 |
| **정확도** | 낮음 | 높음 |
| **배포** | GitHub Pages | Streamlit Cloud |
| **유지보수** | 어려움 | 쉬움 |
| **서버 필요** | 없음 | Streamlit Cloud (무료) |

---

## 🎯 Streamlit의 장점

### ✅ 정확한 변환
- Python pdfplumber 직접 사용
- 복잡한 테이블 구조 완벽 처리
- 병합된 셀 자동 처리

### ✅ 쉬운 사용
- 드래그 앤 드롭
- 실시간 미리보기
- CSV & Excel 다운로드

### ✅ 무료 배포
- Streamlit Cloud 무료 티어
- HTTPS 자동 제공
- 자동 업데이트

### ✅ 확장 가능
- Python 코드로 쉽게 수정
- 새 기능 추가 간단
- API 통합 가능

---

## 🔧 커스터마이징

### 앱 제목 변경

`streamlit_app.py`의 2번째 줄 수정:
```python
st.set_page_config(
    page_title="여기에 새 제목",
    ...
)
```

### 색상 테마 변경

`.streamlit/config.toml` 파일 수정:
```toml
[theme]
primaryColor = "#FF0000"  # 메인 색상
backgroundColor = "#FFFFFF"  # 배경색
```

### 업로드 크기 제한 변경

`.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200  # MB 단위
```

---

## 🐛 문제 해결

### "Module not found" 오류
```bash
pip install -r requirements.txt
```

### Streamlit Cloud 배포 실패
1. requirements.txt 확인
2. Python 버전 확인 (3.8-3.11 권장)
3. 로그 확인

### 파일 업로드 안 됨
- 파일 크기 확인 (기본 200MB 제한)
- PDF 파일인지 확인
- 파일 손상 여부 확인

---

## 📞 도움말

- Streamlit 문서: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- GitHub Issues: 저장소 이슈 탭

---

## 🌐 배포된 앱 예시

배포가 완료되면 다음과 같은 URL을 얻게 됩니다:
```
https://pdf-quotation-converter.streamlit.app
```

이 URL을 누구나 접속하여 사용할 수 있습니다!

---

**Streamlit으로 복잡한 PDF도 완벽하게 변환하세요! 🎉**
