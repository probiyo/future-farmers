import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64
import io

# --- YAPILANDIRMA ---
# Parantezleri ve hatalı biçimlendirmeyi temizledim
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzL_m9kH6d3kM1J25G5h2Y6hR_4z8pX3w/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

# --- ZARARLI VERİ TABANI ---
PEST_DATABASE = {
    "Türkiye": {
        "Çay Bitkisi": ["Yok", "Çay Filiz Güvesi", "Çay Koşnili", "Vampir Kelebek", "Kahverengi Kokarca"],
        "Cucumis sativus": ["Yok", "Yaprak Biti", "Kırmızı Örümcek", "Beyaz Sinek", "Salatalık Mildiyösü"],
        "Diğer": ["Yok", "Bölgesel Zararlı Gözlemlenmedi"]
    },
    "Belçika": {
        "Brassica oleracea (Brüksel Lahanası)": ["Yok", "Yaprak Biti (Aphids)", "Lahana Güvesi", "Toprak Piresi", "Salyangoz"],
        "Diğer": ["Yok", "Bölgesel Zararlı Gözlemlenmedi"]
    }
}

st.set_page_config(page_title="Future Farmers Pro", page_icon="🌱", layout="wide")
st.title("🌱 Future Farmers: Bilimsel Gözlem")

# --- STREAMLIT ARAYÜZÜ ---
tab1, tab2 = st.tabs(["Gözlem Kaydı", "Veri Analizi"])

with tab1:
    ulke = st.selectbox("Bölge Seçiniz", list(PEST_DATABASE.keys()))
    bitki_turu = st.selectbox("Bitki Türü", list(PEST_DATABASE[ulke].keys()))
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input("Rakım (metre)", 0, 2000, 200)
        hava = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağmurlu", "Sisli"])
        stres = st.slider("Stres Skoru (1-5)", 1, 5, 1)
        
        zararli_turu = st.selectbox("Tespit Edilen Zararlı", PEST_DATABASE[ulke][bitki_turu])
        ph_degeri = st.number_input("PH Değeri", 0.0, 14.0, 7.0)
        notlar = st.text_area("Notlar")
        foto = st.camera_input("Fotoğraf Çek")
        
        submit = st.form_submit_button("Veriyi Gönder")
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": f"{ulke} - {bitki_turu}",
                "Rakim": rakim,
                "Hava_Durumu": hava,
                "Stres_Skoru": stres,
                "Notlar": f"{notlar} | Zararlı: {zararli_turu}",
                "PH": ph_degeri,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=15)
                st.success("Veri başarıyla gönderildi!")
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

with tab2:
    st.header("📈 Ekolojik Analiz")
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            
            # Veri tiplerini temizle
            df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
            df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
            df['PH'] = pd.to_numeric(df['PH'], errors='coerce')
            
            if not df.empty:
                # 1. Grafik
                fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", 
                                 size="Stres_Skoru", title="Rakım ve Stres İlişkisi")
                st.plotly_chart(fig1, use_container_width=True)
                
                # 2. Özet
                avg_stres = df['Stres_Skoru'].mean()
                st.metric("Ortalama Stres Skoru", f"{avg_stres:.2f}")
                
                # 3. Grafik
                fig2 = px.box(df, x="Gozlem_Turu", y="PH", title="Türlere Göre pH Dağılımı")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Henüz yeterli veri girişi yapılmamış.")
        else:
            st.error(f"E-Tabloya ulaşılamadı. Hata kodu: {response.status_code}")
            
    except Exception as e:
        st.error(f"Analiz verisi işlenirken bir sorun oluştu: {e}")
