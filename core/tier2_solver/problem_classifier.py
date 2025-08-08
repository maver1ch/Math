"""
Module phân loại đề bài toán
"""
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS
from prompt_engineering.solving_prompts import DIFFICULTY_CLASSIFICATION_PROMPT

def classify_problem(problem_text):
    """
    Phân loại độ khó của bài toán
    
    Args:
        problem_text (str): Đề bài toán
        
    Returns:
        int: Độ khó của bài toán (1-10)
    """
    # Khởi tạo LLM Interface
    llm = LLMInterface()
    
    # Chuẩn bị prompt
    prompt = DIFFICULTY_CLASSIFICATION_PROMPT.format(problem_text=problem_text)
    
    # Gọi API để phân loại bài toán
    model_config = MODELS["problem_classification"]
    response = llm.generate_content(prompt, model_config, with_system_prompt=False)
    
    # Xử lý kết quả
    try:
        # Lấy số nguyên từ response
        difficulty = int(response.strip())
        
        # Đảm bảo giá trị nằm trong khoảng 1-10
        difficulty = max(1, min(10, difficulty))
        
        return difficulty
    except:
        # Nếu không thể chuyển đổi thành số, trả về độ khó mặc định là 5
        print(f"Không thể phân loại độ khó, sử dụng giá trị mặc định. Response: {response}")
        return 5