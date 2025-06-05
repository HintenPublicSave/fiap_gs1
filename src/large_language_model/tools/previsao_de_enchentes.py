import os
import io
import contextlib
import pandas as pd
import joblib
from src.api_metereologica.api import analisar_chuva_5day
from src.api_metereologica.api import get_5day_forecast
from src.large_language_model.tipos_base.base_tools import BaseTool
from src.api_metereologica.api import prever_alagamento_usando_data_ddmm
from dotenv import load_dotenv

class EnchenteTool(BaseTool):

    @property
    def function_declaration(self):

        return self.prever_enchente_proximos_dias

    def prever_enchente_proximos_dias(self, cidade: str):
        """
        Prevê o risco de chuva intensa que pode levar a enchentes para uma cidade nos próximos 5 dias.
        Parâmetro:
            cidade (str): O nome da cidade para a qual obter a previsão. Ex: 'São Paulo'
        """
        print("🧠 [DEBUG] Iniciando previsão de alagamento com modelo treinado")

        api_key = os.getenv('API_MET')
        
        script_dir = os.path.dirname(__file__)
        modelo_path_relativo = os.path.join("..", "..", "..","src", "modelo_preditivo", "modelos_salvos", "BaggingDTd3.pkl")
        modelo_path = os.path.abspath(os.path.join(script_dir, modelo_path_relativo))

        previsao_data = get_5day_forecast(cidade, api_key)
        
        print(f"🛠️ [DEBUG] Caminho do modelo ML: {modelo_path}")
        if not os.path.exists(modelo_path):
            print(f"🛑 [ERRO] Arquivo do modelo ML não encontrado em: {modelo_path}")
            return {
                'error': True,
                'message': f"Arquivo do modelo de Machine Learning não encontrado no caminho esperado: {modelo_path}"
            }
            
        previsao_data_raw = get_5day_forecast(cidade, api_key)
        
        if not previsao_data_raw:
            return {
                'error': True,
                'message': f"Não foi possível obter dados da previsão do tempo (5 dias) para {cidade}."
            }

        # Capturar a saída da função analisar_chuva_5day
        output_buffer_analise_chuva = io.StringIO()
        try:
            with contextlib.redirect_stdout(output_buffer_analise_chuva):
                analisar_chuva_5day(previsao_data_raw)
            analise_formatada = output_buffer_analise_chuva.getvalue()
        finally:
            output_buffer_analise_chuva.close()

        if not analise_formatada.strip():
            # Mesmo que a função não gere erro, pode não haver output se os dados forem insuficientes
            analise_formatada = f"A análise detalhada da previsão para {cidade} não gerou conteúdo visualizável (verifique os logs para detalhes sobre os dados de entrada)."
            print(f"⚠️ [AVISO] {analise_formatada}")

        try:
            # A função prever_alagamento_usando_data_ddmm em api.py espera (cidade, modelo_path)
            print(f"🤖 [DEBUG] Chamando prever_alagamento_usando_data_ddmm com cidade='{cidade}' e modelo_path='{modelo_path}'")
            resultado_ml_str = prever_alagamento_usando_data_ddmm(cidade, modelo_path)
            
            if "Erro" in resultado_ml_str or "não encontrado" in resultado_ml_str.lower() or "não foi possível" in resultado_ml_str.lower() : # Heurística simples para detectar erros retornados como string
                 print(f"⚠️ [AVISO] Modelo ML retornou uma mensagem de erro/aviso: {resultado_ml_str}")
                 # Decide se quer tratar como erro fatal ou apenas incluir a mensagem
                 # return {
                 #    'error': True,
                 #    'message': f"Erro na previsão de alagamento com modelo ML: {resultado_ml_str}"
                 # }

        except Exception as e:
            print(f"🛑 [ERRO] Exceção ao chamar prever_alagamento_usando_data_ddmm: {e}")
            return {
                'error': True,
                'message': f"Erro inesperado ao executar a previsão de alagamento com modelo: {e}"
            }

        # Combinar os dois resultados
        saida_final = analise_formatada + "\n\n" + resultado_ml_str

        return {
            'output': saida_final,
            'error': False, # Assumindo sucesso se chegou aqui e não houve erro explícito retornado como string
            'message': f"Análise completa de chuva e risco de alagamento obtida para {cidade}."
        }

       

    def call_chat_display(self) -> str:
        return "Fazendo a previsão de enchentes..."

    def call_result_display(self, result: dict) -> str:
        """
        Outputs the result of the flood prediction.
        'result' is the dictionary returned by the prever_enchente_proximos_dias function.
        MODIFICADO: Agora retorna o output detalhado em caso de sucesso.
        """
        if result.get('error'):
            return f"Erro ao obter previsão: {result.get('message', 'Erro desconhecido.')}"

        return "Previsão obtida com sucesso"