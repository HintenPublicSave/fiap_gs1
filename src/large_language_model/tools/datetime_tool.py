from datetime import datetime

from src.large_language_model.tipos_base.base_tools import BaseTool


def get_current_time() -> str:
    """
    Retorna a data e hora atual no formato YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM.
    :return: String representando a data e hora atual.
    """
    return datetime.now().isoformat()

class DateTimeTool(BaseTool):

    @property
    def function_declaration(self):
        return get_current_time

    def execute(self, *args, **kwargs) -> str:
        return get_current_time()

    def call_chat_display(self) -> str:
        return "Obtendo data e hora atual."

    def call_result_display(self, result: str) -> str:
        return "Obtida data e hora atual"