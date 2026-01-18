import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from gtts import gTTS

# --- 🛰️ MASTER CONFIG ---
DEFAULT_API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(page_title="Emre Aras AI", layout="wide", page_icon="💎")

# --- 🌑 PREMIUM DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    /* Gemini & Modern SaaS Estetiği */
    .stApp {
        background: radial-gradient(circle at top right, #111827, #000000, #020617);
        color: #f8fafc;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Modern Logo & Header */
    .brand-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 50px 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0) 100%);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 40px;
    }

    .brand-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        font-weight: 800;
        color: white;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
        margin-bottom: 15px;
    }

    .brand-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(to bottom, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphism Kartlar */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 30px;
        transition: 0.3s;
    }

    /* Modern Inputlar */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #fff !important;
        padding: 15px !important;
    }

    /* Apple Tarzı Butonlar */
    .stButton>button {
        background: #ffffff;
        color: #000000;
        border: none;
        border-radius: 100px;
        padding: 12px 40px;
        font-weight: 700;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: auto;
        display: block;
        margin: 10px auto;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        background: #f1f5f9;
        box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
    }

    /* Sidebar Gizleme ve Modernize Etme */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 VERİTABANI VE LOGLAMA ---
USER_DB, LOG_DB = "users.csv", "logs.csv"

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame({"username": ["emrearas"], "password": ["master123"], "role": ["admin"]}).to_csv(USER_DB, index=False)
    if not os.path.exists(LOG_DB):
        pd.DataFrame(columns=["timestamp", "user", "action", "content"]).to_csv(LOG_DB, index=False)

init_db()

def log_action(user, action, content):
    df = pd.read_csv(LOG_DB)
    new_log = pd.DataFrame({
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "user": [user],
        "action": [action],
        "content": [content[:150]]
    })
    pd.concat([df, new_log]).to_csv(LOG_DB, index=False)

# --- 🔐 LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="brand-container"><div class="brand-logo">EA</div><div class="brand-title">EMRE ARAS AI</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        u = st.text_input("Kullanıcı Adı")
        p = st.text_input("Şifre", type="password")
        if st.button("SİSTEMİ UYANDIR"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and str(p) == str(users[users['username']==u]['password'].values[0]):
                st.session_state.logged_in, st.session_state.user, st.session_state.role = True, u, users[users['username']==u]['role'].values[0]
                st.rerun()
            else: st.error("Erişim Reddedildi.")
    st.stop()

# --- 🔱 NEXUS OPERATIONAL INTERFACE ---
genai.configure(api_key=DEFAULT_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

st.markdown('<div class="brand-container"><div class="brand-logo">EA</div><div class="brand-title">EMRE ARAS AI</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 💠 {st.session_state.user.upper()}")
    st.caption(f"YETKİ: {st.session_state.role.upper()}")
    if st.button("GÜVENLİ ÇIKIŞ"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "admin":
        st.markdown("---")
        st.markdown("### ⚙️ YÖNETİM PANELİ")
        with st.expander("Kullanıcı Ekle"):
            nu = st.text_input("Yeni Kullanıcı")
            np = st.text_input("Yeni Şifre", type="password")
            nr = st.selectbox("Yetki", ["user", "admin"])
            if st.button("KAYDET"):
                udf = pd.read_csv(USER_DB)
                pd.concat([udf, pd.DataFrame({"username": [nu], "password": [np], "role": [nr]})]).to_csv(USER_DB, index=False)
                st.success("Kullanıcı eklendi.")
        
        if st.checkbox("İşlem Kayıtlarını İzle"):
            st.dataframe(pd.read_csv(LOG_DB).tail(50), use_container_width=True)

# --- 🌌 MODÜLLER ---
t1, t2, t3 = st.tabs(["🤖 STRATEJİK ANALİZ", "🎨 GENESIS ÜRETİM", "💻 TEKNİK LABORATUVAR"])

with t1:
    prompt = st.text_area("Yapay Zekaya bir talimat verin...", height=150)
    if st.button("ANALİZİ BAŞLAT"):
        with st.spinner("Nexus ağına bağlanılıyor..."):
            response = model.generate_content(prompt)
            st.markdown("### 🤖 Yanıt")
            st.write(response.text)
            log_action(st.session_state.user, "AI Sorgusu", prompt)

with t2:
    img_q = st.text_input("Görsel Konsepti:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("GÖRSELİ VAR ET"):
            url = f"https://pollinations.ai/p/{img_q.replace(' ', '_')}?width=1024&height=1024&model=flux"
            st.image(url, caption="EA AI Visual Asset")
            log_action(st.session_state.user, "Görsel Üretimi", img_q)
    with c2:
        if st.button("SESİ SENTEZLE"):
            tts = gTTS(text=img_q, lang='tr')
            fp = io.BytesIO(); tts.write_to_fp(fp); fp.seek(0)
            st.audio(fp)
            log_action(st.session_state.user, "Ses Sentezi", img_q)

with t3:
    tech_q = st.text_area("Teknik veri veya kod girişi:")
    if st.button("LABORATUVARI ÇALIŞTIR"):
        response = model.generate_content(f"Kıdemli mühendis olarak analiz et: {tech_q}")
        st.code(response.text)
        log_action(st.session_state.user, "Teknik Analiz", tech_q)

st.markdown("<br><p style='text-align: center; color: rgba(255,255,255,0.2); font-size: 11px;'>EMRE ARAS AI | NEXUS CORE | PRIVILEGED ACCESS ONLY</p>", unsafe_allow_html=True)