"""
Module tạo gợi ý phù hợp với từng bước
"""
import json
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS
from prompt_engineering.dialogue_prompts import HINT_GENERATION_PROMPT

class HintGenerator:
    """
    Lớp tạo gợi ý cho học sinh dựa trên bước hiện tại và số lần thử
    """
    
    def __init__(self):
        """
        Khởi tạo generator
        """
        self.llm = LLMInterface()
        self.model_config = MODELS["hint_generator"]
    
    def generate_hint(self, step, attempt_count, conversation_history):
        """
        Tạo gợi ý phù hợp với bước hiện tại và số lần thử
        
        Args:
            step (dict): Thông tin về bước hiện tại
            attempt_count (int): Số lần học sinh đã thử ở bước này
            conversation_history (list): Lịch sử hội thoại gần đây
            
        Returns:
            str: Gợi ý phù hợp
        """
        # Lấy thông tin từ bước hiện tại
        goal = step.get("goal", "")
        knowledge_needed = ", ".join(step.get("knowledge_needed", []))
        input_data = json.dumps(step.get("input_data", {}), ensure_ascii=False)
        calculation = step.get("calculation", "")
        expected_result = step.get("expected_result", "")
        explanation_logic = step.get("explanation_logic", "")
        
        # Lấy lịch sử hội thoại gần đây (tối đa 4 tin nhắn gần nhất)
        recent_messages = conversation_history[-4:] if len(conversation_history) > 0 else []
        recent_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
        
        # Chuẩn bị prompt
        prompt = HINT_GENERATION_PROMPT.format(
            goal=goal,
            knowledge_needed=knowledge_needed,
            input_data=input_data,
            calculation=calculation,
            expected_result=expected_result,
            explanation_logic=explanation_logic,
            attempt_count=attempt_count,
            recent_history=recent_history
        )
        
        # Gọi API để tạo gợi ý
        hint = self.llm.generate_content(prompt, self.model_config, with_system_prompt=False)
        
        return hint