import streamlit as st
from langchain_openai import ChatOpenAI
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="EduGuard-AI", layout="wide")

# 2. Inisialisasi AI (Menggunakan API Key dari Streamlit Secrets)
# Pastikan di secrets.toml kamu kuncinya: OPENROUTER_API_KEY = "sk-or-v1-..."
api_key = st.secrets["OPENROUTER_API_KEY"]

llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="meta-llama/llama-3-8b-instruct"
)

# 3. Data Simulasi (100 Siswa)
data = {
    "Nama": [f"Siswa {i+1}" for i in range(100)],
    "Nilai": [60 + (i % 40) for i in range(100)],
    "Absen": [10 - (i % 10) for i in range(100)]
}
df = pd.DataFrame(data)

# 4. Antarmuka Dashboard
st.title("🛡️ EduGuard-AI: Early Warning System")

# Fitur Early Warning: Filter Siswa Berisiko
st.sidebar.header("Filter Siswa")
tampilkan_berisiko = st.sidebar.checkbox("Tampilkan Hanya Siswa Berisiko (Nilai < 70)")

df_display = df
if tampilkan_berisiko:
    df_display = df[df["Nilai"] < 70]

# Tampilkan Data
st.subheader("Data Siswa")
edited_df = st.data_editor(df_display)

# 5. Advisor Agent (Diagnosis AI)
st.subheader("🤖 Advisor Agent")
target_siswa = st.selectbox("Pilih siswa untuk dianalisis:", edited_df["Nama"].tolist())

if st.button("Analisis Siswa"):
    siswa_data = edited_df[edited_df["Nama"] == target_siswa].iloc[0]
    prompt = f"Analisis performa siswa bernama {target_siswa} dengan Nilai {siswa_data['Nilai']} dan Absen {siswa_data['Absen']}. Berikan rekomendasi singkat."
    
    with st.spinner("Sedang mendiagnosis..."):
        response = llm.invoke(prompt)
        st.write(response.content)

# 6. Visualisasi Sederhana
st.subheader("Visualisasi Performa")
fig = px.bar(edited_df, x="Nama", y="Nilai", color="Nilai", title="Distribusi Nilai Siswa")
st.plotly_chart(fig)