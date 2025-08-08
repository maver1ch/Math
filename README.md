# Math Mentor AI - Hướng dẫn sử dụng

## Cài đặt

```bash
# Clone repository
git clone https://github.com/maver1ch/Math.git

# Tạo môi trường Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

## Cấu hình API key

Tạo file `.streamlit/secrets.toml` với nội dung:
```toml
[api_keys]
gemini_api_key = "YOUR_API_KEY"
```

## Chạy ứng dụng

```bash
# Khởi động server
streamlit run app/main.py
```

Ứng dụng sẽ tự động mở trong trình duyệt mặc định tại địa chỉ http://localhost:8501
