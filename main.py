import streamlit as st
import pandas as pd
import numpy as np
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pytz
import time
import boto3
from datetime import datetime
import pandas as pd
from io import BytesIO
import plotly.graph_objects as go
st.set_page_config(page_title="Chatbot Dashboard", page_icon="./img/logo_pernexium.png", layout="wide")



META_PRICE = 0.0432 * 17
num2curr = lambda num: "${:,.2f}".format(num)

@st.cache_data
def get_from_aws():
    session = boto3.Session(
        aws_access_key_id = st.secrets["aws_access_key_id"],
        aws_secret_access_key = st.secrets["aws_secret_access_key"]
    )

    s3 = session.client('s3')
    bucket = 's3-pernexium-report'

    # Especifica el nombre del bucket y la clave del archivo
    file_key = 'bancoppel/reportes/chatbot/2024_07/2024_07_08_chatbot_reporte.xlsx'

    # Descarga el archivo desde S3
    response = s3.get_object(Bucket=bucket, Key=file_key)
    file_content = response['Body'].read()

    # Carga el contenido del archivo en un DataFrame de Pandas
    file_data = BytesIO(file_content)
    data = pd.read_excel(file_data)
    return data

data = get_from_aws()

with st.sidebar:
    page = st.selectbox(
    'Selecciona la página',
    ('Dashboard',))
    
    col1, col2 = st.columns(2)
    with col1:
        st.image('./img/PXM Logotipo 2.png', use_column_width=True)
    with col2:
        st.image('./img/doit_logo.png', width = 150)
    
