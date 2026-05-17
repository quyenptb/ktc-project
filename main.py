import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Thêm import middleware
from dotenv import load_dotenv

# Load biến môi trường từ file .env trước khi chạy app
load_dotenv()

from adapters.slack_text_adapter import SlackTextAdapter
from slack_bolt.adapter.fastapi import SlackRequestHandler
from adapters.web_voice_adapter import router as voice_router

app = FastAPI(
    title="KTC Onboarding Digital Twin Backend",
    description="Hệ thống Middleware đa nền tảng kết hợp RAG và LLM hỗ trợ nhân sự thử việc",
    version="1.0.0"
)

# Cấu hình CORSMiddleware để cho phép mọi origin (sửa lỗi Swagger UI bị chặn)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo Slack Adapter
slack_adapter = SlackTextAdapter()
slack_handler = SlackRequestHandler(slack_adapter.app)

# Đăng ký router cho luồng Web Voice Demo (Avatar)
app.include_router(voice_router, prefix="/demo")

@app.get("/")
def health_check():
    """Trang chủ để kiểm tra server có đang sống (trên Render) hay không"""
    return {
        "status": "healthy",
        "platform_active": os.getenv("PLATFORM", "slack"),
        "atlassian_connected": "True" if os.getenv("ATLASSIAN_API_TOKEN") else "False"
    }

@app.post("/slack/events")
async def slack_events_endpoint(req: Request):
    """
    Endpoint tiếp nhận toàn bộ Webhook từ Slack Events API.
    Đã sửa lỗi kiểu dữ liệu Request để tránh FastAPI hiểu lầm thành Query Parameter.
    """
    return await slack_handler.handle(req)

if __name__ == "__main__":
    import uvicorn
    # Chạy cục bộ dưới local để debug trước khi đẩy lên Render
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
