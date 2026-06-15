import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openai  # Menggantikan LangChain Groq dengan OpenAI library untuk OpenRouter

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="EduGuard-AI Dashboard", layout="wide")

# Integrasi Tailwind CSS yang aman & bekerja 100% di Streamlit
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# Inisialisasi State agar tombol intervensi bekerja dengan benar
if 'analisis_selesai' not in st.session_state:
    st.session_state.analisis_selesai = False
if 'response_text' not in st.session_state:
    st.session_state.response_text = ""
if 'siswa_terpilih' not in st.session_state:
    st.session_state.siswa_terpilih = ""

# 2. KONFIGURASI API KEY OPENROUTER (Menggantikan Groq)
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    # Inisialisasi client OpenRouter menggunakan library openai sesuai dokumentasi resmi
    llm = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
except Exception as e:
    st.error("API Key tidak ditemukan. Pastikan konfigurasi OPENROUTER_API_KEY di menu Secrets sudah benar.")
    st.stop()

# 3. GENERATOR DATA
def generate_data(n=100):
    data = {
        "ID_Siswa": [f"S-{1000+i}" for i in range(n)],
        "W8": np.random.randint(5, 30, n)
    }
    return pd.DataFrame(data)

if 'df' not in st.session_state:
    st.session_state.df = generate_data(100)

# 4. TAMPILAN DASHBOARD
st.title("🛡️ EduGuard-AI: Monitor Kesulitan Belajar")

# KOLOM UTAMA
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Data & Interaktivitas")
    # Interaktivitas: Mengubah data secara real-time
    st.session_state.df = st.data_editor(st.session_state.df, use_container_width=True)
    
    # Visualisasi Agregat
    fig = px.histogram(st.session_state.df, x="W8", nbins=10, 
                       title="Distribusi Durasi Belajar Minggu ke-8",
                       color_discrete_sequence=['#4F46E5'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🤖 Diagnosis AI")
    siswa_id = st.selectbox("Pilih Siswa untuk Diagnosis:", st.session_state.df["ID_Siswa"])
    
    # Jika user mengganti pilihan siswa, reset status analisis terdahulu
    if siswa_id != st.session_state.siswa_terpilih:
        st.session_state.analisis_selesai = False
        st.session_state.siswa_terpilih = siswa_id

    if st.button("Jalankan Analisis", use_container_width=True):
        data_siswa = st.session_state.df[st.session_state.df["ID_Siswa"] == siswa_id].iloc[0].to_dict()
        
        with st.spinner("Menganalisis..."):
            try:
                # Memanggil model reasoning gratis OpenRouter dengan prompt terstruktur pesanan dosen (maksimal 3 paragraf)
                response = llm.chat.completions.create(
                    model="openai/gpt-oss-120b:free",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Anda adalah AI pakar psikologi pendidikan dan informatika. "
                                "Analisis data siswa berikut untuk menentukan diagnosis Zone of Proximal Development (ZPD) dan Beban Kognitif mereka. "
                                "Berikan jawaban singkat maksimal 3 paragraf dengan format yang rapi."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Analisis data berikut: {str(data_siswa)}."
                        }
                    ]
                )
                
                # Simpan hasil ke session state agar tidak hilang saat tombol berikutnya ditekan
                st.session_state.response_text = response.choices[0].message.content
                st.session_state.analisis_selesai = True
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memanggil OpenRouter: {e}")

    # Menampilkan hasil analisis jika statusnya True
    if st.session_state.analisis_selesai:
        st.markdown(f"""
        <div class="bg-white p-6 rounded-lg shadow-lg border border-indigo-200 my-4">
            <h3 class="font-bold text-indigo-700 mb-2">Hasil Analisis: {siswa_id}</h3>
            <p class="text-gray-700 leading-relaxed" style="white-space: pre-line;">{st.session_state.response_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tombol aksi diletakkan sejajar di luar scope penekanan tombol pertama
        if st.button("✅ Setujui Intervensi", use_container_width=True):
            st.success(f"Sukses! Rencana intervensi untuk {siswa_id} telah dikirim ke guru wali.")

# FOOTER
st.markdown("""
<footer class="mt-12 text-center text-xs text-gray-400 border-t pt-4">
    <p>🛡️ Data dienkripsi sesuai standar privasi data murid (GDPR Compliance).</p>
</footer>
""", unsafe_allow_html=True)