import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

# Aplicar estilos CSS personalizados
st.markdown(
    """
    <style>
        .stApp {
            background-color: #2A3132;
        }
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
        .stSelectbox > div > div > div > div {
            background-color: #336B87;
            color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #90AFC5 !important;
        }
        p, div {
            color: #ffffff !important;
        }
        .stColumn {
            padding: 0 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Datos de ciudades con coordenadas
CITIES_DATA = {
    'Budapest_1': {'lat': 47.4979, 'lon': 19.0402},
    'Prague_1': {'lat': 50.0755, 'lon': 14.4378},
    'Prague_2': {'lat': 50.0875, 'lon': 14.4213},
    'Prague_3': {'lat': 50.0841, 'lon': 14.4677},
    'Brno_1': {'lat': 49.1951, 'lon': 16.6068},
    'Munich_1': {'lat': 48.1351, 'lon': 11.5820},
    'Frankfurt_1': {'lat': 50.1109, 'lon': 8.6821}
}

# Crear DataFrame de ciudades para el mapa
cities_df = pd.DataFrame([
    {'lat': data['lat'], 'lon': data['lon'], 'city': city}
    for city, data in CITIES_DATA.items()
])

# Generar datos de ejemplo para ventas
def generate_sales_data(cities, start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    data = []
    for city in cities:
        sales = np.random.normal(1000, 200, len(dates))
        data.extend(list(zip([city]*len(dates), dates, sales)))
    df = pd.DataFrame(data, columns=['Ciudad', 'Fecha', 'Ventas'])
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

# Título principal
st.markdown("""
    <h1 style='text-align: center; margin-bottom: 30px; color: #90AFC5;'>
        Dashboard de Ventas
    </h1>
""", unsafe_allow_html=True)

# Formulario de selección de ciudades y fechas
with st.form("selection_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Selecciona las ciudades en el mapa")
        # Mostrar el mapa con todas las ciudades
        selected_points = st.map(cities_df, zoom=5)
        
        # Procesar la selección del mapa
        if selected_points is not None and len(selected_points) > 0:
            selected_cities = [
                cities_df.iloc[point['index']]['city']
                for point in selected_points['selected_points']
            ]
        else:
            selected_cities = list(CITIES_DATA.keys())
    
    with col2:
        st.write("### Selecciona el rango de fechas")
        start_date = st.date_input("Fecha de inicio:", datetime(2024, 1, 1))
        end_date = st.date_input("Fecha de fin:", datetime(2024, 1, 31))
    
    submit_button = st.form_submit_button("Actualizar Dashboard")

if submit_button or 'initial_load' not in st.session_state:
    st.session_state.initial_load = True
    
    # Generar datos
    with st.status("Generando datos de ventas...", expanded=True) as status:
        st.write("Cargando datos históricos...")
        df_ventas = generate_sales_data(selected_cities, start_date, end_date)
        df_productos = generate_product_data(selected_cities, start_date, end_date)
        st.toast("¡Datos generados con éxito!", icon="✅")
        status.update(label="Datos listos", state="complete")

    # Métricas de ventas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class='custom-card'>
                <div class='metric-label'>Venta Total</div>
                <div class='metric-value'>€{df_ventas['Ventas'].sum():,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='custom-card'>
                <div class='metric-label'>Promedio Diario</div>
                <div class='metric-value'>€{df_ventas['Ventas'].mean():,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='custom-card'>
                <div class='metric-label'>Venta Máxima</div>
                <div class='metric-value'>€{df_ventas['Ventas'].max():,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    # Gráfico de ventas
    st.markdown("## 📊 Gráficos de Ventas")
    fig_ventas = px.line(df_ventas, x='Fecha', y='Ventas', color='Ciudad',
                         title='Evolución de Ventas por Ciudad',
                         labels={'value': 'Euros', 'variable': 'Ciudad'})
    fig_ventas.update_layout(
        plot_bgcolor='#2A3132',
        paper_bgcolor='#2A3132',
        font=dict(color='white'),
        title_font_color='#90AFC5',
        legend_title_font_color='#90AFC5',
        legend_font_color='white',
        height=500
    )
    st.plotly_chart(fig_ventas, use_container_width=True)

    # Añadir espacio entre secciones
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Media de productos vendidos y disponibilidad
    st.markdown("## 📦 Productos y Disponibilidad")
    col1, col2 = st.columns([1, 1])
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
            legend_font_color='white',
            height=400
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
            legend_font_color='white',
            height=400
        )
        st.plotly_chart(fig_media_disponibilidad, use_container_width=True)

    # Añadir espacio entre secciones
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Top 10 productos más y menos vendidos
    st.markdown("## 🏆 Top 10 Productos Más y Menos Vendidos")
    col1, col2 = st.columns([1, 1])
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
            legend_font_color='white',
            height=400
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
            legend_font_color='white',
            height=400
        )
        st.plotly_chart(fig_least10, use_container_width=True)

    # Pie de página
    st.markdown("""
        ---
        <p style='text-align: center; color: #763626;'>
            Dashboard de Ventas © 2024
        </p>
    """, unsafe_allow_html=True)
