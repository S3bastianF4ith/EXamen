import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-darkgrid")
@st.cache_data
def load_data():
    return pd.read_csv("winequalityN.csv")
@st.cache_data
def build_frequency_table(series, bins=None):
    if pd.api.types.is_numeric_dtype(series):
        if bins is None:
            bins = 8
        categories = pd.cut(series, bins=bins, include_lowest=True)
        counts = categories.value_counts(sort=False)
        index = counts.index.astype(str)
    else:
        counts = series.value_counts(sort=False)
        index = counts.index.astype(str)
    absolute = counts.astype(int)
    relative = absolute / absolute.sum()
    cumulative = absolute.cumsum()
    percent = relative * 100
    table = pd.DataFrame(
        {
            "Categoría": index,
            "Frecuencia absoluta": absolute.values,
            "Frecuencia relativa": relative.values,
            "Porcentaje": percent.values,
            "Frecuencia acumulada": cumulative.values,
        }
    )
    return table
@st.cache_data
def numeric_statistics(series):
    return {
        "Media": series.mean(),
        "Mediana": series.median(),
        "Moda": series.mode().iloc[0] if not series.mode().empty else float("nan"),
        "Mínimo": series.min(),
        "Máximo": series.max(),
        "Desviación estándar": series.std(ddof=1),
    }
@st.cache_data
def categorical_statistics(series):
    mode = series.mode()
    return {
        "Moda": mode.iloc[0] if not mode.empty else "N/A",
        "Número de categorías": series.nunique(),
        "Registro más frecuente": series.value_counts().idxmax(),
    }
def plot_absolute_frequency(table, title):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(table["Categoría"], table["Frecuencia absoluta"], color="#1f77b4")
    ax.set_title(title)
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Frecuencia absoluta")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig
def plot_relative_frequency(table, title):
    fig, ax = plt.subplots(figsize=(6, 6))
    labels = table["Categoría"].tolist()
    sizes = table["Frecuencia relativa"].tolist()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, wedgeprops={"edgecolor": "white"})
    ax.axis("equal")
    ax.set_title(title)
    plt.tight_layout()
    return fig
def plot_cumulative_frequency(table, title):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(table["Categoría"], table["Frecuencia acumulada"], marker="o", color="#2ca02c")
    ax.set_title(title)
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Frecuencia acumulada")
    ax.tick_params(axis="x", rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return fig
def plot_frequency_polygon(table, title):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(table["Categoría"], table["Frecuencia absoluta"], marker="o", linestyle="-", color="#d62728")
    ax.fill_between(table["Categoría"], table["Frecuencia absoluta"], alpha=0.15, color="#d62728")
    ax.set_title(title)
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Frecuencia absoluta")
    ax.tick_params(axis="x", rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return fig
def main():
    st.title("Análisis de frecuencias")
    st.write("Selecciona una variable y mira las tablas y gráficos con este CSV.")
    df = load_data()
    column = st.selectbox(
        "Variable:",
        df.columns.tolist(),
        index=df.columns.get_loc("quality") if "quality" in df.columns else 0,
    )
    bins = st.slider("Intervalos (numérico):", min_value=4, max_value=15, value=8)
    show_data = st.checkbox("Mostrar algunos datos")
    if show_data:
        st.dataframe(df.head(20))
    series = df[column].dropna()
    is_numeric = pd.api.types.is_numeric_dtype(series)
    if is_numeric:
        freq_table = build_frequency_table(series, bins=bins)
    else:
        freq_table = build_frequency_table(series)
    st.write("### Tabla de frecuencias")
    st.table(freq_table)
    st.write("### Estadísticas")
    if is_numeric:
        stats = numeric_statistics(series)
    else:
        stats = categorical_statistics(series)
        
    stats_df = pd.DataFrame.from_dict(stats, orient="index", columns=["Valor"])
    st.table(stats_df)
    st.write("#### Frecuencias absolutas")
    st.pyplot(plot_absolute_frequency(freq_table, "Frecuencia absoluta"))
    st.write("#### Frecuencias relativas")
    st.pyplot(plot_relative_frequency(freq_table, "Frecuencia relativa"))
    st.write("#### Frecuencia acumulada")
    st.pyplot(plot_cumulative_frequency(freq_table, "Frecuencia acumulada"))
    st.write("#### Polígono de frecuencias")
    st.pyplot(plot_frequency_polygon(freq_table, "Polígono de frecuencias"))
    
if __name__ == "__main__":
    main()
#odio mi vida odio a mi jefe llamado ian salven a simon
