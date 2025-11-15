import streamlit as st
import pymysql
import pandas as pd

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
