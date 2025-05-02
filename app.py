# app.py

import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# ──────────────────────────────
# 🖥️ Configuración de la página
# ──────────────────────────────
st.set_page_config(
    page_title="Análisis de Sentimiento Emoji",
    layout="centered",
    page_icon="😊"
)
st.title("😊😐😟 Sentiment Emoji Analyzer")

# ──────────────────────────────
# 🧠 Función de análisis de sentimiento
# ──────────────────────────────
def analizar_sentimiento(texto: str) -> float:
    blob = TextBlob(texto)
    return blob.sentiment.polarity

# ──────────────────────────────
# 🎨 Mapas de emoji animados
# ──────────────────────────────
EMOJI_GIFS = {
    "positive": "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif",  # risa feliz
    "neutral":  "https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif",  # emoji pensativo
    "negative": "https://media.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif"   # carita triste
}

# ──────────────────────────────
# 🖥️ Interfaz
# ──────────────────────────────
st.write("Escribe una frase y presiona el botón para ver cómo se siente (¡en emojis animados!)")

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
