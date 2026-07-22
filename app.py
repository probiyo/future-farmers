import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px
import os

# Sayfa yapılandırması
st.set_page_config(page_title="Future Farmers Pro - Akıllı Tarım ve Biyoloji Laboratuvarı", page_icon="🌱", layout="wide")

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
st.write("Hoş geldiniz hocam! İklim değişimlerinin çay ve bitki ekolojisine etkisini inceleyen akıllı saha takip sistemi.")

# Oturum durumunda veri deposu
if "saha_verileri" not in st.session_state:
    st.session_state.saha_verileri = pd.DataFrame(columns=[
        "Tarih", "Bitki Adı / Türü", "Rakım (m)", "Hava Durumu", "Toprak pH", "Stres Seviyesi", "AI Analiz ve Öneriler"
    ])

# Sekmeler
tab1, tab2, tab3 = st.tabs(["📸 Saha Gözlem & AI Doktor", "🐛 Böcek Bilgileri & Seçimleri", "📊 Saha Verileri ve Grafik Analizleri"])

with tab1:
    st.subheader("Saha Gözlem Verisi, İklim Faktörleri ve AI Analizi")
    st.write("Önce telefonunuzdan fotoğraf çekin veya yükleyin, ardından form alanlarını doldurup analiz başlatın.")
    
    st.markdown("---")
    st.info("💡 **Fotoğraf Çekme / Yükleme:** Aşağıdaki alandan telefonunuzun kamerasını doğrudan açarak fotoğraf çekebilir veya galerinizden seçebilirsiniz.")
    
    uploaded_file = st.file_uploader("Bitki Yaprak veya Toprak Fotoğrafı Seç / Çek", type=["jpg", "jpeg", "png"])
    
    aktif_gorsel = None
    if uploaded_file is not None:
        aktif_gorsel = Image.open(uploaded_file)
        st.image(aktif_gorsel, caption="Yüklenen / Çekilen Saha Görseli", width=300)

    with st.form("gelismis_saha_formu"):
        col1, col2 = st.columns(2)
        with col1:
            tarih_input = st.date_input("Gözlem Tarihi")
            
            gozlem_turu_secimi = st.selectbox("İncelenen Bitki Türü", ["Çay Bitkisi", "Diğer Bitki (Bilimsel Adı Giriniz)"])
            
            bitki_adi = "Camellia sinensis (Çay)"
            if "Diğer" in gozlem_turu_secimi:
                bitki_adi = st.text_input("Bitkinin Bilimsel / Yerel Adı:", value="Örn: Quercus robur")
                
            rakim_input = st.number_input("Rakım (m)", min_value=0, max_value=5000, value=250)
            
        with col2:
            hava_durumu = st.selectbox("Hava Durumu (İklimsel Takip)", ["Güneşli", "Bulutlu", "Yağmurlu", "Sisli", "Karlı", "Don Tehlikesi"])
            toprak_ph = st.number_input("Toprak pH Değeri", min_value=0.0, max_value=14.0, value=4.8, step=0.1)
        
        ek_notlar = st.text_area("Öğrenci Gözlem Notları ve Ek Açıklamalar:")
        
        submit_button = st.form_submit_button(label="AI ile Analiz Et ve Kaydet")
        
        if submit_button:
            if aktif_gorsel is not None:
                with st.spinner("Yapay zeka bitki fizyolojisini, iklim etkilerini ve MEB biyoloji kazanımlarını inceliyor..."):
                    try:
                        # En güncel ve kararlı model adı kullanıldı
                        model = genai.GenerativeModel('gemini-2.0-flash')
                        prompt = (
                            "Sen uzman bir biyoloji ve tarım bilimleri danışmanısın. "
                            f"İncelenen Bitki: {bitki_adi}, Rakım: {rakim_input}m, Hava Durumu: {hava_durumu}, "
                            f"Toprak pH: {toprak_ph}, Öğrenci Notları: {ek_notlar}. "
                            "Küresel iklim değişikliklerinin ve abiyotik faktörlerin bitki ve toprak ekolojisi üzerindeki "
                            "etkilerini göz önüne alarak; 1) Stres Seviyesini (1-10 arası) ve nedenini, 2) Olası hastalık/besin element eksikliklerini, "
                            "3) MEB biyoloji müfredatı ekoloji kazanımlarına uygun bilimsel açıklamaları, 4) Çözüm ve yönetim önerilerini maddeler halinde net olarak açıkla."
                        )
                        response = model.generate_content([prompt, aktif_gorsel])
                        ai_sonuc = response.text
                        
                        stres_tahmini = "Yüksek / İncelendi" if "Stres" in ai_sonuc else "Normal"
                        
                        st.success("Analiz Tamamlandı!")
                        st.markdown("### 🩺 AI Uzman Ekoloji Raporu")
                        st.write(ai_sonuc)
                        
                        yeni_veri = {
                            "Tarih": str(tarih_input),
                            "Bitki Adı / Türü": bitki_adi,
                            "Rakım (m)": rakim_input,
                            "Hava Durumu": hava_durumu,
                            "Toprak pH": toprak_ph,
                            "Stres Seviyesi": stres_tahmini,
                            "AI Analiz ve Öneriler": ai_sonuc
                        }
                        st.session_state.saha_verileri = pd.concat([st.session_state.saha_verileri, pd.DataFrame([yeni_veri])], ignore_index=True)
                        st.info("Saha verisi başarıyla alt tabloya ve grafik arşivine eklendi!")
                        
                    except Exception as e:
                        st.error(f"AI analizi sırasında hata oluştu: {e}")
            else:
                st.warning("Lütfen önce yukarıdan bir fotoğraf yükleyin veya kameradan çekin!")

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
    st.subheader("📊 Kayıtlı Saha Verileri ve Grafik Analizleri")
    
    if not st.session_state.saha_verileri.empty:
        st.dataframe(st.session_state.saha_verileri, use_container_width=True)
        
        csv_data = st.session_state.saha_verileri.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tüm Saha Verilerini CSV Olarak İndir (Google E-Tabloya Aktar)",
            data=csv_data,
            file_name="future_farmers_iklim_saha_verileri.csv",
            mime="text/csv",
        )
        
        st.write("### İklim ve Toprak Verisi Görselleştirme")
        kolonlar = ["Rakım (m)", "Toprak pH"]
        secilen_y = st.selectbox("Grafik Değeri Seçin:", kolonlar)
        
        fig = px.bar(st.session_state.saha_verileri, x="Tarih", y=secilen_y, color="Hava Durumu", title=f"Tarihe Göre {secilen_y} ve İklim Dağılımı")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Henüz girilmiş bir saha verisi bulunmuyor. 'Saha Gözlem & AI Doktor' sekmesinden ilk verinizi ekleyebilirsiniz.")
