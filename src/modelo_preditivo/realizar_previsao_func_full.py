import os
from src.modelo_preditivo.realizar_previsao_func import carregar_modelo_e_realizar_previsao
from src.api_metereologica.api import get_previsao_de_chuva
from src.database.models.sensor import Sensor, LeituraSensor, TipoSensor, TipoSensorEnum
from pprint import pprint


def realizar_previsao_func_full(
        cidade: str,
        dia: int,
        mes: int,
    ) -> str:
    previsao_chuva = get_previsao_de_chuva(cidade)

    primeira_chave, primeiro_valor = next(iter(previsao_chuva.items()))

    pprint(previsao_chuva)

    print(primeira_chave, primeiro_valor)

    chuva_mm = primeiro_valor['chuva_mm']

    tipo = TipoSensor.first(filters=[
        TipoSensor.tipo == TipoSensorEnum.LEITO
    ])

    print(tipo)

    sensor = Sensor.first(filters=[
        Sensor.tipo_sensor_id == tipo.id
    ])

    print(sensor)

    leitura = LeituraSensor.first(filters=[
        LeituraSensor.sensor_id == sensor.id
    ], order_by=[
        LeituraSensor.data_leitura.desc()
    ])

    print(leitura.valor)

    cota = float(leitura.valor)

    modelo_path = os.path.join(
        os.path.dirname(__file__),
        "modelos_salvos",
    )

    # checa se o arquivo do modelo existe
    if not os.path.exists(modelo_path):
        raise FileNotFoundError(f"Modelo não encontrado no caminho: {modelo_path}")

    modelo_completo_path = None

    # interar sobre os arquivos no diretório
    for arquivo in os.listdir(modelo_path):
        if arquivo.endswith(".pkl"):
            modelo_completo_path = os.path.join(modelo_path, arquivo)
            break

    if modelo_completo_path is None:
        raise FileNotFoundError("Nenhum modelo .pkl encontrado no diretório de modelos.")

    retornor = carregar_modelo_e_realizar_previsao(modelo_completo_path,
                                                   dia=dia,
                                                   mes=mes,
                                                   cota=cota,
                                                   chuva=chuva_mm)

    print(retornor)

    return retornor


if __name__ == "__main__":
    from dotenv import load_dotenv
    from src.database.tipos_base.database import Database

    load_dotenv('../../.env')

    Database.init_sqlite('../../database.db')


    resultado = realizar_previsao_func_full("São Paulo", 15, 8)
