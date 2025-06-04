import logging

import streamlit as st
import joblib
import os

from src.modelo_preditivo.realizar_previsao_func import carregar_modelo_e_realizar_previsao
from src.settings import DEBUG


def modelo_preditivo_view():
    """
    View para realizar previsões manuais com o modelo preditivo.
    :return:
    """

    st.title("🔮 Previsão Manual com Modelo Preditivo")

    st.write("Nesta página, você pode realizar previsões manuais utilizando o modelo preditivo treinado.")

    #pega os modelos em src/modelo_preditivo/modelos_salvos

    if not os.path.exists("src/modelo_preditivo/modelos_salvos"):
        st.error("⚠️ Modelo preditivo não encontrado. Por favor, treine o modelo antes de realizar previsões.")
        return

    modelos_paths = [f for f in os.listdir("src/modelo_preditivo/modelos_salvos") if f.endswith('.pkl')]

    # Carrega o modelo preditivo
    modelo_selecionado = st.selectbox(
        "Selecione o modelo preditivo:",
        options=modelos_paths,
        format_func=lambda x: x.replace('.pkl', '')  # Exibe o nome do modelo sem a extensão
    )

    if not modelo_selecionado:
        st.error("⚠️ Nenhum modelo selecionado.")
        return

    modelo_selecionado_full_path = os.path.join("src/modelo_preditivo/modelos_salvos", modelo_selecionado)

    dia = st.number_input("Dia (1-31):", min_value=1, max_value=31, value=1)
    mes = st.number_input("Mês (1-12):", min_value=1, max_value=12, value=1)
    cota = st.number_input("Cota (em metros):", value=100)
    chuva = st.number_input("Chuva (em mm):", value=20)

    if st.button("Realizar Previsão"):
        if not modelo_selecionado:
            st.error("⚠️ Por favor, selecione um modelo preditivo.")
            return

        try:
            previsao = carregar_modelo_e_realizar_previsao(
                modelo_selecionado_full_path,
                dia=dia,
                mes=mes,
                cota=cota,
                chuva=chuva
            )
        except Exception as e:
            st.error(f"⚠️ Erro ao realizar a previsão: {str(e)}")
            logging.error(e)
            if DEBUG:
                raise
            return

        st.success(f"🔮 Previsão realizada com sucesso!\nResultado: {previsao}")

previsao_manual_page = st.Page(
    modelo_preditivo_view,
    title="Previsão Manual",
    url_path="previsao_manual"
)