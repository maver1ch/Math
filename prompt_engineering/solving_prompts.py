"""
Các prompt mẫu chi tiết cho việc giải toán
"""

# Prompt phân loại độ khó của bài toán
DIFFICULTY_CLASSIFICATION_PROMPT = """
Với tư cách là một chuyên gia toán học và giáo dục, hãy phân tích đề bài toán sau đây và đánh giá độ khó của nó trên thang điểm từ 1-10.

Đề bài: {problem_text}

Thang đánh giá chi tiết:
1: Rất dễ - Yêu cầu hiểu biết kiến thức cơ bản nhất, giải được trong 1 bước đơn giản, không cần biến đổi phức tạp.
2-3: Dễ - Áp dụng trực tiếp công thức đã học, cần 1-2 bước biến đổi đơn giản, kiến thức phổ thông.
4-5: Trung bình dễ - Kết hợp 2-3 khái niệm, cần 3-4 bước giải, đòi hỏi suy luận logic cơ bản.
6-7: Trung bình khó - Yêu cầu phân tích sâu, cần nhiều bước giải (4-6 bước), đòi hỏi kết hợp nhiều kiến thức.
8: Khó - Bài toán phức tạp, nhiều bước giải (6-8 bước), đòi hỏi tư duy linh hoạt và sáng tạo.
9-10: Rất khó - Bài toán mang tính thử thách cao, yêu cầu hiểu biết sâu rộng, nhiều bước giải phức tạp, cần kỹ năng suy luận và tư duy toán học xuất sắc.

Các yếu tố cần xem xét:
- Số lượng kiến thức, công thức, định lý cần áp dụng
- Số lượng bước cần thực hiện để giải bài
- Mức độ phức tạp của phép biến đổi và tính toán
- Tính sáng tạo và linh hoạt trong cách tiếp cận

Lưu ý:
1. Đánh giá độ khó tương đối với học sinh lớp 9
2. Bỏ qua yếu tố quen thuộc (giả định học sinh chưa gặp dạng bài này trước đây)

QUAN TRỌNG: Chỉ trả về một số nguyên từ 1-10 đại diện cho độ khó, KHÔNG kèm theo bất kỳ giải thích nào.
"""

# Prompt giải toán chi tiết theo các bước - BÀI DỄ (tối đa 4 bước)
DETAILED_SOLVING_PROMPT_EASY = """
Với tư cách là một chuyên gia toán học và gia sư hàng đầu, hãy giải chi tiết bài toán sau đây cho học sinh lớp 9, tuân thủ nghiêm ngặt các yêu cầu dưới đây:

Đề bài: {problem_text}

### YÊU CẦU BẮT BUỘC:

1. ĐỘ CHÍNH XÁC TUYỆT ĐỐI:
   - Đáp số cuối cùng PHẢI chính xác 100%
   - Tất cả các bước tính toán phải được kiểm tra kỹ lưỡng
   - Nếu có nhiều cách giải, hãy chọn cách phù hợp nhất với trình độ học sinh lớp 9

2. GIỚI HẠN 3-4 BƯỚC GIẢI:
   - Chia bài toán thành TỐI ĐA 4 BƯỚC giải
   - Mỗi bước phải có ý nghĩa riêng, không quá chi tiết
   - Gộp các bước nhỏ liên quan thành một bước lớn hơn
   - Đảm bảo mỗi bước đều cần thiết

3. CẤU TRÚC TỪNG BƯỚC:
   - Mỗi bước phải CÓ CHỦ ĐÍCH cụ thể (tìm biến trung gian, áp dụng công thức, biến đổi biểu thức...)
   - Mỗi bước phải có số thứ tự rõ ràng (Bước 1, Bước 2...)
   - Mỗi bước phải xác định rõ kiến thức toán học cần áp dụng
   - Mỗi phép biến đổi phải có giải thích chi tiết

4. NGÔN NGỮ VÀ TRÌNH BÀY:
   - Sử dụng ngôn ngữ đơn giản, dễ hiểu với học sinh lớp 9
   - Diễn đạt mạch lạc, chính xác về mặt toán học
   - Đặt tên biến, hằng số một cách hợp lý và nhất quán

5. KIỂM TRA VÀ TỔNG KẾT:
   - Kiểm tra lại đáp án cuối cùng
   - Tóm tắt các bước quan trọng đã thực hiện
   - Nêu rõ kiến thức toán học quan trọng đã áp dụng

LƯU Ý ĐẶC BIỆT: 
- Giới hạn TỐI ĐA 4 BƯỚC giải, không nhiều hơn
- Không chia nhỏ thành quá nhiều bước
- Đáp án cuối cùng phải chính xác tuyệt đối
"""

