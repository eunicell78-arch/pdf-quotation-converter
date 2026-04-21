#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Web App for PDF Quotation to CSV Converter
"""

import streamlit as st
import pandas as pd
import io
import os
import time
import traceback
import tempfile
from datetime import datetime
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


def add_source_file_column(df, source_file):
    df_with_source = df.copy()
    df_with_source['source_file'] = source_file
    reordered_columns = [col for col in df_with_source.columns if col != 'source_file'] + ['source_file']
    return df_with_source[reordered_columns]


if 'saved_conversions' not in st.session_state:
    st.session_state.saved_conversions = []

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
    uploaded_files = st.file_uploader(
        "PDF 파일 선택",
        type=['pdf'],
        accept_multiple_files=True,
        help="텍스트 기반 PDF 견적서를 업로드하세요 (스캔 이미지 PDF는 지원하지 않습니다)"
    )

with col2:
    st.markdown("### 📊 변환 통계")
    if 'stats' in st.session_state:
        st.metric("변환된 항목", st.session_state.stats['items'])
        st.metric("변환된 파일", st.session_state.stats.get('files', 1))
        st.metric("처리 시간", f"{st.session_state.stats['time']:.2f}초")
    else:
        st.info("파일을 업로드하면 통계가 표시됩니다")

# 파일 처리
if uploaded_files:
    if st.button("🔄 선택한 PDF 변환 후 저장", type="primary", use_container_width=True):
        batch_results = []
        batch_errors = []

        with st.spinner('🔄 PDF 파일 처리 중...'):
            start_time = time.time()

            for uploaded_file in uploaded_files:
                temp_pdf_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_pdf_path = temp_file.name

                    converter = QuotationConverter(temp_pdf_path)
                    result = converter.convert()

                    st.session_state.saved_conversions.append({
                        'source_file': uploaded_file.name,
                        'result': result
                    })
                    batch_results.append((uploaded_file.name, result))
                except Exception as file_error:
                    batch_errors.append((uploaded_file.name, file_error, traceback.format_exc()))
                finally:
                    if temp_pdf_path and os.path.exists(temp_pdf_path):
                        os.remove(temp_pdf_path)

            end_time = time.time()
            processing_time = end_time - start_time

            st.session_state.stats = {
                'items': sum(len(result) for _, result in batch_results),
                'files': len(batch_results),
                'time': processing_time
            }

        if batch_results:
            extracted_rows = sum(len(result) for _, result in batch_results)
            st.markdown(
                f'<div class="success-box">✅ 변환 완료! {len(batch_results)}개 파일, '
                f'{extracted_rows}개 항목이 저장되었습니다.</div>',
                unsafe_allow_html=True
            )

            st.markdown("### 📋 이번 변환 결과 미리보기")
            latest_combined = pd.concat(
                [add_source_file_column(result, source_file) for source_file, result in batch_results],
                ignore_index=True
            )
            st.dataframe(latest_combined, use_container_width=True, height=300)

        for file_name, file_error, error_trace in batch_errors:
            st.markdown(
                f'<div class="error-box">❌ {file_name} 처리 실패: {type(file_error).__name__}: {str(file_error)}</div>',
                unsafe_allow_html=True
            )
            with st.expander(f"🔍 {file_name} 오류 상세 정보"):
                st.code(error_trace)

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

st.markdown("---")
st.markdown("### 🗂️ 저장된 변환 결과")

saved_conversions = st.session_state.saved_conversions

if saved_conversions:
    total_saved_rows = sum(len(item['result']) for item in saved_conversions)
    st.write(f"저장된 파일: {len(saved_conversions)}개 | 총 행 수: {total_saved_rows}개")

    saved_summary = pd.DataFrame([
        {'No.': idx + 1, '파일명': item['source_file'], '행 수': len(item['result'])}
        for idx, item in enumerate(saved_conversions)
    ])
    st.dataframe(saved_summary, use_container_width=True, height=220)

    combined_df = pd.concat(
        [add_source_file_column(item['result'], item['source_file']) for item in saved_conversions],
        ignore_index=True
    )
    combined_csv_buffer = io.StringIO()
    combined_df.to_csv(combined_csv_buffer, index=False, encoding='utf-8-sig')

    action_col1, action_col2 = st.columns([1, 1])
    with action_col1:
        combined_filename = f"quotations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        st.download_button(
            label="📥 전체 CSV 다운로드",
            data=combined_csv_buffer.getvalue(),
            file_name=combined_filename,
            mime='text/csv',
            use_container_width=True
        )

    with action_col2:
        if st.button("🗑️ Clear saved", use_container_width=True):
            st.session_state.saved_conversions = []
            if 'stats' in st.session_state:
                del st.session_state.stats
            st.rerun()

    if st.checkbox("저장된 데이터 미리보기 표시", value=False):
        st.dataframe(combined_df, use_container_width=True, height=320)
else:
    st.info("저장된 변환 결과가 없습니다.")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    PDF Quotation to CSV Converter | 
    Powered by pdfplumber & Streamlit | 
    © 2025
</div>
""", unsafe_allow_html=True)
