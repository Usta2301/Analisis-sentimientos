# app.py

import streamlit as st
from textblob import TextBlob
import re
from googletrans import Translator

# ──────────────────────────────
# 🖥️ Configuración de la página
# ──────────────────────────────

st.set_page_config(
    page_title="Análisis de Texto",
    layout="wide",
    page_icon="📊"
)
st.title("📊 Analizador de Texto Simple")

# ──────────────────────────────
# 🧠 Funciones auxiliares
# ──────────────────────────────

translator = Translator()

def traducir_texto(texto: str, src='es', dest='en') -> str:
    """Traduce texto entre idiomas usando Googletrans."""
    try:
        return translator.translate(texto, src=src, dest=dest).text
    except:
        return texto  # fallback sin traducción

def contar_palabras(texto: str) -> dict:
    """Cuenta palabras más frecuentes excluyendo las más comunes."""
    stop_words = {
        "the","and","you","are","que","por","para","con","una","los","las","del",
        "this","that","from","your","about","en","el","de"
    }
    tokens = re.findall(r'\b\w+\b', texto.lower())
    filtrados = [t for t in tokens if t not in stop_words and len(t) > 2]
    freq = {}
    for w in filtrados:
        freq[w] = freq.get(w, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

def detectar_entidades_basico(texto: str) -> list:
    """Detecta palabras que empiezan por mayúscula en medio de la frase."""
    entidades = []
    oraciones = re.split(r'[.!?]\s*', texto)
    for ora in oraciones:
        partes = ora.strip().split()
        for palabra in partes[1:]:
            if re.match(r'^[A-ZÁÉÍÓÚÑ][a-zñáéíóú]+$', palabra):
                entidades.append(palabra)
    return list(dict.fromkeys(entidades))

def procesar_texto(texto: str) -> dict:
    """Traduce, analiza sentimiento y cuenta palabras."""
    # 1) Traducción
    texto_en = traducir_texto(texto)
    blob = TextBlob(texto_en)
    # 2) Sentimiento y subjetividad
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    # 3) Frecuencia de palabras
    freq = contar_palabras(texto_en)
    # 4) Entidades (básico)
    entidades = detectar_entidades_basico(texto)
    # 5) Emoji según sentimiento
    if sentimiento > 0.05:
        estado_emoji = "😊 Positivo"
    elif sentimiento < -0.05:
        estado_emoji = "😟 Negativo"
    else:
        estado_emoji = "😐 Neutral"
    return {
        "texto_traducido": texto_en,
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frecuencias": freq,
        "entidades": entidades,
        "estado_emoji": estado_emoji
    }

# ──────────────────────────────
# 🖥️ Interfaz
# ──────────────────────────────

texto = st.text_area(
    "✍️ Ingresa tu texto en español para analizar:",
    height=200
)

if st.button("🔎 Analizar texto") and texto.strip():
    resultados = procesar_texto(texto)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Sentimiento y Subjetividad")
        # Mostrar emoji de estado
        st.markdown(f"**Estado general del texto:** {resultados['estado_emoji']}")
        st.metric("Sentimiento (−1 a 1)", f"{resultados['sentimiento']:.2f}")
        st.progress((resultados["sentimiento"] + 1) / 2)
        st.metric("Subjetividad (0 a 1)", f"{resultados['subjetividad']:.2f}")
        st.progress(resultados["subjetividad"])

        st.subheader("📌 Entidades Detectadas")
        if resultados["entidades"]:
            for ent in resultados["entidades"]:
                st.write(f"- {ent}")
        else:
            st.write("No se detectaron entidades.")

    with col2:
        st.subheader("📊 Palabras Más Frecuentes")
        if resultados["frecuencias"]:
            st.bar_chart(resultados["frecuencias"])
        else:
            st.write("No hay suficientes palabras significativas.")

        st.subheader("🌐 Traducción al Inglés")
        st.text_area("Texto traducido", resultados["texto_traducido"], height=200)
