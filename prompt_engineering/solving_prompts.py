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

# Prompt giải toán chi tiết theo các bước
DETAILED_SOLVING_PROMPT = """
Với tư cách là một chuyên gia toán học và gia sư hàng đầu, hãy giải chi tiết bài toán sau đây cho học sinh lớp 9, tuân thủ nghiêm ngặt các yêu cầu dưới đây:

Đề bài: {problem_text}

### YÊU CẦU BẮT BUỘC:

1. ĐỘ CHÍNH XÁC TUYỆT ĐỐI:
   - Đáp số cuối cùng PHẢI chính xác 100%
   - Tất cả các bước tính toán phải được kiểm tra kỹ lưỡng
   - Nếu có nhiều cách giải, hãy chọn cách chính xác và phù hợp nhất với trình độ học sinh lớp 9

2. CẤU TRÚC LỜI GIẢI:
   - Phân tích đề bài: Xác định dữ kiện, yêu cầu, và mối quan hệ toán học
   - Lập kế hoạch giải: Nêu rõ phương pháp sẽ sử dụng
   - Chia thành các bước nhỏ, mỗi bước có MỤC TIÊU rõ ràng
   - Mỗi bước phải nêu rõ: (a) Mục tiêu, (b) Dữ liệu đầu vào, (c) Phép tính/biến đổi, (d) Kết quả, (e) Lý do/logic của bước này

3. KẾT CẤU TỪNG BƯỚC:
   - Mỗi bước phải CÓ CHỦ ĐÍCH cụ thể (tìm biến trung gian, áp dụng công thức, biến đổi biểu thức...)
   - Mỗi bước phải có số thứ tự rõ ràng (Bước 1, Bước 2...)
   - Mỗi bước phải xác định rõ kiến thức toán học cần áp dụng
   - Mỗi phép biến đổi phải có giải thích chi tiết

4. NGÔN NGỮ VÀ TRÌNH BÀY:
   - Sử dụng ngôn ngữ đơn giản, dễ hiểu với học sinh lớp 9
   - Diễn đạt mạch lạc, chính xác về mặt toán học
   - Đặt tên biến, hằng số một cách hợp lý và nhất quán
   - Sử dụng cách diễn đạt toán học chuẩn mực (ví dụ: "Áp dụng định lý Pytago", không chỉ "Dùng Pytago")

5. KIỂM TRA VÀ TỔNG KẾT:
   - Kiểm tra lại đáp án cuối cùng
   - Tóm tắt các bước quan trọng đã thực hiện
   - Nêu rõ kiến thức toán học quan trọng đã áp dụng

6. BỎ QUA PHẦN GIỚI THIỆU VÀ KẾT LUẬN DÀI DÒNG:
   - Không cần lời mở đầu hay kết luận dài dòng
   - Tập trung vào nội dung lời giải

LƯU Ý ĐẶC BIỆT: Hãy giải bài toán với tâm thế rằng lời giải của bạn sẽ là nguồn tham khảo chuẩn mực cho giáo viên và học sinh. Đảm bảo rằng LỜI GIẢI PHẢI ĐÚNG 100%, LOGIC RÕ RÀNG, và TRÌNH BÀY CHẶT CHẼ.
"""

# Prompt để định dạng lời giải thành JSON có cấu trúc
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