"""
Module tạo gợi ý phù hợp với từng bước
"""
import json
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS

# Prompt riêng cho gợi ý đầu tiên
FIRST_HINT_PROMPT = """
Với tư cách là một gia sư toán học xuất sắc, hãy tạo câu hỏi gợi mở ĐẦU TIÊN cho bước này trong bài toán:

### THÔNG TIN BƯỚC HIỆN TẠI:
- Mục tiêu bước: {goal}
- Kiến thức cần thiết: {knowledge_needed}
- Dữ liệu đầu vào: {input_data}
- Phép tính/biến đổi: {calculation}
- Kết quả mong đợi: {expected_result}
- Giải thích logic: {explanation_logic}

### YÊU CẦU TẠO GỢI Ý ĐẦU TIÊN:

ĐÂY LÀ GỢI Ý ĐẦU TIÊN cho bước này - học sinh CHƯA THỬ GIẢI bước này trước đó.

1. NGUYÊN TẮC TẠO GỢI Ý ĐẦU TIÊN:
   - Đặt câu hỏi mở về cách tiếp cận ban đầu
   - KHÔNG giả định học sinh đã thực hiện bất kỳ bước nào trước đó
   - KHÔNG đề cập đến bất kỳ lỗi hay nỗ lực trước đây
   - Câu mở đầu cần khái quát lại bài toán để học sinh hiểu lại, giới thiệu qua về vùng kiến thức và hướng logic cơ bản. Từ đó, đưa ra câu hỏi đầu tiên để học sinh tiếp cận giải bài.

2. YÊU CẦU VỀ PHONG CÁCH:
   - Thân thiện, nhiệt tình
   - Có thể sử dụng 1 emoji phù hợp 
   - Ngôn ngữ phù hợp với học sinh lớp 9

3. TRÁNH TUYỆT ĐỐI:
   - KHÔNG gợi ý về phương pháp giải
   - KHÔNG giả định học sinh đã làm bất kỳ điều gì

TRẢ VỀ: Chỉ trả về nội dung gợi ý, không kèm theo giải thích hoặc lý do.
"""

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
        
        # Xử lý đặc biệt cho gợi ý đầu tiên
        if attempt_count == 0:
            # Sử dụng prompt riêng cho gợi ý đầu tiên
            prompt = FIRST_HINT_PROMPT.format(
                goal=goal,
                knowledge_needed=knowledge_needed,
                input_data=input_data,
                calculation=calculation,
                expected_result=expected_result,
                explanation_logic=explanation_logic
            )
        else:
            # Lấy lịch sử hội thoại gần đây (tối đa 4 tin nhắn gần nhất)
            recent_messages = conversation_history[-4:] if len(conversation_history) > 0 else []
            recent_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
            
            # Chuẩn bị prompt cho gợi ý tiếp theo
            from prompt_engineering.dialogue_prompts import HINT_GENERATION_PROMPT
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