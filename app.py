import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# --- 2. AYARLAR ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"
# CSV Linkinizi buraya güncellediğinizden emin olun
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

# --- 3. DİNAMİK FORMU AYIRMA ---
# Seçimi formun dışına alıyoruz ki her değişimde form sıfırlanmasın
gozlem_turu = st.sidebar.selectbox("Gözlem Türü / Observation Type", ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])

st.title("🌱 Future Farmers Pro")
tab1, tab2 = st.tabs(["📊 Veri Girişi", "📈 Ekolojik Analiz"])

with tab1:
    st.header(f"Seçilen: {gozlem_turu}")
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input("Rakım (m)", 0, 2000, 200)
        hava = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"])
        stres = st.slider("Stres Skoru", 1, 5, 1)
        
        # Dinamik Alanlar
        ph_degeri = 0
        if gozlem_turu == "Toprak Analizi":
            ph_degeri = st.number_input("Toprak pH Değeri", 0.0, 14.0, 7.0)
        
        if gozlem_turu == "Böcek Analizi":
            st.info("🔍 Böcek Analizi Modülü Aktif")
            st.markdown("- [Çay Kurdu](https://www.google.com/search?q=Eupoecilia+ambiguella)")
            st.markdown("- [Çay Çekirgesi](https://www.google.com/search?q=Empoasca+decipiens)")

        notlar = st.text_area("Notlar")
        foto = st.camera_input("Bitki Fotoğrafı")
        
        submit = st.form_submit_button("Veriyi Gönder")
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().isoformat(),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava": hava,
                "Stres": stres,
                "Notlar": notlar,
                "PH": ph_degeri,
                "Foto": "Yok" if not foto else "Var" # Kod karışmasın diye test amaçlı kısaltıldı
            }
            try:
                res = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if res.status_code == 200:
                    st.success("Veri başarıyla gönderildi!")
                else:
                    st.error("API Hatası: " + res.text)
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header("📈 Ekolojik Analiz")
    try:
        # Debug için veriyi çekmeyi deniyoruz
        df = pd.read_csv(SHEET_CSV_URL)
        
        if not df.empty:
            # Grafik
            fig = px.scatter(df, x="Rakim", y="Stres", color="Hava", size="Stres", title="Rakım ve Stres İlişkisi")
            st.plotly_chart(fig, use_container_width=True)
            
            # Yorum
            st.info("💡 Veri Yorumu: Rize havzasında yükseklik arttıkça bitki stres skorlarının değişimi izlenmektedir.")
        else:
            st.warning("Tablo boş görünüyor.")
            
    except Exception as e:
        st.error(f"VERİ HAVUZUNA BAĞLANILAMADI. Hata detay: {e}")
        st.write("Lütfen Google Sheets 'Web'de Yayınla' (Publish to web) ayarlarının aktif olduğundan emin olun.")
