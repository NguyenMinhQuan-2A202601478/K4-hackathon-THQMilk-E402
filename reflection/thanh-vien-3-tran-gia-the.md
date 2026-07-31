# REFLECTION CÁ NHÂN — THÀNH VIÊN 3
**Họ và tên**: Trần Gia Thế  
**Mã học viên**: `2A202601062`  
**Vai trò trong nhóm**: Eval & User Validation Lead (Nhóm THQMilk · Zone E402)  
**Phân công phụ trách chính**: `eval/` (`golden_set.json`, `run_eval_discord.py`, `evaluation_result.csv`, `evaluation_summary.md`), `validation/` (`feedback_log.md`, `Khảo sát trải nghiệm sử dụng Discord.xlsx`), `spec.md` (§7 - Khung kiểm thử & Quality bar).

---

## 1. VAI TRÒ VÀ CÁC PHẦN VIỆC ĐÃ ĐẢM NHẬN
- **Đóng góp chính**: 
  1. Xây dựng **Bộ Golden Set 20 Test Cases (`eval/golden_set.json`)** phủ đủ 4 hạng mục: Accuracy (5 cases), Security (5 cases), Formatting (5 cases) và Conflict Resolution (5 cases). Trong đó có 10 cases trích xuất trực tiếp từ chatlog Discord thật.
  2. Viết script tự động đánh giá **`run_eval_discord.py`** để đo lường đầu ra AI với các `expect_pass_keywords`, tự động tổng hợp bảng kết quả `evaluation_result.csv` và `evaluation_summary.md`.
  3. Xây dựng tài liệu **Khảo sát định lượng n = 43 học viên ngoài nhóm** tại [validation/feedback_log.md](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/validation/feedback_log.md) và thu thập feedback log từ 5 Willing Users.
  4. Viết §7 trong `spec.md` chốt Quality Bar (≥85.0% Overall Accuracy, 100% SEC PASS) và ghi nhận kết quả đo lường 70.0% một cách trung thực.

---

## 2. AI ĐÃ HỖ TRỢ NHƯ THẾ NÀO TRONG QUÁ TRÌNH LÀM VIỆC?
- **Sử dụng AI cho công việc Kiểm thử & Validation**:
  - Sử dụng AI để sinh các trường hợp adversarial test (Prompt Injection, tin đồn hoãn deadline giả mạo) phục vụ xây dựng Golden Set khó.
  - Dùng AI hỗ trợ viết script Python `run_eval_discord.py` tính toán tỷ lệ % Pass/Fail theo từng hạng mục và xuất dữ liệu thống kê CSV tự động.
  - Dùng AI phân tích 43 câu trả lời tự luận trong file khảo sát Excel để rút ra các trích dẫn nguyên văn (Direct Quotes) về mong muốn của học viên.

---

## 3. BÀI HỌC RÚT RA TỪ CASE FAIL CỦA CHÍNH NHÓM
- **Case Fail cụ thể**: Sự chênh lệch giữa **Quality Bar chốt 85.0%** và **Kết quả đo thực tế 70.0% (14/20 PASS)** trong `eval/evaluation_summary.md`.
- **Phân tích nguyên nhân & Bài học**:
  - *Nguyên nhân*: Nhóm tôi cố tình thiết kế một bộ **Hard Benchmark** (nhiều case mâu thuẫn phức tạp như CNF-03 và CNF-05). Kết quả lượt 1 chỉ đạt 55%, lượt 2 đạt 70%. Mặc dù chưa đạt thanh Quality Bar 85%, nhóm quyết định giữ nguyên báo cáo 70% trung thực chứ không giảm độ khó của Golden Set để lấy số đẹp.
  - *Bài học kinh nghiệm*: Kiểm thử sản phẩm AI không phải là "làm đẹp báo cáo" mà là công cụ chỉ ra điểm yếu thực sự của hệ thống. Nhờ báo cáo 70% trung thực, nhóm mới xác định được chính xác Failure chính nằm ở khâu Xử lý mâu thuẫn (40%) để đề xuất giải pháp Vector DB cho tuần kế tiếp.

---

## 4. BỘ CÂU TRẢ LỜI TRỰC TIẾP CHO VÒNG KIỂM TRA CP5 / DEMO ROUND

### ❓ Câu 1: Augment hay Automate — Vì sao?
> **Trả lời**: Sản phẩm là **Conditional Automation (Tự động hóa có điều kiện)**.  
> - **Dữ liệu từ Validation**: 72.1% học viên gặp khó khăn vì quá tải thông báo. AI tự động hóa việc gom nhóm và trích xuất để tiết kiệm 217 giờ/ngày. Tuy nhiên, khảo sát cũng chỉ ra 100% học viên đòi hỏi "nguồn gốc rõ ràng". Khi có thông báo mơ hồ hoặc xung đột mốc thời gian (cost-of-error cao), AI phải đóng vai trò Augment — trình bày cả 2 mốc đính chính kèm timestamp để học viên/TA là người đưa ra quyết định cuối cùng.

### ❓ Câu 2: Failure nguy hiểm nhất là gì?
> **Trả lời**: Failure nguy hiểm nhất qua số liệu đo lường thực tế là **"Failure trong hạng mục Xử lý mâu thuẫn (Conflict Resolution)"**.  
> - Minh chứng con số: Trên bộ Golden Set 20 cases, trong khi Security đạt 100% (5/5) và Accuracy đạt 80% (4/5), thì hạng mục Conflict Resolution chỉ đạt **40.0% (2/5 PASS)**. Khi có 2 thông báo đính chính đá nhau, AI dễ bị nhầm mốc cũ hoặc bỏ sót quy định nhóm. Đây chính là nguyên nhân kéo điểm tổng của nhóm xuống 70% (chưa đạt bar 85%).

### ❓ Câu 3: Phần bạn làm là gì và cách hoạt động sâu bên trong?
> **Trả lời**: Tôi phụ trách **Khung kiểm thử Eval (`eval/`) và User Validation (`validation/`)**.  
> - Sâu bên trong: Tôi thiết kế `golden_set.json` gồm 20 cases có cấu trúc JSON định nghĩa sẵn `expect_pass_keywords`. Script `run_eval_discord.py` sẽ nạp dữ liệu test, gửi tới bot, sau đó dùng thuật toán string matching & semantic check để đánh giá PASS/FAIL tự động, xuất ra file CSV và Markdown báo cáo minh bạch từng mốc chạy.
