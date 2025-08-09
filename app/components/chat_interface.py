import streamlit as st
from app.utils.llm_logger import LLMLogger

def render_chat_interface():
    # Hiển thị lịch sử chat nếu có
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        for i, message in enumerate(st.session_state.messages):
            # Bỏ qua tin nhắn trống hoặc tin nhắn tạm thời
            if message.get("content", "").strip() == "" or "Đang xử lý..." in message.get("content", ""):
                continue
                
            with st.chat_message(message["role"]):
                # Hiển thị nội dung text
                if "content" in message and message["content"].strip():
                    st.markdown(message["content"])
                
                # Hiển thị hình ảnh nếu có (chỉ ở tin nhắn đầu tiên)
                if "image" in message and message["image"] is not None:
                    st.image(message["image"], caption="Hình ảnh đề bài")
    
    # Nếu chưa có tin nhắn nào, hiển thị tin nhắn chào mừng
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            st.markdown(
                "Xin chào! Tôi là Math Mentor AI, trợ lý toán học của bạn. "
                "Tôi có thể giúp bạn giải các bài toán từ lớp 9. "
                "Hãy nhập đề bài hoặc tải lên ảnh chứa đề bài toán nhé!"
            )
            # Thêm tin nhắn chào mừng vào lịch sử
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Xin chào! Tôi là Math Mentor AI, trợ lý toán học của bạn. "
                "Tôi có thể giúp bạn giải các bài toán từ lớp 9. "
                "Hãy nhập đề bài hoặc tải lên ảnh chứa đề bài toán nhé!"
            })
    
    # Tạo container cho khu vực nhập liệu
    input_container = st.container()
    
    with input_container:
        # Tạo 2 cột: cột 1 cho upload hình ảnh, cột 2 cho chat input
        col1, col2 = st.columns([1, 6])
        
        with col1:
            # Upload hình ảnh
            uploaded_file = st.file_uploader(
                "📷",
                type=["png", "jpg", "jpeg"],
                label_visibility="collapsed",
                key="chat_image_uploader"
            )
        
        with col2:
            # Input chat
            user_input = st.chat_input("Nhập đề bài toán hoặc câu hỏi của bạn...", key="chat_text_input")
    
    # Xử lý khi có input (text hoặc hình ảnh hoặc cả hai)
    if user_input or uploaded_file:
        # Hiển thị tin nhắn của người dùng
        with st.chat_message("user"):
            if user_input:
                st.markdown(user_input)
            
            if uploaded_file:
                st.image(uploaded_file, caption="Hình ảnh đề bài đã tải lên")
        
        # Thêm tin nhắn vào lịch sử
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Tạo tin nhắn người dùng
        user_message = {"role": "user"}
        
        # Chỉ thêm nội dung nếu có text
        if user_input:
            user_message["content"] = user_input
        else:
            user_message["content"] = "" # Đảm bảo luôn có field content
            
        # Chỉ thêm hình ảnh vào tin nhắn đầu tiên
        if uploaded_file and "image_processed" not in st.session_state:
            user_message["image"] = uploaded_file
        
        # Chỉ thêm tin nhắn nếu có nội dung hoặc hình ảnh
        if user_input or (uploaded_file and "image_processed" not in st.session_state):
            st.session_state.messages.append(user_message)
        
        # Chỉ hiển thị thông báo xử lý khi chưa có dialogue_manager
        if "dialogue_manager" not in st.session_state:
            # Phản hồi tạm thời
            with st.chat_message("assistant"):
                if uploaded_file and "image_processed" not in st.session_state:
                    st.markdown("Tôi đã nhận được hình ảnh đề bài của bạn. Đang xử lý...")
                elif user_input:
                    st.markdown("Đang xử lý...")
            
            # Trong quá trình khởi tạo, thêm thông báo tạm thời vào lịch sử
            # Các thông báo này sẽ bị bỏ qua khi hiển thị
            temp_response = {
                "role": "assistant",
                "content": ""
            }
            
            if uploaded_file and "image_processed" not in st.session_state:
                temp_response["content"] = "Tôi đã nhận được hình ảnh đề bài của bạn. Đang xử lý..."
                # Đánh dấu đã xử lý hình ảnh để không hiển thị lại
                st.session_state.image_processed = True
            elif user_input:
                temp_response["content"] = "Đang xử lý..."
            
            # Chỉ thêm tin nhắn nếu có nội dung
            if temp_response["content"]:
                st.session_state.messages.append(temp_response)
    
    return uploaded_file, user_input