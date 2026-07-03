import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Future Farmers - Portal", page_icon="🌱", layout="wide")

# AYARLAR: Kendi URL'lerinizi buraya yapıştırın
WEB_APP_URL = "BURAYA_GOOGLE_APPS_SCRIPT_URLNIZI_YAZIN"
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/edit?gid=0#gid=0"

# DİLLER
translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Projesi Gözlem & Bilimsel Analiz",
        "tab_entry": "📝 Veri Giriş",
        "tab_analytics": "📊 Analiz",
        "obs_type": "Gözlem Nesnesi:",
        "obs_options": ["Proje Bitkim (Çay)", "Diğer Tarım Bitkisi"],
        "altitude": "Rakım (Metre):",
        "weather": "Hava Durumu:",
        "weather_options": ["Güneşli", "Parçalı Bulutlu", "Kapalı", "Yağmurlu", "Sisli"],
        "stress": "Bitki Sağlık ve Stres Skoru (1-5):",
        "stress_help": "1: Çok Sağlıklı, 3: Normal Gelişim, 5: Kritik Stres (Kuruma/Parazit).",
        "pest_guide": "📖 Zararlı Tanıma Rehberi",
        "pest_title": "⚠️ Zararlı ve Hastalık Tespiti",
        "pests": "Görülen Zararlılar:",
        "pest_options": ["Yok (Sağlıklı)", "Yeşil Çay Cücesi", "Çay Akarı", "Trips", "Diğer"],
        "notes": "Gözlem Notlarınız:",
        "upload": "Bitki Fotoğrafı Yükle:",
        "submit": "Verileri Gönder 🚀",
        "success": "Başarıyla gönderildi!"
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Project Observation & Scientific Analysis",
        "tab_entry": "📝 Data Entry",
        "tab_analytics": "📊 Analytics",
        "obs_type": "Observation Target:",
        "obs_options": ["My Tea Plant", "Other Crop"],
        "altitude": "Altitude (Meters):",
        "weather": "Weather Condition:",
        "weather_options": ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Foggy"],
        "stress": "Plant Health & Stress Score (1-5):",
        "stress_help": "1: Very Healthy, 3: Normal Growth, 5: Critical Stress (Drying/Parasites).",
        "pest_guide": "📖 Pest Identification Guide",
        "pest_title": "⚠️ Pest & Disease Detection",
        "pests": "Pests Observed:",
        "pest_options": ["None (Healthy)", "Green Leafhopper", "Tea Mite", "Thrips", "Other"],
        "notes": "Observation Notes:",
        "upload": "Upload Plant Photo:",
        "submit": "Submit Data 🚀",
        "success": "Successfully submitted!"
    }
}

# DİL SEÇİMİ
st.sidebar.title("🌍 Language / Dil")
lang = st.sidebar.selectbox("", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[lang]

st.title(t["title"])
st.subheader(t["subtitle"])

tab1, tab2 = st.tabs([t["tab_entry"], t["tab_analytics"]])

with tab1:
    with st.form("gozlem_formu", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            gozlem_turu = st.selectbox(t["obs_type"], t["obs_options"])
            rakim = st.number_input(t["altitude"], min_value=0, max_value=2500)
        with col_b:
            hava_durumu = st.selectbox(t["weather"], t["weather_options"])
            stres_skoru = st.slider(t["stress"], 1, 5, 3, help=t["stress_help"])
        
        # ZARARLI REHBERİ
        st.write(f"**{t['pest_title']}**")
        with st.expander(t["pest_guide"]):
            c1, c2, c3 = st.columns(3)
            c1.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Empoasca_decipiens.jpg", caption="Yeşil Çay Cücesi")
            c2.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Polyphagotarsonemus_latus.jpg", caption="Çay Akarı")
            c3.image("https://upload.wikimedia.org/wikipedia/commons/2/25/Heliothrips_haemorrhoidalis.jpg", caption="Trips")
            
        zararlilar = st.multiselect(t["pests"], t["pest_options"], default=[t["pest_options"][0]])
        gozlem_notlari = st.text_area(t["notes"])
        uploaded_file = st.file_uploader(t["upload"], type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            if uploaded_file is None:
                st.error("Lütfen bir fotoğraf yükleyin!")
            else:
                bytes_data = uploaded_file.read()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                payload = {
                    "Tarih": datetime.now().strftime("%d-%m-%Y"),
                    "Gozlem_Turu": gozlem_turu,
                    "Rakim": int(rakim),
                    "Hava_Durumu": hava_durumu,
                    "Stres_Skoru": int(stres_skoru),
                    "Zararlilar": ", ".join(zararlilar),
                    "Notlar": gozlem_notlari,
                    "Foto_Base64": base64_image
                }
                try:
                    requests.post(WEB_APP_URL, json=payload)
                    st.success(t["success"])
                except:
                    st.error("Bağlantı hatası!")

with tab2:
    try:
        csv_url = DEFAULT_GOOGLE_SHEET_URL.split("/edit")[0] + "/export?format=csv"
        df = pd.read_csv(csv_url)
        st.write(df)
    except:
        st.info("Veriler henüz yüklenemedi.")
