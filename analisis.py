import pandas as pd 
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

    
#----------------------------------------------------------------------------------------------------------------
#Inicio seccion internet Fijo

@st.cache_data
def cargar_coberturaFijo():
    data = pd.read_csv(r'C:\Users\Usuario\Desktop\Proyecto Analisis Datos\coberturainternetfijo.csv')
    return data

df_coberturaFijo = cargar_coberturaFijo()

st.title('Puntos de Acceso Internet Fijo por Municipio 2023-3')
ultimo_año = df_coberturaFijo['AÑO'].max() #Encontrar el ultimo año del csv
ultimo_trimestre = df_coberturaFijo[df_coberturaFijo['AÑO'] == ultimo_año]['TRIMESTRE'].max()  # encontrar ultimo trimestre del ultimo año
df_filtrado = df_coberturaFijo[(df_coberturaFijo['AÑO'] == ultimo_año) & (df_coberturaFijo['TRIMESTRE'] == ultimo_trimestre)] #filtrar archivo
cobertura_por_departamento = df_filtrado.groupby('DEPARTAMENTO')['No. ACCESOS FIJOS A INTERNET'].sum() #nueva tabla por departamentos y cantidad de accesos
poblacion_por_departamento = df_filtrado.groupby('DEPARTAMENTO')['POBLACIÓN DANE'].max()#nueva tabla por habitantes y departamentos
df_resultado = pd.merge(cobertura_por_departamento, poblacion_por_departamento, on='DEPARTAMENTO', how='left') #unir ambas tablas
df_resultado['% COBERTURA']=(((df_resultado['No. ACCESOS FIJOS A INTERNET']/df_resultado['POBLACIÓN DANE'])*100).round(0)).astype(str) + '%' #Calculo para encontrar porcentaje de cobertura, redondeado y con estilo de porcenaje
df_resultado_ordenado = df_resultado.sort_values(['No. ACCESOS FIJOS A INTERNET'], ascending=False).reset_index()
st.write(df_resultado_ordenado) #mostrar en la web

#Grafico Cantidad x Departamento
plt.figure(figsize=(10, 6))
sns.barplot(x='No. ACCESOS FIJOS A INTERNET',y='DEPARTAMENTO', data=df_resultado_ordenado, palette='viridis')

# Etiquetas y título
plt.ylabel('Departamentos')
plt.xlabel('Cantidad')
plt.title('Número de Accesos Fijos a Internet por Departamento')
plt.xticks(rotation=45)
plt.tight_layout()# Ajustar el diseño para evitar recortes
plt.xlim(0,2300000)
st.pyplot(plt)

# Filtrar datos por año y trimestre
df_filtrado = df_coberturaFijo[
    ((df_coberturaFijo['AÑO'] < 2023) & (df_coberturaFijo['TRIMESTRE'] == 4)) | 
    ((df_coberturaFijo['AÑO'] == 2023) & (df_coberturaFijo['TRIMESTRE'] == 3))
]

df_filtrado_año = df_filtrado.groupby(['AÑO'])['No. ACCESOS FIJOS A INTERNET'].sum().reset_index()
st.write(df_filtrado_año)


#Grafico Crecimiento por año
plt.figure(figsize=(10, 6))
sns.lineplot(x='AÑO', y='No. ACCESOS FIJOS A INTERNET', data=df_filtrado_año, palette='viridis')

# Etiquetas y título
plt.ylabel('Cantidad')
plt.xlabel('Año')
plt.title('Número de Accesos Fijos a Internet por Año')
plt.xticks(rotation=45)
plt.tight_layout()# Ajustar el diseño para evitar recortes
plt.ylim(5000000,9000000)
st.pyplot(plt)

#Fin seccion internet Fijo
#----------------------------------------------------------------------------------------------------------------


## Inicio Seccion internet Movil
#----------------------------------------------------------------------------------------------------------------
@st.cache_data
def cargar_coberturaMovil():
    data = pd.read_csv(r'C:\Users\Usuario\Desktop\Proyecto Analisis Datos\coberturamovil.csv')
    return data

df_coberturaMovil = cargar_coberturaMovil()

st.title('Cobertura Internet Movil por Municipio')
st.write(df_coberturaMovil)

# Filtrar datos por año y trimestre cobertura movil
df_coberturaMovil[['COBERTURA 2G', 'COBERTURA 3G', 'COBERTURA HSPA+, HSPA+DC', 'COBERTUTA 4G', 'COBERTURA LTE', 'COBERTURA 5G']] = df_coberturaMovil[['COBERTURA 2G', 'COBERTURA 3G', 'COBERTURA HSPA+, HSPA+DC', 'COBERTUTA 4G', 'COBERTURA LTE', 'COBERTURA 5G']].replace({'S': 1, 'N': 0})

