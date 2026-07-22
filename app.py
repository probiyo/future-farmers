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
st.write("Hoş geldiniz Hazreti Yusuf hocam! Saha verileri, böcek analizleri, grafikler ve AI Agro Doctor bir arada.")

# Oturum durumunda veri deposu (Saha Verileri için)
if "saha_verileri" not in st.session_state:
    st.session_state.saha_verileri = pd.DataFrame(columns=[
        "Tarih", "Gözlem Türü", "Rakım (m)", "Hava Durumu", "Stres Seviyesi (1-10)", "Notlar ve Açıklamalar"
    ])

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
    st.subheader("Saha Gözlem Verisi Girişi ve Otomatik Analizler")
    st.write("Öğrenciler sahada yaptıkları gözlemleri aşağıdan kaydederek anında analiz, yorum ve grafik oluşturabilirler.")
    
    with st.form("saha_formu"):
        col1, col2 = st.columns(2)
        with col1:
            tarih_input = st.date_input("Gözlem Tarihi")
            gozlem_turu = st.selectbox("Gözlem Türü", ["Çay Bitkisi", "Toprak Analizi", "Zararlı/Böcek Tespiti", "Hastalık Belirtisi", "Diğer"])
            rakim_input = st.number_input("Rakım (m)", min_value=0, max_value=5000, value=200)
        with col2:
            hava_durumu = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağmurlu", "Sisli", "Karlı", "Don Tehlikesi"])
            stres_input = st.slider("Stres Skoru (1-10)", 1, 10, 3)
        
        aciklama_input = st.text_area("Açıklamalar, Gözlemler ve Notlar")
        
        submit_button = st.form_submit_button(label="Saha Verisini Kaydet ve Analiz Et")
        
        if submit_button:
            yeni_veri = {
                "Tarih": str(tarih_input),
                "Gözlem Türü": gozlem_turu,
                "Rakım (m)": rakim_input,
                "Hava Durumu": hava_durumu,
                "Stres Seviyesi (1-10)": stres_input,
                "Notlar ve Açıklamalar": aciklama_input
            }
            st.session_state.saha_verileri = pd.concat([st.session_state.saha_verileri, pd.DataFrame([yeni_veri])], ignore_index=True)
            st.success("Saha verisi başarıyla kaydedildi ve sisteme işlendi!")

    st.markdown("---")
    st.subheader("📊 Kayıtlı Saha Verileri ve Grafik Analizleri")
    
    if not st.session_state.saha_verileri.empty:
        st.dataframe(st.session_state.saha_verileri, use_container_width=True)
        
        csv_data = st.session_state.saha_verileri.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tüm Saha Verilerini CSV Olarak İndir (Google E-Tabloya Aktar)",
            data=csv_data,
            file_name="future_farmers_saha_verileri.csv",
            mime="text/csv",
        )
        
        st.write("### Veri Görselleştirme")
        kolonlar = st.session_state.saha_verileri.columns.tolist()
        c1, c2 = st.columns(2)
        with c1:
            secilen_x = st.selectbox("X Ekseni:", kolonlar, index=0)
        with c2:
            secilen_y = st.selectbox("Y Ekseni:", kolonlar, index=4 if len(kolonlar) > 4 else 0)
            
        fig = px.bar(st.session_state.saha_verileri, x=secilen_x, y=secilen_y, color="Gözlem Türü", title="Saha Ölçüm ve Stres Dağılım Grafiği")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Henüz girilmiş bir saha verisi bulunmuyor. Yukarıdaki formu doldurarak ilk verinizi ekleyebilirsiniz.")
