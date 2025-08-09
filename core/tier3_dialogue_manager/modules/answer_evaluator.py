"""
Module đánh giá câu trả lời của học sinh
"""
import json
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS
from prompt_engineering.dialogue_prompts import ANSWER_EVALUATION_PROMPT
from core.tier2_solver.solution_formatter import extract_json

class AnswerEvaluator:
    """
    Lớp đánh giá câu trả lời của học sinh
    """
    
    def __init__(self):
        """
        Khởi tạo evaluator
        """
        self.llm = LLMInterface()
        self.model_config = MODELS["answer_evaluator"]
    
    def evaluate(self, student_answer, step):
        # Lấy thông tin từ bước hiện tại
        goal = step.get("goal", "")
        calculation = step.get("calculation", "")
        expected_result = step.get("expected_result", "")

        prompt = ANSWER_EVALUATION_PROMPT.format(
            goal=goal,
            calculation=calculation,
            expected_result=expected_result,
            student_answer=student_answer
        )
        
        # Gọi API để đánh giá câu trả lời
        response = self.llm.generate_content(prompt, self.model_config, with_system_prompt=True)
        
        # Xử lý kết quả
        try:
            # Nếu response là chuỗi JSON, parse thành dictionary
            if isinstance(response, str) and response.strip().startswith("{"):
                evaluation = json.loads(response)
            else:
                # Trích xuất JSON từ text nếu cần
                json_text = extract_json(response)
                evaluation = json.loads(json_text)
            return evaluation
        except json.JSONDecodeError as e:
            print(f"Lỗi khi phân tích JSON: {str(e)}")
            print(f"Response: {response}")
            
            # Trả về dictionary mặc định
            return {
                "is_correct": False,
                "correctness_level": "unknown",
                "feedback": "Tôi không thể đánh giá chính xác câu trả lời của bạn.",
                "suggestion": "Hãy thử diễn đạt cụ thể hơn về bước hiện tại.",
                "knowledge_gap": "Không xác định được"
            }