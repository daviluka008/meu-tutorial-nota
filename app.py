import streamlit as st

st.title("Meu tutorial interativo")

nome = st.text_input("Digite seu nome")

if nome:
    st.success(f"Bem-vindo, {nome}!")
