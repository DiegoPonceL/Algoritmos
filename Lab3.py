import streamlit as st
import pandas as pd

st.title("Laboratorio 2 - Análisis de Datos")

menu = st.selectbox("Selecciona dataset", [
    "Vehiculos", "Gimnasio", "Videojuegos", "Netflix"
])

if menu == "Vehiculos":
    df = pd.read_csv("Electric_Vehicle_Population-2.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    if "Model_Year" in df.columns:
        df["Model_Year"] = pd.to_numeric(df["Model_Year"], errors='coerce')
    if "Base_MSRP" in df.columns:
        df["Base_MSRP"] = pd.to_numeric(df["Base_MSRP"], errors='coerce')
    if "Electric_Range" in df.columns:
        df["Electric_Range"] = pd.to_numeric(df["Electric_Range"], errors='coerce')

    st.header("Vehículos Eléctricos")
    st.write("Columnas:", df.columns)
    st.write("Filas y columnas:", df.shape)
    st.dataframe(df.head(6))
    st.write(df.describe())

    st.subheader("Filtros")

    anio = st.number_input("Año menor a:", 2000, 2025, value=2020)
    if "Model_Year" in df.columns:
        df_anio = df[df["Model_Year"].notna()]
        st.dataframe(df_anio[df_anio["Model_Year"] < anio])

    precio = st.number_input("Precio menor a:", 0.0, 845000.0, value=50000.0)
    if "Base_MSRP" in df.columns:
        df_precio = df[df["Base_MSRP"].notna()]
        st.dataframe(df_precio[df_precio["Base_MSRP"] < precio])

    if "Electric_Range" in df.columns:
        def categorizar_autonomia(x):
            if pd.isna(x):
                return "Desconocido"
            elif x < 100:
                return "Bajo"
            elif x <= 250:
                return "Medio"
            else:
                return "Alto"

        df["RangoCategoria"] = df["Electric_Range"].apply(categorizar_autonomia)

        st.write("Distribución por categoría de autonomía:")
        st.write(df["RangoCategoria"].value_counts())
        st.bar_chart(df["RangoCategoria"].value_counts())

        grupo = df.groupby("RangoCategoria").mean(numeric_only=True)
        st.write("Medias por categoría:")
        st.write(grupo)

    if st.button("Guardar Vehículos"):
        df.to_csv("Electric_Vehicle_Population_Actualizado.csv", index=False)
        st.success("Guardado correctamente")

elif menu == "Gimnasio":
    if "df_gym" not in st.session_state:
        df = pd.read_csv("GymExerciseTracking.csv")
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        if "Calories_Burned" in df.columns:
            df["Calories_Burned"] = pd.to_numeric(df["Calories_Burned"], errors='coerce')
        if "Fat_Percentage" in df.columns:
            df["Fat_Percentage"] = pd.to_numeric(df["Fat_Percentage"], errors='coerce')
        if "Workout_Frequency" in df.columns:
            df["Workout_Frequency"] = pd.to_numeric(df["Workout_Frequency"], errors='coerce')

        st.session_state.df_gym = df

    df = st.session_state.df_gym

    st.header("Gimnasio")
    st.write(f"Filas y columnas: {df.shape}")
    st.write("Columnas:", df.columns.tolist())
    st.dataframe(df.head(6))
    st.write(df.describe())

    st.subheader("Agregar registro")
    with st.form("agregar_registro"):
        cal = st.number_input("Calorías quemadas", value=0.0, step=10.0)
        fat = st.number_input("Porcentaje de grasa", value=0.0, step=1.0, min_value=0.0, max_value=100.0)
        submitted = st.form_submit_button("Agregar")

    if submitted:
        new_row = pd.Series([None] * len(df.columns), index=df.columns)
        if "Calories_Burned" in df.columns:
            new_row["Calories_Burned"] = cal
        if "Fat_Percentage" in df.columns:
            new_row["Fat_Percentage"] = fat
        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        st.session_state.df_gym = df
        st.success("Registro añadido correctamente")

    st.subheader("Filtros")
    if "Calories_Burned" in df.columns:
        c = st.number_input("Calorías >= ", value=500.0, step=50.0)
        df_cal = df[df["Calories_Burned"].notna()]
        st.dataframe(df_cal[df_cal["Calories_Burned"] >= c])

    if "Fat_Percentage" in df.columns:
        f = st.number_input("Grasa <= ", value=25.0, step=1.0)
        df_fat = df[df["Fat_Percentage"].notna()]
        st.dataframe(df_fat[df_fat["Fat_Percentage"] <= f])

    if "Workout_Frequency" in df.columns:
        def categorizar_frecuencia(x):
            if pd.isna(x):
                return "Desconocido"
            elif x < 3:
                return "Baja"
            elif x <= 5:
                return "Media"
            else:
                return "Alta"

        df["NivelFrecuencia"] = df["Workout_Frequency"].apply(categorizar_frecuencia)

        st.write("Distribución por frecuencia:")
        st.write(df["NivelFrecuencia"].value_counts())
        st.bar_chart(df["NivelFrecuencia"].value_counts())

        grupo = df.groupby("NivelFrecuencia").mean(numeric_only=True)
        st.write("Medias por nivel de frecuencia:")
        st.write(grupo)

    if st.button("Guardar Gimnasio"):
        st.session_state.df_gym.to_csv("GymExerciseTracking_Actualizado.csv", index=False)
        st.success("Guardado correctamente")

elif menu == "Videojuegos":
    df = pd.read_csv("steam_store_data_2024.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors='coerce')
    if "discount_percent" in df.columns:
        df["discount_percent"] = pd.to_numeric(df["discount_percent"], errors='coerce')

    st.header("Videojuegos")
    st.write(f"Filas y columnas: {df.shape}")
    st.write("Columnas:", df.columns.tolist())
    st.dataframe(df.head(6))
    st.write(df.describe())

    st.subheader("Filtros")
    if "price" in df.columns:
        p = st.number_input("Precio mayor a:", value=20.0, step=5.0)
        df_price = df[df["price"].notna()]
        st.dataframe(df_price[df_price["price"] > p])

    if "discount_percent" in df.columns:
        d = st.number_input("Descuento menor a (%):", value=50, step=5)
        df_disc = df[df["discount_percent"].notna()]
        st.dataframe(df_disc[df_disc["discount_percent"] < d])

    if "price" in df.columns:
        def categorizar_precio(x):
            if pd.isna(x):
                return "Desconocido"
            elif x < 10:
                return "Baja"
            elif x <= 24:
                return "Media"
            else:
                return "Alta"

        df["GamaJuego"] = df["price"].apply(categorizar_precio)

        st.write("Distribución por gama de precio:")
        st.write(df["GamaJuego"].value_counts())
        st.bar_chart(df["GamaJuego"].value_counts())

        grupo = df.groupby("GamaJuego").mean(numeric_only=True)
        st.write("Medias por gama:")
        st.write(grupo)

    if st.button("Guardar Juegos"):
        df.to_csv("steam_store_data_2024_Actualizado.csv", index=False)
        st.success("Guardado correctamente")

elif menu == "Netflix":
    df = pd.read_csv("Netflix_titles.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    if "release_year" in df.columns:
        df["release_year"] = pd.to_numeric(df["release_year"], errors='coerce')
        
    df["country"].value_counts().head(10)

    st.header("Netflix")
    st.write(f"Filas y columnas: {df.shape}")
    st.write("Columnas:", df.columns.tolist())
    st.dataframe(df.head(6))
    st.write(df.describe())

    st.subheader("Filtros")
    if "release_year" in df.columns:
        anio = st.number_input("Año menor a:", 2000, 2025, value=2020)
        df_year = df[df["release_year"].notna()]
        st.dataframe(df_year[df_year["release_year"] < anio])

    if "rating" in df.columns:
        def categorizar_rating(x):
            if pd.isna(x):
                return "Sin clasificar"
            elif x in ["G", "TV-G"]:
                return "Niños"
            elif x in ["PG"]:
                return "Adolescentes"
            else:
                return "Adultos"

        df["TipoAudiencia"] = df["rating"].apply(categorizar_rating)

        st.write("Distribución por tipo de audiencia:")
        st.write(df["TipoAudiencia"].value_counts())
        st.bar_chart(df["TipoAudiencia"].value_counts())

    if st.button("Guardar Netflix"):
        df.to_csv("netflix_titles_Actualizado.csv", index=False)
        st.success("Guardado correctamente")