import os
import json
from datetime import datetime
import inspect

class LLMLogger:
    
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log_llm_interaction(self, prompt, response, model_name, execution_time=None, metadata=None):
        """
        Ghi log tương tác với LLM
        
        Args:
            prompt (str): Prompt gửi cho LLM
            response (str): Phản hồi từ LLM
            model_name (str): Tên model LLM
            execution_time (float, optional): Thời gian xử lý (giây)
            metadata (dict, optional): Metadata bổ sung
        """
        today = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{self.log_dir}/llm_log_{today}.jsonl"
        
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)
        caller_function = caller_info.function
        caller_module = caller_info.filename
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "caller": {
                "module": os.path.basename(caller_module),
                "function": caller_function
            },
            "model": model_name,
            "prompt": prompt,
            "response": response,
            "execution_time": execution_time
        }
        
        if metadata:
            log_entry["metadata"] = metadata
        
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def log_error(self, error_message, context=None):
        """
        Ghi log lỗi
        
        Args:
            error_message (str): Thông báo lỗi
            context (dict, optional): Ngữ cảnh lỗi
        """
        today = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{self.log_dir}/error_log_{today}.jsonl"
        
        # Tạo entry log
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": error_message
        }
        
        # Thêm context nếu có
        if context:
            log_entry["context"] = context
        
        # Ghi log vào file
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
    def log_step(self, step_name, details=None):
        """
        Ghi log bước xử lý
        
        Args:
            step_name (str): Tên bước xử lý
            details (dict, optional): Chi tiết bước xử lý
        """
        # Tạo tên file log theo ngày
        today = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{self.log_dir}/step_log_{today}.jsonl"
        
        # Tạo entry log
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "step": step_name
        }
        
        # Thêm details nếu có
        if details:
            log_entry["details"] = details
        
        # Ghi log vào file
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")