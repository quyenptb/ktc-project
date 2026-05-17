import json
import os
from core.jira_confluence_connector import AtlassianConnector

class SimpleRAGEngine:
    """
    RAG Engine siêu nhẹ chạy trực tiếp trong bộ nhớ (In-Memory).
    Tự động kết hợp dữ liệu Live từ Jira/Confluence và Mock Data dự phòng.
    """
    def __init__(self):
        self.connector = AtlassianConnector()
        self.documents = []
        self.init_vector_store()

    def get_mock_data(self) -> list[dict]:
        """Dữ liệu dự phòng khi không kết nối được API thật."""
        return [
            {
                "title": "Quy trình xin duyệt đơn (Gyeoljae)",
                "content": "Tại KTC, mọi đơn từ nghỉ phép... phải thông qua quy trình Gyeoljae.",
                "source": "Confluence SOP"
            },
            # ... Các dữ liệu mock khác giữ nguyên ...
        ]

    def init_vector_store(self):
        """Khởi tạo và nạp dữ liệu cho RAG."""
        self.documents = []
        
        # 1. Thử kéo dữ liệu thật từ Confluence
        print("[RAG Engine] Đang kết nối lấy dữ liệu từ Confluence...")
        pages = self.connector.fetch_live_confluence_pages() # Sửa tên hàm
        for p in pages:
            self.documents.append({
                "title": p["metadata"]["source"], # Lấy title từ metadata
                "content": p["content"],
                "source": p["metadata"]["source"]
            })
            
        # 2. Thử kéo dữ liệu thật từ Jira
        print("[RAG Engine] Đang kết nối lấy dữ liệu từ Jira...")
        tasks = self.connector.fetch_live_jira_tasks() # Sửa tên hàm
        for t in tasks:
            self.documents.append({
                "title": t["metadata"]["source"], # Lấy title từ metadata
                "content": t["content"],
                "source": t["metadata"]["source"]
            })

        # 3. Fallback sang Mock Data nếu không có dữ liệu Live
        if not self.documents:
            print("[RAG Engine] WARNING: Chế độ Fallback Mock Data kích hoạt.")
            self.documents = self.get_mock_data()
        else:
            print(f"[RAG Engine] SUCCESS: Đã nạp thành công {len(self.documents)} tài liệu Live!")

    def search(self, query: str, limit: int = 2) -> list[dict]:
        """Tìm kiếm ngữ cảnh dựa trên tần suất từ khóa."""
        if not query:
            return []
            
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            doc_text = (doc["title"] + " " + doc["content"]).lower()
            score = sum(1 for word in query_words if word in doc_text)
            if score > 0:
                scored_docs.append((score, doc))
                
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        results = [doc for score, doc in scored_docs[:limit]]
        
        if not results and self.documents:
            return self.documents[:limit]
            
        return results
