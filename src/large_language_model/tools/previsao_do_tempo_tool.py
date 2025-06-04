from datetime import datetime

from src.api_metereologica.api import get_previsao_de_chuva
from src.large_language_model.tipos_base.base_tools import BaseTool
from src.database.models.posts import PostRedeSocial
from src.database.tipos_base.database import Database
from google.genai import types

from src.settings import DEBUG


class PrevisaoDoTempoTool(BaseTool):

    @property
    def function_declaration(self):
        return self.get_weather_forecast

    def get_weather_forecast(self, cidade:str) -> dict:
        """
        Get the weather forecast for a given city for the next 5 days.
        :param cidade:
        :return: dict - A dictionary containing the weather forecast.
        """

        try:
            return {'output': get_previsao_de_chuva(cidade)}
        except Exception as e:
            if DEBUG:
                raise
            return {'error': str(e)}


    def get_result_as_part(self, result: dict) -> types.Part:
        return types.Part.from_function_response(
            name=self.function_name,
            response=result
        )

    def call_chat_display(self) -> str:
        return "Obtendo previsão do tempo..."

    def call_result_display(self, result) -> str:

        if 'error' in result:
            return 'Erro ao obter a previsão do tempo: ' + result['error']


        return "Previsão do tempo obtida com sucesso para a cidade solicitada."