import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- CONFIG ---
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# --- DATA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

st.title("🌱 Future Farmers Pro")
tab1, tab2 = st.tabs(["📊 Veri Girişi", "📈 Ekolojik Analiz"])

with tab1:
    # 1. Adım: Dinamik seçim
    gozlem_turu = st.selectbox("Gözlem Türü", ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input("Rakım (m)", 0, 2000, 200)
        hava = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"])
        stres = st.slider("Stres Skoru", 1, 5, 1)
        
        # 2. Adım: pH Alanı (Sadece Toprak Analizi seçilirse görünür)
        ph_degeri = 0
        if gozlem_turu == "Toprak Analizi":
            ph_degeri = st.number_input("Toprak pH Değeri", 0.0, 14.0, 7.0)
        
        # 3. Adım: Böcek Rehberi (Sadece Böcek Analizi seçilirse görünür)
        if gozlem_turu == "Böcek Analizi":
            st.info("🔍 Böcek Analiz Rehberi")
            st.markdown("- [Çay Kurdu](https://www.google.com/search?q=çay+kurdu+zararlısı)")
            st.markdown("- [Çay Çekirgesi](https://www.google.com/search?q=çay+çekirgesi)")
        
        notlar = st.text_area("Notlar")
        foto = st.camera_input("Bitki Fotoğrafı")
        
        submit = st.form_submit_button("Veriyi Gönder")
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava_Durumu": hava,
                "Stres_Skoru": stres,
                "Notlar": notlar,
                "PH": ph_degeri,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=10)
                st.success("Veri başarıyla gönderildi!")
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header("📈 Ekolojik Analiz")
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        if not df.empty:
            fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", 
                             title="Rakım ve Stres İlişkisi")
            st.plotly_chart(fig, use_container_width=True)
            st.info("💡 Veri Yorumu: Rize havzasında yükseklik arttıkça bitki stres skorlarının değişimi izlenmektedir.")
        else:
            st.warning("Henüz veri bulunmuyor.")
    except Exception as e:
        st.error(f"Veri havuzuna bağlanılamadı. Hata: {e}")
