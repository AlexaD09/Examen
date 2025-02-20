import json
import pandas as pd
import random 
import streamlit as st
from config import GROQ_API_KEY
from groq import Groq


# Inicializar cliente de Groq
qclient = Groq(api_key=GROQ_API_KEY)

st.title("Predicción Electoral")
st.subheader("Evaluación Final - Desarrollo de Sistemas de Información")

# Subir archivo Excel
uploaded_file = st.file_uploader("Sube un archivo XLSX con los datos de votos", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Vista previa de los datos:")
    st.dataframe(df.head())

    # Muestra de datos aleatoria o total
    sample_size = st.slider("Selecciona el tamaño de la muestra", 1, len(df), 5)
    sample_data = df.sample(sample_size) if sample_size < len(df) else df
    st.write("Muestra de datos:")
    st.dataframe(sample_data)

    # Etiquetado de votos
    def etiquetar_voto(texto):
        if "noboa" in texto.lower():
            return "Voto Noboa"
        elif "luisa" in texto.lower():
            return "Voto Luisa"
        else:
            return "Voto Nulo"

    df["Etiqueta Voto"] = df["keywords"].astype(str).apply(etiquetar_voto)
    st.write("Datos con etiquetas de voto:")
    st.dataframe(df[["keywords", "Etiqueta Voto"]])

    # Contar votos
    conteo_votos = df["Etiqueta Voto"].value_counts()
    st.write("Conteo de votos:")
    st.bar_chart(conteo_votos)

    # Identificar quién recibió más votos
    ganador = conteo_votos.idxmax()
    st.success(f"El candidato con más votos es: {ganador}")

    # Contar votos nulos y conclusión
    votos_nulos = conteo_votos.get("Voto Nulo", 0)
    st.write(f"Total de votos nulos: {votos_nulos}")
    conclusion = "Se requiere revisión" if votos_nulos > (len(df) * 0.1) else "No hay problemas significativos"
    st.write(f"Conclusión: {conclusion}")

    # Consultar a Groq sobre la data
    pregunta = st.text_input("Hazle una pregunta al bot sobre los datos")
    if st.button("Preguntar") and pregunta:
        response = qclient.chat.completions.create(
            messages=[{"role": "user", "content": pregunta}],
            model="llama-3.3-70b-versatile",
        )
        respuesta_bot = response.choices[0].message.content
        st.write("Respuesta del bot:", respuesta_bot)

    # Subir a Git (mensaje informativo)
    st.info("Recuerda subir el código al repositorio de Git para obtener el punto fina