import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.graph_objects as go


#Inicio Dashboard
st.set_page_config(layout="wide", page_title="Cobertura Internet VS Educación en Colombia")#Inicializador streamlit

##Inicio carga y limpieza de los datos --------------------------------------------------------------
#importar los datos que se encuentran en formato .csv en @cache para evitar la recarga constante de los datos

@st.cache_data
def cargar_limpieza_fijo():
    data = pd.read_csv('coberturainternetfijo.csv')
    #Limpieza de datos cobertura fijo
    datos_limpios = data.drop_duplicates().dropna() #limpieza datos duplicados y nulos
    #Correción tipo de datos
    datos_limpios['INDICE'] = datos_limpios['INDICE'].str.replace(',','.') #pandas trabaja con '.' y no con ',' por esto se reemplazan
    datos_limpios['INDICE']=pd.to_numeric(datos_limpios['INDICE'], downcast='float')
    datos_limpios = datos_limpios.rename(columns={'COD_MUNICIPIO': 'CODIGO_MUNICIPIO'}) #renombrar la columna codigo municipio para que sea facil hacer el join entre las 4 tablas
    datos_limpios['CODIGO_MUNICIPIO']=pd.to_numeric(datos_limpios['CODIGO_MUNICIPIO'])
    df_filtrado = datos_limpios[
    ((datos_limpios['AÑO'] < 2023) & (datos_limpios['TRIMESTRE'] == 4)) | 
    ((datos_limpios['AÑO'] == 2023) & (datos_limpios['TRIMESTRE'] == 3))
    ]   
    df_filtrado = df_filtrado.iloc[:,[0,3,4,5,6,7,8]] #filtrar dataframe para dejar solo las columnas que se van a usar
    return df_filtrado 

df_coberturaFijo = cargar_limpieza_fijo()


#importar los datos que se encuentran en formato .csv en @cache para evitar la recarga constante de los datos

@st.cache_data
def cargar_limpieza_movil():
    data = pd.read_csv('coberturamovil.csv')
    datos_limpios = data.drop_duplicates().dropna() #Se eliminan datos nulos y duplicados
    datos_limpios[['COBERTURA 2G','COBERTURA 3G','COBERTURA HSPA+, HSPA+DC','COBERTUTA 4G','COBERTURA LTE','COBERTURA 5G']] = datos_limpios[['COBERTURA 2G','COBERTURA 3G','COBERTURA HSPA+, HSPA+DC','COBERTUTA 4G','COBERTURA LTE','COBERTURA 5G'
                         ]].replace({'S':1,'N':0})#Se reemplazan las S por 1 y las N por 0, esto con el fin de facilitar la operaciones matematicas
    datos_limpios = datos_limpios.rename(columns={'COD MUNICIPIO': 'CODIGO_MUNICIPIO'}) #renombrar la columna codigo municipio para que sea facil hacer el join entre las 4 tablas
    #datos_limpios['COBERTURA 2G','COBERTURA 3G','COBERTURA HSPA+, HSPA+DC','COBERTUTA 4G','COBERTURA LTE','COBERTURA 5G']=pd.to_numeric(datos_limpios['COBERTURA 2G','COBERTURA 3G','COBERTURA HSPA+, HSPA+DC','COBERTUTA 4G','COBERTURA LTE','COBERTURA 5G'])     
    
    datos_limpios['CODIGO_MUNICIPIO']=pd.to_numeric(datos_limpios['CODIGO_MUNICIPIO'])    
    datos_limpios = datos_limpios.iloc[:,[0,5,10,11,12,13,14,15]]
    datos_limpios = datos_limpios.groupby(['AÑO','CODIGO_MUNICIPIO']).agg({'COBERTURA 2G':'max','COBERTURA 3G':'max','COBERTURA HSPA+, HSPA+DC':'max','COBERTUTA 4G':'max','COBERTURA LTE':'max','COBERTURA 5G':'max'})
    return datos_limpios

df_coberturaMovil = cargar_limpieza_movil()


#importar los datos que se encuentran en formato .csv en @cache para evitar la recarga constante de los datos

@st.cache_data
def cargar_limpieza_educacion():
    data = pd.read_csv('educacion.csv')
    df_limpio = data.fillna(0) #Cambia los valores nulos por ceros
    df_limpio = df_limpio.replace('',0)#reemplaza los campos vacios por ceros
    df_limpio = df_limpio.rename(columns={'CÓDIGO_MUNICIPIO': 'CODIGO_MUNICIPIO'}) #renombrar la columna codigo municipio para que sea facil hacer el join entre las 4 tablas
    df_limpio['CODIGO_MUNICIPIO']=pd.to_numeric(df_limpio['CODIGO_MUNICIPIO'])
    df_limpio = df_limpio.iloc[:,[0,1,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]]
    return df_limpio

