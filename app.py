import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- CONFIG ---
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# --- ZARARLI VE BİTKİ VERİ TABANI ---
PEST_DATABASE = {
    "Tea Plant": ["Yok", "Çay Filiz Güvesi", "Çay Koşnili", "Vampir Kelebek", "Kahverengi Kokarca"],
    "Brassica oleracea (Brüksel Lahanası)": ["Yok", "Yaprak Biti (Aphids)", "Lahana Güvesi", "Toprak Piresi", "Salyangoz"],
    "Diğer": ["Yok", "Bölgesel Zararlı Gözlemlenmedi"]
}

# --- SIDEBAR: ÜLKE VE DİL ---
st.sidebar.title("🌐 Ayarlar")
country = st.sidebar.selectbox("Ülke / Country", ["Türkiye", "Belçika", "Almanya", "İtalya"])
lang = st.sidebar.radio("Dil / Language", ["TR", "EN"])

st.title("🌱 Future Farmers Pro")

# --- VERİ GİRİŞİ ---
obs_type = st.selectbox("Bitki Türü / Plant Type", list(PEST_DATABASE.keys()))

# --- OTOMATİK ZARARLI LİSTESİ ---
if obs_type in PEST_DATABASE:
    current_pests = PEST_DATABASE[obs_type]
else:
    current_pests = ["Yok"]

zararli_turu = st.selectbox(f"🔍 Bölgesel Zararlı Rehberi ({country})", current_pests)

# --- FORM ---
with st.form("main_form", clear_on_submit=True):
    rakim = st.number_input("Rakım (m)", 0, 2000, 200)
    stres = st.slider("Stres Skoru (1-5)", 1, 5, 1)
    foto = st.camera_input("Bitki Fotoğrafı")
    
    submit = st.form_submit_button("Veriyi Gönder")
    
    if submit:
        # Burada kendi Google Apps Script URL'niz olmalı
        WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"
        
        payload = {
            "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Gozlem_Turu": f"{obs_type} ({country})",
            "Rakim": rakim,
            "Stres_Skoru": stres,
            "Zararli": zararli_turu,
            "Foto_Base64": base64.b64encode(foto.read()).decode() if foto else "Test"
        }
        
        try:
            requests.post(WEB_APP_URL, json=payload, timeout=10)
            st.success("Veri başarıyla Brüksel/Rize veri tabanına iletildi!")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
