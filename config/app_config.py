# Cấu hình ứng dụng

# Thông tin cơ bản
APP_TITLE = "Math Mentor AI - Gia sư Toán học AI"
APP_DESCRIPTION = """
**Math Mentor AI** là chatbot hỏi-đáp toán học theo chương trình Việt Nam.

Thay vì chỉ cung cấp đáp án, chatbot sẽ hướng dẫn bạn từng bước 
để giúp bạn hiểu sâu hơn về cách giải quyết bài toán.

Hiện tại hỗ trợ: Toán học lớp 9
"""

# Cấu hình Chatbot
MAX_HISTORY_LENGTH = 50  # Số lượng tin nhắn tối đa lưu trong lịch sử
SUPPORTED_FORMATS = ["png", "jpg", "jpeg"]  # Định dạng ảnh hỗ trợ

# Cấu hình dạng toán học hỗ trợ
SUPPORTED_MATH_TYPES = [
    "algebra",      # Đại số
    "geometry",     # Hình học
    "word_problem", # Toán có lời văn
    "calculus",     # Giải tích
    "probability"   # Xác suất
]

# Cấu hình độ khó
DIFFICULTY_LEVELS = {
    "easy": (1, 3),     # Dễ: 1-3
    "medium": (4, 7),   # Trung bình: 4-7
    "hard": (8, 10)     # Khó: 8-10
}