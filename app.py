import streamlit as st
from sajupy import calculate_saju, solar_to_lunar, lunar_to_solar
from datetime import datetime
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="사주팔자 만세력 계산기",
    page_icon="🔮",
    layout="wide"
)

# 천간, 지지 한글 변환 사전
CELESTIAL_STEMS_KR = {
    '甲': '갑(甲)', '乙': '을(乙)', '丙': '병(丙)', '丁': '정(丁)', '戊': '무(戊)',
    '己': '기(己)', '庚': '경(庚)', '辛': '신(辛)', '壬': '임(壬)', '癸': '계(癸)'
}

EARTHLY_BRANCHES_KR = {
    '子': '자(子)', '丑': '축(丑)', '寅': '인(寅)', '卯': '묘(卯)', '辰': '진(辰)', '巳': '사(巳)',
    '午': '오(午)', '未': '미(未)', '申': '신(申)', '酉': '유(酉)', '戌': '술(戌)', '亥': '해(亥)'
}

FIVE_ELEMENTS = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

FIVE_ELEMENTS_KR = {
    '木': '목(木)', '火': '화(火)', '土': '토(土)', '金': '금(金)', '水': '수(水)'
}

def get_element_from_stem(stem):
    """천간에서 오행 추출"""
    return FIVE_ELEMENTS.get(stem, '')

# 타이틀
st.title("🔮 사주팔자 만세력 계산기")
st.markdown("---")

