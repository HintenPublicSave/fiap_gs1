import logging

from src.database.tipos_base.model import Model

# Importe manualmente as classes Model dos arquivos referenciados
from src.database.models.files_database import Arquivo
from src.database.models.posts import PostRedeSocial
from src.database.models.sensor import TipoSensor, Sensor, LeituraSensor

def import_models(sort: bool = False) -> dict[str, type[Model]]:
    """
    Importa diretamente todas as classes que herdam de Model
    nos arquivos referenciados.
    :return: dict - Um dicionário com o nome das classes como chave e as classes como valor.
    """
    models = {
        'Arquivo': Arquivo,
        'PostRedeSocial': PostRedeSocial,
        'TipoSensor': TipoSensor,
        'Sensor': Sensor,
        'LeituraSensor': LeituraSensor,
    }

    if sort:
        models = dict(sorted(models.items(), key=lambda item: getattr(item[1], '__database_import_order__', 0)))

    return models

def get_model_by_name(name: str) -> type[Model]:
    """
    Retorna a classe do modelo baseado no nome.
    :param name: Nome do modelo.
    :return: Model - Classe do modelo.
    """
    models = import_models()
    model_class = models.get(name)
    if model_class:
        return model_class
    else:
        raise ValueError(f"Model '{name}' não encontrado.")

def get_model_by_table_name(table_name: str) -> type[Model]:
    """
    Retorna a classe do modelo baseado no nome da tabela.
    :param table_name: Nome da tabela.
    :return: Model - Classe do modelo.
    """
    models = import_models()
    for model_class in models.values():
        if getattr(model_class, '__tablename__', None) == table_name:
            return model_class
    raise ValueError(f"Model com tabela '{table_name}' não encontrado.")

if __name__ == "__main__":
    models = import_models()
    for name, model in models.items():
        print(f"Modelo: {name}, Classe: {model}")
