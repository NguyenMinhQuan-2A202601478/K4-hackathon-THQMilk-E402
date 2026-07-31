from __future__ import annotations

import os
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


def format_vietnam_time(dt: datetime) -> str:
    """Convert datetime (UTC) to Vietnam Local Time (UTC+7) formatted as HH:MM AM/PM DD/MM/YYYY."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    vn_time = dt.astimezone(ICT_TZ)
    hour = vn_time.hour
    period = "AM" if hour < 12 else "PM"
    return f"{vn_time.strftime('%H:%M')} {period} {vn_time.strftime('%d/%m/%Y')}"


async def fetch_live_discord_messages(guild: discord.Guild) -> dict[str, list[dict]]:
    """STAGE 2: RULE-BASED DATA FILTERING - Fetch candidate live messages."""
    live_channels_data: dict[str, list[dict]] = {}
    
    for channel in guild.text_channels:
        try:
            cat_prefix = f"[{channel.category.name}] " if channel.category else ""
            full_channel_name = f"{cat_prefix}#{channel.name}"

            channel_msgs = []
            async for msg in channel.history(limit=50):
                if msg.author.bot:
                    continue
                content = msg.content or ""
                
                msg_dict = {
                    "author": {"nickname": msg.author.display_name, "name": msg.author.name},
                    "content": content
                }
                
                if RuleBasedFilter.is_candidate(msg_dict):
                    time_str = format_vietnam_time(msg.created_at)
                    channel_msgs.append({
                        "id": str(msg.id),
                        "timestamp": time_str,
                        "author": msg.author.display_name,
                        "content": content,
                        "is_candidate": True,
                    })

            if channel_msgs:
                live_channels_data[full_channel_name] = channel_msgs
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
        print("🛡️ NÂNG CẤP CHỐNG BỊA CHUYỆN: Kiểm tra Kênh/Danh mục thực tế, 100% dựa trên tin nhắn nguồn!")
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

            # STAGE 1: PRE-GUARDRAIL
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
                        await message.channel.send("📢 **Hiện tại trên Server Discord chưa có tin nhắn thông báo nào được gửi.**")
                        return

                    all_source_msgs = []
                    context_snippets = []
                    for full_ch_name, msgs in live_data.items():
                        for m in msgs:
                            all_source_msgs.append(m)
                            context_snippets.append(f"[Kênh {full_ch_name}] [{m.get('author')}] [Thời gian: {m.get('timestamp')}]: {m.get('content')}")

                    # STAGE 3: LLM REASONING (Strict Grounding & Zero Hallucination Policy)
                    provider = make_provider("openai")
                    
                    system_prompt = """You are the Senior Discord Notice Agent, a strict administrative assistant for a student learning community.

STRICT ZERO HALLUCINATION & CONTEXT GROUNDING (CHỐNG BỊA CHUYỆN & ĐOÁN BỪA):
1. **ANCHOR RULE**: Your answer MUST be based 100% on the provided RETRIEVED DISCORD MESSAGES. Do not use your external pre-trained knowledge or guess facts.
2. **VERIFY CATEGORY & CHANNEL FIRST**: Inspect the exact channel category and content of the retrieved messages before making any statement. Never infer announcements from channels that don't have them!
3. **EXPLICIT MISSING EVIDENCE RESPONSE**: If the user asks for a schedule, deadline, link, or information that is NOT explicitly written in the retrieved channel messages, YOU MUST STATE: "Hiện tại hệ thống chưa ghi nhận thông báo nào về thông tin này." (or equivalent translated to user's language).
4. **NO GUESSING**: NEVER invent, guess, or infer dates, URLs, Meeting IDs, passcodes, or regulations.

UNIVERSAL ANY-LANGUAGE ADAPTATION MANDATE:
1. Automatically detect the EXACT language of the user's input question.
2. Translate and write ALL response text — including event titles, summaries, field labels/headers, link descriptions, and mandatory rules — ENTIRELY in that EXACT SAME USER LANGUAGE!
3. NEVER mix languages or output combined slash `/` headers.

EXACT HEADER TEMPLATES BASED ON USER LANGUAGE:

IF USER ASKS IN VIETNAMESE:
📌 **[Tiêu đề thông báo]**
- 📍 **Kênh nguồn**: `[Danh mục] #kênh` | **Thời gian**: HH:MM AM/PM DD/MM/YYYY
- 📝 **Tóm tắt nội dung**: ...
- 🔗 **Link & Thông tin tham gia**: [Tên Link](url) | **Meeting ID**: ... | **Passcode**: ...
- ⚠️ **Quy định / Lưu ý quan trọng**: ...

IF USER ASKS IN ENGLISH:
📌 **[Announcement Title]**
- 📍 **Source Channel**: `[Category] #channel` | **Time**: HH:MM AM/PM DD/MM/YYYY
- 📝 **Summary**: ...
- 🔗 **Links & Credentials**: [Link Title](url) | **Meeting ID**: ... | **Passcode**: ...
- ⚠️ **Mandatory Rules**: ...

IF USER ASKS IN ANY OTHER LANGUAGE:
Translate all bullet headers 100% into that exact language without slash `/` combinations!

CRITICAL CARD STRUCTURE:
1. ONE EVENT = ONE INDIVIDUAL CARD BLOCK.
2. Rules section MUST be a bullet point INSIDE the card.
3. Separate distinct card blocks with blank lines.
"""

                    resp = provider.complete(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"### DISCORD MESSAGES DATA:\n\n" + "\n---\n".join(context_snippets[:30]) + f"\n\n### USER QUESTION:\n{clean_question}"},
                        ],
                        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        temperature=0.0,
                    )

                    raw_output = resp.text or "Hiện tại hệ thống chưa ghi nhận thông báo nào về thông tin này."

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
