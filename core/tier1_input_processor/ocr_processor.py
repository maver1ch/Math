"""
Module xử lý OCR để trích xuất đề bài từ ảnh
"""
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS

def process_image(image_file):
    """
    Trích xuất đề bài toán từ ảnh
    
    Args:
        image_file: File ảnh đầu vào
        
    Returns:
        str: Đề bài toán đã trích xuất
    """
    # Khởi tạo LLM Interface
    llm = LLMInterface()
    
    # Prompt cho OCR
    prompt = """
    Bạn là một hệ thống OCR chuyên dụng cho đề toán học tiếng Việt.
    
    Hãy trích xuất đề bài toán từ ảnh này một cách chính xác. 
    Giữ nguyên cấu trúc, định dạng toán học và các ký hiệu đặc biệt.
    Đảm bảo mọi công thức, phương trình và số liệu được trích xuất chính xác.
    
    Chỉ trả về nội dung đề bài, không thêm bất kỳ giải thích, phân tích hoặc lời giải nào.
    """
    
    try:
        # Gọi API để xử lý ảnh
        model_config = MODELS["ocr"]
        extracted_text = llm.process_image(image_file, prompt, model_config)
        return extracted_text
    except Exception as e:
        print(f"Lỗi trong quá trình OCR: {str(e)}")
        return f"Xin lỗi, không thể trích xuất đề bài từ ảnh. Lỗi: {str(e)}"