import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64
import io

# --- DİL AYARLARI ---
LANGS = {
    "TR": {
        "title": "🌱 Future Farmers: Bilimsel Gözlem",
        "tab1": "Gözlem Kaydı", "tab2": "Veri Analizi",
        "region": "Bölge Seçiniz", "plant": "Bitki Türü",
        "alt": "Rakım (metre)", "weather": "Hava Durumu",
        "stress": "Stres Skoru (1-5)", "pest": "Tespit Edilen Zararlı",
        "ph": "PH Değeri", "notes": "Notlar", "cam": "Fotoğraf Çek",
        "send": "Veriyi Gönder", "success": "Veri başarıyla gönderildi!",
        "error": "Hata oluştu", "analysis": "📈 Ekolojik Analiz",
        "metric": "Ortalama Stres Skoru", "chart1": "Rakım ve Stres İlişkisi",
        "chart2": "Türlere Göre pH Dağılımı"
    },
    "EN": {
        "title": "🌱 Future Farmers: Scientific Observation",
        "tab1": "Observation Record", "tab2": "Data Analysis",
        "region": "Select Region", "plant": "Plant Type",
        "alt": "Altitude (meters)", "weather": "Weather",
        "stress": "Stress Score (1-5)", "pest": "Detected Pest",
        "ph": "PH Value", "notes": "Notes", "cam": "Take Photo",
        "send": "Send Data", "success": "Data sent successfully!",
        "error": "An error occurred", "analysis": "📈 Ecological Analysis",
        "metric": "Average Stress Score", "chart1": "Altitude vs Stress Relation",
        "chart2": "pH Distribution by Species"
    }
}

# --- CSS: KAMERA BOYUTLANDIRMA ---
st.markdown("""
    <style>
    [data-testid="stCameraInput"] {
        max-width: 300px;
    }
    </style>
""", unsafe_allow_html=True)

# --- YAPILANDIRMA ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzL_m9kH6d3kM1J25G5h2Y6hR_4z8pX3w/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTnBOJfkLuOrZyDQyhtMtcXgFYwfiu0OFaJfQUC9EpWajKGUcee2lzT8r1aNasf7xjiRdk3tTgXdj9o/pub?gid=0&single=true&output=csv"

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

lang_code = st.sidebar.selectbox("Language / Dil", ["TR", "EN"])
t = LANGS[lang_code]

st.title(t["title"])

tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

with tab1:
    ulke = st.selectbox(t["region"], list(PEST_DATABASE.keys()))
    bitki_turu = st.selectbox(t["plant"], list(PEST_DATABASE[ulke].keys()))
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input(t["alt"], 0, 2000, 200)
        hava = st.selectbox(t["weather"], ["Güneşli", "Bulutlu", "Yağmurlu", "Sisli"])
        stres = st.slider(t["stress"], 1, 5, 1)
        zararli_turu = st.selectbox(t["pest"], PEST_DATABASE[ulke][bitki_turu])
        ph_degeri = st.number_input(t["ph"], 0.0, 14.0, 7.0)
        notlar = st.text_area(t["notes"])
        foto = st.camera_input(t["cam"])
        
        submit = st.form_submit_button(t["send"])
        
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
                st.success(t["success"])
            except Exception as e:
                st.error(f"{t['error']}: {e}")

with tab2:
    st.header(t["analysis"])
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            df['Rakim'] = pd.to_numeric(df['Rakim'], errors='coerce')
            df['Stres_Skoru'] = pd.to_numeric(df['Stres_Skoru'], errors='coerce')
            df['PH'] = pd.to_numeric(df['PH'], errors='coerce')
            
            if not df.empty:
                fig1 = px.scatter(df, x="Rakim", y="Stres_Skoru", color="Hava_Durumu", size="Stres_Skoru", title=t["chart1"])
                st.plotly_chart(fig1, use_container_width=True)
                avg_stres = df['Stres_Skoru'].mean()
                st.metric(t["metric"], f"{avg_stres:.2f}")
                fig2 = px.box(df, x="Gozlem_Turu", y="PH", title=t["chart2"])
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Henüz yeterli veri girişi yapılmamış.")
        else:
            st.error(f"E-Tabloya ulaşılamadı. Hata kodu: {response.status_code}")
    except Exception as e:
        st.error(f"{t['error']}: {e}")
