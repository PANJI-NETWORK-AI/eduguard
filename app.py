"""
===========================================================================
Aplikasi: Sistem Deteksi Dini Kesulitan Belajar
Pengembang: Mahasiswa Palcomtech
Deskripsi: Sistem diagnostik performa siswa berbasis Longitudinal Behavioral 
           Analytics dan ZPD (Zone of Proximal Development).
===========================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from langchain_openai import ChatOpenAI

# --------------------------------------------------------------------------
# INSTRUKSI PENGGUNAAN (Untuk Juri/Dosen)
# Aplikasi ini menggunakan OpenRouter sebagai gateway AI.
# Pastikan di secrets.toml kamu kuncinya: 
# OPENROUTER_API_KEY = "Masukkan API Asli"
# --------------------------------------------------------------------------

st.set_page_config(page_title="EduGuard-AI: Scientific Dashboard", layout="wide")

# Validasi API Key
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    st.error("⚠️ API Key tidak ditemukan. Pastikan 'OPENROUTER_API_KEY' sudah terkonfigurasi di Streamlit Secrets.")
    st.stop()

# Inisialisasi Model
llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="meta-llama/llama-3-8b-instruct"
)

# 1. GENERASI DATA DUMMY (100 Siswa untuk Skalabilitas)
@st.cache_data
def generate_student_data():
    np.random.seed(42)
    return pd.DataFrame({
        "Nama": [f"Siswa {i+1}" for i in range(100)],
        "Normalized_Gain": np.random.uniform(0.1, 0.9, 100),
        "Cognitive_Load": np.random.uniform(0.1, 0.9, 100)
    })

df = generate_student_data()

# 2. LOGIKA ILMIAH (Berdasarkan Li & Chen, 2025)
def classify_student_status(normalized_gain, cognitive_load):
    if normalized_gain >= 0.51:
        return "Optimal ZPD", "Berikan tantangan lebih tinggi (Adaptive Scaffolding)"
    elif 0.35 <= normalized_gain < 0.51:
        return "Batas Bawah ZPD", "Aktifkan Automated Feedback & Hinting"
    elif normalized_gain < 0.35 and cognitive_load > 0.7:
        return "Cognitive Overload", "Intervensi: Chunking Materi & Personalized Path"
    else:
        return "Low Engagement", "Intervensi: Notifikasi Guru (Human-in-the-Loop)"

# 3. ANTARMUKA DASHBOARD
st.title("🛡️ EduGuard-AI: Sistem Deteksi Dini Kesulitan Belajar")
st.markdown("Sistem pemantauan longitudinal untuk efektivitas belajar siswa.")

# Tampilan Tabel Data
st.subheader("📋 Data Performa Siswa (100 Siswa)")
edited_df = st.data_editor(df, use_container_width=True)

# 4. ADVISOR AGENT (Intervensi AI Berbasis Diagnosis)
st.subheader("🤖 AI Advisor (Scientific Diagnostic)")
target_siswa = st.selectbox("Pilih siswa untuk dianalisis:", edited_df["Nama"].tolist())

if st.button("Generate Laporan Diagnostik"):
    siswa_row = edited_df[edited_df["Nama"] == target_siswa].iloc[0]
    status, rekomendasi = classify_student_status(siswa_row["Normalized_Gain"], siswa_row["Cognitive_Load"])
    
    prompt = (f"Analisis siswa {target_siswa}. Data: Gain {siswa_row['Normalized_Gain']:.2f}, "
              f"Load {siswa_row['Cognitive_Load']:.2f}. Status: {status}. "
              f"Berikan rekomendasi intervensi taktis berdasarkan pendekatan pendidikan modern.")
    
    with st.spinner("Menganalisis data longitudinal siswa..."):
        response = llm.invoke(prompt)
        st.info(f"**Profil:** {status} | **Saran:** {rekomendasi}")
        st.write(response.content)

# 5. Visualisasi
st.subheader("📊 Visualisasi Performa Siswa")
fig = px.scatter(edited_df, x="Normalized_Gain", y="Cognitive_Load", color="Normalized_Gain", 
                 hover_data=["Nama"], title="Distribusi Kognitif 100 Siswa")
st.plotly_chart(fig, use_container_width=True)

# 6. KREDIT PENGEMBANG
st.markdown("---")
st.caption("Dikembangkan oleh [Mahasiswa Palcomtech]")