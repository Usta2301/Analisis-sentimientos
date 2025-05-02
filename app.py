# app.py

import streamlit as st
from textblob import TextBlob
import nltk
import re
from googletrans import Translator

# ──────────────────────────────
# ✅ Descarga automática de corpus si faltan
# ──────────────────────────────
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

# ──────────────────────────────
# 🧠 Funciones auxiliares
# ──────────────────────────────

translator = Translator()

def traducir_texto(texto, src='es', dest='en'):
    """Traduce texto de español a inglés (o entre otros idiomas)."""
    try:
        return translator.translate(texto, src=src, dest=dest).text
    except:
        return texto  # fallback sin traducción

def contar_palabras(texto):
    """Cuenta palabras más frecuentes excluyendo 'stop words'."""
    stop_words = set([
        "the", "and", "you", "are", "que", "por", "para", "con", "una", "los", "las", "del",
        "this", "that", "from", "your", "about", "etc", "etc.", "en", "el", "de"
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))

def procesar_texto(texto):
    """Traduce, analiza sentimiento, entidades y palabras clave."""
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    contador = contar_palabras(texto_ingles)
    entidades = blob.noun_phrases
    return {
        "texto_traducido": texto_ingles,
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "contador": contador,
        "entidades": entidades
    }

# ──────────────────────────────
# 🖥️ Interfaz con Streamlit
# ──────────────────────────────

st.set_page_config(page_title="Análisis de Texto", layout="wide")
st.title("📊 Análisis de Texto con IA")

texto = st.text_area("✍️ Ingresa tu texto en español para analizar:", height=200)

if st.button("🔎 Analizar texto") and texto.strip():
    resultados = procesar_texto(texto)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Análisis de Sentimiento")
        st.metric("Sentimiento (de -1 a 1)", f"{resultados['sentimiento']:.2f}")
        st.progress((resultados['sentimiento'] + 1) / 2)

        st.metric("Subjetividad (de 0 a 1)", f"{resultados['subjetividad']:.2f}")
        st.progress(resultados['subjetividad'])

        st.subheader("📌 Entidades Nombradas (Noun Phrases)")
        if resultados['entidades']:
            for ent in resultados['entidades'][:10]:
                st.write(f"- {ent}")
        else:
            st.write("No se encontraron entidades.")

    with col2:
        st.subheader("📊 Palabras Más Frecuentes")
        if resultados['contador']:
            st.bar_chart(resultados['contador'])
        else:
            st.write("No hay suficientes palabras significativas.")

        st.subheader("🌐 Traducción del Texto")
        st.text_area("Texto traducido al inglés", resultados["texto_traducido"], height=200)
