import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from gtts import gTTS

# --- 🛰️ MASTER CONFIG ---
# Kendi API anahtarını buraya yapıştır
DEFAULT_API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(
    page_title="Emre Aras AI | Nexus Pro",
    layout="wide",
    page_icon="💠"
)

# --- 🌌 NEXUS PREMIUM UI (CSS) ---
st.markdown("""
    <style>
    /* Gemini Stil Derin Siyah Tema */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Hero Başlık Alanı */
    .brand-section {
        text-align: center;
        padding: 60px 0;
        background: linear-gradient(180deg, rgba(59, 130, 246, 0.05) 0%, rgba(0,0,0,0) 100%);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 40px;
    }
    
    .brand-text {
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Apple/Gemini Stil Butonlar */
    .stButton>button {
        background: #ffffff !important;
        color: #020617 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        font-weight: 700 !important;
        transition: 0.3s ease !important;
        display: block;
        margin: 0 auto;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }

    /* Giriş Alanları */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: #ffffff !important;
    }

    /* Sidebar Zarifleştirme */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 KALICI VERİ SİSTEMİ ---
USER_DB, LOG_DB = "users_final.csv", "logs_final.csv"

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame({"username": ["emrearas"], "password": ["master123"], "role": ["admin"]}).to_csv(USER_DB, index=False)
    if not os.path.exists(LOG_DB):
        pd.DataFrame(columns=["timestamp", "user", "action", "detail"]).to_csv(LOG_DB, index=False)

init_db()

def write_log(user, action, detail):
    df = pd.read_csv(LOG_DB)
    new_log = pd.DataFrame({"timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user": [user], "action": [action], "detail": [detail[:100]]})
    pd.concat([df, new_log]).to_csv(LOG_DB, index=False)

# --- 🔐 GİRİŞ SİSTEMİ (HATA DÜZELTİLDİ) ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="brand-section"><h1 class="brand-text">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2: # Hata veren col2 değişkeni burada c2 olarak tanımlandı
        u_login = st.text_input("Kullanıcı Adı")
        p_login = st.text_input("Şifre", type="password")
        if st.button("SİSTEME GİRİŞ"):
            udf = pd.read_csv(USER_DB)
            if u_login in udf['username'].values:
                pw_check = udf[udf['username'] == u_login]['password'].values[0]
                if str(p_login) == str(pw_check):
                    st.session_state.logged_in = True
                    st.session_state.user = u_login
                    st.session_state.role = udf[udf['username'] == u_login]['role'].values[0]
                    st.rerun()
            st.error("Erişim Reddedildi.")
    st.stop()

# --- 🔱 NEXUS OPERATIONAL HUB ---
genai.configure(api_key=DEFAULT_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

st.markdown('<div class="brand-section"><h1 class="brand-text">EMRE ARAS AI</h1><p style="color:#64748b; letter-spacing:4px;">NEXUS STRATEGIC HUB</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 💠 {st.session_state.user.upper()}")
    st.caption(f"Role: {st.session_state.role}")
    if st.button("Güvenli Çıkış"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "admin":
        st.markdown("---")
        if st.checkbox("İşlem Kayıtlarını İzle"):
            st.dataframe(pd.read_csv(LOG_DB).tail(20), use_container_width=True)

# --- 🚀 MODÜLLER ---
tab1, tab2 = st.tabs(["💬 STRATEJİK ANALİZ", "🎨 GENESIS YARATIM"])

with tab1:
    user_query = st.text_area("Yapay Zekaya bir talimat verin:", height=200)
    if st.button("ANALİZİ BAŞLAT"):
        if user_query:
            with st.spinner("İşleniyor..."):
                try:
                    res = model.generate_content(user_query)
                    st.markdown("### 🤖 Nexus Yanıtı")
                    st.write(res.text)
                    write_log(st.session_state.user, "Sorgu", user_query)
                except Exception as e: st.error(f"Hata: {e}")

with tab2:
    img_concept = st.text_input("Görsel Konsepti:")
    if st.button("GÖRSELİ VAR ET"):
        with st.spinner("Piksel sentezi..."):
            # Görsel motorunu daha kararlı bir URL ile güncelledim
            img_url = f"https://pollinations.ai/p/{img_concept.replace(' ', '_')}?width=1024&height=1024&model=flux&seed={int(time.time())}"
            st.image(img_url, caption=f"Emre Aras AI | {img_concept}")
            write_log(st.session_state.user, "Görsel", img_concept)

st.markdown("<br><center>© 2026 Emre Aras AI | Nexus Pro | Privacy Guaranteed</center>", unsafe_allow_html=True)