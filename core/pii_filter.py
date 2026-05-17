# Module lọc PII bằng Regex


import re

def mask_pii(text: str) -> str:
    """
    Mã hóa thông tin nhạy cảm trước khi gửi lên LLM.
    Bản MVP dùng Regex. Bản Production cân nhắc Microsoft Presidio.
    """
    if not text:
        return ""
        
    # Mask Email
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL_REDACTED]', text)
    
    # Mask Số điện thoại VN (VD: 098xxxxxxx, 03xxxxxxxx)
    text = re.sub(r'\b0[35789]\d{8}\b', '[PHONE_REDACTED]', text)
    
    # Mask Mã dự án mật (Giả lập: Bắt đầu bằng KTC-SECRET-)
    text = re.sub(r'\bKTC-SECRET-\w+\b', '[PROJECT_REDACTED]', text)
    
    return text