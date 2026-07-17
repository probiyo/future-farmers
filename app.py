import streamlit as st
import pandas as pd
import requests
import datetime
import base64
import plotly.express as px

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# Google Apps Script URL - Güncellediğinizden emin olun!
WEB_APP_URL ="https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱", "entry": "Veri Giriş Portalı", "analytics": "Bilimsel Analiz",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀", "success": "Veri başarıyla bilimsel havuza işlendi!",
        "error": "Veri gönderilemedi. Lütfen bağlantınızı kontrol edin.", "obs_type": "Gözlem Türü", "options": ["Çay", "Böcekler", "Diğer"],
        "bug_type": "Böcek Türü", "bug_options": ["Vampir Kelebek", "Çay Filiz Güvesi", "Çay Koşnili", "Mor Çay Akarı", "Diğer"],
        "alt": "Rakım (m)", "stress": "Sağlık/Stres Skoru (1-5)",
        "weather": "Hava Durumu", "weather_options": ["Güneşli", "Bulutlu", "Kapalı", "Yağmurlu", "Sisli", "Don", "Karlı"],
        "camera_title": "📸 Fotoğraf Çek", "upload_title": "📁 Veya Yükle", "notes": "Notlarınız"
    }
}

t = translations["Türkçe 🇹🇷"]

tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        obs_type = st.selectbox(t["obs_type"], t["options"])
        bug_type = st.selectbox(t["bug_type"], t["bug_options"]) if obs_type == "Böcekler" else "Yok"
        alt = st.number_input(t["alt"], 0, 2500, 0)
        stres_val = st.select_slider(t["stress"], [1, 2, 3, 4, 5])
        notes = st.text_area(t["notes"])
    with col2:
        weather = st.selectbox(t["weather"], t["weather_options"])
        camera_photo = st.camera_input(t["camera_title"])
        uploaded_photo = st.file_uploader(t["upload_title"], type=['jpg', 'png'])

    if st.button(t["submit"]):
        final_photo = camera_photo or uploaded_photo
        foto_base64 = base64.b64encode(final_photo.getvalue()).decode("utf-8") if final_photo else "Test_Verisi"
        
        payload = {
            "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Gozlem_Turu": obs_type if bug_type == "Yok" else f"Böcek: {bug_type}",
            "Rakim": alt,
            "Hava_Durumu": weather,
            "Stres_Skoru": stres_val,
            "Notlar": notes,
            "Foto_Base64": foto_base64
        }
        try:
            response = requests.post(WEB_APP_URL, json=payload, timeout=10)
            if response.status_code == 200:
                st.success(t["success"])
            else:
                st.error(t["error"])
        except Exception as e:
            st.error(f"Hata: {e}")

with tab2:
    st.header(t["analytics"])
    # Google Sheets Yayınla linki (CSV)
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"
    
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Sütun isimleri Sheets'tekiyle birebir olmalı
        df = df.rename(columns={"Rakım (m)": "Rakim", "Sağlık/Stres Skoru": "Stres_Skoru"})
        
        fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", title="Rakım vs. Stres Korelasyonu")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)
    except:
        st.info("Veri havuzu yükleniyor veya boş...")

