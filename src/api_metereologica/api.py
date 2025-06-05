import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import joblib

# --- Função para interagir com a API ---
def get_5day_forecast(cidade, api_key):
    """
    Obtém a previsão do tempo para 5 dias/3 horas da API OpenWeatherMap.
    """
    base_url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': cidade,
        'appid': api_key,
        'units': 'metric',  # Temperatura em Celsius, velocidade do vento em m/s
        'lang': 'pt_br'     # Descrições em português
    }
    try:
        response = requests.get(base_url_forecast, params=params)
        response.raise_for_status()  # Levanta um erro para respostas 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Erro: Chave da API inválida ou não autorizada.")
        elif response.status_code == 404:
            print(f"Erro: Cidade '{cidade}' não encontrada.")
        else:
            print(f"Erro HTTP: {http_err}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da previsão do tempo: {e}")
        return None

# --- Função de Análise de Chuva ---
def analisar_chuva_5day(previsao_data) -> dict or None:
    """
    Analisa os dados da previsão de 5 dias/3 horas, mostrando a probabilidade
    e a quantidade de chuva para cada período nos próximos 5 dias.
    """
    if not previsao_data or 'list' not in previsao_data:
        print("Dados de previsão inválidos ou ausentes.")
        return

    nome_cidade_api = previsao_data.get('city', {}).get('name', 'Cidade Desconhecida')
    print(f"\n--- Previsão Detalhada de Chuva para {nome_cidade_api} (Próximos 5 Dias) ---")

    if not previsao_data['list']:
        print("Não há dados de previsão horária disponíveis.")
        return

    alguma_chuva_com_volume_mm_total = False
    max_pop_geral_sem_volume = 0
    dia_anterior = None

    for previsao_slot in previsao_data['list']:
        dt_txt = previsao_slot.get('dt_txt', 'Horário Desconhecido')
        horario_formatado = dt_txt  # Padrão se a conversão falhar
        data_atual_obj = None
        try:
            # Converte a string de data/hora para um objeto datetime
            horario_obj = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
            # Formata para dd/mm HH:MM
            horario_formatado = horario_obj.strftime('%d/%m %H:%M')
            data_atual_obj = horario_obj.date()
        except ValueError:
            pass  # Usa dt_txt original se o formato for inesperado
        
        # Imprime o cabeçalho do dia quando o dia muda
        if data_atual_obj and data_atual_obj != dia_anterior:
            print(f"\n--- {data_atual_obj.strftime('%d/%m/%Y (%A)')} ---") # Mostra dia da semana
            dia_anterior = data_atual_obj

        pop = previsao_slot.get('pop', 0) * 100  # Probabilidade de precipitação em %
        chuva_mm_3h = 0.0  # Padrão de 0.0 mm
        descricao_tempo = previsao_slot.get('weather', [{}])[0].get('description', 'N/D').capitalize()

        # Verifica se há dados de chuva e se '3h' existe
        if 'rain' in previsao_slot and isinstance(previsao_slot['rain'], dict) and '3h' in previsao_slot['rain']:
            chuva_mm_3h = float(previsao_slot['rain']['3h'])

        if chuva_mm_3h > 0:
            alguma_chuva_com_volume_mm_total = True
        elif pop > max_pop_geral_sem_volume : # Atualiza a probabilidade máxima se não houver volume de chuva
             max_pop_geral_sem_volume = pop


        print(f"- {horario_formatado}: {descricao_tempo}, Chuva: {chuva_mm_3h:.2f} mm, Probabilidade: {pop:.0f}%")

    print(f"\n--- Resumo Geral para os Próximos 5 Dias em {nome_cidade_api} ---")
    if alguma_chuva_com_volume_mm_total:
        print(f"Sim, há previsão de chuva com volume acumulado (em mm) em algum(ns) período(s) nos próximos 5 dias.")
    elif max_pop_geral_sem_volume > 10: # Se a probabilidade máxima sem chuva em mm for relevante
        print(f"Não há previsão de chuva com volume acumulado (em mm) nos próximos 5 dias.")
        print(f"No entanto, a probabilidade de alguma precipitação chega a {max_pop_geral_sem_volume:.0f}% em alguns horários.")
    else: # Se nem volume em mm nem probabilidade significativa
        print(f"Não há previsão de chuva (nem volume em mm, nem probabilidade significativa) nos próximos 5 dias.")

