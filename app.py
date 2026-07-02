import streamlit as st
from datetime import datetime
import urllib.request
import json
import base64

st.title("🌱 Future Farmers - Rize")

gozlem = st.radio("Gözlem Türü:", ["Proje Bitkim (Çay)", "Çevredeki Canlı"])
hava = st.selectbox("Hava Durumu:", ["Güneşli", "Kapalı", "Yağmurlu", "Sisli"])
notlar = st.text_area("Notunuz:")
camera = st.camera_input("Fotoğraf çek:")

URL = "https://script.google.com/macros/s/AKfycbxamU64AHCSNtW3uKjHC0qibj8tYExRKreXZp3iR9TtBc7b0jbs0YFXF_zbleovy0SJ/exec"

if st.button("Veriyi Gönder"):
    if camera:
        # Fotoğrafı internet üzerinden gönderebilmek için metne dönüştürüyoruz
        bytes_data = camera.getvalue()
        base64_photo = base64.b64encode(bytes_data).decode('utf-8')
        
        veri = {
            "Tarih": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Gözlem_Turu": gozlem,
            "Hava_Durumu": hava,
            "Notlar": notlar,
            "Foto_Base64": base64_photo
        }
        
        try:
            data = json.dumps(veri).encode('utf-8')
            req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as res:
                st.success("Veri ve Fotoğraf başarıyla arşive gönderildi! 🎉")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
    else:
        st.error("Lütfen bir fotoğraf çekin.")
