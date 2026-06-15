import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from langchain_openai import ChatOpenAI

# ==============================================================================
# CONFIG & INTERFACE CONFIGURATION (Siap Lomba)
# ==============================================================================
st.set_page_config(
    page_title="EduGuard-AI: Early Warning System Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling agar tampilan rapi & profesional
st.markdown("""
    <style>
    /* Kode CSS kustom dashboard EduGuard kamu di sini */
    </style>
""", unsafe_allow_html=True)

# Title & Deskripsi Proyek
st.title("🛡️ EduGuard-AI Dashboard")
st.subheader("Digital Innovation and Creative Intelligence for Sustainable Education")

# ==============================================================================
# INTEGRASI MODEL-AGNOSTIC GATEWAY (OPENROUTER API) - LANGKAH 2
# ==============================================================================
st.sidebar.header("⚙️ Pengaturan AI Advisor")

# Opsi Model-Agnostic Gateway agar juri terkesan (Bisa ganti vendor AI dalam 1 klik)
model_options = {
    "Meta: Llama 3 8B (Free)": "meta-llama/llama-3-8b-instruct:free",
    "Mistral 7B Instruct (Free)": "mistralai/mistral-7b-instruct:free",
    "OpenAI: GPT-4o Mini": "openai/gpt-4o-mini"
}
selected_model_name = st.sidebar.selectbox("Pilih AI Engine / Model:", list(model_options.keys()))
selected_model_id = model_options[selected_model_name]

# Inisialisasi API OpenRouter secara aman lewat Streamlit Secrets
try:
    # Membaca API Key OpenRouter dari secrets.toml atau Advanced Settings Cloud
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    
    llm = ChatOpenAI(
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name=selected_model_id,
        temperature=0.7
    )
except Exception as e:
    st.sidebar.error("⚠️ API Key tidak ditemukan. Pastikan secrets.toml sudah terisi dengan benar.")
    llm = None

# ==============================================================================
# SIMULASI SKALABILITAS DATA 100 SISWA - LANGKAH 3
# ==============================================================================
@st.cache_data
def generate_student_data():
    np.random.seed(42) # Agar data tetap konsisten setiap refresh
    nama_siswa = [f"Siswa {i}" for i in range(1, 101)]
    
    # Menghasilkan nilai mingguan otomatis (W1 sampai W8)
    data = {
        "ID Siswa": [f"EG-{str(i).zfill(3)}" for i in range(1, 101)],
        "Nama Siswa": nama_siswa,
        "Rata-rata Tugas": np.random.randint(55, 95, size=100),
        "Kehadiran (%)": np.random.randint(70, 100, size=100),
        "Skor Keaktifan": np.random.randint(50, 100, size=100),
        "Status Risiko": "Aman" # Placeholder, akan diperbarui oleh EWS
    }
    
    df = pd.DataFrame(data)
    
    # Logika Otomatis Menentukan Siswa Berisiko (Kriteria EWS)
    # Jika Rata-rata Tugas < 65 ATAU Kehadiran < 80%, otomatis dikategorikan "Butuh Perhatian"
    df.loc[(df["Rata-rata Tugas"] < 65) | (df["Kehadiran (%)"] < 80), "Status Risiko"] = "Butuh Perhatian"
    return df

df_siswa = generate_student_data()

# ==============================================================================
# FITUR UTAMA LOMBA: EARLY WARNING SYSTEM (EWS)
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.header("🎯 Filter Early Warning System")
fitur_filter = st.sidebar.checkbox("Tampilkan Hanya Siswa Berisiko", value=False)

# Memproses Filter EWS berdasarkan pilihan pengguna
if fitur_filter:
    df_tampilan = df_siswa[df_siswa["Status Risiko"] == "Butuh Perhatian"]
else:
    df_tampilan = df_siswa

# Ringkasan Statistik Atas (Metrik Dashboard)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Seluruh Siswa", len(df_siswa))
with col2:
    jumlah_berisiko = len(df_siswa[df_siswa["Status Risiko"] == "Butuh Perhatian"])
    st.metric("Siswa Terdeteksi Berisiko (EWS)", jumlah_berisiko, delta=f"{jumlah_berisiko} Butuh Intervensi", delta_color="inverse")
with col3:
    st.metric("Rata-rata Kehadiran Kelas", f"{round(df_siswa['Kehadiran (%)'].mean(), 1)}%")

# Menampilkan Data Editor Interaktif (Guru bisa edit langsung di dashboard)
st.markdown("### 📊 Dataset Manajemen Siswa (Interaktif)")
st.caption("Gunakan st.data_editor agar pengguna atau guru dapat mengubah/memperbarui data nilai secara langsung.")
edited_df = st.data_editor(df_tampilan, use_container_width=True, hide_index=True)

# ==============================================================================
# VISUALISASI PERFORMA & ANALISIS DATA
# ==============================================================================
st.markdown("### 📈 Grafik Deteksi Dini (Korelasi Nilai vs Kehadiran)")
fig = px.scatter(
    edited_df, 
    x="Rata-rata Tugas", 
    y="Kehadiran (%)", 
    color="Status Risiko",
    hover_data=["Nama Siswa"],
    color_discrete_map={"Aman": "#28a745", "Butuh Perhatian": "#dc3545"},
    title="Peta Risiko Siswa (Koran Merah = Butuh Intervensi Segera)"
)
fig.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="Batas Minimum Kehadiran (80%)")
fig.add_vline(x=65, line_dash="dash", line_color="orange", annotation_text="Batas KKM Tugas (65)")
st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PERSONALISASI AI ADVISOR AGENT (GENERATIVE INSIGHT)
# ==============================================================================
st.markdown("---")
st.markdown("### 🤖 AI Advisor Agent: Diagnosis & Rekomendasi Personalisasi")

