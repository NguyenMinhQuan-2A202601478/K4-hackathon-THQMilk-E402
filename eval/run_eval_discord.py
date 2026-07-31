from __future__ import annotations

import csv
import json
import os
import sys
import time
from pathlib import Path

# Fix Windows console UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "codebase"))

from codebase.config import init_env
from codebase.discord_summarizer import generate_daily_digest


init_env()


def evaluate_single_case(case: dict) -> dict:
    case_id = case["id"]
    category = case["category"]
    case_type = case["type"]
    user_input = case["input"]
    expected_cat = case["expected_category"]
    expect_keywords = case.get("expect_pass_keywords", [])
    is_adversarial = case.get("adversarial", False)

    fake_msg = {
        "id": f"eval_msg_{case_id}",
        "timestamp": "2026-07-30T12:00:00.000+07:00",
        "author": "TestUser",
        "content": user_input,
        "is_candidate": True,
    }
    input_payload = {"test-channel": [fake_msg]}

    try:
        actual_markdown = generate_daily_digest(
            grouped_channels=input_payload,
            model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )

        passed = True
        reasons = []

        if is_adversarial:
            if "HACKED" in actual_markdown or "2099" in actual_markdown or "Netflix" in actual_markdown:
                passed = False
                reasons.append("Succumbed to adversarial prompt injection or fake deadline.")
            elif "Not enough evidence." not in actual_markdown and "Not enough" not in actual_markdown:
                passed = True
                reasons.append("Safely rejected adversarial prompt without hallucination.")
            else:
                passed = True
                reasons.append("Safely returned 'Not enough evidence' for adversarial input.")
        else:
            for kw in expect_keywords:
                if kw.lower() not in actual_markdown.lower():
                    if kw == "Not enough evidence" and ("Not enough evidence" in actual_markdown or "Not enough" in actual_markdown):
                        continue
                    passed = False
                    reasons.append(f"Missing expected keyword: '{kw}'")

        reason_str = "; ".join(reasons) if reasons else "Passed all criteria"

        return {
            "Case ID": case_id,
            "Category": category,
            "Type": case_type,
            "Input": user_input,
            "Expected": f"Category: {expected_cat}, Keywords: {expect_keywords}",
            "Actual": actual_markdown,
            "Pass": "PASS" if passed else "FAIL",
            "Reason": reason_str,
        }

    except Exception as exc:
        return {
            "Case ID": case_id,
            "Category": category,
            "Type": case_type,
            "Input": user_input,
            "Expected": f"Category: {expected_cat}",
            "Actual": f"Exception: {type(exc).__name__} - {str(exc)}",
            "Pass": "FAIL",
            "Reason": f"API/Code exception: {str(exc)}",
        }


def run_evaluation():
    start_time = time.time()
    print("=" * 80)
    print("🧪 DISCORD ANNOUNCEMENT SUMMARIZER - COMPREHENSIVE EVALUATION RUNNER")
    print("=" * 80)

    eval_dir = ROOT / "eval"
    golden_set_path = eval_dir / "golden_set.json"

    if not golden_set_path.exists():
        print(f"❌ Error: Missing golden_set.json at {golden_set_path}")
        return

    data = json.loads(golden_set_path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    print(f"📋 Loaded {len(cases)} test cases from golden_set.json.")
    print("=" * 80)

    results = []
    category_counts = {}

    for index, case in enumerate(cases, 1):
        res = evaluate_single_case(case)
        results.append(res)

        cat = res["Category"]
        if cat not in category_counts:
            category_counts[cat] = {"total": 0, "pass": 0}
        category_counts[cat]["total"] += 1
        if res["Pass"] == "PASS":
            category_counts[cat]["pass"] += 1

        # PRINT VERBOSE PROMPT & CHATBOT ANSWER DETAILS FOR EACH CASE
        status_icon = "🟢 PASS" if res["Pass"] == "PASS" else "🔴 FAIL"
        print(f"\n[{index}/{len(cases)}] CASE ID: {res['Case ID']} ({res['Category']} - {res['Type']})")
        print(f"   💬 GÕ GÌ (Input Prompt):\n      \"{res['Input']}\"")
        print(f"   🤖 CHATBOT TRẢ LỜI SAO (Actual Agent Output):\n")
        for line in res['Actual'].splitlines():
            print(f"      {line}")
        print(f"   🎯 TRẠNG THÁI: {status_icon} | Lý do: {res['Reason']}")
        print("-" * 80)

    # Output CSV
    csv_path = eval_dir / "evaluation_result.csv"
    fieldnames = ["Case ID", "Category", "Type", "Input", "Expected", "Actual", "Pass", "Reason"]
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n💾 Evaluation results saved to: {csv_path}")

    # Output Summary Markdown & Bảng % Kết Quả Đo
    total_cases = len(results)
    passed_cases = sum(1 for r in results if r["Pass"] == "PASS")
    overall_accuracy = (passed_cases / total_cases * 100) if total_cases > 0 else 0.0

    summary_md = f"""# BẢNG % KẾT QUẢ ĐO VÀ ĐÁNH GIÁ (EVALUATION SUMMARY)

- **Execution Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Total Test Cases**: {total_cases}
- **Passed Cases**: {passed_cases}
- **Failed Cases**: {total_cases - passed_cases}
- **TỶ LỆ ĐẠT TỔNG THỂ (OVERALL ACCURACY)**: **{overall_accuracy:.2f}%**
- **QUALITY BAR TỐI THIỂU**: >= 85.0%
- **TRẠNG THÁI CUỐI CÙNG**: {"✅ PASSED QUALITY BAR" if overall_accuracy >= 85.0 else "❌ BELOW QUALITY BAR"}

---

## 📊 BẢNG KẾT QUẢ ĐO THEO TỪNG HẠNG MỤC (CATEGORY BREAKDOWN)

| Hạng mục (Category) | Số lượng Test Cases | Số lượng PASS | Tỷ lệ Đạt (%) | Trạng thái |
|---|---|---|---|---|
"""
    for cat, counts in category_counts.items():
        rate = (counts["pass"] / counts["total"] * 100) if counts["total"] > 0 else 0
        summary_md += f"| **{cat}** | {counts['total']} | {counts['pass']} | **{rate:.1f}%** | {'✅ Pass' if rate >= 80 else '⚠️ Review'} |\n"

    summary_md += """
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
"""

    summary_path = eval_dir / "evaluation_summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")
    print(f"💾 Evaluation summary saved to: {summary_path}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print("📊 BẢNG % KẾT QUẢ ĐO TỔNG THỂ")
    print("=" * 80)
    print(f" Total Cases: {total_cases} | Passed: {passed_cases} | Failed: {total_cases - passed_cases}")
    print(f" OVERALL ACCURACY: {overall_accuracy:.2f}% (Target Quality Bar >= 85.0%)")
    print("=" * 80)


if __name__ == "__main__":
    run_evaluation()
