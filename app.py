import streamlit as st
import pandas as pd
import requests
import datetime
import base64
import plotly.express as px

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# Google Apps Script'ten aldığın güncel URL'yi buraya yaz
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz1-G1Q6w1lZt12mJ2Q47PZ1L1S2V1I0r5w5t1w5w5w5w5w5w5w5w5w5/exec"

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱", "entry": "Veri Giriş Portalı", "analytics": "Bilimsel Analiz",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀", "success": "Veri başarıyla bilimsel havuza işlendi!",
        "error": "Veri gönderilemedi.", "obs_type": "Gözlem Nesnesi", "options": ["Çay", "Böcekler", "Diğer"],
        "bug_type": "Böcek Türü", "bug_options": ["Vampir Kelebek", "Çay Filiz Güvesi", "Çay Koşnili", "Mor Çay Akarı", "Diğer"],
        "alt": "Rakım (m)", "stress": "Bitki Sağlık ve Stres Skoru (1-5)",
        "weather": "Hava Durumu", "weather_options": ["Güneşli", "Bulutlu", "Kapalı", "Yağmurlu", "Sisli", "Don", "Karlı"],
        "camera_title": "📸 Kamera ile Fotoğraf Çek", "upload_title": "📁 Veya Galeriden Yükle", "notes": "Gözlem Notlarınız"
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱", "entry": "Data Entry Portal", "analytics": "Scientific Analysis",
        "submit": "Submit to Scientific Database 🚀", "success": "Data processed successfully!",
        "error": "Data could not be sent.", "obs_type": "Observation Type", "options": ["Tea", "Pests", "Other"],
        "bug_type": "Select Pest Type", "bug_options": ["Vampire Bug", "Tea Shoot Borer", "Tea Scale Insect", "Purple Tea Mite", "Other"],
        "alt": "Altitude (m)", "stress": "Plant Health & Stress Score (1-5)",
        "weather": "Weather", "weather_options": ["Sunny", "Cloudy", "Overcast", "Rainy", "Foggy", "Frost", "Snowy"],
        "camera_title": "📸 Take Photo with Camera", "upload_title": "📁 Or Upload from Gallery", "notes": "Observation Notes"
    }
}

st.sidebar.title("Language / Dil")
lang = st.sidebar.selectbox("", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[lang]

tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        obs_type = st.selectbox(t["obs_type"], t["options"])
        bug_type = st.selectbox(t["bug_type"], t["bug_options"]) if obs_type in ["Böcekler", "Pests"] else "Yok"
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
            response = requests.post(WEB_APP_URL, json=payload)
            if response.status_code == 200:
                st.success(t["success"])
            else:
                st.error(t["error"])
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")

with tab2:
    st.header(t["analytics"])
    # Buraya kendi Google Sheets Yayınla linkini yapıştır
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"
    
    @st.cache_data(ttl=60)
    def load_data():
        return pd.read_csv(SHEET_CSV_URL)

    try:
        df = load_data()
        # Sütun isimlerini eşleştiriyoruz
        df = df.rename(columns={
            "Rakım (m)": "Rakim",
            "Sağlık/Stres Skoru": "Stres_Skoru"
        })
        
        df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
        df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
        df = df.dropna(subset=['Rakim', 'Stres_Skoru'])
        
        # Bilimsel Analiz Grafiği
        fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", title="Rakım vs. Fizyolojik Stres ($S_s$) Korelasyonu")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.info("Veri havuzu güncelleniyor...")
