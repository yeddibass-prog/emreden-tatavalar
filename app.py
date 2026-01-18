import streamlit as st
import google.generativeai as genai
import pandas as pd
import os, time, io
from datetime import datetime
from gtts import gTTS

# --- 🛰️ MASTER CONFIG (ALL-IN-ONE) ---
# API Anahtarını buraya yapıştır
API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

st.set_page_config(page_title="Emre Aras AI", layout="wide", page_icon="🔱")

# --- 🌌 NEXUS SUPREME UI (PROFESSIONAL BLACK) ---
st.markdown("""
    <style>
    /* Gemini & OpenAI Dark Mode Karışımı */
    .stApp { background-color: #030712; color: #f9fafb; font-family: 'Inter', sans-serif; }
    
    /* Header & Branding */
    .header-bar {
        text-align: center;
        padding: 40px;
        background: linear-gradient(180deg, rgba(37, 99, 235, 0.1) 0%, transparent 100%);
        border-bottom: 1px solid #1f2937;
        margin-bottom: 30px;
    }
    .header-title { font-size: 46px; font-weight: 800; color: #ffffff; letter-spacing: -2px; }

    /* Enter Tuşu Desteği & Chat Box */
    .stChatInputContainer { padding: 20px !important; }
    
    /* Modern Sekmeler */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; border: none; }
    .stTabs [data-baseweb="tab"] { font-weight: 700; color: #9ca3af !important; font-size: 15px; }
    .stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }

    /* Butonlar & Kartlar */
    .stButton>button {
        background: #ffffff !important; color: #000 !important;
        border-radius: 100px !important; font-weight: 700 !important;
        padding: 10px 40px !important;
    }
    [data-testid="stSidebar"] { background-color: #000 !important; border-right: 1px solid #1f2937; }
    </style>
    """, unsafe_allow_html=True)

# --- 💾 SİSTEM HAFIZASI ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- 🔱 ALL MODELS INITIALIZATION (NO-ERROR VERSION) ---
try:
    genai.configure(api_key=API_KEY)
    # 404 HATASINI ÇÖZEN EN KARARLI PRO MODEL
    pro_model = genai.GenerativeModel('gemini-1.5-pro-latest') 
    flash_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("API Bağlantı Hatası: Lütfen anahtarınızı kontrol edin.")

# --- 🔓 LOGIN ---
if not st.session_state.logged_in:
    st.markdown('<div class="header-bar"><h1 class="header-title">EMRE ARAS AI</h1></div>', unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1, 1])
    with login_col:
        u = st.text_input("Yönetici Kimliği", placeholder="emrearas")
        p = st.text_input("Giriş Anahtarı", type="password", placeholder="master123")
        if st.button("SİSTEMİ BAŞLAT"):
            if u == "emrearas" and p == "master123":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Erişim Reddedildi.")
    st.stop()

# --- 🖥️ COMMAND CENTER ---
st.markdown('<div class="header-bar"><h1 class="header-title">Emre Aras AI Karargahı</h1></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 👤 ADMIN: EMRE ARAS")
    if st.button("Güvenli Çıkış"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    st.info("✓ 4 Ana YZ Motoru Aktif\n\n✓ Enter Tuşu Desteği Aktif\n\n✓ 404-Hata Koruması Aktif")

# --- 🚀 BÜTÜN YZ MODÜLLERİ (TOTAL INTEGRATION) ---
tab1, tab2, tab3, tab4 = st.tabs(["💬 NEXUS CHAT (ENTER)", "🎨 GENESIS GÖRSEL", "💻 SİBER & KOD LAB", "🔊 SES SENTEZ"])

with tab1:
    # Sohbet Geçmişini Görüntüle
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]): st.markdown(chat["content"])
    
    # ENTER İLE ÇALIŞAN ANA SOHBET
    if prompt := st.chat_input("Yapay Zekaya bir emir verin..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Pro Zeka Analiz Ediyor..."):
                try:
                    # En güçlü modeli kullanıyoruz
                    response = pro_model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except:
                    # Hata durumunda Flash modele yedekleme yapıyoruz
                    response = flash_model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})

with tab2:
    img_prompt = st.text_input("Hayal ettiğiniz görseli tanımlayın:")
    if st.button("GÖRSELİ VAR ET"):
        with st.spinner("Piksel sentezleniyor..."):
            # Flux ve SD Altyapısını kullanan görsel motoru
            url = f"https://pollinations.ai/p/{img_prompt.replace(' ', '_')}?width=1280&height=720&model=flux&seed={int(time.time())}"
            st.image(url, caption="Nexus Visual Hub")

with tab3:
    st.subheader("💻 Teknik ve Siber Analiz Laboratuvarı")
    code_input = st.text_area("Analiz edilecek teknik veri:", height=200)
    if st.button("KODU VE SİBERİ ANALİZ ET"):
        with st.spinner("Teknik tarama yapılıyor..."):
            res = pro_model.generate_content(f"Kıdemli yazılım mimarı ve siber güvenlik uzmanı olarak analiz et: {code_input}")
            st.code(res.text)

with tab4:
    st.subheader("🔊 Ses Sentezleme")
    voice_text = st.text_area("Sese çevrilecek metni girin:")
    if st.button("SESİ OLUŞTUR"):
        tts = gTTS(text=voice_text, lang='tr')
        byte_io = io.BytesIO()
        tts.write_to_fp(byte_io)
        st.audio(byte_io)

st.markdown("<br><center style='color: #4b5563; font-size: 11px;'>EMRE ARAS AI | OMNI-ZENITH PRO | ALL SYSTEMS ONLINE</center>", unsafe_allow_html=True)