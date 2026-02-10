# Streamlit Cloud 배포 가이드

## 🚀 빠른 시작

이 애플리케이션은 Streamlit Cloud에서 무료로 배포할 수 있습니다.

### 1단계: Streamlit Cloud 접속

[Streamlit Cloud](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 로그인하세요.

### 2단계: 새 앱 배포

1. "New app" 버튼 클릭
2. 배포 설정 입력:
   ```
   Repository: eunicell78-arch/pdf-quotation-converter
   Branch: copilot/add-manseong-calculation-app
   Main file path: app.py
   ```
3. "Deploy!" 버튼 클릭

### 3단계: 배포 완료

- 배포는 보통 2-3분 정도 소요됩니다
- 배포가 완료되면 고유한 URL이 생성됩니다
- 이 URL을 통해 어디서든 앱에 접속할 수 있습니다

## 📋 배포 체크리스트

이 저장소는 다음 파일들이 이미 준비되어 있습니다:

- ✅ `app.py` - 메인 애플리케이션
- ✅ `requirements.txt` - Python 패키지 의존성
- ✅ `.streamlit/config.toml` - Streamlit 설정
- ✅ `.python-version` - Python 버전 명시

## 🔧 고급 설정 (선택사항)

### 커스텀 도메인 연결

Streamlit Cloud에서 커스텀 도메인을 연결할 수 있습니다:
1. 앱 설정에서 "Settings" 클릭
2. "Custom domain" 섹션에서 도메인 추가

### 환경 변수 설정

민감한 정보가 필요한 경우 환경 변수를 사용하세요:
1. 앱 설정에서 "Secrets" 클릭
2. TOML 형식으로 비밀 값 추가

### 자동 업데이트

- GitHub 저장소에 푸시하면 자동으로 앱이 재배포됩니다
- "Always rerun" 옵션으로 자동 재시작 설정 가능

## 🆘 문제 해결

### 배포 실패 시

1. **로그 확인**: Streamlit Cloud 대시보드에서 배포 로그 확인
2. **requirements.txt**: 모든 패키지가 올바르게 명시되어 있는지 확인
3. **Python 버전**: `.python-version` 파일에 올바른 버전이 명시되어 있는지 확인

### 앱 실행 오류

1. **의존성 오류**: requirements.txt에 누락된 패키지가 있는지 확인
2. **메모리 부족**: Streamlit Cloud 무료 플랜은 1GB RAM 제한이 있습니다
3. **타임아웃**: 초기 로딩 시간이 너무 길면 타임아웃이 발생할 수 있습니다

## 📚 추가 자료

- [Streamlit Cloud 공식 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit 포럼](https://discuss.streamlit.io/)
- [배포 예제](https://streamlit.io/gallery)

## 💡 팁

1. **무료 플랜 제한**: 
   - 3개의 퍼블릭 앱까지 무료
   - 1GB RAM, 1 CPU 코어
   - 무제한 뷰어

2. **성능 최적화**:
   - `@st.cache_data` 데코레이터로 데이터 캐싱
   - `@st.cache_resource` 데코레이터로 리소스 캐싱
   - 불필요한 재연산 방지

3. **보안**:
   - API 키나 비밀번호는 Streamlit Secrets 사용
   - 절대 코드에 민감한 정보 하드코딩하지 않기

## 🎉 배포 완료!

배포가 완료되면 다음과 같은 URL이 생성됩니다:
```
https://your-app-name.streamlit.app
```

이 URL을 공유하여 누구나 앱을 사용할 수 있게 하세요!
