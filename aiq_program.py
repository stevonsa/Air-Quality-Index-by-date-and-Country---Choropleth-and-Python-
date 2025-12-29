"""
GRAFICACIÓN DEL AIR QUALITY INDEX (AQI) A TRAVÉS DEL TIEMPO

Descripción:
    Este programa consulta la API de WAQI (World Air Quality Index) para obtener el AQI
    de una lista de países (o ubicaciones). Con esos datos construye/actualiza una base
    de datos local (Excel) con registros históricos y luego genera un mapa mundial animado
    (choropleth) con Plotly. Finalmente levanta un servidor web con Dash para visualizar
    el mapa.

Fuentes:
    - API WAQI: https://aqicn.org/api/
    - Endpoint usado (feed por ubicación): https://api.waqi.info/feed/{location}/?token={token}

Autor:
    Steven Gerardo Chacón Salazar
GitHub:
    https://github.com/stevonsa
Fecha:
    04 de julio del 2023
Curso:
    IE-0217 - Universidad de Costa Rica, Escuela de Ingeniería Eléctrica
"""

# =========================
# IMPORTACIÓN DE LIBRERÍAS
# =========================
import os  # Para comprobar existencia de archivos
import requests  # Para realizar peticiones HTTP a la API
import pandas as pd  # Para manipulación de tablas (DataFrames) y lectura/escritura Excel/CSV
import numpy as np  # Para manejo de NaN
import plotly.express as px  # Para gráficos (choropleth)
import pycountry as pc  # Para obtener códigos ISO alpha-3 de países
from dash import Dash, dcc, html  # Para levantar una app web y mostrar el gráfico


# ======================================
# CONFIGURACIÓN: ARCHIVO Y LISTA DE PAÍSES
# ======================================

# Nombre del archivo Excel donde se guarda el histórico de datos (base de datos local).
filename = r"data_countrys.xlsx"

# Lista de países/ubicaciones a consultar en el endpoint /feed/{location}/
# Nota: WAQI responde mejor con ciudades/estaciones; aquí se usa una lista de países.
countrys = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Argentina", "Australia", "Austria", "Azerbaijan",
    "Bahrain", "Bangladesh", "Belgium", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Brazil", "Brunei", "Bulgaria",
    "Cambodia", "Canada", "Chile", "China", "Colombia", "Costa Rica", "Croatia", "Cyprus", "Czech Republic", "Denmark",
    "Ecuador", "Egypt", "Estonia", "Finland", "France", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Guatemala", "Hong Kong",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Japan", "Jordan", "Kazakhstan",
    "Kenya", "South Korea", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Liberia", "Lithuania", "Luxembourg", "Macao",
    "Macedonia", "Malaysia", "Malta", "Mexico", "Mongolia", "Montenegro", "Morocco", "Myanmar", "Nepal", "Netherlands", "New Caledonia", "New Zealand",
    "Norway", "Oman", "Pakistan", "Panama", "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Romania", "Rusia", "El Salvador",
    "Saudi Arabia", "Senegal", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "Spain", "Sri Lanka", "Sweden", "Switzerland",
    "Taiwan", "Tanzania", "Thailand", "Trinidad & Tobago", "Tunisia", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Venezuela", "Vietnam",
]


# ==========================================================
# FUNCIÓN: CREAR BASE DE DATOS (Excel) DESDE CERO
# ==========================================================
def df_create(countrys, filename):
    """
    Crea un archivo Excel con la información consultada en la API (primera ejecución).

    Parámetros:
        countrys (list[str]):
            Lista de países/ubicaciones a consultar en la API.
        filename (str):
            Nombre del archivo Excel donde se guardará el DataFrame.

    Salida:
        - Genera un DataFrame con columnas: date, code, country, aqi
        - Guarda el DataFrame en Excel (filename).
        - Imprime un mensaje indicando que se creó la base de datos.

    Nota:
        Actualmente el token está “hardcodeado” y se usa un try/except general que ignora errores.
    """
    # Se crea un DataFrame vacío con las columnas objetivo.
    df = pd.DataFrame(columns=["date", "code", "country", "aqi"])

    # Consulta uno por uno cada país/ubicación.
    for i in range(len(countrys)):
        try:
            # Token de la API WAQI (debe ser proporcionado por el sitio).
            api_key = "5a487281ef003fb208f3886e5e2e453f08579018"

            # Endpoint feed por ubicación
            url_i = f"https://api.waqi.info/feed/{countrys[i]}/?token={api_key}"

            # Petición a la API
            response = requests.get(url_i)
            country_data = response.json()

            # Extrae fecha/hora (string) y AQI (valor numérico o None)
            date = country_data["data"]["time"]["s"]
            aqi = country_data["data"]["aqi"]

            # Agrega fila al DataFrame
            df = df._append({"date": date, "country": countrys[i], "aqi": aqi}, ignore_index=True)

        except:
            # Si hay error (red, respuesta inválida, clave faltante, etc.), lo ignora.
            pass

    # Ordena por índice y exporta a Excel.
    df.sort_index(inplace=True)
    df.to_excel(filename)
    print("Se ha creado la base de datos.")


