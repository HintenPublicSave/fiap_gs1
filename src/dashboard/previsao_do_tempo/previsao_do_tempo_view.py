import streamlit as st
from datetime import datetime

from src.api_metereologica.api import get_previsao_de_chuva


def previsao_do_tempo_view():
    """
    View para o user obter a previsão do tempo.
    """

    st.title("🌦️ Previsão do Tempo")

    cidade = st.text_input("Digite o nome da cidade:", "São Paulo")

    if not cidade:
        st.warning("Por favor, insira o nome de uma cidade.")
        return

    if st.button("Obter Previsão"):
        try:
            previsao = get_previsao_de_chuva(cidade)

            if previsao:
                st.success(f"Previsão do tempo para {cidade}:")
                for data, info in previsao.items():
                    # Converter data de yyyy-mm-dd para dd/mm/aaaa
                    try:
                        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except Exception:
                        data_formatada = data
                    st.markdown(
                        f"**{data_formatada}**: "
                        f"`{info['chuva_mm']:.2f} mm` de chuva &nbsp;|&nbsp; "
                        f"Probabilidade de chuva: "
                        f"`{info['media_pop']:.2f}%`"
                    )
            else:
                st.error("Não foi possível obter a previsão do tempo.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao obter a previsão: {e}")

previsao_do_tempo_page = st.Page(
    previsao_do_tempo_view,
    title="Previsão do Tempo",
    icon="🌦️",
    url_path="previsao_do_tempo"
)