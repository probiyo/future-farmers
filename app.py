import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- CONFIG ---
st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# --- DATA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

st.title("🌱 Future Farmers Pro")
tab1, tab2 = st.tabs(["📊 Veri Girişi", "📈 Ekolojik Analiz"])

with tab1:
    gozlem_turu = st.selectbox("Gözlem Türü", ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"])
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input("Rakım (m)", 0, 2000, 200)
        hava = st.selectbox("Hava", ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"])
        stres = st.slider("Stres", 1, 5, 1)
        
        ph_degeri = 0.0
        if gozlem_turu == "Toprak Analizi":
            ph_degeri = st.number_input("pH", 0.0, 14.0, 7.0)
        
        notlar = st.text_area("Notlar")
        foto = st.camera_input("Bitki Fotoğrafı")
        
        submit = st.form_submit_button("Veriyi Gönder")
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava_Durumu": hava, # Tablo ile uyumlu hale getirildi
                "Stres_Skoru": stres, # Tablo ile uyumlu hale getirildi
                "Notlar": notlar,
                "PH": ph_degeri,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=10)
                st.success("Veri başarıyla gönderildi!")
            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")

with tab2:
    st.header("📈 Ekolojik Analiz")
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        if not df.empty:
            fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", title="Rakım ve Stres İlişkisi")
            st.plotly_chart(fig1, use_container_width=True)
            
            if "PH" in df.columns:
                ph_df = df[df["PH"] > 0]
                if not ph_df.empty:
                    st.subheader("🧪 pH - Stres Korelasyonu")
                    # pH verisini görselleştirme
                    fig2 = px.scatter(ph_df, x="PH", y="Stres_Skoru", color="Rakim", size="Stres_Skoru", 
                                      title="pH Değerinin Stres Skoruna Etkisi",
                                      labels={"PH": "Toprak pH Değeri", "Stres_Skoru": "Stres Skoru (1-5)"})
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # pH istatistikleri
                    col1, col2 = st.columns(2)
                    col1.metric("Ortalama pH", round(ph_df["PH"].mean(), 2))
                    col2.metric("Stresli Bitki Sayısı", len(ph_df[ph_df["Stres_Skoru"] >= 4]))
                else:
                    st.info("pH verisi henüz yeterli değil.")
            else:
                st.warning("pH sütunu veri tabanında bulunamadı.")
        else:
            st.warning("Henüz veri bulunmuyor.")
    except Exception as e:
        st.error(f"Veri havuzuna bağlanılamadı. Hata: {e}")
