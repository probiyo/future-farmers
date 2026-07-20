import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

st.set_page_config(page_title="Future Farmers Pro", layout="wide")

# --- DATA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

CONTENT = {
    "TR": {
        "title": "🌱 Future Farmers Pro",
        "tab1": "📊 Veri Girişi",
        "tab2": "📈 Ekolojik Analiz",
        "obs": "Gözlem Türü",
        "types": ["Çay Bitkisi", "Böcek Analizi", "Toprak Analizi"],
        "alt": "Rakım (m)",
        "weather": "Hava Durumu",
        "w_opts": ["Güneşli", "Bulutlu", "Yağmurlu", "Don", "Karlı"],
        "stress": "Stres Skoru (1-5)",
        "ph": "Toprak pH Değeri",
        "notes": "Notlar",
        "photo": "Bitki Fotoğrafı",
        "submit": "Veriyi Gönder",
        "report": "📊 Raporu Yazdır / Kaydet"
    }
}
lang = "TR"
c = CONTENT[lang]

st.title(c["title"])
tab1, tab2 = st.tabs([c["tab1"], c["tab2"]])

with tab1:
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            gozlem_turu = st.selectbox(c["obs"], c["types"])
            rakim = st.number_input(c["alt"], 0, 2000, 200)
            hava = st.selectbox(c["weather"], c["w_opts"])
        with col2:
            stres = st.slider(c["stress"], 1, 5, 1)
            ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0) if gozlem_turu == "Toprak Analizi" else 0.0
            notlar = st.text_area(c["notes"], height=68)
        
        # Kamera alanı küçültüldü
        foto = st.camera_input(c["photo"])
        submit = st.form_submit_button(c["submit"])
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava_Durumu": hava,
                "Stres_Skoru": stres,
                "Notlar": notlar,
                "PH": ph_degeri,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=15)
                st.success("Veri başarıyla kaydedildi!")
            except Exception as e:
                st.error(f"Hata: {e}")

with tab2:
    st.header(c["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        if not df.empty:
            fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", title="Rakım ve Stres İlişkisi")
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.bar(df, x="Gozlem_Turu", y="Stres_Skoru", color="Gozlem_Turu", title="Gözlem Türüne Göre Ortalama Stres")
            st.plotly_chart(fig2, use_container_width=True)
            
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(c["report"], data=csv_data, file_name="ekolojik_rapor.csv", mime="text/csv")
        else:
            st.warning("Henüz veri girilmemiş.")
    except Exception as e:
        st.error("Analiz verisi güncelleniyor, lütfen bekleyin...")
