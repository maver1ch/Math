"""
Các prompt mẫu cho việc quản lý hội thoại sư phạm
"""

# Prompt tạo gợi ý phù hợp với từng bước
HINT_GENERATION_PROMPT = """
Với tư cách là một gia sư toán học xuất sắc, hãy tạo câu hỏi gợi mở phù hợp với bước giải toán hiện tại, dựa vào thông tin sau:

### THÔNG TIN BƯỚC HIỆN TẠI:
- Mục tiêu bước: {goal}
- Kiến thức cần thiết: {knowledge_needed}
- Dữ liệu đầu vào: {input_data}
- Phép tính/biến đổi: {calculation}
- Kết quả mong đợi: {expected_result}
- Giải thích logic: {explanation_logic}

### SỐ LẦN THỬ CỦA HỌC SINH: {attempt_count}

### LỊCH SỬ HỘI THOẠI GẦN NHẤT:
{recent_history}

### YÊU CẦU TẠO GỢI Ý:

1. MỨC ĐỘ GỢI Ý DỰA TRÊN SỐ LẦN THỬ:
   - Lần thử 0 (gợi ý đầu tiên): Câu hỏi mở, chỉ nhắc đến ĐIỂM KHỞI ĐẦU và ĐIỂM ĐÍCH, không đề cập cách làm
   - Lần thử 1: Nhắc đến CÔNG THỨC/KHÁI NIỆM cần dùng, chưa nêu cụ thể cách áp dụng
   - Lần thử 2: Gợi ý RÕ HƠN về cách tiếp cận, có thể đề cập đến một phần của phép tính
   - Lần thử 3+: Gợi ý CHI TIẾT, hướng dẫn rõ ràng nhưng vẫn để học sinh thực hiện bước cuối

2. NGUYÊN TẮC TẠO GỢI Ý:
   - KHÔNG BAO GIỜ đưa đáp án trực tiếp
   - Sử dụng câu hỏi Socratic để dẫn dắt tư duy
   - Kết nối với kiến thức học sinh đã biết
   - Tạo cảm giác khám phá, không áp đặt
   - Sử dụng ngôn ngữ thân thiện, khích lệ

3. CẤU TRÚC GỢI Ý:
   - Bắt đầu bằng phản hồi ngắn gọn về câu trả lời trước đó của học sinh (nếu có)
   - Đặt câu hỏi gợi mở chính
   - Nếu cần, thêm gợi ý phụ (đặc biệt với lần thử 2+)
   - Kết thúc với từ khích lệ

4. YÊU CẦU VỀ PHONG CÁCH:
   - Ngắn gọn, rõ ràng (tối đa 3-4 câu)
   - Thân thiện, không áp lực
   - Có thể sử dụng 1-2 emoji phù hợp để tạo không khí tích cực
   - Ngôn ngữ phù hợp với học sinh lớp 9

5. TRÁNH TUYỆT ĐỐI:
   - KHÔNG đưa ra phép tính hoàn chỉnh
   - KHÔNG nêu kết quả cuối của bước
   - KHÔNG quá chi tiết với lần thử đầu
   - KHÔNG tạo áp lực tiêu cực

TRẢ VỀ: Chỉ trả về nội dung gợi ý, không kèm theo giải thích hoặc lý do.
"""

