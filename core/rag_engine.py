import json
import os
import math
import logging
from typing import List, Dict, Set
from core.jira_confluence_connector import AtlassianConnector

logger = logging.getLogger("SimpleRAGEngine")

# =============================================================================
# CONFIGURATION: Danh sách từ dừng và từ khóa boosting cho tiếng Việt
# =============================================================================
VI_STOPWORDS: Set[str] = {
    "sếp", "em", "tớ", "mình", "cậu", "ạ", "nhỉ", "nhé", "nha", "cho", "giúp", 
    "hỏi", "xem", "có", "những", "nào", "đang", "cần", "làm", "thế", "là", "gì", 
    "ở", "trong", "của", "để", "và", "với", "ơi", "đâu", "ai", "được", "bị", "ra", 
    "vào", "lên", "xuống", "kiểm", "tra", "thế", "này", "đó", "mấy", "giờ",
    # Bổ sung thêm các từ dừng phổ biến khác
    "tôi", "bạn", "anh", "chị", "ông", "bà", "cô", "chú", "bác", "đã", "sẽ", "đang"
}

BOOST_KEYWORDS: Dict[str, float] = {
    # Technical keywords - High priority
    "task": 5.0, "tasks": 5.0, "jira": 5.0, "ticket": 4.5,
    # Domain-specific keywords (Korean/Vietnamese mix)
    "bogo": 5.0, "gyeoljae": 5.0, "hoesik": 5.0, "nunchi": 5.0,
    # Vietnamese business keywords
    "đầu việc": 4.0, "công việc": 3.5, "quy trình": 3.5, 
    "báo cáo": 3.0, "lịch": 3.0, "hạn": 3.0, "deadline": 4.0,
    # Action keywords
    "duyệt": 3.0, "phê duyệt": 3.5, "xin phép": 3.0
}

TASK_INDICATORS: Set[str] = {"task", "tasks", "jira", "việc", "đầu việc", "ticket", "công việc"}


