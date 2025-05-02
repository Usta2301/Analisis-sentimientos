import streamlit as st
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(page_title="Analizador de Texto", page_icon="📊", layout="centered")

# Título y descripción
st.title("📝 Analizador de Texto Simple")
st.markdown("""
Esta aplicación utiliza TextBlob para realizar un análisis básico de texto:
- Análisis de sentimiento
- Análisis de frecuencia de palabras
- Detección de entidades nombradas
""")

# Función para contar palabras sin depender de NLTK
def contar_palabras(texto):
    stop_words = set([
        # Lista de palabras vacías en español e inglés (reduce a lo esencial)
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words and len(palabra) > 2]
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))

# Inicializar el traductor
translator = Translator()

# Función para traducir texto
def traducir_texto(texto, src='es', dest='en'):
    try:
        return translator.translate(texto, src=src, dest=dest).text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

# Función para analizar entidades nombradas y sentimiento
def procesar_texto(texto):
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    
    # Sentimiento y subjetividad
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    # Contar palabras
    contador_palabras = contar_palabras(texto_ingles)
    
    # Detección de entidades nombradas
    entidades = blob.noun_phrases
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "contador_palabras": contador_palabras,
        "entidades": entidades,
        "texto_traducido": texto_ingles
    }

# Función para mostrar visualizaciones
def mostrar_resultados(resultados):
    st.subheader("Análisis de Sentimiento")
    st.progress((resultados["sentimiento"] + 1) / 2)
    if resultados["sentimiento"] > 0.05:
        st.success(f"Positivo ({resultados['sentimiento']:.2f})")
    elif resultados["sentimiento"] < -0.05:
        st.error(f"Negativo ({resultados['sentimiento']:.2f})")
    else:
        st.info(f"Neutral ({resultados['sentimiento']:.2f})")
    
    st.subheader("Subjetividad")
    st.progress(resultados["subjetividad"])
    if resultados["subjetividad"] > 0.5:
        st.warning(f"Alta subjetividad ({resultados['subjetividad']:.2f})")
    else:
        st.info(f"Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    # Palabras más frecuentes
    st.subheader("Palabras más frecuentes")
    if resultados["contador_palabras"]:
        st.bar_chart(resultados["contador_palabras"])

    # Entidades nombradas
    st.subheader("Entidades Nombradas Detectadas")
    if resultados["entidades"]:
        for entidad in resultados["entidades"][:10]:
            st.write(f"- {entidad}")
    
    # Mostrar texto traducido
    st.subheader("Texto Traducido")
    st.text(resultados["texto_traducido"])

# Lógica principal
texto = st.text_area("Ingresa tu texto para analizar", height=200)
if st.button("Analizar texto") and texto.strip():
    with st.spinner("Analizando texto..."):
        resultados = procesar_texto(texto)
        mostrar_resultados(resultados)
