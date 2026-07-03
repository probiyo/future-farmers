import streamlit as st
import requests
import json
import base64
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Future Farmers - Portal",
    page_icon="🌱",
    layout="wide"
)

# 1. Canlı Google Apps Script API adresimiz:
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzpPAf0keTr8FLmsbdMuMRkVAZWyPKigwxTHSyZMiQRI2KSZXTFvWnXrEXsu15oFA_g/exec"

# 2. Canlı Google E-Tablo Paylaşım Linkimiz (Analiz panelinde otomatik görünmesi için):
# NOT: E-tablonuzun paylaşım ayarını "Bağlantıyı bilen herkes görüntüleyebilir" yapmayı unutmayın!
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No/edit?usp=sharing"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        color: #113425;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #4a5c53;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 30px;
    }
    .info-box {
        background-color: #f0f4f1;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #113425;
        margin-bottom: 25px;
        font-size: 1rem;
        line-height: 1.6;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #113425;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 5px;
    }
    .stButton>button {
        background-color: #113425 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        height: 48px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b4d37 !important;
    }
    </style>
""", unsafe_allow_html=True)

translations = {
    "Türkçe 🇹🇷": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Projesi Gözlem, Mikroklima & Bilimsel Analiz Portalı",
        "welcome": "🔬 <b>Sevgili Vatandaş Bilimciler,</b><br>Seçtiğiniz sabit çay bitkisinin gelişimini, rakıma ve hava koşullarına bağlı olarak gözlemleyip kaydediniz. Toplanan veriler anlık olarak aşağıdaki <b>Analiz & Raporlama</b> panelinde bilimsel grafiklere dönüştürülecektir.",
        "tab_entry": "📝 Veri Giriş Portalı",
        "tab_analytics": "📊 Bilimsel Analiz & Grafikler",
        "sec1_title": "### 1. Konum ve Ortam Koşulları / Location & Environment",
        "obs_type": "Gözlem Nesnesi / Türü:",
        "obs_options": ["Proje Bitkim (Çay)", "Diğer Tarım Bitkisi", "Çevredeki Doğal Canlı"],
        "altitude": "Bulunduğunuz Konumun Rakımı (Metre):",
        "altitude_help": "Telefonunuzun pusula veya altimetre uygulamasından yüksekliğinizi deniz seviyesine göre metre cinsinden yazın.",
        "weather": "Hava Durumu:",
        "weather_options": ["Güneşli", "Parçalı Bulutlu", "Çok Bulutlu / Kapalı", "Yağmurlu", "Sisli", "Karlı"],
        "sec2_title": "### 2. Bitki Sağlığı ve Gözlemler / Health & Observations",
        "stress": "Bitki Sağlık ve Stres Skoru (1-5):",
        "stress_help": "1: Çok Sağlıklı (Maksimum canlılık, bol taze sürgün), 2: Hafif Stres (Çok hafif renk açılması, gelişim durağanlığı), 3: Normal Gelişim (Standart sağlıklı seyir), 4: Belirgin Stres (Yaprak uçlarında kuruma, hafif sararma veya solma), 5: Kritik Stres (Yoğun kuruma, hastalık veya parazit istilası).",
        "notes": "Gözlem Notlarınız ve Bulgularınız:",
        "notes_placeholder": "Örn: Bu hafta yeni taze filizler (sürgünler) oluşmaya başladı. Yapraklarda lekelenme yok...",
        "photo_source": "Fotoğraf Ekleme Yöntemi:",
        "photo_camera": "Kamera ile Fotoğraf Çek 📸",
        "photo_upload": "Galeriden/Dosyadan Yükle 📁",
        "photo_camera_label": "Kamerayı Başlat ve Fotoğraf Çek:",
        "photo_upload_label": "Bitki Fotoğrafı Yükle (JPEG/PNG):",
        "photo_help": "Doğru analiz için her hafta aynı açıdan ve mesafeden fotoğraf çekmeye özen gösterin.",
        "submit_btn": "Verileri Bilim Veritabanına Gönder 🚀",
        "err_config": "⚠️ Sistem Ayarı Eksik: Lütfen geçerli bir Apps Script adresi tanımlayın!",
        "err_photo": "⚠️ Lütfen bilimsel kanıt olarak bitkinizin bir fotoğrafını çekin veya yükleyin!",
        "spinner": "Verileriniz şifreleniyor ve veri havuzuna aktarılıyor...",
        "success": "🎉 Harika! Gözlem verileriniz başarıyla kaydedildi. Bir sonraki haftalık gözlemde görüşmek üzere vatandaş bilimci!",
        "err_server": "Sunucudan geçersiz yanıt alındı: ",
        "err_general": "Veri gönderilirken bir hata oluştu: ",
        # Dashboard Translations
        "db_intro": "Bu panel, Rize genelinde farklı rakımlarda yapılan çay bitkisi gözlemlerinin iklim parametreleri ile ilişkisini canlı olarak gösterir.",
        "db_source": "Veri Kaynağı Seçimi:",
        "db_source_demo": "Örnek Proje Verileri (Demo Modu)",
        "db_source_live": "Canlı E-Tablo Verilerim (Google Sheets)",
        "db_sheet_url": "Google E-Tablo Paylaşım Linkini Girin:",
        "db_sheet_help": "E-tablonuzu 'Bağlantıyı sahip olan herkes görüntüleyebilir' şeklinde paylaşıp linkini buraya yapıştırın.",
        "stat_total": "Toplam Gözlem Sayısı",
        "stat_alt": "Ortalama Ölçülen Rakım",
        "stat_stress": "Ortalama Stres Skoru",
        "chart_title_1": "⛰| Rakıma Göre Bitki Stres Dağılımı (Korelasyon)",
        "chart_title_2": "☁| Hava Durumuna Göre Stres Seviyeleri",
        "chart_desc_1": "Bu grafik, dikey yükseklik (rakım) artışının çay bitkisindeki stres skoru üzerindeki fizyolojik etkilerini analiz eder.",
        "chart_desc_2": "Farklı mikro-hava koşullarının bitki sağlığı üzerindeki anlık yansımalarını gösterir.",
        "table_title": "📋 Son Gözlem Kayıtları ve Saha Notları"
    },
    "English 🇬🇧": {
        "title": "Future Farmers 🌱",
        "subtitle": "Scientix Project Observation, Microclimate & Scientific Analysis Portal",
        "welcome": "🔬 <b>Dear Citizen Scientists,</b><br>Please observe and record the growth of your selected tea plant based on altitude and weather conditions. Collected data will be instantly visualized in the <b>Analysis & Dashboard</b> panel below.",
        "tab_entry": "📝 Data Entry Portal",
        "tab_analytics": "📊 Scientific Analysis & Charts",
        "sec1_title": "### 1. Location and Environmental Conditions",
        "obs_type": "Observation Object / Type:",
        "obs_options": ["My Project Plant (Tea)", "Other Agricultural Plant", "Surrounding Natural Organism"],
        "altitude": "Altitude of Your Location (Meters):",
        "altitude_help": "Enter your altitude in meters from your phone's compass or altimeter app.",
        "weather": "Weather Condition:",
        "weather_options": ["Sunny", "Partly Cloudy", "Overcast / Cloudy", "Rainy", "Foggy", "Snowy"],
        "sec2_title": "### 2. Plant Health and Observations",
        "stress": "Plant Health & Stress Score (1-5):",
        "stress_help": "1: Excellent (Vibrant, lots of shoots), 2: Mild Stress (Slight discoloration, slow growth), 3: Moderate Health (Standard healthy growth), 4: High Stress (Dry tips, visible wilting), 5: Severe Stress (Advanced disease, critical loss risk).",
        "notes": "Your Observation Notes & Findings:",
        "notes_placeholder": "e.g., New fresh shoots started to form this week. No yellowing on leaves...",
        "photo_source": "Photo Adding Method:",
        "photo_camera": "Take Photo with Camera 📸",
        "photo_upload": "Upload from Gallery/File 📁",
        "photo_camera_label": "Start Camera and Take Photo:",
        "photo_upload_label": "Upload Plant Photo (JPEG/PNG):",
        "photo_help": "For accurate analysis, try to take the photo from the same angle and distance each week.",
        "submit_btn": "Submit Data to Scientific Database 🚀",
        "err_config": "⚠️ System Configuration Missing: Please embed your valid Apps Script address!",
        "err_photo": "⚠️ Please upload or take a photo of your plant as scientific evidence!",
        "spinner": "Encrypting your data and transferring to the scientific database...",
        "success": "🎉 Fantastic! Your observation data has been successfully recorded. See you next week, citizen scientist!",
        "err_server": "Invalid response received from server: ",
        "err_general": "An error occurred while sending data: ",
        # Dashboard Translations
        "db_intro": "This panel demonstrates live correlations between tea plant observations at various altitudes and microclimatic parameters in Rize.",
        "db_source": "Select Data Source:",
        "db_source_demo": "Sample Project Data (Demo Mode)",
        "db_source_live": "My Live Spreadsheet (Google Sheets)",
        "db_sheet_url": "Enter Google Sheet Share Link:",
        "db_sheet_help": "Ensure your Google Sheet share setting is 'Anyone with link can view' and paste the link here.",
        "stat_total": "Total Observations",
        "stat_alt": "Average Measured Altitude",
        "stat_stress": "Average Stress Score",
        "chart_title_1": "⛰| Plant Stress vs Altitude (Correlation Analysis)",
        "chart_title_2": "☁| Stress Levels by Weather Condition",
        "chart_desc_1": "This chart analyzes the physiological impact of vertical altitude increase on the tea plant's stress scores.",
        "chart_desc_2": "Displays the immediate reflection of different micro-weather conditions on overall plant health.",
        "table_title": "📋 Recent Observation Logs & Field Notes"
    }
}

selected_lang = st.sidebar.radio("Language / Dil Seçin", ["Türkçe 🇹🇷", "English 🇬🇧"])
t = translations[selected_lang]

st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_form, tab_analysis = st.tabs([t["tab_entry"], t["tab_analytics"]])

with tab_form:
    st.markdown(f"<div class='info-box'>{t['welcome']}</div>", unsafe_allow_html=True)
    
    with st.form("gozlem_formu", clear_on_submit=False):
        st.markdown(t["sec1_title"])
        
        gozlem_turu = st.selectbox(t["obs_type"], t["obs_options"])
        
        rakim = st.number_input(
            t["altitude"],
            min_value=0,
            max_value=2500,
            value=0,
            step=5,
            help=t["altitude_help"]
        )
        
        hava_durumu = st.selectbox(t["weather"], t["weather_options"])
        
        st.markdown("---")
        st.markdown(t["sec2_title"])
        
        stres_skoru = st.slider(
            t["stress"],
            min_value=1,
            max_value=5,
            value=3,
            help=t["stress_help"]
        )
        
        gozlem_notlari = st.text_area(
            t["notes"],
            placeholder=t["notes_placeholder"]
        )
        
        foto_yontemi = st.radio(
            t["photo_source"],
            [t["photo_camera"], t["photo_upload"]],
            horizontal=True
        )
        
        uploaded_file = None
        if foto_yontemi == t["photo_camera"]:
            uploaded_file = st.camera_input(
                t["photo_camera_label"],
                help=t["photo_help"]
            )
        else:
            uploaded_file = st.file_uploader(
                t["photo_upload_label"],
                type=["jpg", "jpeg", "png"],
                help=t["photo_help"]
            )
        
        submitted = st.form_submit_button(t["submit_btn"])

        if submitted:
            if not WEB_APP_URL or WEB_APP_URL == "BURAYA_KOPYALADIGINIZ_YENI_URL_YAPISTIRIN" or not WEB_APP_URL.startswith("https://"):
                st.error(t["err_config"])
            elif not uploaded_file:
                st.error(t["err_photo"])
            else:
                with st.spinner(t["spinner"]):
                    try:
                        bytes_data = uploaded_file.read()
                        base64_image = base64.b64encode(bytes_data).decode('utf-8')
                        
                        payload = {
                            "Tarih": datetime.now().strftime("%d-%m-%Y %H:%M"),
                            "Gozlem_Turu": gozlem_turu,
                            "Rakim": int(rakim),
                            "Hava_Durumu": hava_durumu,
                            "Stres_Skoru": int(stres_skoru),
                            "Notlar": gozlem_notlari,
                            "Foto_Base64": base64_image
                        }
                        
                        headers = {'Content-Type': 'application/json'}
                        response = requests.post(WEB_APP_URL, data=json.dumps(payload), headers=headers)
                        
                        if response.status_code == 200 and "Başarılı" in response.text:
                            st.success(t["success"])
                            st.balloons()
                        else:
                            st.error(f"{t['err_server']}{response.text}")
                            
                    except Exception as e:
                        st.error(f"{t['err_general']}{str(e)}")

with tab_analysis:
    st.markdown(f"<p style='color:#4a5c53; font-size:1.05rem; margin-bottom: 20px;'>{t['db_intro']}</p>", unsafe_allow_html=True)
    
    # Varsayılan olarak canlı tablo linki varsa otomatik "Canlı E-Tablo" seçeneğini aktif et, yoksa demoyu seç
    default_source_index = 1 if DEFAULT_GOOGLE_SHEET_URL != "BURAYA_GOOGLE_ETABLO_LINKINIZI_YAPISTIRIN" else 0
    source_type = st.radio(t["db_source"], [t["db_source_demo"], t["db_source_live"]], index=default_source_index, horizontal=True)
    
    df = None
    
    if source_type == t["db_source_demo"]:
        # Generates realistic mock data simulating various Rize microclimates
        np.random.seed(42)
        demo_records = 32
        
        # Simulating realistic correlation: Higher altitude usually equals slightly more microclimatic stress (wind & cold)
        simulated_altitudes = np.random.randint(20, 950, size=demo_records)
        simulated_stress = []
        for alt in simulated_altitudes:
            if alt < 200:
                stress = np.random.choice([1, 2, 3], p=[0.5, 0.4, 0.1])
            elif alt < 500:
                stress = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])
            else:
                stress = np.random.choice([3, 4, 5], p=[0.2, 0.4, 0.4])
            simulated_stress.append(int(stress))
            
        demo_data = {
            "Tarih": pd.date_range(end=datetime.now(), periods=demo_records, freq='D').strftime("%d-%m-%Y %H:%M"),
            "Gozlem_Turu": np.random.choice(["Proje Bitkim (Çay)", "Diğer Tarım Bitkisi"], size=demo_records, p=[0.8, 0.2]),
            "Rakim": simulated_altitudes,
            "Hava_Durumu": np.random.choice(t["weather_options"], size=demo_records),
            "Stres_Skoru": simulated_stress,
            "Notlar": [
                f"Yükseklik gözlemi yapıldı. Sürgün boyu normal." if s <= 3 else f"Rüzgarlı hava ve soğuk nedeniyle yaprak uçlarında hafif kuruma ve stres saptandı."
                for s in simulated_stress
            ]
        }
        df = pd.DataFrame(demo_data)
    else:
        # En tepedeki default link varsa otomatik buraya yazar, yoksa boş input kutusu gösterir
        initial_url_val = DEFAULT_GOOGLE_SHEET_URL if DEFAULT_GOOGLE_SHEET_URL != "BURAYA_GOOGLE_ETABLO_LINKINIZI_YAPISTIRIN" else ""
        sheet_url = st.text_input(t["db_sheet_url"], value=initial_url_val, placeholder="https://docs.google.com/spreadsheets/d/...", help=t["db_sheet_help"])
        
        if sheet_url:
            try:
                # Converts default Google Sheet links into direct download links for instant pandas parsing
                if "/edit" in sheet_url:
                    csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
                else:
                    csv_url = sheet_url
                
                raw_df = pd.read_csv(csv_url)
                
                # Maps spreadsheet columns safely in case user customized names
                # Index position assumptions: 0: Date, 1: Type, 2: Altitude, 3: Weather, 4: Stress, 5: Notes
                df = pd.DataFrame()
                df["Tarih"] = raw_df.iloc[:, 0]
                df["Gozlem_Turu"] = raw_df.iloc[:, 1]
                df["Rakim"] = pd.to_numeric(raw_df.iloc[:, 2], errors='coerce').fillna(0).astype(int)
                df["Hava_Durumu"] = raw_df.iloc[:, 3]
                df["Stres_Skoru"] = pd.to_numeric(raw_df.iloc[:, 4], errors='coerce').fillna(3).astype(int)
                df["Notlar"] = raw_df.iloc[:, 5]
            except Exception as e:
                st.warning("E-Tablo verileri yüklenirken bir hata oluştu. Linkin paylaşım izinlerinin 'Bağlantıyı bilen herkes' olarak açık olduğundan emin olun.")
                df = None

    if df is not None and not df.empty:
        # Key Summary Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{len(df)}</div>
                    <div class='metric-label'>{t['stat_total']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            avg_alt = int(df["Rakim"].mean())
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{avg_alt} m</div>
                    <div class='metric-label'>{t['stat_alt']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            avg_stress = round(df["Stres_Skoru"].mean(), 2)
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{avg_stress} / 5.0</div>
                    <div class='metric-label'>{t['stat_stress']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown(f"#### {t['chart_title_1']}")
            st.markdown(f"<p style='font-size:0.85rem; color:#64748b; margin-bottom:10px;'>{t['chart_desc_1']}</p>", unsafe_allow_html=True)
            
            # Scatter Plot mapping Altitude vs Plant Stress
            chart_data = df[["Rakim", "Stres_Skoru"]].copy()
            st.scatter_chart(
                data=chart_data,
                x="Rakim",
                y="Stres_Skoru",
                color="#113425",
                use_container_width=True
            )
            
        with chart_col2:
            st.markdown(f"#### {t['chart_title_2']}")
            st.markdown(f"<p style='font-size:0.85rem; color:#64748b; margin-bottom:10px;'>{t['chart_desc_2']}</p>", unsafe_allow_html=True)
            
            # Bar Chart mapping Stress Scores per weather condition
            weather_stresses = df.groupby("Hava_Durumu")["Stres_Skoru"].mean().reset_index()
            st.bar_chart(
                data=weather_stresses,
                x="Hava_Durumu",
                y="Stres_Skoru",
                color="#b45309",
                use_container_width=True
            )
            
        st.write("---")
        
        # Complete searchable scientific records table
        st.markdown(f"#### {t['table_title']}")
        st.dataframe(df[["Tarih", "Gozlem_Turu", "Rakim", "Hava_Durumu", "Stres_Skoru", "Notlar"]], use_container_width=True)
        
    else:
        if source_type == t["db_source_live"]:
            st.info("Lütfen canlı verilerinizi görmek için geçerli bir Google E-Tablo paylaşım linki giriniz.")
