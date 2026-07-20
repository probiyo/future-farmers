import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- CONFIG ---
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# --- ZARARLI VE BİTKİ VERİ TABANI ---
PEST_DATABASE = {
    "Türkiye": {
        "Çay Bitkisi": ["Yok", "Çay Filiz Güvesi", "Çay Koşnili", "Vampir Kelebek", "Kahverengi Kokarca"],
        "Diğer": ["Yok", "Bölgesel Zararlı Gözlemlenmedi"]
    },
    "Belçika": {
        "Brassica oleracea (Brüksel Lahanası)": ["Yok", "Yaprak Biti (Aphids)", "Lahana Güvesi", "Toprak Piresi", "Salyangoz"],
        "Diğer": ["Yok", "Bölgesel Zararlı Gözlemlenmedi"]
    }
}

# --- DATA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

# --- MULTILINGUAL CONTENT ---
CONTENT = {
    "TR": {
        "title": "🌱 Future Farmers Pro",
        "tab1": "📊 Veri Girişi",
        "tab2": "📈 Ekolojik Analiz",
        "obs": "Gözlem Türü",
        "alt": "Rakım (m)",
        "weather": "Hava Durumu",
        "w_opts": ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"],
        "stress": "Stres Skoru (1-5)",
        "stress_desc": "1: Çok Sağlıklı | 2: Hafif Solgun | 3: Orta Derece Stres | 4: Ciddi Stres | 5: Kritik / Kuruma Riski",
        "ph": "Toprak pH Değeri",
        "notes": "Notlar",
        "photo": "Bitki Fotoğrafı",
        "submit": "Veriyi Gönder",
        "success": "Veri başarıyla gönderildi!",
        "pest_title": "🔍 Zararlı Rehberi"
    },
    "EN": {
        "title": "🌱 Future Farmers Pro",
        "tab1": "📊 Data Entry",
        "tab2": "📈 Ecological Analysis",
        "obs": "Observation Type",
        "alt": "Altitude (m)",
        "weather": "Weather",
        "w_opts": ["Sunny", "Cloudy", "Rainy", "Frost", "Snowy"],
        "stress": "Stress Score (1-5)",
        "stress_desc": "1: Very Healthy | 2: Slightly Wilted | 3: Moderate Stress | 4: Severe Stress | 5: Critical / Drying Risk",
        "ph": "Soil pH Level",
        "notes": "Notes",
        "photo": "Plant Photo",
        "submit": "Submit Data",
        "success": "Data sent successfully!",
        "pest_title": "🔍 Pest Guide"
    }
}

# --- SIDEBAR ---
country = st.sidebar.selectbox("Ülke Seçiniz", list(PEST_DATABASE.keys()))
lang = st.sidebar.radio("🌐 Language / Dil", ["TR", "EN"])
c = CONTENT[lang]

st.title(c["title"])
tab1, tab2 = st.tabs([c["tab1"], c["tab2"]])

with tab1:
    # --- DİNAMİK SEÇİM ---
    obs_options = list(PEST_DATABASE[country].keys())
    gozlem_turu = st.selectbox(c["obs"], obs_options)
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input(c["alt"], 0, 2000, 200)
        hava = st.selectbox(c["weather"], c["w_opts"])
        stres = st.slider(c["stress"], 1, 5, 1)
        st.caption(c["stress_desc"]) 
        
        col1, col2 = st.columns(2)
        with col1:
            ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0)
        with col2:
            # Ülke ve Bitkiye göre dinamik zararlı listesi
            zararli_turu = st.selectbox("Tespit Edilen Zararlı", PEST_DATABASE[country][gozlem_turu])
            
        notlar = st.text_area(c["notes"])
        col_cam1, col_cam2 = st.columns([1, 3])
        with col_cam1:
            foto = st.camera_input(c["photo"])
        
        submit = st.form_submit_button(c["submit"])
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": f"{gozlem_turu} ({country})",
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

    st.markdown(f"### {c['pest_title']}")
    for pest in PEST_DATABASE[country][gozlem_turu]:
        if pest != "Yok":
            st.markdown(f"- {pest}")

with tab2:
    # ... existing code ...
    st.header(c["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # ... existing code (rest of tab2)
    except Exception as e:
        st.error(f"Analiz verisi yüklenemedi: {e}")
