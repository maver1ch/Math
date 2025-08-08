import streamlit as st

def render_chat_interface():
    """
    Hiển thị giao diện chat tích hợp cho ứng dụng Math Mentor AI
    """
    # Hiển thị lịch sử chat nếu có
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                # Hiển thị nội dung text
                if "content" in message:
                    st.markdown(message["content"])
                
                # Hiển thị hình ảnh nếu có
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
        
        user_message = {"role": "user"}
        if user_input:
            user_message["content"] = user_input
        if uploaded_file:
            user_message["image"] = uploaded_file
        
        st.session_state.messages.append(user_message)
        
        # TODO: Xử lý OCR nếu có ảnh (sẽ triển khai trong bước tiếp theo)
        # TODO: Xử lý đầu vào text
        
        # Phản hồi tạm thời
        with st.chat_message("assistant"):
            if uploaded_file:
                st.markdown(
                    f"Tôi đã nhận được hình ảnh đề bài của bạn. "
                    f"Tính năng trích xuất đề bài từ ảnh sẽ được triển khai trong bước tiếp theo."
                )
                if user_input:
                    st.markdown(f"Bạn cũng nhập thêm: '{user_input}'")
            elif user_input:
                st.markdown(
                    f"Tôi đã nhận được câu hỏi của bạn: '{user_input}'\n\n"
                )
        
        # Thêm phản hồi vào lịch sử
        assistant_response = {
            "role": "assistant",
            "content": ""
        }
        
        st.session_state.messages.append(assistant_response)
        
    return uploaded_file, user_input