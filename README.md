# Parcial-ll-Ingenieria-de-datos
# 📊 Data Warehouse - Proyecto de Ingeniería de Datos

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-Open%20Source-green)](https://github.com)

## 📋 Descripción

Este proyecto implementa un **Data Warehouse** utilizando el modelo Estrella (Star Schema), un patrón ampliamente usado en Business Intelligence y Análisis de Datos. El pipeline ETL integra múltiples fuentes de datos en un solo Data Warehouse listo para análisis.

## 🏗️ Estructura del Proyecto

```
PARCIAL/
├── data/                     # Datos fuente
│   ├── clientes.csv         # Dimensión clientes
│   ├── productos.csv      # Dimensión productos
│   ├── fechas.csv        # Dimensión fechas
│   └── ventas.csv       # Tabla de hechos
├── notebooks/               # Notebooks Jupyter
│   └── DW_EST.ipynb       # Tutorial de construcción
├── app.py                 # Dashboard Streamlit
├── cleaned_dataset.csv    # Dataset limpio (resultado ETL)
├── index.html          # Landing page
├── requirements.txt    # Dependencias
└── README.md         # Este archivo
```

---

## 🔄 Pipeline ETL - Explicación Técnica

El pipeline ETL (Extract, Transform, Load) es el proceso fundamental para construir este Data Warehouse.

### 1️⃣ EXTRACT (Extraer)

En la fase de extracción, los datos se cargan desde las fuentes originales:

```python
import pandas as pd

# Cargar tablas de dimensiones
clientes = pd.read_csv('data/clientes.csv')
productos = pd.read_csv('data/productos.csv')
fechas = pd.read_csv('data/fechas.csv')

# Cargar tabla de hechos
ventas = pd.read_csv('data/ventas.csv')
```

**Origen de datos:**
- Archivos CSV en el directorio `data/`
- 4 tablas separadas (ventas, clientes, productos, fechas)

### 2️⃣ TRANSFORM (Transformar)

En la fase de transformación, los datos se limpian y unen:

```python
# Construir Data Warehouse con JOIN (Star Schema)
dw = ventas.merge(clientes, on='id_cliente')
dw = dw.merge(productos, on='id_producto')
dw = dw.merge(fechas, on='id_fecha')

# Limpieza de datos
dw = dw.dropna()  # Eliminar valores faltantes
dw = dw.drop_duplicates()  # Eliminar duplicados
```

**Transformaciones aplicadas:**
- Join con claves foráneas para Enriched data
- Eliminación de valores nulos
- Normalización de tipos de datos

### 3️⃣ LOAD (Cargar)

En la fase de carga, los datos transformados se almacenan:

```python
# Guardar Data Warehouse limpio
dw.to_csv('cleaned_dataset.csv', index=False)
```

**Resultado:**
- Dataset consolidado: `cleaned_dataset.csv`
- Listo para análisis y visualización

---

## 🚀 Uso del Dashboard

### Requisitos

```bash
pip install -r requirements.txt
```

### Ejecutar

```bash
streamlit run app.py
```

### Panels disponibles

1. **📈 Dashboard** - Visualizaciones interactivas
   - Histogramas de ventas por categoría
   - Mapa de distribución por ciudad
   - Tablas de datos filtrables

2. **🔮 Análisis Predictivo**
   - Predicciones de ventas
   - Tendencias temporales
   - Correlación de variables

3. **⚙️ Orquestación de Datos**
   - Explicación del pipeline ETL
   - Simulación de DAG (Airflow)
   - Métricas del proceso

---

## 📊 Badges

| Badge | Descripción |
|-------|-------------|
| ![Python](https://img.shields.io/badge/Python-3.12-blue) | Lenguaje de programación |
| ![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red) | Framework del dashboard |
| ![GitHub](https://img.shields.io/badge/GitHub-Open%20Source-green) | Control de versiones |

---

## 📖 Documentación Adicional

- [Landing Page](index.html) - Página de inicio para GitHub Pages
- [Diccionario de Variables](index.html#diccionario) - Definición de campos
- [Código Fuente](app.py) - Dashboard completo

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abra un issue o envíe un pull request.

---

## 📝 Licencia

Este proyecto es de uso educativo - Universidad de Ingeniería de Datos.

---

*Construido con Python, Streamlit y ❤️*
