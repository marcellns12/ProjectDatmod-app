import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Taarifa Waterpoints Dashboard", layout="wide")

st.title("🌍 Taarifa Waterpoints Dashboard - Tanzania")
st.write("Visualisasi data prediksi status waterpoint berdasarkan lokasi dan region.")

uploaded_file = st.file_uploader("📂 Upload Data Test CSV (harus ada kolom region, latitude, longitude, status_group)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_columns = {"region", "latitude", "longitude", "status_group"}
    if not required_columns.issubset(df.columns):
        st.error(f"File CSV harus mengandung kolom: {required_columns}")
    else:
        st.success("✅ Data berhasil dimuat")

        st.subheader("🧾 Data Preview")
        st.dataframe(df.head())

        st.subheader("📊 Ringkasan Status Group")
        summary = df.groupby(["region", "status_group"]).size().reset_index(name="count")
        st.dataframe(summary)

        st.subheader("🗺️ Peta Interaktif Waterpoints")

        map_center = [df["latitude"].mean(), df["longitude"].mean()]
        m = folium.Map(location=map_center, zoom_start=6)

        # Mapping warna berdasarkan nilai numerik di kolom status_group
        color_dict = {
            0.0: "green",   # functional
            1.0: "orange",  # functional needs repair
            2.0: "red"      # non functional
        }

        for _, row in df.iterrows():
            status_val = row["status_group"]
            color = color_dict.get(status_val, "gray")  # default warna abu-abu kalau nilai tidak ada di dict

            folium.CircleMarker(
                location=(row["latitude"], row["longitude"]),
                radius=5,
                popup=f"Region: {row['region']}<br>Status Group: {status_val}",
                color=color,
                fill=True,
                fill_opacity=0.7
            ).add_to(m)

        st_folium(m, width=900, height=500)
