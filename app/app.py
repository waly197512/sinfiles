import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# Configurar la página para utilizar un layout más amplio
st.set_page_config(page_title="TU COMPAÑIA PERFECTA", layout="wide")







# 1. DEFINICIÓN DEL DATASET (Tipos de mascotas + lemas + imágenes)
data = {
    'mascota': ['Perro', 'Perro', 'Gato', 'Gato', 'Ave', 'Ave', 'Roedor', 'Roedor', 'Otro', 'Otro'],
    'imagen': ['media/feliz.png', 'media/activo.png', 
               'media/elegante.png', 'media/juguetona.png',
               'media/pajaro.png', 'media/song_bird_21844.png',
               'media/hamster.png', 'media/hamster (1).png',
               'media/pufferfish_puffer_fish_blowfish_aquarium_icon_209474 (1).png', 'media/22285snake_98774.png'],
    'tipo': ['친절한 (Amigable)', '활동적인 (Activo)', '우아한 (Elegante)', '독립적인 (Independiente)', 
             '쾌활한 (Alegre)', '노래하는 (Cantor)', '귀여운 (Adorable)', '호기심 많은 (Curioso)', 
             '이국적인 (Exótico)', '조용한 (Tranquilo)'],
    'horario': ['Diurno', 'Nocturno', 'Diurno', 'Nocturno', 'Diurno', 'Diurno', 'Nocturno', 'Nocturno', 'Diurno', 'Diurno'],
    'actividad': ['Alta', 'Muy Alta', 'Baja', 'Media', 'Alta', 'Media', 'Baja', 'Media', 'Baja', 'Baja'],
    'ambiente': ['Exterior', 'Exterior', 'Interior', 'Interior', 'Exterior', 'Interior', 'Interior', 'Interior', 'Exterior', 'Interior'],
    'ruido': ['Alto', 'Medio', 'Bajo', 'Bajo', 'Alto', 'Alto', 'Bajo', 'Medio', 'Bajo', 'Bajo'],
    'companero': ['Sí', 'Sí', 'No', 'Sí', 'Sí', 'No', 'Sí', 'No', 'No', 'No'],
    'lema': [
        "Siempre a tu lado,\ncon amor incondicional,\nladridos de sol.",
        "Energía pura,\ncorre sin mirar atrás,\nun salto al futuro.",
        "Garras en silencio,\nelegancia y mirada,\nbelleza que cuida.",
        "Libre y sereno,\nla noche es su refugio,\nsus ojos te miran.",
        "El viento le canta,\nvuelos de alegría viva,\nluz en cada ala.",
        "Notas que resuenan,\nun canto en la mañana,\nes tu despertar.",
        "Pequeño y leal,\nun corazón que palpita,\nmirada que ama.",
        "Curiosidad fiel,\nun viaje de aventuras,\nsilencio y amor.",
        "El mundo es su hogar,\nexótico y misterioso,\nsu calma te abraza.",
        "Quieto en la brisa,\nel silencio es su fuerza,\ncompañero fiel."
    ]
}
df = pd.DataFrame(data)

# 2. ENCABEZADO Y DESCRIPCIÓN
col1, col2 = st.columns([3, 1])
with col1:
    st.title("TU COMPAÑÍA PERFECTA '동반자'")
    st.write("Responde unas breves preguntas y descubre qué mascota es ideal para ti junto con un lema especial.")
with col2:
    st.image("media/sonreir.png", width=150)

# 3. FORMULARIO DE ENTRADA
st.sidebar.header("Responde el cuestionario:")
horario = st.sidebar.selectbox("¿Tu horario es principalmente?", ['Diurno', 'Nocturno'])
actividad = st.sidebar.selectbox("Tu nivel de actividad es:", ['Baja', 'Media', 'Alta', 'Muy Alta'])
ambiente = st.sidebar.selectbox("Prefieres ambientes:", ['Interior', 'Exterior'])
ruido = st.sidebar.selectbox("¿Toleras niveles de ruido?", ['Bajo', 'Medio', 'Alto'])
companero = st.sidebar.selectbox("¿Buscas un compañero cercano?", ['Sí', 'No'])

# 4. PROCESAR RESPUESTAS Y CALCULAR SIMILITUD
if st.sidebar.button("Descubrir mi mascota ideal"):
    # Codificar las respuestas del usuario
    usuario_respuestas = {
        'horario': horario,
        'actividad': actividad,
        'ambiente': ambiente,
        'ruido': ruido,
        'companero': companero
    }
    encoder = OneHotEncoder(sparse_output=False)
    df_encoded = pd.DataFrame(encoder.fit_transform(df[['horario', 'actividad', 'ambiente', 'ruido', 'companero']]))
    usuario_encoded = encoder.transform([[usuario_respuestas['horario'], 
                                          usuario_respuestas['actividad'], 
                                          usuario_respuestas['ambiente'], 
                                          usuario_respuestas['ruido'], 
                                          usuario_respuestas['companero']]])

    # Calcular similitud
    similaridades = np.dot(df_encoded, usuario_encoded.T)
    df['Similitud'] = similaridades
    mascota_recomendada = df.sort_values(by='Similitud', ascending=False).iloc[0]

    # 5. MOSTRAR RESULTADO
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🐾 Tu mascota ideal es:")
        st.markdown(f"### **{mascota_recomendada['mascota']}** ({mascota_recomendada['tipo']})")
        st.write("✨ Lema especial:")
        st.markdown(f"_{mascota_recomendada['lema']}_")
    with col2:
        st.image(mascota_recomendada['imagen'], width=200)