df_filtrado = df_coberturaMovil[
    ((df_coberturaMovil['AÑO'] < 2023) & (df_coberturaMovil['TRIMESTRE'] == 4)) | 
    ((df_coberturaMovil['AÑO'] == 2023) & (df_coberturaMovil['TRIMESTRE'] == 3))
]
df_filtrado_año_cobertura = df_filtrado.groupby(['AÑO'])[['COBERTURA 2G','COBERTURA 3G','COBERTURA HSPA+, HSPA+DC','COBERTUTA 4G','COBERTURA LTE','COBERTURA 5G']].sum().reset_index()
st.write(df_filtrado_año_cobertura)

# Transformando el DataFrame para usar seaborn
df_consolidado_coberturaAño = df_filtrado_año_cobertura.melt(id_vars='AÑO', 
                                     value_vars=['COBERTURA 2G', 'COBERTURA 3G', 
                                                 'COBERTURA HSPA+, HSPA+DC', 'COBERTUTA 4G', 
                                                 'COBERTURA LTE', 'COBERTURA 5G'], 
                                     var_name='Cobertura', value_name='Valor')
df_consolidado_coberturaAño['Valor'] = df_consolidado_coberturaAño['Valor'].astype(int)
st.write(df_consolidado_coberturaAño)
# Configurando el gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_consolidado_coberturaAño, x='AÑO', y='Valor', hue='Cobertura', marker='o', palette='viridis')

plt.ylim(0,10500)
plt.title('Cobertura de Servicios Móviles por Año')
plt.xlabel('Año')
plt.ylabel('Cobertura')

plt.xticks(df_consolidado_coberturaAño['AÑO'].unique())
plt.grid()
plt.tight_layout()
st.pyplot(plt)



#Fin seccion internet Movil
#----------------------------------------------------------------------------------------------------------------

## Inicio Seccion educacion
#----------------------------------------------------------------------------------------------------------------
@st.cache_data
def cargar_coberturaEducacion():
    data = pd.read_csv(r'C:\Users\Usuario\Desktop\Proyecto Analisis Datos\educacion.csv')
    return data

df_coberturaEducacion = cargar_coberturaEducacion()

st.title('Cobertura Educacion por Municipio')
st.write(df_coberturaEducacion)

df_educacion_departamento = (df_coberturaEducacion.groupby(['DEPARTAMENTO'])[['COBERTURA_NETA','CÓDIGO_DEPARTAMENTO']].mean()).round(0)
st.write(df_educacion_departamento)

#Grafico % de cobertura por departamento
plt.figure(figsize=(10, 6))
sns.barplot(x='COBERTURA_NETA',y='DEPARTAMENTO', data=df_educacion_departamento.sort_values(['COBERTURA_NETA'], ascending=False), palette='viridis')
plt.ylabel('Departamentos')
plt.xlabel('% Cobertura Neta')
plt.title('Cobertura Neta por Departamento')
plt.xticks(rotation=45)
plt.tight_layout()
plt.xlim(50,100)
st.pyplot(plt)

df_educacion_año = (df_coberturaEducacion.groupby(['AÑO'])['COBERTURA_NETA'].mean()).round(0).reset_index()
st.write(df_educacion_año)


#Grafico cobertura neta por año
plt.figure(figsize=(10, 6))
sns.lineplot(x='AÑO', y='COBERTURA_NETA', data=df_educacion_año, palette='viridis')


plt.ylabel('Cantidad')
plt.xlabel('Año')
plt.title('Porcentaje cobertura neta por año')
plt.xticks(rotation=45)
plt.tight_layout()# Ajustar el diseño para evitar recortes
plt.ylim(70,100)
plt.grid()
plt.tight_layout()
st.pyplot(plt)

#Fin seccion educacion
#----------------------------------------------------------------------------------------------------------------



## Inicio Unir las 3 bases de datos
#----------------------------------------------------------------------------------------------------------------

df_resultado_ordenado['COD DEPARTAMENTO']= df_coberturaFijo['COD_DEPARTAMENTO']#internet fijo

df_coberturaMovil_departamento = df_coberturaMovil.groupby(['DEPARTAMENTO'])[['COBERTURA 2G','COBERTURA 3G','COBERTURA HSPA+, HSPA+DC','COBERTUTA 4G','COBERTURA LTE','COBERTURA 5G']].sum().reset_index()

df_movil_fijo = pd.merge(df_resultado_ordenado, df_coberturaMovil_departamento, on='DEPARTAMENTO', how='inner')

df_consolidado = pd.merge(df_movil_fijo, df_educacion_departamento,   
                          left_on='COD DEPARTAMENTO',
                          right_on='CÓDIGO_DEPARTAMENTO',
                          how='inner')

st.write(df_consolidado)





#Fin Unir las 3 bases de datos
#----------------------------------------------------------------------------------------------------------------