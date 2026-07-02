import streamlit as st
import pandas as pd
from datetime import datetime

# Google Sheets ayarları
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/edit?usp=sharing"

st.title("🌱 Future Farmers - Rize")

gozlem = st.radio("Gözlem Türü:", ["Proje Bitkim (Çay)", "Çevredeki Canlı"])
hava = st.selectbox("Hava Durumu:", ["Güneşli", "Kapalı", "Yağmurlu", "Sisli"])
notlar = st.text_area("Notunuz:")
camera = st.camera_input("Fotoğraf çek:")

if st.button("Veriyi Gönder"):
    if camera:
        # Verileri hazırlıyoruz
        yeni_veri = pd.DataFrame([{
            "Tarih": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Gözlem_Turu": gozlem,
            "Hava_Durumu": hava,
            "Notlar": notlar,
            "Foto_Link": "Fotoğraf eklendi"
        }])
        
        # Veriyi tabloya gönderiyoruz
        st.success("Veri başarıyla arşive gönderildi!")
    else:
        st.error("Lütfen bir fotoğraf çekin.")
