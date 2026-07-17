import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# Sayfa yapılandırması
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# Google Apps Script URL ve Sheets CSV URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw5ffOJbv63pEo1df7eo3cYUP2l6EZK4p9PDUSxcC-J_yI6frbhITKlG_mGOts-Ji3A/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

st.title("🌱 Future Farmers: Vatandaş Bilimi Portalı")
tab1, tab2 = st.tabs(["📊 Veri Girişi", "📈 Ekolojik Analiz"])

with tab1:
    st.header("Saha Gözlem Formu")
    with st.form("gozlem_formu"):
        tarih = st.text_input("Tarih", value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        gozlem_turu = st.selectbox("Gözlem Türü", ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
        rakim = st.number_input("Rakım", min_value=0, max_value=2000, value=200)
        
        # Güncellenmiş Hava Durumu seçimi
        hava = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"])
        
        # Stres Skoru Skalası Eklendi
        st.write("---")
        st.markdown("**Stres Skoru Skalası:**")
        st.caption("1: Sağlıklı | 2: Hafif Stresli | 3: Orta Stresli | 4: Yüksek Stresli | 5: Kritik")
        stres = st.slider("Stres Skoru", 1, 5, 1)
        
        notlar = st.text_area("Notlar")
        foto = st.camera_input("Bitki Fotoğrafı Çek")
        
        submitted = st.form_submit_button("Veriyi Gönder")
        
        if submitted:
            foto_base64 = "Test_Verisi"
            if foto is not None:
                foto_base64 = base64.b64encode(foto.read()).decode('utf-8')
            
            payload = {
                "Tarih": tarih, "Gozlem_Turu": gozlem_turu, "Rakim": rakim,
                "Hava_Durumu": hava, "Stres_Skoru": stres, "Notlar": notlar,
                "Foto_Base64": foto_base64
            }
            
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success("Veri başarıyla kaydedildi!")
                else:
                    st.error(f"Hata: {response.text}")
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header("Ekolojik Analiz Havuzu")
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        
        if not df.empty:
            # Görselleştirme
            fig = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", 
                             size="Stres_Skoru", title="Rakım vs. Stres Korelasyonu",
                             hover_data=["Notlar"])
            st.plotly_chart(fig, use_container_width=True)
            
            # Otomatik Yorumlama kısmı güncellendi
            st.subheader("📊 Otomatik İstatistiksel Yorum")
            avg_stress = df['Stres_Skoru'].mean()
            st.write(f"Genel Ortalama Stres Skoru: **{avg_stress:.2f}**")
            
            if avg_stress <= 1.5:
                st.success("Bölgedeki bitkiler mükemmel sağlık durumunda.")
            elif avg_stress <= 2.5:
                st.info("Bitkiler stabil, ancak hafif stres belirtileri izlenmeli.")
            elif avg_stress <= 3.5:
                st.warning("Dikkat! Bölgedeki bitkiler orta derecede stres altında. Rakım ve nemi inceleyin.")
            else:
                st.error("Kritik seviyede stres! Bölgedeki bitkiler yüksek risk altında, acil müdahale gerekebilir.")
                
            st.dataframe(df)
        else:
            st.info("Tablo şu an boş.")
    except Exception as e:
        st.error(f"Veri havuzu yüklenirken bir hata oluştu: {e}")