# Dropdown dinamis berdasarkan baris data siswa yang sedang ditampilkan di dashboard
siswa_terpilih_nama = st.selectbox("Pilih nama siswa untuk didiagnosis oleh AI:", edited_df["Nama Siswa"].tolist())

if siswa_terpilih_nama:
    # Mengambil data spesifik baris siswa terpilih
    data_terpilih = edited_df[edited_df["Nama Siswa"] == siswa_terpilih_nama].iloc[0]
    
    # Tampilan kartu informasi singkat siswa yang dipilih
    c1, c2, c3, c4 = st.columns(4)
    c1.text(f"ID: {data_terpilih['ID Siswa']}")
    c2.text(f"Rata-rata Tugas: {data_terpilih['Rata-rata Tugas']}")
    c3.text(f"Kehadiran: {data_terpilih['Kehadiran (%)']}%")
    c4.text(f"Status Risiko: {data_terpilih['Status Risiko']}")
    
    # Tombol aksi untuk memicu panggilan API AI Agent
    if st.button(f"Generate Analisis AI untuk {siswa_terpilih_nama}"):
        if llm is not None:
            with st.spinner(f"EduGuard-AI sedang merumuskan rekomendasi belajar menggunakan {selected_model_name}..."):
                # Menyusun prompt dinamis berdasarkan real-data siswa untuk dikirim ke API
                prompt = f"""
                Anda adalah seorang AI Advisor Agent Pendidikan profesional di platform EduGuard-AI.
                Tugas Anda adalah melakukan diagnosis dini dan memberikan rekomendasi personalisasi belajar (personalized learning) 
                berdasarkan data akademik siswa berikut ini:
                
                - Nama Siswa: {data_terpilih['Nama Siswa']}
                - Rata-rata Nilai Tugas: {data_terpilih['Rata-rata Tugas']} (Batas KKM: 65)
                - Tingkat Kehadiran: {data_terpilih['Kehadiran (%)']}% (Batas Minimal: 80%)
                - Skor Keaktifan di Kelas: {data_terpilih['Skor Keaktifan']}/100
                - Status Deteksi Sistem: {data_terpilih['Status Risiko']}
                
                Berikan laporan analitis terstruktur berformat Markdown yang mencakup:
                1. Analisis singkat akar masalah (mengapa siswa tersebut aman atau berisiko).
                2. Strategi intervensi / rekomendasi metode pembelajaran yang personal dan adaptif (Personalized Learning) yang cocok dengan kondisinya saat ini agar nilainya optimal atau terus bertahan.
                
                Gunakan gaya bahasa formal, taktis, namun memotivasi untuk dibaca oleh Wali Kelas atau Guru Bimbingan Konseling.
                """
                
                try:
                    # Memanggil LLM OpenRouter
                    response = llm.invoke(prompt)
                    
                    # Menampilkan hasil narasi AI di dalam kontainer berformat rapi agar spasi tidak berantakan 
                    st.markdown(f"#### 📄 Hasil Diagnosis AI ({selected_model_name}):")
                    st.markdown(f'<div class="advisor-box">{response.content}</div>', unsafe_allowed_html=True)
                except Exception as error_call:
                    st.error(f"Gagal terhubung dengan OpenRouter API: {error_call}")
        else:
            st.warning("Fitur AI tidak aktif karena API Key tidak valid. Periksa konfigurasi secrets Anda.")