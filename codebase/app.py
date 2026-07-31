import json
from pathlib import Path
import sys

# Fix UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from config import init_env
from providers import make_provider
from tools.discord_loader.tool import load_and_group_messages
from tools.discord_summarizer.tool import generate_daily_digest

init_env()

st.set_page_config(
    page_title="Discord Important Announcement Summarizer Agent",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("⚙️ Cấu hình Discord Agent")
    provider_name = st.selectbox("LLM Provider", options=["openai", "gemini"], index=0)
    model_name = st.selectbox("Model", options=["gpt-4o-mini", "gpt-4o"], index=0)

st.title("🤖 Discord Daily Announcement Summarizer Agent")
st.caption("Agent tự động lọc nhiễu, quét thông báo quan trọng trong ngày từ các kênh gán nhãn (#thông-báo-chung, #thông-báo, #thông-báo-nhóm) và tổng hợp bản tin Daily Updates.")

if st.button("🚀 Bắt đầu quét & Tóm tắt Thông báo hôm nay", type="primary"):
    with st.status("🔍 Agent đang quét dữ liệu từ data/data-discord...", expanded=True) as status:
        st.write("📥 Loading & Parsing Discord Export Files...")
        ds = load_and_group_messages()
        st.write(f"✅ Đã tải: {ds.get('files_loaded', 0)} files ({ds.get('total_messages', 0)} tin nhắn gốc, {ds.get('candidate_count', 0)} ứng viên thông báo).")
        
        st.write("🤖 Gọi OpenAI API để phân loại & trích xuất...")
        digest_md = generate_daily_digest(ds.get("channels", {}), model_name=model_name)
        status.update(label="✅ Đã tổng hợp thành công!", state="complete", expanded=False)

    st.markdown("---")
    st.markdown(digest_md)
