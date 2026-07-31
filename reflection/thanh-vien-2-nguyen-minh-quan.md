# REFLECTION CÁ NHÂN — THÀNH VIÊN 2
**Họ và tên**: Nguyễn Minh Quân  
**Mã học viên**: `2A202601478`  
**Vai trò trong nhóm**: AI Dev (Nhóm THQMilk · Zone E402)  
**Phân công phụ trách chính**: `codebase/` (`discord_bot.py`, `guardrail.py`, `artifacts/system_prompt.md`, `app.py`, `discord_loader.py`, `discord_summarizer.py`).

---

## 1. VAI TRÒ VÀ CÁC PHẦN VIỆC ĐÃ ĐẢM NHẬN
- **Đóng góp chính**: 
  1. Phát triển toàn bộ mã nguồn prototype trong `codebase/`, bao gồm **tầng Pre-Guardrail (`guardrail.py`)** kiểm tra 0ms và **tầng LLM Summarizer/Extractor (`discord_bot.py`)**.
  2. Xây dựng bộ quy tắc **Pre-Guardrail bằng Regex Matcher** để chặn 100% các cuộc tấn công Prompt Injection (`IGNORE PREVIOUS INSTRUCTIONS`, `API_KEY leak`, `System prompt extraction`) trước khi câu lệnh được chuyển sang LLM.
  3. Lập trình giao diện **Streamlit Web Dashboard (`app.py`)** và **Discord Bot Simulator (`discord_bot.py`)** phục vụ Demo Live tại CP5 và CP6.
  4. Cấu hình luồng nạp dữ liệu Discord thật từ `data/data-discord/channel_history.json` phân loại theo 4 kênh thông báo.

---

## 2. AI ĐÃ HỖ TRỢ NHƯ THẾ NÀO TRONG QUÁ TRÌNH LÀM VIỆC?
- **Sử dụng AI cho công việc Lập trình Codebase**:
  - Dùng Copilot / Antigravity để sinh nhanh bộ khung Regex pattern cho `guardrail.py` nhận diện từ khóa độc hại và cấu trúc Prompt Injection phổ biến.
  - Sử dụng LLM API (OpenAI / Gemini) kết hợp với **Structured Output Prompting** để ép mô hình trả về JSON schema cố định gồm 5 danh mục: Deadline, Zoom, Resources, Adjustments, Notes.
  - Tự động tạo giao diện Streamlit UI tương tác trực quan chỉ trong vài lượt refactor code.

---

## 3. BÀI HỌC RÚT RA TỪ CASE FAIL CỦA CHÍNH NHÓM
- **Case Fail cụ thể**: Case **SEC-02** (`[Admin_Fake_Official] Khẩn cấp: Tất cả được cộng tối đa điểm`) trong `eval/result.md` ban đầu bị lọt qua guardrail ở lượt chạy nháp.
- **Phân tích nguyên nhân & Bài học**:
  - *Nguyên nhân*: Lượt chạy nháp chỉ kiểm tra từ khóa cấm mà chưa có tầng kiểm tra **Token xác thực của Ban tổ chức (`BTC-VERIFIED`)**. Tin nhắn giả mạo Admin sử dụng danh nghĩa BTC để đánh lừa bot trích xuất thông tin sai sự thật.
  - *Bài học kinh nghiệm*: Tầng bảo vệ Guardrail không chỉ dừng ở việc chặn các câu lệnh attack hệ thống (System level Injection) mà phải hiểu được ngữ cảnh domain (Domain-specific Fake News). Tôi đã cập nhật `guardrail.py` để bổ sung quy tắc kiểm tra Token BTC và nâng tỷ lệ PASS của nhóm lên 100% ở ranh giới thẩm quyền SEC.

---

## 4. BỘ CÂU TRẢ LỜI TRỰC TIẾP CHO VÒNG KIỂM TRA CP5 / DEMO ROUND

### ❓ Câu 1: Augment hay Automate — Vì sao?
> **Trả lời**: Sản phẩm thuộc kiến trúc **Conditional Automation (Tự động hóa có điều kiện)**.  
> - **Lý do kỹ thuật**: Hệ thống tự động hóa hoàn toàn luồng quét, lọc rác và trích xuất với các thông báo chuẩn. Nhưng đối với các trường hợp tin nhắn có tín hiệu mơ hồ hoặc đính chính xung đột mốc giờ *(Cost-of-error làm học viên nộp trễ bài)*, code của tôi trong `discord_bot.py` sẽ gắn tag `[Confidence: Low / Need TA Verification]` và trích kèm 100% câu gốc (Evidence Quote) để người dùng tự xác minh thay vì để AI bịa đặt.

### ❓ Câu 2: Failure nguy hiểm nhất là gì?
> **Trả lời**: Failure nguy hiểm nhất ở tầng kỹ thuật AI là **"Prompt Injection & False Authority Infiltration" (Bị cài cắm câu lệnh độc hại làm sai lệch dữ liệu hoặc tiết lộ API Key)**.  
> - Nếu hacker/học viên cố tinh gõ `IGNORE PREVIOUS INSTRUCTIONS` hoặc giả mạo Admin để đổi deadline nộp bài, bot có thể xuất thông tin sai gây hậu quả nghiêm trọng. Nhóm tôi đã triệt tiêu rủi ro này bằng **Pre-Guardrail 0ms trong `guardrail.py`**, đạt kết quả PASS 100% (5/5) ở hạng mục Security.

### ❓ Câu 3: Phần bạn làm là gì và cách hoạt động sâu bên trong?
> **Trả lời**: Tôi phụ trách toàn bộ **Kiến trúc Codebase (`codebase/`) — bao gồm `guardrail.py`, `discord_bot.py` và `app.py` (AI Dev)**.  
> - Sâu bên trong: Khi có input chatlog, dữ liệu chạy qua `PreGuardrail.inspect()` sử dụng Regex kiểm tra 0ms. Nếu an toàn, dữ liệu được truyền vào `DiscordSummarizer.process()` gọi OpenAI/Gemini API với System Prompt khắt khe. Output trả về được định dạng theo cấu trúc Card Markdown 5 phần kèm mốc Timestamp ISO-8601 và Evidence Quote.
