"""
===========================================================================
Aplikasi: EduGuard-AI - Early Warning System (RAKERNAS IndoCEISS 2026)
Pengembang: Mahasiswa Palcomtech
Deskripsi: Sistem diagnostik performa siswa berbasis Longitudinal Behavioral 
           Analytics dan ZPD (Zone of Proximal Development).
===========================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_openai import ChatOpenAI

# --------------------------------------------------------------------------
# INSTRUKSI PENGGUNAAN (Untuk Juri/Dosen)
# Aplikasi ini menggunakan OpenRouter sebagai gateway AI.
# OPENROUTER_API_KEY 
# --------------------------------------------------------------------------

st.set_page_config(page_title="EduGuard-AI: Scientific Dashboard", layout="wide")

# Validasi API Key
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    st.error("⚠️ API Key tidak ditemukan. Pastikan 'OPENROUTER_API_KEY' sudah terkonfigurasi di Streamlit Secrets.")
    st.stop()

# Inisialisasi Model melalui OpenRouter
llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="meta-llama/llama-3-8b-instruct"
)

# 1. LOGIKA ILMIAH: Klasifikasi Performa (Berdasarkan Riset Li & Chen, 2025)
def classify_student_status(normalized_gain, cognitive_load):
    """
    Mengimplementasikan logika threshold untuk deteksi dini (Early Warning System).
    - Threshold 0.51: Optimal untuk strategi Hybrid Context-Aware.
    - Threshold 0.35: Batas performa stagnan.
    """
    if normalized_gain >= 0.51:
        return "Optimal ZPD", "Berikan tantangan lebih tinggi (Adaptive Scaffolding)"
    elif 0.35 <= normalized_gain < 0.51:
        return "Batas Bawah ZPD", "Aktifkan Automated Feedback & Hinting"
    elif normalized_gain < 0.35 and cognitive_load > 0.7:
        return "Cognitive Overload", "Intervensi: Chunking Materi & Personalized Path"
    else:
        return "Low Engagement", "Intervensi: Notifikasi Guru (Human-in-the-Loop)"

# 2. ANTARMUKA DASHBOARD
st.title("🛡️ EduGuard-AI: Early Warning System")
st.markdown("Sistem pemantauan longitudinal untuk efektivitas belajar siswa.")

# Input parameter untuk simulasi diagnosis
col1, col2 = st.columns(2)
with col1:
    gain = st.slider("Normalized Gain (0.0 - 1.0)", 0.0, 1.0, 0.4)
with col2:
    load = st.slider("Cognitive Load (0.0 - 1.0)", 0.0, 1.0, 0.6)

# Hasil Diagnosa Ilmiah
status, rekomendasi = classify_student_status(gain, load)
st.metric("Profil Kognitif", status)
st.info(f"Rekomendasi Strategi: {rekomendasi}")

# 3. ADVISOR AGENT (Intervensi AI)
st.subheader("🤖 AI Advisor (Scientific Diagnostic)")
if st.button("Generate Laporan Diagnostik"):
    prompt = (f"Anda adalah sistem AI diagnostik pendidikan. Analisis siswa dengan "
              f"Normalized Gain {gain} dan Cognitive Load {load}. "
              f"Status klasifikasi: {status}. "
              f"Berdasarkan standar Longitudinal Behavioral Analytics, berikan "
              f"strategi intervensi yang tepat secara ilmiah.")
    
    with st.spinner("Menganalisis data longitudinal..."):
        response = llm.invoke(prompt)
        st.write(response.content)

# 4. KREDIT PENGEMBANG
st.markdown("---")
st.caption("Dikembangkan oleh [Tim Mahasasiswa Palcomtech] | RAKERNAS IndoCEISS 2026")