"""
Aplikasi EduGuard-AI: Longitudinal Performance Tracking System
Tujuan: Implementasi 'Longitudinal Behavioral Analytics' untuk deteksi dini 
        performa siswa berdasarkan standar ilmiah dan ZPD (Zone of Proximal Development).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_openai import ChatOpenAI

# --------------------------------------------------------------------------
# INSTRUKSI KONFIGURASI API KEY (Untuk Juri/Pengguna Repository)
# --------------------------------------------------------------------------

st.set_page_config(page_title="EduGuard-AI: Scientific Dashboard", layout="wide")

# Mengambil API Key dari Streamlit Secrets
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    st.error("⚠️ API Key tidak ditemukan. Pastikan 'OPENROUTER_API_KEY' sudah diisi.")
    st.stop()

# Inisialisasi Model AI
llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="meta-llama/llama-3-8b-instruct"
)

# 1. Logika Ilmiah: Klasifikasi Status Siswa (Berdasarkan Li & Chen, 2025)
def classify_student_status(normalized_gain, cognitive_load):
    """
    Mengklasifikasikan siswa berdasarkan metrik longitudinal:
    - 0.51: Batas kesuksesan Hybrid Context-Aware Strategy
    - 0.35: Batas stagnansi strategi rule-based
    """
    if normalized_gain >= 0.51:
        return "Optimal ZPD", "Berikan tantangan lebih tinggi (Adaptive Scaffolding)"
    elif 0.35 <= normalized_gain < 0.51:
        return "Batas Bawah ZPD", "Aktifkan Automated Feedback & Hinting"
    elif normalized_gain < 0.35 and cognitive_load > 0.7:
        return "Cognitive Overload", "Intervensi: Chunking Materi & Personalized Path"
    else:
        return "Low Engagement", "Intervensi: Notifikasi Guru (Human-in-the-Loop)"

# 2. Antarmuka Aplikasi
st.title("🛡️ EduGuard-AI: Longitudinal Performance Tracker")
st.markdown("Dashboard ini menggunakan **Longitudinal Behavioral Analytics** untuk mendeteksi profil kognitif siswa secara otomatis.")

# Simulasi Input Data
col1, col2 = st.columns(2)
with col1:
    gain = st.slider("Normalized Gain (0.0 - 1.0)", 0.0, 1.0, 0.4)
with col2:
    load = st.slider("Cognitive Load (0.0 - 1.0)", 0.0, 1.0, 0.6)

status, rekomendasi = classify_student_status(gain, load)

st.metric("Status Siswa", status)
st.info(f"Rekomendasi Intervensi: {rekomendasi}")

# 3. Advisor Agent (Proses AI)
st.subheader("🤖 AI Scientific Advisor")
if st.button("Generate Analisis Ilmiah"):
    prompt = (f"Anda adalah sistem AI diagnostik pendidikan. Analisis siswa dengan "
              f"Normalized Gain {gain} dan Cognitive Load {load}. Status saat ini: {status}. "
              f"Berikan rekomendasi tindakan taktis berbasis sains.")
    
    with st.spinner("Menganalisis pola perilaku digital..."):
        response = llm.invoke(prompt)
        st.write(response.content)

st.caption("Dikembangkan oleh kami - RAKERNAS IndoCEISS 2026")