import streamlit as st
import pandas as pd
import requests
import datetime
import base64
import plotly.express as px

# 1. STREAMING_CHUNK:Konfigürasyon ve Başlatma
st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

# 2. STREAMING_CHUNK:Çeviri Sözlüğü
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
            st.success(t["success"]) if response.status_code == 200 else st.error(t["error"])
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")

# 4. STREAMING_CHUNK:Veri Analiz ve Görselleştirme Motoru
with tab2:
    st.header(t["analytics"])
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"
    
    @st.cache_data(ttl=60)
    def load_data():
        return pd.read_csv(SHEET_CSV_URL)

    try:
        df = load_data()
        
        # TABLO BAŞLIKLARINI EŞLEŞTİRME (Google Sheets'teki isimlere göre yeniden adlandırıyoruz)
        df = df.rename(columns={
            "Rakim": "Rakim",
            "Stres_Skoru": "Stres_Skoru",
            "Hava Durumu": "Hava_Durumu"
        })
        
        # Veri temizliği
        df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
        df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
        
        # Grafik için kullanılacak ana dataframe
        df_plot = df.dropna(subset=['Rakim', 'Stres_Skoru', 'Hava_Durumu'])
        
        # Plotly grafik
        fig = px.scatter(df_plot, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", 
                         title="Rakım vs. Fizyolojik Stres ($S_s$)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabloyu göster
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        st.write("Mevcut Sütun Başlıkları:", df.columns.tolist() if 'df' in locals() else "Tablo okunamadı.")
```eof
