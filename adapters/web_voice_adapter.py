from fastapi import APIRouter
from pydantic import BaseModel
from core.pii_filter import mask_pii
from core.glossary_mapper import map_cultural_terms
from core.rag_engine import SimpleRAGEngine
from core.llm_handler import LLMHandler

router = APIRouter()

class VoiceChatRequest(BaseModel):
    user_id: str
    text: str  # Được speech-to-text từ Web Client chuyển lên

# Khởi tạo các instance nghiệp vụ toàn cục của Core Engine
rag_engine = SimpleRAGEngine()
llm_handler = LLMHandler()

@router.post("/api/v1/voice-chat")
async def handle_voice_chat(request: VoiceChatRequest):
    """
    Endpoint chuyên dụng cho luồng Demo có Avatar 2D/3D trên màn hình bự.
    Đã sửa toàn bộ lỗi import sai hàm và xử lý dữ liệu đầu ra dạng dict chuẩn xác.
    """
    raw_text = request.text
    
    # Bước 1: Masking dữ liệu nhạy cảm PII
    masked_text = mask_pii(raw_text)
    
    # Bước 2: Truy xuất ngữ cảnh RAG tài liệu
    rag_context = rag_engine.search(masked_text)
    
    # Bước 3: Lấy từ điển ngữ cảnh văn hóa bổ sung
    glossary_context = map_cultural_terms(raw_text)
    if glossary_context:
        # Bổ sung thuật ngữ văn hóa phát hiện được vào tập ngữ cảnh của RAG
        rag_context.append({
            "title": "Ngữ cảnh thuật ngữ văn hóa phát hiện",
            "content": glossary_context,
            "source": "Local Glossary Mapper"
        })
    
    # Bước 4: Gọi LLM sinh phản hồi có cấu trúc nghiêm ngặt
    ai_response = llm_handler.generate_response(masked_text, rag_context)
    
    # Trả kết quả JSON chuẩn về cho Frontend Client (React)
    return {
        "status": "success",
        "audio_text": ai_response.get("response_vi", ""),
        "avatar_emotion": "concerned" if ai_response.get("escalate", False) else "friendly",
        "meta": {
            "confidence": ai_response.get("confidence", 1.0)
        }
    }