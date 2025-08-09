"""
Module giải thích khi học sinh bế tắc
"""
import json
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS
from prompt_engineering.dialogue_prompts import DEADLOCK_EXPLANATION_PROMPT, FINAL_STEP_DEADLOCK_PROMPT, AUTO_ADVANCE_DEADLOCK_PROMPT

class DeadlockExplainer:
    
    def __init__(self):
        """
        Khởi tạo explainer
        """
        self.llm = LLMInterface()
        self.model_config = MODELS["medium_solver"]  # Dùng model mạnh hơn để giải thích
    
    def explain(self, step, conversation_history, is_final_step=False, auto_advance=False):
        # Lấy thông tin từ bước hiện tại
        goal = step.get("goal", "")
        knowledge_needed = ", ".join(step.get("knowledge_needed", []))
        input_data = json.dumps(step.get("input_data", {}), ensure_ascii=False)
        calculation = step.get("calculation", "")
        expected_result = step.get("expected_result", "")
        explanation_logic = step.get("explanation_logic", "")
        
        recent_messages = conversation_history[-6:] if len(conversation_history) > 0 else []
        recent_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
        
        # Chuẩn bị prompt phù hợp với từng trường hợp
        if is_final_step:
            # Sử dụng prompt đặc biệt cho bước cuối cùng
            prompt = FINAL_STEP_DEADLOCK_PROMPT.format(
                goal=goal,
                knowledge_needed=knowledge_needed,
                input_data=input_data,
                calculation=calculation,
                expected_result=expected_result,
                explanation_logic=explanation_logic,
                recent_history=recent_history
            )
        elif auto_advance:
            # Sử dụng prompt đặc biệt khi tự động chuyển bước
            prompt = AUTO_ADVANCE_DEADLOCK_PROMPT.format(
                goal=goal,
                knowledge_needed=knowledge_needed,
                input_data=input_data,
                calculation=calculation,
                expected_result=expected_result,
                explanation_logic=explanation_logic,
                recent_history=recent_history
            )
        else:
            # Sử dụng prompt mặc định
            prompt = DEADLOCK_EXPLANATION_PROMPT.format(
                goal=goal,
                knowledge_needed=knowledge_needed,
                input_data=input_data,
                calculation=calculation,
                expected_result=expected_result,
                explanation_logic=explanation_logic,
                recent_history=recent_history
            )
        
        # Gọi API để tạo giải thích
        explanation = self.llm.generate_content(prompt, self.model_config, with_system_prompt=False)
        
        return explanation