from datetime import datetime

from src.large_language_model.tipos_base.base_tools import BaseTool


class EnchenteTool(BaseTool):

    @property
    def function_declaration(self):
        return self.prever_enchente_proximos_dias

    def prever_enchente_proximos_dias(self):
        """
        Preview if there will be a flooding in the next 7 days
        """

        print("Chamou função previsão de enchente")

        return {
            'flood': True,
            'info': "WARNING, FLOOD COMMING IN THE NEXT FEW DAYS"
        }

    def call_chat_display(self) -> str:
        return "Fazendo a previsão de enchentes"

    def call_result_display(self, result: dict) -> str:
        """
        result {
            "output": dados
        }
        """

        return "Previsão obtida com sucesso"