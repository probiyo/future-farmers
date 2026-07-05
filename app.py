import streamlit as st
import pandas as pd
import requests
import datetime
import base64

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")

# LÜTFEN KENDİ GOOGLE APPS SCRIPT LİNKİNİZİ AŞAĞIDAKİ TIRNAKLARIN İÇİNE YAPIŞTIRIN
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "entry": "Veri Giriş Portalı",
        "analytics": "Bilimsel Analiz",
        "submit": "Verileri Bilimsel Kayıta Ekle 🚀",
        "success": "Veri başarıyla bilimsel havuza işlendi!",
        "error": "Veri gönderilemedi.",
        "obs_type": "Gözlem Nesnesi (Ne Gözlemliyorsunuz?)",
        "options": ["Çay", "Böcekler", "Diğer"],
        "bug_type": "Böcek Türünü Seçiniz",
        "bug_options": ["Yeşil Cırcır Böceği (Tettigonia viridissima)", "Kırmızı Örümcek (Tetranychus urticae)", "Çay Güvesi (Parametriotes theae)", "Diğer"],
        "alt": "Rakım (Deniz Seviyesinden Yükseklik - Metre)",
        "stress": "Bitki Sağlık ve Stres Skoru (1-5 Arası Değerlendirin)",
        "weather": "Hava Durumu",
        "weather_options": ["Güneşli", "Bulutlu", "Kapalı", "Yağmurlu", "Sisli", "Don", "Karlı"],
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
        "bug_options": ["Green Grasshopper (Tettigonia viridissima)", "Red Spider Mite (Tetranychus urticae)", "Tea Moth (Parametriotes theae)", "Other"],
        "alt": "Altitude (Meters)",
        "stress": "Plant Health & Stress Score (1-5)",
        "weather": "Weather",
        "weather_options": ["Sunny", "Cloudy", "Overcast", "Rainy", "Foggy", "Frost", "Snowy"],
        "camera_title": "📸 Take Photo with Camera",
        "upload_title": "📁 Or Upload Photo from Gallery",
        "notes": "Observation Notes (Optional)"
    }
}

