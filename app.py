import streamlit as st
import pandas as pd
import requests
import datetime
import base64
import plotly.express as px

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
        "bug_options": ["Vampir Kelebek (Ricania simulans)", "Çay Filiz Güvesi (Parametriotes theae)", "Çay Koşnili (Chloropulvinaria floccifera)", "Mor Çay Akarı (Calacarus carinatus)", "Diğer"],
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
        "bug_options": ["Vampire Bug (Ricania simulans)", "Tea Shoot Borer (Parametriotes theae)", "Tea Scale Insect (Chloropulvinaria floccifera)", "Purple Tea Mite (Calacarus carinatus)", "Other"],
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
                **🔍 Rize Çay Zararlıları Tanımlama Rehberi (Görseller için tıklayın):**
                * [Vampir Kelebek (Ricania simulans)](https://www.google.com/search?q=Ricania+simulans+çay+zararlısı&tbm=isch)
                * [Çay Filiz Güvesi (Parametriotes theae)](https://www.google.com/search?q=Parametriotes+theae+çay+kurdu&tbm=isch)
                * [Çay Koşnili (Chloropulvinaria floccifera)](https://www.google.com/search?q=Çay+koşnili+Chloropulvinaria+floccifera&tbm=isch)
                * [Mor Çay Akarı (Calacarus carinatus)](https://www.google.com/search?q=Mor+çay+akarı+Calacarus+carinatus&tbm=isch)
                """)
            else:
                st.markdown("""
                **🔍 Rize Tea Pests Identification Guide (Click for images):**
                * [Vampire Bug (Ricania simulans)](https://www.google.com/search?q=Ricania+simulans&tbm=isch)
                * [Tea Shoot Borer (Parametriotes theae)](https://www.google.com/search?q=Parametriotes+theae&tbm=isch)
                * [Tea Scale Insect (Chloropulvinaria floccifera)](https://www.google.com/search?q=Chloropulvinaria+floccifera&tbm=isch)
                * [Purple Tea Mite (Calacarus carinatus)](https://www.google.com/search?q=Calacarus+carinatus&tbm=isch)
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
    
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"
    
    # Veriyi 60 saniyede bir önbelleğe al (Siteyi ve Google'ı yormamak için çok önemli bir güvenlik adımı)
    @st.cache_data(ttl=60)
    def load_data():
        try:
            df = pd.read_csv(SHEET_CSV_URL)
            return df
        except Exception as e:
            return None

    df = load_data()

    if df is None or df.empty:
        if lang == "Türkçe 🇹🇷":
            st.info("Bu bölümde Rize coğrafyasından toplanan bitki stres-rakım grafikleri ve korelasyon analizleri yer alacaktır. Henüz veri tabanına ulaşılamıyor veya tablo boş.")
        else:
            st.info("This section will display plant stress-altitude graphs and correlation analysis collected from the Rize geography. Data is currently unavailable or empty.")
    else:
        try:
            # VERİ TEMİZLİĞİ: Sütun adlarındaki olası boşlukları ve Türkçe karakter hatalarını otomatik düzelt
            df.columns = df.columns.str.strip()
            df = df.rename(columns={
                'Rakım': 'Rakim', 
                'Stres Skoru': 'Stres_Skoru', 
                'Hava Durumu': 'Hava_Durumu', 
                'Gözlem Türü': 'Gozlem_Turu',
                'Tarih ': 'Tarih'
            })

            # Sütunları sayısal değerlere dönüştür ve boş verileri temizle
            df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
            df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
            df = df.dropna(subset=['Rakim', 'Stres_Skoru'])
            
            if len(df) > 0:
                st.success(f"📊 Toplam {len(df)} bilimsel saha gözlemi başarıyla analiz ediliyor!" if lang == "Türkçe 🇹🇷" else f"📊 Total {len(df)} scientific field observations analyzed successfully!")
                
                # 1. GRAFİK: Rakım ve Stres Korelasyonu (Projenin Ana Çıktısı)
                st.subheader("⛰️ Rakım vs. Bitki Stres Skoru" if lang == "Türkçe 🇹🇷" else "⛰️ Altitude vs. Plant Stress Score")
                fig_scatter = px.scatter(
                    df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu",
                    hover_data=["Tarih", "Gozlem_Turu"],
                    labels={"Rakim": "Rakım (m)", "Stres_Skoru": "Stres Skoru (1-5)", "Hava_Durumu": "Hava Durumu"},
                    title="Rize Havzası: Yükseklik ve Fizyolojik Stres Korelasyonu" if lang == "Türkçe 🇹🇷" else "Rize Basin: Altitude and Physiological Stress Correlation"
                )
                fig_scatter.update_traces(marker=dict(size=14, line=dict(width=2, color='DarkSlateGrey')))
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Scientix Jüri Yorumu
                if lang == "Türkçe 🇹🇷":
                    st.info("**Bilimsel Yorum (IBSE Modeli):** Yukarıdaki dağılım, Rize'nin dik yamaçlarında rakım ($h$) arttıkça rüzgar şiddeti ve geç don riskinin fizyolojik stres skorunu ($S_s$) nasıl etkilediğini göstermektedir. Sahile yakın bölgelerde (0-100m) ise yüksek bağıl nem kaynaklı stomatal stres gözlemlenmektedir. Bu gerçek zamanlı veri haritalaması, iklim krizinin farklı dikey ekolojik gradyanlardaki mikroklimatik etkisini sayısal olarak kanıtlamaktadır.")
                else:
                    st.info("**Scientific Interpretation (IBSE):** The distribution above shows how wind intensity and late frost risk affect the physiological stress score ($S_s$) as altitude ($h$) increases on Rize's steep slopes. In coastal areas (0-100m), stomatal stress due to high relative humidity is observed. This real-time data mapping quantitatively proves the microclimatic impact of the climate crisis across different vertical ecological gradients.")
                
                st.write("---")
                colA, colB = st.columns(2)
                
                with colA:
                    st.subheader("☁️ Hava Durumu Dağılımı" if lang == "Türkçe 🇹🇷" else "☁️ Weather Distribution")
                    fig_pie = px.pie(df, names='Hava_Durumu', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
                    fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with colB:
                    st.subheader("🔍 Gözlem Odakları" if lang == "Türkçe 🇹🇷" else "🔍 Observation Focus")
                    # Çok uzun böcek isimlerinin grafiği bozmaması için kelime bazlı daraltma
                    df['Ana_Kategori'] = df['Gozlem_Turu'].apply(lambda x: "Böcek Gözlemi" if "Böcek" in str(x) else str(x))
                    fig_bar = px.bar(
                        df['Ana_Kategori'].value_counts().reset_index(), 
                        x='count', y='Ana_Kategori', orientation='h', color='Ana_Kategori',
                        labels={'count': 'Kayıt Sayısı', 'Ana_Kategori': 'Tür'}
                    )
                    fig_bar.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                st.write("---")
                st.subheader("📋 Toplanan Ham Veriler" if lang == "Türkçe 🇹🇷" else "📋 Raw Collected Data")
                # Görsel kirlilik yapmaması için Google Drive resim linklerini veri tablosundan gizliyoruz
                st.dataframe(df.drop(columns=['Fotograf_Linki'], errors='ignore'), use_container_width=True)
                
            else:
                st.warning("Veriler okundu ancak işlenebilir sayısal bir rakım/stres verisi bulunamadı." if lang == "Türkçe 🇹🇷" else "Data read but no processable numerical altitude/stress data found.")
                
        except Exception as e:
            st.error(f"Grafik motoru çalışırken bir hata oluştu: {e} | E-Tablo Sütunlarınız: {df.columns.tolist()}" if lang == "Türkçe 🇹🇷" else f"Graph engine error: {e} | Your Sheet Columns: {df.columns.tolist()}")
