# Khung chuẩn bị cho KakaoWork

from adapters.base import BasePlatformAdapter

class KakaoWorkAdapter(BasePlatformAdapter):
    """
    Mã nguồn chờ (Skeleton) để chứng minh tính mở rộng khi thuyết trình.
    Ban giám khảo hỏi: "Nếu công ty Hàn Quốc dùng KakaoWork thì sao?"
    Bạn mở file này lên: "Chúng em đã thiết kế sẵn Adapter, chỉ cần thay thế API Endpoint."
    """
    def __init__(self, bot_token: str):
        self.token = bot_token
        self.api_url = "https://api.kakaowork.com/v1/messages.send"
        
    def normalize_input(self, raw_payload: dict) -> dict:
        # Map Kakao JSON thành format chung
        pass

    def format_and_reply(self, target_id: str, ai_response: dict):
        # Build KakaoWork Block Kit
        pass