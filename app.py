import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests # Veriyi Google Sheets'e göndermek için

# --- AYARLAR ---
# Google Apps Script'ten aldığınız URL'yi buraya yapıştırın:
WEB_APP_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/edit?gid=0#gid=0"

# Streamlit sayfa ayarları
st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# Mock Veri (Analiz tabı için)
@st.cache_data
def get_sample_data():
    return pd.DataFrame({
        "Rakim": [0, 50, 70, 150, 300, 450, 600],
        "Stres_Skoru": [1, 2, 2, 3, 4, 4, 5],
        "Hava": ["Güneşli", "Güneşli", "Parçalı Bulutlu", "Sisli", "Yağmurlu", "Don", "Karlı"]
    })

# Dil Sözlüğü
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

# Arayüz
st.title(t["title"])
tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    with st.form("pro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            obs_type = st.selectbox(t["obs_type"], ["Çay", "Diğer"])
            alt = st.number_input(t["altitude"], 0, 2500)
            weather = st.selectbox(t["weather"], t["weather_options"])
            
            st.write(f"**{t['stress']}**")
            stres_val = st.select_slider("", options=[1, 2, 3, 4, 5], value=3)
            st.caption(t["stress_help"][stres_val])
            notes = st.text_area("Gözlem Notları")
            
        with col2:
            photo_choice = st.radio(t["photo_method"], [t["upload"], t["camera"]], horizontal=True)
            uploaded_file = None
            if photo_choice == t["upload"]:
                uploaded_file = st.file_uploader(t["upload"], type=['jpg', 'png'])
            else:
                uploaded_file = st.camera_input(t["camera"])
                
            with st.expander(t["pest_title"], expanded=True):
                p1, p2, p3 = st.columns(3)
                p1.image("https://via.placeholder.com/150/FF5733/FFFFFF?text=Yeşil+Çay+Cücesi", caption="Yeşil Çay Cücesi")
                p2.image("https://via.placeholder.com/150/33FF57/FFFFFF?text=Çay+Akarı", caption="Çay Akarı")
                p3.image("https://via.placeholder.com/150/3357FF/FFFFFF?text=Trips", caption="Trips")

        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            # Burası veri gönderim mantığı
            data_to_send = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": obs_type,
                "Rakim": alt,
                "Hava_Durumu": weather,
                "Stres_Skoru": stres_val,
                "Notlar": notes,
                "Foto_Base64": "Gelecek_Sürümde_Eklenecek" # Basitleştirilmiş versiyon
            }
            
            try:
                response = requests.post(WEB_APP_URL, json=data_to_send)
                if response.status_code == 200:
                    st.success(t["success"])
                else:
                    st.error(f"{t['error']} (Kod: {response.status_code})")
            except:
                st.warning("URL tanımlanmadı veya bağlantı kurulamadı. Lütfen WEB_APP_URL değişkenini kontrol edin.")

with tab2:
    st.subheader(t["chart_title"])
    df = get_sample_data()
    fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava", size="Stres_Skoru", 
                     title="Rakım Artışı ve Bitki Stres İlişkisi",
                     labels={"Rakim": "Rakım (m)", "Stres_Skoru": "Stres Skoru (1-5)"})
    st.plotly_chart(fig, use_container_width=True)
    
    st.line_chart(df.set_index("Rakim")["Stres_Skoru"])
