import streamlit as st
import requests
import json
import base64
from datetime import datetime

st.set_page_config(
    page_title="Future Farmers - Citizen Science Portal",
    page_icon="🌱",
    layout="centered"
)

# Kopyaladığınız yeni URL'yi aşağıdaki tırnak işaretlerinin arasına yapıştırın hocam:
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxamU64AHCSNtW3uKjHC0qibj8tYExRKreXZp3iR9TtBc7b0jbs0YFXF_zbleovy0SJ/exec"

st.markdown("""
    <style>
    .main-title {
        color: #113425;
        font-family: 'Playfair Display', serif;
        font-size: 2.3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #4a5c53;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 25px;
    }
    .info-box {
        background-color: #f0f4f1;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #113425;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }
    .stButton>button {
        background-color: #113425 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        height: 48px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b4d37 !important;
    }
    </style>
""", unsafe_allow_html=True)

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Projesi Gözlem ve Mikroklima Veri Giriş Portalı",
        "welcome": "🔬 <b>Sevgili Vatandaş Bilimciler,</b><br>Seçtiğiniz sabit çay bitkisinin gelişimini, rakıma ve hava koşullarına bağlı olarak gözlemleyip kaydediniz. Girdiğiniz veriler doğrudan bilimsel analiz veri tabanımıza aktarılacaktır.",
        "sec1_title": "### 1. Konum ve Ortam Koşulları",
        "obs_type": "Gözlem Nesnesi / Türü:",
        "obs_options": ["Proje Bitkim (Çay)", "Diğer Tarım Bitkisi", "Çevredeki Doğal Canlı"],
        "altitude": "Bulunduğunuz Konumun Rakımı (Metre):",
        "altitude_help": "Telefonunuzun pusula veya altimetre uygulamasından yüksekliğinizi deniz seviyesine göre metre cinsinden yazın.",
        "weather": "Hava Durumu:",
        "weather_options": ["Güneşli", "Parçalı Bulutlu", "Çok Bulutlu / Kapalı", "Yağmurlu", "Sisli", "Karlı"],
        "sec2_title": "### 2. Bitki Sağlığı ve Gözlemler",
        "stress": "Bitki Sağlık ve Stres Skoru (1-5):",
        "stress_help": "1: Çok Sağlıklı/Canlı, 3: Normal Gelişim, 5: Kritik Stres (Kuruma, hastalık veya zararlı yoğun).",
        "notes": "Gözlem Notlarınız ve Bulgularınız:",
        "notes_placeholder": "Örn: Bu hafta yeni taze filizler oluşmaya başladı. Yapraklarda sararma yok...",
        "photo": "Bitki Gözlem Fotoğrafı (JPEG formatında):",
        "photo_help": "Doğru analiz için her hafta aynı açıdan ve mesafeden fotoğraf çekmeye özen gösterin.",
        "submit_btn": "Verileri Bilim Veritabanına Gönder 🚀",
        "err_config": "⚠️ Sistem Ayarı Eksik: Lütfen kodun en üstündeki WEB_APP_URL değişkenine geçerli Apps Script adresinizi gömün!",
        "err_photo": "⚠️ Lütfen bilimsel kanıt olarak bitkinizin bir fotoğrafını yükleyin!",
        "spinner": "Verileriniz şifreleniyor ve veri havuzuna aktarılıyor...",
        "success": "🎉 Harika! Gözlem verileriniz başarıyla kaydedildi. Bir sonraki haftalık gözlemde görüşmek üzere vatandaş bilimci!",
        "err_server": "Sunucudan geçersiz yanıt alındı: ",
        "err_general": "Veri gönderilirken bir hata oluştu: "
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Project Observation & Microclimate Data Entry Portal",
        "welcome": "🔬 <b>Dear Citizen Scientists,</b><br>Please observe and record the growth of your selected tea plant based on altitude and weather conditions. Your data will be directly transferred to our scientific database.",
        "sec1_title": "### 1. Location and Environmental Conditions",
        "obs_type": "Observation Object / Type:",
        "obs_options": ["My Project Plant (Tea)", "Other Agricultural Plant", "Surrounding Natural Organism"],
        "altitude": "Altitude of Your Location (Meters):",
        "altitude_help": "Enter your altitude in meters from your phone's compass or altimeter app.",
        "weather": "Weather Condition:",
        "weather_options": ["Sunny", "Partly Cloudy", "Overcast / Cloudy", "Rainy", "Foggy", "Snowy"],
        "sec2_title": "### 2. Plant Health and Observations",
        "stress": "Plant Health & Stress Score (1-5):",
        "stress_help": "1: Very Healthy/Vigorous, 3: Normal Growth, 5: Critical Stress (Drying, disease, or pest infestation).",
        "notes": "Your Observation Notes & Findings:",
        "notes_placeholder": "e.g., New fresh shoots started to form this week. No yellowing on leaves...",
        "photo": "Plant Observation Photo (JPEG format):",
        "photo_help": "For accurate analysis, try to take the photo from the same angle and distance each week.",
        "submit_btn": "Submit Data to Scientific Database 🚀",
        "err_config": "⚠️ System Configuration Missing: Please embed your valid Apps Script address into the WEB_APP_URL variable!",
        "err_photo": "⚠️ Please upload a photo of your plant as scientific evidence!",
        "spinner": "Encrypting your data and transferring to the scientific database...",
        "success": "🎉 Fantastic! Your observation data has been successfully recorded. See you next week, citizen scientist!",
        "err_server": "Invalid response received from server: ",
        "err_general": "An error occurred while sending data: "
    }
}

