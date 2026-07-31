# REFLECTION CÁ NHÂN — THÀNH VIÊN 1
**Họ và tên**: Nguyễn Quang Huy  
**Mã học viên**: `2A202601314`  
**Vai trò trong nhóm**: Spec Risks & Slide, Leader (Nhóm THQMilk · Zone E402)  
**Phân công phụ trách chính**: `spec.md` (§5 - 4 lớp chỗ khó & §6 - 4 đường đi trải nghiệm), `demo-slides.pdf` / `demo-slides.md`, `README.md`.

---

## 1. VAI TRÒ VÀ CÁC PHẦN VIỆC ĐÃ ĐẢM NHẬN
- **Đóng góp chính**: 
  1. Thiết kế taxonomy **4 lớp chỗ khó** (① Nguồn sự thật, ② Mơ hồ/thiếu thông tin, ③ Ngoài ranh giới thẩm quyền, ④ Đặc thù domain) và xây dựng 8 kịch bản rủi ro/fallback chi tiết tại [spec.md:L109-L121](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/spec.md#L109-L121).
  2. Xây dựng **4 đường đi của trải nghiệm** (Happy path, Low-confidence, Failure/không căn cứ, User correction) trong spec và kiểm tra tính nhất quán với prototype.
  3. Biên soạn nội dung slide thuyết trình 6 trang (`demo-slides.pdf` / `demo-slides.md`) tuân thủ nghiêm ngặt **Luật "Không có bằng chứng thì không có slide"** — 100% slide đều có con số kiểm chứng được.
  4. Quản lý cấu trúc `README.md` và rà soát tiến độ nộp bài các mốc CP1 - CP5.

---

## 2. AI ĐÃ HỖ TRỢ NHƯ THẾ NÀO TRONG QUÁ TRÌNH LÀM VIỆC?
- **Sử dụng AI cho công việc Spec & Slide**:
  - Dùng AI Pair Programming (Gemini / Antigravity) để brainstorm và phân loại các tình huống edge-case của dữ liệu Discord vào đúng 4 lớp chỗ khó.
  - Sử dụng AI để kiểm tra đối chiếu (cross-check) giữa các con số trong `eval/evaluation_summary.md` và `validation/feedback_log.md` nhằm đảm bảo mọi claim trên slide thuyết trình đều có link nguồn kiểm chứng chuẩn xác.
  - AI hỗ trợ sinh cấu trúc slide Markdown gọn gàng, loại bỏ các diễn đạt mang tính slogan hay persona chung chung.

---

## 3. BÀI HỌC RÚT RA TỪ CASE FAIL CỦA CHÍNH NHÓM
- **Case Fail cụ thể**: Case **CNF-03** và **CNF-04** trong bộ test `eval/golden_set.json` (Hạng mục *Xử lý thông tin mâu thuẫn* chỉ đạt **40.0% PASS - 2/5 cases**).
- **Phân tích nguyên nhân & Bài học**:
  - *Nguyên nhân*: Khi viết spec ban đầu, tôi đã giả định LLM có thể tự động nhận biết tin đồn hoãn deadline và tự lọc mã `BTC-VERIFIED` chỉ bằng System Prompt chung. Tuy nhiên, kết quả kiểm thử thực tế cho thấy LLM bị quá tải khi xử lý nhiều thông báo từ nhiều kênh cùng lúc mà không có cơ chế phân cấp trọng số nguồn tin.
  - *Bài học kinh nghiệm*: Spec sản phẩm AI không được viết dựa trên "kỳ vọng lý tưởng" vào năng lực của LLM. Cần phải kiểm thử empirical thực tế, chấp nhận kết quả 70% chưa đạt bar 85% và đưa ra phương án kỹ thuật rõ ràng (như bổ sung Vector DB ChromaDB ở tuần tiếp theo) thay vì sửa số liệu hay giấu case lỗi.

---

## 4. BỘ CÂU TRẢ LỜI TRỰC TIẾP CHO VÒNG KIỂM TRA CP5 / DEMO ROUND

### ❓ Câu 1: Augment hay Automate — Vì sao?
> **Trả lời**: Sản phẩm thuộc dạng **Conditional Automation (Tự động hóa có điều kiện)** nghiêng về **Augmentation (Bổ trợ con người)**.  
> - **Lý do theo Cost-of-error**: Khi thông báo rõ ràng, AI tự động 100% việc trích xuất (tốn 30s thay vì 30p lội chat). Nhưng khi có mâu thuẫn mốc thời gian (gia hạn deadline cũ vs mới), **cost-of-error rất đắt** (học viên trễ hạn bị trừ 10-20% điểm). Khi đó, AI không tự phán đoán mà trả về bảng đối chiếu mốc đính chính kèm timestamp hoặc hiển thị cảnh báo *"Cần TA xác minh"* để con người ra quyết định cuối (tuân thủ nguyên tắc HAX G10 & PAIR Graceful Failure).

### ❓ Câu 2: Failure nguy hiểm nhất là gì?
> **Trả lời**: Failure nguy hiểm nhất là **"Conflicting Announcement Misresolution" (Xử lý sai hoặc bỏ sót thông báo đính chính khi mốc giờ bị xung đột)**.  
> - Nếu AI trích xuất nhầm mốc deadline cũ 17:00 thay vì mốc đính chính 23:59 mới nhất, hoặc tin vào tin đồn hoãn deadline chưa xác thực từ tài khoản giả mạo Admin, học viên sẽ bị nộp trễ bài. Nhóm đã công khai minh bạch kết quả đo hạng mục này chỉ đạt 40% (2/5 PASS) trên bộ Hard Benchmark để tập trung khắc phục ở phiên bản tiếp theo.

### ❓ Câu 3: Phần bạn làm là gì và cách hoạt động sâu bên trong?
> **Trả lời**: Tôi phụ trách **Thiết kế rủi ro (`spec.md` §5-§6) & Biên soạn Slide thuyết trình (`demo-slides.pdf`), Leader**.  
> - Sâu bên trong: Tôi xây dựng taxonomy 4 lớp chỗ khó ép AI tuân thủ ranh giới thẩm quyền (VD: lớp 3 - chặn Prompt Injection và đòi hỏi lộ API Key). Đồng thời, tôi thiết kế slide bám sát luật *"không bằng chứng thì không có slide"*, đảm bảo mọi con số (72.1% khó khăn, 217 giờ tiết kiệm, 70% accuracy) đều trỏ trực tiếp tới file dữ liệu nguồn trong repo.
