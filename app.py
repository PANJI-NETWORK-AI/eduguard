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
    if client:
    st.success("Koneksi ke server AI OpenRouter Berhasil!")
    
    # 1. Input Data Siswa (Contoh)
    data_siswa = st.text_area("Masukkan Data Aktivitas/Nilai Siswa:", 
                              placeholder="Contoh: Siswa Panji, Nilai Tugas 1: 85, Tugas 2: 40 (mengalami kendala di fungsi matriks)...")
    
    # 2. Tombol untuk Eksekusi AI
    if st.button("🛡️ Mulai Analisis EduGuard-AI"):
        if data_siswa:
            with st.spinner("Model NVIDIA Nemotron sedang menganalisis beban kognitif..."):
                try:
                    # Menembak ke model OpenRouter gratisan
                    response = client.chat.completions.create(
                        model="nvidia/nemotron-3-ultra:free",
                        messages=[
                            {"role": "system", "content": "Anda adalah AI pakar psikologi pendidikan. Analisis data siswa untuk mendeteksi kesulitan belajar dan ZPD mereka."},
                            {"role": "user", "content": data_siswa}
                        ]
                    )
                    
                    # Menampilkan hasil dari AI ke layar dashboard
                    st.markdown("### 📊 Hasil Analisis AI:")
                    st.write(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memanggil AI: {e}")
        else:
            st.warning("Harap isi data siswa terlebih dahulu sebelum menganalisis!")
    
    # Taruh sisa logika dashboard kamu di bawah sini...
    # (Contoh: tombol analisis, pemanggilan model nvidia/nemotron-3-ultra:free, dll)
else:
    st.warning("Silakan periksa kembali konfigurasi OPENROUTER_API_KEY di menu Secrets.")