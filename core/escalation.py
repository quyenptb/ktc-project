import os
import logging

# Fallback Rule-based: Các từ khóa nhạy cảm mà LLM có thể bỏ sót
CRITICAL_KEYWORDS = ["mệt mỏi", "áp lực", "nghỉ việc", "bắt nạt", "stress", "không hiểu", "bỏ cuộc"]

def check_and_escalate(slack_client, user_id: str, raw_text: str, ai_response: dict) -> bool:
    """
    Kiểm tra các điều kiện Escalation. Trả về True nếu phát hiện bất thường và đã báo động.
    Đã sửa lỗi không khớp số lượng tham số và chuyển sang truy cập dạng Dictionary an toàn.
    """
    reason = ""
    lower_text = raw_text.lower()
    
    # Lấy các trường dữ liệu an toàn từ dict phản hồi của AI
    confidence = ai_response.get("confidence", 1.0)
    escalate_flag = ai_response.get("escalate", False)
    
    # 1. Rule-based Filter (An toàn nhất, quét từ khóa thô của người dùng)
    if any(kw in lower_text for kw in CRITICAL_KEYWORDS):
        reason = "Phát hiện từ khóa rủi ro/tiêu cực trong tin nhắn gốc của nhân viên."
        
    # 2. Confidence Filter (Nếu AI phản hồi quá mơ hồ)
    elif confidence < 0.70:
        reason = f"AI không chắc chắn về câu trả lời (Độ tự tin thấp: {confidence})."
        
    # 3. LLM Flag (AI chủ động phân tích tâm lý tiêu cực từ ngữ cảnh sâu)
    elif escalate_flag:
        reason = "Hệ thống AI chủ động cảnh báo tình huống stress/nhạy cảm của nhân sự."
        
    if reason:
        trigger_human_buddy(slack_client, raw_text, reason)
        return True
        
    return False

def trigger_human_buddy(slack_client, user_input: str, reason: str):
    buddy_channel = os.getenv("HUMAN_BUDDY_CHANNEL_ID")
    if not buddy_channel or not slack_client:
        return
        
    msg = (
        f"🚨 *[HUMAN BUDDY ALERT]* 🚨\n"
        f"Hệ thống phát hiện nhân sự thử việc cần hỗ trợ khẩn cấp!\n"
        f"> *Tin nhắn của user:* {user_input}\n"
        f"> *Lý do kích hoạt:* {reason}\n"
        f"_Chị Hwang vui lòng vào ứng cứu và chia sẻ trực tiếp nhé!_"
    )
    try:
        slack_client.chat_postMessage(channel=buddy_channel, text=msg)
    except Exception as e:
        logging.error(f"Lỗi gửi tin nhắn cho Human Buddy qua Slack API: {e}")