import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Estadísticas de Ventas", page_icon="📊", layout="wide")

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
st.dataframe(filtered_data)

# Gráfico de ventas por fecha
st.subheader("Ventas por Fecha")
fig_fecha = px.line(filtered_data, x='Fecha', y='Ventas', title=f"Ventas de {producto_seleccionado} por Fecha")
st.plotly_chart(fig_fecha, use_container_width=True)

# Gráfico de ventas por región
st.subheader("Ventas por Región")
fig_region = px.bar(filtered_data, x='Región', y='Ventas', title=f"Ventas de {producto_seleccionado} por Región")
st.plotly_chart(fig_region, use_container_width=True)

# Gráfico de torta de distribución de ventas por producto
st.subheader("Distribución de Ventas por Producto")
ventas_por_producto = data.groupby('Producto')['Ventas'].sum().reset_index()
fig_torta = px.pie(ventas_por_producto, values='Ventas', names='Producto', title="Distribución de Ventas por Producto")
st.plotly_chart(fig_torta, use_container_width=True)

# Estadísticas descriptivas
st.subheader("Estadísticas Descriptivas")
st.write(filtered_data['Ventas'].describe())

# Heatmap de correlación (solo para columnas numéricas)
st.subheader("Heatmap de Correlación")

# Seleccionar solo las columnas numéricas
numeric_data = data.select_dtypes(include=[np.number])

# Calcular la matriz de correlación
corr = numeric_data.corr()

# Crear el heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale='Viridis'
))
st.plotly_chart(fig_heatmap, use_container_width=True)
# Notas finales
st.markdown("---")
st.markdown("**Nota:** Esta aplicación es un ejemplo básico para mostrar estadísticas de ventas y análisis de datos utilizando Streamlit.")