# ==========================================================
# FUNCIÓN: ACTUALIZAR BASE DE DATOS (agrega nuevas filas)
# ==========================================================
def df_load(countrys, filename):
    """
    Actualiza el archivo Excel existente con nuevas consultas a la API.

    Flujo:
        1) Crea un DataFrame (df) con los datos nuevos consultados.
        2) Carga el Excel existente en df2.
        3) Concatena df2 + df, elimina duplicados y guarda de nuevo.

    Parámetros:
        countrys (list[str]):
            Lista de países/ubicaciones a consultar.
        filename (str):
            Archivo Excel existente (base de datos local).

    Salida:
        - Actualiza el archivo Excel con nuevos registros.
    """
    df = pd.DataFrame(columns=["date", "code", "country", "aqi"])

    for i in range(len(countrys)):
        try:
            api_key = "5a487281ef003fb208f3886e5e2e453f08579018"
            url_i = f"https://api.waqi.info/feed/{countrys[i]}/?token={api_key}"
            response = requests.get(url_i)
            country_data = response.json()

            date = country_data["data"]["time"]["s"]
            aqi = country_data["data"]["aqi"]

            df = df._append({"date": date, "country": countrys[i], "aqi": aqi}, ignore_index=True)

        except:
            pass

    # Carga histórico existente
    df.sort_index(inplace=True)
    df2 = pd.read_excel(filename, index_col=0)
    df2.sort_index(inplace=True)

    # Une histórico + nuevos datos
    df3 = pd.concat([df2, df], axis=0)
    df3.sort_index(inplace=True)

    # Elimina duplicados (sin especificar columnas; elimina filas idénticas)
    df3 = df3.drop_duplicates()

    # Guarda en Excel
    df3.to_excel(filename)
    print("Se ha actualizado la base de datos.")


# ==========================================================
# FUNCIÓN: DECIDIR SI CREAR O ACTUALIZAR EL EXCEL
# ==========================================================
def update_df(filename, countrys):
    """
    Decide si se crea o se actualiza la base de datos local.

    Si el archivo no existe:
        - Llama df_create() para crear Excel desde cero.
    Si el archivo sí existe:
        - Llama df_load() para actualizar.

    Parámetros:
        filename (str): archivo Excel de datos.
        countrys (list[str]): lista de países/ubicaciones.
    """
    if os.path.exists(filename) is False:
        df_create(countrys, filename)
    else:
        df_load(countrys, filename)


# ==========================================================
# FUNCIÓN: OBTENER ISO ALPHA-3 PARA CADA PAÍS
# ==========================================================
def get_alpha_3(location):
    """
    Convierte el nombre del país a su código ISO alpha-3 (por ejemplo: 'Costa Rica' -> 'CRI').

    Parámetros:
        location (str): nombre del país (según la columna 'country').

    Retorna:
        str | None:
            - Código alpha-3 si se encuentra el país en pycountry.
            - None si no se encuentra o hay error.

    Nota:
        Algunos nombres pueden no coincidir exactamente con pycountry (ej: 'Rusia' vs 'Russia').
    """
    try:
        return pc.countries.get(name=location).alpha_3
    except:
        return None


# ==========================================================
# FUNCIÓN (NO USADA EN EL FLUJO ACTUAL): CLASIFICAR AQI
# ==========================================================
def set_aqi(df):
    """
    Clasifica el AQI en categorías.

    Parámetros:
        df (Series/dict-like):
            Se asume que df['aqi'] existe.

    Retorna:
        str:
            Categoría textual (good, moderate, ...)

    Nota:
        Esta función NO se usa en el flujo final.
        Además, usa rangos con huecos (50, 51, 100, etc.) por los operadores '<'.
    """
    if 0 < df["aqi"] < 50:
        return "good"
    if 51 < df["aqi"] < 100:
        return "moderate"
    if 101 < df["aqi"] < 150:
        return "unhealty for sensitive groups"
    if 151 < df["aqi"] < 200:
        return "unhealty"
    if 201 < df["aqi"] < 300:
        return "very unhealty"
    if 301 < df["aqi"] < 1000:
        return "hazardous"


