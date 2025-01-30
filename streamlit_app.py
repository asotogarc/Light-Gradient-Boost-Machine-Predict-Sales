import streamlit as st
import plotly.express as px
import requests

# Inicializar sesión
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

# Cambiar tema dinámicamente
def toggle_theme():
    st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'

# Aplicar estilos CSS
st.markdown(
    f"""
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: {'#121212' if st.session_state['theme'] == 'dark' else '#FFFFFF'};
            color: {'#FFFFFF' if st.session_state['theme'] == 'dark' else '#000000'};
        }}
        .stButton > button {{
            background-color: #007AFF;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: #005ECF;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Título
theme_icon = "🌙" if st.session_state['theme'] == 'dark' else "☀️"
st.title(f"📱 Aplicación Estilo Apple {theme_icon}")

# Botón para cambiar tema
st.button("Cambiar Tema", on_click=toggle_theme)

# Entrada de usuario
nombre = st.text_input("Ingresa tu nombre:")

# Selector de opción
opcion = st.selectbox("Elige una opción:", ["Datos Aleatorios", "Clima Actual"])

# Gráficos interactivos con Plotly
if opcion == "Datos Aleatorios":
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="Gráfico Interactivo de Iris")
    st.plotly_chart(fig)

# Consulta API externa
elif opcion == "Clima Actual":
    ciudad = st.text_input("Ingresa una ciudad para ver el clima:")
    if st.button("Consultar Clima"):
        if ciudad:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid=TU_API_KEY&units=metric"
            response = requests.get(api_url).json()
            if response.get("main"):
                temp = response["main"]["temp"]
                st.success(f"La temperatura en {ciudad} es {temp}°C")
            else:
                st.error("Ciudad no encontrada")
        else:
            st.warning("Por favor, ingresa una ciudad")

# Mensaje final
if st.button("Enviar"):
    if nombre:
        st.success(f"Hola, {nombre}. Has elegido {opcion}.")
    else:
        st.warning("Por favor, ingresa tu nombre antes de continuar.")
