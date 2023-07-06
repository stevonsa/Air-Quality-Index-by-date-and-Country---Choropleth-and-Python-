'''
GRAFICACIÓN DE LA AIR QUALITY INDEX A TRAVÉS DEL TIEMPO

El programa permite conectarse a la página: https://aqicn.org/api/, mediante un usuario y una contraseña 
dado por la misma página, en esta se solicita el país/ciudad de la que se desea consultar, mediante conexión .json 
podemos almacenar fecha, país y el AQI, correspondiente, creando una base de datos que modificamos para mostrar el cambio
estado de la contaminación del aire através del tiempo en un mapa mundial.

Autor: Steven Gerardo Chacón Salazar.
GIHUB: https://github.com/stevonsa
Fecha: 04 de julio del 2023
Curso: IE-0217
Universidad de Costa Rica
Escuela de Ingeniería Eléctrica
'''
#importación de librerias 
import os
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import pycountry as pc
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html

#creación del nombre del documento que almacena los datos
filename = r'data_countrys.xlsx'

#lista de los países en la base de datos.
countrys = ['Afghanistan','Albania','Algeria','Andorra','Argentina','Australia','Austria','Azerbaijan',
            'Bahrain','Bangladesh','Belgium','Bhutan','Bolivia','Bosnia and Herzegovina','Brazil','Brunei','Bulgaria',
            'Cambodia','Canada','Chile','China','Colombia','Costa Rica','Croatia','Cyprus','Czech Republic','Denmark',
            'Ecuador','Egypt','Estonia','Finland','France','Georgia','Germany','Ghana','Gibraltar','Greece','Guatemala','Hong Kong',
            'Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel','Italy','Japan','Jordan','Kazakhstan',
            'Kenya','South Korea','Kosovo','Kuwait','Kyrgyzstan','Laos','Lebanon','Liberia','Lithuania','Luxembourg','Macao',
            'Macedonia','Malaysia','Malta', 'Mexico','Mongolia','Montenegro','Morocco','Myanmar','Nepal','Netherlands','New Caledonia','New Zealand',
            'Norway','Oman','Pakistan','Panama','Peru','Philippines','Poland','Portugal','Puerto Rico','Qatar','Romania','Rusia','El Salvador',
            'Saudi Arabia', 'Senegal','Serbia','Singapore','Slovakia','Slovenia','South Africa','Spain','Sri Lanka','Sweden','Switzerland',
            'Taiwan','Tanzania','Thailand','Trinidad & Tobago','Tunisia','Turkey','Ukraine','United Arab Emirates','United Kingdom','United States','Venezuela','Vietnam']

def df_create(countrys, filename):
    '''
    Permite la conexión con el servidor y extraer los datos, además de la creación de la database.
    
    Variables: 
    
        - countrys: lista de los países involucrados y consultados.
        
        - filename: nombre del archivo a modificar.
    
    Termina de guardar en filename los datos consultados.
    '''
    df = pd.DataFrame()
    df = pd.DataFrame(columns=['date','code','country','aqi'])
    for i in range(len(countrys)):
        try:
            api_key = '5a487281ef003fb208f3886e5e2e453f08579018'
            url_i=  f'https://api.waqi.info/feed/{countrys[i]}/?token={api_key}'   
            response = requests.get(url_i) 
            country_data = response.json()   
            date = country_data['data']['time']['s']
            aqi= country_data['data']['aqi']
            df = df._append({'date': date, 'country': countrys[i], 'aqi':aqi}, ignore_index = True)     
        except:
            pass
        
    df.sort_index(inplace=True)
    df.to_excel(filename)
    print('Se ha creado la base de datos.')

def df_load(countrys, filename):
    '''
    Permite la conexión con el servidor y extraer los datos, además de la actualización de la database.
    
    Variables: 
    
        - countrys: lista de los países involucrados y consultados.
        
        - filename: nombre del archivo a modificar.
    
    Termina de guardar en filename los datos consultados.
    '''
    df = pd.DataFrame()
    df = pd.DataFrame(columns=['date','code','country','aqi'])
    for i in range(len(countrys)):
        try:
            api_key = '5a487281ef003fb208f3886e5e2e453f08579018'
            url_i=  f'https://api.waqi.info/feed/{countrys[i]}/?token={api_key}'   
            response = requests.get(url_i) 
            country_data = response.json()   
            date = country_data['data']['time']['s']
            aqi= country_data['data']['aqi']
            df = df._append({'date': date, 'country': countrys[i], 'aqi':aqi}, ignore_index = True)     
        except:
            pass
    df.sort_index(inplace=True)
    df2 = pd.read_excel(filename, index_col=0)
    df2.sort_index(inplace=True)
    df3 = pd.concat([df2, df], axis = 0)
    df3.sort_index(inplace=True)
    df3 = df3.drop_duplicates()
    df3.to_excel(filename)
    print('Se ha actualizado la base de datos.')

