import streamlit as st
import pandas as pd
import requests
import json
import base64
from datetime import datetime

st.set_page_config(page_title="Future Farmers Pro", layout="wide")

c = {
    "title": "Future Farmers: Rize Ekolojik İzleme",
    "notes": "Gözlemlerinizi buraya not edebilirsiniz...",
    "submit": "Gözlemi Kaydet"
}

st.title(c["title"])

# API URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw6U5_hI889oB9xH-80hD6Z6k641_V7B3o0c_t6x8r1yQJg3H-h8YqG_K_M6z4n/exec"

with st.form("gozlem_formu"):
    tarih = st.date_input("Gözlem Tarihi")
    gozlem_turu = st.selectbox("Gözlem Türü", ["Bitki Gelişimi", "Böcek Analizi", "Toprak Analizi"])
    rakim = st.number_input("Rakım (m)", min_value=0, max_value=2000, value=200)
    hava_durumu = st.selectbox("Hava Durumu", ["Güneşli", "Bulutlu", "Yağışlı", "Sisli"])
    stres_skoru = st.slider("Bitki Stres Skoru (1-5)", 1, 5, 1)
    
    if gozlem_turu == "Böcek Analizi":
        zararli_turu = st.selectbox("Tespit Edilen Zararlı", [
            "Çay Koşnili", "Çay Filiz Güvesi (Parametriotes theae)", 
            "Vampir Kelebek", "Kahverengi Kokarca", "Diğer"
        ])
        
    notlar = st.text_area(c["notes"])
    foto = st.camera_input("Bitki Fotoğrafı Çek")
    
    submitted = st.form_submit_button(c["submit"])

if submitted:
    foto_base64 = "Test_Verisi"
    if foto:
        foto_bytes = foto.getvalue()
        foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
    
    payload = {
        "Tarih": str(tarih),
        "Gozlem_Turu": gozlem_turu,
        "Rakim": rakim,
        "Hava_Durumu": hava_durumu,
        "Stres_Skoru": stres_skoru,
        "Notlar": notlar,
        "Foto_Base64": foto_base64,
        "PH": "" 
    }
    
    try:
        response = requests.post(WEB_APP_URL, json=payload)
        if response.text == "Başarılı":
            st.success("Veri başarıyla kaydedildi!")
        else:
            st.error(f"Hata: {response.text}")
    except Exception as e:
        st.error(f"Bağlantı hatası: {str(e)}")

st.markdown("---")
st.subheader("🎓 Zararlı İzleme Kaynakları")

pest_list = [
    ("Çay Koşnili", "https://agrobaseapp.com/turkey/pest/cay-kosnili"),
    ("Çay Filiz Güvesi (Parametriotes theae)", "https://arastirma.tarimorman.gov.tr/ktae/Sayfalar/Detay.aspx?TermStoreId=368e785b-af33-487d-a98d-c11d5495130b&TermSetId=279e10a1-a60d-421b-9d0c-a06a9ce2ebfa&TermId=2b9226ff-4a3b-4ab9-a217-c4482dc84dfa&UrlSuffix=25/Cay-Filiz-Guvesi"),
    ("Vampir Kelebek (Ricania)", "https://tr.wikipedia.org/wiki/Vampir_kelebek"),
    ("Kahverengi Kokarca", "https://arastirma.tarimorman.gov.tr/ktae/Sayfalar/Detay.aspx?TermStoreId=368e785b-af33-487d-a98d-c11d5495130b&TermSetId=279e10a1-a60d-421b-9d0c-a06a9ce2ebfa&TermId=2b9226ff-4a3b-4ab9-a217-c4482dc84dfa&UrlSuffix=25/Kahverengi-Kokarca")
]

for name, url in pest_list:
    st.markdown(f"- [{name}]({url})")