df_coberturaEducacion = cargar_limpieza_educacion()

@st.cache_data
def cargar_limpieza_viviendas():
    data = pd.read_excel('viviendas_hogares_proyeccion.xlsx', sheet_name=2) #Cargar documento xlsx y usar la hoja 3
    df_limpios = data.iloc[10:] #trabajar desde la fila 10 en adelante
    #df_limpios = df_limpios.drop(df_limpios.columns[11:23], axis=1) #eliminar las columna desde la 11 a la 22
    df_limpios = df_limpios.rename(columns={ #renombrar todos los encabezados
            'Unnamed: 0': 'Codigo Departamento',
            'Unnamed: 1': 'Nombre Departamento',
            'Unnamed: 2': 'CODIGO_MUNICIPIO',
            'Unnamed: 3': 'Nombre Municipio',
            'Unnamed: 4': 'Área',
            'Unnamed: 5': '2018',
            'Unnamed: 6': '2019',
            'Unnamed: 7': '2020',
            'Unnamed: 8': '2021',
            'Unnamed: 9': '2022',
            'Unnamed: 10': '2023',    
    })
    df_filtrado = df_limpios[df_limpios['Área']=='Total'] # Filtrar en la columna area solo los totales
    df_convertido = pd.melt(df_filtrado, #hacer un funcion unpivot para covertir las columna de años en filas
                    id_vars=['Codigo Departamento','Nombre Departamento', 'CODIGO_MUNICIPIO', 'Nombre Municipio', 'Área'], 
                    value_vars=['2018', '2019', '2020','2021', '2022', '2023'],
                    var_name='AÑO', 
                    value_name='Hogares')
    df_convertido['CODIGO_MUNICIPIO']=pd.to_numeric(df_convertido['CODIGO_MUNICIPIO'])
    df_convertido['AÑO']=pd.to_numeric(df_convertido['AÑO'])
    #st.write(df_convertido) previsualización para identificar columnas
    df_convertido = df_convertido.iloc[:,[2,5,6]]
    return df_convertido

df_viviendas = cargar_limpieza_viviendas()


#st.title("Cobertura Fijo")
#st.write(df_coberturaFijo) # validacion de que los datos se este imprimiendo correctamente

#st.title("Cobertura Educacion")
#st.write(df_coberturaEducacion) # validacion de que los datos se este imprimiendo correctamente

#st.title("Cobertura Movil")
#st.write(df_coberturaMovil) # validacion de que los datos se este imprimiendo correctamente

#st.title("Cobertura Vivienda")
#st.write(df_viviendas) # validacion de que los datos se este imprimiendo correctamente
##Fin carga, limpieza y transformación de los datos --------------------------------------------------------------

#Unión de las 4 tablas
df_fijo_movil = pd.merge(df_coberturaFijo, 
                       df_coberturaMovil, 
                       on=['CODIGO_MUNICIPIO', 'AÑO'], how='inner')
df_fijo_movil_educacion = pd.merge(df_fijo_movil, 
                       df_coberturaEducacion,
                       on=['CODIGO_MUNICIPIO', 'AÑO'], how='inner')
df_completo = pd.merge(df_fijo_movil_educacion, 
                       df_viviendas,
                       on=['CODIGO_MUNICIPIO', 'AÑO'], how='inner')



#st.title("Data Frame Completo")
#st.write(df_completo) # validacion de que los datos se este imprimiendo correctamente




#Inicio analisis de los datos para reponder las preguntas
##Fin analisis de los datos --------------------------------------------------------------



#¿Preguntas para plasmar en el Dashboard?
#1.Existe una correlación entre la cobertura de internet y la deserción estudiantil o la aprobación estudiantil? 

df_cobertura_educacion = df_completo.groupby(['AÑO','DEPARTAMENTO']).agg({'POBLACIÓN DANE':'sum',
                                                                    'Hogares':'sum',
                                                                    'No. ACCESOS FIJOS A INTERNET':'sum',
                                                                    'COBERTURA 2G':'sum','COBERTURA 3G':'sum',
                                                                    'COBERTURA HSPA+, HSPA+DC':'sum','COBERTUTA 4G':'sum',
                                                                    'COBERTURA LTE':'sum',
                                                                    'COBERTURA 5G':'sum'}).reset_index()

