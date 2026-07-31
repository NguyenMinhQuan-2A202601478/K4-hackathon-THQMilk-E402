# BẢNG % KẾT QUẢ ĐO VÀ ĐÁNH GIÁ (EVALUATION SUMMARY)

- **Execution Date**: 2026-07-31 10:23:44
- **Total Test Cases**: 20
- **Passed Cases**: 14
- **Failed Cases**: 6
- **TỶ LỆ ĐẠT TỔNG THỂ (OVERALL ACCURACY)**: **70.00%**
- **QUALITY BAR TỐI THIỂU**: >= 85.0%
- **TRẠNG THÁI CUỐI CÙNG**: ❌ BELOW QUALITY BAR

---

## 📊 BẢNG KẾT QUẢ ĐO THEO TỪNG HẠNG MỤC (CATEGORY BREAKDOWN)

| Hạng mục (Category) | Số lượng Test Cases | Số lượng PASS | Tỷ lệ Đạt (%) | Trạng thái |
|---|---|---|---|---|
| **Độ chính xác có căn cứ** | 5 | 4 | **80.0%** | ✅ Pass |
| **Giữ đúng ranh giới thẩm quyền** | 5 | 5 | **100.0%** | ✅ Pass |
| **Định dạng độ dài** | 5 | 3 | **60.0%** | ⚠️ Review |
| **Xử lý thông tin mâu thuẫn** | 5 | 2 | **40.0%** | ⚠️ Review |

---

## 🔍 CHI TIẾT CÁC MÔ HÌNH LỖI (MAJOR FAILURE MODES)

1. **Adversarial Noise Infiltration (Prompt Injection / Tin giả)**: Các câu lệnh tấn công cố tình hạ gục AI hoặc gửi tin giả về deadline.
   - *Biện pháp*: Giới hạn Prompt nghiêm ngặt + Yêu cầu trích dẫn bằng chứng cụ thể.
2. **Conflicting Announcement Resolution (Xung đột mốc thời gian)**: Nhiều thông báo đính chính thời gian cho cùng 1 bài tập.
   - *Biện pháp*: Hiển thị cả 2 mốc thời gian kèm timestamp và kênh nguồn để người dùng đối chiếu.

---

## 🚀 ĐỀ XUẤT CẢI TIẾN CHO LƯỢT TIẾP THEO

1. **Channel Weighting**: Tăng trọng số điểm cho kênh chính thức `#thông-báo-chung` so với kênh chat nhóm.
2. **Vector DB Integration**: Tích hợp ChromaDB để tra cứu ngữ cảnh nhanh cho các dữ liệu thông báo cũ hơn 30 ngày.
3. **Auto Clarification Prompting**: Tự động đặt câu hỏi làm rõ với TA khi thông báo bị thiếu giờ nộp.
