import streamlit as st
import pymysql
import pandas as pd
import time

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

st.title("Data Dashboard")

tab1, tab2, tab3 = st.tabs(["📊 Kulutusdata","🌧️ Säädata", "⚡ Sähkön hinta"])

with tab1:
  connection = pymysql.connect(
    host="localhost",
    user="exampleuser",
    password="Linux1harjoittelu2025!",
    database="exampledb"
  )

  df = pd.read_sql("SELECT * FROM consumption;", connection)
  connection.close()

  st.title("Kulutusdata-analyysi (MySQL)")
  st.table(df)
  st.line_chart(df.set_index("month")["amount"])

with tab2:
    st.header("Säädata Helsingistä")

    import mysql.connector

    conn_weather = mysql.connector.connect(
      host='localhost',
      user='exampleuser',
      password='Linux1harjoittelu2025!',
      database='weather_db'
    )

    df_weather = pd.read_sql(
    'SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50',
    conn_weather
    )

    conn_weather.close()

    st.subheader("Säädata taulukkona")
    st.dataframe(df_weather)

    st.subheader("Lämpötilan kehitys")
    st.line_chart(df_weather.set_index("timestamp")["temperature"])

    st.subheader("Kosteuden kehitys")
    st.line_chart(df_weather.set_index("timestamp")["humidity"])

with tab3:
    st.subheader("Sähkön hinta (€/kWh)")

    conn_elec = mysql.connector.connect(
      host="localhost",
      user="exampleuser",
      password="Linux1harjoittelu2025!",
      database="weather_db"
    )

    df_elec = pd.read_sql(
    "SELECT * FROM electricity_prices ORDER BY timestamp DESC LIMIT 96",
    conn_elec
    )
    df_elec["timestamp"] = pd.to_datetime(df_elec["timestamp"])



    latest_price = df_elec.iloc[0]["price"]
    st.metric("Nykyinen sähkön hinta", f"{latest_price:.4f} €/kWh")
    
    df_elec = df_elec.sort_values("timestamp")

    # Luo uusi sarake 24h-muodossa
    df_elec["Aika"] = df_elec["timestamp"].dt.strftime("%H:%M")

    # Käytä uutta saraketta indeksinä
    df_elec = df_elec.set_index("Aika")

    # Näytä line chart 24h aikamuodolla
    st.line_chart(df_elec["price"])
