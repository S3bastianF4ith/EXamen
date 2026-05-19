import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#explico aqui como decidi usar streamlit, me ahorro la interfaz grafica fea porque esta cosa lo hace solo
#segundo y es que si en el hipotetico caso la pagina no jala solo dele volver a activar y listo
plt.style.use("seaborn-v0_8-darkgrid")
@st.cache_data
def cargar_datos():
    return pd.read_csv("winequalityN.csv")
@st.cache_data
def construir_tabla_frecuencias(serie, intervalos=None):
    if pd.api.types.is_numeric_dtype(serie):
        if intervalos is None:
            intervalos = 8
        categorias = pd.cut(serie, bins=intervalos, include_lowest=True)
        conteos = categorias.value_counts(sort=False)
        index = conteos.index.astype(str)
    else:
        conteos = serie.value_counts(sort=False)
        index = conteos.index.astype(str)
    absoluto = conteos.astype(int)
    relativo = absoluto / absoluto.sum()
    acumulado = absoluto.cumsum()
    porcentaje = relativo * 100
    table = pd.DataFrame(
        {
            "Categoría": index,
            "Frecuencia absoluta": absoluto.values,
            "Frecuencia relativa": relativo.values,
            "Porcentaje": porcentaje.values,
            "Frecuencia acumulada": acumulado.values,
        }
    )
    return table
@st.cache_data
def estadisticas_numericas(serie):
    return {
        "Media": serie.mean(),
        "Mediana": serie.median(),
        "Moda": serie.mode().iloc[0],
        "Mínimo": serie.min(),
        "Máximo": serie.max(),
        "Desviación estándar": serie.std(ddof=1),
    }
@st.cache_data
def estadisticas_categoricas(serie):
    moda = serie.mode()
    return {
        "Moda": moda.iloc[0] if not moda.empty else "N/A",
        "Número de categorías": serie.nunique(),
        "Registro más frecuente": serie.value_counts().idxmax(),
    }
def graficar_frecuencia_absoluta(tabla, titulo):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(tabla["Categoría"], tabla["Frecuencia absoluta"], color="#1f77b4")
    ax.set_title(titulo)
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Frecuencia absoluta")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig
def graficar_frecuencia_relativa(tabla, titulo):
    fig, ax = plt.subplots(figsize=(6, 6))
    labels = tabla["Categoría"].tolist()
    sizes = tabla["Frecuencia relativa"].tolist()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, wedgeprops={"edgecolor": "white"})
    ax.axis("equal")
    ax.set_title(titulo)
    plt.tight_layout()
    return fig
def graficar_frecuencia_acumulada(tabla, titulo):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(tabla["Categoría"], tabla["Frecuencia acumulada"], marker="o", color="#2ca02c")
    ax.set_title(titulo)
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Frecuencia acumulada")
    ax.tick_params(axis="x", rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return fig
def graficar_poligono_frecuencias(tabla, titulo):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(tabla["Categoría"], tabla["Frecuencia absoluta"], marker="o", linestyle="-", color="#d62728")
    ax.fill_between(tabla["Categoría"], tabla["Frecuencia absoluta"], alpha=0.15, color="#d62728")
    ax.set_title(titulo)
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Frecuencia absoluta")
    ax.tick_params(axis="x", rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return fig
def main():
    st.title("Análisis de frecuencias")
    st.write("Profa no me mate es la primera vez que uso esta cosa de Streamlit")
    datos = cargar_datos()
    columna = st.selectbox("Elige una variable.", datos.columns.tolist())
    intervalos = st.slider("Intervalos (numérico):", min_value=4, max_value=15, value=8)
    mostrar_datos = st.checkbox("Mostrar datos (solo los primeros 10 registros)")
    if mostrar_datos:
        st.dataframe(datos.head(10))
    serie = datos[columna].dropna()
    es_numerico = pd.api.types.is_numeric_dtype(serie)
    if es_numerico:
        tabla_frecuencias = construir_tabla_frecuencias(serie, intervalos=intervalos)
    else:
        tabla_frecuencias = construir_tabla_frecuencias(serie)
    st.write("Tabla de frecuencias:")
    st.table(tabla_frecuencias)
    st.write("Estadísticas:")
    if es_numerico:
        estadisticas = estadisticas_numericas(serie)
    else:
        estadisticas = estadisticas_categoricas(serie)
    tabla_estadisticas = pd.DataFrame.from_dict(estadisticas, orient="index", columns=["Valor"])
    st.table(tabla_estadisticas)
    st.pyplot(graficar_frecuencia_absoluta(tabla_frecuencias, "Frecuencia absoluta"))
    st.pyplot(graficar_frecuencia_relativa(tabla_frecuencias, "Frecuencia relativa"))
    st.pyplot(graficar_frecuencia_acumulada(tabla_frecuencias, "Frecuencia acumulada"))
    st.pyplot(graficar_poligono_frecuencias(tabla_frecuencias, "Polígono de frecuencias"))
    
if __name__ == "__main__":
    main()
#olvidelo al final es streamlit no estaba tan feo 
#odio mi vida odio a mi jefe llamado ian salven a simon
