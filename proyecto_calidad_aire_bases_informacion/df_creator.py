import os
import requests
import pandas as pd

def data_countrys_create(countrys, filename):
    for key in countrys:
        api_key = '5a487281ef003fb208f3886e5e2e453f08579018' 
        url_i=  f'https://api.waqi.info/feed/{key}/?token={api_key}'
        response = requests.get(url_i)
        country_data = response.json()
        country = country_data['data']['city']['name']
        date = country_data['data']['time']['s']
        aqi= country_data['data']['aqi']
        countrys[key].update({date:aqi})
        
    df = pd.DataFrame(countrys)
    df.sort_index(inplace=True)
    df.to_excel(filename)

def data_countrys_load(countrys, filename):
    for key in countrys:
        api_key = '5a487281ef003fb208f3886e5e2e453f08579018' 
        url_i=  f'https://api.waqi.info/feed/{key}/?token={api_key}'
        response = requests.get(url_i)
        country_data = response.json()
        country = country_data['data']['city']['name']
        date = country_data['data']['time']['s']
        aqi= country_data['data']['aqi']
        countrys[key].update({date:aqi})
    
    df = pd.DataFrame(countrys)
    df.sort_index(inplace=True)
    df2 = pd.read_excel(filename, index_col=0)
    #df2.sort_index(inplace=True)
    df3 = pd.concat([df2,df], axis=0)
    #df3.sort_index(inplace=True)
    df3 = df3.drop_duplicates()
    df3.to_excel(filename)
        
countrys = {'Afganistan':{},
                #'Albania':{},
                'Algeria':{},
                'Andorra':{},
                'Argentina':{},
                'Australia':{},
                'Austria':{},
                'Azerbaijan':{},
                'Bahrain':{},
                'Bangladesh':{},
                'Belgium':{},
                #'Bhutan':{},
                'Bolivia':{},
                'Bosnia and Herzegovina':{},
                'Brazil':{},
                #'Brunei':{},
                'Bulgaria':{},
                'Cambodia':{},
                'Canada':{},
                'Chile':{},
                'China':{},
                'Colombia':{},
                'Costa Rica':{},
                'Croatia':{},
                'Cyprus':{},
                'Czech Republic':{},
                'Denmark':{},
                'Ecuador':{},
                #'Egypt':{},
                'Estonia':{},
                'Finland':{},
                'France':{},
                'Georgia':{},
                'Germany':{},
                'Ghana':{},
                'Gibraltar':{},
                'Greece':{},
                'Guatemala':{},
                'Hong Kong':{},
                'Hungary':{},
                'Iceland':{},
                'India':{},
                'Indonesia':{},
                #'Iran':{}, --> problema con la hora y fecha
                'Iraq':{},    
                'Ireland':{},
                'Israel':{},
                'Italy':{},
                'Japan':{},
                'Jordan':{},
                'Kazakhstan':{},
                'Kenya':{},
                'South Korea':{},
                'Kosovo':{},
                'Kuwait':{},
                'Kyrgyzstan':{},
                'Laos':{},
                #'Lebanon':{},
                #Liberia':{},
                'Lithuania':{},
                'Luxembourg':{},
                'Macao':{},
                'Macedonia':{},
                'Malaysia':{},
                'Malta':{}, 
                'Mexico':{},
                'Mongolia':{},
                'Montenegro':{},
                #'Morocco':{},
                'Myanmar':{},
                #'Nepal':{},
                'Netherlands':{},
                'New Caledonia':{},
                'New Zealand':{},
                'Norway':{},
                'Oman':{},
                'Pakistan':{},
                'Panama':{},
                'Peru':{},
                'Philippines':{},
                'Poland':{},
                'Portugal':{},
                'Puerto Rico':{},
                #'Qatar':{},
                'Romania':{},
                'Russia':{},
                'El Salvador':{},
                #'Saudi Arabia':{}, --> problema con las fechas y horas
                #'Senegal':{},
                #'Serbia':{},
                'Singapore':{},
                'Slovakia':{},
                'Slovenia':{},
                'South Africa':{},
                'Spain':{},
                'Sri Lanka':{},
                'Sweden':{},
                'Switzerland':{},
                'Taiwan':{},
                #'Tanzania':{},  
                'Thailand':{},
                #'Trinidad & Tobago':{},
                #'Tunisia':{},
                'Turkey':{},
                'Ukraine':{},
                #'United Arab Emirates':{},
                'United Kingdom':{},
                'United States':{},
                #'Venezuela':{},
                'Vietnam':{}
                }

filename = r'data_countrys.xlsx'

if os.path.exists(filename) == False:
    data_countrys_create(countrys, filename)

elif os.path.exists(filename) == True:
    data_countrys_load(countrys, filename)


