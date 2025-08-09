"""
Module phân loại ý định người dùng
"""
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS

def classify_intent(text):
    """
    Phân loại ý định của người dùng (toán học / không phải toán học)
    
    Args:
        text (str): Văn bản đầu vào từ người dùng
        
    Returns:
        str: Loại ý định ('math' hoặc 'non_math')
    """
    # Khởi tạo LLM Interface
    llm = LLMInterface()
    
    # Prompt để phân loại ý định
    prompt = f"""
    Hãy phân loại yêu cầu sau đây có phải là câu hỏi hoặc yêu cầu về Toán học không:
    "{text}"
    
    Chỉ trả lời "math" nếu đây là câu hỏi hoặc yêu cầu liên quan đến Toán học,
    hoặc "non" nếu không liên quan đến Toán học.
    LƯU Ý QUAN TRỌNG: Bài toán có thể là một tình huống thực tế (in real life). Bạn cần phải đọc thật kĩ trước và xem xét trước khi đưa ra quyết định. 
    Không trả lời bất kỳ nội dung nào khác. NO EXPLANATION. 
    Output format: math / non (chọn một trong hai)
    """
    
    # Gọi API để phân loại ý định
    model_config = MODELS["intent_classification"]
    response = llm.generate_content(prompt, model_config, with_system_prompt=False)
    
    # Chuẩn hóa kết quả
    response = response.strip().lower()
    
    # Phân loại kết quả
    if "math" in response:
        return "math"
    else:
        return "non"