st.sidebar.title("Language / Dil Seçimi")
lang = st.sidebar.selectbox("", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[lang]

tab1, tab2 = st.tabs([t["entry"], t["analytics"]])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        obs_type = st.selectbox(t["obs_type"], t["options"])
        
        bug_type = "Yok"
        if obs_type == "Böcekler" or obs_type == "Pests":
            st.info("Böcekler seçildi. Lütfen aşağıdaki listeden türü belirtin:")
            bug_type = st.selectbox(t["bug_type"], t["bug_options"])
            
            # Böcek tanıma rehberi linkleri
            if lang == "Türkçe 🇹🇷":
                st.markdown("""
                **🔍 Böcek Tanımlama Rehberi (Görseller için tıklayın):**
                * [Yeşil Cırcır Böceği (Tettigonia viridissima)](https://www.google.com/search?q=Tettigonia+viridissima&tbm=isch)
                * [Kırmızı Örümcek (Tetranychus urticae)](https://www.google.com/search?q=Tetranychus+urticae+çay&tbm=isch)
                * [Çay Güvesi (Parametriotes theae)](https://www.google.com/search?q=Parametriotes+theae&tbm=isch)
                """)
            else:
                st.markdown("""
                **🔍 Pest Identification Guide (Click for images):**
                * [Green Grasshopper (Tettigonia viridissima)](https://www.google.com/search?q=Tettigonia+viridissima&tbm=isch)
                * [Red Spider Mite (Tetranychus urticae)](https://www.google.com/search?q=Tetranychus+urticae&tbm=isch)
                * [Tea Moth (Parametriotes theae)](https://www.google.com/search?q=Parametriotes+theae&tbm=isch)
                """)
        else:
            st.caption("ℹ️ Not: Böcek türü menüsünü görmek için yukarıdan 'Böcekler'i seçmelisiniz.")
        
        st.write("---")
        
        alt = st.number_input(t["alt"], min_value=0, max_value=2500, value=0)
        
        stres_val = st.select_slider(t["stress"], options=[1, 2, 3, 4, 5])
        
        # Yeni ve Tam Stres Skoru Açıklamaları
        if lang == "Türkçe 🇹🇷":
            st.markdown("""
            **ℹ️ Puanlama Rehberi:** 
            * **1 Puan:** Çok Sağlıklı, hiç hasar yok.
            * **2 Puan:** Sağlıklı ancak ufak tefek lekeler veya çok hafif stres belirtileri var.
            * **3 Puan:** Orta derecede stres, belirgin sararma veya hafif kuruma.
            * **4 Puan:** Yüksek stres, ciddi hasar, büyümede durma veya yaygın kuruma.
            * **5 Puan:** Çok Yüksek Stres, ağır hastalık veya bitkinin tamamen kuruması.
            """)
        else:
            st.markdown("""
            **ℹ️ Scoring Guide:** 
            * **1:** Very Healthy, no damage.
            * **2:** Healthy but minor spots or very slight stress symptoms.
            * **3:** Moderate stress, noticeable yellowing or slight withering.
            * **4:** High stress, severe damage, stunted growth or widespread withering.
            * **5:** Very Stressed, heavy disease or completely dying.
            """)
            
        notes = st.text_area(t["notes"])

    with col2:
        weather = st.selectbox(t["weather"], t["weather_options"])
        
        st.write("---")
        
        # Kamera Kısmı (Net Açıklamalı)
        st.markdown(f"### {t['camera_title']}")
        if lang == "Türkçe 🇹🇷":
            st.caption("👇 Kameranız otomatik açılır. Görüntü netleşince resmin hemen altındaki **'Take Photo'** butonuna tıklayın.")
        else:
            st.caption("👇 Camera opens automatically. Once focused, click the **'Take Photo'** button below the image.")
        camera_photo = st.camera_input("")

        st.write("---")

        # Dosya Yükleme Kısmı (Net Açıklamalı)
        st.markdown(f"### {t['upload_title']}")
        if lang == "Türkçe 🇹🇷":
            st.caption("👇 Veya cihazınızdaki hazır bir resmi buraya tıklayarak yükleyin (**'Browse files' / 'Upload'**).")
        else:
            st.caption("👇 Or upload a ready image from your device by clicking here (**'Browse files' / 'Upload'**).")
        uploaded_photo = st.file_uploader("", type=['jpg', 'jpeg', 'png'])

    st.write("---")
    if st.button(t["submit"]):
        final_photo = camera_photo if camera_photo else uploaded_photo
        foto_base64 = "Test_Verisi"

        if final_photo is not None:
            foto_base64 = base64.b64encode(final_photo.getvalue()).decode("utf-8")

        # Gönderilecek veri paketi hazırlanıyor
        payload = {
            "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Gozlem_Turu": obs_type if obs_type != "Böcekler" and obs_type != "Pests" else f"Böcek: {bug_type}",
            "Rakim": alt,
            "Hava_Durumu": weather,
            "Stres_Skoru": stres_val,
            "Notlar": notes,
            "Foto_Base64": foto_base64
        }

        try:
            with st.spinner('Veriler bilimsel havuza aktarılıyor...'):
                response = requests.post(WEB_APP_URL, json=payload)
                if response.status_code == 200:
                    st.success(t["success"])
                else:
                    st.error(f"{t['error']} Kod: {response.status_code}")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header(t["analytics"])
    if lang == "Türkçe 🇹🇷":
        st.info("Bu bölümde Rize coğrafyasından toplanan bitki stres-rakım grafikleri ve korelasyon analizleri yer alacaktır. Yeterli veri toplandığında aktifleşecektir.")
    else:
        st.info("This section will display plant stress-altitude graphs and correlation analysis collected from the Rize geography. It will become active when enough data is collected.")
