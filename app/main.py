import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.components.chat_interface import render_chat_interface
from app.components.knowledge_gaps import render_knowledge_gaps
from app.utils.session_manager import init_session_state, reset_session
from config.app_config import APP_TITLE, APP_DESCRIPTION
from core.tier1_input_processor.intent_classifier import classify_intent
from core.tier1_input_processor.ocr_processor import process_image
from core.tier2_solver.problem_classifier import classify_problem
from core.tier2_solver.solver_selector import select_solver
from core.tier3_dialogue_manager.dialogue_manager import DialogueManager
from core.tier3_dialogue_manager.knowledge_analyzer import KnowledgeAnalyzer

def main():
    # Thiết lập trang
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🧮",
        layout="wide"
    )
    
    # Khởi tạo session state
    init_session_state()
    
    # Tiêu đề
    st.title(APP_TITLE)
    
    # Sidebar với thông tin
    with st.sidebar:
        st.header("Thông tin")
        st.info(APP_DESCRIPTION)
        
        # Nút để bắt đầu bài toán mới
        if st.button("Bài toán mới", use_container_width=True):
            reset_session()
            st.rerun()
        
        # Hiển thị thông tin phiên bản
        st.markdown("---")
        st.caption("Math Mentor AI - Phiên bản 0.1.0")
    
    # Khu vực Chat chính
    st.subheader("Hãy đặt câu hỏi toán học của bạn")
    
    # Xử lý phân tích lỗ hổng kiến thức nếu bài toán đã hoàn thành
    if st.session_state.get("dialogue_completed", False) and not st.session_state.get("knowledge_analysis"):
        with st.spinner("Đang phân tích lỗ hổng kiến thức..."):
            # Tạo knowledge analyzer
            analyzer = KnowledgeAnalyzer()
            
            # Phân tích lỗ hổng kiến thức
            knowledge_analysis = analyzer.analyze(
                st.session_state.solution_json,
                st.session_state.dialogue_manager.conversation_history
            )
            
            # Lưu kết quả phân tích
            st.session_state.knowledge_analysis = knowledge_analysis
    
    # Hiển thị phân tích lỗ hổng kiến thức nếu có
    if st.session_state.get("knowledge_analysis"):
        render_knowledge_gaps(st.session_state.knowledge_analysis)
    
    # Xử lý trạng thái hội thoại
    if "dialogue_manager" in st.session_state and not st.session_state.get("dialogue_completed", False):
        # Lấy gợi ý đầu tiên nếu chưa có
        if "first_hint_generated" not in st.session_state:
            with st.spinner("Đang chuẩn bị gợi ý..."):
                first_hint = st.session_state.dialogue_manager.generate_hint()
                st.session_state.first_hint_generated = True
                # Thêm tin nhắn vào lịch sử ứng dụng (không phải lịch sử của dialogue_manager)
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": first_hint
                })
    
    # Render giao diện chat tích hợp
    uploaded_file, user_input = render_chat_interface()
    
    # Xử lý đầu vào
    if not st.session_state.get("dialogue_manager"):
        # Chưa có dialogue_manager, xử lý đầu vào để bắt đầu bài toán
        if (uploaded_file or user_input) and not st.session_state.get("processing", False):
            # Đánh dấu đang xử lý
            st.session_state.processing = True
            
            # Xử lý OCR nếu có ảnh
            if uploaded_file:
                with st.spinner("Đang trích xuất đề bài từ ảnh..."):
                    try:
                        extracted_text = process_image(uploaded_file)
                        st.session_state.ocr_result = extracted_text
                        
                        # Đánh dấu đã xử lý hình ảnh
                        st.session_state.image_processed = True
                        
                        # Hiển thị kết quả OCR
                        with st.chat_message("assistant"):
                            st.markdown(f"**Đề bài từ ảnh:**\n\n{extracted_text}")
                        
                        # Thêm kết quả OCR vào lịch sử
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**Đề bài từ ảnh:**\n\n{extracted_text}"
                        })
                        
                    except Exception as e:
                        error_message = f"Xin lỗi, đã xảy ra lỗi khi xử lý ảnh: {str(e)}"
                        st.error(error_message)
                        
                        # Thêm thông báo lỗi vào lịch sử
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_message
                        })
            
            # Xử lý text input (hoặc kết quả OCR)
            text_to_process = user_input if user_input else st.session_state.ocr_result
            
            if text_to_process:
                # Phân loại ý định
                with st.spinner("Đang phân tích yêu cầu..."):
                    intent = classify_intent(text_to_process)
                    
                    # Xử lý dựa trên ý định
                    if intent == "math":
                        # Lưu đề bài
                        st.session_state.problem_text = text_to_process
                        
                        # Phân loại độ khó
                        with st.spinner("Đang phân tích độ khó của bài toán..."):
                            difficulty = classify_problem(text_to_process)
                            st.session_state.difficulty = difficulty
                        
                        # Chọn solver phù hợp
                        solver = select_solver(difficulty)
                        
                        # Giải bài toán
                        with st.spinner("Đang giải bài toán..."):
                            solution_json = solver.solve(text_to_process)
                            st.session_state.solution_json = solution_json
                        
                        # Tạo dialogue manager
                        st.session_state.dialogue_manager = DialogueManager(solution_json)
                        
                        # Hiển thị thông báo đã sẵn sàng giải
                        with st.chat_message("assistant"):
                            st.markdown(
                                f"Tôi đã phân tích bài toán của bạn. "
                                f"Hãy cùng giải nó từng bước một nhé!"
                            )
                        
                        # Thêm thông báo vào lịch sử
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Tôi đã phân tích bài toán của bạn. "
                            f"Hãy cùng giải nó từng bước một nhé!"
                        })
                    else:
                        # Từ chối yêu cầu không liên quan đến toán học
                        with st.chat_message("assistant"):
                            st.markdown(
                                "Xin lỗi, tôi chỉ có thể hỗ trợ về toán học. "
                                "Vui lòng đặt câu hỏi liên quan đến toán học để tôi có thể giúp bạn."
                            )
                        
                        # Thêm từ chối vào lịch sử
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "Xin lỗi, tôi chỉ có thể hỗ trợ về toán học. "
                            "Vui lòng đặt câu hỏi liên quan đến toán học để tôi có thể giúp bạn."
                        })
            
            # Đánh dấu đã xử lý xong
            st.session_state.processing = False
            
            # Refresh trang để hiển thị kết quả mới
            st.rerun()
    else:
        # Đã có dialogue_manager, xử lý hội thoại với học sinh
        if user_input and not st.session_state.get("processing", False):
            # Đánh dấu đang xử lý
            st.session_state.processing = True
            
            # Xử lý câu trả lời của học sinh
            with st.spinner("Đang đánh giá câu trả lời..."):
                response = st.session_state.dialogue_manager.evaluate_answer(user_input)
                
                # Hiển thị phản hồi
                with st.chat_message("assistant"):
                    st.markdown(response)
                
                # Thêm phản hồi vào lịch sử
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Kiểm tra nếu đã hoàn thành bài toán
                if st.session_state.dialogue_manager.is_completed():
                    st.session_state.dialogue_completed = True
                    
                    # Hiển thị thông báo hoàn thành
                    with st.success("🎉 Bài toán đã được giải xong!"):
                        st.markdown(
                            "Đang phân tích lỗ hổng kiến thức..."
                        )
            
            # Đánh dấu đã xử lý xong
            st.session_state.processing = False
            
            # Refresh trang để hiển thị kết quả mới
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("© 2025 Math Mentor AI - Trợ lý toán học thông minh")

if __name__ == "__main__":
    main()