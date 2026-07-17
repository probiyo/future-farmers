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

# --- MULTILINGUAL CONTENT ---
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
        "success": "Veri başarıyla gönderildi!",
        "pest_title": "🔍 Rize Çay Zararlıları Rehberi"
    },
    "EN": {
        "title": "🌱 Future Farmers Pro",
        "tab1": "📊 Data Entry",
        "tab2": "📈 Ecological Analysis",
        "obs": "Observation Type",
        "types": ["Tea Plant", "Pest Analysis", "Soil Analysis"],
        "alt": "Altitude (m)",
        "weather": "Weather",
        "w_opts": ["Sunny", "Cloudy", "Rainy", "Frost", "Snowy"],
        "stress": "Stress Score (1-5)",
        "ph": "Soil pH Level",
        "notes": "Notes",
        "photo": "Plant Photo",
        "submit": "Submit Data",
        "success": "Data sent successfully!",
        "pest_title": "🔍 Rize Tea Pest Guide"
    }
}

# --- SIDEBAR ---
lang = st.sidebar.radio("🌐 Language / Dil", ["TR", "EN"])
c = CONTENT[lang]

st.title(c["title"])
tab1, tab2 = st.tabs([c["tab1"], c["tab2"]])

with tab1:
    gozlem_turu = st.selectbox(c["obs"], c["types"])
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input(c["alt"], 0, 2000, 200)
        hava = st.selectbox(c["weather"], c["w_opts"])
        stres = st.slider(c["stress"], 1, 5, 1)
        
        ph_degeri = 0.0
        if gozlem_turu == "Toprak Analizi":
            ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0)
            
        notlar = st.text_area(c["notes"])
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
                st.success(c["success"])
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown(f"### {c['pest_title']}")
    cols = st.columns(5)
    # RTEÜ verilerine göre çay zararlıları listesi
    pest_data = [
        ("Sarı Çay Akarı", "https://cayihtisas.erdogan.edu.tr/Files/ckFiles/cayihtisas-erdogan-edu-tr/Sari_Cay_Akari.jpg"),
        ("Çay Koşnili", "https://cayihtisas.erdogan.edu.tr/Files/ckFiles/cayihtisas-erdogan-edu-tr/Cay_Kosnili.jpg"),
        ("Çay Filiz Güvesi", "https://cayihtisas.erdogan.edu.tr/Files/ckFiles/cayihtisas-erdogan-edu-tr/Cay_Filiz_Guvesi.jpg"),
        ("Vampir Kelebek (Ricania)", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ricania_simulans.jpg/200px-Ricania_simulans.jpg"),
        ("Kahverengi Kokarca", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Halyomorpha_halys_3.jpg/200px-Halyomorpha_halys_3.jpg")
    ]
    for i, (ad, resim) in enumerate(pest_data):
        with cols[i]:
            st.image(resim, use_container_width=True)
            st.caption(ad)

with tab2:
    st.header(c["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
        df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
        df['PH'] = pd.to_numeric(df['PH'], errors='coerce')
        df = df.dropna(subset=['Rakim', 'Stres_Skoru'])
        
        if not df.empty:
            # Grafik 1
            fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", title="Rakım ve Stres İlişkisi")
            st.plotly_chart(fig1, use_container_width=True)
            
            # Grafik 2 (pH Analizi)
            ph_df = df[df["PH"] > 0]
            if not ph_df.empty:
                st.subheader("🧪 pH - Stres Korelasyonu")
                fig2 = px.scatter(ph_df, x="PH", y="Stres_Skoru", color="Rakim", size="Stres_Skoru", title="pH Değerinin Stres Skoruna Etkisi")
                st.plotly_chart(fig2, use_container_width=True)
                
                c1, c2 = st.columns(2)
                c1.metric("Ortalama pH", round(ph_df["PH"].mean(), 2))
                c2.metric("Stresli Bitki Sayısı", int((ph_df["Stres_Skoru"] >= 4).sum()))
        else:
            st.warning("Veri bulunamadı.")
    except Exception as e:
        st.error(f"Analiz verisi yüklenemedi: {e}")
