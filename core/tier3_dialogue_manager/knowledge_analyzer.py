"""
Module phân tích lỗ hổng kiến thức từ lịch sử hội thoại
"""
import json
from llm.llm_interface import LLMInterface
from config.llm_config import MODELS

class KnowledgeAnalyzer:
    """
    Phân tích lỗ hổng kiến thức của học sinh
    """
    
    def __init__(self):
        """
        Khởi tạo analyzer
        """
        self.llm = LLMInterface()
        self.model_config = MODELS["medium_solver"]
    
    def analyze(self, solution, conversation_history):
        """
        Phân tích lỗ hổng kiến thức từ lịch sử hội thoại
        
        Args:
            solution (dict): Lời giải dạng JSON có cấu trúc
            conversation_history (list): Lịch sử hội thoại
            
        Returns:
            dict: Kết quả phân tích lỗ hổng kiến thức
        """
        # Chuẩn bị prompt
        prompt = self._prepare_prompt(solution, conversation_history)
        
        # Gọi API để phân tích
        response = self.llm.generate_content(prompt, self.model_config)
        
        # Xử lý kết quả
        try:
            # Chuyển đổi response thành JSON
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError as e:
            print(f"Lỗi khi phân tích JSON: {str(e)}")
            print(f"Response: {response}")
            
            # Tạo kết quả mặc định nếu không thể phân tích JSON
            return self._create_default_analysis(solution)
    
    def _prepare_prompt(self, solution, conversation_history):
        """
        Chuẩn bị prompt để phân tích lỗ hổng kiến thức
        
        Args:
            solution (dict): Lời giải dạng JSON có cấu trúc
            conversation_history (list): Lịch sử hội thoại
            
        Returns:
            str: Prompt phân tích
        """
        # Chuyển đổi lịch sử hội thoại thành text
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        # Trích xuất kiến thức cần thiết từ lời giải
        all_knowledge = []
        for step in solution["steps"]:
            all_knowledge.extend(step.get("knowledge_needed", []))
        unique_knowledge = list(set(all_knowledge))
        
        # Tạo prompt
        prompt = f"""
        Với tư cách là một chuyên gia phân tích giáo dục toán học, hãy phân tích lịch sử hội thoại sau đây giữa chatbot (assistant) và học sinh (user) để xác định lỗ hổng kiến thức của học sinh và đưa ra đề xuất ôn tập.

        ### THÔNG TIN BÀI TOÁN:
        - Đề bài: {solution.get('problem_text', 'Không có đề bài')}
        - Đáp án cuối cùng: {solution.get('final_answer', 'Không có đáp án')}
        
        ### CÁC KIẾN THỨC CẦN THIẾT:
        {", ".join(unique_knowledge)}

        ### LỊCH SỬ HỘI THOẠI:
        {history_text}

        ### HƯỚNG DẪN PHÂN TÍCH CHI TIẾT:

        1. PHÂN TÍCH LỖ HỔNG KIẾN THỨC:
        - Xác định những khái niệm/kiến thức học sinh gặp khó khăn
        - Phân tích mức độ hiểu của học sinh với từng khái niệm (dựa trên số lần thử và chất lượng câu trả lời)
        - Chú ý đến các câu trả lời sai hoặc "không biết" - đây là dấu hiệu của lỗ hổng kiến thức
        - Tìm kiếm các mẫu lỗi lặp đi lặp lại trong câu trả lời của học sinh

        2. XÁC ĐỊNH ĐIỂM MẠNH:
        - Nhận diện những khái niệm/kiến thức học sinh thể hiện sự hiểu biết tốt
        - Tìm bằng chứng cụ thể từ hội thoại cho thấy học sinh nắm vững kiến thức
        - Đánh giá khả năng tư duy logic và vận dụng kiến thức của học sinh

        3. ĐỀ XUẤT KIẾN THỨC CẦN ÔN TẬP:
        - Ưu tiên các lỗ hổng kiến thức nghiêm trọng nhất
        - Đề xuất tài nguyên học tập phù hợp (video, sách, bài tập)
        - Cung cấp mô tả ngắn gọn về nội dung cần ôn tập
        - Gợi ý phương pháp học tập hiệu quả

        4. ĐÁNH GIÁ TỔNG QUÁT:
        - Tóm tắt ngắn gọn về mức độ hiểu bài toán của học sinh
        - Nhận xét về tiềm năng và hướng phát triển
        - Đưa ra lời khuyên tổng quát cho việc học tập

        ### TRẢ VỀ KẾT QUẢ PHÂN TÍCH DƯỚI DẠNG JSON:
        ```json
        {{
        "knowledge_gaps": [
            {{
            "concept": "Tên khái niệm/kiến thức",
            "confidence_level": "low/medium/high",
            "explanation": "Giải thích ngắn gọn về lỗ hổng",
            "examples": ["Ví dụ 1", "Ví dụ 2"]
            }}
        ],
        "strengths": [
            {{
            "concept": "Tên khái niệm/kiến thức",
            "evidence": "Bằng chứng từ hội thoại"
            }}
        ],
        "study_recommendations": [
            {{
            "topic": "Chủ đề cần ôn tập",
            "resource_type": "video/book/exercise",
            "description": "Mô tả ngắn gọn"
            }}
        ],
        "overall_assessment": "Đánh giá tổng quát ngắn gọn"
        }}
        ```

        QUAN TRỌNG: Chỉ trả về object JSON hợp lệ, không kèm theo bất kỳ giải thích hay văn bản nào khác.
        """
        
        return prompt
    
    def _create_default_analysis(self, solution):
        """
        Tạo kết quả phân tích mặc định
        
        Args:
            solution (dict): Lời giải dạng JSON có cấu trúc
            
        Returns:
            dict: Kết quả phân tích mặc định
        """
        # Trích xuất kiến thức cần thiết từ lời giải
        all_knowledge = []
        for step in solution["steps"]:
            all_knowledge.extend(step.get("knowledge_needed", []))
        unique_knowledge = list(set(all_knowledge))
        
        # Tạo kết quả mặc định
        knowledge_gaps = []
        for i, knowledge in enumerate(unique_knowledge):
            knowledge_gaps.append({
                "concept": knowledge,
                "confidence_level": "medium",
                "explanation": f"Kiến thức cần thiết cho bài toán này.",
                "examples": [f"Xem lại các ví dụ trong SGK về {knowledge}"]
            })
        
        return {
            "knowledge_gaps": knowledge_gaps,
            "strengths": [],
            "study_recommendations": [
                {
                    "topic": "Ôn tập tổng hợp",
                    "resource_type": "book",
                    "description": "Sách giáo khoa và bài tập toán lớp 9"
                }
            ],
            "overall_assessment": "Cần ôn tập lại các kiến thức cơ bản đã học."
        }