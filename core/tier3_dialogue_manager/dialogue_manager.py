"""
Module quản lý hội thoại dẫn dắt sư phạm
"""
from core.tier3_dialogue_manager.modules.hint_generator import HintGenerator
from core.tier3_dialogue_manager.modules.answer_evaluator import AnswerEvaluator
from core.tier3_dialogue_manager.modules.deadlock_explainer import DeadlockExplainer
from llm.llm_interface import LLMInterface
import json

class DialogueManager:
    """
    Quản lý hội thoại giữa chatbot và học sinh
    """
    def __init__(self, solution_json):
        """
        Khởi tạo dialogue manager
        
        Args:
            solution_json (dict): Lời giải dạng JSON có cấu trúc
        """
        self.solution = solution_json
        self.current_step_id = 1
        self.attempts_on_current_step = 0
        self.conversation_history = []
        
        # Khởi tạo các module
        self.hint_generator = HintGenerator()
        self.answer_evaluator = AnswerEvaluator()
        self.deadlock_explainer = DeadlockExplainer()
    
    def get_current_step(self):
        """
        Lấy thông tin về bước hiện tại
        
        Returns:
            dict: Thông tin bước hiện tại hoặc None nếu đã hoàn thành
        """
        if self.current_step_id > len(self.solution["steps"]):
            return None
        
        return self.solution["steps"][self.current_step_id - 1]
    
    def generate_hint(self):
        """
        Tạo gợi ý cho bước hiện tại
        
        Returns:
            str: Gợi ý cho học sinh
        """
        current_step = self.get_current_step()
        if not current_step:
            return self._generate_completion_message()
        
        # Tạo gợi ý dựa trên số lần thử
        hint = self.hint_generator.generate_hint(
            current_step,
            self.attempts_on_current_step,
            self.conversation_history
        )
        
        # Cập nhật lịch sử hội thoại
        self.conversation_history.append({
            "role": "assistant",
            "content": hint
        })
        
        return hint
    
    def evaluate_answer(self, student_answer):
        """
        Đánh giá câu trả lời của học sinh
        
        Args:
            student_answer (str): Câu trả lời của học sinh
            
        Returns:
            str: Phản hồi cho học sinh
        """
        current_step = self.get_current_step()
        if not current_step:
            return "Bài toán đã được giải xong."
        
        # Cập nhật lịch sử
        self.conversation_history.append({
            "role": "user",
            "content": student_answer
        })
        
        # Đánh giá câu trả lời
        evaluation = self.answer_evaluator.evaluate(
            student_answer,
            current_step
        )
        
        if isinstance(evaluation, str):
            try:
                evaluation = json.loads(evaluation)
            except:
                evaluation = {
                    "is_correct": False,
                    "feedback": "Không thể đánh giá câu trả lời",
                    "suggestion": "Hãy thử lại với cách diễn đạt khác."
                }

        self.attempts_on_current_step += 1
        
        # Xử lý dựa trên kết quả đánh giá
        if evaluation["is_correct"]:
            response = self._handle_correct_answer(evaluation)
        elif self._is_deadlocked():
            response = self._handle_deadlock(current_step)
        else:
            response = self._handle_incorrect_answer(evaluation)
        
        # Cập nhật lịch sử
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _handle_correct_answer(self, evaluation):
        """
        Xử lý khi học sinh trả lời đúng
        
        Args:
            evaluation (dict): Kết quả đánh giá
            
        Returns:
            str: Phản hồi tích cực
        """
        # Tạo phản hồi tích cực
        feedback = evaluation.get("feedback", "Chính xác!")
        
        # Chuyển sang bước tiếp theo
        self.current_step_id += 1
        self.attempts_on_current_step = 0
        
        # Nếu còn bước tiếp theo, tạo gợi ý mới
        if self.current_step_id <= len(self.solution["steps"]):
            next_step = self.get_current_step()
            transition = f"Bây giờ chúng ta hãy chuyển sang {next_step['goal']}."
            return f"{feedback} {transition}"
        else:
            # Hoàn thành bài toán
            return f"{feedback} {self._generate_completion_message()}"
    
    def _handle_incorrect_answer(self, evaluation):
        """
        Xử lý khi học sinh trả lời sai
        
        Args:
            evaluation (dict): Kết quả đánh giá
            
        Returns:
            str: Phản hồi hỗ trợ
        """
        feedback = evaluation.get("feedback", "Câu trả lời chưa chính xác.")
        suggestion = evaluation.get("suggestion", "Hãy thử lại.")

        improved_suggestion = self._humanize_suggestion(suggestion)
        
        return f"{feedback} {improved_suggestion}"
    
    def _humanize_suggestion(self, suggestion):
        
        llm = LLMInterface()

        """Làm mềm mại gợi ý bằng LLM"""
        prompt = f"""
        Bạn là một giáo viên toán học tận tâm và yêu thương học sinh. 
        Hãy biến gợi ý khô khan này thành lời khuyên ấm áp, khích lệ:
        
        "{suggestion}"
        
        Quy tắc:
        - Giữ nguyên nội dung kiến thức nhưng làm giọng điệu mềm mại hơn
        - Thêm từ ngữ động viên, khích lệ
        - Ngắn gọn nhưng thân thiện
        - Có thể thêm 1 emoji phù hợp
        
        Chỉ trả về lời khuyên đã cải thiện, không thêm giải thích.
        """
        
        try:
            # Sử dụng model nhỏ để tiết kiệm
            model_config = {"model_name": "gemini-2.0-flash", "temperature": 0.7}
            improved = llm.generate_content(prompt, model_config, with_system_prompt=False)
            return improved.strip()
        except:
            # Fallback nếu có lỗi
            return suggestion
    
    def _is_deadlocked(self):
        """
        Kiểm tra xem học sinh có bị bế tắc không
        
        Returns:
            bool: True nếu học sinh bị bế tắc
        """
        # Bế tắc nếu thử nhiều lần hoặc nói "không biết"
        return (self.attempts_on_current_step >= 3 or 
                any(["không biết" in msg["content"].lower() 
                     for msg in self.conversation_history[-3:] 
                     if msg["role"] == "user"]))
    
    def _handle_deadlock(self, current_step):
        """
        Xử lý khi học sinh bị bế tắc
        
        Args:
            current_step (dict): Thông tin bước hiện tại
            
        Returns:
            str: Giải thích chi tiết
        """
        return self.deadlock_explainer.explain(
            current_step,
            self.conversation_history
        )
    
    def _generate_completion_message(self):
        """
        Tạo thông báo hoàn thành bài toán
        
        Returns:
            str: Thông báo hoàn thành
        """
        final_answer = self.solution.get("final_answer", "")
        
        return (
            f"Chúc mừng! Bạn đã hoàn thành bài toán. "
            f"Đáp án cuối cùng là: {final_answer}. "
            f"Bây giờ bạn có thể bắt đầu một bài toán mới hoặc xem phân tích lỗ hổng kiến thức."
        )
    
    def is_completed(self):
        """
        Kiểm tra xem bài toán đã được giải xong chưa
        
        Returns:
            bool: True nếu đã hoàn thành tất cả các bước
        """
        return self.current_step_id > len(self.solution["steps"])
    
    def get_knowledge_gaps(self):
        """
        Lấy thông tin về lỗ hổng kiến thức từ lịch sử hội thoại
        
        Returns:
            list: Danh sách các lỗ hổng kiến thức
        """
        # Thu thập các lỗ hổng kiến thức từ lịch sử đánh giá
        knowledge_gaps = []
        
        for msg in self.conversation_history:
            if msg["role"] == "assistant" and "knowledge_gap" in msg.get("content", ""):
                try:
                    # Thử trích xuất lỗ hổng kiến thức từ tin nhắn
                    evaluation = json.loads(msg["content"])
                    if "knowledge_gap" in evaluation and evaluation["knowledge_gap"] != "Không xác định được":
                        knowledge_gaps.append(evaluation["knowledge_gap"])
                except:
                    pass
        
        # Loại bỏ các lỗ hổng trùng lặp
        unique_gaps = list(set(knowledge_gaps))
        
        # Nếu không tìm thấy lỗ hổng cụ thể, tạo danh sách từ các kiến thức cần thiết
        if not unique_gaps:
            all_knowledge = []
            for step in self.solution["steps"]:
                all_knowledge.extend(step.get("knowledge_needed", []))
            
            unique_gaps = list(set(all_knowledge))
        
        return unique_gaps