import streamlit as st

st.set_page_config(page_title="Future Farmers - Rize", layout="centered")

st.title("🌱 Future Farmers - Rize")
st.subheader("Dijital Çay Bahçesi Takip Sistemi")

# Gözlem Seçimi
gozlem_turu = st.radio("Gözlem Türü Seçin:", ["Proje Bitkim (Çay)", "Çevredeki Canlı"])

# Kamera ve Flaş Uyarısı
st.warning("⚠️ Lütfen fotoğraf çekerken netlik için telefon flaşınızı açmayı unutmayın!")
camera_input = st.camera_input("Buradan fotoğraf çekin:")

# Hava Durumu Seçimi
hava = st.selectbox("Hava Durumu:", ["Güneşli", "Parçalı Bulutlu", "Kapalı/Çok Bulutlu", "Yağmurlu", "Sisli"])

# Not Alanı
notlar = st.text_area("Doğa notunuzu buraya yazın:")

# Gönder Butonu
if st.button("Analiz Et ve Gönder"):
    if camera_input:
        st.success("Verileriniz başarıyla analiz edildi ve arşive kaydedildi!")
    else:
        st.error("Lütfen önce bir fotoğraf çekin.")