def update_df(filename, countrys):
    '''
    Determina la existencia del documento, y en caso de no existir continua con la función df_create, para crear la data base.
    En caso contrario, continua con la función df_load, para actualizar la data base.
    
    Variables: 
    
        - countrys: lista de los países involucrados y consultados.
        
        - filename: nombre del archivo a modificar.
    
    Termina de decidir y crear la data base.
    '''
    if os.path.exists(filename) == False:
        df_create(countrys, filename)

    elif os.path.exists(filename) == True:
        df_load(countrys, filename)
    
def get_alpha_3(location):
    '''
    Otorga el alpha_3 según la variable country.
    
    Variables: 

        - location: country en la data base.
    
    En la columna code da el alpha_3 de cada país.
    
    '''
    try: 
        return pc.countries.get(name=location).alpha_3
    except:
        return None

def set_aqi(df):
    '''
    Determina la catedoría según el aqi y lo agrega a la columna a status.
    
    Variables: 

        - df: es la database.
    
    '''
    if 0 < df['aqi'] < 50:
        return 'good'
    if 51 < df['aqi'] < 100:
        return 'moderate'
    if 101 < df['aqi'] < 150:
        return 'unhealty for sensitive groups'
    if 151 < df['aqi'] < 200:
        return 'unhealty'
    if 201 < df['aqi'] < 300:
        return 'very unhealty'
    if 301 < df['aqi'] <1000:
        return 'hazardous'

def world_map(filename):
    '''
    Modifica el database además de crear las condiciones necesarias para la fig choropleth.
    
    Variables: 

        - filename: nombre del archivo a modificar.
    
    '''
    df = pd.read_excel(filename, index_col=0)
    df = df.drop_duplicates()
    df['code'] = df['country'].apply(lambda x: get_alpha_3(x))
    df = df.sort_values(by='date')
    df = df.reset_index(drop=True)
    value_aqi = []
    status = []
    for i in range(len(df['aqi'])):
        valor = df['aqi'][i]
        valores = pd.to_numeric(valor, errors='coerce')
        value_aqi.append(valores)
    
    for i in range(len(value_aqi)):
        if 0 <= value_aqi[i] <= 50:
            status.append('good')
        if 51 <= value_aqi[i] <= 100:
            status.append('moderate')
        if 101 <= value_aqi[i] <= 150:
            status.append('unhealty for sensitive groups') 
        if 151 <= value_aqi[i] <= 200:
            status.append('unhealty') 
        if 201 <= value_aqi[i] <= 300:
            status.append('very unhealty') 
        if 301 <= value_aqi[i] <= 1000:
            status.append('hazardous') 
        if np.isnan(value_aqi[i]) == True : 
            status.append('unavailable')
        
    df['status'] = status
    df = df.to_csv('data.csv')

#declaración de update_df
#update_df(filename, countrys)

#declaración de world_map
world_map(filename) 

#lectura del documento preprocesado
data = pd.read_csv('data.csv')

#creación de la figura con los datos de data.cvs
fig = px.choropleth(data, locations='code',
                        color='status', 
                        color_discrete_map={
                            'good' : '#009966',
                            'moderate' : '#ffde33',
                            'unhealty for sensitive groups' : '#ff9933',
                            'unhealty' : '#cc0033',
                            'very unhealty' : '#660099',
                            'hazardous' : '#7e0023',
                            'unavailable' : '#FFF9C9'
                        },
                        category_orders={
                            'status': [
                                'good',
                                'moderate',
                                'unhealty for sensitive groups',
                                'unhealty',
                                'very unhealty',
                                'hazardous',
                                'unavailable'
                                ]},
                        animation_frame='date',
                        hover_name='country',
                        animation_group="status",
                        projection='natural earth',
                        title='<b>AIR QUALITY INDEX GLOBAL</b>',
                    )
fig.update_layout(
                    showlegend=True,
                    legend_title_text='<b>AQI STATUS</b>',
                    font={"size": 16, "color": "#808080", "family" : "calibri"},
                    margin={"r":0,"t":40,"l":0,"b":0},
                    legend=dict(orientation='v'),
                    geo=dict(bgcolor= 'rgba(0,0,0,0)', 
                            showlakes = True, lakecolor='#2D4356',
                            showocean = True, oceancolor='#435B66',
                            showland = True, landcolor='#FBFFDC',
                            subunitcolor='grey')
                )

#declaración del layout en dash para el servidor
app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# corre las funcionalidades de dash
app.run_server(debug=True, use_reloader=False) 