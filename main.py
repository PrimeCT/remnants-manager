
import streamlit as st
import pandas as pd
from datetime import datetime

def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("Senha incorreta")
        return False
    else:
        return True

st.sidebar.title("Remnants Manager")

menu = st.sidebar.selectbox("Escolha a área", ["Visualização", "Admin"])

# Leitura de dados
try:
    df = pd.read_csv("remnants.csv")
except FileNotFoundError:
    st.error("Arquivo remnants.csv não encontrado.")
    st.stop()

if menu == "Visualização":
    st.title("Estoque de Remnants")
    st.dataframe(df)

elif menu == "Admin":
    if check_password():
        st.title("Área Administrativa")

        if st.button("Mostrar Estoque"):
            st.dataframe(df)

        st.subheader("Atualizar Estoque via CSV")
        uploaded_file = st.file_uploader("Upload de novo CSV para sobrescrever o estoque", type="csv")
        if uploaded_file is not None:
            new_df = pd.read_csv(uploaded_file)
            new_df.to_csv("remnants.csv", index=False)
            st.success("Estoque atualizado com sucesso!")

        st.subheader("Editar Remnant Individual")
        selected_id = st.text_input("ID do Remnant para editar")

        if st.button("Carregar Remnant"):
            if selected_id:
                filtered_df = df[df["id"] == selected_id]
                if not filtered_df.empty:
                    selected_data = filtered_df.iloc[0]
                    st.write(selected_data)
                else:
                    st.error("Remnant não encontrado.")
            else:
                st.warning("Insira um ID para buscar.")
