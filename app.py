import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# URL'yi senin verdiğin ile güncelledim
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "success": "Veriler başarıyla işlendi!",
        "error": "Veri gönderilemedi. Lütfen tarayıcı izinlerini kontrol edin.",
        "obs_type": "Gözlem Nesnesi",
        "options": ["Çay", "Böcekler", "Diğer"],
        "bug_type": "Böcek Türü",
        "bug_options": ["Yeşil Cırcır Böceği", "Kırmızı Örümcek", "Diğer"],
        "alt": "Rakım (Metre)",
        "stress": "Bitki Sağlık ve Stres Skoru (1-5)",
        "stress_help": "1: Çok Sağlıklı, 5: Çok Stresli",
        "weather": "Hava Durumu",
        "weather_options": ["Güneşli", "Kapalı", "Yağmurlu"],
        "camera": "Kamera ile Çek",
        "upload": "Veya Dosya Yükle",
        "notes": "Gözlem Notlarınız"
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "entry": "Data Entry Portal",
        "analytics": "Scientific Analysis",
        "submit": "Submit to Scientific Database 🚀",
        "success": "Data processed successfully!",
        "error": "Data could not be sent. Please check browser permissions.",
        "obs_type": "Observation Type",
        "options": ["Tea", "Pests", "Other"],
        "bug_type": "Pest Type",
        "bug_options": ["Green Grasshopper", "Red Spider", "Other"],
        "alt": "Altitude (Meters)",
        "stress": "Plant Health & Stress Score (1-5)",
        "stress_help": "1: Very Healthy, 5: Very Stressed",
        "weather": "Weather",
        "weather_options": ["Sunny", "Cloudy", "Rainy"],
        "camera": "Take Photo",
        "upload": "Or Upload File",
        "notes": "Observation Notes"
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
            obs_type = st.selectbox(t["obs_type"], t["options"])
            
            bug_type = "Yok"
            # Böcek seçimi görünürlük mantığı
            if obs_type in ["Böcekler", "Pests"]:
                bug_type = st.selectbox(t["bug_type"], t["bug_options"])
            
            alt = st.number_input(t["alt"], 0, 2500)
            stres_val = st.select_slider(t["stress"], options=[1, 2, 3, 4, 5], help=t["stress_help"])
            
        with col2:
            weather = st.selectbox(t["weather"], t["weather_options"])
            uploaded_file = st.camera_input(t["camera"])
            file_upload = st.file_uploader(t["upload"], type=['jpg', 'jpeg', 'png'])
            notes = st.text_area(t["notes"])

        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            image_to_process = uploaded_file if uploaded_file else file_upload
            foto_base64 = "Test_Verisi"
            if image_to_process is not None:
                foto_bytes = image_to_process.getvalue()
                foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
            
            data = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": f"{obs_type} ({bug_type})" if bug_type != "Yok" else obs_type,
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
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/gviz/tq?tqx=out:csv&sheet=Sayfa1"
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        st.dataframe(df)
    except Exception as e:
        st.warning("Veriler henüz yüklenemedi veya boş.")