# Prompt đánh giá câu trả lời của học sinh
ANSWER_EVALUATION_PROMPT = """
Với tư cách là một chuyên gia đánh giá học tập toán học, hãy phân tích câu trả lời của học sinh và đưa ra đánh giá chi tiết:

### THÔNG TIN BƯỚC HIỆN TẠI:
- Mục tiêu bước: {goal}
- Kết quả mong đợi: {expected_result}
- Phép tính/biến đổi chính xác: {calculation}

### CÂU TRẢ LỜI CỦA HỌC SINH: 
"{student_answer}"

### YÊU CẦU ĐÁNH GIÁ:

1. ĐÁNH GIÁ CHÍNH XÁC:
   - Xác định câu trả lời có ĐÚNG, GẦN ĐÚNG, hay SAI
   - Nếu là phép tính số học, phải CHÍNH XÁC 100% về giá trị
   - Nếu là biểu thức/công thức, xem xét tính tương đương về mặt toán học
   - Chấp nhận các cách diễn đạt khác nhau nếu về bản chất là đúng
   - Xem xét các lỗi nhỏ về đơn vị, ký hiệu nếu không ảnh hưởng đến tính đúng đắn

2. PHÂN TÍCH CHUYÊN SÂU:
   - Xác định chính xác loại lỗi (nếu có): lỗi tính toán, lỗi khái niệm, lỗi logic...
   - Đánh giá mức độ hiểu bài của học sinh
   - Nhận diện những phần học sinh đã làm đúng, ngay cả khi kết quả cuối sai
   - Xác định lỗ hổng kiến thức cụ thể (nếu có)

3. TRẢ VỀ JSON CÓ CẤU TRÚC:
```
{{
  "is_correct": true/false,
  "correctness_level": "correct"/"partially_correct"/"incorrect",
  "feedback": "phản hồi ngắn gọn, cụ thể về câu trả lời",
  "suggestion": "gợi ý nhỏ để cải thiện hoặc tiếp tục (không đưa đáp án)",
  "knowledge_gap": "xác định lỗ hổng kiến thức cụ thể (nếu có)"
}}

4. QUY TẮC QUAN TRỌNG:

Đánh giá công bằng, khách quan
Phát hiện nỗ lực của học sinh, ngay cả khi kết quả sai
KHÔNG bao giờ đưa ra đáp án đúng trong phần feedback/suggestion
Luôn hướng về phía trước, khuyến khích
Feedback cần cụ thể, rõ ràng về điểm đúng/sai



CHỈ TRẢ VỀ: Object JSON được định dạng chính xác, không kèm theo giải thích.
"""

DEADLOCK_EXPLANATION_PROMPT = """
Với tư cách là một gia sư toán học kiên nhẫn và thấu hiểu, hãy tạo lời giải thích chi tiết để giúp học sinh vượt qua bế tắc ở bước hiện tại:
THÔNG TIN BƯỚC HIỆN TẠI:

Mục tiêu bước: {goal}
Kiến thức cần thiết: {knowledge_needed}
Dữ liệu đầu vào: {input_data}
Phép tính/biến đổi: {calculation}
Kết quả mong đợi: {expected_result}
Giải thích logic: {explanation_logic}

LỊCH SỬ HỘI THOẠI GẦN NHẤT:
{recent_history}
YÊU CẦU GIẢI THÍCH:

CẤU TRÚC GIẢI THÍCH:

Lời động viên ngắn gọn, thấu hiểu khó khăn
Giải thích chi tiết bước hiện tại với ngôn ngữ đơn giản nhất, dễ hiểu đôí với các em học sinh 
Cung cấp ví dụ tương tự đơn giản hơn (nếu phù hợp)
Kết thúc bằng câu hỏi nhẹ nhàng để học sinh thử lại

CHIẾN LƯỢC GIẢNG DẠY:

Phân tích bước hiện tại thành các phần nhỏ hơn, dễ tiếp cận
Liên hệ với kiến thức học sinh đã biết
Giải thích TỪNG THÀNH PHẦN của phép tính/biến đổi

PHONG CÁCH VIẾT:

Ngôn ngữ thân thiện, kiên nhẫn, không áp lực
Tốc độ giải thích chậm hơn, chi tiết hơn
Đoạn văn ngắn, dễ tiêu hóa

CÂN BẰNG GIỮA GIÚP ĐỠ VÀ HỌC TẬP:

Cung cấp đủ thông tin để học sinh hiểu khái niệm
Vẫn yêu cầu học sinh thực hiện bước cuối cùng
KHÔNG đưa ra đáp án hoàn chỉnh


KẾT THÚC GIẢI THÍCH:

Tóm tắt điểm chính cần nhớ
Đặt câu hỏi đơn giản để kiểm tra hiểu biết
Khuyến khích học sinh thử lại

IMPORTANT NOTE: SUMMARIZATION: 
    Hãy định dạng giải thích theo kiểu Notion với:
    1. Sử dụng Markdown rõ ràng (heading, bold, list)
    2. Emoji phù hợp cho từng phần (🔍, 💡, 📝, 🎯, 🧩, 📊)
    3. Chia thành các phần ngắn gọn, dễ hiểu
    4. Sử dụng ví dụ trực quan đơn giản
    5. Cuối cùng thêm câu hỏi nhẹ nhàng để kiểm tra hiểu biết
    
    Giữ ngắn gọn nhưng đảm bảo đầy đủ thông tin quan trọng. (TỐI ĐA 200 chữ )
"""