import streamlit as st
import pandas as pd
import plotly.express as px
import os

def view():

    
    st.title("💧 Análise Interativa de Cota e Chuva")
    
    data = pd.read_csv("src/modelo_preditivo/COTAxCHUVA.csv")
    df = pd.DataFrame(data)
    

    #  Preparação da coluna Data
    df["Data"] = df["Data"].astype(str).str.zfill(4)
    df["DiaMes"] = df["Data"].str[:2] + "/" + df["Data"].str[2:]
    df["Ordem"] = df["Data"].astype(int)
    df = df.sort_values("Ordem")

    #  Filtro de intervalo de datas
    st.sidebar.header("🗓️ Filtro de Intervalo de Datas")
    datas_disponiveis = df["DiaMes"].tolist()
    start_idx, end_idx = st.sidebar.select_slider(
        "Selecione o intervalo de dias:",
        options=list(range(len(datas_disponiveis))),
        value=(0, len(datas_disponiveis) - 1),
        format_func=lambda i: datas_disponiveis[i]
    )
    df_filtrado:pd.DataFrame = df.iloc[start_idx:end_idx + 1]

    #  Tabela com os dados filtrados
    st.subheader("📄 Dados")
    st.dataframe(df_filtrado[["DiaMes", "Cota", "Chuva"]])

    st.subheader("📊 Estatísticas Descritivas")

    st.write(df_filtrado.describe())

    #  Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Evolução da Cota")
        fig_cota = px.line(df_filtrado, x="DiaMes", y="Cota", markers=True)
        st.plotly_chart(fig_cota, use_container_width=True)

    with col2:
        st.markdown("### 🌧️ Volume de Chuva")
        fig_chuva = px.bar(df_filtrado, x="DiaMes", y="Chuva")
        st.plotly_chart(fig_chuva, use_container_width=True)

    #  Gráfico de dispersão com segurança no uso do size
    st.markdown("### 🔍 Relação entre Cota e Chuva")
    df_disp = df_filtrado[df_filtrado["Chuva"].notna()]
    if not df_disp.empty:
        fig_disp = px.scatter(df_disp, x="Chuva", y="Cota", size="Chuva")
        st.plotly_chart(fig_disp, use_container_width=True)
    else:
        st.warning("⚠️ Não há dados de chuva disponíveis neste intervalo para exibir o gráfico de dispersão.")

    #  Histograma da Cota
    st.markdown("### 📊 Distribuição da Cota")
    fig_hist = px.histogram(df_filtrado, x="Cota", nbins=5)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Gráfico de temperatura (correlação)
    st.markdown("### 🌡️ Correlação entre Variáveis (Gráfico de Temperatura)")

    # Filtra colunas numéricas
    colunas_numericas = df_filtrado.select_dtypes(include=['float64', 'int64']).columns

    if len(colunas_numericas) >= 2:
        corr_matrix = df_filtrado[colunas_numericas].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            title="Mapa de Correlação"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("⚠️ São necessárias pelo menos duas variáveis numéricas para gerar o mapa de correlação.")


exploracao_de_dados = st.Page(
    view,
    title="Exploração de Dados",
    url_path="exploracao_de_dados",
)
