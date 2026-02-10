#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Web App for PDF Quotation to CSV Converter
"""

import streamlit as st
import pandas as pd
import io
from converter import QuotationConverter

# 페이지 설정
st.set_page_config(
    page_title="PDF 견적서 변환기",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-header">📄 PDF 견적서 → CSV 변환기</div>', unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.header("ℹ️ 사용 방법")
    st.markdown("""
    1. PDF 견적서 파일 업로드
    2. 자동 변환 대기
    3. 결과 확인 및 다운로드
    
    ---
    
    ### ✨ 특징
    - ✅ 복잡한 테이블 구조 지원
    - ✅ 병합된 셀 처리
    - ✅ 정확한 데이터 추출
    - ✅ Python pdfplumber 사용
    
    ---
    
    ### 📋 지원 형식
    - 텍스트 기반 PDF
    - 견적서 테이블 구조
    - Item, Product, MOQ 등 필드
    
    ---
    
    ### 🔒 개인정보 보호
    모든 처리는 서버에서 이루어지며,
    파일은 처리 후 즉시 삭제됩니다.
    """)
    
    st.markdown("---")
    st.markdown("**버전:** 1.0.0")
    st.markdown("**엔진:** pdfplumber")

# 메인 콘텐츠
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="info-box">💡 PDF 견적서 파일을 업로드하면 자동으로 CSV로 변환됩니다.</div>', unsafe_allow_html=True)

    # 파일 업로드
    uploaded_file = st.file_uploader(
        "PDF 파일 선택",
        type=['pdf'],
        help="텍스트 기반 PDF 견적서를 업로드하세요 (스캔 이미지 PDF는 지원하지 않습니다)"
    )

with col2:
    st.markdown("### 📊 변환 통계")
    if 'stats' in st.session_state:
        st.metric("변환된 항목", st.session_state.stats['items'])
        st.metric("처리 시간", f"{st.session_state.stats['time']:.2f}초")
    else:
        st.info("파일을 업로드하면 통계가 표시됩니다")

# 파일 처리
if uploaded_file is not None:
    try:
        # 진행 표시
        with st.spinner('🔄 PDF 파일 처리 중...'):
            import time
            start_time = time.time()
            
            # 임시 파일로 저장
            temp_pdf_path = f"/tmp/{uploaded_file.name}"
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 변환 실행
            converter = QuotationConverter(temp_pdf_path)
            result = converter.convert()
            
            # CSV 생성
            csv_buffer = io.StringIO()
            result.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            csv_content = csv_buffer.getvalue()
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # 통계 저장
            st.session_state.stats = {
                'items': len(result),
                'time': processing_time
            }
        
        # 성공 메시지
        st.markdown(f'<div class="success-box">✅ 변환 완료! {len(result)}개 항목이 추출되었습니다.</div>', unsafe_allow_html=True)
        
        # 결과 표시
        st.markdown("### 📋 변환 결과 미리보기")
        
        # 탭으로 구분
        tab1, tab2 = st.tabs(["📊 테이블 뷰", "📄 CSV 원본"])
        
        with tab1:
            st.dataframe(
                result,
                use_container_width=True,
                height=400
            )
        
        with tab2:
            st.code(csv_content, language='csv')
        
        # 다운로드 버튼
        st.markdown("### 💾 다운로드")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv_content,
                file_name=uploaded_file.name.replace('.pdf', '.csv'),
                mime='text/csv',
                use_container_width=True
            )
        
        with col2:
            # Excel 다운로드 옵션
            excel_buffer = io.BytesIO()
            result.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            
            st.download_button(
                label="📊 Excel 다운로드",
                data=excel_buffer,
                file_name=uploaded_file.name.replace('.pdf', '.xlsx'),
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        
        # 파일 정보
        st.markdown("### 📄 파일 정보")
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.metric("열 수", len(result.columns))
        
        with info_col2:
            st.metric("행 수", len(result))
        
        with info_col3:
            st.metric("파일 크기", f"{len(csv_content) / 1024:.1f} KB")
        
    except Exception as e:
        st.markdown(f'<div class="error-box">❌ 오류 발생: {str(e)}</div>', unsafe_allow_html=True)
        st.error("변환 중 문제가 발생했습니다. PDF 파일이 올바른 견적서 형식인지 확인해주세요.")
        
        with st.expander("🔍 오류 상세 정보"):
            st.code(str(e))
            
        st.markdown("""
        ### 💡 문제 해결 팁:
        - PDF가 텍스트 기반인지 확인 (스캔 이미지가 아닌)
        - 파일이 손상되지 않았는지 확인
        - 테이블 구조가 있는지 확인
        - 다른 브라우저에서 시도
        """)

else:
    # 초기 화면
    st.info("👆 위의 파일 업로드 버튼을 클릭하여 PDF 견적서를 선택하세요.")
    
    # 데모/설명
    st.markdown("### 🎯 변환 프로세스")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 1️⃣ 업로드")
        st.markdown("PDF 파일 선택")
    
    with col2:
        st.markdown("#### 2️⃣ 분석")
        st.markdown("테이블 추출")
    
    with col3:
        st.markdown("#### 3️⃣ 변환")
        st.markdown("CSV 생성")
    
    with col4:
        st.markdown("#### 4️⃣ 다운로드")
        st.markdown("결과 저장")
    
    st.markdown("---")
    
    # 샘플 결과 표시
    st.markdown("### 📊 예상 결과 형식")
    sample_data = {
        'Date': ['Dec. 22, 2025'],
        'Customer': ['Daeyoung Chaevi Co., Ltd.'],
        'Planner': [''],
        'Product': ['NACS Charging Cable_J3400'],
        'Rated Current': ['250A'],
        'Cable Length': ['6.5M'],
        'Description': ['Production Site: China\nKC Certification'],
        'Delivery Term': ['FOB SH'],
        'MOQ': ['1'],
        'Price': ['$535.62'],
        'L/T': ['4-6'],
        'Remark': ['Sample']
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    PDF Quotation to CSV Converter | 
    Powered by pdfplumber & Streamlit | 
    © 2025
</div>
""", unsafe_allow_html=True)
