import joblib
import pandas as pd
from datetime import date
from typing import Literal

def data_valida(dia: int, mes: int, ano: int or None) -> bool:

    ano = ano if ano is not None else date.today().year

    try:
        date(ano, month=mes, day=dia)
        return True
    except ValueError:
        return False

def carregar_modelo_e_realizar_previsao(path_arquivo: str, *,
                                        dia: int,
                                        mes: int,
                                        cota: float,
                                        chuva: float,
                                        ) -> Literal["Condições normais", "Inundação provável"]:
    """
    Carrega o modelo, scaler e label encoder salvos, aplica o scaler ao novo dado,
    realiza a previsão e converte o resultado para a categoria original (texto).

    :param dia: Dia do mês (1-31).
    :param mes: Mês do ano (1-12).
    :param cota: Valor da cota.
    :param chuva: Valor da chuva.
    :param path_arquivo: Caminho do arquivo onde o modelo, scaler e label encoder estão salvos.
    :return: Previsão em formato de texto.
    """

    # checa se a data é válida

    if not data_valida(dia, mes, date.today().year):
        raise ValueError(f"Data inválida: {dia:02d}/{mes:02d}/{date.today().year}")

    dia_mes_aglutinado = int(f"{dia:02d}{mes:02d}")

    data_frame_prever = pd.DataFrame({
        'Data': [dia_mes_aglutinado],
        'Cota': [cota],
        'Chuva': [chuva]
    })

    # Carregando modelo, scaler e label encoder salvos
    modelo_load = joblib.load(path_arquivo)

    modelo = modelo_load['modelo']
    scaler = modelo_load['scaler']
    le = modelo_load['label_encoder']  # Carregando o LabelEncoder

    # Aplicando o scaler ao novo dado
    novo_dado_scaled = scaler.transform(data_frame_prever)

    # Fazendo a previsão
    previsao = modelo.predict(novo_dado_scaled)

    # Convertendo o resultado para a categoria original (texto)
    previsao_texto = le.inverse_transform(previsao)

    return previsao_texto[0]