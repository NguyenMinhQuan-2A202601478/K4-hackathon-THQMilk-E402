from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Fix UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "codebase"))

from codebase.config import init_env
from codebase.discord_loader import is_noise_message
from codebase.discord_summarizer import generate_daily_digest
from codebase.guardrail import DefenseInDepthGuardrail, RuleBasedFilter
from codebase.providers import make_provider

init_env()

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("⚠️ Thư viện discord.py chưa được cài đặt. Hãy chạy: pip install discord.py")
    discord = None


BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

# Vietnam Timezone offset (UTC+7)
ICT_TZ = timezone(timedelta(hours=7))

# Initialize Defense-in-Depth Guardrail Manager
guardrail_pipeline = DefenseInDepthGuardrail()

# Official Announcement Channels defined in system_prompt.md
OFFICIAL_CHANNELS_KEYWORDS = [
    "thông-báo-chung",
    "thông-báo",
    "lớp học - khóa 3",
    "lớp học - khóa 4",
    "khóa 3",
    "khóa 4",
    "g-06",
    "build",
]


def format_vietnam_time(dt: datetime) -> str:
    """Convert datetime (UTC) to Vietnam Local Time (UTC+7) formatted as HH:MM AM/PM DD/MM/YYYY."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    vn_time = dt.astimezone(ICT_TZ)
    hour = vn_time.hour
    period = "AM" if hour < 12 else "PM"
    return f"{vn_time.strftime('%H:%M')} {period} {vn_time.strftime('%d/%m/%Y')}"


def deduplicate_candidate_messages(live_channels_data: dict[str, list[dict]]) -> list[dict]:
    """Deduplicate messages with identical/near-identical content across multiple channels."""
    seen_contents: dict[str, dict] = {}
    deduped_list: list[dict] = []

    for full_channel_name, msgs in live_channels_data.items():
        for m in msgs:
            raw_content = m.get("content", "").strip()
            # Normalize whitespace for exact content comparison
            normalized_key = re.sub(r"\s+", " ", raw_content.lower())

            if normalized_key in seen_contents:
                existing = seen_contents[normalized_key]
                # Merge channel mention and jump URL if new
                if full_channel_name not in existing["all_channels"]:
                    existing["all_channels"].append(full_channel_name)
                    existing["all_jump_urls"].append(m.get("jump_url"))
            else:
                m_copy = dict(m)
                m_copy["all_channels"] = [full_channel_name]
                m_copy["all_jump_urls"] = [m.get("jump_url")]
                seen_contents[normalized_key] = m_copy
                deduped_list.append(m_copy)

    return deduped_list


async def fetch_live_discord_messages(guild: discord.Guild) -> dict[str, list[dict]]:
    """STAGE 2: RULE-BASED DATA FILTERING - Fetch candidate live messages from official text channels with direct message jump URLs."""
    live_channels_data: dict[str, list[dict]] = {}
    
    # Collect text channels and active threads from the guild safely.
    all_channels = list(getattr(guild, "text_channels", []) or [])
    try:
        all_channels.extend(getattr(guild, "threads", []) or [])
    except Exception:
        pass

    print(f"🔍 SCANNING {len(all_channels)} CHANNELS & THREADS ON SERVER: '{guild.name}'...")

    for channel in all_channels:
        try:
            # Check Bot permissions on this channel (handles both view_channel and read_messages)
            perms = channel.permissions_for(guild.me)
            can_view = getattr(perms, "view_channel", None)
            if can_view is None:
                can_view = getattr(perms, "read_messages", False)
            can_read_history = getattr(perms, "read_message_history", False)

            if not can_view or not can_read_history:
                missing = []
                if not can_view:
                    missing.append("View Channel")
                if not can_read_history:
                    missing.append("Read Message History")
                print(f"⚠️ [PERMISSION DENIED] Bot lacks {', '.join(missing)} for #{channel.name}")
                continue

            cat_name = channel.category.name if getattr(channel, "category", None) else ""
            ch_mention = getattr(channel, "mention", f"#{channel.name}")
            full_channel_name = f"[{cat_name}] {ch_mention}" if cat_name else ch_mention
            ch_raw_name = f"[{cat_name}] #{channel.name}" if cat_name else f"#{channel.name}"

            channel_msgs = []
            async for msg in channel.history(limit=100):
                if getattr(msg.author, "bot", False):
                    continue
                content = (msg.content or "").strip()
                if not content:
                    continue

                author_name = getattr(msg.author, "name", "") or ""
                author_display_name = getattr(msg.author, "display_name", None) or author_name
                
                # Direct Message Jump URL
                jump_url = getattr(msg, "jump_url", f"https://discord.com/channels/{guild.id}/{channel.id}/{msg.id}")

                msg_dict = {
                    "author": {"nickname": author_display_name, "name": author_name},
                    "content": content
                }
                
                # Rule-Based Filter Check (Rejects student questions, keeps official notices)
                if RuleBasedFilter.is_candidate(msg_dict, ch_raw_name):
                    time_str = format_vietnam_time(msg.created_at)
                    channel_msgs.append({
                        "id": str(msg.id),
                        "timestamp": time_str,
                        "author": author_display_name,
                        "content": content,
                        "jump_url": jump_url,
                        "full_channel_name": full_channel_name,
                        "is_candidate": True,
                    })

            if channel_msgs:
                print(f"   ✅ '{full_channel_name}': Found {len(channel_msgs)} candidate messages.")
                live_channels_data[full_channel_name] = channel_msgs
            else:
                print(f"   ℹ️ '{full_channel_name}': 0 candidate messages.")

        except Exception as exc:
            print(f"⚠️ Could not fetch history for channel #{channel.name}: {exc}")
                
    return live_channels_data


def create_bot():
    if not discord:
        raise RuntimeError("discord.py is not installed. Run `pip install discord.py`")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    intents.guilds = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print("=" * 75)
        print(f"🤖 DISCORD BOT LIVE ONLINE: {bot.user.name} (ID: {bot.user.id})")
        print("🛡️ ĐÃ CẬP NHẬT THUẬT TOÁN KHỚP MỐC GIỜ HOÀN HẢO CHÓ CHO LỚP HỌC - KHÓA 3!")
        print("=" * 75)

    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        content = message.content or ""

        # Check if Bot is mentioned (@bot_agent)
        is_mentioned = (
            bot.user in message.mentions
            or any(m.id == bot.user.id for m in message.mentions)
            or f"<@{bot.user.id}>" in content
            or f"<@!{bot.user.id}>" in content
        )

        if is_mentioned:
            clean_question = content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

            # STAGE 1: PRE-GUARDRAIL (Input safety & strict scope partitioning firewall)
            pre_res = guardrail_pipeline.process_input(clean_question)

            if not pre_res.is_safe:
                print(f"🛡️ Pre-Guardrail Intercepted [{pre_res.reason}]: \"{clean_question}\"")
                await message.channel.send(pre_res.output_text)
                return

            # STAGE 2: RULE-BASED DATA FILTERING
            async with message.channel.typing():
                try:
                    if not message.guild:
                        await message.channel.send("⚠️ Vui lòng gõ câu hỏi trong Server Discord để Agent có thể quét tin nhắn!")
                        return

                    live_data = await fetch_live_discord_messages(message.guild)

                    if not live_data or all(len(msgs) == 0 for msgs in live_data.values()):
                        await message.channel.send("📢 **Hiện tại trên Server Discord chưa có tin nhắn thông báo nào được ghi nhận.**\n\n*(Lưu ý: Hãy chắc chắn Bot có quyền View Channel / Read Message History trong kênh mới tạo nhé!)*")
                        return

                    # DEDUPLICATE MESSAGES ACROSS CHANNELS
                    deduped_messages = deduplicate_candidate_messages(live_data)
                    print(f"🧹 [DEDUPLICATION] Deduplicated candidate messages count: {len(deduped_messages)}")

                    all_source_msgs = []
                    context_snippets = []
                    for m in deduped_messages:
                        all_source_msgs.append(m)
                        channels_str = ", ".join(m.get("all_channels", []))
                        links_str = " | ".join([f"[Xem tin nhắn gốc]({u})" for u in m.get("all_jump_urls", []) if u])
                        snippet = (
                            f"KÊNH NGUỒN: {channels_str}\n"
                            f"LINK TIN NHẮN GỐC: {links_str}\n"
                            f"NGƯỜI GỬI: {m.get('author')}\n"
                            f"THỜI GIAN: {m.get('timestamp')}\n"
                            f"NỘI DUNG: {m.get('content')}"
                        )
                        context_snippets.append(snippet)

                    # RELEVANCE PRIORITY SORTING: Channel name & exact keyword matching boost
                    query_keywords = [w.lower() for w in clean_question.split() if len(w) >= 2]
                    
                    def snippet_relevance(snippet: str) -> int:
                        score = 0
                        snip_lower = snippet.lower()

                        # Priority match for specific requested channel like "khóa 3" / "khóa 4"
                        if "khóa 3" in clean_question.lower() or "khoá 3" in clean_question.lower() or "k3" in clean_question.lower():
                            if "khóa 3" in snip_lower or "khoá 3" in snip_lower or "k3" in snip_lower:
                                score += 150
                        
                        if "khóa 4" in clean_question.lower() or "khoá 4" in clean_question.lower() or "k4" in clean_question.lower():
                            if "khóa 4" in snip_lower or "khoá 4" in snip_lower or "k4" in snip_lower:
                                score += 150

                        # General Official channels priority check matching system_prompt.md
                        if any(official in snip_lower for official in OFFICIAL_CHANNELS_KEYWORDS):
                            score += 80

                        # Heavy penalty for test-case and general chat channels
                        if "test-case" in snip_lower or "test" in snip_lower or "chitchat" in snip_lower:
                            score -= 200

                        for kw in query_keywords:
                            if kw in snip_lower:
                                score += 10
                        return score

                    sorted_snippets = sorted(context_snippets, key=snippet_relevance, reverse=True)
                    # Filter out snippets with negative score (test channels)
                    valid_snippets = [s for s in sorted_snippets if snippet_relevance(s) > -30]
                    if not valid_snippets:
                        valid_snippets = sorted_snippets

                    formatted_data = "\n\n====================\n\n".join(valid_snippets[:50])

                    # DYNAMIC REAL-TIME TEMPORAL CONTEXT WITH HOURLY TIME SLOTS
                    now_vn = datetime.now(ICT_TZ)
                    today_str = now_vn.strftime("%d/%m/%Y")
                    yesterday_vn = now_vn - timedelta(days=1)
                    yesterday_str = yesterday_vn.strftime("%d/%m/%Y")
                    current_time_str = format_vietnam_time(now_vn)

                    # STAGE 3: LLM REASONING (Strict Deduplication, Version Matching, Time Ranges, Domain Boundary)
                    provider = make_provider("openai")
                    
                    system_prompt = f"""You are the Senior Discord Notice Agent, a strict administrative assistant for a student learning community.

