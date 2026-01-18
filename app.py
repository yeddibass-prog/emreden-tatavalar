import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from PIL import Image

# --- 🛰️ MASTER CONFIG (OMNI-PRO) ---
# API Anahtarını buraya hatasız yapıştır
DEFAULT_API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(
    page_title="Emre Aras AI | Nexus Pro",
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# --- 🌌 NEXUS DESIGN SYSTEM (ULTRA-CSS) ---
st.markdown("""
    <style>
    /* Gemini Premium Glassmorphism Theme */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Hero Header */
    .hero-container {
        text-align: center;
        padding: 80px 0 40px 0;
        background: linear-gradient(180deg, rgba(59, 130, 246, 0.05) 0%, rgba(0,0,0,0) 100%);
    }
    
    .hero-logo {
        font-size: 56px;
        font-weight: 800;
        letter-spacing: -3px;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* Glass Cards */
    .st-emotion-cache-1r6slb0, .st-emotion-cache-ocq980 {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }

    /* Apple Style Pill Buttons */
    .stButton>button {
        background: #ffffff;
        color: #020617;
        border: none;
        border-radius: 100px;
        padding: 12px 40px;
        font-weight: 700;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: auto;
        margin: 0 auto;
        display: block;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        background: #f8fafc;
        box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }

    /* Modern Text Areas */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: #f1f5f9 !important;
        font-size: 16px !important;
    }

    /* Tab Customization */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; border-bottom: none; justify-content: center; }
    .stTabs [data-baseweb="tab"] { color: #64748b !important; font-weight: 600; font-size: 16px; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 PERSISTENT CORE (DB) ---
USER_DB, LOG_DB = "users_pro.csv", "logs_pro.csv"

def init_pro_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame({"username": ["emrearas"], "password": ["master123"], "role": ["admin"]}).to_csv(USER_DB, index=False)
    if not os.path.exists(LOG_DB):
        pd.DataFrame(columns=["timestamp", "user", "action", "detail"]).to_csv(LOG_DB, index=False)

init_pro_db()

def log_pro(user, action, detail):
    df = pd.read_csv(LOG_DB)
    new_log = pd.DataFrame({"timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "user": [user], "action": [action], "detail": [detail[:100]]})
    pd.concat([df, new_log]).to_csv(LOG_DB, index=False)

# --- 🔐 PRO AUTH ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="hero-container"><h1 class="hero-logo">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with col2:
        u = st.text_input("Kullanıcı Adı", placeholder="admin...")
        p = st.text_input("Parola", type="password", placeholder="••••••••")
        if st.button("SİSTEME ERİŞ"):
            udf = pd.read_csv(USER_DB)
            if u in udf['username'].values and str(p) == str(udf[udf['username']==u]['password'].values[0]):
                st.session_state.logged_in, st.session_state.user, st.session_state.role = True, u, udf[udf['username']==u]['role'].values[0]
                st.rerun()
            else: st.error("Erişim Reddedildi.")
    st.stop()

# --- 🔱 OMNI-NEXUS OPERATIONAL HUB ---
genai.configure(api_key=DEFAULT_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

st.markdown('<div class="hero-container"><h1 class="hero-logo">EMRE ARAS AI</h1><p style="color:#64748b; letter-spacing:4px; font-weight:500;">NEXUS STRATEGIC COMMAND</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 💠 {st.session_state.user.upper()}")
    st.caption(f"Status: Operational | Role: {st.session_state.role}")
    if st.button("Sistemden Çık"):
        st.session_state.logged_in = False
        st.rerun()
    
    if st.session_state.role == "admin":
        st.markdown("---")
        st.markdown("### ⚙️ ADMIN CENTER")
        with st.expander("User Management"):
            nu = st.text_input("Yeni Kullanıcı")
            np = st.text_input("Şifre", type="password")
            if st.button("Onayla ve Kaydet"):
                udf = pd.read_csv(USER_DB)
                pd.concat([udf, pd.DataFrame({"username": [nu], "password": [np], "role": ["user"]})]).to_csv(USER_DB, index=False)
                st.success("Kullanıcı Mühürlendi.")
        
        if st.checkbox("Canlı Sistem Kayıtları"):
            st.dataframe(pd.read_csv(LOG_DB).tail(15), use_container_width=True)

# --- 🚀 MODULES ---
tab1, tab2 = st.tabs(["💬 STRATEJİK ZEKA", "🎨 GENESİS YARATIM"])

with tab1:
    q = st.text_area("İşlem emrini tanımlayın...", height=200, placeholder="Nexus Pro sizi dinliyor...")
    if st.button("ANALİZİ BAŞLAT"):
        if q:
            with st.spinner("Omni-Core veriyi işliyor..."):
                try:
                    res = model.generate_content(q)
                    st.markdown("### 🤖 Nexus Analiz Sonucu")
                    st.write(res.text)
                    log_pro(st.session_state.user, "AI_QUERY", q)
                except Exception as e: st.error(f"Bağlantı Hatası: {e}")

with tab2:
    img_p = st.text_input("Görsel Konsepti:")
    if st.button("GÖRSELİ VAR ET"):
        with st.spinner("Piksel sentezi yapılıyor..."):
            url = f"https://pollinations.ai/p/{img_p.replace(' ', '_')}?width=1024&height=1024&model=flux&nologo=true"
            st.image(url, caption=f"Emre Aras AI | {img_p}")
            log_pro(st.session_state.user, "IMAGE_GEN", img_p)

st.markdown("<br><p style='text-align: center; color: #334155; font-size: 11px;'>EMRE ARAS AI | OMNI-NEXUS PRO | PRIVILEGED ACCESS ONLY</p>", unsafe_allow_html=True)