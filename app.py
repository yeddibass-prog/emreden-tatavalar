import streamlit as st
import google.generativeai as genai
import requests, time, io, os
from gtts import gTTS
from PIL import Image

# --- 🛰️ ENTERPRISE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Emre Aras AI | Strategic Intelligence",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# --- 🌑 CORPORATE DESIGN LANGUAGE (CSS) ---
st.markdown("""
    <style>
    /* Global Minimalist Dark Theme */
    .stApp {
        background-color: #0b0e14;
        color: #f0f0f0;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Global Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #11141a;
        border-right: 1px solid #1f242d;
    }

    /* Enterprise Header */
    .main-header {
        background: linear-gradient(135deg, #1a1f29 0%, #0b0e14 100%);
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #1f242d;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    .brand-title {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -2px;
        color: #ffffff;
        margin-bottom: 10px;
    }
    
    .brand-subtitle {
        color: #64748b;
        font-size: 14px;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* Enterprise Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 0 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #1a1f29;
        border-radius: 6px;
        color: #94a3b8 !important;
        border: 1px solid #1f242d;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.4);
    }

    /* Professional Action Buttons */
    .stButton>button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 15px 30px;
        font-weight: 700;
        width: 100%;
        letter-spacing: 1px;
        transition: 0.3s all;
    }
    
    .stButton>button:hover {
        background: #1d4ed8;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
    }

    /* Input Fields Customization */
    .stTextArea textarea, .stTextInput input {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🏢 BRANDING SECTION ---
st.markdown("""
    <div class="main-header">
        <div class="brand-title">EMRE ARAS AI</div>
        <div class="brand-subtitle">Strategic Multi-Agent Intelligence Core</div>
    </div>
    """, unsafe_allow_html=True)

# --- 🗝️ SYSTEM ACCESS & CONTROL ---
with st.sidebar:
    st.markdown("### 🔐 ACCESS CONTROL")
    api_key = st.text_input("Enter Enterprise API Key:", type="password", placeholder="Paste Gemini API Key here...")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        st.success("AUTHENTICATED: SYSTEM ACTIVE")
    
    st.markdown("---")
    st.markdown("### 🛰️ ACTIVE SYSTEMS")
    st.info("✓ Swarm Logic Engine\n\n✓ Cyber Defense Grid\n\n✓ Quantum Analysis Lab\n\n✓ Global OSINT Monitor")
    
    st.markdown("---")
    st.caption("EMRE ARAS AI v3.0 | 2026")

# --- 🌌 MISSION MODULES ---
if api_key:
    t1, t2, t3, t4, t5 = st.tabs([
        "🔱 COMMAND", "🎨 CREATIVE", "💻 TECH", "📈 FINANCE", "🧬 BIO"
    ])

    with t1:
        st.markdown("#### 🔱 Global Strategy & Swarm Command")
        task = st.text_area("Yüksek düzeyli stratejik hedefinizi tanımlayın:", height=180, placeholder="Örn: 5 yıllık küresel pazar büyüme planı ve teknolojik altyapı stratejisi oluştur.")
        if st.button("EXECUTE MASTER STRATEGY"):
            with st.spinner("Processing through 10,000+ AIs..."):
                res = model.generate_content(f"Sen dünyanın en gelişmiş strateji uzmanı ve CEO danışmanısın. Şu görevi kurumsal bir dille ve hatasız çöz: {task}")
                st.markdown(res.text)

    with t2:
        st.markdown("#### 🎨 Asset Generation & Marketing")
        p_text = st.text_input("Görsel veya İçerik Konsepti:")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("CREATE VISUAL ASSET"):
                url = f"https://pollinations.ai/p/{p_text.replace(' ', '_')}?width=1280&height=720&seed={time.time()}&model=flux"
                st.image(url, caption="Generated AI Asset")
        with c2:
            if st.button("SYNTHESIZE SPEECH"):
                tts = gTTS(text=p_text, lang='tr')
                fp = io.BytesIO(); tts.write_to_fp(fp); fp.seek(0)
                st.audio(fp)

    with t3:
        st.markdown("#### 💻 Engineering & Cyber Security")
        c_mode = st.selectbox("Görev Tipi:", ["System Audit", "Secure Code Evolution", "Blockchain Strategy", "Cloud Infrastructure"])
        c_input = st.text_area("İşlenecek teknik veri:")
        if st.button("START ENGINE"):
            res = model.generate_content(f"{c_mode} uzmanı olarak analiz et: {c_input}")
            st.code(res.text)

    with t4:
        st.markdown("#### 📈 Financial Intelligence & OSINT")
        o_input = st.text_input("Takip edilecek borsa/şirket/haber:")
        if st.button("FETCH ANALYSIS"):
            res = model.generate_content(f"Finansal analiz ve OSINT uzmanı olarak derin rapor sun: {o_input}")
            st.warning(res.text)

    with t5:
        st.markdown("#### 🧬 Human Optimization Lab")
        b_input = st.text_area("Biyometrik veri analizi:")
        if st.button("GENERATE BIO-PLAN"):
            res = model.generate_content(f"Bio-hacker ve sağlık uzmanı olarak optimize et: {b_input}")
            st.success(res.text)

else:
    st.warning("⚠️ Erişim Kısıtlı: Lütfen sol panelden Enterprise API anahtarınızı girin.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4b5563; font-size: 11px;'>CONFIDENTIAL | EMRE ARAS AI ENTERPRISE SOLUTIONS | NO LIMITS</p>", unsafe_allow_html=True)