import streamlit as st

def render_image_uploader():
    uploaded_file = st.file_uploader(
        "Tải lên ảnh chứa đề bài toán",
        type=["png", "jpg", "jpeg"],
        help="Hỗ trợ các định dạng PNG, JPG, JPEG"
    )
    
    if uploaded_file is not None:
        # Hiển thị ảnh đã tải lên
        st.image(
            uploaded_file,
            caption="Ảnh đề bài đã tải lên",
            use_column_width=True
        )
        
        # Nút xử lý ảnh
        if st.button("Xử lý đề bài từ ảnh", use_container_width=True):
            with st.spinner("Đang trích xuất đề bài từ ảnh..."):
                # TODO: Sẽ thêm xử lý OCR ở bước tiếp theo
                # Hiện tại chỉ hiển thị thông báo
                st.success("Đã nhận được ảnh. Tính năng OCR sẽ được triển khai trong bước tiếp theo.")
                
                # Thêm tin nhắn giả lập vào lịch sử chat
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Tôi đã nhận được ảnh đề bài của bạn. Tính năng trích xuất đề bài từ ảnh sẽ được triển khai trong bước tiếp theo."
                })
    
    return uploaded_file