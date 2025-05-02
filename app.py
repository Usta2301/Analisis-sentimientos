# app.py

import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# ──────────────────────────────
# 🖥️ Configuración de la página
# ──────────────────────────────
st.set_page_config(
    page_title="Analizador Emoji de Sentimiento",
    layout="centered",
    page_icon="😊"
)
st.title("😊😐😟 Sentiment Emoji Analyzer")

# ──────────────────────────────
# 🌐 Inicializa traductor
# ──────────────────────────────
translator = Translator()

# ──────────────────────────────
# 🧠 Función de análisis de sentimiento con traducción
# ──────────────────────────────
def analizar_sentimiento(texto: str) -> float:
    try:
        # Traduce al inglés para mejorar el análisis
        texto_en = translator.translate(texto, src='es', dest='en').text
    except:
        texto_en = texto  # si falla la traducción, usa original
    blob = TextBlob(texto_en)
    return blob.sentiment.polarity

# ──────────────────────────────
# 🎨 Mapa de emojis animados
# ──────────────────────────────
EMOJI_GIFS = {
    "positive": "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif",
    "neutral":  "https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif",
    "negative": "https://media.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif"
}

# ──────────────────────────────
# 🖥️ Interfaz
# ──────────────────────────────
st.write("Escribe una frase en español y presiona el botón para ver cómo se siente (¡con emoji animado!)")

frase = st.text_input("✍️ Tu frase aquí:")

if st.button("🔍 Analizar sentimiento") and frase.strip():
    polaridad = analizar_sentimiento(frase)
    
    if polaridad >  0.05:
        estado = "positive"
        desc  = "Positivo"
    elif polaridad < -0.05:
        estado = "negative"
        desc  = "Negativo"
    else:
        estado = "neutral"
        desc  = "Neutral"
    
    st.markdown(f"### Estado: **{desc}** ({polaridad:.2f})")
    st.image(EMOJI_GIFS[estado], width=300)
