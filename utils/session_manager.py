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
    
    # Trạng thái dialogue manager
    if "dialogue_manager" not in st.session_state:
        st.session_state.dialogue_manager = None
    
    # Trạng thái gợi ý đầu tiên
    if "first_hint_generated" not in st.session_state:
        st.session_state.first_hint_generated = False
    
    # Trạng thái hoàn thành bài toán
    if "dialogue_completed" not in st.session_state:
        st.session_state.dialogue_completed = False
    
    # Kết quả phân tích lỗ hổng kiến thức
    if "knowledge_analysis" not in st.session_state:
        st.session_state.knowledge_analysis = None

def reset_session():
    """
    Reset session state để bắt đầu bài toán mới
    """
    # Giữ lại API key nếu có
    api_key = st.session_state.get("api_key", None)
    
    # Xóa tất cả các biến trong session state
    for key in list(st.session_state.keys()):
        if key != "api_key":
            del st.session_state[key]
    
    # Khôi phục API key nếu có
    if api_key:
        st.session_state.api_key = api_key
    
    # Khởi tạo lại session state
    init_session_state()