#2. Cuales son los departamentos con mayor y menor cobertura a nivel nacional?
df_cobertura_2023 = df_completo[df_completo['AÑO']==2023].groupby('DEPARTAMENTO').agg({'POBLACIÓN DANE':'sum',
                                                                                       'Hogares':'sum',
                                                                                       'No. ACCESOS FIJOS A INTERNET':'sum',
                                                                                       'COBERTURA 2G':'sum','COBERTURA 3G':'sum',
                                                                                       'COBERTURA HSPA+, HSPA+DC':'sum','COBERTUTA 4G':'sum',
                                                                                       'COBERTURA LTE':'sum',
                                                                                       'COBERTURA 5G':'sum'}).reset_index()
df_cobertura_2023['COBERTURA TOTAL MOVIL']= df_cobertura_2023['COBERTURA 2G']+\
                                        df_cobertura_2023['COBERTURA 3G']+\
                                        df_cobertura_2023['COBERTURA HSPA+, HSPA+DC']+\
                                        df_cobertura_2023['COBERTUTA 4G']+\
                                        df_cobertura_2023['COBERTURA LTE']+\
                                            df_cobertura_2023['COBERTURA 5G']
                                            
df_cobertura_2023['%COBERTURA']=(df_cobertura_2023['No. ACCESOS FIJOS A INTERNET']/df_cobertura_2023['Hogares'])*100

df_cobertura_2023=df_cobertura_2023[['DEPARTAMENTO','POBLACIÓN DANE','Hogares','No. ACCESOS FIJOS A INTERNET','%COBERTURA','COBERTURA TOTAL MOVIL']]  

top10_mejores= df_cobertura_2023.sort_values(by='%COBERTURA',ascending=False).head(5)#Crear un dataframe con los 5 primeros datos de forma ascendete para sacar los 10 peores departamentos
top10_peores= df_cobertura_2023.sort_values(by='%COBERTURA',ascending=True).head(5)#Crear un dataframe con los 5 primeros datos de forma descente para sacar los 10 mejores departamentos


df_departamentos = df_completo['DEPARTAMENTO'].unique() #df para seleccionar los departamentos
df_opciones_departamento = ['Todos']+ sorted(df_departamentos)



#Evolución cobertura movil a traves de los años





#cobertura por municipio

df_completo = df_completo.sort_values(by=(['AÑO','DEPARTAMENTO','MUNICIPIO']), ascending=True).reset_index()
df_cobertura_municipio = df_completo[['DEPARTAMENTO','MUNICIPIO','AÑO','No. ACCESOS FIJOS A INTERNET','Hogares']]
df_cobertura_municipio=df_cobertura_municipio[df_cobertura_municipio['AÑO']==2023]
df_cobertura_municipio['%COBERTURA'] = (df_completo['No. ACCESOS FIJOS A INTERNET']/df_completo['Hogares'])*100

# Sidebar para seleccionar el Departamento y el tema de color
st.sidebar.title("📈 Comportamiento Cobertura internet VS Educación en Colombia")
select_departamento = st.sidebar.selectbox("Selecciona un departamento", df_opciones_departamento)  # Seleccionar un departamento o dejar todos para afectar tablas y graficos
select_año = st.sidebar.selectbox("Selecciona año",['2018','2019','2020','2021','2022','2023'])


if select_departamento == "Todos":
    total_hogares = df_completo[df_completo['AÑO'] == int(select_año)]['Hogares'].sum()
       
else:
    total_hogares = df_completo[
        (df_completo['DEPARTAMENTO']==select_departamento) & (df_completo['AÑO']==int(select_año))
    ]
    total_hogares = total_hogares['Hogares'].sum()

if select_departamento == "Todos":
    total_fijo = df_completo[df_completo['AÑO'] == int(select_año)]['No. ACCESOS FIJOS A INTERNET'].sum()
       
else:
    total_fijo = df_completo[
        (df_completo['DEPARTAMENTO']==select_departamento) & (df_completo['AÑO']==int(select_año))
    ]
    total_fijo = total_fijo['No. ACCESOS FIJOS A INTERNET'].sum()
    
    

    


with st.container():
    st.sidebar.metric(label="Número de Hogares", value=int(total_hogares), delta_color="normal")
    st.sidebar.metric(label="Número de Acceso fijo", value=int(total_fijo), delta_color="normal")
    st.sidebar.metric(label="% De Cobertura", value=f"{int((total_fijo/total_hogares)*100)} %", delta_color="normal")

