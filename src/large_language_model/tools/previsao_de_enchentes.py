from src.large_language_model.tipos_base.base_tools import BaseTool
from src.modelo_preditivo.realizar_previsao_func_full import realizar_previsao_func_full
from datetime import datetime, timedelta


class EnchenteTool(BaseTool):

    @property
    def function_declaration(self):

        return self.prever_enchente_proximos_dias

    def prever_enchente_proximos_dias(self, cidade: str):
        """
        Predicts the risk of heavy rainfall that may lead to flooding in a city over the next 5 days.
        Parameter:
            cidade (str): The name of the city for which to obtain the forecast. E.g.: 'São Paulo'
        """

        hoje = datetime.now() + timedelta(days=1)  # Começa a previsão a partir de amanhã

        try:
            previsao = realizar_previsao_func_full(cidade, dia=hoje.day, mes=hoje.month)

            return {
                "previsao": previsao,
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
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