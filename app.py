import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# Google Apps Script URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

st.title("🌱 Future Farmers: Vatandaş Bilimi Portalı")
tab1, tab2 = st.tabs(["📊 Veri Girişi", "📈 Ekolojik Analiz"])

with tab1:
    st.header("Saha Gözlem Formu")
    with st.form("gozlem_formu"):
        tarih = st.text_input("Tarih", value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        gozlem_turu = st.selectbox("Gözlem Türü", ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
        rakim = st.number_input("Rakım (m)", min_value=0, max_value=2000, value=200)
        hava = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağmurlu", "Sisli", "Don", "Karlı"])
        stres = st.slider("Stres Skoru (1: Sağlıklı, 5: Kritik)", 1, 5, 1)
        notlar = st.text_area("Gözlem Notları")
        foto = st.camera_input("Bitki Fotoğrafı Çek")
        
        submitted = st.form_submit_button("Veriyi Gönder")
        
        if submitted:
            foto_base64 = "Test_Verisi"
            if foto is not None:
                foto_base64 = base64.b64encode(foto.read()).decode('utf-8')
            
            payload = {
                "Tarih": tarih, "Gozlem_Turu": gozlem_turu, "Rakim": rakim,
                "Hava_Durumu": hava, "Stres_Skoru": stres, "Notlar": notlar,
                "Foto_Base64": foto_base64
            }
            
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success("Veri başarıyla kaydedildi!")
                else:
                    st.error(f"Hata: {response.text}")
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header("Ekolojik Analiz Havuzu")
    try:
        # CSV Verisini çekiyoruz
        df = pd.read_csv(SHEET_CSV_URL)
        
        # Sütun isimlerini tablonuzdaki başlıklarla eşleştiriyoruz
        rename_map = {
            "Rakım (m)": "Rakim", 
            "Sağlık/Stres Skoru": "Stres_Skoru",
            "Hava Durumu": "Hava_Durumu"
        }
        df = df.rename(columns=rename_map)
        
        if not df.empty and "Rakim" in df.columns:
            fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", 
                             size="Stres_Skoru", title="Rakım vs. Stres Korelasyonu",
                             hover_data=["Gozlem Notları"])
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df)
        else:
            st.info("Tablo şu an boş veya sütun başlıkları eşleşmiyor. Lütfen kontrol edin.")
    except Exception as e:
        st.error(f"Veri havuzu yüklenirken bir hata oluştu: {e}")