#------------------------Inicio Mapa--------------------------------------------------------------

def mapa():
    df_departamentos_gpd = gpd.read_file('departamentos/Depto.shp')#Importar datos de los departamentos
    df_completo['%COBERTURA'] = (df_completo['No. ACCESOS FIJOS A INTERNET']/df_completo['Hogares'])*100

    df_cobertura_municipio = df_completo.rename(columns={'DEPARTAMENTO': 'DeNombre'})#renombrar columna para facilitar que coincida para el join
    # Agrupar los datos de cobertura por año y nombre del departamento
    df_cobertura_municipio = df_cobertura_municipio.groupby(['AÑO', 'DeNombre'])['%COBERTURA'].mean().reset_index()
    # Asegurar que los nombres de los departamentos coincidan en ambos DataFrames
    df_departamentos_gpd['DeNombre'] = df_departamentos_gpd['DeNombre'].astype(str).str.upper()

    # Hacer el merge inicial con todos los datos de cobertura
    df_departamentos_gpd = df_departamentos_gpd.merge(df_cobertura_municipio, on='DeNombre', how='inner')
    anio_seleccionado = select_año

    # Filtrar los datos de cobertura por el año seleccionado    
    df_cobertura_seleccionado = df_departamentos_gpd[df_departamentos_gpd['AÑO'] == int(anio_seleccionado)]

    # Graficar el mapa según el año seleccionado
    st.markdown(f"### Cobertura de Internet para el año {anio_seleccionado}")

    # Crear el gráfico
    fig, ax = plt.subplots(1, 1, figsize=(4, 5), dpi=100)
    
    df_cobertura_seleccionado.plot(column='%COBERTURA', cmap='Blues', ax=ax, vmin=0, vmax=100)

    # Quitar etiquetas y ticks de los ejes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('') 
    ax.set_ylabel('') 
    fig.tight_layout()
    # Mostrar el gráfico en la app de Streamlit
    st.pyplot(fig,)  # Asegúrate de que el gráfico use el ancho del contenedor



# dataframe para los % de aprobación y deserción

#Agrupado por años y departamentos
df_aprobacion_desercion = df_completo[['AÑO','DEPARTAMENTO','MUNICIPIO','DESERCIÓN','APROBACIÓN']]
df_aprobacion_desercion_departamentos = df_aprobacion_desercion.groupby(['AÑO','DEPARTAMENTO']).agg({'DESERCIÓN':'mean',
                                                                                                     'APROBACIÓN':'mean'}).reset_index()

df_aprobacion_desercion_departamentos['AÑO']=df_aprobacion_desercion_departamentos['AÑO'].astype(str)

df_AD_añosDepartamento = df_aprobacion_desercion_departamentos[
        ((df_aprobacion_desercion_departamentos['AÑO'] == select_año) & 
         (df_aprobacion_desercion_departamentos['DEPARTAMENTO'] == select_departamento)) 
]

# dataframe para los % de aprobación y deserción
#Agrupado por años

df_aprobacion_desercion = df_completo[['AÑO','DEPARTAMENTO','MUNICIPIO','DESERCIÓN','APROBACIÓN']]
df_aprobacion_desercion_departamentos = df_aprobacion_desercion.groupby(['AÑO']).agg({'DESERCIÓN':'mean',
                                                                                                     'APROBACIÓN':'mean'}).reset_index()

df_aprobacion_desercion_departamentos['AÑO']=df_aprobacion_desercion_departamentos['AÑO'].astype(str)

df_AD_AÑOS = df_aprobacion_desercion_departamentos[
        ((df_aprobacion_desercion_departamentos['AÑO'] == select_año)) 
]



# DataFrame para las Correlaciones, cobertura hogar vs deseción y aprobación
# Inicio___________________________________________________________________________________________________________________


df_cobertura_correcion = df_completo[['DEPARTAMENTO','MUNICIPIO','AÑO','No. ACCESOS FIJOS A INTERNET','Hogares','DESERCIÓN','APROBACIÓN']]
df_cobertura_correcion = df_cobertura_correcion.groupby(['AÑO','DEPARTAMENTO']).agg({'DESERCIÓN':'mean','APROBACIÓN':'mean','No. ACCESOS FIJOS A INTERNET':'sum','Hogares':'sum'}).reset_index()
df_cobertura_correcion['%COBERTURA']=(df_cobertura_correcion['No. ACCESOS FIJOS A INTERNET']/df_cobertura_correcion['Hogares'])*100


