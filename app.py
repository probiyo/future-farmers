import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px
import os

# Sayfa yapılandırması
st.set_page_config(page_title="Future Farmers Pro - Biyoloji & Tarım Asistanı", page_icon="🌱", layout="wide")

# API Anahtarı Ayarı
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            st.warning("API Anahtarı bulunamadı! AI özellikleri için secrets.toml dosyasını kontrol edin.")
except Exception as e:
    st.error(f"Yapılandırma hatası: {e}")

st.title("🌱 Future Farmers Pro - Akıllı Tarım ve Biyoloji Laboratuvarı")
st.write("Hoş geldiniz Hocam! Saha verileri, böcek analizleri, grafikler ve AI Agro Doctor bir arada.")

# Sekmeler
tab1, tab2, tab3 = st.tabs(["📸 AI Agro Doctor & Gözlem", "🐛 Böcek Bilgileri & Seçimleri", "📊 Saha Verileri ve Grafikler"])

with tab1:
    st.subheader("Bitki Sağlığı, Stres Analizi ve Yapay Zeka Doktoru")
    
    upload_option = st.radio("Görüntü Kaynağı:", ["Fotoğraf Yükle", "Kameradan Çek"])
    
    image = None
    if upload_option == "Fotoğraf Yükle":
        uploaded_file = st.file_uploader("Bitki yaprak veya kök fotoğraflarını seçin...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Yüklenen Bitki Görseli", use_column_width=True)
    else:
        camera_file = st.camera_input("Kameradan Çek")
        if camera_file is not None:
            image = Image.open(camera_file)
            st.image(image, caption="Çekilen Bitki Görseli", use_column_width=True)

    rakim = st.number_input("Rakım (metre)", min_value=0, max_value=5000, value=0)
    stres_skoru = st.slider("Tahmini Stres Seviyesi (1-10)", 1, 10, 1)
    notlar = st.text_area("Eklemek istediğiniz gözlemler veya notlar:")

    if st.button("AI Agro Doctor ile Analiz Et"):
        if image is not None:
            with st.spinner("Yapay zeka bitki fizyolojisini inceliyor..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = (
                        "Sen uzman bir tarım ve bitki fizyolojisi doktorusun. "
                        f"Rakım: {rakim}m, Gözlenen Stres Seviyesi: {stres_skoru}/10, Notlar: {notlar}. "
                        "Lütfen bu bitki görselini ve verileri inceleyerek olası hastalıkları, besin element eksikliklerini "
                        "ve çözüm önerilerini maddeler halinde net ve somut örneklerle açıkla."
                    )
                    response = model.generate_content([prompt, image])
                    st.success("Analiz Tamamlandı!")
                    st.markdown("### 🩺 Uzman Raporu")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analiz sırasında bir hata oluştu: {e}")
        else:
            st.warning("Lütfen önce bir bitki görseli yükleyin veya çekin!")

with tab2:
    st.subheader("Böcek Bilgileri ve Zararlı Seçimleri")
    st.write("Saha çalışmalarında karşılaşılan zararlılar ve entegre mücadele kriterleri:")
    
    bocek_secimi = st.selectbox(
        "İncelemek istediğiniz zararlıyı seçin:",
        ["Yeşil Kurt (Helicoverpa armigera)", "Yaprak Bitleri (Aphididae)", "Kırmızı Örümcek (Tetranychidae)", "Kahverengi Kokarca"]
    )
    
    if "Yeşil Kurt" in bocek_secimi:
        st.info("**Biyolojisi ve Zararı:** Polifag bir zararlıdır. Larvaları bitkinin generatif organları (çiçek ve meyve) ile beslenir.")
        st.success("**Mücadele Yöntemleri:** Biyoteknolojik mücadele (feromon tuzaklar), kültürel önlemler ve ekonomik zarar seviyesi aşılırsa uygun ilaçlama.")
    elif "Yaprak Bitleri" in bocek_secimi:
        st.info("**Biyolojisi ve Zararı:** Bitki özsuyunu emerek beslenirler ve virüs hastalıklarını taşırlar.")
        st.success("**Mücadele Yöntemleri:** Uğur böceği gibi doğal düşmanların korunması, zararlı yoğunluğuna göre spesifik preparatlar.")
    elif "Kırmızı Örümcek" in bocek_secimi:
        st.info("**Biyolojisi:** Özellikle sıcak ve kurak dönemlerde yaprak altlarında ağ örerek özsu emerler.")
        st.success("**Mücadele Yöntemleri:** Kükürtlü uygulamalar ve akarisitler.")
    else:
        st.info("**Biyolojisi ve Zararı:** Tarım alanlarında yeni nesil istilacı zararlılardandır, meyve ve sebzelerde kalite kaybına yol açar.")
        st.success("**Mücadele Yöntemleri:** Feromon tuzaklar ile kitle yakalama ve mekanik mücadele.")

with tab3:
    st.subheader("Saha Veri Yükleme ve Grafik Analizleri")
    st.write("Excel veya CSV formatındaki saha ölçüm verilerinizi yükleyerek interaktif grafikler oluşturun.")
    
    uploaded_data = st.file_uploader("Saha Veri Dosyasını Yükle (CSV veya Excel)", type=["csv", "xlsx"])
    
    if uploaded_data is not None:
        try:
            if uploaded_data.name.endswith('.csv'):
                df = pd.read_csv(uploaded_data)
            else:
                df = pd.read_excel(uploaded_data)
                
            st.write("### Yüklenen Veri Önizlemesi", df.head())
            
            # Grafik Çizdirme Alanı
            st.write("### Veri Görselleştirme")
            kolonlar = df.columns.tolist()
            secilen_x = st.selectbox("X Ekseni için sütun seçin:", kolonlar)
            secilen_y = st.selectbox("Y Ekseni için sütun seçin:", kolonlar)
            
            if st.button("Grafik Oluştur"):
                fig = px.bar(df, x=secilen_x, y=secilen_y, title="Saha Ölçüm Grafiği")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Veri okunurken hata oluştu: {e}")
    else:
        st.info("Henüz veri yüklenmedi. Örnek bir veri analizi için yukarıdan dosya yükleyebilirsiniz.")
