import os
from slack_bolt import App
from core.pii_filter import mask_pii
from core.rag_engine import SimpleRAGEngine
from core.llm_handler import LLMHandler
from core.escalation import check_and_escalate

class SlackTextAdapter:
    """
    Adapter xử lý giao tiếp thực tế với Slack Workspace sử dụng Slack Bolt Framework.
    Nhận sự kiện Webhook từ Slack -> Chuẩn hóa -> Chạy qua Core Engine -> Phản hồi.
    """
    def __init__(self):
        self.app = App(
            token=os.getenv("SLACK_BOT_TOKEN"),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET")
        )
        self.rag_engine = SimpleRAGEngine()
        self.llm_handler = LLMHandler()
        self.register_events()

    def register_events(self):
        # 1. Bắt sự kiện lần đầu tiên nhân viên mở tab tin nhắn của App Home
        @self.app.event("app_home_opened")
        def handle_app_home_opened(event, client, ack):
            ack()
            user_id = event["user"]
            
            # Gửi Block Kit chào mừng nhân viên mới, thiết lập tâm lý "Chạm thẻ để bắt đầu"
            welcome_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Chào mừng cậu đã gia nhập gia đình KTC! 🎉\nTôi là *Park Ji-hoon (Sếp Park)*, người sẽ đồng hành và hỗ trợ cậu trong suốt quá trình thử việc tại đây."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hãy chạm nhẹ thẻ NFC cá nhân của cậu vào điện thoại để mở cổng thông tin và sẵn sàng nhận nhiệm vụ đầu tiên nhé!"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Bắt đầu Onboarding"
                            },
                            "style": "primary",
                            "value": "onboard_start_clicked",
                            "action_id": "btn_onboard_start"
                        }
                    ]
                }
            ]
            try:
                # Gửi tin nhắn trực tiếp cho người dùng
                client.chat_postMessage(channel=user_id, blocks=welcome_blocks)
            except Exception as e:
                print(f"[SlackAdapter] Lỗi gửi tin nhắn chào mừng: {e}")

        # 2. Xử lý khi nhân viên nhấn nút "Bắt đầu Onboarding"
        @self.app.action("btn_onboard_start")
        def handle_onboard_start(ack, body, client):
            ack()
            user_id = body["user"]["id"]
            
            start_message = (
                "Ne! Rất tốt! Tinh thần làm việc rất khẩn trương.\n"
                "Nhiệm vụ đầu tiên của cậu là tìm hiểu về quy trình phê duyệt đơn từ (*Gyeoljae*) và viết báo cáo (*Bogo*) hàng tuần.\n"
                "Cậu có câu hỏi nào cho tôi về 2 quy trình này không?"
            )
            client.chat_postMessage(channel=user_id, text=start_message)

        # 3. Lắng nghe mọi tin nhắn dạng text của người dùng gửi cho Bot
        @self.app.event("message")
        def handle_message_events(event, client, ack):
            ack()
            # Bỏ qua tin nhắn do chính Bot gửi để tránh lặp vô hạn
            if event.get("bot_id") is not None:
                return

            user_id = event["user"]
            raw_text = event.get("text", "")
            channel_id = event["channel"]

            # TIẾN TRÌNH XỬ LÝ CORE ENGINE (Platform-Agnostic):
            # Bước 1: Masking thông tin nhạy cảm PII bảo vệ dữ liệu
            masked_text = mask_pii(raw_text)

            # Bước 2: Truy xuất tài liệu nội bộ (RAG)
            context = self.rag_engine.search(masked_text)

            # Bước 3: Đưa qua LLM xử lý định dạng JSON
            ai_response = self.llm_handler.generate_response(masked_text, context)

            # Bước 4: Chạy bộ lọc Escalation an toàn (Human-in-the-loop)
            check_and_escalate(client, user_id, masked_text, ai_response)

            # Bước 5: Đóng gói và gửi phản hồi lại Slack bằng Block Kit cho trực quan
            response_text = ai_response.get("response_vi", "")
            terms_dict = ai_response.get("korean_terms_explained", {})

            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": response_text
                    }
                }
            ]

            # Nếu có từ vựng tiếng Hàn khó hiểu, đính kèm bảng giải nghĩa văn hóa
            if terms_dict:
                terms_list = [f"• *{k}*: {v}" for k, v in terms_dict.items()]
                terms_text = "\n".join(terms_list)
                blocks.append({
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"✍️ *Từ điển văn hóa của sếp:*\n{terms_text}"
                        }
                    ]
                })

            try:
                client.chat_postMessage(channel=channel_id, blocks=blocks)
            except Exception as e:
                print(f"[SlackAdapter] Lỗi gửi phản hồi chat: {e}")