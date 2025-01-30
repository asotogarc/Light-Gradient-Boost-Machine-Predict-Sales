import streamlit as st
import plotly.express as px
import requests
import json

# Inicializar sesión
def init_session():
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'dark'
    if 'weather_history' not in st.session_state:
        st.session_state['weather_history'] = []

def toggle_theme():
    st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'

def convert_temperature(temp_celsius, unit):
    if unit == "Fahrenheit":
        return temp_celsius * 9/5 + 32
    elif unit == "Kelvin":
        return temp_celsius + 273.15
    return temp_celsius

# Aplicar estilos CSS
def apply_styles():
    st.markdown(
        f"""
        <style>
            body {{
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
            /* Añadir este bloque para esconder la cabecera */
            .css-1dp5vir {{
                display: none;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Inicializar sesión
init_session()
apply_styles()

# Añadir espacio para compensar la falta de cabecera
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Título con más espacio hacia abajo
st.markdown(f"""
    <h1 style='text-align: center; margin-bottom: 30px;'>VENTAS ROHLEK FORECASTING</h1>
""", unsafe_allow_html=True)

# Crear columnas para las dos cajas de texto
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
            <p style="text-align-last: justify;">
                Esta aplicación muestra datos de las ventas de la compañía de Rohlek Forecasting subidos en el reto de Kaggle que se encuentra en el siguiente <a href="https://www.kaggle.com/c/rohlik-orders-forecasting-challenge" target="_blank">enlace</a>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
            <p style="text-align-last: justify;">
                También se comparten datos del entrenamiento de un modelo predictivo de ventas de LightGBM; el notebook con la información se encuentra en este otro <a href="https://www.kaggle.com/code/angelsotogarca/rohlik-sales-forecasting/edit" target="_blank">enlace</a>.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Botón para cambiar tema
st.button("Cambiar Tema", on_click=toggle_theme)

# Entrada de usuario
nombre = st.text_input("Ingresa tu nombre:")

# Selector de opción
opcion = st.selectbox("Elige una opción:", ["Datos Aleatorios", "Clima Actual", "Conversión de Moneda"])

# ... (el resto de tu código sigue igual)

if opcion == "Datos Aleatorios":
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="Gráfico Interactivo de Iris")
    st.plotly_chart(fig)

elif opcion == "Clima Actual":
    ciudad = st.text_input("Ingresa una ciudad para ver el clima:")
    unidad = st.selectbox("Elige la unidad de temperatura:", ["Celsius", "Fahrenheit", "Kelvin"])
    if st.button("Consultar Clima"):
        if ciudad:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid=TU_API_KEY&units=metric"
            response = requests.get(api_url).json()
            if response.get("main"):
                temp_c = response["main"]["temp"]
                temp_converted = convert_temperature(temp_c, unidad)
                st.success(f"La temperatura en {ciudad} es {temp_converted:.2f}° {unidad}")
                
                st.session_state['weather_history'].append(f"{ciudad}: {temp_converted:.2f}° {unidad}")
                
                fig = px.bar(x=[ciudad], y=[temp_converted], labels={'x': 'Ciudad', 'y': f'Temperatura ({unidad})'}, title="Temperatura Actual")
                st.plotly_chart(fig)
            else:
                st.error("Ciudad no encontrada")
        else:
            st.warning("Por favor, ingresa una ciudad")
    
    # Mostrar historial de búsquedas
    if st.session_state['weather_history']:
        st.subheader("Historial de Consultas")
        st.write(st.session_state['weather_history'])

elif opcion == "Conversión de Moneda":
    base_currency = st.selectbox("Moneda base:", ["USD", "EUR", "GBP", "JPY"])
    target_currency = st.selectbox("Moneda objetivo:", ["USD", "EUR", "GBP", "JPY"])
    amount = st.number_input("Cantidad a convertir:", min_value=1.0, step=1.0)
    if st.button("Convertir"):
        api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(api_url).json()
        if target_currency in response["rates"]:
            converted_amount = amount * response["rates"][target_currency]
            st.success(f"{amount} {base_currency} equivale a {converted_amount:.2f} {target_currency}")
        else:
            st.error("Error en la conversión")

# Mensaje final
if st.button("Enviar"):
    if nombre:
        st.success(f"Hola, {nombre}. Has elegido {opcion}.")
    else:
        st.warning("Por favor, ingresa tu nombre antes de continuar.")