class SimpleRAGEngine:
    """
    RAG Engine thông minh chạy trực tiếp trong bộ nhớ (In-Memory).
    
    Features:
    - ✅ Lọc từ dừng tiếng Việt (Stopwords) để giảm nhiễu
    - ✅ Boosting từ khóa cốt lõi với trọng số tùy chỉnh
    - ✅ Chuẩn hóa độ dài tài liệu (Length Normalization) ưu tiên nội dung súc tích
    - ✅ Ưu tiên tài liệu loại 'task' khi query liên quan đến công việc
    - ✅ Fallback tự động sang Mock Data khi API không khả dụng
    - ✅ Logging chi tiết phục vụ debugging và monitoring
    """
    
    def __init__(self, enable_logging: bool = True):
        """
        Khởi tạo RAG Engine.
        
        Args:
            enable_logging: Bật/tắt logging chi tiết (default: True)
        """
        self.connector = AtlassianConnector()
        self.documents: List[Dict] = []
        self.enable_logging = enable_logging
        self._log_level = logging.INFO if enable_logging else logging.WARNING
        self.init_vector_store()

    def get_mock_data(self) -> List[Dict]:
        """Trả về dữ liệu dự phòng khi không thể kết nối API thật."""
        return [
            {
                "title": "Quy trình xin duyệt đơn (Gyeoljae)",
                "content": "Tại KTC, mọi đơn từ nghỉ phép, chi phí dự án hoặc đề xuất kỹ thuật đều phải thông qua quy trình Gyeoljae (Phê duyệt điện tử). Người dùng cần đăng nhập hệ thống, chọn loại đơn, điền thông tin và gửi đến người phê duyệt theo sơ đồ tổ chức.",
                "source": "Confluence SOP",
                "type": "policy",
                "metadata": {"last_updated": "2024-01-15"}
            },
            {
                "title": "Task: Cập nhật tài liệu onboarding",
                "content": "Cần cập nhật tài liệu hướng dẫn onboarding cho nhân viên mới, bao gồm quy trình đăng ký tài khoản, setup môi trường làm việc và lịch training tuần đầu.",
                "source": "Jira PROJ-1234",
                "type": "task",
                "metadata": {"status": "in_progress", "assignee": "team-lead"}
            }
        ]

    def init_vector_store(self) -> None:
        """Khởi tạo và nạp dữ liệu từ các nguồn vào vector store in-memory."""
        self.documents = []
        fetch_errors = []
        
        # 1. Tải dữ liệu từ Confluence
        logger.log(self._log_level, "[RAG Engine] Đang kết nối lấy dữ liệu từ Confluence...")
        try:
            pages = self.connector.fetch_live_confluence_pages()
            for p in pages:
                self.documents.append({
                    "title": p.get("metadata", {}).get("source", "Untitled"),
                    "content": p.get("content", ""),
                    "source": p.get("metadata", {}).get("source", "Unknown"),
                    "type": "policy",
                    "metadata": p.get("metadata", {})
                })
            logger.log(self._log_level, f"✓ Đã nạp {len(pages)} trang từ Confluence")
        except Exception as e:
            fetch_errors.append(f"Confluence: {str(e)}")
            logger.warning(f"[RAG Engine] Lỗi khi fetch Confluence: {e}")
            
        # 2. Tải dữ liệu từ Jira
        logger.log(self._log_level, "[RAG Engine] Đang kết nối lấy dữ liệu từ Jira...")
        try:
            tasks = self.connector.fetch_live_jira_tasks()
            for t in tasks:
                self.documents.append({
                    "title": t.get("metadata", {}).get("source", "Untitled"),
                    "content": t.get("content", ""),
                    "source": t.get("metadata", {}).get("source", "Unknown"),
                    "type": "task",
                    "metadata": t.get("metadata", {})
                })
            logger.log(self._log_level, f"✓ Đã nạp {len(tasks)} task từ Jira")
        except Exception as e:
            fetch_errors.append(f"Jira: {str(e)}")
            logger.warning(f"[RAG Engine] Lỗi khi fetch Jira: {e}")

        # 3. Fallback sang Mock Data nếu không có dữ liệu Live
        if not self.documents:
            logger.warning("[RAG Engine] ⚠️ WARNING: Không có dữ liệu Live. Kích hoạt chế độ Fallback Mock Data.")
            if fetch_errors:
                logger.warning(f"[RAG Engine] Lỗi kết nối: {'; '.join(fetch_errors)}")
            self.documents = self.get_mock_data()
        else:
            logger.info(f"[RAG Engine] ✅ SUCCESS: Đã nạp {len(self.documents)} tài liệu vào RAG!")

    def _normalize_query(self, query: str) -> List[str]:
        """Chuẩn hóa câu query: lowercase, loại bỏ punctuation, lọc stopwords."""
        import re
        # Remove punctuation và normalize whitespace
        cleaned = re.sub(r'[^\w\s]', ' ', query.lower())
        raw_words = cleaned.split()
        # Filter stopwords
        filtered = [w for w in raw_words if w not in VI_STOPWORDS]
        # Fallback: nếu lọc xong trống, dùng từ gốc để tránh mất thông tin
        return filtered if filtered else raw_words

    def _calculate_score(self, query_words: List[str], doc: Dict) -> tuple[float, List[str]]:
        """
        Tính điểm relevance cho document dựa trên:
        1. Keyword matching với boosting weight
        2. Type-based boosting (ưu tiên task khi query liên quan)
        3. Length normalization (ưu tiên nội dung súc tích)
        
        Returns:
            tuple: (normalized_score, list_of_matched_words)
        """
        doc_text = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
        score = 0.0
        matched_words = []
        
        # Bước 1: Keyword matching với boosting
        for word in query_words:
            if word in doc_text:
                weight = BOOST_KEYWORDS.get(word, 1.0)
                score += weight
                matched_words.append(word)
        
        if score == 0:
            return 0.0, []
        
        # Bước 2: Type-based boosting (2x cho task khi query liên quan)
        if any(w in TASK_INDICATORS for w in query_words) and doc.get("type") == "task":
            score *= 2.0
            if self.enable_logging:
                logger.debug(f"  → Boost 2x cho task document: {doc.get('source')}")
        
        # Bước 3: Length normalization (log penalty để tránh bias document dài)
        word_count = len(doc_text.split())
        if word_count == 0:
            length_penalty = 1.0
        else:
            length_penalty = math.log(word_count + 1)
        
        normalized_score = score / length_penalty
        return normalized_score, matched_words

    def search(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Tìm kiếm thông minh với ranking dựa trên relevance score.
        
        Args:
            query: Câu hỏi/từ khóa tìm kiếm của người dùng
            limit: Số lượng kết quả tối đa trả về (default: 3)
            
        Returns:
            List[Dict]: Danh sách documents được rank theo độ phù hợp
        """
        if not query or not query.strip():
            return []
            
        # Bước 1: Preprocess query
        query_words = self._normalize_query(query)
        if self.enable_logging:
            logger.info(f"🔍 Query: '{query}' → Keywords sau lọc: {query_words}")
        
        scored_docs = []
        
        # Bước 2: Score từng document
        for doc in self.documents:
            score, matched = self._calculate_score(query_words, doc)
            if score > 0:
                scored_docs.append((score, doc, matched))
                if self.enable_logging and len(scored_docs) <= 5:
                    logger.debug(f"  Score={score:.3f} | {doc.get('source')} | Matched: {matched}")
        
        # Bước 3: Sort và lấy top-K
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Logging kết quả (chỉ top 5 để tránh spam log)
        if self.enable_logging and scored_docs:
            logger.info("=== 📊 RAG Ranking Results (Top 5) ===")
            for idx, (score, doc, matched) in enumerate(scored_docs[:5], 1):
                logger.info(f"#{idx} Score={score:.3f} | {doc.get('source')} | {matched}")
        
        results = [doc for score, doc, matched in scored_docs[:limit]]
        
        # Fallback: nếu không có match, trả về documents mới nhất (nếu có)
        if not results and self.documents:
            logger.warning(f"⚠️ No keyword match for '{query}'. Returning default documents.")
            return self.documents[:limit]
            
        return results

    def refresh(self) -> None:
        """Làm mới dữ liệu từ các nguồn live (dùng khi cần cập nhật real-time)."""
        logger.info("[RAG Engine] 🔄 Refreshing vector store...")
        self.init_vector_store()