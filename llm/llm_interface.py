import google.generativeai as genai
from config.llm_config import API_KEY, SYSTEM_PROMPT
from PIL import Image
import io
import time
from app.utils.llm_logger import LLMLogger

class LLMInterface:
    def __init__(self):
        genai.configure(api_key=API_KEY)
        self.logger = LLMLogger()
    
    def generate_content(self, prompt, model_config, with_system_prompt=True):
        """        
        Args:
            prompt (str): Prompt đầu vào
            model_config (dict): Cấu hình model
            with_system_prompt (bool): Có sử dụng system prompt hay không
            
        Returns:
            str: Nội dung được sinh bởi model
        """
        try:                       
            model_name = model_config.get("model_name", "gemini-1.5-flash")
            temperature = model_config.get("temperature", 0.1)
            top_p = model_config.get("top_p", 0.95)
            top_k = model_config.get("top_k", 20)

            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            }
            
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )

            # Ghi log bắt đầu xử lý
            self.logger.log_step("start_generate_content", {
                "model": model_name,
                "with_system_prompt": with_system_prompt
            })
            
            # Đo thời gian xử lý
            start_time = time.time()

            if with_system_prompt:
                response = model.generate_content(
                    [
                        {"role": "user", "parts": [SYSTEM_PROMPT]},
                        {"role": "model", "parts": ["Tôi đã hiểu vai trò của mình. Tôi sẽ tuân thủ các hướng dẫn."]},
                        {"role": "user", "parts": [prompt]}
                    ]
                )
            else:
                response = model.generate_content(prompt)
            
            # Tính thời gian xử lý
            execution_time = time.time() - start_time
            
            # Ghi log kết quả
            self.logger.log_llm_interaction(
                prompt=prompt,
                response=response.text,
                model_name=model_name,
                execution_time=execution_time,
                metadata={
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "with_system_prompt": with_system_prompt
                }
            )
            
            return response.text
            
        except Exception as e:
            error_message = f"Lỗi khi gọi API Gemini: {str(e)}"
            self.logger.log_error(error_message, {
                "model": model_config.get("model_name", "gemini-1.5-flash"),
                "prompt": prompt[:500] + "..." if len(prompt) > 500 else prompt
            })
            return f"Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn: {str(e)}"
    
    def process_image(self, image_file, prompt=None, model_config=None):
        """
        Xử lý ảnh bằng model Gemini
        
        Args:
            image_file: File ảnh đầu vào
            prompt (str, optional): Prompt đi kèm với ảnh
            model_config (dict, optional): Cấu hình model
            
        Returns:
            str: Kết quả xử lý ảnh
        """
        try:
            # Sử dụng cấu hình mặc định cho OCR nếu không được cung cấp
            if model_config is None:
                from config.llm_config import MODELS
                model_config = MODELS["ocr"]
            
            # Lấy thông tin cấu hình
            model_name = model_config.get("model_name")
            temperature = model_config.get("temperature", 0.1)
            top_p = model_config.get("top_p", 0.95)
            top_k = model_config.get("top_k", 40)
            
            # Khởi tạo model
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            }
            
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            
            # Xử lý hình ảnh: Chuyển đổi từ bytes sang định dạng PIL Image
            image_bytes = image_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Tạo prompt OCR mặc định nếu không được cung cấp
            if prompt is None:
                prompt = """
                Hãy trích xuất đề bài toán từ ảnh này. 
                Chỉ trả về đề bài, không thêm bất kỳ giải thích hoặc phân tích nào.
                Giữ nguyên định dạng toán học và ký hiệu.
                """
            
            # Ghi log bắt đầu xử lý ảnh
            self.logger.log_step("start_process_image", {
                "model": model_name,
                "prompt_length": len(prompt) if prompt else 0
            })
            
            # Đo thời gian xử lý
            start_time = time.time()
            
            # Gọi API để xử lý ảnh
            response = model.generate_content([prompt, image])
            
            # Tính thời gian xử lý
            execution_time = time.time() - start_time
            
            # Ghi log kết quả
            self.logger.log_llm_interaction(
                prompt=prompt,
                response=response.text,
                model_name=model_name,
                execution_time=execution_time,
                metadata={
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "image_processing": True
                }
            )
            
            # Lấy nội dung từ response
            return response.text
            
        except Exception as e:
            error_message = f"Lỗi khi xử lý ảnh: {str(e)}"
            self.logger.log_error(error_message, {
                "model": model_config.get("model_name") if model_config else "unknown",
                "prompt": prompt[:500] + "..." if prompt and len(prompt) > 500 else prompt
            })
            return f"Xin lỗi, đã xảy ra lỗi khi xử lý ảnh của bạn: {str(e)}"