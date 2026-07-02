import streamlit as st
import requests
import json
import base64
from datetime import datetime

# Sayfa yapılandırması - Akademik ve doğa dostu koyu yeşil tema
st.set_page_config(
    page_title="Future Farmers - Vatandaş Bilimi Gözlem Formu",
    page_icon="🌱",
    layout="centered"
)

# Apps Script URL'nizi buraya gömüyoruz (Öğrencilerden gizlemek ve sistemi otomatikleştirmek için)
# Kopyaladığınız yeni URL'yi aşağıdaki tırnak işaretlerinin arasına yapıştırın hocam:
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxamU64AHCSNtW3uKjHC0qibj8tYExRKreXZp3iR9TtBc7b0jbs0YFXF_zbleovy0SJ/exec"

# Arayüzü görsel olarak zenginleştiren modern CSS kodları
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

# Başlık ve Proje Bilgisi
st.markdown("<div class='main-title'>Future Farmers 🌱</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Scientix Projesi Gözlem ve Mikroklima Veri Giriş Portalı</div>", unsafe_allow_html=True)

st.markdown("""
<div class='info-box'>
    🔬 <b>Sevgili Vatandaş Bilimciler,</b><br>
    Seçtiğiniz sabit çay bitkisinin gelişimini, rakıma ve hava koşullarına bağlı olarak gözlemleyip kaydediniz. 
    Girdiğiniz veriler doğrudan bilimsel analiz veri tabanımıza aktarılacaktır.
</div>
""", unsafe_allow_html=True)

# Bilimsel Gözlem Formu
with st.form("gozlem_formu", clear_on_submit=False):
    
    st.markdown("### 1. Konum ve Ortam Koşulları")
    
    # Gözlem Türü Seçimi
    gozlem_turu = st.selectbox(
        "Gözlem Nesnesi / Türü:",
        ["Proje Bitkim (Çay)", "Diğer Tarım Bitkisi", "Çevredeki Doğal Canlı"]
    )
    
    # Rize mikrokliması için kritik olan Rakım parametresi
    rakim = st.number_input(
        "Bulunduğunuz Konumun Rakımı (Metre):",
        min_value=0,
        max_value=2500,
        value=0,
        step=5,
        help="Telefonunuzun pusula veya altimetre uygulamasından yüksekliğinizi deniz seviyesine göre metre cinsinden yazın."
    )
    
    # Hava Durumu
    hava_durumu = st.selectbox(
        "Hava Durumu:",
        ["Güneşli", "Parçalı Bulutlu", "Çok Bulutlu / Kapalı", "Yağmurlu", "Sisli", "Karlı"]
    )
    
    st.markdown("---")
    st.markdown("### 2. Bitki Sağlığı ve Gözlemler")
    
    # Scientix için nicel veri sağlayacak 1-5 Stres/Sağlık Skoru
    stres_skoru = st.slider(
        "Bitki Sağlık ve Stres Skoru (1-5):",
        min_value=1,
        max_value=5,
        value=3,
        help="1: Çok Sağlıklı/Canlı, 3: Normal Gelişim, 5: Kritik Stres (Kuruma, hastalık veya zararlı yoğun)."
    )
    
    # Detaylı öğrenci notları
    gozlem_notlari = st.text_area(
        "Gözlem Notlarınız ve Bulgularınız:",
        placeholder="Örn: Bu hafta yeni taze filizler (sürgünler) oluşmaya başladı. Yapraklarda herhangi bir lekelenme veya sararma yok. Çevrede hafif böcek aktivitesi gözlendi."
    )
    
    # Fotoğraf Yükleme / Kamera ile Çekme alanı
    uploaded_file = st.file_uploader(
        "Bitki Gözlem Fotoğrafı (JPEG formatında):", 
        type=["jpg", "jpeg", "png"],
        help="Doğru analiz için her hafta aynı açıdan ve mesafeden fotoğraf çekmeye özen gösterin."
    )
    
    # Form Gönderim Butonu
    submitted = st.form_submit_with_button_on_click("Verileri Bilim Veritabanına Gönder 🚀")

    if submitted:
        if WEB_APP_URL == "BURAYA_KOPYALADIGINIZ_YENI_URL_YAPISTIRIN" or not WEB_APP_URL.startswith("https://"):
            st.error("⚠️ Sistem Ayarı Eksik: Lütfen kodun en üstündeki WEB_APP_URL değişkenine geçerli Apps Script adresinizi gömün!")
        elif not uploaded_file:
            st.error("⚠️ Lütfen bilimsel kanıt olarak bitkinizin bir fotoğrafını yükleyin!")
        else:
            with st.spinner("Verileriniz şifreleniyor ve veri havuzuna aktarılıyor..."):
                try:
                    # Fotoğrafı veritabanına iletmek için Base64 formatına çeviriyoruz
                    bytes_data = uploaded_file.read()
                    base64_image = base64.b64encode(bytes_data).decode('utf-8')
                    
                    # Apps Script'e göndereceğimiz veri paketi
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
                        st.success("🎉 Harika! Gözlem verileriniz başarıyla kaydedildi. Bir sonraki haftalık gözlemde görüşmek üzere vatandaş bilimci!")
                        st.balloons()
                    else:
                        st.error(f"Sunucudan geçersiz yanıt alındı: {response.text}")
                        
                except Exception as e:
                    st.error(f"Veri gönderilirken bir hata oluştu: {str(e)}")
