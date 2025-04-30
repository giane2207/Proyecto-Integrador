import streamlit as st

st.set_page_config(
    page_title="Encuest-AR",
    page_icon="📈",
    layout="wide"
)

# Título de la aplicación
st.title("Encuest-AR")

# Párrafo explicativo sobre la EPH
st.markdown(
    """
    ## ¿Qué es la Encuesta Permanente de Hogares (EPH)?
    
    La **Encuesta Permanente de Hogares (EPH)** es un estudio estadístico realizado por el **Instituto Nacional de Estadística y Censos (INDEC)** de Argentina, que proporciona información sobre las características socioeconómicas de los hogares y la población en diversas regiones del país. 
    
    La EPH abarca temas como la situación laboral, los ingresos, la educación, y otros aspectos clave para analizar el bienestar y las condiciones de vida de los habitantes de Argentina.
    
    En esta aplicación podrás acceder a los datos más recientes de la EPH, explorar estadísticas por tema, y visualizar los resultados de manera interactiva.
    """
)

