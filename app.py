import streamlit as st
import openai

# 1. Pastikan Secrets sudah mengarah ke OPENROUTER_API_KEY nanti
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# 2. Setup client OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# 3. Fungsi analisis data siswa pakai Nvidia Nemotron 3 Ultra (Gratis)
def analisa_kesulitan_belajar(data_progres_siswa):
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra:free",  # Pakai model gratis spek dewa
        messages=[
            {
                "role": "system",
                "content": "Anda adalah AI pakar psikologi pendidikan. Analisis data siswa berikut untuk menentukan Zone of Proximal Development (ZPD) dan tingkat beban kognitif mereka."
            },
            {
                "role": "user",
                "content": f"Berikut data aktivitas belajar siswa: {data_progres_siswa}"
            }
        ]
    )
    return response.choices[0].message.content