# 사이드바 - 설명
with st.sidebar:
    st.header("📖 사용 방법")
    st.markdown("""
    1. **생년월일 입력**: 양력 또는 음력 선택
    2. **출생 시간 입력**: 시와 분
    3. **출생 지역 입력**: 태양시 보정용 (선택사항)
    4. **계산 버튼 클릭**
    
    ### 주요 기능
    - ✅ 정확한 사주팔자 계산 (1900-2100년)
    - ✅ 음력/양력 자동 변환
    - ✅ 태양시 보정 지원
    - ✅ 절기 시간 정확히 반영
    - ✅ 조자시/야자시 처리
    
    ### 참고 사항
    - 태양시 보정: 정확한 출생 지역 입력 시 적용
    - 음력 윤달은 자동으로 처리됩니다
    - 시간은 24시간 형식으로 입력하세요
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 참고 자료")
    st.markdown("""
    - [sajupy GitHub](https://github.com/0ssw1/sajupy)
    - [manseryeok](https://github.com/yhj1024/manseryeok)
    """)

# 메인 컨텐츠
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📅 생년월일 입력")
    
    # 음력/양력 선택
    calendar_type = st.radio(
        "달력 종류",
        ["양력 (Solar)", "음력 (Lunar)"],
        horizontal=True
    )
    
    is_lunar = calendar_type.startswith("음력")
    
    # 날짜 입력
    col_date1, col_date2, col_date3 = st.columns(3)
    
    with col_date1:
        year = st.number_input("년도", min_value=1900, max_value=2100, value=1990, step=1)
    
    with col_date2:
        month = st.number_input("월", min_value=1, max_value=12, value=1, step=1)
    
    with col_date3:
        day = st.number_input("일", min_value=1, max_value=31, value=1, step=1)
    
    if is_lunar:
        is_leap = st.checkbox("윤달 여부", value=False)
    else:
        is_leap = False

with col2:
    st.subheader("⏰ 출생 시간")
    
    hour = st.number_input("시 (0-23)", min_value=0, max_value=23, value=0, step=1)
    minute = st.number_input("분 (0-59)", min_value=0, max_value=59, value=0, step=1)

# 고급 옵션
with st.expander("🔧 고급 옵션 (태양시 보정)"):
    use_solar_time = st.checkbox("태양시 보정 사용", value=False)
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        city = st.text_input("출생 도시", value="Seoul", 
                             help="예: Seoul, Busan, New York 등")
    
    with col_adv2:
        utc_offset = st.number_input("UTC 오프셋", value=9, 
                                     help="한국 표준시 = 9")

st.markdown("---")

# 계산 버튼
if st.button("🔮 사주팔자 계산하기", type="primary", use_container_width=True):
    try:
        with st.spinner("사주팔자를 계산하는 중..."):
            # 음력인 경우 양력으로 변환
            if is_lunar:
                lunar_result = lunar_to_solar(year, month, day, is_leap)
                solar_year = lunar_result['solar_year']
                solar_month = lunar_result['solar_month']
                solar_day = lunar_result['solar_day']
                st.info(f"음력 {year}년 {month}월 {day}일 {'(윤)' if is_leap else ''} → 양력 {solar_year}년 {solar_month}월 {solar_day}일")
            else:
                solar_year, solar_month, solar_day = year, month, day
                # 양력 -> 음력 변환 정보 표시
                lunar_result = solar_to_lunar(solar_year, solar_month, solar_day)
                st.info(f"양력 {year}년 {month}월 {day}일 → 음력 {lunar_result['lunar_year']}년 {lunar_result['lunar_month']}월 {lunar_result['lunar_day']}일 {'(윤)' if lunar_result['is_leap_month'] else ''}")
            
            # 사주팔자 계산
            if use_solar_time and city:
                result = calculate_saju(
                    solar_year, solar_month, solar_day, 
                    hour, minute,
                    city=city,
                    use_solar_time=True,
                    utc_offset=utc_offset
                )
            else:
                result = calculate_saju(
                    solar_year, solar_month, solar_day, 
                    hour, minute
                )
            
            st.success("✅ 사주팔자 계산 완료!")
            
            # 결과 표시
            st.markdown("---")
            st.header("📊 사주팔자 결과")
            
            # 사주팔자 테이블
            col_result1, col_result2, col_result3, col_result4 = st.columns(4)
            
            pillars = [
                ("시주 (時柱)", result['hour_pillar'], result['hour_stem'], result['hour_branch']),
                ("일주 (日柱)", result['day_pillar'], result['day_stem'], result['day_branch']),
                ("월주 (月柱)", result['month_pillar'], result['month_stem'], result['month_branch']),
                ("년주 (年柱)", result['year_pillar'], result['year_stem'], result['year_branch']),
            ]
            
            for col, (title, pillar, stem, branch) in zip([col_result1, col_result2, col_result3, col_result4], pillars):
                with col:
                    st.markdown(f"### {title}")
                    st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>{pillar}</h2>", unsafe_allow_html=True)
                    stem_element = get_element_from_stem(stem)
                    stem_kr = CELESTIAL_STEMS_KR.get(stem, stem)
                    branch_kr = EARTHLY_BRANCHES_KR.get(branch, branch)
                    element_kr = FIVE_ELEMENTS_KR.get(stem_element, stem_element)
                    st.markdown(f"<p style='text-align: center;'>천간: {stem_kr} ({element_kr})<br>지지: {branch_kr}</p>", unsafe_allow_html=True)
            
            # 상세 정보
            st.markdown("---")
            st.subheader("📋 상세 정보")
            
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.markdown(f"""
                **📅 생년월일 정보**
                - 출생일: {result['birth_date']}
                - 출생시간: {result['birth_time']}
                """)
                
                # 오행 분석
                st.markdown("**🌟 오행 분석**")
                elements_count = {}
                for stem in [result['year_stem'], result['month_stem'], result['day_stem'], result['hour_stem']]:
                    element = get_element_from_stem(stem)
                    elements_count[element] = elements_count.get(element, 0) + 1
                
                for element, count in sorted(elements_count.items()):
                    element_kr = FIVE_ELEMENTS_KR.get(element, element)
                    st.markdown(f"- {element_kr}: {count}개")
            
            with detail_col2:
                # 태양시 보정 정보
                if 'solar_correction' in result and result['solar_correction']:
                    sc = result['solar_correction']
                    st.markdown("**🌞 태양시 보정 정보**")
                    st.markdown(f"""
                    - 도시: {sc.get('city', 'N/A')}
                    - 경도: {sc.get('longitude', 'N/A')}°
                    - UTC 오프셋: {sc.get('utc_offset', 'N/A')}
                    - 보정 시간: {sc.get('correction_minutes', 'N/A')} 분
                    - 원래 시간: {sc.get('original_time', 'N/A')}
                    - 태양시: {sc.get('solar_time', 'N/A')}
                    """)
                
                # 자시 정보
                if result.get('zi_time_type'):
                    st.markdown(f"**⏰ 자시 정보**: {result['zi_time_type']}")
            
            # DataFrame으로 요약 표시
            st.markdown("---")
            st.subheader("📊 사주팔자 요약표")
            
            df_data = {
                '구분': ['년주 (年柱)', '월주 (月柱)', '일주 (日柱)', '시주 (時柱)'],
                '천간': [
                    CELESTIAL_STEMS_KR.get(result['year_stem'], result['year_stem']),
                    CELESTIAL_STEMS_KR.get(result['month_stem'], result['month_stem']),
                    CELESTIAL_STEMS_KR.get(result['day_stem'], result['day_stem']),
                    CELESTIAL_STEMS_KR.get(result['hour_stem'], result['hour_stem'])
                ],
                '지지': [
                    EARTHLY_BRANCHES_KR.get(result['year_branch'], result['year_branch']),
                    EARTHLY_BRANCHES_KR.get(result['month_branch'], result['month_branch']),
                    EARTHLY_BRANCHES_KR.get(result['day_branch'], result['day_branch']),
                    EARTHLY_BRANCHES_KR.get(result['hour_branch'], result['hour_branch'])
                ],
                '기둥': [
                    result['year_pillar'],
                    result['month_pillar'],
                    result['day_pillar'],
                    result['hour_pillar']
                ],
                '오행': [
                    FIVE_ELEMENTS_KR.get(get_element_from_stem(result['year_stem']), ''),
                    FIVE_ELEMENTS_KR.get(get_element_from_stem(result['month_stem']), ''),
                    FIVE_ELEMENTS_KR.get(get_element_from_stem(result['day_stem']), ''),
                    FIVE_ELEMENTS_KR.get(get_element_from_stem(result['hour_stem']), '')
                ]
            }
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {str(e)}")
        st.info("입력한 날짜와 시간을 확인해주세요. 1900-2100년 범위 내의 유효한 날짜여야 합니다.")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>사주팔자 만세력 계산기 | Powered by sajupy & Streamlit</p>
    <p>참고: @0ssw1/sajupy, @yhj1024/manseryeok</p>
</div>
""", unsafe_allow_html=True)