if page == 'Dashboard':
    
    st.header("Dashboard Chatbot")
    
    col1, col2 = st.columns(2)
    
    with col1:
        categoria = st.selectbox('Selecciona una campaña', options=['BanCoppel', 'Monte de Piedad'])

    # Date picker para seleccionar rango de fechas
    with col2:
        col1_, col2_ = st.columns(2)
        with col1_:
            start_date = st.date_input('Desde')
            
        with col2_:
            end_date = st.date_input('Hasta')
    
    # Indicadores
    detonaciones_enviadas_periodo = 8_052#data.detonaciones_enviadas_periodo.sum()
    eficiencia = 0.134#data.total_respuestas_periodo.sum() / detonaciones_enviadas_periodo
    
    col1, col2, col3, col4 = st.columns(4)
    
    
    col1.metric("Mensajes enviados", str(detonaciones_enviadas_periodo), 40)
        
    col2.metric("Eficiencia", f"{eficiencia*100:.2f}%", "2.1%")
    
    col3.metric("Gasto meta", num2curr(META_PRICE*detonaciones_enviadas_periodo))
    
    col4.metric("Recuperación", num2curr(345028))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        categories = ["no define", "negativa de pago", "carta convenio", "próximo pago", "no reconoce"]
        values = [2000, 1500, 1200, 1800, 1552]  # Asegúrate de que sumen 8052

        # Crear el gráfico de barras
        fig = go.Figure(data=[
            go.Bar(name='Categorías', x=categories, y=values)
        ])

        # Configurar el diseño del gráfico
        fig.update_layout(
            title='Distribución de Categorías',
            xaxis_title='Categorías',
            yaxis_title='Valores',
            yaxis=dict(tickformat=',d'),  # Formato de los valores en el eje Y para mostrar como enteros
               autosize=False,
            width=550,  # Ajusta el ancho según lo necesites
            height=400,
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
        
    with col2:


        # Definir los días del mes de julio del 1 al 10
        days = list(range(1, 11))

        # Datos de ejemplo para las cantidades de respuestas y mensajes enviados
        # Asegúrate de que la suma de las cantidades corresponda a los valores requeridos
        np.random.seed(42)  # Para reproducibilidad

        # Generar respuestas que sumen 1079 con variaciones
        responses = np.random.randint(50, 160, size=10)
        responses = responses / responses.sum() * 1079
        responses = np.round(responses).astype(int)

        # Generar mensajes enviados que sumen 8052 con variaciones
        messages_sent = np.random.randint(900, 1200, size=10)
        messages_sent = messages_sent / messages_sent.sum() * 8052
        messages_sent = np.round(messages_sent).astype(int)

        # Crear el gráfico de líneas
        fig = go.Figure()

        # Añadir la línea de cantidad de respuestas
        fig.add_trace(go.Scatter(x=days, y=responses, mode='lines+markers', name='Cantidad de Respuestas'))

        # Añadir la línea de cantidad de mensajes enviados
        fig.add_trace(go.Scatter(x=days, y=messages_sent, mode='lines+markers', name='Cantidad de Mensajes Enviados'))

        # Configurar el diseño del gráfico
        fig.update_layout(
            title='Cantidad de Respuestas y Mensajes Enviados (1 al 10 de Julio)',
            xaxis_title='Días de Julio',
            yaxis_title='Cantidad',
            xaxis=dict(tickmode='linear'),
            yaxis=dict(tickformat=',d'),  # Formato de los valores en el eje Y para mostrar como enteros
            autosize=False,
            width=600,  # Ajusta el ancho según lo necesites
            height=400,
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)


    
    
    st.divider()
    
    st.subheader("Sobre la temporalidad")
    
    col1, col2 = st.columns(2)

    with col1:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = [f"{h}:00" for h in range(7, 22)]  # De 7 AM a 9 PM

        # Generar datos aleatorios para el mapa de calor (para el ejemplo)
        data = np.random.rand(len(hours), len(days))*500

        # Crear el mapa de calor
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=days,
            y=hours,
            colorscale='gray',
            colorbar=dict(title='Envíos')
        ))

        # Configurar el diseño del gráfico
        fig.update_layout(
            title='Envíos por día',
            xaxis_title='Días de la Semana',
            yaxis_title='Horas del Día',
            autosize=False,
            width=600,  # Ajusta el ancho según lo necesites
            height=400,
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
        
    with col2:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = [f"{h}:00" for h in range(7, 22)]  # De 7 AM a 9 PM

        # Generar datos aleatorios para el mapa de calor (para el ejemplo)
        data = np.random.rand(len(hours), len(days))*100

        # Crear el mapa de calor
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=days,
            y=hours,
            colorscale='gray',
            colorbar=dict(title='Respuestas')
        ))

        # Configurar el diseño del gráfico
        fig.update_layout(
            title='Respuestas por día',
            xaxis_title='Días de la Semana',
            yaxis_title='Horas del Día',
            
            width=600,  # Ajusta el ancho según lo necesites
            height=400,
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
        
        
        
    st.divider()
    
    st.subheader("Sobre los envíos")
    
    col1, col2 = st.columns(2)
    with col1:
    


        # Definir palabras típicas de la cobranza y sus frecuencias
        word_freq = {
            "pagar": 100,
            "quiero": 90,
            "descuento": 80,
            "no quiero": 70,
            "me interesa": 60,
            "oferta": 50,
            "cuota": 40,
            "deuda": 30,
            "crédito": 20,
            "cuenta": 10,
            "saldo": 15,
            "acuerdo": 25,
            "fecha límite": 35,
            "recordatorio": 45,
            "plazo": 55
        }

        # Crear la nube de palabras
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

        # Mostrar la nube de palabras usando Matplotlib
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        plt.title("Conversaciones chatbot")
        ax.axis('off')

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        
        
    with col2:

        # Definir las categorías y sus valores
        categories = ["descuento_50", "descuento_60", "descuento_50", "descuento_general", "ultima_oportunidad"]
        values = [1500, 2500, 1500, 2000, 552]  # Asegúrate de que sumen 8,052

        # Crear el gráfico de pastel
        fig = go.Figure(data=[go.Pie(labels=categories, values=values, hole=.3)])

        # Configurar el diseño del gráfico
        fig.update_layout(
            title='Distribución templates enviados',
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)




