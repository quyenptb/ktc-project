# Abstract class (normalize, reply)from abc import ABC, abstractmethod

from abc import ABC, abstractmethod

class BasePlatformAdapter(ABC):
    """
    Abstract Class quy định chuẩn cho mọi nền tảng (Slack, Kakao, Web)
    để đảm bảo Core Engine không bao giờ bị phụ thuộc vào API bên thứ 3.
    """
    
    @abstractmethod
    def normalize_input(self, raw_payload: dict) -> dict:
        """Chuẩn hóa dữ liệu webhook thành format: {user_id, text, metadata}"""
        pass

    @abstractmethod
    def format_and_reply(self, target_id: str, ai_response: dict):
        """Nhận JSON chuẩn từ LLM và biến đổi thành UI của nền tảng tương ứng"""
        pass