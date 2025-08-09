from core.tier2_solver.solvers.base_solver import BaseSolver
from llm.llm_interface import LLMInterface
from core.tier2_solver.solution_formatter import format_solution
import uuid

class GeneralSolver(BaseSolver):
    """
    Solver tổng quát cho mọi dạng bài toán
    """
    
    def __init__(self, model_config, thinking_budget, solving_prompt=None):
        super().__init__(model_config, thinking_budget)
        self.solving_prompt = solving_prompt
    
    def solve(self, problem_text):
        """
        Giải bài toán sử dụng LLM với quy trình 2 giai đoạn
        """
        # GIAI ĐOẠN 1: Giải bài toán và nhận kết quả dạng text
        llm = LLMInterface()
        
        # Sử dụng prompt đã được cung cấp hoặc prompt mặc định
        from prompt_engineering.solving_prompts import DETAILED_SOLVING_PROMPT_MEDIUM
        prompt_template = self.solving_prompt if self.solving_prompt else DETAILED_SOLVING_PROMPT_MEDIUM
        prompt = prompt_template.format(problem_text=problem_text)
        
        # Điều chỉnh config cho model giải toán
        model_config = dict(self.model_config)
        
        try:
            # Gọi API để giải bài toán
            solution_text = llm.generate_content(prompt, model_config, with_system_prompt=False)
        except Exception as e:
            print(f"Lỗi khi giải bài toán: {str(e)}")
            return self._create_error_solution(str(e))
        
        # GIAI ĐOẠN 2: Format lời giải thành JSON
        try:
            formatted_solution = format_solution(solution_text)
            
            # Thêm đề bài vào solution JSON
            formatted_solution["problem_text"] = problem_text
            
            return formatted_solution
        except Exception as e:
            print(f"Lỗi khi format lời giải: {str(e)}")
            return self._create_fallback_solution(solution_text, str(e))
        
    def _get_token_limit(self):
        """Trả về token limit phù hợp với budget"""
        limits = {
            "low": 3096, "medium": 7152, 
            "high": 10000, "very_high": 10000
        }
        return limits.get(self.thinking_budget, 2048)

    def _create_error_solution(self, error_msg):
        """Tạo JSON giải pháp dự phòng khi giải thất bại"""
        return {
            "problem_id": str(uuid.uuid4()),
            "final_answer": "Không thể giải bài toán này",
            "steps": [
                {
                    "step_id": 1,
                    "goal": "Thông báo lỗi",
                    "knowledge_needed": ["N/A"],
                    "input_data": {},
                    "calculation": f"Lỗi: {error_msg}",
                    "expected_result": "",
                    "explanation_logic": "Vui lòng thử lại với bài toán khác."
                }
            ]
        }

    def _create_fallback_solution(self, solution_text, error_msg):
        """Tạo JSON giải pháp dự phòng khi formatting thất bại"""
        return {
            "problem_id": str(uuid.uuid4()),
            "final_answer": "Xem lời giải đầy đủ bên dưới",
            "steps": [
                {
                    "step_id": 1,
                    "goal": "Lời giải đầy đủ",
                    "knowledge_needed": ["Kiến thức toán học cơ bản"],
                    "input_data": {},
                    "calculation": solution_text,
                    "expected_result": "",
                    "explanation_logic": f"Lỗi khi format: {error_msg}"
                }
            ]
        }