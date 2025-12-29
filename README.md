# 🌍 Air Quality Index (AQI) – Visualización Global

Este proyecto permite **consultar, almacenar y visualizar el Índice de Calidad del Aire (AQI)** de múltiples países a lo largo del tiempo, utilizando la **API de World Air Quality Index (WAQI)** y una **visualización interactiva en un mapa mundial** mediante Plotly y Dash.

El sistema construye una base de datos histórica local y muestra la evolución del estado de la contaminación del aire en una animación temporal.

---

## 📌 Objetivo del proyecto

- Consultar datos de calidad del aire (AQI) desde una API pública.
- Almacenar los datos en una base local (Excel / CSV).
- Clasificar el AQI según categorías estándar.
- Visualizar la información en un **mapa mundial animado**.
- Desplegar la visualización en una **aplicación web** con Dash.

---

## 🧪 Fuente de datos

- **World Air Quality Index (WAQI)**  
  https://aqicn.org/api/

Se utiliza el endpoint:

https://api.waqi.info/feed/%7Blocation%7D/?token=%7BAPI_TOKEN%7D

## 🗂️ Estructura del proyecto

Air-Quality-Index-by-date-and-Country/
│
├── app.py # Script principal (consulta, procesamiento y visualización)
├── data_countrys.xlsx # Base de datos local (histórico AQI)
├── data.csv # Archivo preprocesado para la visualización
├── README.md # Documentación del proyecto
├── requirements.txt # Dependencias del proyecto
└── .venv/ # Entorno virtual


---

## ⚙️ Requisitos

- Python **3.9 o superior**
- Conexión a internet
- Token válido de la API WAQI

---

## 📦 Dependencias

Instalar las librerías necesarias con:

```bash
pip install requests pandas numpy plotly pycountry dash openpyxl
```

O usando un archivo requirements.txt:

- requests
- pandas
- numpy
- plotly
- pycountry
- dash
- openpyxl

---

## 🔐 API Token (WAQI)

Es necesario crear una cuenta en WAQI y obtener un **token personal**.

Actualmente el token está definido directamente en el código (`api_key`).  
⚠️ Para un entorno profesional se recomienda usar variables de entorno.

Ejemplo (PowerShell):

```powershell
setx AQI_TOKEN "TU_TOKEN_AQUI"
```
### ▶️ Ejecución del proyecto

(Opcional) Crear y activar un entorno virtual:

`python -m venv .venv`

`.\.venv\Scripts\activate`

Ejecutar el programa:

`python app.py`

Abrir el navegador en:

http://127.0.0.1:8050/

---

## 🗺️ Visualización

El mapa muestra:

Colores por categoría de AQI (Good, Moderate, etc.)

Animación temporal según la fecha del registro

Información detallada al pasar el cursor sobre cada país


---

## 📊 Clasificación del AQI

| Rango AQI | Categoría |
|----------|----------|
| 0 – 50 | Good |
| 51 – 100 | Moderate |
| 101 – 150 | Unhealthy for Sensitive Groups |
| 151 – 200 | Unhealthy |
| 201 – 300 | Very Unhealthy |
| > 300 | Hazardous |
| NaN | Unavailable |

---

## ⚠️ Limitaciones conocidas

- La API WAQI responde mejor a **ciudades o estaciones**, no siempre a países completos.
- Algunos nombres de países no coinciden con `pycountry`, por lo que el código ISO puede ser `None`.
- El manejo de errores está simplificado (`try/except pass`).
- El token de la API está hardcodeado (no recomendado para producción).

---

## 🚀 Posibles mejoras

- Uso de variables de entorno para el token.
- Sustituir Excel por SQLite.
- Manejo explícito de errores y logs.
- Usar ciudades o estaciones en lugar de países.
- Filtros interactivos (dropdown por país, rango de fechas).
- Despliegue en la nube (Render, etc.).

---

## 👨‍💻 Autor

**Steven Gerardo Chacón Salazar**  
Universidad de Costa Rica – Escuela de Ingeniería Eléctrica  
GitHub: https://github.com/stevonsa

---

## 📚 Contexto académico

- Curso: **IE-0217**
- Institución: **Universidad de Costa Rica**
- Fecha: **Julio 2023**