import streamlit as st
import openai

# Pindahkan inisialisasi client ke dalam fungsi atau setelah elemen UI dasar dimuat
def dapatkan_client_ai():
    try:
        # Mengambil key dari Streamlit Secrets
        api_key = st.secrets["OPENROUTER_API_KEY"]
        
        return openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    except Exception as e:
        st.error(f"Gagal menghubungkan AI: {e}")
        return None

# --- BAGIAN UI UTAMA (Ditaruh di atas agar halaman tidak blank) ---
st.set_page_config(page_title="EduGuard-AI Dashboard", layout="wide")
st.title("🛡️ EduGuard-AI Dashboard")
st.subheader("Sistem Analisis Progres Belajar Siswa")

# Panggil client-nya di sini
client = dapatkan_client_ai()

# Contoh input atau tombol yang kamu punya di dashboard
if client:
    st.success("Koneksi ke server AI OpenRouter Berhasil!")
    
    # Taruh sisa logika dashboard kamu di bawah sini...
    # (Contoh: tombol analisis, pemanggilan model nvidia/nemotron-3-ultra:free, dll)
else:
    st.warning("Silakan periksa kembali konfigurasi OPENROUTER_API_KEY di menu Secrets.")