REAL-TIME TEMPORAL CONTEXT & HOURLY TIME SLOTS:
- CURRENT TIME (Vietnam Local Time UTC+7): {current_time_str}
- TODAY'S DATE: {today_str}
- YESTERDAY'S DATE: {yesterday_str}

CRITICAL HOURLY TIME SLOT MATCHING MANDATE:
1. "lúc 12 giờ" or "12h" means the 12 o'clock hour slot (from 12:00 PM to 12:59 PM for noon, or 12:00 AM to 12:59 AM for midnight).
2. If messages in the requested channel exist between 12:00 PM - 12:59 PM (e.g. 12:03 PM, 12:15 PM, 12:50 PM), YOU MUST SUMMARIZE THEM! DO NOT state that no announcements exist if messages exist in that hour slot!
3. ONLY state "Hiện tại hệ thống chưa ghi nhận thông báo nào trong khoảng thời gian từ 12:00 đến 12:59 ngày DD/MM/YYYY." IF NO MESSAGES AT ALL exist in that hour slot!

STRICT CHANNEL MATCHING MANDATE:
- If the user specifically asks for announcements in "LỚP HỌC - KHÓA 3", inspect the RETRIEVED DISCORD MESSAGES for KÊNH NGUỒN containing "LỚP HỌC - KHÓA 3" or "KHÓA 3" and summarize their exact content!

