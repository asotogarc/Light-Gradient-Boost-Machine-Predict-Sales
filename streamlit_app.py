import streamlit as st
import plotly.express as px
import requests

# Inicializar sesión
def init_session():
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'dark'
    if 'weather_history' not in st.session_state:
        st.session_state['weather_history'] = []

# Cambiar tema
def toggle_theme():
    st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'

# Convertir temperatura
def convert_temperature(temp_celsius, unit):
    if unit == "Fahrenheit":
        return temp_celsius * 9/5 + 32
    elif unit == "Kelvin":
        return temp_celsius + 273.15
    return temp_celsius

# Aplicar estilos CSS personalizados
def apply_styles():
    st.markdown(
        f"""
        <style>
            body {{
                background-color: {'#1e1e1e' if st.session_state['theme'] == 'dark' else '#f5f5f5'};
                color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'};
                font-family: 'Arial', sans-serif;
            }}
            .stButton > button {{
                background-color: #007AFF;
                color: white;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 16px;
                transition: all 0.3s ease;
                border: none;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .stButton > button:hover {{
                background-color: #005ECF;
                transform: translateY(-2px);
                box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.15);
            }}
            .stTextInput > div > div > input {{
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
            }}
            .stSelectbox > div > div {{
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
            }}
            .stMarkdown h1 {{
                font-size: 36px;
                font-weight: bold;
                color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'};
                text-align: center;
                margin-bottom: 30px;
            }}
            .stMarkdown h2 {{
                font-size: 24px;
                font-weight: bold;
                color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'};
                margin-bottom: 20px;
            }}
            .stMarkdown p {{
                font-size: 16px;
                line-height: 1.6;
                color: {'#ffffff' if st.session_state['theme'] == 'dark' else '#000000'};
            }}
            .stMarkdown a {{
                color: #007AFF;
                text-decoration: none;
            }}
            .stMarkdown a:hover {{
                text-decoration: underline;
            }}
            /* Ocultar la cabecera */
            .css-1dp5vir {{
                display: none;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Inicializar sesión y aplicar estilos
init_session()
apply_styles()

# Añadir espacio para compensar la falta de cabecera
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Título de la aplicación con un diseño más atractivo
st.markdown(f"""
    <h1 style='text-align: center; margin-bottom: 30px;'>
        🌟 VENTAS ROHLEK FORECASTING 🌟
    </h1>
""", unsafe_allow_html=True)

# Crear columnas para las dos cajas de texto
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
            <p style="text-align-last: justify;">
                📊 Esta aplicación muestra datos de las ventas de la compañía de Rohlek Forecasting subidos en el reto de Kaggle que se encuentra en el siguiente <a href="https://www.kaggle.com/c/rohlik-orders-forecasting-challenge" target="_blank">enlace</a>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
            <p style="text-align-last: justify;">
                🚀 También se comparten datos del entrenamiento de un modelo predictivo de ventas de LightGBM; el notebook con la información se encuentra en este otro <a href="https://www.kaggle.com/code/angelsotogarca/rohlik-sales-forecasting/edit" target="_blank">enlace</a>.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Botón para cambiar tema con un ícono
st.button("🌓 Cambiar Tema", on_click=toggle_theme)

# Entrada de usuario con un placeholder
nombre = st.text_input("👤 Ingresa tu nombre:", placeholder="Ej: Juan Pérez")

# Selector de opción con un ícono
opcion = st.selectbox("🔍 Elige una opción:", ["Datos Aleatorios", "Clima Actual"])

# Opción 1: Datos Aleatorios
if opcion == "Datos Aleatorios":
    st.markdown("### 📈 Gráfico Interactivo de Datos Aleatorios")
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="Gráfico de Iris")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white' if st.session_state['theme'] == 'dark' else 'black')
    )
    st.plotly_chart(fig, use_container_width=True)

# Opción 2: Clima Actual
elif opcion == "Clima Actual":
    st.markdown("### 🌤️ Consulta el Clima Actual")
    ciudad = st.text_input("🏙️ Ingresa una ciudad para ver el clima:", placeholder="Ej: Madrid")
    unidad = st.selectbox("🌡️ Elige la unidad de temperatura:", ["Celsius", "Fahrenheit", "Kelvin"])
    if st.button("🔍 Consultar Clima"):
        if ciudad:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid=TU_API_KEY&units=metric"
            response = requests.get(api_url).json()
            if response.get("main"):
                temp_c = response["main"]["temp"]
                temp_converted = convert_temperature(temp_c, unidad)
                st.success(f"✅ La temperatura en {ciudad} es {temp_converted:.2f}° {unidad}")
                
                # Guardar en el historial
                st.session_state['weather_history'].append(f"{ciudad}: {temp_converted:.2f}° {unidad}")
                
                # Mostrar gráfico de temperatura
                fig = px.bar(x=[ciudad], y=[temp_converted], labels={'x': 'Ciudad', 'y': f'Temperatura ({unidad})'}, title="Temperatura Actual")
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white' if st.session_state['theme'] == 'dark' else 'black')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("❌ Ciudad no encontrada")
        else:
            st.warning("⚠️ Por favor, ingresa una ciudad")
    
    # Mostrar historial de búsquedas
    if st.session_state['weather_history']:
        st.markdown("### 📜 Historial de Consultas")
        for entry in st.session_state['weather_history']:
            st.write(f"📌 {entry}")

# Mensaje final con un toque personalizado
if st.button("🚀 Enviar"):
    if nombre:
        st.success(f"👋 Hola, {nombre}. Has elegido {opcion}.")
    else:
        st.warning("⚠️ Por favor, ingresa tu nombre antes de continuar.")
