import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
import base64

# --- ZARARLI VERİ TABANI ---
PEST_DATABASE = {
    "Çay Bitkisi": ["Yok", "Çay Filiz Güvesi", "Çay Koşnili", "Vampir Kelebek", "Kahverengi Kokarca"],
    "Diğer (Lütfen Yazınız)": ["Yok", "Bölgesel Zararlı Gözlemlenmedi"]
}

# ... existing code ... (Config ve Multilingual Content kısımlarını koruyun)

with tab1:
    gozlem_turu_secim = st.selectbox(c["obs"], list(PEST_DATABASE.keys()))
    
    if gozlem_turu_secim == "Diğer (Lütfen Yazınız)":
        gozlem_turu = st.text_input("Bitki Adı")
        zararli_options = PEST_DATABASE["Diğer (Lütfen Yazınız)"]
    else:
        gozlem_turu = gozlem_turu_secim
        zararli_options = PEST_DATABASE[gozlem_turu_secim]
    
    with st.form("main_form", clear_on_submit=True):
        rakim = st.number_input(c["alt"], 0, 2000, 200)
        hava = st.selectbox(c["weather"], c["w_opts"])
        stres = st.slider(c["stress"], 1, 5, 1)
        st.caption(c["stress_desc"]) 
        
        col1, col2 = st.columns(2)
        with col1:
            ph_degeri = st.number_input(c["ph"], 0.0, 14.0, 7.0)
        with col2:
            # Dinamik zararlı listesi buraya bağlandı
            zararli_turu = st.selectbox("Tespit Edilen Zararlı", zararli_options)
            
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

# --- ZARARLI VE BİTKİ VERİ TABANI ---
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
# ... existing code ...
```

### Neleri Değiştirdik?
1.  **`PEST_DATABASE` sözlüğü oluşturduk:** Zararlıları bitki türlerine göre gruplandırdık.
2.  **Dinamik Filtreleme:** `gozlem_turu_secim` seçimine göre `zararli_options` değişkenini güncelleyen bir `if` bloğu ekledik.
3.  **Form Entegrasyonu:** `st.selectbox` öğesinin `options` parametresine bu dinamik değişkeni (`zararli_options`) atadık. Böylece kullanıcı "Çay Bitkisi" seçtiğinde sadece çay zararlıları listelenecektir.

Bu değişikliği yaptığınızda, "Gözlem Türü" değiştiği anda altındaki "Tespit Edilen Zararlı" kutusu anında güncellenecektir. Kodunuzu GitHub'a bu şekilde aktarabilirsiniz.
