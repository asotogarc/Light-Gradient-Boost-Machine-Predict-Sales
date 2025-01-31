import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Inicializar tema
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

# Aplicar estilos CSS
st.markdown(
    """
    <style>
        .custom-card {
            background-color: #2d2d2d;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #007AFF;
        }
        .metric-label {
            font-size: 14px;
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Generar datos de ejemplo para ventas
def generate_sales_data():
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    sales = np.random.normal(1000, 200, len(dates))
    return pd.DataFrame({
        'Fecha': dates,
        'Ventas': sales,
        'Predicción': sales * np.random.uniform(0.8, 1.2, len(dates))
    })

# Generar métricas del modelo
def generate_model_metrics():
    return {
        'MAE': round(np.random.uniform(50, 150), 2),
        'RMSE': round(np.random.uniform(100, 200), 2),
        'R2': round(np.random.uniform(0.7, 0.95), 3)
    }

# Título principal
st.markdown("""
    <h1 style='text-align: center; margin-bottom: 30px;'>
        Dashboard de Ventas y Predicciones
    </h1>
""", unsafe_allow_html=True)

# Selector de opción principal
opcion = st.selectbox(
    "Selecciona el tipo de análisis:",
    ["Datos de Ventas", "Modelo Predictivo"]
)

if opcion == "Datos de Ventas":
    st.markdown("## 📈 Análisis de Ventas")
    
    # Generar datos de ventas
    df_ventas = generate_sales_data()
    
    # Métricas de ventas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class='custom-card'>
                <div class='metric-label'>Venta Total</div>
                <div class='metric-value'>€{:,.2f}</div>
            </div>
        """.format(df_ventas['Ventas'].sum()), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='custom-card'>
                <div class='metric-label'>Promedio Diario</div>
                <div class='metric-value'>€{:,.2f}</div>
            </div>
        """.format(df_ventas['Ventas'].mean()), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='custom-card'>
                <div class='metric-label'>Venta Máxima</div>
                <div class='metric-value'>€{:,.2f}</div>
            </div>
        """.format(df_ventas['Ventas'].max()), unsafe_allow_html=True)
    
    # Gráfico de ventas
    fig_ventas = px.line(df_ventas, x='Fecha', y=['Ventas', 'Predicción'],
                        title='Ventas vs Predicción',
                        labels={'value': 'Euros', 'variable': 'Tipo'})
    fig_ventas.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_ventas, use_container_width=True)

else:  # Modelo Predictivo
    st.markdown("## 🤖 Métricas del Modelo")
    
    # Métricas del modelo
    metricas = generate_model_metrics()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='custom-card'>
                <div class='metric-label'>MAE</div>
                <div class='metric-value'>{}</div>
            </div>
        """.format(metricas['MAE']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='custom-card'>
                <div class='metric-label'>RMSE</div>
                <div class='metric-value'>{}</div>
            </div>
        """.format(metricas['RMSE']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='custom-card'>
                <div class='metric-label'>R²</div>
                <div class='metric-value'>{}</div>
            </div>
        """.format(metricas['R2']), unsafe_allow_html=True)
    
    # Información del modelo
    st.markdown("""
        ### 📝 Detalles del Modelo
        - **Tipo de Modelo**: LightGBM
        - **Variables principales**: Histórico de ventas, temporada, día de la semana
        - **Periodo de entrenamiento**: 6 meses
        - **Frecuencia de actualización**: Diaria
    """)

# Pie de página
st.markdown("""
    ---
    <p style='text-align: center; color: gray;'>
        Dashboard de Ventas © 2024
    </p>
""", unsafe_allow_html=True)
