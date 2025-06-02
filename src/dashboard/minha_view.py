import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def view():

    df = pd.DataFrame({
        'Nome': ['Pelé', 'Maradona'],
        'Nacionalidade': ['Brasil', 'Argentina'],
        'Gols': [1281, 345],
        'Títulos': [3, 1]
    })

    st.write(df)

    st.subheader("Gráfico de Gols por Jogador")
    plt.figure(figsize=(10, 5))
    plt.bar(df['Nome'], df['Gols'], color=['green', 'blue'])
    plt.xlabel('Jogador')
    plt.ylabel('Número de Gols')
    plt.title('Gols Marcados por Jogador')
    st.pyplot(plt)


pagina_minha_view = st.Page(
    view,
    title="Minha View",
    url_path="minha_view",
)
