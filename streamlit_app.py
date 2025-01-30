import streamlit as st

# Estilos CSS personalizados con un diseño inspirado en Apple
st.markdown(
    """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: #F5F5F7;
        }
        .stApp {
            max-width: 800px;
            margin: auto;
            padding: 2rem;
            border-radius: 12px;
            background: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 {
            font-weight: 600;
            color: #1D1D1F;
            text-align: center;
        }
        .stButton > button {
            background-color: #007AFF;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #005ECF;
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #D1D1D6;
            padding: 10px;
            font-size: 16px;
        }
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 1px solid #D1D1D6;
            padding: 10px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📱 Aplicación Estilo Apple")

st.write("Explora una interfaz moderna con contrastes y colores llamativos inspirados en el diseño de Apple.")

# Entrada de texto
nombre = st.text_input("Ingresa tu nombre:")

# Selector de opción
opcion = st.selectbox("Elige una opción:", ["Opción 1", "Opción 2", "Opción 3"])

# Botón interactivo
if st.button("Enviar"):
    if nombre:
        st.success(f"Hola, {nombre}. Elegiste {opcion}.")
    else:
        st.warning("Por favor, ingresa tu nombre antes de continuar.")
