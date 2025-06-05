import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
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
        'lang': 'pt_br'    # Descrições em português
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
def analisar_chuva_5day(previsao_data) -> None: # Alterado para None, pois a captura é feita externamente
    """
    Analisa os dados da previsão de 5 dias/3 horas, mostrando a probabilidade
    e a quantidade de chuva para cada período nos próximos 5 dias.
    A saída é impressa no console.
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
            # Obtém o nome do dia da semana em português
            dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
            nome_dia_semana = dias_semana[data_atual_obj.weekday()]
            print(f"\n--- {data_atual_obj.strftime('%d/%m/%Y')} ({nome_dia_semana}) ---") # Mostra dia da semana
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
        raise ValueError("Dados de previsão inválidos ou ausentes para chuva_por_dia.")

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
    for data_key in resultado: # Renomeado 'data' para 'data_key' para evitar conflito com módulo datetime
        if contagem_pop[data_key] > 0:
            resultado[data_key]['media_pop'] = resultado[data_key]['soma_pop'] / contagem_pop[data_key]
        else:
            resultado[data_key]['media_pop'] = 0.0
        del resultado[data_key]['soma_pop'] # Remove a soma_pop que é intermediária

    return resultado

def get_previsao_de_chuva(cidade:str) -> dict:
    """
    Obtém a previsão de chuva diária agregada para uma cidade específica.
    :param cidade: Nome da cidade para a qual obter a previsão.
    :return: Dicionário com a previsão de chuva por dia.
    """
    api_key = os.getenv('API_MET')

    if not api_key:
        if not api_key: 
             raise ValueError("Chave da API 'API_MET' não encontrada nas variáveis de ambiente.")

    previsao_completa_data = get_5day_forecast(cidade, api_key)

    if not previsao_completa_data:
        raise ValueError(f"Não foi possível obter a previsão do tempo completa para {cidade}.")

    dados_chuva_diaria = chuva_por_dia(previsao_completa_data)
    
    return dados_chuva_diaria


# --- Função principal de previsão de alagamento com 'Data', 'Chuva' e 'Cotas' ---
def prever_alagamento_usando_data_ddmm(cidade: str, modelo_path: str) -> str:
    """
    Prevê o risco de alagamento para uma cidade usando um modelo de ML,
    considerando Data, Chuva e um valor fixo de Cotas.
    Retorna uma string formatada com os resultados da previsão.
    """
    print(f"🔍 [DEBUG] Iniciando previsão de alagamento para {cidade} com modelo ML (incluindo Cotas).")
    resultados_formatados = [f"--- Previsão de Risco de Alagamento para {cidade} (Modelo ML com Cotas) ---"]

    # Defina o valor fixo para as cotas aqui.
    # Este valor será usado para todas as previsões diárias.
    VALOR_FIXO_COTA = 10.0  # Exemplo: cota de referência de 10.0 unidades (ajuste conforme necessário)
    resultados_formatados.append(f"Utilizando valor fixo para Cotas: {VALOR_FIXO_COTA:.2f}")


    try:
        dados_chuva = get_previsao_de_chuva(cidade)
    except ValueError as e:
        print(f"Erro ao obter dados de chuva para o modelo ML: {e}")
        return f"Não foi possível obter a previsão de chuva para {cidade} para análise de alagamento.\nDetalhe: {e}"
    
    if not dados_chuva:
        msg = f"Não foram retornados dados de chuva para {cidade} pela função get_previsao_de_chuva."
        print(msg)
        return msg

    # Transformar em DataFrame
    try:
        df = pd.DataFrame.from_dict(dados_chuva, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'DataStr', 'chuva_mm': 'Chuva'}, inplace=True)

        if 'DataStr' not in df.columns or 'Chuva' not in df.columns:
            return "Erro: DataFrame não contém as colunas 'DataStr' ou 'Chuva' após a transformação."

        # Converter data YYYY-MM-DD para DDMM (como no dataset original)
        df['Data'] = pd.to_datetime(df['DataStr']).dt.strftime('%d%m')
        
        # Adicionar a coluna de Cotas com o valor fixo
        df['Cotas'] = VALOR_FIXO_COTA
        
        # Certifique-se de que as colunas 'Data', 'Chuva' e 'Cotas' são do tipo esperado pelo modelo.
        # Se o modelo foi treinado com 'Data' como inteiro:
        # df['Data'] = df['Data'].astype(int)
        # Se o modelo espera 'Chuva' e 'Cotas' como float, já deve estar correto.

    except Exception as e:
        print(f"Erro ao preparar DataFrame para o modelo ML: {e}")
        return f"Erro ao processar dados de chuva e cotas para o modelo: {e}"

    # Carregar o modelo
    try:
        if not os.path.exists(modelo_path):
            return f"Erro: Arquivo do modelo não encontrado em '{modelo_path}'"
        modelo = joblib.load(modelo_path)
    except Exception as e:
        print(f"Erro ao carregar o modelo de ML de '{modelo_path}': {e}")
        return f"Erro crítico ao carregar o modelo de previsão: {e}"

    # Realiza a previsão
    try:
        # Assegure que as colunas passadas para predict() são exatamente
        # as mesmas (nomes e ordem) e tipos que o modelo espera.
        # IMPORTANTE: O modelo DEVE ter sido treinado com as features 'Data', 'Chuva' e 'Cotas'.
        features_para_previsao = ['Data', 'Chuva', 'Cotas'] 
        if not all(feature in df.columns for feature in features_para_previsao):
            missing_features = [f for f in features_para_previsao if f not in df.columns]
            return f"Erro: DataFrame não contém as features necessárias para previsão: {missing_features}"
        
        print(f"DataFrame antes da previsão (primeiras linhas):\n{df[features_para_previsao].head()}")

        previsoes = modelo.predict(df[features_para_previsao])
        df['Alagamento'] = previsoes
    except Exception as e:
        print(f"Erro durante a predição com o modelo ML: {e}")
        print("Verifique se o modelo foi treinado com as features: 'Data', 'Chuva', 'Cotas' (nessa ordem e tipos corretos).")
        return f"Erro ao realizar a predição de alagamento: {e}"

    # Exibe os resultados
    if df.empty:
        resultados_formatados.append("Não há dados de previsão para processar.")
    else:
        for _, row in df.iterrows():
            try:
                data_formatada = pd.to_datetime(row['DataStr']).strftime('%d/%m/%Y')
                status = "⚠️ Risco de Alagamento" if row['Alagamento'] else "✅ Sem Risco de Alagamento"
                # Incluindo a cota no output, embora seja fixa por enquanto
                resultados_formatados.append(f"{data_formatada}: {status} | Chuva Prevista: {row['Chuva']:.2f} mm | Cotas: {row['Cotas']:.2f}")
            except Exception as e:
                 resultados_formatados.append(f"Erro ao formatar resultado para {row.get('DataStr', 'Data Desconhecida')}: {e}")


    return "\n".join(resultados_formatados)

# --- Principal ---
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    load_dotenv(dotenv_path)
    
    api_key_env = os.getenv('API_MET') 
    
    if not api_key_env:
        api_key_input = input("Por favor, insira sua chave da API OpenWeatherMap: ").strip()
        if not api_key_input:
            print("Chave da API não fornecida. Saindo.")
            exit()
        api_key_to_use = api_key_input
    else:
        api_key_to_use = api_key_env

    cidade_usuario = input("Digite o nome da sua cidade: ").strip()
    modelo_path_main = os.path.join(os.path.dirname(__file__), "..", "..", "modelo_preditivo", "modelos_salvos", "BaggingDTd3.pkl")
    modelo_path_main = os.path.normpath(modelo_path_main)


    if cidade_usuario:
        print("\n--- Obtendo previsão de 5 dias / 3 horas ---")
        previsao_raw = get_5day_forecast(cidade_usuario, api_key_to_use)

        if previsao_raw:
            analisar_chuva_5day(previsao_raw)

            print("\n--- Calculando chuva por dia (para possível uso ou debug) ---")
            try:
                dados_chuva_diaria = chuva_por_dia(previsao_raw)
                print("Dados de chuva por dia:")
                for data, info in dados_chuva_diaria.items():
                    print(f"  {pd.to_datetime(data).strftime('%d/%m/%Y')}: Chuva {info['chuva_mm']:.2f} mm, Média POP {info['media_pop']:.0f}%")
            except ValueError as e:
                print(f"Erro ao calcular chuva por dia: {e}")


            print("\n--- Iniciando previsão de alagamento com modelo ML (com Cotas) ---")
            if os.path.exists(modelo_path_main):
                # A função prever_alagamento_usando_data_ddmm agora usa a cidade e o caminho do modelo
                resultado_previsao_ml = prever_alagamento_usando_data_ddmm(cidade_usuario, modelo_path_main)
                print(resultado_previsao_ml)
            else:
                print(f"Erro Crítico: Arquivo do modelo não encontrado em '{modelo_path_main}'. Não é possível fazer a previsão de alagamento.")
        else:
            print(f"Não foi possível obter a previsão do tempo para {cidade_usuario}.")
    else:
        print("Nome da cidade não fornecido.")
