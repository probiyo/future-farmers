import streamlit as st
import requests
import json
import base64
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Future Farmers - Portal", page_icon="🌱", layout="wide")

# API ve E-Tablo Ayarları
# Lütfen buraya kendi Google Apps Script URL'nizi ve Sheet URL'nizi yapıştırın!
WEB_APP_URL = "BURAYA_GOOGLE_APPS_SCRIPT_URLNIZI_YAZIN"
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/edit?gid=0#gid=0"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-title { color: #113425; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #4a5c53; font-size: 1.1rem; text-align: center; margin-bottom: 30px; }
    .interpretation-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 25px; margin-top: 25px; }
    .stButton>button { background-color: #113425 !important; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; height: 48px; border: none; }
    </style>
""", unsafe_allow_html=True)

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Projesi Gözlem, Mikroklima & Bilimsel Analiz Portalı",
        "tab_entry": "📝 Veri Giriş Portalı",
        "tab_analytics": "📊 Bilimsel Analiz & Grafikler",
        "obs_type": "Gözlem Nesnesi:",
        "obs_options": ["Proje Bitkim (Çay)", "Diğer Tarım Bitkisi"],
        "altitude": "Rakım (Metre):",
        "weather": "Hava Durumu:",
        "weather_options": ["Güneşli", "Parçalı Bulutlu", "Kapalı", "Yağmurlu", "Sisli"],
        "stress": "Bitki Sağlık ve Stres Skoru (1-5):",
        "stress_help": "1: Çok Sağlıklı, 2: Hafif Stres (Yaprak kenarı kuruması), 3: Normal Gelişim, 4: Belirgin Stres (Solgunluk), 5: Kritik Stres (Kuruma/Yoğun Parazit).",
        "pests": "Görülen Zararlılar:",
        "pest_options": ["Yok (Sağlıklı)", "Yeşil Çay Cücesi (Empoasca decipiens)", "Çay Akarı (Polyphagotarsonemus latus)", "Trips (Heliothrips haemorrhoidalis)", "Diğer"],
        "notes": "Gözlem Notlarınız:",
        "photo_upload_label": "Bitki Fotoğrafı Yükle:",
        "submit_btn": "Verileri Gönder 🚀",
        "guide_title": "🔍 Bilimsel Grafik Yorumlama Rehberi",
        "guide_text": "📈 <b>Rakım Korelasyonu:</b> Noktalar sağa doğru yükseliyorsa, yüksek rakımlarda rüzgar ve soğuk stresi baskındır.<br><br>🌧️ <b>Hava Etkisi:</b> Yağmurlu günlerde stres düşüyorsa, bölgede mikro-kuraklık problemi var demektir."
    }
}

t = translations["Türkçe 🇹🇷"]
st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

tab_form, tab_analysis = st.tabs([t["tab_entry"], t["tab_analytics"]])

with tab_form:
    with st.form("gozlem_formu"):
        gozlem_turu = st.selectbox(t["obs_type"], t["obs_options"])
        rakim = st.number_input(t["altitude"], min_value=0, max_value=2500)
        hava_durumu = st.selectbox(t["weather"], t["weather_options"])
        stres_skoru = st.slider(t["stress"], 1, 5, 3, help=t["stress_help"])
        
        # Zararlı Teşhis Kılavuzu
        st.subheader("⚠️ Zararlı ve Hastalık Tespiti")
        with st.expander("📖 Zararlı Tanıma Rehberi (Görsel Destekli)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Empoasca_decipiens.jpg/320px-Empoasca_decipiens.jpg", caption="Yeşil Çay Cücesi")
            with col2:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Polyphagotarsonemus_latus.jpg/320px-Polyphagotarsonemus_latus.jpg", caption="Çay Akarı")
            with col3:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Heliothrips_haemorrhoidalis.jpg/320px-Heliothrips_haemorrhoidalis.jpg", caption="Trips")
        
        zararlilar = st.multiselect(t["pests"], t["pest_options"], default=["Yok (Sağlıklı)"])
        gozlem_notlari = st.text_area(t["notes"])
        uploaded_file = st.file_uploader(t["photo_upload_label"], type=["jpg", "png"])
        
        submitted = st.form_submit_button(t["submit_btn"])
        
        if submitted:
            if uploaded_file is None:
                st.warning("Lütfen bir bitki fotoğrafı yükleyin.")
            else:
                with st.spinner("Gönderiliyor..."):
                    bytes_data = uploaded_file.read()
                    base64_image = base64.b64encode(bytes_data).decode('utf-8')
                    payload = {
                        "Tarih": datetime.now().strftime("%d-%m-%Y"), 
                        "Gozlem_Turu": gozlem_turu, 
                        "Rakim": int(rakim), 
                        "Hava_durumu": hava_durumu, 
                        "Stres_Skoru": int(stres_skoru),
                        "Zararlilar": ", ".join(zararlilar),
                        "Notlar": gozlem_notlari, 
                        "Foto_Base64": base64_image
                    }
                    try:
                        requests.post(WEB_APP_URL, json=payload)
                        st.success("Başarıyla kaydedildi!")
                    except:
                        st.error("Bağlantı hatası oluştu.")

with tab_analysis:
    try:
        csv_url = DEFAULT_GOOGLE_SHEET_URL.split("/edit")[0] + "/export?format=csv"
        df = pd.read_csv(csv_url)
        
        # Veri temizleme
        df["Rakim"] = pd.to_numeric(df.iloc[:, 2], errors='coerce')
        df["Stres_Skoru"] = pd.to_numeric(df.iloc[:, 4], errors='coerce')
        
        # Metrikler
        col1, col2, col3 = st.columns(3)
        col1.metric("Toplam Gözlem", len(df))
        col2.metric("Ort. Rakım", f"{int(df['Rakim'].mean())} m" if not df['Rakim'].isna().all() else "0 m")
        col3.metric("Ort. Stres", f"{round(df['Stres_Skoru'].mean(), 1)} / 5" if not df['Stres_Skoru'].isna().all() else "0 / 5")
        
        # Grafikler
        c1, c2 = st.columns(2)
        c1.subheader("Rakım - Stres Korelasyonu")
        c1.scatter_chart(data=df, x="Rakim", y="Stres_Skoru")
        c2.subheader("Hava Durumu - Stres Analizi")
        c2.bar_chart(data=df.groupby("Hava_Durumu")["Stres_Skoru"].mean())
        
        with st.expander(f"📖 {t['guide_title']}"):
            st.markdown(f"<div class='interpretation-card'>{t['guide_text']}</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.info("E-Tablo verileri henüz yüklenemedi. İlk verinizi girerek sistemi aktive edebilirsiniz.")


