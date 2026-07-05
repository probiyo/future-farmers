import streamlit as st
import pandas as pd
import requests
import json
import base64
from datetime import datetime

# --- AYARLAR ---
# Veri tablonuzun CSV linki
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/gviz/tq?tqx=out:csv&sheet=Sayfa1"
# Google Apps Script Web App URL (BURAYA KENDİ URL'Nİ YAZ)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# --- DİL SÖZLÜĞÜ ---
translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "success": "Veriler başarıyla işlendi!",
        "error": "Veri gönderilemedi. Lütfen internet bağlantınızı ve Apps Script URL'sini kontrol edin."
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "entry": "Data Entry Portal",
        "analytics": "Scientific Analysis",
        "submit": "Submit to Scientific Database 🚀",
        "success": "Data processed successfully!",
        "error": "Data could not be sent. Please check your connection and Apps Script URL."
    }
}

lang = st.sidebar.selectbox("Language / Dil", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[lang]

st.title(t["title"])
tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    with st.form("pro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            obs_type = st.selectbox("Gözlem Nesnesi", ["Çay", "Böcekler", "Diğer"])
            alt = st.number_input("Rakım (Metre)", 0, 2500)
            stres_val = st.select_slider("Bitki Sağlık ve Stres Skoru (1-5)", options=[1, 2, 3, 4, 5], help="1: Çok Sağlıklı, 5: Çok Stresli")
        with col2:
            weather = st.selectbox("Hava Durumu", ["Güneşli", "Kapalı", "Yağmurlu"])
            uploaded_file = st.camera_input("Kamera ile Çek")
            notes = st.text_area("Gözlem Notlarınız")

        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            # Fotoğrafı base64 formatına çevir
            foto_base64 = "Test_Verisi"
            if uploaded_file is not None:
                foto_bytes = uploaded_file.getvalue()
                foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
            
            # Gönderilecek veri paketi
            data = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": obs_type,
                "Rakim": alt,
                "Hava_Durumu": weather,
                "Stres_Skoru": stres_val,
                "Notlar": notes,
                "Foto_Base64": foto_base64
            }
            
            try:
                response = requests.post(WEB_APP_URL, json=data)
                if response.status_code == 200:
                    st.success(t["success"])
                else:
                    st.error(t["error"])
            except Exception as e:
                st.error(f"{t['error']} Detay: {e}")

with tab2:
    st.subheader(t["analytics"])
    try:
        # Veriyi çekiyoruz
        df = pd.read_csv(SHEET_URL)
        
        # Sütun isimlerini temizle
        df.columns = df.columns.str.strip()
        
        # Tabloyu göster
        st.dataframe(df)
        
    except Exception as e:
        st.warning("Veriler yüklenirken bir hata oluştu. Lütfen Google Sheets'in herkese açık olduğundan emin olun.")
        st.write("Hata detayı:", e)
