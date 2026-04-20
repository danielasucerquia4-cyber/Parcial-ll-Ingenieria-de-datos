"""
Dashboard de Data Warehouse - Construcción ETL
===============================================
Aplicación Streamlit para visualización y análisis de datos
del Data Warehouse de ventas con modelo Estrella (Star Schema)

Autor: Pipeline ETL
Versión: 1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="DW Ventas - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    """Carga los datasets desde CSV"""
    ventas = pd.read_csv('data/ventas.csv')
    clientes = pd.read_csv('data/clientes.csv')
    productos = pd.read_csv('data/productos.csv')
    fechas = pd.read_csv('data/fechas.csv')
    
    # Construir Data Warehouse (joins)
    dw = ventas.merge(clientes, on='id_cliente')
    dw = dw.merge(productos, on='id_producto')
    dw = dw.merge(fechas, on='id_fecha')
    
    # Convertir fecha a datetime
    dw['fecha'] = pd.to_datetime(dw['fecha'])
    
    return dw, ventas, clientes, productos, fechas

# Cargar datos
dw, ventas, clientes, productos, fechas = load_data()

# Título principal
st.title("📊 Data Warehouse - Dashboard de Ventas")
st.markdown("---")

# Función para crear el panel de navegación
def create_navigation():
    """Crea el sidebar de navegación"""
    st.sidebar.title("🧭 Navegación")
    
    menu_options = [
        "📈 Dashboard",
        "🔮 Análisis Predictivo",
        "⚙️ Orquestación de Datos"
    ]
    
    selected = st.sidebar.radio("Ir a:", menu_options)
    
    st.sidebar.markdown("---")
    st.sidebar.title("ℹ️ Información")
    st.sidebar.info("""
    **Pipeline ETL - Data Warehouse**
    
    Estedashboard muestra un modelo 
    estrella (Star Schema) con:
    - Tabla de hechos: ventas
    - Dimensiones: clientes, 
      productos, fechas
    """)
    
    return selected

# Página Dashboard
def show_dashboard():
    """Muestra el dashboard principal con visualizaciones"""
    st.header("📈 Dashboard de Ventas")
    
    # Filtros interactivos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_regions = st.multiselect(
            "Filtrar por Región",
            options=dw['region'].unique(),
            default=dw['region'].unique()
        )
    
    with col2:
        selected_categories = st.multiselect(
            "Filtrar por Categoría",
            options=dw['categoria'].unique(),
            default=dw['categoria'].unique()
        )
    
    with col3:
        year_filter = st.selectbox(
            "Filtrar por Año",
            options=['Todos'] + list(dw['año'].unique())
        )
    
    # Aplicar filtros
    filtered_dw = dw.copy()
    if selected_regions:
        filtered_dw = filtered_dw[filtered_dw['region'].isin(selected_regions)]
    if selected_categories:
        filtered_dw = filtered_dw[filtered_dw['categoria'].isin(selected_categories)]
    if year_filter != 'Todos':
        filtered_dw = filtered_dw[filtered_dw['año'] == year_filter]
    
    # Métricas principales
    st.subheader("📌 Métricas Clave")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Total Ventas", f"${filtered_dw['total'].sum():,.0f}")
    with m2:
        st.metric("Cantidad Vendida", f"{filtered_dw['cantidad'].sum():,}")
    with m3:
        st.metric("Clientes Únicos", filtered_dw['id_cliente'].nunique())
    with m4:
        st.metric("Productos Únicos", filtered_dw['id_producto'].nunique())
    
    st.markdown("---")
    
    # Visualizaciones
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("📊 Histograma: Ventas por Categoría")
        fig_hist = px.bar(
            filtered_dw.groupby('categoria')['total'].sum().reset_index(),
            x='categoria',
            y='total',
            color='categoria',
            title="Ventas Totales por Categoría",
            labels={'total': 'Ventas Totales', 'categoria': 'Categoría'}
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col_v2:
        st.subheader("🌍 Mapa: Ventas por Ciudad")
        city_sales = filtered_dw.groupby(['ciudad', 'region'])['total'].sum().reset_index()
        fig_map = px.scatter_geo(
            city_sales,
            locations=city_sales['ciudad'],
            locationmode="locations",
            size='total',
            color='total',
            title="Distribución de Ventas por Ciudad",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # Tabla de datos
    st.subheader("📋 Datos Detallados")
    st.dataframe(
        filtered_dw[['fecha', 'nombre', 'ciudad', 'nombre_producto', 'categoria', 'cantidad', 'total']],
        use_container_width=True,
        hide_index=True
    )
    
    # Descarga de datos filtrados
    csv = filtered_dw.to_csv(index=False).encode('utf-8')
    st.download_button(
        "💾 Descargar Datos Filtrados (CSV)",
        data=csv,
        file_name="datos_filtrados.csv",
        mime="text/csv"
    )

# Página de Análisis Predictivo
def show_predictive_analysis():
    """Muestra análisis predictivo de ventas"""
    st.header("🔮 Análisis Predictivo")
    
    st.markdown("""
    ### 🧠 Modelo de Predicción de Ventas
    
    Esta sección simula un modelo de Machine Learning para predecir 
    ventas futuras basado en datos históricos.
    
    **Técnicas utilizadas:**
    - Regresión Lineal
    - Random Forest
    - Series Temporales (ARIMA)
    """)
    
    # Simulación de predicción
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Predicción de Ventas por Producto")
        
        # Agrupar por producto
        product_sales = dw.groupby('nombre_producto')['total'].sum().reset_index()
        product_sales = product_sales.sort_values('total', ascending=False).head(10)
        
        fig_pred = px.bar(
            product_sales,
            x='nombre_producto',
            y='total',
            color='total',
            title="Top 10 Productos por Ventas Totales",
            labels={'total': 'Ventas Totales ($)'}
        )
        fig_pred.update_layout(xaxis_title="Producto", showlegend=False)
        st.plotly_chart(fig_pred, use_container_width=True)
    
    with col2:
        st.subheader("📊 Tendencia de Ventas Mensuales")
        
        monthly_sales = dw.groupby(['año', 'mes'])['total'].sum().reset_index()
        monthly_sales = monthly_sales.sort_values(['año', 'mes'])
        
        fig_trend = px.line(
            monthly_sales,
            x='mes',
            y='total',
            color='año',
            title="Tendencia de Ventas por Mes",
            markers=True
        )
        fig_trend.update_layout(xaxis_title="Mes", yaxis_title="Ventas Totales ($)")
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    
    # Matriz de correlación
    st.subheader("🔗 Matriz de Correlación")
    
    numeric_cols = dw.select_dtypes(include=['number']).columns
    corr_matrix = dw[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Matriz de Correlación de Variables",
        color_continuous_scale="RdBu_r"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Predicción simulada
    st.markdown("---")
    st.subheader("🎯 Predicción para Próximo Mes")
    
    avg_monthly = dw.groupby('mes')['total'].mean().mean()
    prediction = avg_monthly * 1.1  # 10% crecimiento esperado
    
    st.info(f"""
    **Predicción de ventas para el próximo mes:** 
    ${prediction:,.0f}
    
    *Basado en el promedio histórico con un factor de crecimiento del 10%*
    """)

# Página de Orquestación de Datos
def show_data_orchestration():
    """Explica el pipeline ETL de orquestación de datos"""
    st.header("⚙️ Orquestación de Datos")
    
    st.markdown("""
    ## 🔄 Pipeline ETL - Extraer, Transformar, Cargar
    
    El pipeline ETL (Extract, Transform, Load) es el proceso fundamental
    para construir este Data Warehouse.
    """)
    
    # Diagrama del pipeline
    st.subheader("📋 Fases del Pipeline ETL")
    
    phases = {
        "1. EXTRACT (Extraer)": """
        - **Origen:** Archivos CSV (ventas.csv, clientes.csv, productos.csv, fechas.csv)
        - Cargar datos desde fuentes heterogéneas
        - Validar integridad de los datos
        """,
        "2. TRANSFORM (Transformar)": """
        - **Limpieza:** Manejar valores faltantes, duplicados
        - **Enriquecimiento:** Unir tablas con JOIN (Star Schema)
        - **Agregación:** Calcular métricas aggregadas
        - **Filtrado:** Eliminar outliers si es necesario
        """,
        "3. LOAD (Cargar)": """
        - **Almacenamiento:** Guardar en cleaned_dataset.csv
        - **Disponibilidad:** Listo para análisis y visualización
        - **Actualización:** Pipeline reproducible
        """
    }
    
    for phase, description in phases.items():
        with st.expander(phase):
            st.markdown(description)
    
    st.markdown("---")
    
    # DAG_simulado
    st.subheader("🔀 DAG (Directed Acyclic Graph)")
    
    st.markdown("""
    El siguiente DAG representa el flujo de tareas en Apache Airflow:
    """)
    
    # Crear visualización del DAG
    dag_data = pd.DataFrame({
        'Task': ['start', 'extract', 'transform', 'load', 'validate', 'end'],
        'Status': ['success', 'success', 'success', 'success', 'running', 'pending'],
        'Type': ['sensor', 'operator', 'operator', 'operator', 'operator', 'sensor']
    })
    
    fig_dag = go.Figure()
    
    # Agregar nodos
    for i, row in dag_data.iterrows():
        color = {'success': '#28a745', 'running': '#ffc107', 'pending': '#6c757d'}[row['Status']]
        fig_dag.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode='markers+text',
            marker=dict(size=50, color=color),
            text=[row['Task']],
            textposition='bottom center',
            name=row['Task']
        ))
    
    fig_dag.update_layout(
        title="DAG de Apache Airflow - Pipeline ETL",
        showlegend=False,
        xaxis=dict(range=[-1, 6], showticklabels=False),
        yaxis=dict(range=[-1, 1], showticklabels=False),
        height=300
    )
    
    st.plotly_chart(fig_dag, use_container_width=True)
    
    # Referencia a imagen DAG
    st.markdown("""
    > **Nota:** La imagen visual del DAG se encuentra en `dag.png`
     
    ![DAG Pipeline](dag.png)
    """)
    
    st.markdown("---")
    
    # Código del pipeline
    st.subheader("💻 Código del Pipeline (Simulado)")
    
    st.code("""
    # Simulación de DAG en Airflow
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from datetime import datetime
    
    default_args = {
        'owner': 'etl_pipeline',
        'start_date': datetime(2024, 1, 1),
    }
    
    dag = DAG(
        'dw_ventas_etl',
        default_args=default_args,
        schedule_interval='@daily'
    )
    
    def extract():
        # Extraer datos de fuentes
        pass
    
    def transform():
        # Transformar y limpiar datos
        pass
    
    def load():
        # Cargar al Data Warehouse
        pass
    
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        dag=dag
    )
    
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        dag=dag
    )
    
    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        dag=dag
    )
    
    extract_task >> transform_task >> load_task
    """, language="python")
    
    st.markdown("---")
    
    # Métricas del pipeline
    st.subheader("📊 Métricas del Pipeline")
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Filas Procesadas", len(dw))
    with m2:
        st.metric("Fuentes", "4 CSV")
    with m3:
        st.metric("Última Ejecución", datetime.now().strftime("%Y-%m-%d %H:%M"))
    with m4:
        st.metric("Estado", "✅ Completo")

# Función principal
def main():
    """Función principal de la aplicación"""
    
    # Obtener página seleccionada
    page = create_navigation()
    
    # Mostrar página según selección
    if page == "📈 Dashboard":
        show_dashboard()
    elif page == "🔮 Análisis Predictivo":
        show_predictive_analysis()
    elif page == "⚙️ Orquestación de Datos":
        show_data_orchestration()

if __name__ == "__main__":
    main()