selected_lang = st.radio("Select Language / Dil Seçin", ["Türkçe 🇹🇷", "English 🇬🇧"], horizontal=True)
t = translations[selected_lang]

# Başlık ve Bilgilendirme Alanı
st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='info-box'>{t['welcome']}</div>", unsafe_allow_html=True)

with st.form("gozlem_formu", clear_on_submit=False):
    
    st.markdown(t["sec1_title"])
    
    # Gözlem Türü Seçimi
    gozlem_turu = st.selectbox(
        t["obs_type"],
        t["obs_options"]
    )
    
    # Rakım Girişi
    rakim = st.number_input(
        t["altitude"],
        min_value=0,
        max_value=2500,
        value=0,
        step=5,
        help=t["altitude_help"]
    )
    
    # Hava Durumu
    hava_durumu = st.selectbox(
        t["weather"],
        t["weather_options"]
    )
    
    st.markdown("---")
    st.markdown(t["sec2_title"])
    
    # Sağlık/Stres Skoru
    stres_skoru = st.slider(
        t["stress"],
        min_value=1,
        max_value=5,
        value=3,
        help=t["stress_help"]
    )
    
    # Notlar
    gozlem_notlari = st.text_area(
        t["notes"],
        placeholder=t["notes_placeholder"]
    )
    
    # Fotoğraf Yükleme
    uploaded_file = st.file_uploader(
        t["photo"], 
        type=["jpg", "jpeg", "png"],
        help=t["photo_help"]
    )
    
    submitted = st.form_submit_button(t["submit_btn"])

    if submitted:
        if WEB_APP_URL == "BURAYA_KOPYALADIGINIZ_YENI_URL_YAPISTIRIN" or not WEB_APP_URL.startswith("https://"):
            st.error(t["err_config"])
        elif not uploaded_file:
            st.error(t["err_photo"])
        else:
            with st.spinner(t["spinner"]):
                try:
                    # Fotoğrafı Base64 formatına çevirme
                    bytes_data = uploaded_file.read()
                    base64_image = base64.b64encode(bytes_data).decode('utf-8')
                    
                    # Veri paketi
                    payload = {
                        "Tarih": datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "Gozlem_Turu": gozlem_turu,
                        "Rakim": int(rakim),
                        "Hava_Durumu": hava_durumu,
                        "Stres_Skoru": int(stres_skoru),
                        "Notlar": gozlem_notlari,
                        "Foto_Base64": base64_image
                    }
                    
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(WEB_APP_URL, data=json.dumps(payload), headers=headers)
                    
                    if response.status_code == 200 and "Başarılı" in response.text:
                        st.success(t["success"])
                        st.balloons()
                    else:
                        st.error(f"{t['err_server']}{response.text}")
                        
                except Exception as e:
                    st.error(f"{t['err_general']}{str(e)}")
```
eof

