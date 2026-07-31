from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Tuple

from codebase.providers import make_provider


@dataclass
class GuardrailResult:
    is_safe: bool
    stage: str
    reason: str | None
    output_text: str | None


def detect_language(text: str) -> str:
    """Heuristic language detector (en vs vi vs other)."""
    en_words = ["what", "how", "when", "where", "can", "you", "do", "help", "ignore", "system", "please", "deadline", "summary"]
    text_lower = text.lower()
    words = text_lower.split()
    en_count = sum(1 for w in words if w in en_words)
    if en_count >= 1 or any(kw in text_lower for kw in ["what can you do", "help me", "who are you", "summary"]):
        return "en"
    return "vi"


class PreGuardrail:
    """
    STAGE 1: PRE-GUARDRAIL (Input Safety, Strict Scope Partitioning & Out-of-Domain Firewall)
    """
    @staticmethod
    def generate_universal_refusal(user_prompt: str, refusal_reason: str) -> str:
        """Generate empathetic refusal in EXACT same language as user_prompt."""
        user_lang = detect_language(user_prompt)
        try:
            provider = make_provider("openai")
            prompt = (
                f"User asked: \"{user_prompt}\"\n\n"
                f"Refusal/Context reason: {refusal_reason}\n\n"
                f"STRICT MANDATE:\n"
                f"- RESPOND 100% IN THE EXACT SAME LANGUAGE AS THE USER'S INPUT!\n"
                f"- If user asked in English, reply in English.\n"
                f"- If user asked in Vietnamese, reply in Vietnamese.\n"
                f"- Be warm, cheerful, and polite with an emoji (e.g. 🌸, 😅).\n"
                f"- Explain that you are strictly an Announcement Agent and ask a clarifying question.\n"
                f"- Keep it concise (2 sentences max)."
            )
            resp = provider.complete(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                temperature=0.0
            )
            if resp.text:
                return resp.text
        except Exception:
            pass

        if user_lang == "en":
            return (
                "Hi there! 🌸 Your question is a bit ambiguous. "
                "Are you looking for a **Zoom meeting link**, **GitHub repository link**, or **VLearn slide link**? Please clarify so I can help! 😊"
            )
        return (
            "Dạ câu hỏi của bạn nghe hơi ngắn và chưa rõ ý lắm ạ 😅! "
            "Bạn đang muốn tra cứu thông báo hay nội dung gì vậy ạ? Bạn nói rõ thêm một chút để mình hỗ trợ nhé! 🌸"
        )

    @classmethod
    def validate_input(cls, user_prompt: str) -> Tuple[bool, str | None, str | None]:
        if not user_prompt:
            return False, "empty_prompt", "Dạ xin lỗi bạn nha! 😅 Bạn chưa nhập nội dung câu hỏi ạ."

        clean_prompt = user_prompt.strip().lower()
        user_lang = detect_language(user_prompt)

        # 0A. AMBIGUOUS VAGUE LINK PATTERNS -> Tailored Link Clarification Response!
        vague_link_patterns = [
            r"^link (ở đâu|đâu|gì|nào)$",
            r"^(cho xin |xem |gửi |xin )?link$",
            r"^ở đâu$",
            r"^ở đâu vậy$",
            r"^nộp (bài )?ở đâu$",
        ]
        for pattern in vague_link_patterns:
            if re.search(pattern, clean_prompt):
                if user_lang == "en":
                    refusal = (
                        "Hi there! 🌸 Your question about links is a bit ambiguous. "
                        "Are you looking for a **Zoom meeting link**, **GitHub repository link**, or **VLearn slide link**? Please clarify so I can get you the right link! 😊"
                    )
                else:
                    refusal = (
                        "Dạ bạn cho mình hỏi bạn đang muốn xin **link Zoom học**, **link repo GitHub nộp bài** hay **link slide VLearn** vậy ạ? "
                        "Bạn nói rõ tên kênh hoặc chủ đề để mình tìm đúng link cho bạn nhé! 🌸"
                    )
                return False, "vague_link_clarification", refusal

        # 0B. AMBIGUOUS VAGUE SUMMARY PATTERNS -> Tailored Summary Clarification Response!
        vague_summary_patterns = [
            r"tóm tắt cái kia",
            r"tóm tắt cái đó",
            r"tóm tắt cái này",
            r"tóm tắt giúp cái kia",
        ]
        for pattern in vague_summary_patterns:
            if re.search(pattern, clean_prompt):
                if user_lang == "en":
                    refusal = (
                        "Hi there! 🌸 Could you please clarify which channel or announcement you want me to summarize? "
                        "Are you looking for **Cohort 3**, **Cohort 4**, or **Build Workshop** announcements? 😊"
                    )
                else:
                    refusal = (
                        "Dạ bạn cho mình hỏi 'cái kia' là bạn đang muốn tóm tắt **Thông báo Khóa 3**, **Thông báo Khóa 4** hay **Workshop Build Phase 1** vậy ạ? "
                        "Bạn nói rõ tên kênh để mình tóm tắt chính xác cho bạn nhé! 🌸"
                    )
                return False, "vague_summary_clarification", refusal

        # 0C. GENERAL AMBIGUOUS / VAGUE PATTERNS
        vague_general_patterns = [
            r"mấy cái lạ",
            r"quần áo",
            r"xyz",
            r"abc",
            r"bạn hiểu không",
            r"huh",
        ]
        for pattern in vague_general_patterns:
            if re.search(pattern, clean_prompt):
                if user_lang == "en":
                    refusal = (
                        "Your question seems a bit ambiguous! 😅 "
                        "Are you looking for **Zoom meeting links**, **assignment deadlines**, or **lecture slides**? Please clarify so I can help you! 🌸"
                    )
                else:
                    refusal = (
                        "Dạ câu hỏi của bạn nghe hơi lạ và chưa rõ ý lắm ạ 😅! "
                        "Ý bạn là bạn đang muốn tra cứu **Lịch họp Zoom**, **Hạn nộp bài tập** hay **Slide bài giảng** hôm nay vậy ạ? "
                        "Bạn nói rõ hơn chút để mình hỗ trợ bạn chính xác nhất nhé! 🌸"
                    )
                return False, "ambiguous_general_clarification", refusal

        # 1. Math / Calculations check (e.g. 1+1, 2*3, 10/2)
        if re.match(r"^[\d\s\+\-\*\/\%\(\)\.\=]+$", clean_prompt):
            refusal = cls.generate_universal_refusal(user_prompt, "User asked a math calculation. Explain you only summarize student class announcements.")
            return False, "math_calculation", refusal

        # 2. Strict Scope Partitioning: Block General Programming Theory & Out-of-Domain Academic Concepts
        theory_patterns = [
            r"(là gì|thế nào là|giải thích|hướng dẫn|nguyên lý|định nghĩa|khái niệm|dùng để làm gì) (về |cho tôi về )?(oop|fastapi|python|sql|html|css|javascript|code|thuật toán|cấu trúc dữ liệu|lập trình|kế thừa|đóng gói|đa hình|trừu tượng|database|rest api|docker|git|pydantic|react)",
            r"viết (code|script|hàm|chương trình|đoạn code)",
            r"giải (bài tập|đề thi|câu hỏi|đáp án)",
            r"what is (oop|fastapi|python|sql|programming|class|object|inheritance|polymorphism|docker|git)",
            r"explain (oop|fastapi|python|sql|code|algorithm|inheritance)",
            r"how to (code|program|write script|implement)",
        ]
        for pattern in theory_patterns:
            if re.search(pattern, clean_prompt):
                if user_lang == "en":
                    refusal = (
                        "Hi there! 🌸 I am strictly a Discord Announcement Assistant. "
                        "I am not authorized to answer general programming theory, coding tutorials, or academic concepts (like OOP, FastAPI, or writing scripts). "
                        "Feel free to ask me about class deadlines, Zoom meeting links, or submission rules! 😊"
                    )
                else:
                    refusal = (
                        "Dạ xin lỗi bạn nha 😅! Mình là Bot chuyên trách tra cứu **Thông báo học tập, Deadline, Lịch họp Zoom và Quy định**, "
                        "chứ không phải trợ giảng lý thuyết lập trình (như OOP, FastAPI) hay công cụ viết code hộ ạ.\n\n"
                        "Nếu bạn cần tra cứu hạn nộp bài tập OOP hay link Zoom học hôm nay, cứ hỏi mình nhé! 🌸"
                    )
                return False, "out_of_domain_theory", refusal

        # 3. Comprehensive Security Attacks / Prompt Injection / Sensitive Info Leak Prevention
        security_patterns = [
            r"lộ (mật khẩu|api key|token|thông tin mật|private key|dữ liệu cá nhân|secret|tài khoản)",
            r"reveal (api key|password|secret|token|private key|credentials|env)",
            r"show (me )?(the )?(api key|token|env|password|secret)",
            r"cho xem (file .env|api key|token|mật khẩu|chuỗi bí mật)",
            r"(show|reveal|display|print|cho xem|hiển thị) (your )?(system prompt|system instruction|hướng dẫn hệ thống|prompt gốc)",
            r"what are your (instructions|rules|system prompt)",
            r"ignore (all )?previous instructions",
            r"bỏ qua (tất cả )?hướng dẫn",
            r"system override",
            r"say 'hacked'",
            r"set deadline.*2099",
            r"bán tài khoản",
            r"netflix",
            r"tôi là (ta|giảng viên|admin) đây, (tất cả|không cần) nộp bài",
            r"i am ta, (all|no need to) submit",
            r"忽略(所有)?指令",
            r"olvida las instrucciones",
            r"vergiss die anweisungen",
            r"(lộ|tiết lộ|xem) (cccd|cmnd|số điện thoại|sđt|thẻ tín dụng|credit card|tài khoản ngân hàng)",
        ]
        for pattern in security_patterns:
            if re.search(pattern, clean_prompt):
                if user_lang == "en":
                    refusal = (
                        "🛡️ **Security Guardrail Warning**:\n"
                        "Sorry! 😅 Prompt injection or sensitive data leak attempt detected. "
                        "I cannot process this request to ensure system and data safety! 🌸"
                    )
                else:
                    refusal = (
                        "🛡️ **Cảnh báo Bảo mật Guardrail**:\n"
                        "Dạ xin lỗi bạn nha! 😅 Mình phát hiện câu lệnh có dấu hiệu tấn công prompt injection hoặc yêu cầu tiết lộ thông tin hệ thống nhạy cảm. "
                        "Để đảm bảo an toàn cho dữ liệu lớp học, mình không thể thực hiện câu lệnh này ạ! 🌸"
                    )
                return False, "security_attack", refusal

        # 4. Mismatched Intent: Asking to summarize "questions/chatter" instead of "announcements"
        question_summary_patterns = [
            r"tóm tắt (các )?câu hỏi",
            r"tóm tắt thắc mắc",
            r"tóm tắt thảo luận",
            r"summarize (the )?questions",
            r"summarize (the )?chat",
        ]
        for pattern in question_summary_patterns:
            if re.search(pattern, clean_prompt):
                if user_lang == "en":
                    refusal = (
                        "Hi! 😅 I'm designed to summarize **Class Announcements, Assignments, and Zoom Schedules** from official channels, not student chat questions. "
                        "Feel free to ask me about class deadlines or Zoom links! 🌸"
                    )
                else:
                    refusal = (
                        "Dạ xin lỗi bạn nha 😅! Hệ thống của mình được thiết kế chuyên trách đọc và tóm tắt các **Thông báo học tập, Bài tập, Lịch họp Zoom và Quy định** từ BTC/Giáo viên, "
                        "chứ không tóm tắt các câu hỏi thảo luận của học viên ạ.\n\n"
                        "Nếu bạn cần tra cứu hạn nộp bài hay lịch học Zoom hôm nay, cứ hỏi mình nhé! 🌸"
                    )
                return False, "mismatched_intent_questions", refusal

        # 5. General Off-Topic / Capability Queries
        capability_patterns = [
            r"đọc (được |cái )?đường link",
            r"bạn (có thể|có biết) làm (được )?gì",
            r"what (can|do) you do",
            r"who are you",
            r"bạn là ai",
            r"hôm nay ăn gì",
            r"viết (bài thơ|văn|kịch bản)",
            r"tell me a story",
            r"weather",
            r"thời tiết",
            r"chơi game",
        ]
        for pattern in capability_patterns:
            if re.search(pattern, clean_prompt):
                refusal = cls.generate_universal_refusal(user_prompt, "User asked what the bot can do or asked off-topic questions. Explain your scope is summarizing student class announcements.")
                return False, "off_topic", refusal

        # 6. Universal Scope Check: Must have announcement intent
        announcement_keywords = [
            "thông báo", "hạn", "nộp", "bài", "lịch", "zoom", "deadline", "quy định",
            "slide", "meeting", "workshop", "link", "tóm tắt", "hôm nay", "tuần này",
            "bài tập", "họp", "mentor", "code", "repo", "lab", "g01", "t001", "đề tài",
            "mô tả", "nội dung", "mấy giờ", "khi nào", "phòng", "kênh", "channel", "mới",
            "tìm", "cho", "lớp", "khóa", "k3", "k4", "xem", "tra cứu", "tin nhắn", "trưa", "sáng", "chiều", "tối",
            "summary", "announcement", "assignment", "schedule", "resource", "project",
            "notice", "tarea", "entrega", "résumé", "zusammenfassung", "通知", "課題"
        ]
        has_intent = any(kw in clean_prompt for kw in announcement_keywords)

        if not has_intent:
            refusal = cls.generate_universal_refusal(user_prompt, "Query is ambiguous or out of scope. Ask clarifying question or explain scope.")
            return False, "out_of_scope", refusal

        return True, None, None


