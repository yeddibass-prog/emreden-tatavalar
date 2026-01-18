import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from gtts import gTTS

# --- 🛰️ MASTER KEY (BURAYI UNUTMA) ---
# Kendi API anahtarını buraya hatasız yapıştır.
DEFAULT_API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(page_title="Emre Aras AI", layout="wide", page_icon="🧠")

# --- 🌑 DARK NEBULA UI DESIGN (PREMIUM CSS) ---
st.markdown("""
    <style>
    /* Gemini Stil Arka Plan ve Yazı Tipi */
    .stApp {
        background-color: #0b0d11;
        color: #e3e3e3;
        font-family: 'Google Sans', 'Inter', sans-serif;
    }

    /* Üst Header Konteynırı */
    .st-emotion-cache-1833z0 { /* Sidebar'ı daha zarif yapar */
        background-color: #111418 !important;
    }

    /* Ana Başlık Alanı */
    .main-hero {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(180deg, rgba(66, 133, 244, 0.1) 0%, rgba(11, 13, 17, 0) 100%);
        border-radius: 0 0 40px 40px;
        margin-bottom: 30px;
    }
    
    .main-logo {
        font-size: 48px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -1.5px;
        margin: 0;
    }

    /* Cam Kartlar */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* Giriş Kutuları */
    .stTextArea textarea {
        background-color: #1e2126 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 16px !important;
        color: #e3e3e3 !important;
        padding: 15px !important;
    }

    /* Aksiyon Butonları (Mavi Gradient) */
    .stButton>button {
        background: linear-gradient(90deg, #4285f4, #9b72f3);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        width: 100%;
        transition: 0.3s ease;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(66, 133, 244, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 VERİ YÖNETİMİ ---
USER_DB, LOG_DB = "users.csv", "logs.csv"
def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame({"username": ["emrearas"], "password": ["master123"], "role": ["admin"]}).to_csv(USER_DB, index=False)
    if not os.path.exists(LOG_DB):
        pd.DataFrame(columns=["timestamp", "user", "action", "content"]).to_csv(LOG_DB, index=False)

init_db()

# --- 🔐 GİRİŞ SİSTEMİ ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="main-hero"><h1 class="main-logo">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        u = st.text_input("Kullanıcı Adı")
        p = st.text_input("Şifre", type="password")
        if st.button("SİSTEME GİRİŞ"):
            users = pd.read_csv(USER_DB)
            if u in users['username'].values and str(p) == str(users[users['username']==u]['password'].values[0]):
                st.session_state.logged_in, st.session_state.user, st.session_state.role = True, u, users[users['username']==u]['role'].values[0]
                st.rerun()
            else: st.error("Hatalı bilgiler.")
    st.stop()

# --- 🔱 YAPAY ZEKA BAĞLANTISI ---
try:
    genai.configure(api_key=DEFAULT_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")

# --- 🖥️ ANA ARAYÜZ ---
st.markdown('<div class="main-hero"><h1 class="main-logo">Emre Aras AI</h1></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user.upper()}")
    st.caption(f"YETKİ: {st.session_state.role}")
    if st.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "admin":
        st.markdown("---")
        if st.checkbox("İşlem Kayıtlarını Göster"):
            st.dataframe(pd.read_csv(LOG_DB).tail(20), use_container_width=True)

# --- 🌌 MODÜLLER ---
tab1, tab2 = st.tabs(["💬 Akıllı Sohbet", "🎨 Görsel Üretim"])

with tab1:
    prompt = st.text_area("Size nasıl yardımcı olabilirim?", height=200, placeholder="Emrinizi buraya yazın...")
    if st.button("ANALİZ ET"):
        if prompt:
            with st.spinner("YZ Düşünüyor..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 🤖 Yanıt")
                    st.write(response.text)
                    
                    # Loglama
                    logs = pd.read_csv(LOG_DB)
                    new_log = pd.DataFrame({"timestamp": [datetime.now().strftime("%H:%M:%S")], "user": [st.session_state.user], "action": ["Sohbet"], "content": [prompt[:50]]})
                    pd.concat([logs, new_log]).to_csv(LOG_DB, index=False)
                except Exception as e:
                    st.error(f"YZ Hatası: {e}. API anahtarınızı kontrol edin.")

with tab2:
    img_q = st.text_input("Görsel Konsepti (Örn: Erzurum manzarası):")
    if st.button("GÖRSELİ OLUŞTUR"):
        with st.spinner("Görsel çiziliyor..."):
            url = f"https://pollinations.ai/p/{img_q.replace(' ', '_')}?width=1024&height=1024&model=flux"
            st.image(url, caption="Emre Aras AI Tarafından Üretildi")

st.markdown("<br><hr><center>© 2026 Emre Aras AI | Stratejik Yapay Zeka Çözümleri</center>", unsafe_allow_html=True)