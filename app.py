import streamlit as st
from app_util import processa_entrada

st.write("# Trabalho de Linguagens Formais:")

entrada = st.text_input('### Informe a entrada que deseja verificar: ')

col1, col2 = st.columns([1,1])

with col1:
    btn_processa_entrada =  st.button("Processar Entrada")
with col2:
    btn_limpa_entrada = st.button("Limpar Campos")


if btn_processa_entrada:
    limpa_entrada = False
    retorno, df = processa_entrada(entrada)

    st.table(df)

    st.write(retorno)

if btn_limpa_entrada:
    entrada = ''
    btn_processa_entrada = False
