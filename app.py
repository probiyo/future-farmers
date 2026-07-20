import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- STREAMING_CHUNK:Initializing configuration and data sources ---
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

# --- STREAMING_CHUNK:Defining multilingual UI content ---
CONTENT = {
    "TR": {
        "title": "🌱 Future Farmers Pro",
        "tab1": "📊 Veri Girişi",
        "tab2": "📈 Ekolojik Analiz",
        "obs": "Gözlem Detayları",
        "weather": "Hava Durumu",
        "w_opts": ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"],
        "stress": "Bitki Stres Skoru (1-5)",
        "ph": "Toprak pH",
        "pest": "Zararlı Analizi (Opsiyonel)",
        "pest_opts": ["Yok", "Çay Filiz Güvesi", "Çay Koşnili", "Vampir Kelebek", "Kahverengi Kokarca"],
        "notes": "Ek Notlar",
        "photo": "Bitki Fotoğrafı",
        "submit": "Veriyi Gönder",
        "success": "Veri başarıyla kaydedildi!"
    }
}
c = CONTENT["TR"] # Varsayılan TR

st.title(c["title"])
tab1, tab2 = st.tabs([c["tab1"], c["tab2"]])

# --- STREAMING_CHUNK:Rendering main form logic ---
with tab1:
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            rakim = st.number_input("Rakım (m)", 0, 2000, 200)
            hava = st.selectbox(c["weather"], c["w_opts"])
            stres = st.slider(c["stress"], 1, 5, 1)
        with col2:
            ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0)
            zararli_turu = st.selectbox(c["pest"], c["pest_opts"])
            notlar = st.text_area(c["notes"])
        
        foto = st.camera_input(c["photo"])
        submit = st.form_submit_button(c["submit"])
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Rakim": rakim,
                "Hava_Durumu": hava,
                "Stres_Skoru": stres,
                "PH": ph_degeri,
                "Zararli": zararli_turu,
                "Notlar": notlar,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=15)
                st.success(c["success"])
            except Exception as e:
                st.error(f"Error: {e}")

# --- STREAMING_CHUNK:Rendering analysis charts ---
with tab2:
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        st.subheader("Veri Görselleştirme")
        if not df.empty:
            fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Zararli", title="Rakım ve Zararlı Stres İlişkisi")
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Veri bekleniyor...")
