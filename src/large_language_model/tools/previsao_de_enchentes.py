import os
import io
import contextlib
import pandas as pd
import joblib
from src.api_metereologica.api import analisar_chuva_5day
from src.api_metereologica.api import get_5day_forecast
from src.large_language_model.tipos_base.base_tools import BaseTool
from src.api_metereologica.api import prever_alagamento_usando_data_ddmm

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
        
        modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../modelo_preditivo/modelos_salvos/BaggingDtd3.pkl"))

        previsao_data = get_5day_forecast(cidade, api_key)
        

        if not previsao_data:
            return {
                'error': True,
                'message': f"Não foi possível obter dados da previsão do tempo para {cidade}"
            }
        output_buffer = io.StringIO() #    Usamos io.StringIO e contextlib.redirect_stdout para capturar o que analisar_chuva_5day imprimiria.
        try:
            with contextlib.redirect_stdout(output_buffer):
                analisar_chuva_5day(previsao_data)
            analise_formatada = output_buffer.getvalue()
        finally:
            output_buffer.close()

        if not analise_formatada.strip():
            return {
                'error': True,
                'message': f"A análise da previsão para {cidade} não gerou conteúdo."
            }

        # --- Parte 2: Previsão com modelo ML ---
        try:
            resultado_ml = prever_alagamento_usando_data_ddmm(previsao_data, modelo_path, cidade)
        except Exception as e:
            return {
                'error': True,
                'message': f"Erro ao prever alagamento com modelo: {e}"
            }

        # Combinar os dois resultados
        saida_final = analise_formatada + "\n\n" + resultado_ml

        return {
            'output': saida_final,
            'error': False,
            'message': f"Análise completa de chuva e alagamento obtida para {cidade}."
        }
        


    def call_chat_display(self) -> str:
        return "Fazendo a previsão de enchentes..."

    def call_result_display(self, result: dict) -> str:
        """
        Outputs the result of the flood prediction.
        'result' is the dictionary returned by the prever_enchente_proximos_dias function.
        """

        return "Previsão obtida com sucesso"