df_cobertura_correcion_filtro = df_cobertura_correcion[
    
        ((df_cobertura_correcion['DEPARTAMENTO'] == select_departamento)) 
]


df_cobertura_correcion_nacional = df_completo[['DEPARTAMENTO','MUNICIPIO','AÑO','No. ACCESOS FIJOS A INTERNET','Hogares','DESERCIÓN','APROBACIÓN']]
df_cobertura_correcion_nacional = df_cobertura_correcion_nacional.groupby(['AÑO']).agg({'DESERCIÓN':'mean','APROBACIÓN':'mean','No. ACCESOS FIJOS A INTERNET':'sum','Hogares':'sum'}).reset_index()

df_cobertura_correcion_nacional['%COBERTURA']=(df_cobertura_correcion_nacional['No. ACCESOS FIJOS A INTERNET']/df_cobertura_correcion_nacional['Hogares'])*100

print(df_cobertura_correcion_nacional)

#Fin correlacion ________________________________________________________________________________________________________

    # Datos de ejemplo
def cobertura_desercion():
    x = [2018, 2019, 2020, 2021, 2022, 2023]
    
    if select_departamento == 'Todos':
        y1 = df_cobertura_correcion_nacional['%COBERTURA'].to_list() # Primer conjunto de datos
        y2 = df_cobertura_correcion_nacional['DESERCIÓN'].to_list()  # Segundo conjunto de datos
    else:
        y1 = df_cobertura_correcion_filtro['%COBERTURA'].to_list() # Primer conjunto de datos
        y2 = df_cobertura_correcion_filtro['DESERCIÓN'].to_list()  # Segundo conjunto de datos
    # Crear el gráfico
    fig, ax1 = plt.subplots(figsize=(6 , 3))

    # Primer eje Y
    ax1.plot(x, y1, 'g-', marker='o', label='Datos 1')  # Línea verde
    ax1.set_xlabel('Años')
    ax1.set_ylabel('% Cobertura', color='g')
    ax1.tick_params(axis='y', labelcolor='g')  # Color de los ticks del eje Y
    #ax1.set_ylim(43, 52)
    # Segundo eje Y
    ax2 = ax1.twinx()  # Crea un segundo eje Y que comparte el mismo eje X
    ax2.plot(x, y2, 'b-', marker='x', label='Datos 2')  # Línea azul
    ax2.set_ylabel('Deserción', color='b')
    ax2.tick_params(axis='y', labelcolor='b')  # Color de los ticks del eje Y
    #ax2.set_ylim(2.5, 4.5)
    # Título y leyenda
    plt.title('% Cobertura vs Deserción')
    fig.tight_layout()  # Ajustar layout para evitar solapamientos
    plt.grid()
    #plt.show()

    st.pyplot(plt,)


def cobertura_aprobacion():
    x = [2018, 2019, 2020, 2021, 2022, 2023]
    
    if select_departamento == 'Todos':
        y1 = df_cobertura_correcion_nacional['%COBERTURA'].to_list() # Primer conjunto de datos
        y2 = df_cobertura_correcion_nacional['APROBACIÓN'].to_list()  # Segundo conjunto de datos
    else:
        y1 = df_cobertura_correcion_filtro['%COBERTURA'].to_list() # Primer conjunto de datos
        y2 = df_cobertura_correcion_filtro['APROBACIÓN'].to_list()  # Segundo conjunto de datos
    

    # Crear el gráfico
    fig, ax1 = plt.subplots(figsize=(6, 3))

    # Primer eje Y
    ax1.plot(x, y1, 'g-', marker='o', label='Datos 1')  # Línea verde
    ax1.set_xlabel('Años')
    ax1.set_ylabel('% Cobertura', color='g')
    ax1.tick_params(axis='y', labelcolor='g')  # Color de los ticks del eje Y
    #ax1.set_ylim(43, 52)
    # Segundo eje Y
    ax2 = ax1.twinx()  # Crea un segundo eje Y que comparte el mismo eje X
    ax2.plot(x, y2, 'b-', marker='x', label='Datos 2')  # Línea azul
    ax2.set_ylabel('Aprobación', color='b')
    ax2.tick_params(axis='y', labelcolor='b')  # Color de los ticks del eje Y
    #ax2.set_ylim(89, 92)
    
    # Título y leyenda
    plt.title('% Cobertura vs Aprobación')
    fig.tight_layout()  # Ajustar layout para evitar solapamientos
    plt.grid()
    #plt.show()

    st.pyplot(plt,)


