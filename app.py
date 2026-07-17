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
        "form": "Saha Gözlem Formu", "type": "Gözlem Türü", "alt": "Rakım", 
        "weather": "Hava Durumu", "stress": "Stres Skoru", "notes": "Notlar", 
        "photo": "Bitki Fotoğrafı", "submit": "Veriyi Gönder", "ph": "Toprak pH Değeri"
    },
    "English": {
        "title": "🌱 Future Farmers: Citizen Science Portal",
        "tab1": "📊 Data Entry", "tab2": "📈 Ecological Analysis",
        "form": "Field Observation Form", "type": "Observation Type", "alt": "Altitude", 
        "weather": "Weather", "stress": "Stress Score", "notes": "Notes", 
        "photo": "Plant Photo", "submit": "Submit Data", "ph": "Soil pH Level"
    }
}

t = texts[lang]
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

st.title(t["title"])
tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

with tab1:
    st.header(t["form"])
    gozlem_turu = st.selectbox(t["type"], ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
    
    with st.form("gozlem_formu", clear_on_submit=True):
        rakim = st.number_input(t["alt"], 0, 2000, 200)
        hava = st.selectbox(t["weather"], ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"])
        
        ph_degeri = None
        if gozlem_turu == "Toprak Analizi":
            ph_degeri = st.number_input(t["ph"], 0.0, 14.0, 7.0)
            
        if gozlem_turu == "Böcek Analizi":
            st.markdown("### 🔍 Böcek Analizi Rehberi")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("[Çay Kurdu (Eupoecilia ambiguella)](https://www.google.com/search?q=Eupoecilia+ambiguella+tea)")
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Eupoecilia_ambiguella.jpg/320px-Eupoecilia_ambiguella.jpg")
            with col2:
                st.markdown("[Çay Çekirgesi (Empoasca decipiens)](https://www.google.com/search?q=Empoasca+decipiens+tea)")
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Empoasca_decipiens.jpg/320px-Empoasca+decipiens.jpg")
        
        stres = st.slider(t["stress"], 1, 5, 1)
        notlar = st.text_area(t["notes"])
        foto = st.camera_input(t["photo"])
        
        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            payload = {
                "Tarih": datetime.datetime.now().isoformat(),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava": hava,
                "Stres": stres,
                "Notlar": notlar,
                "PH": ph_degeri if ph_degeri else 0,
                "Foto": base64.b64encode(foto.read()).decode() if foto else "Yok"
            }
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=15)
                if response.status_code == 200:
                    st.success("Veri başarıyla gönderildi!")
                else:
                    st.error(f"Hata: {response.text}")
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header(t["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        if not df.empty:
            fig = px.scatter(df, x="Rakim", y="Stres", color="Hava", size="Stres", title="Rakım vs. Stres Analizi")
            st.plotly_chart(fig, use_container_width=True)
            st.write("### 💡 Veri Yorumu")
            st.info("Grafik, yüksek rakımlı bölgelerdeki bitkilerin stres skorlarının sahil şeridine göre değişimini göstermektedir.")
    except Exception as e:
        st.warning("Veri havuzuna bağlanılamadı. Google Sheets'in 'Herkes görüntüleyebilir' olduğundan emin olun.")
