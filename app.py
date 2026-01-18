import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time
from datetime import datetime

# --- 🛰️ MASTER CONFIG ---
# Kendi API anahtarını buraya hatasız yapıştır
DEFAULT_API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(
    page_title="Emre Aras AI | Nexus Enterprise",
    layout="wide",
    page_icon="💠"
)

# --- 🌌 NEXUS ENTERPRISE UI (CSS) ---
st.markdown("""
    <style>
    /* Ultra Modern Karanlık Tema */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0a0c10 0%, #010203 100%);
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Üst Başlık Alanı */
    .hero-header {
        text-align: center;
        padding: 50px 0;
        background: linear-gradient(180deg, rgba(31, 111, 235, 0.05) 0%, rgba(1, 2, 3, 0) 100%);
        border-bottom: 1px solid #30363d;
        margin-bottom: 40px;
    }
    
    .hero-text {
        font-size: 48px;
        font-weight: 700;
        letter-spacing: -1.5px;
        color: #ffffff;
    }

    /* Giriş Kutusu ve Kartlar */
    .stTextArea textarea {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        color: #e6edf3 !important;
        font-size: 16px !important;
        padding: 15px !important;
    }

    /* Apple Tarzı Mavi Butonlar */
    .stButton>button {
        background-color: #1f6feb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        transition: 0.2s ease !important;
        margin: 0 auto;
        display: block;
    }
    
    .stButton>button:hover {
        background-color: #388bfd !important;
        box-shadow: 0 0 20px rgba(31, 111, 235, 0.4);
        transform: translateY(-1px);
    }

    /* Sidebar Zarifleştirme */
    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 VERİ YÖNETİMİ ---
USER_DB, LOG_DB = "users_v2.csv", "logs_v2.csv"

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame({"username": ["emrearas"], "password": ["master123"], "role": ["admin"]}).to_csv(USER_DB, index=False)
    if not os.path.exists(LOG_DB):
        pd.DataFrame(columns=["timestamp", "user", "action", "detail"]).to_csv(LOG_DB, index=False)

init_db()

def log_event(user, action, detail):
    df = pd.read_csv(LOG_DB)
    new_entry = pd.DataFrame({"timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user": [user], "action": [action], "detail": [detail[:100]]})
    pd.concat([df, new_entry]).to_csv(LOG_DB, index=False)

# --- 🔐 GİRİŞ KONTROLÜ ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="hero-header"><h1 class="hero-text">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1, 1])
    with login_col:
        u_in = st.text_input("Yönetici Kimliği")
        p_in = st.text_input("Parola", type="password")
        if st.button("SİSTEME GİRİŞ"):
            udf = pd.read_csv(USER_DB)
            if u_in in udf['username'].values:
                correct_p = udf[udf['username'] == u_in]['password'].values[0]
                if str(p_in) == str(correct_p):
                    st.session_state.logged_in = True
                    st.session_state.user = u_in
                    st.session_state.role = udf[udf['username'] == u_in]['role'].values[0]
                    st.rerun()
            st.error("Erişim Reddedildi.")
    st.stop()

# --- 🔱 NEXUS PRO HUB ---
# Model isimlendirme hatasını (404) gidermek için güncel yapı
try:
    genai.configure(api_key=DEFAULT_API_KEY)
    # En kararlı model ismini kullanıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

st.markdown('<div class="hero-header"><h1 class="hero-text">EMRE ARAS AI</h1><p style="text-align:center; color:#8b949e;">Nexus Enterprise Intelligence Core</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 💠 {st.session_state.user.upper()}")
    st.caption(f"Status: Operational | Role: {st.session_state.role}")
    if st.button("Güvenli Çıkış"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "admin":
        st.markdown("---")
        if st.checkbox("Sistem Loglarını İzle"):
            st.dataframe(pd.read_csv(LOG_DB).tail(20), use_container_width=True)

# --- 🚀 MISSION MODULES ---
tabs = st.tabs(["💬 STRATEJİK ANALİZ", "🎨 GÖRSEL YARATIM"])

with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    cmd = st.text_area("Yapay Zekaya bir emir verin veya soru sorun:", height=200, placeholder="Nexus Pro sizi dinliyor...")
    if st.button("ANALİZİ BAŞLAT"):
        if cmd:
            with st.spinner("Omni-Core veriyi işliyor..."):
                try:
                    # generate_content çağrısı kararlı hale getirildi
                    response = model.generate_content(cmd)
                    st.markdown("---")
                    st.markdown("### 🤖 Nexus Analiz Raporu")
                    st.write(response.text)
                    log_event(st.session_state.user, "AI_QUERY", cmd)
                except Exception as e:
                    st.error(f"Sistem Hatası: {e}")

with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    img_prompt = st.text_input("Yaratılacak görsel konsepti:")
    if st.button("GÖRSELİ VAR ET"):
        if img_prompt:
            with st.spinner("Piksel sentezi yapılıyor..."):
                url = f"https://pollinations.ai/p/{img_prompt.replace(' ', '_')}?width=1024&height=1024&model=flux&seed={int(time.time())}"
                st.image(url, caption=f"Emre Aras AI | {img_prompt}")
                log_event(st.session_state.user, "IMAGE_GEN", img_prompt)

st.markdown("<br><hr><center>© 2026 Emre Aras AI | Nexus Enterprise | Confidential</center>", unsafe_allow_html=True)