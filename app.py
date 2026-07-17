import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# Sayfa yapılandırması
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# Dil Seçimi
lang = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

texts = {
    "Türkçe": {
        "title": "🌱 Future Farmers: Vatandaş Bilimi Portalı",
        "tab1": "📊 Veri Girişi", "tab2": "📈 Ekolojik Analiz",
        "form": "Saha Gözlem Formu", "date": "Tarih", "type": "Gözlem Türü",
        "alt": "Rakım", "weather": "Hava Durumu", "stress": "Stres Skoru",
        "notes": "Notlar", "photo": "Bitki Fotoğrafı", "submit": "Veriyi Gönder",
        "ph": "Toprak pH Değeri", "insect": "Böcek Analizi"
    },
    "English": {
        "title": "🌱 Future Farmers: Citizen Science Portal",
        "tab1": "📊 Data Entry", "tab2": "📈 Ecological Analysis",
        "form": "Field Observation Form", "date": "Date", "type": "Observation Type",
        "alt": "Altitude", "weather": "Weather", "stress": "Stress Score",
        "notes": "Notes", "photo": "Plant Photo", "submit": "Submit Data",
        "ph": "Soil pH Level", "insect": "Insect Analysis"
    }
}

t = texts[lang]
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

st.title(t["title"])
tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

with tab1:
    st.header(t["form"])
    
    # Form dışı seçim alanı (Dinamik görünüm için)
    gozlem_turu = st.selectbox(t["type"], ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
    
    with st.form("gozlem_formu", clear_on_submit=True):
        tarih = datetime.datetime.now().isoformat()
        rakim = st.number_input(t["alt"], 0, 2000, 200)
        hava = st.selectbox(t["weather"], ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"])
        
        # pH Alanı: Sadece Toprak Analizi ise görünür
        ph_degeri = None
        if gozlem_turu == "Toprak Analizi":
            ph_degeri = st.number_input(t["ph"], 0.0, 14.0, 7.0)
            
        # Böcek Rehberi: Sadece Böcek Analizi ise görünür
        if gozlem_turu == "Böcek Analizi":
            st.info(f"🔍 {t['insect']}")
            st.markdown("- [Çay Kurdu (Eupoecilia ambiguella)](https://www.google.com/search?q=çay+kurdu+zararlısı)")
            st.markdown("- [Çay Çekirgesi (Empoasca decipiens)](https://www.google.com/search?q=çay+çekirgesi)")
        
        stres = st.slider(t["stress"], 1, 5, 1)
        notlar = st.text_area(t["notes"])
        foto = st.camera_input(t["photo"])
        
        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            payload = {
                "Tarih": tarih, "Gozlem_Turu": gozlem_turu, "Rakim": rakim, 
                "Hava": hava, "Stres": stres, "Notlar": notlar, 
                "PH": ph_degeri, "Foto": "Test" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=10)
                st.success("Veri başarıyla gönderildi!")
            except: 
                st.error("Bağlantı hatası. Lütfen API URL'sini kontrol edin.")

with tab2:
    st.header(t["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Sütun isimlerini kontrol ederek görselleştirme
        if not df.empty:
            fig = px.scatter(df, x="Rakim", y="Stres", color="Hava", size="Stres", title="Rakım vs. Stres Analizi")
            st.plotly_chart(fig, use_container_width=True)
            st.write("### 💡 Veri Yorumu")
            st.info("Grafik, yüksek rakımlı bölgelerdeki bitkilerin stres skorlarının sahil şeridine göre değişimini göstermektedir. Veriler, Rize'nin mikroklimatik yapısını anlamamıza yardımcı olur.")
        else:
            st.warning("Henüz veri bulunmuyor.")
    except Exception as e:
        st.info("Veri havuzuna bağlanılamadı. Lütfen Google Sheets'in 'Herkes görüntüleyebilir' modunda olduğundan emin olun.")
