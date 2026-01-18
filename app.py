import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from gtts import gTTS

# --- 🛰️ SİSTEM AYARLARI ---
# API Anahtarını buraya yapıştır
API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(
    page_title="Emre Aras AI | Nexus Pro",
    layout="wide",
    page_icon="🔱"
)

# --- 🌌 GÖRSELDEKİ MODERN ARAYÜZ (CSS) ---
st.markdown("""
    <style>
    /* Ana Tema: Derin Uzay Siyahı */
    .stApp {
        background-color: #05070a;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Üst Panel (Header) */
    .main-header {
        text-align: center;
        padding: 50px 0;
        background: linear-gradient(180deg, rgba(59, 130, 246, 0.08) 0%, rgba(5, 7, 10, 0) 100%);
        border-bottom: 1px solid #1e293b;
        margin-bottom: 30px;
    }
    
    .main-title {
        font-size: 50px;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Kartlar ve Giriş Alanları */
    .stChatInputContainer { padding: 20px !important; }
    .stTextArea textarea, .stTextInput input {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }

    /* Apple Tarzı Butonlar */
    .stButton>button {
        background: #ffffff !important;
        color: #020617 !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        font-weight: 700 !important;
        transition: 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }

    /* Sidebar Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid #1e293b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🔱 OTOMATİK MODEL SEÇİCİ (HATA SAVAR) ---
@st.cache_resource
def load_nexus_engine():
    try:
        genai.configure(api_key=API_KEY)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Hata vermemesi için çalışan en iyi modelleri sırayla dener
        for target in ['models/gemini-1.5-pro-latest', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if target in models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(models[0]) if models else None
    except:
        return None

# --- 💾 OTURUM YÖNETİMİ ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- 🔐 GİRİŞ EKRANI ---
if not st.session_state.logged_in:
    st.markdown('<div class="main-header"><h1 class="main-title">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1, 1])
    with login_col:
        u = st.text_input("Sistem Kimliği")
        p = st.text_input("Erişim Kodu", type="password")
        if st.button("SİSTEMİ BAŞLAT"):
            if u == "emrearas" and p == "master123":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Yetkisiz Erişim.")
    st.stop()

# --- 🖥️ ANA KOMUTA MERKEZİ ---
st.markdown('<div class="main-header"><h1 class="main-title">Nexus Pro Karargahı</h1></div>', unsafe_allow_html=True)
engine = load_nexus_engine()

with st.sidebar:
    st.markdown(f"### 💠 ADMIN: EMRE ARAS")
    st.caption("Status: All Systems Functional")
    if st.button("Güvenli Çıkış"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    st.write("✓ Bütün YZ'ler Yüklü")
    st.write("✓ Enter Desteği Aktif")

# --- 🚀 TÜM YAPAY ZEKALAR (TABS) ---
tab1, tab2, tab3, tab4 = st.tabs(["💬 STRATEJİ & CHAT", "🎨 GENESİS GÖRSEL", "💻 KOD/SİBER LAB", "🔊 SES SENTEZ"])

with tab1:
    # Sohbet geçmişini göster
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]): st.markdown(chat["content"])
    
    # Enter tuşu ile çalışan ana giriş
    if prompt := st.chat_input("Emrinizi buraya yazın..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if engine:
                try:
                    response = engine.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e: st.error(f"Bağlantı Hatası: {e}")

with tab2:
    img_q = st.text_input("Yaratılacak görsel konsepti:")
    if st.button("GÖRSELİ VAR ET"):
        with st.spinner("Piksel sentezleniyor..."):
            url = f"https://pollinations.ai/p/{img_q.replace(' ', '_')}?width=1024&height=1024&model=flux&seed={int(time.time())}"
            st.image(url, caption="Nexus Visual Output")

with tab3:
    st.subheader("💻 Teknik Analiz ve Siber Güvenlik")
    code_input = st.text_area("Analiz edilecek veri:", height=200)
    if st.button("ANALİZİ BAŞLAT"):
        if engine:
            res = engine.generate_content(f"Kıdemli mühendis olarak teknik analiz yap: {code_input}")
            st.code(res.text)

with tab4:
    st.subheader("🔊 Ses Sentezleme")
    text_to_voice = st.text_area("Sese çevrilecek metin:")
    if st.button("SES ÜRET"):
        tts = gTTS(text=text_to_voice, lang='tr')
        b = io.BytesIO()
        tts.write_to_fp(b)
        st.audio(b)

st.markdown("<br><center>© 2026 Emre Aras AI | Omni-Nexus Pro | Kusursuz Sürüm</center>", unsafe_allow_html=True)