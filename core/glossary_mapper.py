# Map từ vựng KR-VN

# Từ điển văn hóa KR-VN (MVP có thể hardcode tĩnh hoặc đọc từ JSON)
GLOSSARY_DB = {
    "결재": "Gyeoljae (Quy trình duyệt đơn nội bộ với nhiều cấp)",
    "보고": "Bogo (Văn hóa báo cáo trực tiếp, liên tục cho cấp trên)",
    "회식": "Hoesik (Tiệc gắn kết nội bộ sau giờ làm, quan trọng để thăng tiến)",
    "눈치": "Nunchi (Kỹ năng quan sát tinh tế, đoán ý sếp/đồng nghiệp)"
}

def map_cultural_terms(text: str) -> str:
    """
    Quét tin nhắn người dùng, nếu chứa từ khóa thì trích xuất nghĩa
    để nhồi vào prompt cho AI, giúp AI có "Nunchi".
    """
    matched_terms = {}
    lower_text = text.lower()
    
    for kr_term, definition in GLOSSARY_DB.items():
        # Kiểm tra cả tiếng Hàn lẫn tiếng Việt/Romaja
        term_keyword = definition.split("(")[0].strip().lower()
        if kr_term in text or term_keyword in lower_text:
            matched_terms[kr_term] = definition
            
    if not matched_terms:
        return ""
        
    context = "💡 [Cultural Context Detected]:\n"
    for k, v in matched_terms.items():
        context += f"- {k}: {v}\n"
    return context