# ==========================================================
# FUNCIÓN: PREPROCESAR DATOS PARA EL MAPA Y EXPORTAR A CSV
# ==========================================================
def world_map(filename):
    """
    Preprocesa la base de datos (Excel) para crear un CSV listo para graficar.

    Pasos:
        1) Lee el Excel.
        2) Elimina duplicados.
        3) Agrega columna 'code' (ISO alpha-3) a partir de 'country'.
        4) Ordena por fecha.
        5) Convierte 'aqi' a numérico (por si hay strings o valores no válidos).
        6) Genera 'status' según rangos de AQI.
        7) Exporta a 'data.csv'.

    Parámetros:
        filename (str): nombre del archivo Excel de entrada.

    Salida:
        - Genera 'data.csv' con columnas: date, country, aqi, code, status (y otras si están presentes).
    """
    # Cargar datos históricos
    df = pd.read_excel(filename, index_col=0)

    # Limpiar duplicados
    df = df.drop_duplicates()

    # Agregar código ISO alpha-3 para Plotly (choropleth usa ISO-3 típicamente)
    df["code"] = df["country"].apply(lambda x: get_alpha_3(x))

    # Ordenar por fecha
    df = df.sort_values(by="date").reset_index(drop=True)

    # Convertir AQI a numérico (coerce -> NaN si no puede convertir)
    value_aqi = []
    status = []

    for i in range(len(df["aqi"])):
        valor = df["aqi"][i]
        valores = pd.to_numeric(valor, errors="coerce")
        value_aqi.append(valores)

    # Clasificación por rangos (incluye "unavailable" si NaN)
    for i in range(len(value_aqi)):
        if 0 <= value_aqi[i] <= 50:
            status.append("good")
        if 51 <= value_aqi[i] <= 100:
            status.append("moderate")
        if 101 <= value_aqi[i] <= 150:
            status.append("unhealty for sensitive groups")
        if 151 <= value_aqi[i] <= 200:
            status.append("unhealty")
        if 201 <= value_aqi[i] <= 300:
            status.append("very unhealty")
        if 301 <= value_aqi[i] <= 1000:
            status.append("hazardous")
        if np.isnan(value_aqi[i]) is True:
            status.append("unavailable")

    # Guardar status en el DF
    df["status"] = status

    # Exportar a CSV (ojo: esta línea devuelve None y sobrescribe df si se reasigna)
    df.to_csv("data.csv", index=False)


# ======================================
# EJECUCIÓN PRINCIPAL
# ======================================

# Si querés crear/actualizar la base automáticamente, descomentá:
# update_df(filename, countrys)

# Preprocesa Excel -> data.csv para graficar
world_map(filename)

# Lectura del CSV preprocesado
data = pd.read_csv("data.csv")

# ======================================
# CREACIÓN DE FIGURA (CHOROPLETH)
# ======================================
fig = px.choropleth(
    data,
    locations="code",          # ISO alpha-3
    color="status",            # categoría de AQI
    hover_name="country",      # nombre que aparece al pasar el mouse
    animation_frame="date",    # animación por fecha
    animation_group="status",
    projection="natural earth",
    title="<b>AIR QUALITY INDEX GLOBAL</b>",
    color_discrete_map={
        "good": "#009966",
        "moderate": "#ffde33",
        "unhealty for sensitive groups": "#ff9933",
        "unhealty": "#cc0033",
        "very unhealty": "#660099",
        "hazardous": "#7e0023",
        "unavailable": "#FFF9C9",
    },
    category_orders={
        "status": [
            "good",
            "moderate",
            "unhealty for sensitive groups",
            "unhealty",
            "very unhealty",
            "hazardous",
            "unavailable",
        ]
    },
)

# Ajustes visuales del mapa
fig.update_layout(
    showlegend=True,
    legend_title_text="<b>AQI STATUS</b>",
    font={"size": 16, "color": "#808080", "family": "calibri"},
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    legend=dict(orientation="v"),
    geo=dict(
        bgcolor="rgba(0,0,0,0)",
        showlakes=True,
        lakecolor="#2D4356",
        showocean=True,
        oceancolor="#435B66",
        showland=True,
        landcolor="#FBFFDC",
        subunitcolor="grey",
    ),
)

# ======================================
# DASH APP (VISUALIZACIÓN EN WEB)
# ======================================
app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Ejecuta el servidor Dash
app.run(debug=True)

