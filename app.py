import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

st.set_page_config(page_title="Future Farmers Pro", layout="wide", page_icon="🌱")

# --- DATA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

# --- CONTENT ---
CONTENT = {
    "TR": {
        "title": "🌱 Future Farmers Pro: Bilimsel Araştırma",
        "tab1": "📊 Veri Girişi & Saha",
        "tab2": "📈 Ekolojik Analiz",
        "obs": "Gözlem Türü",
        "types": ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"],
        "alt": "Rakım (m)",
        "weather": "Hava Durumu",
        "w_opts": ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"],
        "stress": "Stres Skoru (1: Sağlıklı - 5: Kritik)",
        "ph": "Toprak pH Değeri",
        "notes": "Bilimsel Notlar",
        "photo": "Bitki Fotoğrafı",
        "submit": "Veriyi Kaydet ve Analize Gönder",
        "success": "Veri başarıyla kaydedildi!",
        "pest_title": "🔍 Rize Çay Zararlıları Rehberi",
        "sidebar_info": "MEB Müfredatı ile Uyumlu (10. Sınıf Ekosistem Ekolojisi & 12. Sınıf Bitki Biyolojisi). Sorgulayıcı Bilim (IBSE) odaklı saha çalışması."
    },
    "EN": {
        "title": "🌱 Future Farmers Pro: Scientific Portal",
        "tab1": "📊 Data Entry & Field",
        "tab2": "📈 Ecological Analysis",
        "obs": "Observation Type",
        "types": ["Tea Plant", "Pest Analysis", "Soil Analysis"],
        "alt": "Altitude (m)",
        "weather": "Weather",
        "w_opts": ["Sunny", "Cloudy", "Rainy", "Frost", "Snowy"],
        "stress": "Stress Score (1: Healthy - 5: Critical)",
        "ph": "Soil pH Level",
        "notes": "Scientific Notes",
        "photo": "Plant Photo",
        "submit": "Submit Data for Analysis",
        "success": "Data saved successfully!",
        "pest_title": "🔍 Rize Tea Pest Guide",
        "sidebar_info": "Aligned with Curriculum Standards. Fostering Inquiry-Based Science Education (IBSE) skills through systematic data collection."
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("🌍 Ayarlar")
    lang = st.radio("Dil / Language", ["TR", "EN"])
    c = CONTENT[lang]
    st.markdown("---")
    st.write("### 📚 Pedagojik Kılavuz")
    st.info(c["sidebar_info"])

st.title(c["title"])
tab1, tab2 = st.tabs([c["tab1"], c["tab2"]])

with tab1:
    gozlem_turu = st.selectbox(c["obs"], c["types"])
    
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            rakim = st.number_input(c["alt"], 0, 2000, 200)
            hava = st.selectbox(c["weather"], c["w_opts"])
        with col2:
            stres = st.slider(c["stress"], 1, 5, 1)
            
            if stres == 1: 
                st.success("🟢 1 - Sağlıklı: Bitki canlı, yapraklar parlak ve kompakt yapıda.")
            elif stres == 2: 
                st.info("🟡 2 - Hafif Stres: Yapraklarda hafif renk değişimi veya yavaş büyüme gözlemleniyor.")
            elif stres == 3: 
                st.warning("🟠 3 - Orta Stres: Belirgin yaprak solgunluğu, uç kurumaları veya zararlı izleri mevcut.")
            elif stres == 4: 
                st.error("🔴 4 - Ciddi Stres: Kurumalar, ciddi zararlı tahribatı veya gövde formunda bozulma.")
            elif stres == 5: 
                st.error("💀 5 - Kritik: Bitki canlılığını kaybetmek üzere, acil müdahale gerekli.")
            
            ph_degeri = 0.0
            if gozlem_turu == "Toprak Analizi":
                ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0)
        
        zararli_turu = "Yok"
        if gozlem_turu == "Böcek Analizi":
            zararli_turu = st.selectbox("Tespit Edilen Zararlı", ["Sarı Çay Akarı", "Çay Koşnili", "Çay Filiz Güvesi", "Vampir Kelebek", "Kahverengi Kokarca"])
        
        notlar = st.text_area(c["notes"])
        foto = st.camera_input(c["photo"])
        
        if st.form_submit_button(c["submit"]):
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava_Durumu": hava,
                "Stres_Skoru": stres,
                "Notlar": f"{notlar} | Zararlı: {zararli_turu}",
                "PH": ph_degeri,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=15)
                st.success(c["success"])
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.header(c["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
        df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
        df = df.dropna(subset=['Rakim', 'Stres_Skoru'])
        
        if not df.empty:
            fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", title="Rakım ve Bitki Stresi Korelasyonu")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Veri havuzu hazırlanıyor...")
    except Exception as e:
        st.error("Analiz verisi yüklenemedi.")