def chuva_por_dia(previsao_data:dict) -> dict:
    """
    Retorna um dicionário com a soma dos mm de chuva e a média da probabilidade de chuva para cada dia.
    Exemplo de retorno:
    {
        '2024-06-10': {'chuva_mm': 12.5, 'media_pop': 35.2},
        '2024-06-11': {'chuva_mm': 0.0, 'media_pop': 10.0},
        ...
    }
    """
    if not previsao_data or 'list' not in previsao_data:
        raise ValueError("Dados de previsão inválidos ou ausentes.")

    resultado = {}
    contagem_pop = {}

    for previsao_slot in previsao_data['list']:
        dt_txt = previsao_slot.get('dt_txt', None)
        if not dt_txt:
            continue
        data_str = dt_txt.split(' ')[0]  # 'YYYY-MM-DD'
        pop = previsao_slot.get('pop', 0) * 100  # %
        chuva_mm_3h = 0.0
        if 'rain' in previsao_slot and isinstance(previsao_slot['rain'], dict) and '3h' in previsao_slot['rain']:
            chuva_mm_3h = float(previsao_slot['rain']['3h'])

        if data_str not in resultado:
            resultado[data_str] = {'chuva_mm': 0.0, 'soma_pop': 0.0}
            contagem_pop[data_str] = 0

        resultado[data_str]['chuva_mm'] += chuva_mm_3h
        resultado[data_str]['soma_pop'] += pop
        contagem_pop[data_str] += 1

    # Calcula a média da probabilidade de chuva para cada dia
    for data in resultado:
        if contagem_pop[data] > 0:
            resultado[data]['media_pop'] = resultado[data]['soma_pop'] / contagem_pop[data]
        else:
            resultado[data]['media_pop'] = 0.0
        del resultado[data]['soma_pop']

    return resultado

def get_previsao_de_chuva(cidade:str) -> dict:
    """
    Obtém a previsão de chuva para uma cidade específica.
    :param cidade: Nome da cidade para a qual obter a previsão.
    :return: Dicionário com a previsão de chuva.
    """
    api_key = os.getenv('API_MET')

    if not api_key:
        raise ValueError("Chave da API não fornecida.")

    previsao_data = get_5day_forecast(cidade, api_key)

    if not previsao_data:
        raise ValueError("Não foi possível obter a previsão do tempo.")

    return chuva_por_dia(previsao_data)

# --- Função principal de previsão de alagamento com 'Data' e 'Chuva' ---
def prever_alagamento_usando_data_ddmm(cidade: str, modelo_path: str):
    print("🔍 [DEBUG] Entrando na função de previsão de alagamento (usando modelo ML)")
    dados_chuva = get_previsao_de_chuva(cidade)
    if not dados_chuva:
        print("Não foi possível obter a previsão de chuva.")
        return

    # Transformar em DataFrame
    df = pd.DataFrame.from_dict(dados_chuva, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'DataStr', 'chuva_mm': 'Chuva'}, inplace=True)

    # Converter data YYYY-MM-DD para DDMM (como no dataset original)
    df['Data'] = pd.to_datetime(df['DataStr']).dt.strftime('%d%m')

    # Carregar o modelo
    modelo = joblib.load(modelo_path)

    # Converter 'Data' para o tipo que foi usado no treinamento (string ou inteiro)
    # df['Data'] = df['Data'].astype(int)  # Descomente se o modelo espera int

    # Realiza a previsão
    previsoes = modelo.predict(df[['Data', 'Chuva']])
    df['Alagamento'] = previsoes

    # Exibe os resultados
    for _, row in df.iterrows():
        data_formatada = pd.to_datetime(row['DataStr']).strftime('%d/%m/%Y')
        status = "⚠️ Alagamento" if row['Alagamento'] else "✅ Sem alagamento"
        print(f"{data_formatada}: {status} | Chuva: {row['Chuva']:.2f} mm")

# --- Principal ---
if __name__ == "__main__":
    load_dotenv("../../.env")
    api_key = os.getenv('API_MET')
    
    if not api_key:
        api_key = input("Por favor, insira sua chave da API OpenWeatherMap: ").strip()

    if not api_key:
        print("Chave da API não fornecida. Saindo.")
    else:
        cidade_usuario = input("Digite o nome da sua cidade: ").strip()
        modelo_path = "../modelo_preditivo/modelos_salvos/BaggingDTd3.pkl"

        if cidade_usuario:
            previsao = get_5day_forecast(cidade_usuario, api_key)

            if previsao:
                print(chuva_por_dia(previsao))
        else:
            print("Nome da cidade não fornecido.")