# Agregar contenido en las primeras columnas
col1, col2 = st.columns([4, 1])  # Ajusta las proporciones según necesites
with col1:
    tab1, tab2, tab3 = st.tabs(['Mapa','Relación','Datos'])
    with tab1:
        
        col1_mapa, col2_mapa, = st.columns([1,3])
        with col1_mapa:
            if select_departamento == 'Todos':
                desercion = round(df_AD_AÑOS.iloc[0]['DESERCIÓN'], 1)
                aprobacion = round(df_AD_AÑOS.iloc[0]['APROBACIÓN'], 1)
            else:
                desercion = round(df_AD_añosDepartamento.iloc[0]['DESERCIÓN'], 1)
                aprobacion = round(df_AD_añosDepartamento.iloc[0]['APROBACIÓN'], 1)

            
            def create_full_circle_pie(value, title, color):
                # Porcentaje a mostrar y el resto del círculo
                values = [value, 100 - value]
                
                # Crear gráfico tipo pie
                pie_chart = go.Figure(go.Pie(
                    values=values,
                    hole=0.7,  # Esto hace que el círculo sea un "donut"
                    marker_colors=[color, "#F0F0F0"],  # Color de la parte activa y del fondo
                    textinfo='none',  # No mostrar info de texto en los segmentos
                    direction='clockwise',
                    sort=False
                ))
                
                # Personalización del layout
                pie_chart.update_layout(
                    annotations=[dict(text=f'{value}%', x=0.5, y=0.5, font_size=36, showarrow=False, font_color="black")],
                    showlegend=False,
                    title={'text': title, 'font': {'size': 24, 'color': 'black'}, 'x': 0.5, 'xanchor': 'center'},
                    margin=dict(l=0, r=0, t=50, b=0),
                    paper_bgcolor="white",  # Fondo de la página en negro
                    plot_bgcolor="white",   # Fondo del gráfico en negro
                    height=300,  # Ajusta el tamaño del gráfico
                )
                
                return pie_chart
            st.markdown("""<br>""",unsafe_allow_html=True)
            # Crear gráficos
            gauge_inbound = create_full_circle_pie(aprobacion, "Aprobación", "green")
            gauge_outbound = create_full_circle_pie(desercion, "Deserción", "red")

            # Mostrar los gráficos
            st.plotly_chart(gauge_inbound, use_container_width=True)
            st.plotly_chart(gauge_outbound, use_container_width=True)

            
        with col2_mapa:
            mapa()       
    with tab2:
        cobertura_desercion()
        cobertura_aprobacion()

                








                
    with tab3:
        st.write(df_cobertura_municipio)

  
with col2:

    #condional que evaluea si selecciona Todos para que no filtre por departamento y el else por si escoje algún departamento
    if select_departamento == 'Todos':
        departamentoMunicipio='DEPARTAMENTO'
    else:
        top10_mejores = df_cobertura_municipio[df_cobertura_municipio['DEPARTAMENTO']==select_departamento].sort_values(by='%COBERTURA', ascending=False).head(5)
        top10_peores = df_cobertura_municipio[df_cobertura_municipio['DEPARTAMENTO']==select_departamento].sort_values(by='%COBERTURA', ascending=True).head(5)
        departamentoMunicipio='MUNICIPIO'
        
        
    st.markdown(""" <br> """, unsafe_allow_html=True)
    #Top 5 Mejores
    st.header("Cobertura fijo 2023")
    st.subheader("5 Mejores")
    #Grafico de barras
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(3, 2))
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    sns.set_color_codes("muted")
    sns.barplot(x="%COBERTURA", y=departamentoMunicipio, data=top10_mejores,color="b")
    # Add a legend and informative axis label
    ax.set(xlim=(0, 100), ylabel="",
        xlabel="Porcentaje  ")
    st.pyplot(plt)
    
    
    #Top 5 peores
    st.subheader("5 Peores")
    #Grafico de barras
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(3, 2))
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    # Load the example car crash dataset

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")
    sns.barplot(x="%COBERTURA", y=departamentoMunicipio, data=top10_peores,
                 color="b")
    # Add a legend and informative axis label
    ax.set(xlim=(0, 20), ylabel="",
        xlabel="Porcentaje  ")
    st.pyplot(plt)
    
st.markdown("---")   

