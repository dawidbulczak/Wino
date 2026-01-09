import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ======================
# KONFIGURACJA STRONY
# ======================
st.set_page_config(
    page_title="🍷 Wine Analytics",
    layout="wide"
)

# ======================
# ŁADOWANIE DANYCH
# ======================
@st.cache_data
def load_wine_quality():
    return pd.read_csv("data/winequality-red.csv")

@st.cache_data
def load_food_pairings():
    return pd.read_csv("data/wine_food_pairings.csv")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("🍷 Wine Analytics")
dataset = st.sidebar.radio(
    "Wybierz analizę:",
    ["Jakość czerwonego wina", "Wine & Food Pairing"]
)

# ======================
# DASHBOARD 1: JAKOŚĆ WINA
# ======================
def wine_quality_dashboard():
    df = load_wine_quality()

    st.title("🍷 Analiza jakości czerwonego wina")

    st.subheader("📄 Podgląd danych")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rozkład jakości wina")
        fig = px.histogram(df, x="quality", nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Alkohol vs jakość")
        fig = px.box(df, x="quality", y="alcohol")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Korelacje cech chemicznych")
    corr = df.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False, ax=ax)
    st.pyplot(fig)

    st.subheader("🔍 Analiza cechy vs jakość")
    feature = st.selectbox(
        "Wybierz cechę:",
        [col for col in df.columns if col != "quality"]
    )

    fig = px.scatter(
        df,
        x=feature,
        y="quality",
        trendline="ols",
        opacity=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Statystyki opisowe")
    st.dataframe(df.describe())

# ======================
# DASHBOARD 2: FOOD PAIRING
# ======================
def food_pairing_dashboard():
    df = load_food_pairings()

    st.title("🍽️ Wine & Food Pairing Analysis")

    st.subheader("📄 Podgląd danych")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rozkład jakości dopasowania")
        fig = px.histogram(df, x="pairing_quality", nbins=5)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Typ wina vs jakość")
        fig = px.box(
            df,
            x="wine_type",
            y="pairing_quality"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌍 Kuchnia a średnia jakość pairingów")
    cuisine_avg = (
        df.groupby("cuisine")["pairing_quality"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        cuisine_avg.head(15),
        x="cuisine",
        y="pairing_quality"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎯 Interaktywny filtr")
    col3, col4 = st.columns(2)

    with col3:
        wine_type = st.selectbox(
            "Typ wina:",
            df["wine_type"].unique()
        )

    with col4:
        cuisine = st.selectbox(
            "Kuchnia:",
            df["cuisine"].unique()
        )

    filtered = df[
        (df["wine_type"] == wine_type) &
        (df["cuisine"] == cuisine)
    ]

    st.write(f"Liczba rekordów: **{len(filtered)}**")
    st.dataframe(filtered.sample(min(10, len(filtered))))

# ======================
# ROUTING
# ======================
if dataset == "Jakość czerwonego wina":
    wine_quality_dashboard()
else:
    food_pairing_dashboard()
