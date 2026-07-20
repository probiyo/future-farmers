import streamlit as st
import pandas as pd
import requests
import json
import base64
from datetime import datetime

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱")
st.title("🌱 Future Farmers Pro")

gozlem_turu = st.selectbox("Gözlem Türü", ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
rakim = st.number_input("Rakım (m)", min_value=0, max_value=2000, value=200)
hava_durumu = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağışlı", "Sisli"])

st.write("**Bitki Stres Skoru (1-5):**")
st.caption("1: Çok Sağlıklı | 2: Hafif Solgun | 3: Orta Derece Stres | 4: Ciddi Stres | 5: Kritik / Kuruma Riski")
stres_skoru = st.slider("Stres Skoru (1-5)", 1, 5, 1)

if gozlem_turu == "Böcek Analizi":
    st.info("Böcek popülasyon yoğunluğunu notlar kısmında belirtiniz.")

notlar = st.text_area("Notlar")
foto = st.camera_input("Bitki Fotoğrafı")

if st.button("Gönder"):
    if foto:
        # Fotoğrafı base64 formatına çevir
        bytes_data = foto.getvalue()
        foto_base64 = base64.b64encode(bytes_data).decode('utf-8')
        
        # Gönderilecek veri paketi
        payload = {
            "Tarih": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Gozlem_Turu": gozlem_turu,
            "Rakim": rakim,
            "Hava_Durumu": hava_durumu,
            "Stres_Skoru": stres_skoru,
            "Notlar": notlar,
            "Foto_Base64": foto_base64
        }
        
        # WEB_APP_URL buraya gelecek (Apps Script'ten aldığınız link)
        WEB_APP_URL = "BURAYA_KOPYALADIGINIZ_YENI_URL_YAPISTIRIN"
        
        try:
            response = requests.post(WEB_APP_URL, json=payload)
            if response.status_code == 200:
                st.success("Veri başarıyla kaydedildi!")
            else:
                st.error("Bağlantı hatası: " + str(response.status_code))
        except Exception as e:
            st.error("Hata oluştu: " + str(e))
    else:
        st.warning("Lütfen fotoğraf çekiniz.")
