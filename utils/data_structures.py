"""
Định nghĩa các cấu trúc dữ liệu cho dự án Math Mentor AI
"""

class MathProblem:
    """Lớp đại diện cho một bài toán"""
    
    def __init__(self, problem_text, problem_id=None):
        """
        Khởi tạo đối tượng bài toán
        
        Args:
            problem_text (str): Nội dung đề bài
            problem_id (str, optional): ID của bài toán
        """
        self.problem_text = problem_text
        self.problem_id = problem_id
        self.problem_type = None  # loại bài toán (algebra, geometry, word_problem, ...)
        self.difficulty = None    # độ khó (1-10)
        self.solution_json = None # lời giải dạng JSON
    
    def __str__(self):
        return f"Bài toán: {self.problem_text[:50]}..."
    
    def set_classification(self, problem_type, difficulty):
        """
        Đặt phân loại cho bài toán
        
        Args:
            problem_type (str): Loại bài toán
            difficulty (int): Độ khó (1-10)
        """
        self.problem_type = problem_type
        self.difficulty = difficulty
    
    def set_solution(self, solution_json):
        """
        Đặt lời giải cho bài toán
        
        Args:
            solution_json (dict): Lời giải dạng JSON
        """
        self.solution_json = solution_json
    
    def to_dict(self):
        """
        Chuyển đổi đối tượng bài toán thành dictionary
        
        Returns:
            dict: Dictionary đại diện cho bài toán
        """
        return {
            "problem_id": self.problem_id,
            "problem_text": self.problem_text,
            "problem_type": self.problem_type,
            "difficulty": self.difficulty,
            "solution_json": self.solution_json
        }