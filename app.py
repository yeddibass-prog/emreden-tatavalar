import streamlit as st
import google.generativeai as genai
import io
from gtts import gTTS

# --- 🛰️ MASTER CONFIG (EMRE ARAS AI) ---
API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(page_title="EMRE ARAS AI", layout="wide", page_icon="🔱")

# --- 🌌 NEXUS TOTAL SUPREMACY UI (SİYAH TEMA) ---
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    .header-bar { text-align: center; padding: 30px; border-bottom: 1px solid #1e293b; margin-bottom: 20px; }
    .header-title { font-size: 40px; font-weight: 800; color: #ffffff; }
    .stButton>button { background: #ffffff !important; color: #000 !important; border-radius: 50px !important; font-weight: 700 !important; width: 100%; }
    [data-testid="stSidebar"] { background-color: #000 !important; border-right: 1px solid #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔱 AUTO-STABLE ENGINE (HATASIZ BAĞLANTI) ---
@st.cache_resource
def load_nexus_engine():
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except: return None

# --- 🔐 SESSION MANAGEMENT ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- 🔓 LOGIN (ENTER TUŞU AKTİF) ---
if not st.session_state.logged_in:
    st.markdown('<div class="header-bar"><h1 class="header-title">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.form("nexus_login_gate"):
            u = st.text_input("Kimlik", value="emrearas")
            p = st.text_input("Parola", type="password")
            if st.form_submit_button("SİSTEMİ BAŞLAT (Enter)"):
                if u == "emrearas" and p == "master123":
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Erişim Reddedildi.")
    st.stop()

# --- 🖥️ COMMAND HUB ---
st.markdown('<div class="header-bar"><h1 class="header-title">EMRE ARAS AI KARARGAHI</h1></div>', unsafe_allow_html=True)
engine = load_nexus_engine()

with st.sidebar:
    st.markdown("### 👤 EMRE ARAS")
    st.write("Status: **Operational**")
    st.write("Role: **Master Admin**")
    if st.button("Güvenli Çıkış"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    st.info("✓ Gemini 1.5 Active\n✓ Flux Vision\n✓ Nexus TTS\n✓ Enter Key Support")

# --- 🚀 MISSION CONTROL (4 MOTOR BİR ARADA) ---
t1, t2, t3, t4 = st.tabs(["💬 CHAT", "🎨 GÖRSEL", "💻 ANALİZ", "🔊 SES"])

with t1:
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]): st.markdown(chat["content"])
    if pr := st.chat_input("Mesajınızı yazın (Enter)..."):
        st.session_state.chat_history.append({"role": "user", "content": pr})
        with st.chat_message("user"): st.markdown(pr)
        with st.chat_message("assistant"):
            if engine:
                r = engine.generate_content(pr)
                st.markdown(r.text)
                st.session_state.chat_history.append({"role": "assistant", "content": r.text})

with t2:
    with st.form("img_engine"):
        prompt = st.text_input("Görsel Konsepti (Enter):")
        if st.form_submit_button("ÜRET"):
            st.image(f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&model=flux")

with t3:
    with st.form("analiz_lab"):
        code_input = st.text_area("Kod veya Veri (Enter):")
        if st.form_submit_button("ANALİZ ET"):
            if engine:
                res = engine.generate_content(f"Teknik analiz yap: {code_input}")
                st.code(res.text)

with t4:
    with st.form("voice_lab"):
        text_to_voice = st.text_area("Metni Sese Çevir (Enter):")
        if st.form_submit_button("SESLENDİR"):
            tts = gTTS(text=text_to_voice, lang='tr')
            b = io.BytesIO(); tts.write_to_fp(b); b.seek(0)
            st.audio(b)

st.markdown("<br><center>© 2026 EMRE ARAS AI | Master Control Center</center>", unsafe_allow_html=True)