class RuleBasedFilter:
    """STAGE 2: RULE-BASED DATA FILTER"""
    NOISE_PATTERNS = [
        r"^(hi|hello|cảm ơn|cam on|tks|thanks|dạ|da|ok|okay|thả tim|vâng|chuẩn|hay quá|👍|❤️|😃)$",
        r"^có 1 bạn quên sạc",
        r"^cho em hỏi",
        r"^alo",
        r"^bạn ơi",
    ]

    ANNOUNCEMENT_KEYWORDS = [
        "thông báo", "hạn", "nộp", "bài tập", "lịch", "zoom", "deadline", 
        "quy định", "bắt buộc", "slide", "slides", "codelab", "codelabs", 
        "link", "meeting", "workshop", "kick-off", "xác nhận", "nộp bài",
        "hạn cuối", "bài lab", "spec", "checkpoint", "cp1", "cp2", "cp3", "cp4", "cp5", "cp6",
        "announcement", "summary", "schedule", "assignment", "notice", "tarea", "通知"
    ]

    OFFICIAL_ROLES = ["lab coach", "coach", "btc", "teacher", "giảng viên", "trợ giảng", "admin"]

    USER_QUERY_PATTERNS = [
        r"<@!?\d+>",
        r"tóm tắt (các |các thông báo|thông báo)",
        r"có (thông báo|lịch|zoom) nào",
        r"cho (xin|mình xin|tôi xin)",
        r"hôm nay có (mấy|thông báo|gì)",
        r"là (bao nhiêu|gì)",
        r"khi nào",
        r"mấy giờ",
        r"passcode phòng zoom",
        r"hạn chót bài",
    ]

    @classmethod
    def is_noise(cls, text: str) -> bool:
        if not text or len(text.strip()) < 2:
            return True
        cleaned = text.strip().lower()
        return any(re.search(pat, cleaned) for pat in cls.NOISE_PATTERNS)

    @classmethod
    def is_candidate(cls, msg: dict[str, Any], channel_name: str = "") -> bool:
        content = (msg.get("content") or "").strip()
        if cls.is_noise(content):
            return False

        content_lower = content.lower()
        author = msg.get("author", {})
        nickname = (author.get("nickname") or "").lower() if isinstance(author, dict) else str(author).lower()
        roles = [r.get("name", "").lower() for r in author.get("roles", [])] if isinstance(author, dict) else []

        is_official_author = (
            any(role in cls.OFFICIAL_ROLES for role in roles)
            or any(kw in nickname for kw in ["coach", "btc", "teacher", "giảng viên", "trợ giảng", "admin"])
        )

        # REJECT STUDENT QUESTIONS/QUERY MESSAGES SENT IN CHAT CHANNELS
        is_user_query = any(re.search(pat, content_lower) for pat in cls.USER_QUERY_PATTERNS)
        if is_user_query and not is_official_author:
            return False

        # Any non-noise message in an announcement/class channel IS A CANDIDATE!
        ch_lower = channel_name.lower()
        if any(kw in ch_lower for kw in ["thông-báo", "thông báo", "announcement", "notice", "thong-bao", "thong bao"]):
            return True

        has_keyword = any(kw in content_lower for kw in cls.ANNOUNCEMENT_KEYWORDS)
        return is_official_author or has_keyword


