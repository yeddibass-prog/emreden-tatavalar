import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from gtts import gTTS

# --- 🛰️ MASTER CONFIG ---
# API Anahtarını buraya yapıştır
API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(page_title="Emre Aras AI", layout="wide", page_icon="🔱")

# --- 🌌 NEXUS SUPREME UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e3e3e3; font-family: 'Inter', sans-serif; }
    .brand-header { text-align: center; padding: 30px; border-bottom: 1px solid #1a1a1a; margin-bottom: 20px; }
    .brand-title { font-size: 38px; font-weight: 800; color: #ffffff; letter-spacing: -1px; }
    /* Chat Girişi */
    .stChatInputContainer { padding: 20px !important; }
    /* Modern Sekmeler */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; color: #666 !important; }
    .stTabs [aria-selected="true"] { color: #fff !important; border-bottom: 2px solid #1a73e8 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🔐 AUTH & DB ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []

# --- 🔱 MODEL INTEGRATION ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest') 
except: pass

# --- 🔓 LOGIN ---
if not st.session_state.logged_in:
    st.markdown('<div class="brand-header"><div class="brand-title">EMRE ARAS AI</div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        u = st.text_input("Kimlik")
        p = st.text_input("Parola", type="password")
        if st.button("SİSTEMİ AÇ"):
            if u == "emrearas" and p == "master123":
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 🖥️ MAIN HUB ---
st.markdown('<div class="brand-header"><div class="brand-title">Emre Aras AI Karargahı</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 💠 SİSTEM DURUMU: AKTİF")
    if st.button("Güvenli Çıkış"):
        st.session_state.logged_in = False
        st.rerun()

# --- 🚀 TÜM YZ MODÜLLERİ (ALL AI MODULES) ---
tab1, tab2, tab3, tab4 = st.tabs(["💬 STRATEJİK SOHBET", "🎨 GÖRSEL MOTORU", "💻 KOD/SİBER", "🔊 SES SENTEZ"])

with tab1:
    # Sohbet Geçmişi
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Emrinizi yazın (Enter)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

with tab2:
    img_q = st.text_input("Oluşturulacak görselin detaylı tarifi:")
    if st.button("GÖRSELİ VAR ET"):
        with st.spinner("Piksel sentezleniyor..."):
            url = f"https://pollinations.ai/p/{img_q.replace(' ', '_')}?width=1024&height=1024&model=flux"
            st.image(url)

with tab3:
    code_q = st.text_area("Analiz edilecek kod veya teknik veri:", height=150)
    if st.button("TEKNİK ANALİZ YAP"):
        res = model.generate_content(f"Kıdemli yazılım ve siber güvenlik uzmanı olarak analiz et: {code_q}")
        st.code(res.text)

with tab4:
    text_s = st.text_area("Sese dönüştürülecek metin:")
    if st.button("SES DOSYASI OLUŞTUR"):
        tts = gTTS(text=text_s, lang='tr')
        fp = io.BytesIO(); tts.write_to_fp(fp); fp.seek(0)
        st.audio(fp)

st.markdown("<br><center>© 2026 Emre Aras AI | Tüm Sistemler Yüklü</center>", unsafe_allow_html=True)