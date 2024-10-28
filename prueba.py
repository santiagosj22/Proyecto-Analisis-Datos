import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

# Configuración inicial
st.set_page_config(layout="wide", page_title="US Population Dashboard")

# Sidebar para seleccionar el año y el tema de color
st.sidebar.title("🧮 US Population Dashboard")
year = st.sidebar.selectbox("Select a year", [2019, 2018, 2017, 2016])  # Puedes agregar más años
color_theme = st.sidebar.selectbox("Select a color theme", ['Blues', 'Reds', 'Greens'])

# Datos de ejemplo (reemplazar con tu DataFrame)
data = {
    'state': ['Texas', 'New York', 'California', 'Florida', 'Pennsylvania'],
    'population': [29000000, 19500000, 39500000, 21500000, 13000000],
    'inbound': [0.23, 0.12, 0.17, 0.19, 0.15],
    'outbound': [0.04, 0.08, 0.07, 0.06, 0.05],
    'gains_losses': [367000, -77000, 50000, 30000, -25000],
    'lat': [31.9686, 40.7128, 36.7783, 27.9944, 41.2033],
    'lon': [-99.9018, -74.0060, -119.4179, -81.7603, -77.1945]
}
df = pd.DataFrame(data)

# Mapa de población por estado
st.subheader(f"Total Population for {year}")
view_state = pdk.ViewState(latitude=37.0902, longitude=-95.7129, zoom=3.5, pitch=50)
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',  # Color rojo con algo de transparencia
    get_radius=50000,  # Ajustar el radio
    pickable=True
)
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(r)

# Gráfico de ganancias/pérdidas
st.subheader("Gains/Losses")
fig = px.bar(df, x='state', y='gains_losses', color='gains_losses', color_continuous_scale=color_theme.lower())
st.plotly_chart(fig, use_container_width=True)

# Gráfico de migración (entrante/saliente)
st.subheader("States Migration")
col1, col2 = st.columns(2)
with col1:
    st.metric("Inbound", f"{df['inbound'].mean()*100:.0f}%", delta=f"{df['inbound'].sum()*100:.0f}%")
with col2:
    st.metric("Outbound", f"{df['outbound'].mean()*100:.0f}%", delta=f"{df['outbound'].sum()*100:.0f}%")

# Gráfico de barra horizontal para los estados con mayor población
st.subheader("Top States")
fig2 = px.bar(df.sort_values(by="population", ascending=False), x='population', y='state', orientation='h', color='population', color_continuous_scale=color_theme.lower())
st.plotly_chart(fig2, use_container_width=True)

# Sección de información y fuentes
st.sidebar.markdown("""


""")
