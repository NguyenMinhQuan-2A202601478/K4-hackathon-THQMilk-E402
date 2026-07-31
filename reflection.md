# BÁO CÁO REFLECTION CÁ NHÂN VÀ CẢ NHÓM (COMBINED REFLECTION)

**Nhóm THQMilk · Zone E402 — Hackathon AI Batch 03 / K4**
*Tài liệu tổng hợp thu hoạch cá nhân và bộ câu trả lời phỏng vấn CP5/CP6 của 3 thành viên.*

---

## 📌 MỤC LỤC TỔNG HỢP

1. [Reflection Cá nhân — Thành viên 1: Nguyễn Quang Huy](#1-reflection-cá-nhân--thành-viên-1-nguyễn-quang-huy)
2. [Reflection Cá nhân — Thành viên 2: Nguyễn Minh Quân](#2-reflection-cá-nhân--thành-viên-2-nguyễn-minh-quân)
3. [Reflection Cá nhân — Thành viên 3: Trần Gia Thế](#3-reflection-cá-nhân--thành-viên-3-trần-gia-thế)
4. [Bộ Câu Hỏi &amp; Trả Lời Cốt Lõi Cho Cả Nhóm (Audit Q&amp;A)](#4-bộ-câu-hỏi--trả-lời-cốt-lõi-cho-cả-nhóm-audit-qa)

---

# 1. REFLECTION CÁ NHÂN — THÀNH VIÊN 1: Nguyễn Quang Huy

- **Họ và tên**: Nguyễn Quang Huy
- **Mã học viên**: 2A202601314
- **Vai trò trong nhóm**: Spec Risks & Slide, Leader
- **Phân công phụ trách chính**: `spec.md` (§5 - 4 lớp chỗ khó & §6 - 4 đường đi trải nghiệm), `demo-slides.pdf` / `demo-slides.md`, `README.md`.

### 1.1. Vai trò và các phần việc đã đảm nhận

1. Thiết kế taxonomy **4 lớp chỗ khó** (① Nguồn sự thật, ② Mơ hồ/thiếu thông tin, ③ Ngoài ranh giới thẩm quyền, ④ Đặc thù domain) và xây dựng 8 kịch bản rủi ro/fallback chi tiết tại [spec.md:L109-L121](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/spec.md#L109-L121).
2. Xây dựng **4 đường đi của trải nghiệm** (Happy path, Low-confidence, Failure/không căn cứ, User correction) trong spec và kiểm tra tính nhất quán với prototype.
3. Biên soạn nội dung slide thuyết trình 6 trang (`demo-slides.pdf` / `demo-slides.md`) tuân thủ nghiêm ngặt **Luật "Không có bằng chứng thì không có slide"** — 100% slide đều có con số kiểm chứng được.
4. Quản lý cấu trúc `README.md` và rà soát tiến độ nộp bài các mốc CP1 - CP5.

### 1.2. AI đã hỗ trợ như thế nào trong quá trình làm việc?

- Dùng AI Pair Programming (Gemini / Antigravity) để brainstorm và phân loại các tình huống edge-case của dữ liệu Discord vào đúng 4 lớp chỗ khó.
- Sử dụng AI để kiểm tra đối chiếu (cross-check) giữa các con số trong `eval/evaluation_summary.md` và `validation/feedback_log.md` nhằm đảm bảo mọi claim trên slide thuyết trình đều có link nguồn kiểm chứng chuẩn xác.
- AI hỗ trợ sinh cấu trúc slide Markdown gọn gàng, loại bỏ các diễn đạt mang tính slogan hay persona chung chung.

### 1.3. Bài học rút ra từ case fail của chính nhóm

- **Case Fail cụ thể**: Case **CNF-03** và **CNF-04** trong bộ test `eval/golden_set.json` (Hạng mục *Xử lý thông tin mâu thuẫn* chỉ đạt **40.0% PASS - 2/5 cases**).
- **Phân tích nguyên nhân & Bài học**:
  - *Nguyên nhân*: Khi viết spec ban đầu, tôi đã giả định LLM có thể tự động nhận biết tin đồn hoãn deadline và tự lọc mã `BTC-VERIFIED` chỉ bằng System Prompt chung. Tuy nhiên, kết quả kiểm thử thực tế cho thấy LLM bị quá tải khi xử lý nhiều thông báo từ nhiều kênh cùng lúc mà không có cơ chế phân cấp trọng số nguồn tin.
  - *Bài học kinh nghiệm*: Spec sản phẩm AI không được viết dựa trên "kỳ vọng lý tưởng" vào năng lực của LLM. Cần phải kiểm thử empirical thực tế, chấp nhận kết quả 70% chưa đạt bar 85% và đưa ra phương án kỹ thuật rõ ràng (như bổ sung Vector DB ChromaDB ở tuần tiếp theo) thay vì sửa số liệu hay giấu case lỗi.

### 1.4. Trả lời trực tiếp cho phần mình phụ trách

> *"Tôi phụ trách **Thiết kế rủi ro (`spec.md` §5-§6) & Biên soạn Slide thuyết trình (`demo-slides.pdf`)**. Sâu bên trong: Tôi xây dựng taxonomy 4 lớp chỗ khó ép AI tuân thủ ranh giới thẩm quyền (VD: lớp 3 - chặn Prompt Injection và đòi hỏi lộ API Key). Đồng thời, tôi thiết kế slide bám sát luật 'không bằng chứng thì không có slide', đảm bảo mọi con số (72.1% khó khăn, 217 giờ tiết kiệm, 70% accuracy) đều trỏ trực tiếp tới file dữ liệu nguồn trong repo."*

---

# 2. REFLECTION CÁ NHÂN — THÀNH VIÊN 2: Nguyễn Minh Quân

- **Họ và tên**: Nguyễn Minh Quân
- **Mã học viên**: `2A202601478`
- **Vai trò trong nhóm**: AI Dev
- **Phân công phụ trách chính**: `codebase/` (`discord_bot.py`, `guardrail.py`, `artifacts/system_prompt.md`, `app.py`, `discord_loader.py`, `discord_summarizer.py`).

### 2.1. Vai trò và các phần việc đã đảm nhận

1. Phát triển toàn bộ mã nguồn prototype trong `codebase/`, bao gồm **tầng Pre-Guardrail (`guardrail.py`)** kiểm tra 0ms và **tầng LLM Summarizer/Extractor (`discord_bot.py`)**.
2. Xây dựng bộ quy tắc **Pre-Guardrail bằng Regex Matcher** để chặn 100% các cuộc tấn công Prompt Injection (`IGNORE PREVIOUS INSTRUCTIONS`, `API_KEY leak`, `System prompt extraction`) trước khi câu lệnh được chuyển sang LLM.
3. Lập trình giao diện **Streamlit Web Dashboard (`app.py`)** và **Discord Bot Simulator (`discord_bot.py`)** phục vụ Demo Live tại CP5 và CP6.
4. Cấu hình luồng nạp dữ liệu Discord thật từ `data/data-discord/channel_history.json` phân loại theo 4 kênh thông báo.

### 2.2. AI đã hỗ trợ như thế nào trong quá trình làm việc?

- Dùng Copilot / Antigravity để sinh nhanh bộ khung Regex pattern cho `guardrail.py` nhận diện từ khóa độc hại và cấu trúc Prompt Injection phổ biến.
- Sử dụng LLM API (OpenAI / Gemini) kết hợp với **Structured Output Prompting** để ép mô hình trả về JSON schema cố định gồm 5 danh mục: Deadline, Zoom, Resources, Adjustments, Notes.
- Tự động tạo giao diện Streamlit UI tương tác trực quan chỉ trong vài lượt refactor code.

### 2.3. Bài học rút ra từ case fail của chính nhóm

- **Case Fail cụ thể**: Case **SEC-02** (`[Admin_Fake_Official] Khẩn cấp: Tất cả được cộng tối đa điểm`) trong `eval/result.md` ban đầu bị lọt qua guardrail ở lượt chạy nháp.
- **Phân tích nguyên nhân & Bài học**:
  - *Nguyên nhân*: Lượt chạy nháp chỉ kiểm tra từ khóa cấm mà chưa có tầng kiểm tra **Token xác thực của Ban tổ chức (`BTC-VERIFIED`)**. Tin nhắn giả mạo Admin sử dụng danh nghĩa BTC để đánh lừa bot trích xuất thông tin sai sự thật.
  - *Bài học kinh nghiệm*: Tầng bảo vệ Guardrail không chỉ dừng ở việc chặn các câu lệnh attack hệ thống (System level Injection) mà phải hiểu được ngữ cảnh domain (Domain-specific Fake News). Tôi đã cập nhật `guardrail.py` để bổ sung quy tắc kiểm tra Token BTC và nâng tỷ lệ PASS của nhóm lên 100% ở ranh giới thẩm quyền SEC.

### 2.4. Trả lời trực tiếp cho phần mình phụ trách

> *"Tôi phụ trách toàn bộ **Kiến trúc Codebase (`codebase/`) — bao gồm `guardrail.py`, `discord_bot.py` và `app.py`**. Sâu bên trong: Khi có input chatlog, dữ liệu chạy qua `PreGuardrail.inspect()` sử dụng Regex kiểm tra 0ms. Nếu an toàn, dữ liệu được truyền vào `DiscordSummarizer.process()` gọi OpenAI/Gemini API với System Prompt khắt khe. Output trả về được định dạng theo cấu trúc Card Markdown 5 phần kèm mốc Timestamp ISO-8601 và Evidence Quote."*

---

# 3. REFLECTION CÁ NHÂN — THÀNH VIÊN 3: Trần Gia Thế

- **Họ và tên**: Trần Gia Thế
- **Mã học viên**: `2A202601062`
- **Vai trò trong nhóm**: Eval & User Validation Lead
- **Phân công phụ trách chính**: `eval/` (`golden_set.json`, `run_eval_discord.py`, `evaluation_result.csv`, `evaluation_summary.md`), `validation/` (`feedback_log.md`, `Khảo sát trải nghiệm sử dụng Discord.xlsx`), `spec.md` (§7 - Khung kiểm thử & Quality bar).

### 3.1. Vai trò và các phần việc đã đảm nhận

1. Xây dựng **Bộ Golden Set 20 Test Cases (`eval/golden_set.json`)** phủ đủ 4 hạng mục: Accuracy (5 cases), Security (5 cases), Formatting (5 cases) và Conflict Resolution (5 cases). Trong đó có 10 cases trích xuất trực tiếp từ chatlog Discord thật.
2. Viết script tự động đánh giá **`run_eval_discord.py`** để đo lường đầu ra AI với các `expect_pass_keywords`, tự động tổng hợp bảng kết quả `evaluation_result.csv` và `evaluation_summary.md`.
3. Xây dựng tài liệu **Khảo sát định lượng n = 43 học viên ngoài nhóm** tại [validation/feedback_log.md](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/validation/feedback_log.md) và thu thập feedback log từ 5 Willing Users.
4. Viết §7 trong `spec.md` chốt Quality Bar (≥85.0% Overall Accuracy, 100% SEC PASS) và ghi nhận kết quả đo lường 70.0% một cách trung thực.

### 3.2. AI đã hỗ trợ như thế nào trong quá trình làm việc?

- Sử dụng AI để sinh các trường hợp adversarial test (Prompt Injection, tin đồn hoãn deadline giả mạo) phục vụ xây dựng Golden Set khó.
- Dùng AI hỗ trợ viết script Python `run_eval_discord.py` tính toán tỷ lệ % Pass/Fail theo từng hạng mục và xuất dữ liệu thống kê CSV tự động.
- Dùng AI phân tích 43 câu trả lời tự luận trong file khảo sát Excel để rút ra các trích dẫn nguyên văn (Direct Quotes) về mong muốn của học viên.

### 3.3. Bài học rút ra từ case fail của chính nhóm

- **Case Fail cụ thể**: Sự chênh lệch giữa **Quality Bar chốt 85.0%** và **Kết quả đo thực tế 70.0% (14/20 PASS)** trong `eval/evaluation_summary.md`.
- **Phân tích nguyên nhân & Bài học**:
  - *Nguyên nhân*: Nhóm tôi cố tình thiết kế một bộ **Hard Benchmark** (nhiều case mâu thuẫn phức tạp như CNF-03 và CNF-05). Kết quả lượt 1 chỉ đạt 55%, lượt 2 đạt 70%. Mặc dù chưa đạt thanh Quality Bar 85%, nhóm quyết định giữ nguyên báo cáo 70% trung thực chứ không giảm độ khó của Golden Set để lấy số đẹp.
  - *Bài học kinh nghiệm*: Kiểm thử sản phẩm AI không phải là "làm đẹp báo cáo" mà là công cụ chỉ ra điểm yếu thực sự của hệ thống. Nhờ báo cáo 70% trung thực, nhóm mới xác định được chính xác Failure chính nằm ở khâu Xử lý mâu thuẫn (40%) để đề xuất giải pháp Vector DB cho tuần kế tiếp.

### 3.4. Trả lời trực tiếp cho phần mình phụ trách

> *"Tôi phụ trách **Khung kiểm thử Eval (`eval/`) và User Validation (`validation/`)**. Sâu bên trong: Tôi thiết kế `golden_set.json` gồm 20 cases có cấu trúc JSON định nghĩa sẵn `expect_pass_keywords`. Script `run_eval_discord.py` sẽ nạp dữ liệu test, gửi tới bot, sau đó dùng thuật toán string matching & semantic check để đánh giá PASS/FAIL tự động, xuất ra file CSV và Markdown báo cáo minh bạch từng mốc chạy."*

---

# 4. BỘ CÂU HỎI & TRẢ LỜI CỐT LÕI CHO CẢ NHÓM (AUDIT Q&A)

### ❓ Q1: "Augment hay Automate — vì sao?"

> **Trả lời**: Sản phẩm thuộc kiến trúc **Conditional Automation (Tự động hóa có điều kiện)** nghiêng về **Augmentation (Bổ trợ con người)**.
>
> - **Lý do theo Cost-of-error**:
>   - Khi thông báo rõ ràng, đơn nhất: AI tự động hóa 100% việc gom nhóm và trích xuất (tiết kiệm 217 giờ/ngày toàn khóa). Cost-of-error thấp.
>   - Khi có đính chính mâu thuẫn mốc giờ (Conflict) hoặc thiếu thông tin mã môn quy định: **Cost-of-error rất đắt** — nếu AI tự động chốt một mốc sai, học viên sẽ bị nộp bài trễ hạn và trừ 10-20% điểm.
>   - Hành vi AI: AI **không tự ý quyết định hay phán đoán vô căn cứ**, mà trả về đối chiếu cả 2 mốc đính chính kèm timestamp/kênh nguồn, hoặc hiển thị cảnh báo *"Cần TA xác minh"* để con người (TA/Học viên) ra quyết định cuối (tuân thủ nguyên tắc **HAX G10** & **PAIR Graceful Failure**).

### ❓ Q2: "Failure nguy hiểm nhất?"

> **Trả lời**: Failure nguy hiểm nhất qua số liệu đo lường thực tế là **"Conflicting Announcement Misresolution" (Nhầm lẫn hoặc bỏ sót mốc đính chính khi có thông báo xung đột)**.
>
> - **Dữ liệu thực tế**:
>   - Hạng mục Security (Prompt Injection): Nhóm đã xử lý triệt để bằng **Pre-Guardrail 0ms**, đạt **PASS 100% (5/5 cases)**.
>   - Hạng mục Conflict Resolution (Xử lý mâu thuẫn): Đây là **Failure thực tế còn tồn tại**. Trên bộ Golden Set 20 cases, hạng mục này chỉ đạt **40.0% PASS (2/5 cases)**.
>   - Minh chứng (Case CNF-03/04): Khi chatlog chứa tin đồn hoãn deadline từ học viên và tin khẳng định từ BTC nhưng thiếu mã Token `BTC-VERIFIED`, LLM bị quá tải ngữ cảnh và bỏ sót việc tổng hợp ma trận.
>   - Nhóm công khai báo cáo chỉ số 70% (chưa đạt bar 85%) một cách trung thực chứ không giảm độ khó của Golden Set để lấy số đẹp, làm tiền đề bổ sung Vector DB ChromaDB ở tuần tiếp theo.

- **Thành viên 1 — Nguyễn Quang Huy (Leader)**: Spec Risks §5-§6 (4 lớp chỗ khó & 8 kịch bản rủi ro), Slide pitch 6 trang theo luật *"không bằng chứng thì không có slide"*, README.md.
- **Thành viên 2 — Nguyễn Minh Quân (AI Dev)**: Codebase Architecture (Pre-Guardrail 0ms chống Injection + LLM Summarizer 5 danh mục + Streamlit Web UI & Discord Bot Simulator UI).
- **Thành viên 3 — Trần Gia Thế**: Eval Golden Set 20 cases + Script `run_eval_discord.py` tự động đo + Khảo sát định lượng n=43 học viên ngoài nhóm & feedback log 5 Willing Users.
