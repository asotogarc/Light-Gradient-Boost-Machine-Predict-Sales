import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
)

# Aplicar estilos CSS personalizados
st.markdown(
    """
    <style>
        /* Fondo general de la aplicación */
        .stApp {
            background-color: #2A3132;
        }
        /* Tarjetas personalizadas */
        .custom-card {
            background-color: #336B87;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #90AFC5;
        }
        .metric-label {
            font-size: 14px;
            color: #ffffff;
        }
        /* Selector de opciones */
        .stSelectbox > div > div > div > div {
            background-color: #336B87;
            color: #ffffff;
        }
        .stSelectbox > div > div > div > div:hover {
            background-color: #763626;
        }
        /* Títulos y textos */
        h1, h2, h3, h4, h5, h6 {
            color: #90AFC5 !important;
        }
        p, div {
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Generar datos de ejemplo para ventas
def generate_sales_data(cities, start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    data = []
    for city in cities:
        sales = np.random.normal(1000, 200, len(dates))
        data.extend(list(zip([city]*len(dates), dates, sales)))
    df = pd.DataFrame(data, columns=['Ciudad', 'Fecha', 'Ventas'])
    df['Predicción'] = df['Ventas'] * np.random.uniform(0.8, 1.2, len(df))
    return df

# Generar datos de productos
def generate_product_data(cities, start_date, end_date):
    products = ['Bakery', 'Fruit and vegetable', 'Meat and fish']
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    data = []
    for city in cities:
        for date in dates:
            for product in products:
                sales = np.random.normal(100, 20)
                availability = np.random.uniform(0.7, 1.0)
                data.append([city, date, product, sales, availability])
    df = pd.DataFrame(data, columns=['Ciudad', 'Fecha', 'Producto', 'Ventas', 'Disponibilidad'])
    return df

# Generar métricas del modelo
def generate_model_metrics():
    return {
        'MAE': round(np.random.uniform(50, 150), 2),
        'RMSE': round(np.random.uniform(100, 200), 2),
        'R2': round(np.random.uniform(0.7, 0.95), 3)
    }

# Título principal
st.markdown("""
    <h1 style='text-align: center; margin-bottom: 30px; color: #90AFC5;'>
        Dashboard de Ventas y Predicciones
    </h1>
""", unsafe_allow_html=True)

# Selector de opción principal
opcion = st.selectbox(
    "Selecciona el tipo de análisis:",
    ["Datos de Ventas", "Modelo Predictivo"]
)

# Selección de ciudades y fechas
cities = ['Budapest_1', 'Prague_2', 'Brno_1', 'Prague_1', 'Prague_3', 'Munich_1', 'Frankfurt_1']
selected_cities = st.multiselect("Selecciona las ciudades:", cities, default=cities)
start_date = st.date_input("Fecha de inicio:", datetime(2024, 1, 1))
end_date = st.date_input("Fecha de fin:", datetime(2024, 1, 31))

if opcion == "Datos de Ventas":
    st.markdown("## 📈 Análisis de Ventas")
    
    # Barra de progreso para simular carga de datos
    with st.status("Generando datos de ventas...", expanded=True) as status:
        st.write("Cargando datos históricos...")
        df_ventas = generate_sales_data(selected_cities, start_date, end_date)
        df_productos = generate_product_data(selected_cities, start_date, end_date)
        st.write("Procesando predicciones...")
        st.toast("¡Datos generados con éxito!", icon="✅")
        status.update(label="Datos listos", state="complete")
    
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
    st.markdown("## 📊 Gráficos de Ventas")
    col1, col2 = st.columns(2)
    with col1:
        fig_ventas = px.line(df_ventas, x='Fecha', y='Ventas', color='Ciudad',
                             title='Evolución de Ventas por Ciudad',
                             labels={'value': 'Euros', 'variable': 'Ciudad'})
        fig_ventas.update_layout(
            plot_bgcolor='#2A3132',
            paper_bgcolor='#2A3132',
            font=dict(color='white'),
            title_font_color='#90AFC5',
            legend_title_font_color='#90AFC5',
            legend_font_color='white'
        )
        st.plotly_chart(fig_ventas, use_container_width=True)
    
    with col2:
        fig_pred_vs_real = px.line(df_ventas, x='Fecha', y=['Ventas', 'Predicción'],
                                   title='Ventas vs Predicción',
                                   labels={'value': 'Euros', 'variable': 'Tipo'})
        fig_pred_vs_real.update_layout(
            plot_bgcolor='#2A3132',
            paper_bgcolor='#2A3132',
            font=dict(color='white'),
            title_font_color='#90AFC5',
            legend_title_font_color='#90AFC5',
            legend_font_color='white'
        )
        st.plotly_chart(fig_pred_vs_real, use_container_width=True)
    
    # Media de productos vendidos y disponibilidad
    st.markdown("## 📦 Productos y Disponibilidad")
    col1, col2 = st.columns(2)
    with col1:
        df_media_productos = df_productos.groupby('Producto')['Ventas'].mean().reset_index()
        fig_media_productos = px.bar(df_media_productos, x='Producto', y='Ventas',
                                     title='Media de Ventas por Producto',
                                     labels={'Ventas': 'Media de Ventas', 'Producto': 'Producto'})
        fig_media_productos.update_layout(
            plot_bgcolor='#2A3132',
            paper_bgcolor='#2A3132',
            font=dict(color='white'),
            title_font_color='#90AFC5',
            legend_title_font_color='#90AFC5',
            legend_font_color='white'
        )
        st.plotly_chart(fig_media_productos, use_container_width=True)
    
    with col2:
        df_media_disponibilidad = df_productos.groupby('Ciudad')['Disponibilidad'].mean().reset_index()
        fig_media_disponibilidad = px.bar(df_media_disponibilidad, x='Ciudad', y='Disponibilidad',
                                          title='Media de Disponibilidad por Ciudad',
                                          labels={'Disponibilidad': 'Media de Disponibilidad', 'Ciudad': 'Ciudad'})
        fig_media_disponibilidad.update_layout(
            plot_bgcolor='#2A3132',
            paper_bgcolor='#2A3132',
            font=dict(color='white'),
            title_font_color='#90AFC5',
            legend_title_font_color='#90AFC5',
            legend_font_color='white'
        )
        st.plotly_chart(fig_media_disponibilidad, use_container_width=True)
    
    # Top 10 productos más y menos vendidos
    st.markdown("## 🏆 Top 10 Productos Más y Menos Vendidos")
    col1, col2 = st.columns(2)
    with col1:
        df_top10 = df_productos.groupby('Producto')['Ventas'].sum().reset_index().sort_values(by='Ventas', ascending=False)
        fig_top10 = px.bar(df_top10, x='Producto', y='Ventas',
                           title='Top 10 Productos Más Vendidos',
                           labels={'Ventas': 'Total de Ventas', 'Producto': 'Producto'})
        fig_top10.update_layout(
            plot_bgcolor='#2A3132',
            paper_bgcolor='#2A3132',
            font=dict(color='white'),
            title_font_color='#90AFC5',
            legend_title_font_color='#90AFC5',
            legend_font_color='white'
        )
        st.plotly_chart(fig_top10, use_container_width=True)
    
    with col2:
        df_least10 = df_productos.groupby('Producto')['Ventas'].sum().reset_index().sort_values(by='Ventas', ascending=True)
        fig_least10 = px.bar(df_least10, x='Producto', y='Ventas',
                             title='Top 10 Productos Menos Vendidos',
                             labels={'Ventas': 'Total de Ventas', 'Producto': 'Producto'})
        fig_least10.update_layout(
            plot_bgcolor='#2A3132',
            paper_bgcolor='#2A3132',
            font=dict(color='white'),
            title_font_color='#90AFC5',
            legend_title_font_color='#90AFC5',
            legend_font_color='white'
        )
        st.plotly_chart(fig_least10, use_container_width=True)

else:  # Modelo Predictivo
    st.markdown("## 🤖 Métricas del Modelo")
    
    # Barra de progreso para simular carga de métricas
    with st.status("Calculando métricas del modelo...", expanded=True) as status:
        st.write("Cargando datos del modelo...")
        metricas = generate_model_metrics()
        st.write("Procesando métricas...")
        st.toast("¡Métricas calculadas con éxito!", icon="✅")
        status.update(label="Métricas listas", state="complete")
    
    # Métricas del modelo
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
    
    # Gráfico de valores predichos vs reales
    st.markdown("## 📈 Valores Predichos vs Reales")
    df_ventas = generate_sales_data(selected_cities, start_date, end_date)
    fig_pred_vs_real = px.line(df_ventas, x='Fecha', y=['Ventas', 'Predicción'],
                               title='Ventas vs Predicción',
                               labels={'value': 'Euros', 'variable': 'Tipo'})
    fig_pred_vs_real.update_layout(
        plot_bgcolor='#2A3132',
        paper_bgcolor='#2A3132',
        font=dict(color='white'),
        title_font_color='#90AFC5',
        legend_title_font_color='#90AFC5',
        legend_font_color='white'
    )
    st.plotly_chart(fig_pred_vs_real, use_container_width=True)

# Pie de página
st.markdown("""
    ---
    <p style='text-align: center; color: #763626;'>
        Dashboard de Ventas © 2024
    </p>
""", unsafe_allow_html=True)
