
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import database

# Banco de dados
conn = database.create_connection("remnants.db")
database.create_table(conn)

# Página
st.title("Remnants Manager")

# Adicionar novo remnant
st.subheader("Adicionar novo remnant")
name = st.text_input("Nome")
material = st.text_input("Material")
size = st.text_input("Tamanho")
location = st.text_input("Localização")
used_in = st.text_input("Usado em")
photo_url = st.text_input("URL da Foto")

if st.button("Salvar"):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO remnants (name, material, size, location, used_in, photo_url) VALUES (?, ?, ?, ?, ?, ?)", 
                  (name, material, size, location, used_in, photo_url))
        conn.commit()
        st.success("Remnant salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# Mostrar lista
st.subheader("Estoque de Remnants")
df = pd.read_sql_query("SELECT * FROM remnants", conn)
st.dataframe(df)
