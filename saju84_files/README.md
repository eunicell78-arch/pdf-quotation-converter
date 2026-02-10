# saju84 - 사주팔자 만세력 계산기

웹 브라우저에서 바로 사용할 수 있는 사주팔자 만세력 계산기입니다.

## 🔮 주요 기능

- ✅ 정확한 사주팔자 계산 (1900-2100년)
- ✅ 음력/양력 자동 변환
- ✅ 태양시 보정 지원
- ✅ 절기 시간 정확히 반영
- ✅ 조자시/야자시 처리
- ✅ 오행 분석 및 시각화
- ✅ 웹 UI로 쉬운 사용

## 🚀 로컬 사용 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 웹 앱 실행
streamlit run app.py
```

웹 브라우저에서 http://localhost:8501 에 접속하여 사용할 수 있습니다.

## 🌐 Streamlit Cloud 배포

### 빠른 배포

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 배포 설정:
   - **Repository**: `eunicell78-arch/saju84`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. "Deploy!" 클릭

배포 후 자동으로 생성된 URL로 어디서든 접속 가능합니다! 🎉

## 🛠️ 기술 스택

- **Python 3.12**
- **Streamlit** - 웹 인터페이스
- **sajupy** - 사주팔자 계산 엔진
- **pandas** - 데이터 처리

## 📂 프로젝트 구조

```
saju84/
├── app.py                # 메인 Streamlit 애플리케이션
├── requirements.txt      # Python 패키지 의존성
├── .python-version       # Python 버전 (3.12)
├── .streamlit/
│   └── config.toml       # Streamlit 설정
└── README.md            # 프로젝트 문서
```

## 📚 참고 자료

- [sajupy GitHub](https://github.com/0ssw1/sajupy) - 사주팔자 계산 Python 라이브러리
- [manseryeok](https://github.com/yhj1024/manseryeok) - 만세력 계산 참고

## 🔗 관련 프로젝트

- [eunicell78-arch/pdf-quotation-converter](https://github.com/eunicell78-arch/pdf-quotation-converter) - PDF 견적서 변환기

## 📝 라이선스

MIT License
