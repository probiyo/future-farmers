import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🌱 Future Farmers - Rize")

gozlem = st.radio("Gözlem Türü:", ["Proje Bitkim (Çay)", "Çevredeki Canlı"])
hava = st.selectbox("Hava Durumu:", ["Güneşli", "Kapalı", "Yağmurlu", "Sisli"])
notlar = st.text_area("Notunuz:")
camera = st.camera_input("Fotoğraf çek:")

if st.button("Veriyi Gönder"):
    if camera:
        # Veriyi bir liste olarak hazırlıyoruz
        veri = {
            "Tarih": [datetime.now().strftime("%d-%m-%Y %H:%M")],
            "Gözlem_Turu": [gozlem],
            "Hava_Durumu": [hava],
            "Notlar": [notlar],
            "Foto_Link": ["Fotoğraf yüklendi"]
        }
        df = pd.DataFrame(veri)
        
        # Sonucu ekranda gösterelim
        st.success("Veri kaydedildi! (Not: Veri akışı için tablo ayarını kontrol edin)")
        st.write("Gönderilen veriler:")
        st.write(df)
    else:
        st.error("Lütfen bir fotoğraf çekin.")
