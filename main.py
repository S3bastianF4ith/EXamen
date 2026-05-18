import math

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de página simple, sin diseño especial

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


def plot_relative_frequency(table, title, chart_type):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"} if chart_type == "Polar" else {})
    labels = table["Categoría"].tolist()
    sizes = table["Frecuencia relativa"].tolist()

    if chart_type == "Pastel":
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, wedgeprops={"edgecolor": "white"})
        ax.axis("equal")
        ax.set_title(title)
    else:
        angles = [i * 2 * math.pi / len(sizes) for i in range(len(sizes))]
        bars = ax.bar(angles, sizes, width=2 * math.pi / len(sizes), bottom=0.0, color="#ff7f0e", alpha=0.8)
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylim(0, max(sizes) * 1.15)
        ax.set_title(title, pad=20)

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
    st.title("Análisis feo de frecuencias")
    st.write("Esta app usa `winequalityN.csv` para hacer cálculos de frecuencias y gráficos sin muchas florituras.")

    df = load_data()

    st.write("Descripción:")
    st.write("El dataset tiene vinos y sus características químicas y de calidad.")
    st.write("Se muestran frecuencias absolutas, relativas, acumuladas y polígono de frecuencias.")

    column = st.selectbox("Seleccione una variable", df.columns.tolist(), index=df.columns.get_loc("quality") if "quality" in df.columns else 0)
    chart_type = st.radio("Tipo de gráfico relativo", ["Pastel", "Polar"])
    bins = st.slider("Número de intervalos (variables numéricas)", min_value=4, max_value=15, value=8)
    show_data = st.checkbox("Mostrar datos crudos")

    if show_data:
        st.subheader("Vista preliminar de los datos")
        st.dataframe(df.head(20))

    st.subheader(f"Análisis de la variable: {column}")

    series = df[column].dropna()
    is_numeric = pd.api.types.is_numeric_dtype(series)

    if is_numeric:
        st.markdown(
            "La variable seleccionada es numérica. Se agrupa en intervalos para calcular la distribución de frecuencias."
        )
        freq_table = build_frequency_table(series, bins=bins)
    else:
        st.markdown(
            "La variable seleccionada es categórica. Se calcula la distribución de frecuencias por categoría."
        )
        freq_table = build_frequency_table(series)

    st.markdown("### Tabla de frecuencias")
    st.dataframe(freq_table)

    st.write("### Estadísticas descriptivas")
    if is_numeric:
        stats = numeric_statistics(series)
    else:
        stats = categorical_statistics(series)
    stats_df = pd.DataFrame.from_dict(stats, orient="index", columns=["Valor"])
    st.table(stats_df)

    st.write("#### Frecuencias absolutas")
    st.pyplot(plot_absolute_frequency(freq_table, "Frecuencia absoluta"))

    st.write("#### Frecuencias relativas")
    st.pyplot(plot_relative_frequency(freq_table, "Frecuencia relativa", chart_type))

    st.write("#### Frecuencia acumulada")
    st.pyplot(plot_cumulative_frequency(freq_table, "Frecuencia acumulada"))

    st.write("#### Polígono de frecuencias")
    st.pyplot(plot_frequency_polygon(freq_table, "Polígono de frecuencias"))
if __name__ == "__main__":
    main()

