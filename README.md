# Mini Hackathon AI — Batch 03

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

- Thời lượng: **1,5 ngày** (một ngày build + một buổi demo)
- Nhóm: **4-5 người** · zone tối đa 5 nhóm · thi theo lớp

## Bắt đầu từ đâu?

1. Đọc **`01-de-bai.md`** để chọn hướng và hiểu tiêu chí.
2. Mở **`02-guide.md`** — hướng dẫn từng giai đoạn, đứng ở đâu đọc mục đó.
3. Viết spec theo **`03-template-ai-spec.md`** — deliverable trung tâm của cả sự kiện.
4. Đọc **`04-rubric.md`** ngay từ đầu — biết trước bài được chấm theo tiêu chí nào.

| File / thư mục           | Nội dung                                                                                                                                                       |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01-de-bai.md`           | Đề bài 3 hướng · 5 tiêu chí nghiệm thu · ràng buộc chung                                                                                            |
| `02-guide.md`            | Hướng dẫn 5 giai đoạn: khám phá → spec → build → đo & validate → demo                                                                               |
| `03-template-ai-spec.md` | Template AI Spec (nộp 23:59 ngày 1)                                                                                                                           |
| `04-rubric.md`           | Rubric 100 điểm (25 nộp checkpoint + 75 chấm bài) + checklist xác minh 6 mốc                                                                             |
| `data/`                  | Dữ liệu thật đã ẩn danh: chatlog VLearn tutor + 6 transcript bài giảng + 2 bộ slide bản hackathon — dùng để tìm bằng chứng và xây golden set |
| `tham-khao/`             | JTBD Playbook (PDF) + worksheet JTBD đầy đủ — đọc khi muốn đào sâu                                                                                   |

## Lịch — 6 mốc

| Mốc                                                                   | Khoá 3       | Khoá 4       |
| ---------------------------------------------------------------------- | ------------- | ------------- |
| Khai mạc + phát đề                                                 | 09:00 ngày 1 | 14:00 ngày 1 |
| CP1 · Chốt Canvas                                                    | 10:00 ngày 1 | 15:00 ngày 1 |
| CP2 · Show được thứ bấm được                                  | 12:00 ngày 1 | 17:00 ngày 1 |
| CP3 · AI chạy thật + đo lượt đầu                               | 16:00 ngày 1 | 10:30 ngày 2 |
| CP4 · Chốt tiến độ — spec nộp hạn cứng**23:59 ngày 1** | 17:30 ngày 1 | 12:00 ngày 2 |
| CP5 · Xác minh + validation + dry run                                | 09:00 ngày 2 | 14:00 ngày 2 |
| CP6 · Demo                                                            | 10:00 ngày 2 | 15:00 ngày 2 |

Mỗi mốc cần show gì và được xác minh thế nào: xem bảng trong `04-rubric.md`.

## Nộp bài

Một repo nhóm, cấu trúc như sau. Spec chốt lúc 23:59 ngày 1; bản hoàn chỉnh trước CP6.

```
repo/
├── README.md          ← thành viên (mã HV + tên) + phân công có tên từng phần
├── spec.md            ← AI Spec theo 03-template-ai-spec.md
├── demo-slides.pdf    ← slide 6 trang theo 02-guide.md §5.1
├── codebase/          ← prototype (ghi rõ phần nào mock)
├── eval/              ← golden set + bảng kết quả các lượt chạy
├── validation/        ← feedback log từ vòng user test
└── reflection/        ← mỗi người 1 file
```

### Bảng Phân Công Nhiệm Vụ Nhóm 3 Thành Viên (Nhóm THQMilk · Zone E402)

| Thành viên | Mã HV | Vai trò | Phụ trách File / Thư mục chính | File Reflection Cá Nhân | Nhiệm vụ chính & Trách nhiệm Demo |
|---|---|---|---|---|---|
| **Nguyễn Quang Huy** | `2A202601314` | **Spec Risks & Slide, Leader** | `spec.md` (§5-§6)<br>`demo-slides.pdf` / `demo-slides.md`<br>`README.md` | [reflection.md#1-reflection-cá-nhân--thành-viên-1-nguyễn-quang-huy](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/reflection.md#1-reflection-cá-nhân--thành-viên-1-nguyễn-quang-huy)<br>*(hoặc [reflection/thanh-vien-1-nguyen-quang-huy.md](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/reflection/thanh-vien-1-nguyen-quang-huy.md))* | • Viết §5 & §6 trong `spec.md` (4 lớp chỗ khó & 8 kịch bản rủi ro).<br>• Biên soạn Slide pitch 6 trang theo luật *"không bằng chứng thì không có slide"*.<br>• Thuyết trình Slide 1 & Slide 2 tại Demo Round. |
| **Nguyễn Minh Quân** | `2A202601478` | **AI Dev** | `codebase/`<br>(`guardrail.py`, `discord_bot.py`, `app.py`) | [reflection.md#2-reflection-cá-nhân--thành-viên-2-nguyễn-minh-quân](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/reflection.md#2-reflection-cá-nhân--thành-viên-2-nguyễn-minh-quân)<br>*(hoặc [reflection/thanh-vien-2-nguyen-minh-quan.md](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/reflection/thanh-vien-2-nguyen-minh-quan.md))* | • Xây dựng tầng Pre-Guardrail 0ms chống Injection & LLM Extractor 5 phần.<br>• Lập trình Streamlit Dashboard & Discord Bot Simulator UI.<br>• Trực tiếp chạy Demo Live 2 Cases & Thẻ Giám Khảo. |
| **Trần Gia Thế** | `2A202601062` | **Eval & User Validation Lead** | `eval/`<br>`validation/`<br>`spec.md` (§7) | [reflection.md#3-reflection-cá-nhân--thành-viên-3-trần-gia-thế](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/reflection.md#3-reflection-cá-nhân--thành-viên-3-trần-gia-thế)<br>*(hoặc [reflection/thanh-vien-3-tran-gia-the.md](file:///c:/Users/huyqu/Desktop/ai-thuc-chien/K4-hackathon-THQMilk-E402/reflection/thanh-vien-3-tran-gia-the.md))* | • Xây dựng Golden Set 20 cases & script `run_eval_discord.py` tự động đo.<br>• Thu thập log khảo sát n=43 & 5 Willing Users feedback.<br>• Thuyết trình Slide 4 (70% vs Bar 85%), Slide 5 & Slide 6. |

---

### 🛡️ Bộ Trả Lời 3 Câu Hỏi Cốt Lõi Vibe-Coding / Audit (Cả nhóm đã luyện tập):
1. **"Augment hay Automate — vì sao?"**: **Conditional Automation (Bổ trợ con người)**. Tự động hóa 100% khi thông báo rõ ràng (tiết kiệm 217h/ngày). Chuyển sang con người (Augment) khi có đính chính mâu thuẫn mốc giờ *(Cost-of-error rất đắt: trễ hạn nộp bài)* bằng cách xuất cả 2 mốc kèm Timestamp hoặc cảnh báo *"Cần TA xác minh"* (HAX G10 & PAIR Graceful Failure).
2. **"Failure nguy hiểm nhất?"**: **Conflicting Announcement Misresolution (Xử lý sai hoặc bỏ sót mốc đính chính khi có nhiều thông báo xung đột)**. Kết quả đo thực tế ở hạng mục này chỉ đạt **40.0% PASS (2/5 cases)**. Nhóm công khai trung thực chỉ số này trên Hard Benchmark để nâng cấp Vector DB (ChromaDB) ở tuần tiếp theo.
3. **"Phần bạn làm là gì?"**: Nguyễn Quang Huy phụ trách Spec Rủi ro & Slide pitch, Leader; Nguyễn Minh Quân phụ trách AI Dev (Codebase Architecture: Pre-Guardrail 0ms + LLM Summarizer + Streamlit/Discord UI); Trần Gia Thế phụ trách Eval Golden Set (20 cases) & User Validation Survey (n=43).


## Chấm điểm

Tổng **100 điểm = 25 điểm nộp checkpoint + 75 điểm chấm bài nộp**. Chi tiết từng ý điểm: `04-rubric.md`.

**25 điểm nộp — mỗi checkpoint 5 điểm (CP1-CP5):** nộp đúng hạn → 5 điểm · nộp muộn → 0 điểm cho mốc đó. Mỗi thành viên nộp riêng, cả nhóm dùng chung một link repo.

**75 điểm chấm — trên artifact trong repo, mỗi con điểm trỏ về một file:**

| Khối                                | Điểm | Chấm trên file nào                       |
| ------------------------------------ | ------ | ------------------------------------------- |
| R1 · Bằng chứng & impact          | 15     | `spec.md` §1-§2 + log khảo sát/mining |
| R2 · Lát cắt & thiết kế         | 15     | `spec.md` §4                             |
| R3 · Chỗ khó & kịch bản rủi ro | 11     | `spec.md` §5-§6                         |
| R4 · Kiểm thử                     | 15     | `spec.md` §7 + `eval/`                 |
| R5 · Prototype chạy được        | 8      | `codebase/` + demo                        |
| R6 · Validation với user           | 8      | `validation/`                             |
| R7 · Quy trình & repo              | 3      | cấu trúc repo                             |

Ba điều nên biết trước khi làm:

- Điểm dựa trên **chuỗi quyết định và bằng chứng**, không dựa trên mức độ hoành tráng của sản phẩm.
- Kết quả đo **ghi nhận trung thực** — kể cả khi không đạt mục tiêu nhóm tự đặt — vẫn được tính đủ điểm. Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính.
- Reflection cá nhân chấm riêng theo rubric của khoá. Điểm vòng demo, chấm chéo trong zone và thưởng thêm (nếu có) theo thể lệ công bố lúc khai mạc.

## Luật chung

1. Prototype có 3 mức **Sketch / Mock / Working** — mức nào cũng bắt buộc **≥1 lời gọi AI chạy thật**.
2. **Vibe-coding rule:** dùng AI để build thoải mái, nhưng không giải thích được phần có tên mình thì phần đó 0 điểm (kiểm tra tại CP5).
3. **Quality bar** chốt tại spec.md 23:59 ngày 1 và giữ nguyên sau đó.
4. Chỉ dùng dữ liệu trong `data/` hoặc dữ liệu giả tự sinh — không dùng dữ liệu thật của người thật. Không commit API key.
5. Tuân thủ **quy định bảo mật dữ liệu** bên dưới — đây là điều kiện để được cấp data.

## Bảo mật dữ liệu được cung cấp

Dữ liệu trong `data/` là dữ liệu thật của khoá học (đã ẩn danh), cấp riêng cho hackathon này. Khi nhận data, nhóm cam kết:

1. **Chỉ dùng trong phạm vi hackathon** — cho việc tìm bằng chứng, xây golden set và build prototype. Không dùng cho mục đích khác.
2. **Không chia sẻ ra ngoài khoá học** — không đăng lên mạng xã hội, không gửi cho người ngoài, không đưa vào bất kỳ dataset hay repo công khai nào.
3. **Không commit data pack vào repo nộp bài** — repo nhóm chỉ chứa trích dẫn ngắn để minh hoạ (vài dòng); golden set trích từ data ghi rõ mã đoạn/mã hội thoại thay vì dán nguyên văn dài.
4. **Cẩn trọng khi đưa data vào công cụ ngoài** — chỉ đưa phần tối thiểu cần cho việc đang làm; lưu ý API/công cụ free tier có thể dùng dữ liệu để huấn luyện (xem `02-guide.md` §3.4).
5. **Không cố suy ngược danh tính** từ dữ liệu đã ẩn danh ([học viên], mã U/C/T/M).
6. Sau sự kiện, **xoá các bản sao data pack** khỏi máy cá nhân và các công cụ đã upload nếu ban tổ chức yêu cầu.

Vi phạm được xử lý theo quy định của khoá và có thể ảnh hưởng trực tiếp đến điểm của nhóm.
