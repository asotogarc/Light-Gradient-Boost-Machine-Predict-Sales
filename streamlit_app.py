import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Estadísticas de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    /* Fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    /* Títulos más grandes y modernos */
    h1 {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1d1d1f;
    }
    h2 {
        font-size: 2rem;
        font-weight: 500;
        color: #1d1d1f;
    }
    h3 {
        font-size: 1.5rem;
        font-weight: 500;
        color: #1d1d1f;
    }
    /* Sidebar con fondo claro */
    .css-1d391kg {
        background-color: #f5f5f7;
        padding: 1rem;
        border-radius: 10px;
    }
    /* Botones y filtros modernos */
    .stSelectbox, .stMultiselect {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #d2d2d7;
    }
    /* Tablas con bordes redondeados */
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Gráficos con fondo transparente */
    .plotly-graph-div {
        background-color: transparent !important;
    }
    /* Notas finales con estilo */
    .stMarkdown {
        font-size: 0.9rem;
        color: #6e6e73;
    }
    </style>
    """, unsafe_allow_html=True)

# Añadir sonido al interactuar con los filtros
st.markdown("""
    <audio id="clickSound">
        <source src="https://www.soundjay.com/buttons/button-3.mp3" type="audio/mpeg">
        Tu navegador no soporta el elemento de audio.
    </audio>
    <script>
        function playSound() {
            var audio = document.getElementById("clickSound");
            audio.play();
        }
        // Escuchar cambios en los filtros
        document.addEventListener("DOMContentLoaded", function() {
            var selectbox = document.querySelector(".stSelectbox select");
            var multiselect = document.querySelector(".stMultiselect input");
            if (selectbox) {
                selectbox.addEventListener("change", function() {
                    playSound();
                });
            }
            if (multiselect) {
                multiselect.addEventListener("change", function() {
                    playSound();
                });
            }
        });
    </script>
    """, unsafe_allow_html=True)

# Título de la aplicación
st.title("📊 Análisis de Ventas y Ciencia de Datos")

# Cargar datos de ejemplo
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'Fecha': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'Producto': np.random.choice(['Producto A', 'Producto B', 'Producto C'], 100),
        'Ventas': np.random.randint(100, 1000, 100),
        'Región': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], 100)
    })
    return data

data = load_data()

# Sidebar para filtros
st.sidebar.header("Filtros")
producto_seleccionado = st.sidebar.selectbox("Selecciona un producto", data['Producto'].unique())
region_seleccionada = st.sidebar.multiselect("Selecciona una región", data['Región'].unique(), default=data['Región'].unique())

# Filtrar datos
filtered_data = data[(data['Producto'] == producto_seleccionado) & (data['Región'].isin(region_seleccionada))]

# Mostrar datos filtrados
st.subheader("Datos Filtrados")
st.dataframe(filtered_data.style.format({"Ventas": "{:,.0f}"}), height=300)

# Gráfico de ventas por fecha
st.subheader("Ventas por Fecha")
fig_fecha = px.line(
    filtered_data,
    x='Fecha',
    y='Ventas',
    title=f"Ventas de {producto_seleccionado} por Fecha",
    labels={'Ventas': 'Total de Ventas', 'Fecha': 'Fecha'},
    line_shape="spline",
    color_discrete_sequence=["#007AFF"]
)
fig_fecha.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)
st.plotly_chart(fig_fecha, use_container_width=True)

# Gráfico de ventas por región
st.subheader("Ventas por Región")
fig_region = px.bar(
    filtered_data,
    x='Región',
    y='Ventas',
    title=f"Ventas de {producto_seleccionado} por Región",
    labels={'Ventas': 'Total de Ventas', 'Región': 'Región'},
    color='Región',
    color_discrete_sequence=["#007AFF", "#34C759", "#FF9500", "#FF2D55"]
)
fig_region.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)
st.plotly_chart(fig_region, use_container_width=True)

# Gráfico de torta de distribución de ventas por producto
st.subheader("Distribución de Ventas por Producto")
ventas_por_producto = data.groupby('Producto')['Ventas'].sum().reset_index()
fig_torta = px.pie(
    ventas_por_producto,
    values='Ventas',
    names='Producto',
    title="Distribución de Ventas por Producto",
    color_discrete_sequence=["#007AFF", "#34C759", "#FF9500"]
)
fig_torta.update_traces(textposition='inside', textinfo='percent+label')
fig_torta.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_torta, use_container_width=True)

# Estadísticas descriptivas
st.subheader("Estadísticas Descriptivas")
st.write(filtered_data['Ventas'].describe().to_frame().style.format("{:,.0f}"))

# Heatmap de correlación (solo para columnas numéricas)
st.subheader("Heatmap de Correlación")
numeric_data = data.select_dtypes(include=[np.number])
corr = numeric_data.corr()
fig_heatmap = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale='Blues'
))
fig_heatmap.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Notas finales
st.markdown("---")
st.markdown("**Nota:** Esta aplicación es un ejemplo básico para mostrar estadísticas de ventas y análisis de datos utilizando Streamlit.")
