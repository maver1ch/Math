from abc import ABC, abstractmethod

class BaseSolver(ABC):
    """
    Lớp cơ sở trừu tượng cho các solver
    """
    
    def __init__(self, model_config, thinking_budget):
        """
        Khởi tạo solver
        
        Args:
            model_config (dict): Cấu hình model LLM
            thinking_budget (str): Mức độ suy nghĩ ("low", "medium", "high", "very_high")
        """
        self.model_config = model_config
        self.thinking_budget = thinking_budget
    
    @abstractmethod
    def solve(self, problem_text):
        """
        Giải bài toán
        
        Args:
            problem_text (str): Đề bài toán
            
        Returns:
            dict: Lời giải dạng JSON có cấu trúc
        """
        pass