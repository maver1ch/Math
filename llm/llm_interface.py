"""
Module kết nối với API của Gemini
"""
import os
import base64
import google.generativeai as genai
from config.llm_config import API_KEY, SYSTEM_PROMPT
from PIL import Image
import io

class LLMInterface:
    """
    Lớp giao tiếp với Large Language Models (Gemini)
    """
    def __init__(self):
        """
        Khởi tạo giao tiếp với API Gemini
        """
        # Cấu hình API key
        genai.configure(api_key=API_KEY)
    
    def generate_content(self, prompt, model_config, with_system_prompt=True):
        """
        Gọi API Gemini để sinh nội dung
        
        Args:
            prompt (str): Prompt đầu vào
            model_config (dict): Cấu hình model
            with_system_prompt (bool): Có sử dụng system prompt hay không
            
        Returns:
            str: Nội dung được sinh bởi model
        """
        try:
            # Lấy thông tin cấu hình
            safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH" 
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
            ]
                        
            model_name = model_config.get("model_name", "gemini-1.5-flash")
            temperature = model_config.get("temperature", 0.1)
            top_p = model_config.get("top_p", 0.95)
            top_k = model_config.get("top_k", 40)
            max_output_tokens = model_config.get("max_output_tokens", 1024)
            
            # Khởi tạo model
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            }
            
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                safety_settings=safety_settings 
            )
            
            # Thêm system prompt nếu cần
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
            
            return response.text
            
        except Exception as e:
            print(f"Lỗi khi gọi API Gemini: {str(e)}")
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
            max_output_tokens = model_config.get("max_output_tokens", 1024)
            
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
            
            # Gọi API để xử lý ảnh
            response = model.generate_content([prompt, image])
            
            # Lấy nội dung từ response
            return response.text
            
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh: {str(e)}")
            return f"Xin lỗi, đã xảy ra lỗi khi xử lý ảnh của bạn: {str(e)}"