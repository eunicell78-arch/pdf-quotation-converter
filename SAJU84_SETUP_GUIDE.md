# Saju84 Repository Setup Guide

이 문서는 `eunicell78-arch/saju84` 저장소에 만세력 계산기를 구축하기 위한 완벽한 가이드입니다.

## 📦 준비된 파일들

`saju84_files/` 디렉토리에 saju84 저장소에 필요한 모든 파일이 준비되어 있습니다:

```
saju84_files/
├── app.py                # 메인 Streamlit 애플리케이션
├── requirements.txt      # Python 패키지 의존성
├── .python-version       # Python 버전 (3.12)
├── .gitignore           # Git 제외 파일 목록
├── .streamlit/
│   └── config.toml      # Streamlit 설정
├── README.md            # 프로젝트 문서
└── DEPLOYMENT.md        # 배포 가이드
```

## 🚀 saju84 저장소 생성 방법

### 방법 1: GitHub 웹사이트에서 생성

1. GitHub에서 새 저장소 생성
   - Repository name: `saju84`
   - Description: "사주팔자 만세력 계산기 - Korean Four Pillars Calculator"
   - Public 또는 Private 선택
   - "Create repository" 클릭

2. 로컬에서 저장소 초기화 및 파일 추가:
   ```bash
   # 새 디렉토리 생성
   mkdir saju84
   cd saju84
   
   # Git 초기화
   git init
   
   # 준비된 파일들 복사
   cp -r /path/to/saju84_files/* .
   cp -r /path/to/saju84_files/.* .
   
   # Git 추가 및 커밋
   git add .
   git commit -m "Initial commit: Add Manseryeok calculator"
   
   # 원격 저장소 연결
   git remote add origin https://github.com/eunicell78-arch/saju84.git
   git branch -M main
   git push -u origin main
   ```

### 방법 2: GitHub CLI 사용

```bash
# GitHub CLI 설치 (이미 설치된 경우 생략)
# 저장소 생성
gh repo create eunicell78-arch/saju84 --public --description "사주팔자 만세력 계산기"

# 클론
git clone https://github.com/eunicell78-arch/saju84.git
cd saju84

# 준비된 파일들 복사
cp -r /path/to/saju84_files/* .
cp -r /path/to/saju84_files/.* .

# 커밋 및 푸시
git add .
git commit -m "Initial commit: Add Manseryeok calculator"
git push origin main
```

## 📝 파일 설명

### app.py
- Streamlit 기반 웹 애플리케이션
- 사주팔자 계산 기능
- 음력/양력 변환
- 태양시 보정
- 오행 분석

### requirements.txt
```
sajupy>=0.2.0        # 사주팔자 계산 엔진
streamlit>=1.54.0    # 웹 프레임워크
pandas>=2.0.0        # 데이터 처리
```

### .streamlit/config.toml
- Streamlit 테마 설정
- 서버 설정
- 브라우저 설정

### .python-version
- Python 3.12 명시
- Streamlit Cloud가 자동으로 인식

## 🌐 Streamlit Cloud 배포

저장소 생성 후:

1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. "New app" 클릭
3. 설정 입력:
   - Repository: `eunicell78-arch/saju84`
   - Branch: `main`
   - Main file path: `app.py`
4. "Deploy!" 클릭

배포 완료까지 약 2-3분 소요됩니다.

## ✅ 확인 사항

- [ ] GitHub에 saju84 저장소 생성 완료
- [ ] 모든 파일 업로드 완료
- [ ] Streamlit Cloud 배포 완료
- [ ] 웹 브라우저에서 앱 접속 테스트

## 🔗 참고 자료

- [sajupy GitHub](https://github.com/0ssw1/sajupy) - 사주팔자 계산 라이브러리
- [Streamlit 문서](https://docs.streamlit.io/) - Streamlit 공식 문서
- [Streamlit Cloud](https://streamlit.io/cloud) - 무료 배포 플랫폼

## 💡 추가 정보

### 로컬 테스트
```bash
cd saju84
pip install -r requirements.txt
streamlit run app.py
```

### 앱 기능
- 🔮 사주팔자 계산 (1900-2100년)
- 📅 음력/양력 자동 변환
- ⏰ 태양시 보정 지원
- 🌟 오행 분석
- 📊 결과 시각화

## ⚠️ 중요 사항

이 만세력 계산기는 **eunicell78-arch/saju84** 저장소에 있어야 합니다.
**pdf-quotation-converter** 저장소는 PDF 견적서 변환 전용입니다.
