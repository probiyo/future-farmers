import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

st.set_page_config(page_title="Future Farmers Pro", layout="wide")

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
        "stress_exp": "Stres Skoru Anlamları",
        "stress_desc": "1: Çok Sağlıklı, 2: İyi, 3: Orta (Gözlem Gerekli), 4: Stresli, 5: Kritik (Acil Müdahale)",
        "notes": "Notlar",
        "photo": "Bitki Fotoğrafı",
        "submit": "Veriyi Gönder",
        "success": "Veri başarıyla gönderildi!",
        "pest_title": "🔍 Rize Çay Zararlıları Rehberi",
        "pest_info": {
            "Sarı Çay Akarı": ("Polphagotarsonemus latus (Acari: Tarsonemidae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Polyphagotarsonemus_latus.jpg/300px-Polyphagotarsonemus_latus.jpg"),
            "Siyah Turunçgil Yaprak Biti": ("Toxoptera aurantii (Homoptera: Aphididae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Toxoptera_aurantii.jpg/300px-Toxoptera_aurantii.jpg"),
            "Çay Koşnili": ("Chloropulvinaria floccifera (Homoptera: Coccidae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Chloropulvinaria_floccifera.jpg/300px-Chloropulvinaria_floccifera.jpg"),
            "Çay Filiz Güvesi": ("Parametriotes theae (Lepidoptera: Coleophoridae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Parametriotes_theae.jpg/300px-Parametriotes_theae.jpg"),
            "Yalancı Kelebek": ("Orasanga japonica (Hemiptera: Ricaniidae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Orasanga_japonica.jpg/300px-Orasanga_japonica.jpg")
        }
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
        "stress_exp": "Meaning of Stress Scores",
        "stress_desc": "1: Very Healthy, 2: Good, 3: Moderate (Monitor), 4: Stressed, 5: Critical (Immediate Action)",
        "notes": "Notes",
        "photo": "Plant Photo",
        "submit": "Submit Data",
        "success": "Data sent successfully!",
        "pest_title": "🔍 Rize Tea Pest Guide",
        "pest_info": {
            "Broad Mite": ("Polphagotarsonemus latus (Acari: Tarsonemidae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Polyphagotarsonemus_latus.jpg/300px-Polyphagotarsonemus_latus.jpg"),
            "Black Citrus Aphid": ("Toxoptera aurantii (Homoptera: Aphididae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Toxoptera_aurantii.jpg/300px-Toxoptera_aurantii.jpg"),
            "Tea Scale": ("Chloropulvinaria floccifera (Homoptera: Coccidae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Chloropulvinaria_floccifera.jpg/300px-Chloropulvinaria_floccifera.jpg"),
            "Tea Leaf Moth": ("Parametriotes theae (Lepidoptera: Coleophoridae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Parametriotes_theae.jpg/300px-Parametriotes_theae.jpg"),
            "False Butterfly": ("Orasanga japonica (Hemiptera: Ricaniidae)", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Orasanga_japonica.jpg/300px-Orasanga_japonica.jpg")
        }
    }
}

# --- SIDEBAR LANGUAGE ---
lang = st.sidebar.radio("🌐 Language / Dil", ["TR", "EN"])
c = CONTENT[lang]

st.title(c["title"])
tab1, tab2 = st.tabs([c["tab1"], c["tab2"]])

# --- DATA SUBMISSION ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwoMSJje6QqoCd7L8lkvlIkGAHMnUzriUnX0jsiJm08rvO2gxAks8wzE6z8JQpCFcg6/exec"

with tab1:
    gozlem_turu = st.selectbox(c["obs"], c["types"])
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input(c["alt"], 0, 2000, 200)
        hava = st.selectbox(c["weather"], c["w_opts"])
        stres = st.slider(c["stress"], 1, 5, 1)
        
        with st.expander(c["stress_exp"]):
            st.write(c["stress_desc"])
            
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
                "PH": 0.0,
                "Foto_Base64": "Test_Verisi" if not foto else base64.b64encode(foto.read()).decode()
            }
            try:
                requests.post(WEB_APP_URL, json=payload, timeout=15)
                st.success(c["success"])
            except Exception as e:
                st.error(f"Error: {e}")

    # --- PEST GUIDE ---
    st.markdown(f"### {c['pest_title']}")
    cols = st.columns(len(c["pest_info"]))
    for i, (name, (latin, img)) in enumerate(c["pest_info"].items()):
        with cols[i]:
            st.image(img, use_container_width=True)
            st.caption(f"**{name}**\n*{latin}*")

# --- ANALYSIS TAB ---
with tab2:
    st.header(c["tab2"])
    # ... (Buradaki analiz kısmı mevcut yapıda kalmaya devam edecek)
