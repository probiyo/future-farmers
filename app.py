import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests 

# --- AYARLAR ---
# URL'yi tekrar kontrol edin: script.google.com/macros/s/..../exec formatında olmalı
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzpPAf0keTr8FLmsbdMuMRkVAZWyPKigwxTHSyZMiQRI2KSZXTFvWnXrEXsu15oFA_g/exec"

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# --- HATA AYIKLAMA FONKSİYONU ---
def debug_connection(data):
    st.write("🔍 **Bağlantı Denetimi:**")
    st.json(data)
    try:
        response = requests.post(WEB_APP_URL, json=data, timeout=10)
        st.write(f"Status Code: {response.status_code}")
        st.write(f"Response: {response.text}")
        return response
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "obs_type": "Gözlem Nesnesi",
        "altitude": "Rakım (Metre)",
        "weather": "Hava Durumu",
        "weather_options": ["Güneşli", "Parçalı Bulutlu", "Kapalı", "Yağmurlu", "Sisli", "Karlı", "Don"],
        "stress": "Bitki Sağlık ve Stres Skoru",
        "stress_help": {1: "1: Çok Sağlıklı", 2: "2: Hafif Stres", 3: "3: Normal Gelişim", 4: "4: Belirgin Stres", 5: "5: Kritik Stres"},
        "pest_title": "Zararlı Tanımlama Rehberi",
        "photo_method": "Fotoğraf Metodu",
        "upload": "Dosya Yükle",
        "camera": "Kamera ile Çek",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "chart_title": "Rakım vs. Stres Korelasyonu",
        "success": "Veriler başarıyla bilimsel veritabanına işlendi!",
        "error": "Bağlantı hatası oluştu!"
    }
}

t = translations["Türkçe 🇹🇷"]

st.title(t["title"])
tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    with st.form("pro_form", clear_on_submit=False): # Hata ayıklama için false yaptık
        col1, col2 = st.columns(2)
        with col1:
            obs_type = st.selectbox(t["obs_type"], ["Çay", "Diğer"])
            alt = st.number_input(t["altitude"], 0, 2500)
            weather = st.selectbox(t["weather"], t["weather_options"])
            stres_val = st.select_slider(t["stress"], options=[1, 2, 3, 4, 5], value=3)
            notes = st.text_area("Gözlem Notları")
            
        with col2:
            photo_choice = st.radio(t["photo_method"], [t["upload"], t["camera"]], horizontal=True)
            if photo_choice == t["upload"]:
                uploaded_file = st.file_uploader(t["upload"], type=['jpg', 'png'])
            else:
                uploaded_file = st.camera_input(t["camera"])

        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            data_to_send = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": obs_type,
                "Rakim": alt,
                "Hava_Durumu": weather,
                "Stres_Skoru": stres_val,
                "Notlar": notes,
                "Foto_Base64": "Test_Verisi" 
            }
            
            # Hata ayıklamalı gönderim
            response = debug_connection(data_to_send)
            
            if response and response.status_code == 200:
                st.success(t["success"])
            elif response:
                st.error(f"Sunucu hatası: {response.text}")

with tab2:
    st.subheader(t["chart_title"])
    # (Analiz kısmı aynı kalabilir)
