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
        "stress_desc": "1: Çok Sağlıklı | 2: Hafif Solgun | 3: Orta Derece Stres | 4: Ciddi Stres | 5: Kritik / Kuruma Riski",
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
        "stress_desc": "1: Very Healthy | 2: Slightly Wilted | 3: Moderate Stress | 4: Severe Stress | 5: Critical / Drying Risk",
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
        st.caption(c["stress_desc"]) 
        
        # --- pH VE ZARARLI SEÇİMİ (AYRI PENCERELER) ---
        col1, col2 = st.columns(2)
        with col1:
            ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0)
        with col2:
            zararli_turu = st.selectbox("Tespit Edilen Zararlı", [
                "Yok", "Çay Filiz Güvesi", "Çay Koşnili", "Vampir Kelebek", "Kahverengi Kokarca", "Diğer"
            ])
        # -----------------------------------------------
            
        notlar = st.text_area(c["notes"])
        col_cam1, col_cam2 = st.columns([1, 3])
        with col_cam1:
            foto = st.camera_input(c["photo"])
        
        submit = st.form_submit_button(c["submit"])
        
        if submit:
            payload = {
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gozlem_Turu": gozlem_turu,
                "Rakim": rakim,
                "Hava_Durumu": hava,
                "Stres_Skoru": stres,
                "Notlar": f"{notlar} | Zararlı: {zararli_turu}",
                "PH": ph_degeri,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=15)
                st.success(c["success"])
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown(f"### {c['pest_title']}")
    pest_list = [
        ("Çay Filiz Güvesi (Parametriotes theae)", "https://agrobaseapp.com/turkey/pest/cay-filiz-guvesi"),
        ("Çay Koşnili", "https://agrobaseapp.com/turkey/pest/cay-kosnili"),
        ("Vampir Kelebek (Ricania)", "https://tr.wikipedia.org/wiki/Vampir_kelebek"),
        ("Kahverengi Kokarca", "https://arastirma.tarimorman.gov.tr/ktae/Sayfalar/Detay.aspx")
    ]
    for name, url in pest_list:
        st.markdown(f"- [{name}]({url})")

with tab2:
    st.header(c["tab2"])
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
        df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
        df['PH'] = pd.to_numeric(df['PH'], errors='coerce')
        df = df.dropna(subset=['Rakim', 'Stres_Skoru'])
        
        if not df.empty:
            fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", title="Rakım ve Stres İlişkisi")
            st.plotly_chart(fig1, use_container_width=True)
            
            avg_stres = df['Stres_Skoru'].mean()
            st.info(f"**Otomatik Analiz:** Genel stres ortalamanız: {avg_stres:.2f}. " + 
                    ("Yüksek stres gözlemlendi, acil inceleme önerilir!" if avg_stres > 3 else "Genel durum stabil ve sağlıklı görünüyor."))
            
            ph_df = df[df["PH"] > 0]
            if not ph_df.empty:
                st.subheader("🧪 pH - Stres Korelasyonu")
                fig2 = px.scatter(ph_df, x="PH", y="Stres_Skoru", color="Rakim", size="Stres_Skoru", title="pH Değerinin Stres Skoruna Etkisi")
                st.plotly_chart(fig2, use_container_width=True)
                
                avg_ph = ph_df['PH'].mean()
                if avg_ph < 6.5 or avg_ph > 7.5:
                    st.warning(f"Dikkat! Ortalama pH değeriniz ({avg_ph:.2f}) ideal aralığın (6.5-7.5) dışında.")
                else:
                    st.success(f"Toprak pH seviyesi ({avg_ph:.2f}) ideal aralıkta.")
        else:
            st.warning("Veri bulunamadı.")
    except Exception as e:
        st.error(f"Analiz verisi yüklenemedi: {e}")
