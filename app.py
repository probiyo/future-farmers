import streamlit as st
import requests
import base64
from datetime import datetime

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "obs_type": "Gözlem Nesnesi",
        "obs_opts": ["Çay", "Diğer"],
        "altitude": "Rakım (Metre)",
        "weather": "Hava Durumu",
        "weather_opts": ["Güneşli", "Parçalı Bulutlu", "Kapalı", "Yağmurlu", "Sisli", "Don", "Karlı"],
        "stress_title": "Bitki Sağlık ve Stres Skoru (1-5)",
        "photo_method": "Fotoğraf Metodu",
        "upload_lbl": "Dosya Yükle",
        "camera_lbl": "Kamera ile Çek",
        "pests": "Görülen Zararlılar",
        "notes": "Gözlem Notlarınız",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "success": "Veriler başarıyla Google Sheets'e gönderildi!",
        "error": "Bağlantı hatası: "
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "entry": "Data Entry Portal",
        "analytics": "Scientific Analysis",
        "obs_type": "Observation Target",
        "obs_opts": ["Tea", "Other"],
        "altitude": "Altitude (Meters)",
        "weather": "Weather Condition",
        "weather_opts": ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Foggy", "Frost", "Snowy"],
        "stress_title": "Plant Health & Stress Score (1-5)",
        "photo_method": "Photo Method",
        "upload_lbl": "Upload File",
        "camera_lbl": "Take with Camera",
        "pests": "Pests Observed",
        "notes": "Observation Notes",
        "submit": "Submit to Scientific Database 🚀",
        "success": "Data sent successfully to Google Sheets!",
        "error": "Connection error: "
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
            obs_type = st.selectbox(t["obs_type"], t["obs_opts"])
            alt = st.number_input(t["altitude"], 0, 2500)
            weather = st.selectbox(t["weather"], t["weather_opts"])
            stres_val = st.select_slider(t["stress_title"], options=[1, 2, 3, 4, 5], value=3)

        with col2:
            photo_choice = st.radio(t["photo_method"], [t["upload_lbl"], t["camera_lbl"]], horizontal=True)
            uploaded_file = None
            if photo_choice == t["upload_lbl"]:
                uploaded_file = st.file_uploader(t["upload_lbl"], type=['jpg', 'png', 'jpeg'])
            else:
                uploaded_file = st.camera_input(t["camera_lbl"])
            
            notes = st.text_area(t["notes"])

        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            if uploaded_file is None:
                st.warning("Lütfen fotoğraf ekleyin veya çekin.")
            else:
                with st.spinner("Veri Google'a gönderiliyor..."):
                    # Fotoğrafı Base64 formatına çevir
                    bytes_data = uploaded_file.getvalue()
                    foto_base64 = base64.b64encode(bytes_data).decode('utf-8')
                    
                    # Gönderilecek veri paketi
                    data_to_send = {
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Gozlem_Turu": obs_type,
                        "Rakim": alt,
                        "Hava_Durumu": weather,
                        "Stres_Skoru": stres_val,
                        "Notlar": notes,
                        "Foto_Base64": foto_base64
                    }
                    
                    try:
                        # Google Apps Script'e gönder
                        response = requests.post(WEB_APP_URL, json=data_to_send, timeout=15)
                        
                        if response.status_code == 200:
                            st.success(t["success"])
                        else:
                            st.error(f"Hata {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"{t['error']} {str(e)}")

with tab2:
    st.subheader(t["analytics"])
    st.info("Verileriniz Google Sheets'e aktarıldığında burada görünecektir.")
