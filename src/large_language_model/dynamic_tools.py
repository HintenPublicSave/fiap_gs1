from src.large_language_model.tipos_base.base_tools import BaseTool

# Importações diretas das ferramentas
from src.large_language_model.tools.datetime_tool import DateTimeTool
from src.large_language_model.tools.image_tool import ImageGenerationTool
from src.large_language_model.tools.previsao_de_enchentes import EnchenteTool
from src.large_language_model.tools.previsao_do_tempo_tool import PrevisaoDoTempoTool
from src.large_language_model.tools.save_post_tool import SavePostTool

def import_tools(sort: bool = False) -> dict[str, type[BaseTool]]:
    """
    Importa diretamente todas as classes que herdam de BaseTool
    nos arquivos referenciados.
    :return: dict - Um dicionário com o nome das classes como chave e as classes como valor.
    """
    tools = {
        'DateTimeTool': DateTimeTool,
        'ImageGenerationTool': ImageGenerationTool,
        'EnchenteTool': EnchenteTool,
        'PrevisaoDoTempoTool': PrevisaoDoTempoTool,
        'SavePostTool': SavePostTool,
    }

    if sort:
        tools = dict(sorted(tools.items(), key=lambda item: item[0].lower()))

    return tools

def get_tool_by_name(name: str) -> type[BaseTool]:
    """
    Retorna a classe da ferramenta baseada no nome.
    :param name: Nome da ferramenta.
    :return: BaseTool - Classe da ferramenta.
    """
    tools = import_tools()
    tool_class = tools.get(name)
    if tool_class:
        return tool_class
    else:
        raise ValueError(f"Tool '{name}' não encontrada.")
