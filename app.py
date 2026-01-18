import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# --- 🛰️ MASTER CONFIG ---
DEFAULT_API_KEY = "AIzaSyBPmRSFFfVL6CrSGpJNSdwM5LkPVZ4ULkQ"

# --- 💾 VERİTABANI YÖNETİMİ (Kullanıcılar ve Yetkiler) ---
USER_DB = "user_database.csv"
LOG_DB = "system_logs.csv"

def load_data():
    if not os.path.exists(USER_DB):
        # Başlangıç Ayarı: Kullanıcı Adı, Şifre, Yetki (admin veya user)
        df = pd.DataFrame({
            "username": ["emrearas"], 
            "password": ["master123"], 
            "role": ["admin"]
        })
        df.to_csv(USER_DB, index=False)
    
    if not os.path.exists(LOG_DB):
        df = pd.DataFrame(columns=["timestamp", "user", "action", "content"])
        df.to_csv(LOG_DB, index=False)
    
    return pd.read_csv(USER_DB), pd.read_csv(LOG_DB)

def save_user(username, password, role):
    df = pd.read_csv(USER_DB)
    if username in df['username'].values:
        # Eğer kullanıcı varsa güncelle (Şifre veya Yetki değiştirme)
        df.loc[df['username'] == username, ['password', 'role']] = [password, role]
    else:
        # Yeni kullanıcı ekle
        new_user = pd.DataFrame({"username": [username], "password": [password], "role": [role]})
        df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DB, index=False)

def add_log(user, action, content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(LOG_DB)
    new_log = pd.DataFrame({"timestamp": [now], "user": [user], "action": [action], "content": [content]})
    df = pd.concat([df, new_log], ignore_index=True)
    df.to_csv(LOG_DB, index=False)

users_df, logs_df = load_data()

# --- 🔐 GİRİŞ KONTROLÜ ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Emre Aras AI | Giriş")
    u = st.text_input("Kullanıcı Adı")
    p = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if u in users_df['username'].values:
            user_data = users_df[users_df['username'] == u].iloc[0]
            if str(p) == str(user_data['password']):
                st.session_state.logged_in = True
                st.session_state.user = u
                st.session_state.role = user_data['role']
                st.rerun()
        st.error("Hatalı bilgiler.")
    st.stop()

# --- 🔱 ANA SİSTEM ---
st.sidebar.title(f"👤 {st.session_state.user.upper()}")
st.sidebar.info(f"Yetki: {st.session_state.role.upper()}")

if st.sidebar.button("Çıkış Yap"):
    st.session_state.logged_in = False
    st.rerun()

# --- ⚙️ YÖNETİCİ PANELİ (Sadece 'admin' rolündekiler görebilir) ---
if st.session_state.role == "admin":
    with st.sidebar.expander("🛡️ Yönetim Merkezi"):
        st.subheader("Kullanıcı & Yetki Yönetimi")
        target_user = st.text_input("Hedef Kullanıcı Adı")
        target_pw = st.text_input("Şifre Belirle", type="password")
        target_role = st.selectbox("Yetki Seviyesi", ["user", "admin"])
        
        if st.button("Kullanıcıyı Kaydet/Güncelle"):
            save_user(target_user, target_pw, target_role)
            st.success(f"{target_user} ({target_role}) kaydedildi!")

        st.markdown("---")
        st.markdown("#### 📜 Sistem Kayıtları")
        current_logs = pd.read_csv(LOG_DB)
        st.dataframe(current_logs.tail(20))

# --- 🌌 YAPAY ZEKA MODÜLLERİ ---
# (Buraya daha önce hazırladığımız Gemini fonksiyonlarını ekleyebilirsin)
st.header("Emre Aras AI Stratejik Merkezi")
prompt = st.text_area("Sorunuzu buraya yazın:")
if st.button("Analiz Et"):
    add_log(st.session_state.user, "AI Sorgusu", prompt)
    # Gemini API çağrısı buraya gelecek...
    st.write("Analiz tamamlandı. (Loglara kaydedildi)")