class PostGuardrail:
    """STAGE 3: POST-GUARD (Evidence Grounding Verification)"""
    @staticmethod
    def verify_output(raw_llm_output: str, source_messages: list[dict[str, Any]]) -> Tuple[bool, str, str]:
        if not raw_llm_output or "Not enough evidence" in raw_llm_output and len(raw_llm_output) < 150:
            return True, "valid_empty", raw_llm_output

        verified_lines = []
        has_hallucination = False

        for line in raw_llm_output.splitlines():
            if "Evidence" in line or "Bằng chứng" in line:
                quote_match = re.search(r'"([^"]+)"', line) or re.search(r'“([^”]+)”', line)
                if quote_match:
                    quote = quote_match.group(1).lower().strip()
                    grounded = any(quote[:20] in (m.get("content", "") or "").lower() for m in source_messages)
                    if not grounded and len(source_messages) > 0:
                        has_hallucination = True
                        verified_lines.append("  - **Evidence**: \"Not enough evidence from source messages.\" [Post-Guard Verified]")
                        continue

            verified_lines.append(line)

        final_output = "\n".join(verified_lines)

        if has_hallucination:
            return True, "hallucination_corrected", final_output

        return True, "valid_grounded", final_output


class DefenseInDepthGuardrail:
    def __init__(self):
        self.pre_guard = PreGuardrail()
        self.rule_filter = RuleBasedFilter()
        self.post_guard = PostGuardrail()

    def process_input(self, user_prompt: str) -> GuardrailResult:
        is_safe, category, refusal = self.pre_guard.validate_input(user_prompt)
        if not is_safe:
            return GuardrailResult(
                is_safe=False,
                stage="pre_guard",
                reason=category,
                output_text=refusal
            )
        return GuardrailResult(is_safe=True, stage="passed", reason=None, output_text=None)

    def verify_llm_output(self, raw_llm_output: str, source_messages: list[dict[str, Any]]) -> str:
        _, _, safe_output = self.post_guard.verify_output(raw_llm_output, source_messages)
        return safe_output
