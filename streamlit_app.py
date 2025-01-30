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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📱 App Estilo Apple")

st.write("Esta es una aplicación simple con un diseño limpio y moderno inspirado en Apple.")

if st.button("Presiona Aquí"):
    st.success("¡Botón presionado!")