STRICT DEDUPLICATION MANDATE:
- MERGE DUPLICATE ANNOUNCEMENTS across channels into ONE SINGLE CARD BLOCK. List all source channels together under "Kênh nguồn".

EXACT HEADER TEMPLATE FOR VIETNAMESE:
📌 **[Tiêu đề thông báo]**
- 📍 **Kênh nguồn**: `[Danh mục]` <#channel_id> | 🔗 [Xem tin nhắn gốc](LINK_TIN_NHẮN_GỐC) | **Thời gian**: HH:MM AM/PM DD/MM/YYYY
- 📝 **Tóm tắt nội dung**: ...
- 🔗 **Link & Thông tin tham gia**: [Tên Link](url) | **Meeting ID**: ... | **Passcode**: ...
- ⚠️ **Quy định quan trọng**: ...

CRITICAL CARD STRUCTURE:
1. ONE EVENT = ONE INDIVIDUAL CARD BLOCK.
2. Rules section MUST be a bullet point INSIDE the card.
3. Separate distinct card blocks with blank lines.
"""

                    user_prompt = f"### DISCORD MESSAGES DATA:\n\n{formatted_data}\n\n### USER QUESTION:\n{clean_question}"

                    print(f"\n🧠 [AI REASONING] Processing prompt for query: '{clean_question}' (Today: {today_str}, Yesterday: {yesterday_str})...")
                    resp = provider.complete(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        temperature=0.0,
                    )

                    raw_output = resp.text or "Hiện tại hệ thống chưa ghi nhận thông báo nào trong khung giờ này."
                    print(f"🤖 [AI RAW OUTPUT]:\n{raw_output}\n")

                    # STAGE 4: POST-GUARDRAIL
                    final_safe_output = guardrail_pipeline.verify_llm_output(raw_output, all_source_msgs)

                    if len(final_safe_output) <= 2000:
                        await message.channel.send(final_safe_output)
                    else:
                        parts = final_safe_output.split("\n📌 ")
                        await message.channel.send(parts[0][:1990])
                        for part in parts[1:]:
                            await message.channel.send(f"📌 {part}"[:1990])

                except Exception as exc:
                    print(f"❌ Error during live Q&A: {exc}")
                    await message.channel.send(f"❌ Có lỗi khi đọc tin nhắn từ Server: {exc}")
            return

        await bot.process_commands(message)

    @bot.command(name="summary", help="Tóm tắt thông báo thực tế trên Server Discord")
    async def summary_command(ctx):
        if not ctx.guild:
            await ctx.send("⚠️ Lệnh `!summary` cần được chạy trong Server Discord.")
            return

        await ctx.send("🔍 **Agent đang quét tin nhắn thực tế trực tiếp từ các kênh trong Server Discord...**")
        live_data = await fetch_live_discord_messages(ctx.guild)

        if not live_data or all(len(msgs) == 0 for msgs in live_data.values()):
            await ctx.send("📢 **Hiện tại trong Server Discord chưa có bất kỳ tin nhắn thông báo nào.**")
            return

        digest_md = generate_daily_digest(live_data, model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

        if len(digest_md) <= 2000:
            await ctx.send(digest_md)
        else:
            sections = digest_md.split("\n## ")
            await ctx.send(sections[0])
            for sec in sections[1:]:
                await ctx.send(f"## {sec}"[:1990])

    @bot.command(name="ping", help="Kiểm tra độ trễ Bot")
    async def ping_command(ctx):
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Độ trễ kết nối Bot: `{latency}ms`")

    return bot


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ LỖI: Chưa cài đặt DISCORD_BOT_TOKEN trong file .env!")
        sys.exit(1)

    bot_app = create_bot()
    bot_app.run(BOT_TOKEN)
