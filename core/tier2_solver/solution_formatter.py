"""
Module định dạng lời giải thành JSON có cấu trúc
"""
import json
import uuid
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS
from prompt_engineering.solving_prompts import SOLUTION_FORMATTING_PROMPT
import re

def format_solution(solution_text):
    """
    Chuyển đổi lời giải dạng text thành JSON có cấu trúc
    
    Args:
        solution_text (str): Lời giải dạng text
        
    Returns:
        dict: Lời giải dạng JSON có cấu trúc
    """
    # Khởi tạo LLM Interface
    llm = LLMInterface()
    
    # Chuẩn bị prompt
    prompt = SOLUTION_FORMATTING_PROMPT.format(solution_text=solution_text)
    
    # Gọi API để định dạng lời giải
    model_config = MODELS["easy_solver"]  
    response = llm.generate_content(prompt, model_config, with_system_prompt=False)
    
    # Xử lý kết quả
    try:
        # Chuyển đổi response thành JSON
        json_text = extract_json(response)
        formatted_solution = json.loads(json_text)
        return formatted_solution
    
    except Exception as e:
        print(f"Lỗi khi format JSON: {str(e)}")
        print(f"Response gốc: {response}")
        
        # Tạo JSON đơn giản từ text
        return create_simple_json(solution_text)
    
def extract_json(text):
    """Trích xuất phần JSON từ response"""
    # Tìm dấu { đầu tiên và } cuối cùng
    start = text.find('{') 
    end = text.rfind('}')
    
    if start >= 0 and end > start:
        return text[start:end+1]
    return "{}"  # Trả về JSON rỗng nếu không tìm thấy

def create_simple_json(solution_text):
    """Tạo JSON đơn giản từ text khi parsing thất bại"""
    # Chia lời giải thành các bước dựa trên "Bước X" hoặc dòng trống
    parts = re.split(r'Bước \d+:|(?:\r?\n){2,}', solution_text)
    steps = [p.strip() for p in parts if p.strip()]
    
    # Tìm đáp án cuối cùng (thường ở cuối bài)
    final_answer = ""
    for line in solution_text.split('\n'):
        if "đáp án" in line.lower() or "kết quả" in line.lower():
            final_answer = line
            break
    
    # Tạo JSON đơn giản
    result = {
        "problem_id": str(uuid.uuid4()),
        "final_answer": final_answer or "Xem các bước giải",
        "steps": []
    }
    
    # Thêm các bước
    for i, step in enumerate(steps):
        result["steps"].append({
            "step_id": i + 1,
            "goal": f"Bước {i+1}",
            "knowledge_needed": ["Kiến thức toán học"],
            "input_data": {},
            "calculation": step,
            "expected_result": "",
            "explanation_logic": ""
        })
    
    return result