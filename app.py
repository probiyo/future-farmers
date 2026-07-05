import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime

# Sayfa Ayarları (Geniş ekran, başlık ve ikon)
st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# Google Apps Script Web App URL'niz (SABİTLENDİ - DOKUNMAYIN)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "success": "Veriler başarıyla işlendi ve tabloya kaydedildi!",
        "error": "Veri gönderilemedi. Lütfen bağlantınızı kontrol edin.",
        "obs_type": "Gözlem Nesnesi (Ne Gözlemliyorsunuz?)",
        "options": ["Çay", "Böcekler", "Diğer"],
        "bug_type": "Böcek Türünü Seçiniz",
        "bug_options": ["Yeşil Cırcır Böceği", "Kırmızı Örümcek", "Çay Güvesi", "Diğer"],
        "alt": "Rakım (Deniz Seviyesinden Yükseklik - Metre)",
        "stress": "Bitki Sağlık ve Stres Skoru (1-5 Arası Değerlendirin)",
        "weather": "Hava Durumu",
        "weather_options": ["Güneşli", "Kapalı", "Yağmurlu", "Sisli"],
        "camera_title": "📸 Kamera İle Fotoğraf Çek",
        "upload_title": "📁 Veya Galeriden Fotoğraf Yükle",
        "notes": "Gözlem Notlarınız (İsteğe Bağlı)"
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "entry": "Data Entry Portal",
        "analytics": "Scientific Analysis",
        "submit": "Submit to Scientific Database 🚀",
        "success": "Data processed successfully!",
        "error": "Data could not be sent.",
        "obs_type": "Observation Type",
        "options": ["Tea", "Pests", "Other"],
        "bug_type": "Select Pest Type",
        "bug_options": ["Green Grasshopper", "Red Spider", "Tea Moth", "Other"],
        "alt": "Altitude (Meters)",
        "stress": "Plant Health & Stress Score (1-5)",
        "weather": "Weather",
        "weather_options": ["Sunny", "Cloudy", "Rainy", "Foggy"],
        "camera_title": "📸 Take Photo with Camera",
        "upload_title": "📁 Or Upload File",
        "notes": "Observation Notes"
    }
}

lang = st.sidebar.selectbox("Language / Dil Seçimi", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[lang]

st.title(t["title"])
tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    with st.form("pro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Gözlem Nesnesi Seçimi
            obs_type = st.selectbox(t["obs_type"], t["options"])
            
            # 2. Böcek Seçimi Mantığı (Açık ve Anlaşılır)
            bug_type = "Yok"
            if obs_type == "Böcekler" or obs_type == "Pests":
                st.info("Böcekler seçildi. Lütfen aşağıdaki listeden türü belirtin:")
                bug_type = st.selectbox(t["bug_type"], t["bug_options"])
            else:
                st.caption("ℹ️ Not: Böcek türü menüsünü görmek için yukarıdan 'Böcekler'i seçmelisiniz.")
            
            st.write("---") # Araya çizgi çektik
            
            # 3. Rakım ve Stres Skoru
            alt = st.number_input(t["alt"], min_value=0, max_value=2500, value=0)
            
            stres_val = st.select_slider(t["stress"], options=[1, 2, 3, 4, 5])
            # Stres açıklaması artık gizli değil, hep görünür:
            if lang == "Türkçe 🇹🇷":
                st.markdown("**ℹ️ Puanlama Rehberi:** \n* **1 Puan:** Çok Sağlıklı, hiç hasar yok \n* **3 Puan:** Orta derecede stres veya hafif kuruma \n* **5 Puan:** Çok Yüksek Stres, ağır hastalık veya kuruma")
            else:
                st.markdown("**ℹ️ Scoring Guide:** \n* **1:** Very Healthy \n* **5:** Very Stressed/Damaged")
            
            notes = st.text_area(t["notes"])

        with col2:
            weather = st.selectbox(t["weather"], t["weather_options"])
            st.write("---")
            
            # 4. Kamera Modülü
            st.subheader(t["camera_title"])
            if lang == "Türkçe 🇹🇷":
                st.caption("👇 Kameranız otomatik açılır. Görüntü netleşince resmin hemen altındaki **'Take Photo'** butonuna tıklayın.")
            uploaded_file = st.camera_input("Kamera", label_visibility="collapsed")
            
            st.write("---")
            
            # 5. Dosya Yükleme Modülü
            st.subheader(t["upload_title"])
            if lang == "Türkçe 🇹🇷":
                st.caption("👇 Veya cihazınızdaki hazır bir resmi buraya tıklayarak yükleyin ('Browse files' / 'Upload').")
            file_upload = st.file_uploader("Dosya", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

        st.write("---")
        submitted = st.form_submit_button(t["submit"], use_container_width=True)
        
        if submitted:
            # Resim önceliği: Kamera ile çekildiyse onu al, yoksa yükleneni al
            image_to_process = uploaded_file if uploaded_file else file_upload
            foto_base64 = "Test_Verisi"
            
            if image_to_process is not None:
                foto_bytes = image_to_process.getvalue()
                foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
            
            # Gönderilecek veriyi hazırlama
            data = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": f"{obs_type} ({bug_type})" if bug_type != "Yok" else obs_type,
                "Rakim": alt,
                "Hava_Durumu": weather,
                "Stres_Skoru": stres_val,
                "Notlar": notes,
                "Foto_Base64": foto_base64
            }
            
            # Google Script'e veriyi yollama
            try:
                with st.spinner('Veriler bilimsel ağa aktarılıyor... Lütfen bekleyin.'):
                    response = requests.post(WEB_APP_URL, json=data)
                    if response.status_code == 200:
                        st.success(t["success"])
                    else:
                        st.error(t["error"])
            except Exception as e:
                st.error(f"{t['error']} Sistem Mesajı: {e}")

with tab2:
    st.subheader(t["analytics"])
    # Tablo URL'si (Bu sadece okuma amaçlıdır, dokunmayın)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/gviz/tq?tqx=out:csv&sheet=Sayfa1"
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip()
        st.dataframe(df, use_container_width=True)
        
        # Basit bir bar grafiği (Stres skoru vs Rakım)
        if not df.empty and "Rakim" in df.columns and "Stres_Skoru" in df.columns:
            st.write("### Rakım ve Stres Skoru Dağılımı")
            st.bar_chart(data=df, x="Rakim", y="Stres_Skoru")
            
    except Exception as e:
        st.warning("E-Tablo'ya henüz bağlanılamadı veya tablo tamamen boş.")
