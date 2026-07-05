import streamlit as st
import requests
from datetime import datetime

# --- AYARLAR ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzvSysth2wAg12-2y-tMCnek_pRkJsk40sWZ5Aa16j9Q79HTLqYucEiEDuHSYhFwkUF/exec"

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# --- DİL SÖZLÜĞÜ ---
translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "obs_type": "Gözlem Nesnesi",
        "obs_opts": ["Çay", "Diğer"],
        "altitude": "Rakım (Metre)",
        "weather": "Hava Durumu",
        "weather_opts": ["Güneşli", "Parçalı Bulutlu", "Kapalı", "Yağmurlu", "Sisli", "Don", "Karlı"],
        "stress_title": "Bitki Sağlık ve Stres Skoru (1-5)",
        "stress_opts": {
            1: "1: Çok Sağlıklı - Mükemmel Gelişim",
            2: "2: Hafif Stres - İzlenmeli",
            3: "3: Normal Gelişim - Stabil",
            4: "4: Belirgin Stres - Müdahale Gerekebilir",
            5: "5: Kritik Stres - Acil Müdahale!"
        },
        "photo_method": "Fotoğraf Metodu",
        "upload_lbl": "Dosya Yükle",
        "camera_lbl": "Kamera ile Çek",
        "pest_title": "⚠️ Zararlı Tanımlama Rehberi (Tıklayarak Araştır)",
        "pests": "Görülen Zararlılar",
        "pest_opts": ["Yok (Sağlıklı)", "Yeşil Çay Cücesi", "Çay Akarı", "Trips", "Vampir Kelebek (Metcalfa)"],
        "notes": "Gözlem Notlarınız",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "success": "Veriler başarıyla işlendi!"
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "entry": "Data Entry Portal",
        "analytics": "Scientific Analysis",
        "obs_type": "Observation Target",
        "obs_opts": ["Tea", "Other"],
        "altitude": "Altitude (Meters)",
        "weather": "Weather Condition",
        "weather_opts": ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Foggy", "Frost", "Snowy"],
        "stress_title": "Plant Health & Stress Score (1-5)",
        "stress_opts": {
            1: "1: Very Healthy - Excellent Growth",
            2: "2: Mild Stress - Monitor",
            3: "3: Normal Growth - Stable",
            4: "4: Significant Stress - Intervention Needed",
            5: "5: Critical Stress - Emergency Action!"
        },
        "photo_method": "Photo Method",
        "upload_lbl": "Upload File",
        "camera_lbl": "Take with Camera",
        "pest_title": "⚠️ Pest Identification Guide (Click to Search)",
        "pests": "Pests Observed",
        "pest_opts": ["None (Healthy)", "Green Leafhopper", "Tea Mite", "Thrips", "Vampire Butterfly (Metcalfa)"],
        "notes": "Observation Notes",
        "submit": "Submit to Scientific Database 🚀",
        "success": "Data processed successfully!"
    }
}

# --- ARAYÜZ ---
lang = st.sidebar.selectbox("Language / Dil", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[lang]

st.title(t["title"])
tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    with st.form("pro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            obs_type = st.selectbox(t["obs_type"], t["obs_opts"])
            alt = st.number_input(t["altitude"], 0, 2500)
            weather = st.selectbox(t["weather"], t["weather_opts"])
            
            st.write(f"**{t['stress_title']}**")
            stres_val = st.select_slider("", options=[1, 2, 3, 4, 5], value=3)
            
            # Tüm ölçeği göster
            st.markdown("---")
            for i in range(1, 6):
                prefix = "✅ " if i == stres_val else "○ "
                st.write(f"{prefix} {t['stress_opts'][i]}")
            st.markdown("---")

        with col2:
            photo_choice = st.radio(t["photo_method"], [t["upload_lbl"], t["camera_lbl"]], horizontal=True)
            uploaded_file = None
            
            if photo_choice == t["upload_lbl"]:
                uploaded_file = st.file_uploader(t["upload_lbl"], type=['jpg', 'png', 'jpeg'])
            else:
                # Kamera için en yalın kullanım
                uploaded_file = st.camera_input(t["camera_lbl"])
                st.info("Kamera açılmazsa tarayıcı izinlerini kontrol edin.")
            
            st.write(f"**{t['pest_title']}**")
            for pest in t["pest_opts"]:
                if pest != "Yok (Sağlıklı)" and pest != "None (Healthy)":
                    search_url = f"https://www.google.com/search?q={pest}+Rize+çay+zararlısı"
                    st.markdown(f"- [{pest}]({search_url})")
            
            zararlilar = st.multiselect(t["pests"], t["pest_opts"])
            notes = st.text_area(t["notes"])

        submitted = st.form_submit_button(t["submit"])
        
        if submitted:
            if uploaded_file is None:
                st.warning("Lütfen fotoğraf ekleyin veya çekin.")
            else:
                st.success(t["success"])

with tab2:
    st.subheader(t["analytics"])
    st.info("Verileriniz Google Sheets'e aktarıldığında burada görünecektir.")
