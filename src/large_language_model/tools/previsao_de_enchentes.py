from datetime import datetime
import os
import io
import contextlib
from src.API_met import get_5day_forecast, analisar_chuva_5day
from dotenv import load_dotenv
from src.large_language_model.tipos_base.base_tools import BaseTool


class EnchenteTool(BaseTool):

    @property
    def function_declaration(self):
         return {
            "name": "prever_risco_enchente_proximos_dias",
            "description": "Prevê o risco de chuva intensa que pode levar a enchentes para uma cidade nos próximos 5 dias.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {
                        "type": "string",
                        "description": "O nome da cidade para a qual obter a previsão. Ex: 'São Paulo'"
                    }
                },
                "required": ["cidade"]
            }
        }
    def prever_enchente_proximos_dias(self, cidade: str):
        """
        Preview if there will be a flooding in the next 5 days
        """

        print("Chamou função previsão de enchente")

        load_dotenv()
        api_key = os.getenv('API_MET')

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
            output_buffer.close() # para ter fechar o buffer
        if not analise_formatada.strip(): # Verifica se algo foi capturado
            return {
                'error': True,
                'message': f"A análise da previsão para {cidade} não gerou conteúdo."
            }
        return {
            'output': analise_formatada,
            'error': False,
            'message': f"Previsão detalhada de chuva para {cidade} obtida e analisada."
        }


    def call_chat_display(self) -> str:
        return "Fazendo a previsão de enchentes..."

    def call_result_display(self, result: dict) -> str:
        """
        Outputs the result of the flood prediction.
        'result' is the dictionary returned by the prever_enchente_proximos_dias function.
        """

        return "Previsão obtida com sucesso"