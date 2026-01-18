import streamlit as st
import google.generativeai as genai
import requests, time, io, os
from gtts import gTTS
from PIL import Image

# --- 🛰️ NEXUS CORE: ULTRA-MODERN CONFIG ---
st.set_page_config(
    page_title="Emre Aras AI | Nexus Intelligence",
    layout="wide",
    page_icon="🌌"
)

# --- 🌌 GEMINI STYLE GLASSMORPHISM (CSS) ---
st.markdown("""
    <style>
    /* Gemini Animasyonlu Arka Plan */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a, #020617);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Cam Efekti Kartlar (Glassmorphism) */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Premium Header */
    .nexus-header {
        text-align: center;
        padding: 60px 0;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nexus-title {
        font-size: 64px;
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0;
    }

    /* Gemini Tarzı Glow Butonlar */
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 100px; /* Tam yuvarlak */
        padding: 14px 40px;
        font-weight: 600;
        width: auto;
        display: block;
        margin: 0 auto;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.4);
    }
    
    .stButton>button:hover {
        transform: scale(1.05) translateY(-3px);
        box-shadow: 0 20px 40px -10px rgba(124, 58, 237, 0.6);
        color: white;
    }

    /* Sidebar Gizleme ve Modernize Etme */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Input Alanları */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #f8fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🌌 NEXUS BRANDING ---
st.markdown("""
    <div class="nexus-header">
        <h1 class="nexus-title">EMRE ARAS AI</h1>
        <p style="color: #94a3b8; letter-spacing: 5px; font-weight: 500;">NEXUS STRATEGIC ECOSYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

# --- 🗝️ SYSTEM ACCESS ---
with st.sidebar:
    st.markdown("### 🛡️ CONTROL CENTER")
    api_key = st.text_input("Enter Nexus Key:", type="password", placeholder="AI Studio Key...")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        st.success("BİLİNÇ: ONLINE")
    
    st.markdown("---")
    st.caption("EMRE ARAS AI v4.0 | NEXUS EDITION")

if api_key:
    # --- 🌌 PREMIUM SEKMELER ---
    tabs = st.tabs(["🔱 STRATEJİ", "🎨 YARATIM", "💻 TEKNOLOJİ", "📈 İSTİHBARAT"])

    with tabs[0]:
        st.markdown("### 🔱 Master Strategy Swarm")
        task = st.text_area("Karmaşık bir görev tanımlayın:", height=150)
        if st.button("SİSTEMİ TETİKLE"):
            with st.spinner("Nexus ağına bağlanılıyor..."):
                res = model.generate_content(f"Sen dünyanın en zeki AI asistanısın. Şu konuyu en derin haliyle çöz: {task}")
                st.markdown(res.text)

    with tabs[1]:
        st.markdown("### 🎨 Creative Asset Generator")
        p_text = st.text_input("Yaratılacak konsept:")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("GÖRSELİ VAR ET"):
                url = f"https://pollinations.ai/p/{p_text.replace(' ', '_')}?width=1280&height=720&seed={time.time()}&model=flux"
                st.image(url, use_container_width=True)
        with c2:
            if st.button("SESİ SENTEZLE"):
                tts = gTTS(text=p_text, lang='tr')
                fp = io.BytesIO(); tts.write_to_fp(fp); fp.seek(0)
                st.audio(fp)

    with tabs[2]:
        st.markdown("### 💻 Neural Architecture & Code")
        c_input = st.text_area("Analiz edilecek veri:")
        if st.button("KODU EVRİLT"):
            res = model.generate_content(f"Kıdemli yazılım mimarı olarak analiz et: {c_input}")
            st.code(res.text)

    with tabs[3]:
        st.markdown("### 📈 Global Market & OSINT")
        o_input = st.text_input("Haber veya borsa odağı:")
        if st.button("İSTİHBARATI ÇEK"):
            res = model.generate_content(f"OSINT ve Finansal Deha olarak analiz et: {o_input}")
            st.warning(res.text)

else:
    st.markdown("<div style='text-align: center; padding: 50px; color: #64748b;'>Sistemi uyandırmak için Nexus anahtarını sidebar paneline girin.</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569; font-size: 11px;'>EMRE ARAS AI | NEXUS CORE | 2026</p>", unsafe_allow_html=True)