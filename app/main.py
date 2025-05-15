import streamlit as st
import pandas as pd
from app import database
import sqlite3
from datetime import datetime

# Inicializa DB
database.create_tables()

def connect_db():
    return sqlite3.connect("data/remnants.db")

st.title("📦 Remnants Manager")

menu = ["📃 Ver estoque", "➕ Adicionar remnant", "📌 Registrar uso"]
choice = st.sidebar.selectbox("Menu", menu)

conn = connect_db()

# 📃 Ver estoque
if choice == "📃 Ver estoque":
    st.header("📦 Estoque de Remnants")
    df = pd.read_sql_query("SELECT * FROM remnants", conn)
    if df.empty:
        st.warning("Nenhum remnant cadastrado.")
    else:
        st.dataframe(df)
        for _, row in df.iterrows():
            st.subheader(f"{row['nome']} - {row['material']}")
            st.write(f"Tamanho: {row['largura']} x {row['altura']} cm")
            st.write(f"Status: {row['status']}")
            st.image(row['imagem_url'], width=300)

# ➕ Adicionar remnant
elif choice == "➕ Adicionar remnant":
    st.header("Adicionar novo remnant")
    nome = st.text_input("Nome")
    material = st.text_input("Material")
    largura = st.number_input("Largura (cm)", min_value=0.0)
    altura = st.number_input("Altura (cm)", min_value=0.0)
    status = st.selectbox("Status", ["Disponível", "Reservado", "Usado"])
    imagem_url = st.text_input("URL da imagem (Google Photos link)")

    if st.button("Salvar"):
        c = conn.cursor()
        c.execute('''
            INSERT INTO remnants (nome, material, largura, altura, status, imagem_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, material, largura, altura, status, imagem_url))
        conn.commit()
        st.success("Remnant cadastrado com sucesso!")

# 📌 Registrar uso
elif choice == "📌 Registrar uso":
    st.header("Registrar uso de um remnant")
    c = conn.cursor()
    c.execute("SELECT id, nome FROM remnants WHERE status != 'Usado'")
    options = c.fetchall()

    if options:
        remnant = st.selectbox("Selecione o remnant", options, format_func=lambda x: x[1])
        projeto = st.text_input("Projeto")
        data_uso = st.date_input("Data de uso", datetime.now())

        if st.button("Registrar uso"):
            c.execute('''
                INSERT INTO historico_uso (remnant_id, projeto, data_uso)
                VALUES (?, ?, ?)
            ''', (remnant[0], projeto, data_uso.strftime("%Y-%m-%d")))

            c.execute("UPDATE remnants SET status = 'Usado' WHERE id = ?", (remnant[0],))
            conn.commit()
            st.success("Uso registrado com sucesso!")
    else:
        st.warning("Nenhum remnant disponível para uso.")

conn.close()
