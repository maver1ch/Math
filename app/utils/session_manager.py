import streamlit as st

def init_session_state():
    """
    Khởi tạo các biến trong session_state
    """
    # Khởi tạo danh sách tin nhắn nếu chưa có
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Trạng thái xử lý
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Dữ liệu đề bài
    if "problem_text" not in st.session_state:
        st.session_state.problem_text = None
    
    # Dữ liệu OCR
    if "ocr_result" not in st.session_state:
        st.session_state.ocr_result = None
    
    # Trạng thái bài toán
    if "problem_solved" not in st.session_state:
        st.session_state.problem_solved = False

def reset_session():
    """
    Reset session state để bắt đầu bài toán mới
    """
    st.session_state.messages = []
    st.session_state.processing = False
    st.session_state.problem_text = None
    st.session_state.ocr_result = None
    st.session_state.problem_solved = False