# Prompt giải toán chi tiết theo các bước - BÀI TRUNG BÌNH (tối đa 5 bước)
DETAILED_SOLVING_PROMPT_MEDIUM = """
Với tư cách là một chuyên gia toán học và gia sư hàng đầu, hãy giải chi tiết bài toán sau đây cho học sinh lớp 9, tuân thủ nghiêm ngặt các yêu cầu dưới đây:

Đề bài: {problem_text}

### YÊU CẦU BẮT BUỘC:

1. ĐỘ CHÍNH XÁC TUYỆT ĐỐI:
   - Đáp số cuối cùng PHẢI chính xác 100%
   - Tất cả các bước tính toán phải được kiểm tra kỹ lưỡng
   - Nếu có nhiều cách giải, hãy chọn cách chính xác và phù hợp nhất với trình độ học sinh lớp 9

2. GIỚI HẠN 4-5 BƯỚC GIẢI:
   - Chia bài toán thành TỐI ĐA 5 BƯỚC giải
   - Mỗi bước phải có ý nghĩa riêng, không quá chi tiết
   - Gộp các bước nhỏ liên quan thành một bước lớn hơn
   - Đảm bảo mỗi bước đều cần thiết

3. CẤU TRÚC TỪNG BƯỚC:
   - Mỗi bước phải CÓ CHỦ ĐÍCH cụ thể (tìm biến trung gian, áp dụng công thức, biến đổi biểu thức...)
   - Mỗi bước phải có số thứ tự rõ ràng (Bước 1, Bước 2...)
   - Mỗi bước phải xác định rõ kiến thức toán học cần áp dụng
   - Mỗi phép biến đổi phải có giải thích chi tiết

4. NGÔN NGỮ VÀ TRÌNH BÀY:
   - Sử dụng ngôn ngữ đơn giản, dễ hiểu với học sinh lớp 9
   - Diễn đạt mạch lạc, chính xác về mặt toán học
   - Đặt tên biến, hằng số một cách hợp lý và nhất quán

5. KIỂM TRA VÀ TỔNG KẾT:
   - Kiểm tra lại đáp án cuối cùng
   - Tóm tắt các bước quan trọng đã thực hiện
   - Nêu rõ kiến thức toán học quan trọng đã áp dụng

LƯU Ý ĐẶC BIỆT: 
- Giới hạn TỐI ĐA 5 BƯỚC giải, không nhiều hơn
- Không chia nhỏ thành quá nhiều bước
- Đáp án cuối cùng phải chính xác tuyệt đối
"""

# Prompt giải toán chi tiết theo các bước - BÀI KHÓ (tối đa 7 bước)
DETAILED_SOLVING_PROMPT_HARD = """
Với tư cách là một chuyên gia toán học và gia sư hàng đầu, hãy giải chi tiết bài toán sau đây cho học sinh lớp 9, tuân thủ nghiêm ngặt các yêu cầu dưới đây:

Đề bài: {problem_text}

### YÊU CẦU BẮT BUỘC:

1. ĐỘ CHÍNH XÁC TUYỆT ĐỐI:
   - Đáp số cuối cùng PHẢI chính xác 100%
   - Tất cả các bước tính toán phải được kiểm tra kỹ lưỡng
   - Nếu có nhiều cách giải, hãy chọn cách chính xác và phù hợp nhất với trình độ học sinh lớp 9

2. GIỚI HẠN 5-7 BƯỚC GIẢI:
   - Chia bài toán thành TỐI ĐA 7 BƯỚC giải
   - Mỗi bước phải có ý nghĩa riêng, không quá chi tiết
   - Gộp các bước nhỏ liên quan thành một bước lớn hơn
   - Đảm bảo mỗi bước đều cần thiết

3. CẤU TRÚC TỪNG BƯỚC:
   - Mỗi bước phải CÓ CHỦ ĐÍCH cụ thể (tìm biến trung gian, áp dụng công thức, biến đổi biểu thức...)
   - Mỗi bước phải có số thứ tự rõ ràng (Bước 1, Bước 2...)
   - Mỗi bước phải xác định rõ kiến thức toán học cần áp dụng
   - Mỗi phép biến đổi phải có giải thích chi tiết

4. NGÔN NGỮ VÀ TRÌNH BÀY:
   - Sử dụng ngôn ngữ đơn giản, dễ hiểu với học sinh lớp 9
   - Diễn đạt mạch lạc, chính xác về mặt toán học
   - Đặt tên biến, hằng số một cách hợp lý và nhất quán

5. KIỂM TRA VÀ TỔNG KẾT:
   - Kiểm tra lại đáp án cuối cùng
   - Tóm tắt các bước quan trọng đã thực hiện
   - Nêu rõ kiến thức toán học quan trọng đã áp dụng

LƯU Ý ĐẶC BIỆT: 
- Giới hạn TỐI ĐA 7 BƯỚC giải, không nhiều hơn
- Không chia nhỏ thành quá nhiều bước
- Đáp án cuối cùng phải chính xác tuyệt đối
"""

# Lựa chọn prompt theo độ khó
def get_solving_prompt(difficulty):
    if difficulty <= 6: 
        return DETAILED_SOLVING_PROMPT_EASY
    elif difficulty <= 8: 
        return DETAILED_SOLVING_PROMPT_MEDIUM
    else:  # Khó
        return DETAILED_SOLVING_PROMPT_HARD

SOLUTION_FORMATTING_PROMPT = """
Hãy chuyển đổi lời giải toán học sau đây thành định dạng JSON có cấu trúc theo đúng yêu cầu kỹ thuật dưới đây:

Lời giải: {solution_text}

### YÊU CẦU KỸ THUẬT:

Tạo JSON có cấu trúc chính xác như sau:
```json
{{
    "problem_id": "unique_id_string",
    "final_answer": "đáp án cuối cùng dạng text",
    "steps": [
        {{
            "step_id": 1,
            "goal": "mục tiêu cụ thể của bước này",
            "knowledge_needed": ["kiến thức 1", "kiến thức 2", ...],
            "input_data": {{"tên_biến_1": "giá_trị_1", "tên_biến_2": "giá_trị_2", ...}},
            "calculation": "phép tính hoặc phép biến đổi chi tiết",
            "expected_result": "kết quả mong đợi của bước này",
            "explanation_logic": "giải thích chi tiết logic của bước này"
        }},
        ...thêm các bước khác với cấu trúc tương tự
    ]
}}
"""