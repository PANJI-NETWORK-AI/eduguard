import streamlit as st
import openai

# --- 1. KONFIGURASI HALAMAN (Wajib di Paling Atas) ---
st.set_page_config(page_title="EduGuard-AI Dashboard", layout="wide")

# --- 2. FUNGSI INISIALISASI CLIENT AI ---
def dapatkan_client_ai():
    try:
        # Mengambil API key dari Streamlit Secrets
        api_key = st.secrets["OPENROUTER_API_KEY"]
        return openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    except Exception as e:
        return None

# --- 3. UI UTAMA DASHBOARD ---
st.title("🛡️ EduGuard-AI Dashboard")
st.subheader("Sistem Analisis Progres Belajar Siswa")

# Panggil fungsi client AI
client = dapatkan_client_ai()

# --- 4. LOGIKA UTAMA (INDENTASI SUDAH DIPERBAIKI) ---
if client:
    st.success("Koneksi ke server AI OpenRouter Berhasil!")
    
    # Input Area untuk Data Aktivitas Siswa
    data_siswa = st.text_area(
        "Masukkan Data Aktivitas/Nilai Siswa untuk Analisis ZPD & Beban Kognitif:", 
        placeholder="Contoh: Siswa mengalami kesulitan memahami matriks pada pertemuan 6, nilai evaluasi menurun..."
    )
    
    # Tombol Analisis
    if st.button("🛡️ Mulai Analisis EduGuard-AI"):
        if data_siswa:
            with st.spinner("Model NVIDIA Nemotron sedang menganalisis data..."):
                try:
                    # Memanggil model reasoning gratis terbaik dari NVIDIA via OpenRouter
                    response = client.chat.completions.create(
                        model="nvidia/nemotron-3-ultra:free",
                        messages=[
                            {
                                "role": "system", 
                                "content": "Anda adalah AI pakar psikologi pendidikan dan informatika. Analisis data progres belajar siswa berikut untuk menentukan tingkat beban kognitif dan Zone of Proximal Development (ZPD) mereka."
                            },
                            {
                                "role": "user", 
                                "content": data_siswa
                            }
                        ]
                    )
                    
                    # Menampilkan Hasil Analisis
                    st.markdown("### 📊 Hasil Analisis EduGuard-AI:")
                    st.write(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memanggil model AI: {e}")
        else:
            st.warning("Harap isi data aktivitas siswa terlebih dahulu!")

else:
    # Pasangan else dari 'if client:' (Sudah Lurus & Sejajar)
    st.warning("Silakan periksa kembali konfigurasi OPENROUTER_API_KEY di menu Secrets Streamlit Cloud.")